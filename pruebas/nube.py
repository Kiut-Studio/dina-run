# Prueba de la nube (☁️ cuenta de Google) con una nube FALSA: cada "teléfono" es un navegador aparte y todos
# comparten este diccionario de Python en vez de Firebase. Copiada de la de Dina Beat (pruebas/nube.py).
# Revisa: que Dina Run escriba solo sus campos (run, runAt) sin borrar los de Dina Beat, que dos teléfonos se junten
# sin perder nada, que entre solo si ya entraste en Dina Beat, que las frutillas que suma Dina Beat en otra pestaña
# no se pisen, que "Borrar mi progreso" con cuenta deje la nube a salvo, y el ranking de todos (0.9.1): primer nombre y
# foto de Google, quien no tiene cuenta lo ve pero no aparece, desafío de la semana y quién ganó la semana pasada.
import asyncio,json,os,subprocess,time,sys,datetime
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT=os.path.join(ROOT,'pruebas','capturas');os.makedirs(OUT,exist_ok=True)
PORT=8773
_hoy=datetime.date.today();_lun=_hoy-datetime.timedelta(days=_hoy.weekday())
SEM='S'+_lun.strftime('%Y-%m-%d');SEM_ANT='S'+(_lun-datetime.timedelta(days=7)).strftime('%Y-%m-%d')
NUBE={'semanas/'+SEM_ANT+'/filas/G2':{'n':'Sofía','f':'','c':'nora','v':30,'r':'x','at':1},
      'semanas/'+SEM_ANT+'/filas/G1':{'n':'Leandro','f':'','c':'sofi','v':10,'r':'x','at':1},'jugadores/G1':{'beat':{'stars':[3,1,0],'best':[9000,0,0]},'beatAt':1,'nombre':'Leandro','personaje':'sofi'}}
def mock(op,path,data):
  if op=='get': return NUBE.get(path)
  if op=='set':
    d=json.loads(json.dumps(data['d']))
    if data.get('f') and isinstance(NUBE.get(path),dict): NUBE[path]={**NUBE[path],**{k:d[k] for k in data['f']}}
    else: NUBE[path]=d
    return True
  pre=path+'/';kids=[(k[len(pre):],v) for k,v in NUBE.items() if k.startswith(pre) and '/' not in k[len(pre):]]
  if op=='top': return [{'id':k,'data':v} for k,v in sorted(kids,key=lambda x:-x[1].get(data['f'],0))[:data['n']]]
  if op=='above': return sum(1 for k,v in kids if v.get(data['f'],0)>data['v'])
  return None
MOCK='''window.CLOUD_MOCK={
  onUser:cb=>{cb(JSON.parse(localStorage.getItem('mockUser')||'null'))},
  google:async()=>{const u={uid:window.MOCK_UID,anon:false,name:window.MOCK_NAME||'Leandro Casco',email:'leandro@ejemplo.com',photo:window.MOCK_PHOTO||''};localStorage.setItem('mockUser',JSON.stringify(u));return u},
  anon:async()=>{const u={uid:'anon-'+Math.random().toString(36).slice(2,8),anon:true};localStorage.setItem('mockUser',JSON.stringify(u));return u},
  top:(p,f,n)=>window.mockCloud('top',p,{f,n}),above:(p,f,v)=>window.mockCloud('above',p,{f,v}),
  out:async()=>{localStorage.removeItem('mockUser')},
  get:p=>window.mockCloud('get',p,null),set:(p,d,f)=>window.mockCloud('set',p,{d,f:f||null})};'''
TIPS={'practica':1,'jump':1,'doble':1,'pan':1,'kamp_iman':1,'kamp_doble':1,'kamp_escudo':1,'dina':1,'dinaOver':1,'dulces':1}
fallas=[]
def check(ok,txt):
  print(('✔️ ' if ok else '❌ ')+txt)
  if not ok: fallas.append(txt)
async def phone(b,uid,errs,save=None,extra=None,name='Leandro Casco',photo=''):
  ctx=await b.new_context(viewport={'width':390,'height':844})
  await ctx.expose_function('mockCloud',mock)
  await ctx.add_init_script(f"window.MOCK_UID={json.dumps(uid)};window.MOCK_NAME={json.dumps(name)};window.MOCK_PHOTO={json.dumps(photo)};"+MOCK)
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
        'runs':[{'nombre':'Leandro','metros':1200,'personaje':'deisy'}],'avatars':{'leandro':'dina'}}
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
    check(all(k not in s for k in ['runs','name','avatars','wk']),'los datos del ranking viejo (nombre escrito, íconos) ya no están')
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
    # 🏆 ranking de todos
    r=NUBE.get('ranking/G1',{})
    check(r.get('n')=='Leandro' and r.get('m')==3000 and r.get('l',0)>=2,f"ranking: Leandro aparece con su primer nombre y su récord juntado ({r.get('n')}, {r.get('m')} m, {r.get('l')} logros)")
    cd_,dd=await phone(b,'G2',errs,{'total':50,'best':5000,'char':'nora','tips':TIPS,'seenVersion':'9.9','ach':{'primera':1}},name='Sofía Casco',photo='http://localhost:%d/assets/sofi.webp'%PORT)
    await dd.click('#acctBtn');await dd.wait_for_timeout(200);await dd.click('#gIn');await dd.wait_for_timeout(1500)
    r2=NUBE.get('ranking/G2',{})
    check(r2.get('n')=='Sofía' and 'sofi.webp' in r2.get('f','') and r2.get('m')==5000,'Sofía entra: aparece como "Sofía" (sin apellido) y con su foto')
    sd=await dd.evaluate('TR.save')
    check(sd.get('wins')==[SEM_ANT] and r2.get('g')==1,'Sofía ganó el desafío de la semana pasada: se le anota (🏆 1)')
    await a.evaluate("document.getElementById('menuBtn').click()");await a.wait_for_timeout(300)
    if await a.evaluate('!document.getElementById("acct").hidden'): await a.click('#acctBack');await a.wait_for_timeout(200)
    await a.click('#rankBtn');await a.wait_for_timeout(1200)
    filas=await a.evaluate('[...document.querySelectorAll("#rankList li")].map(l=>[l.className,l.textContent])')
    check(len(filas)>=2 and 'Sofía' in filas[0][1] and '👑' in filas[0][1] and 'Leandro' in filas[1][1] and 'me' in filas[1][0],f"A ve el ranking de todos: {[f[1][:40] for f in filas]}")
    check('Así aparecés' in await a.inner_text('#rkMe') and await a.inner_text('#rankMode')=='Récords de todos','abajo dice cómo aparecés (nombre y foto de Google)')
    await a.screenshot(path=OUT+'/nube_ranking.png')
    await a.click('#tabReto');await a.wait_for_timeout(200);await a.screenshot(path=OUT+'/nube_desafio.png');await a.click('#rankBack')
    # partida con cuenta: sube el desafío de la semana y muestra el puesto
    await a.evaluate("document.getElementById('playBtn').click()");await a.wait_for_timeout(300)
    await a.evaluate('TR.setDist(800);TR.got=20');await a.evaluate('TR.die()');await a.wait_for_timeout(2500)
    tag=await a.inner_text('#rankLine')
    check(tag.strip()=='🏆 #2' and await a.evaluate('document.getElementById("rankJoin").hidden'),f'al terminar la partida: puesto en el ranking ({tag})')
    sem=NUBE.get(f'semanas/{SEM}/filas/G1')
    check(sem is not None and sem.get('v',0)>0 and sem.get('n')=='Leandro',f'su partida cuenta para el desafío de la semana ({sem and sem.get("v")})')
    # 📱 E: sin cuenta. Ve el ranking, no aparece, y se le invita a entrar
    ce,e=await phone(b,'G7',errs,{'total':0,'best':9999,'tips':TIPS,'seenVersion':'9.9'})
    await e.click('#rankBtn');await e.wait_for_timeout(1200)
    fe=await e.evaluate('[...document.querySelectorAll("#rankList li")].map(l=>l.textContent)')
    check(len(fe)>=2 and 'Sofía' in fe[0] and await e.evaluate('!!document.getElementById("rkIn")'),'sin cuenta: ve el ranking y el botón "Entrar con Google"')
    await e.screenshot(path=OUT+'/nube_ranking_sin_cuenta.png');await e.click('#rankBack')
    await e.evaluate("document.getElementById('playBtn').click()");await e.wait_for_timeout(300)
    await e.evaluate('TR.setDist(900)');await e.evaluate('TR.die()');await e.wait_for_timeout(2500)
    check(not await e.evaluate('document.getElementById("rankJoin").hidden') and await e.evaluate('document.getElementById("rankLine").hidden'),'sin cuenta, al terminar: "☁️ Entrá con Google para aparecer en el ranking"')
    await e.screenshot(path=OUT+'/nube_fin_sin_cuenta.png')
    check(not any(k.startswith('ranking/anon') for k in NUBE) and not any('/filas/anon' in k for k in NUBE),'quien juega sin cuenta no aparece en el ranking')
    await e.click('#rankJoin');await e.wait_for_timeout(200);await e.click('#gIn');await e.wait_for_timeout(1500)
    await e.click('#acctBack');await e.wait_for_timeout(1200)
    check(NUBE.get('ranking/G7',{}).get('m')==9999 and 'G7' in json.dumps(NUBE.get(f'semanas/{SEM}/filas/G7',{})) or NUBE.get('ranking/G7',{}).get('m')==9999,'entra desde la pantalla final: su récord sube al ranking')
    check(not await e.evaluate('document.getElementById("rankLine").hidden'),'y ya ve su puesto')
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
