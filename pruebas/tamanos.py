import subprocess, time, os, sys
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(ROOT,'pruebas','capturas'); os.makedirs(OUT,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8771'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
SIZES=[(1920,1080,0),(1366,768,0),(1280,600,0),(1024,768,0),(768,1024,1),(820,1180,1),(412,915,1),(390,844,1),(360,640,1),(320,568,1),(915,412,1),(844,390,1),(740,360,1),(640,360,1),(568,320,1)]
MENU='''(()=>{const B=e=>{const r=e.getBoundingClientRect();return {t:r.top,b:r.bottom,l:r.left,r:r.right,w:r.width,h:r.height}};
const q=s=>document.querySelector(s);const m=q('#menu');const M=B(m);const P=[];
const vis=e=>e&&!e.hidden&&e.offsetParent!==null;
const blocks=[['barra','.mBar'],['desafío','#retoPill'],['carrusel','.carousel'],['info','#carInfo'],['cosméticos','.cosm'],['botones','.mGo']].map(([n,s])=>[n,q(s)]).filter(x=>vis(x[1])).map(([n,e])=>[n,B(e)]);
for(const [n,r] of blocks){ if(r.t<M.t-1||r.b>M.b+1) P.push(`${n} fuera de la pantalla (${Math.round(r.t)}..${Math.round(r.b)} de ${Math.round(M.t)}..${Math.round(M.b)})`);
  if(r.l<M.l-1||r.r>M.r+1) P.push(`${n} se sale de costado`);}
for(let i=0;i<blocks.length;i++)for(let j=i+1;j<blocks.length;j++){const [a,A]=blocks[i],[b,Bb]=blocks[j];
  const ov=Math.min(A.b,Bb.b)-Math.max(A.t,Bb.t),oh=Math.min(A.r,Bb.r)-Math.max(A.l,Bb.l);if(ov>2&&oh>2)P.push(`${a} se encima con ${b} (${Math.round(ov)}px)`)}
const tr=B(q('#carTrack')),c=q('.carItem.center');if(c){const r=B(c);if(r.t<tr.t-1||r.b>tr.b+1||r.l<tr.l-1||r.r>tr.r+1)P.push('la tarjeta del centro se corta');
  if(r.h<70)P.push('tarjeta del centro muy chica ('+Math.round(r.h)+'px)')}
if(m.scrollHeight>m.clientHeight+1)P.push('el menú desliza '+(m.scrollHeight-m.clientHeight)+'px');
for(const e of document.querySelectorAll('.abDesc,.ability,.cNm,.carName,#retoPill .x,.mBar .pill')) if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).textOverflow!=='ellipsis')P.push('texto cortado: '+e.textContent.slice(0,30));
for(const e of document.querySelectorAll('.mBar .ibtn')){const r=B(e);if(r.r>M.r+1)P.push('ícono fuera: '+e.textContent)}
if(document.documentElement.scrollWidth>innerWidth)P.push('desborde horizontal de la página');
const btns=[...document.querySelectorAll('.mBar .ibtn')].map(B);for(let i=1;i<btns.length;i++){if(Math.abs(btns[i].t-btns[0].t)>2)P.push('íconos en dos filas');break}
return P})()'''
FIT='''(s=>{const e=document.querySelector(s);const r=e.getBoundingClientRect();const o=e.closest('.overlay')||document.body;const R=o.getBoundingClientRect();
 const P=[];if(r.top<R.top-1||r.bottom>R.bottom+1)P.push(`${s} no entra (${Math.round(r.top)}..${Math.round(r.bottom)} de ${Math.round(R.height)})`);if(r.left<R.left-1||r.right>R.right+1)P.push(s+' se sale de costado');return P})'''
TIPS={'practica':1,'jump':1,'doble':1,'pan':1,'kamp_iman':1,'kamp_doble':1,'kamp_escudo':1,'dina':1,'dinaOver':1,'dulces':1}
tot=0
try:
  with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h,mob in SIZES:
      pg=b.new_page(viewport={'width':w,'height':h},is_mobile=bool(mob),has_touch=bool(mob),device_scale_factor=2 if mob else 1)
      errs=[];pg.on('pageerror',lambda e:errs.append('error js: '+str(e)))
      pg.goto('http://localhost:8771/index.html#prueba');pg.wait_for_timeout(150)
      pg.evaluate("d=>localStorage.setItem('sofiRunner.v1',JSON.stringify(d))",{'total':900,'spent':0,'seenVersion':'0.6','tips':TIPS,'ach':{'primera':1}})
      pg.reload();pg.wait_for_timeout(900);pg.evaluate("TR.setSeason('halloween')");pg.wait_for_timeout(150) # con Halloween: botón y pantalla del pase
      probs=pg.evaluate(MENU)
      pg.screenshot(path=f'{OUT}/{w}x{h}_menu.png')
      # con un personaje bloqueado al centro (botón Comprar) y un cosmético sin comprar
      pg.click('#carNext');pg.click('#accNext');pg.click('#trailNext');pg.wait_for_timeout(500)
      probs+=['[bloqueado] '+x for x in pg.evaluate(MENU)]
      pg.screenshot(path=f'{OUT}/{w}x{h}_menu2.png')
      for ov,sel in [('#settings','#settings .goCard'),('#help','#help .goCard'),('#shop','#shop .goCard'),('#news','#news .goCard'),('#ach','#ach .goCard'),('#rank','#rank .goCard'),('#pass','#pass .goCard')]:
        pg.evaluate("TR.openPass()" if ov=='#pass' else f"document.querySelector('{ov}').hidden=false");pg.wait_for_timeout(150)
        probs+=pg.evaluate(FIT,sel)
        # nada del menú puede quedar por encima de la ventana: se mira qué elemento está arriba en varios puntos
        probs+=pg.evaluate('''(o=>{const ov=document.querySelector(o),r=ov.getBoundingClientRect(),P=[];
          for(let i=1;i<8;i++)for(let j=1;j<8;j++){const x=r.left+r.width*i/8,y=r.top+r.height*j/8,e=document.elementFromPoint(x,y);
            if(e&&!ov.contains(e)){P.push(o+' tapado por '+(e.id||e.className||e.tagName));return P}}return P})''',ov)
        pg.evaluate(f"document.querySelector('{ov}').hidden=true")
      pg.evaluate("document.getElementById('playBtn').click()");pg.wait_for_timeout(300);pg.evaluate('TR.hold()')
      pg.evaluate('TR.setNextCard(0)');pg.wait_for_timeout(700);probs+=pg.evaluate(FIT,'.cardsBox')
      for _ in range(6): # varias tandas de dulces al azar
        probs+=pg.evaluate('''(()=>{const P=[];for(const c of document.querySelectorAll('.dulce')){const r=c.getBoundingClientRect();for(const e of c.querySelectorAll('.fx,.dt')){const q=e.getBoundingClientRect();if(q.left<r.left-1||q.right>r.right+1)P.push('dulce: se sale '+e.textContent)}}return P})()''')
        pg.evaluate("TR.cards()");pg.wait_for_timeout(80)
      pg.screenshot(path=f'{OUT}/{w}x{h}_dulces.png')
      pg.wait_for_timeout(500); pg.evaluate("TR.pick(0)"); pg.wait_for_timeout(200); pg.evaluate("TR.D.triple=0; TR.D.corazon=0; TR.hearts=0"); pg.evaluate("TR.power(\"iman\")")
      pg.evaluate('TR.got=100');pg.evaluate('TR.cake(80)');pg.wait_for_timeout(900);pg.evaluate('TR.cake(80)');pg.wait_for_timeout(900)
      if pg.evaluate('TR.state')=='offer': probs+=pg.evaluate(FIT,'#offer .goCard')
      else: probs.append('no apareció ¡Una más! (estado '+pg.evaluate('TR.state')+')')
      pg.evaluate("document.getElementById('offerNo').click()");pg.wait_for_timeout(1500)
      probs+=pg.evaluate(FIT,'#overCard')
      pg.screenshot(path=f'{OUT}/{w}x{h}_dina.png')
      pg.evaluate('TR.openPass()');pg.wait_for_timeout(150);pg.screenshot(path=f'{OUT}/{w}x{h}_pase.png')
      probs+=errs
      tot+=len(probs)
      print(f'{w}x{h}:', 'ok' if not probs else '\n   - '+'\n   - '.join(probs))
      pg.close()
    b.close()
finally: srv.terminate()
print('TOTAL problemas:',tot)
