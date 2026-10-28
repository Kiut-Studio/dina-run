# Prueba de la nube (☁️ cuenta de Google) con una nube FALSA: cada "teléfono" es un navegador aparte y todos
# comparten este diccionario de Python en vez de Firebase. Copiada de la de Dina Beat (pruebas/nube.py).
# Revisa: que Dina Run escriba solo sus campos (run, runAt) sin borrar los de Dina Beat, que dos teléfonos se junten
# sin perder nada, que entre solo si ya entraste en Dina Beat, que las frutillas que suma Dina Beat en otra pestaña
# no se pisen, y que "Borrar mi progreso" con cuenta deje la nube a salvo.
import asyncio,json,os,subprocess,time,sys
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'pruebas','capturas');os.makedirs(OUT,exist_ok=True)
PORT=8773
NUBE={'jugadores/G1':{'beat':{'stars':[3,1,0],'best':[9000,0,0]},'beatAt':1,'nombre':'Leandro','personaje':'sofi'}}
def mock(op,path,data):
  if op=='get': return NUBE.get(path)
  if op=='set':
    d=json.loads(json.dumps(data['d']))
    if data.get('f') and isinstance(NUBE.get(path),dict): NUBE[path]={**NUBE[path],**{k:d[k] for k in data['f']}}
    else: NUBE[path]=d
    return True
  return None
MOCK='''window.CLOUD_MOCK={
  onUser:cb=>{cb(JSON.parse(localStorage.getItem('mockUser')||'null'))},
  google:async()=>{const u={uid:window.MOCK_UID,anon:false,name:'Leandro Casco',email:'leandro@ejemplo.com',photo:''};localStorage.setItem('mockUser',JSON.stringify(u));return u},
  out:async()=>{localStorage.removeItem('mockUser')},
  get:p=>window.mockCloud('get',p,null),set:(p,d,f)=>window.mockCloud('set',p,{d,f:f||null})};'''
TIPS={'practica':1,'jump':1,'doble':1,'pan':1,'kamp_iman':1,'kamp_doble':1,'kamp_escudo':1,'dina':1,'dinaOver':1,'dulces':1}
fallas=[]
def check(ok,txt):
  print(('✔️ ' if ok else '❌ ')+txt)
  if not ok: fallas.append(txt)
async def phone(b,uid,errs,save=None,extra=None):
  ctx=await b.new_context(viewport={'width':390,'height':844})
  await ctx.expose_function('mockCloud',mock)
  await ctx.add_init_script(f"window.MOCK_UID={json.dumps(uid)};"+MOCK)
  pg=await ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.goto(f'http://localhost:{PORT}/index.html#prueba');await pg.wait_for_timeout(200)
  if save is not None or extra:
    await pg.evaluate('([s,x])=>{if(s)localStorage.setItem("sofiRunner.v1",JSON.stringify(s));for(const k in x||{})localStorage.setItem(k,typeof x[k]==="string"?x[k]:JSON.stringify(x[k]))}',[save,extra or {}])
    await pg.reload()
  await pg.wait_for_timeout(700);return ctx,pg
async def main():
  srv=subprocess.Popen([sys.executable,'-m','http.server',str(PORT)],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
  try:
   async with async_playwright() as p:
    b=await p.chromium.launch();errs=[]
    # 📱 A: tiene progreso, entra con Google desde el botón ☁️ del menú
    A0={'total':900,'spent':500,'owned':['sofi','deisy'],'cosm':['default','none','corazon'],'best':1200,'char':'deisy','outfit':'corazon',
        'ach':{'primera':111},'tips':TIPS,'seenVersion':'9.9','muted':True,'set':{'music':40},'name':'Leandro','mod':1000,
        'runs':[{'nombre':'Leandro','metros':1200,'personaje':'deisy'}]}
    ca,a=await phone(b,'G1',errs,A0)
    check(await a.evaluate('document.getElementById("acctBtn").textContent')=='☁️Entrar','botón "☁️ Entrar" en el menú (en pantallas angostas, solo ☁️)')
    await a.click('#acctBtn');await a.wait_for_timeout(300)
    await a.screenshot(path=OUT+'/nube_entrar.png')
    await a.click('#gIn');await a.wait_for_timeout(1200)
    d=NUBE.get('jugadores/G1',{})
    check('run' in d and d['run'].get('total')==900,'A entra: su progreso sube a la nube (900 🍓)')
    check(d.get('beat',{}).get('stars')==[3,1,0] and d.get('nombre')=='Leandro','los campos de Dina Beat siguen intactos')
    check(all(k not in d['run'] for k in ['muted','set','seenVersion']),'lo propio del teléfono (sonido, ajustes, novedades vistas) no sube')
    await a.screenshot(path=OUT+'/nube_cuenta.png')
    check(await a.evaluate('document.getElementById("acctBtn").classList.contains("in")'),'el botón del menú muestra la cuenta')
    # 📱 B: otro teléfono con otro progreso; entra desde ⚙️ Ajustes
    B0={'total':300,'spent':0,'owned':['sofi','nora'],'cosm':['default','none','corona'],'best':3000,'char':'nora','outfit':'corona','up':{'iman':2},
        'ach':{'primera':50,'mil':60},'tips':TIPS,'seenVersion':'9.9','set':{'music':80},'mod':5000,
        'pass':{'key':'halloween-2026','m':4000,'got':[0,1],'day':'x','dm':100},'dinaLooks':['bruja'],
        'runs':[{'nombre':'Sofi','metros':3000,'personaje':'nora'}]}
    cb_,bb=await phone(b,'G1',errs,B0)
    await bb.click('#setBtn');await bb.wait_for_timeout(200);await bb.click('#acctSet');await bb.wait_for_timeout(300);await bb.click('#gIn');await bb.wait_for_timeout(1200)
    s=await bb.evaluate('TR.save')
    check(s['total']==900 and s['spent']==500,f"B se junta: frutillas {s['total']}−{s['spent']} (lo mejor de cada uno)")
    check(set(s['owned'])=={'sofi','deisy','nora'} and {'corazon','corona'}<=set(s['cosm']),f"personajes y cosméticos juntados: {s['owned']}")
    check(s['best']==3000 and s['up'].get('iman')==2 and s['ach'].get('primera')==50 and 'mil' in s['ach'],'récord, mejoras y logros juntados')
    check(s['pass']['m']==4000 and s['dinaLooks']==['bruja'],'pase y disfraces de Dina juntados')
    check(s['char']=='nora' and s['outfit']=='corona','personaje y accesorio: los del guardado más nuevo (B)')
    check(s['set']['music']==80,'B conserva sus propios ajustes')
    check(sorted(r['nombre'] for r in s['runs'])==['Leandro','Sofi'],'ranking de este aparato juntado')
    d=NUBE['jugadores/G1']['run'];check(d['best']==3000 and d['total']==900,'la nube queda con lo juntado')
    # 📱 A sincroniza y recibe lo de B
    await a.evaluate('TR.cloudSyncAll()');await a.wait_for_timeout(800)
    s=await a.evaluate('TR.save')
    check(s['best']==3000 and 'nora' in s['owned'] and s['set']['music']==40 and s['muted']==True,'A recibe lo de B y conserva su sonido y ajustes')
    # 🐱 Dina Beat suma frutillas en otra pestaña (sin cambiar la fecha del guardado) mientras A juega
    a2=await ca.new_page();await a2.goto(f'http://localhost:{PORT}/index.html');await a2.wait_for_timeout(300)
    await a.evaluate("document.getElementById('playBtn').click()");await a.wait_for_timeout(300)
    await a2.evaluate('()=>{const k="sofiRunner.v1",s=JSON.parse(localStorage.getItem(k));s.total+=37;localStorage.setItem(k,JSON.stringify(s))}')
    await a.wait_for_timeout(300)
    mid=await a.evaluate('TR.save.total')
    await a.evaluate('TR.got=12');await a.evaluate('TR.die()');await a.wait_for_timeout(2500)
    s=await a.evaluate('TR.save');got=await a.evaluate('TR.got')
    check(mid==900 and s['total']==900+37+got,f"frutillas de Dina Beat: se suman al terminar la partida (900 + 37 + {got} de la partida = {s['total']})")
    ls=await a.evaluate('JSON.parse(localStorage.getItem("sofiRunner.v1")).total')
    check(ls==s['total'],'y quedan guardadas en el teléfono')
    await a2.close()
    # 📱 C: ya entró en Dina Beat (misma sesión de Google en el sitio): Dina Run entra solo
    cc,c=await phone(b,'G1',errs,{'total':5,'tips':TIPS,'seenVersion':'9.9'},{'sofiSilbato.v1':{'cloud':1},'mockUser':{'uid':'G1','anon':False,'name':'Leandro Casco','email':'leandro@ejemplo.com','photo':''}})
    await c.wait_for_timeout(1800)
    s=await c.evaluate('TR.save')
    check(await c.evaluate('TR.cloud().google') and s['best']==3000 and s.get('cloud')==1,'si ya entraste en Dina Beat, Dina Run entra solo y trae tu progreso')
    # 🗑️ Borrar mi progreso con cuenta: sale de la cuenta, la nube queda igual
    antes=json.dumps(NUBE['jugadores/G1']['run'],sort_keys=True)
    await c.click('#setBtn');await c.wait_for_timeout(200);await c.click('#resetBtn');await c.click('#resetYes');await c.wait_for_timeout(4000)
    s=await c.evaluate('TR.save')
    check(s['total']==0 and not await c.evaluate('TR.cloud().google'),'borrar con cuenta: se borra del teléfono y sale de la cuenta')
    check(json.dumps(NUBE['jugadores/G1']['run'],sort_keys=True)==antes,'lo de la nube queda a salvo')
    check(not errs,'sin errores de JavaScript '+str(errs[:3]))
    await b.close()
  finally: srv.terminate()
  print('\nTOTAL fallas:',len(fallas))
asyncio.run(main())
