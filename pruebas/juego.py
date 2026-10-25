import subprocess, time, os
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(ROOT,'pruebas','capturas'); os.makedirs(OUT,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8772'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
errors,ok=[],[]
def check(c,m):(ok if c else errors).append(m);print(('OK   ' if c else 'FAIL ')+m)
TIPS={'practica':1,'jump':1,'doble':1,'pan':1,'kamp_iman':1,'kamp_doble':1,'kamp_escudo':1,'dina':1,'dinaOver':1,'dulces':1}
def seed(pg,d):
    base={'seenVersion':'0.6','tips':TIPS};base.update(d)
    pg.evaluate("d=>localStorage.setItem('sofiRunner.v1',JSON.stringify(d))",base);pg.reload();pg.wait_for_timeout(1000)
try:
  with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':720})
    pg.on('pageerror',lambda e:errors.append('error js: '+str(e)))
    pg.goto('http://localhost:8772/index.html#prueba');pg.wait_for_timeout(200)
    # migración de 0.2: outfits que ya tenía por frutillas juntadas
    seed(pg,{'total':100,'owned':['sofi'],'outfit':'corona'})
    sv=pg.evaluate('TR.save')
    check(set(sv['cosm'])>={'default','none','hoodie','corazon','corona'} and sv['outfit']=='corona','al venir de la 0.2 se conservan los outfits que tenía')
    seed(pg,{'total':800,'spent':0,'owned':['sofi'],'cosm':['default','none']})
    check('Sin accesorio' in pg.inner_text('#accVal') and 'Sin confeti' in pg.inner_text('#trailVal'),'arranca sin accesorio ni confeti')
    pg.click('#accNext');pg.wait_for_timeout(200)
    check('Corazón' in pg.inner_text('#accVal') and pg.is_visible('#accAct .cBuy') and pg.evaluate('TR.save.outfit')=='default','mirar el Corazón: botón de compra, sin ponérselo todavía')
    pg.click('#trailNext');pg.wait_for_timeout(700)
    pg.screenshot(path=f'{OUT}/01_preview.png')
    px=pg.evaluate("""(()=>{const c=document.getElementById('prevCv');const x=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<x.length;i+=16)if(x[i+3]>0)n++;return n})()""")
    check(px>500,'la vista previa dibuja al personaje con accesorio y confeti')
    pg.click('#trailAct .cBuy');pg.wait_for_timeout(200)
    sv=pg.evaluate('TR.save')
    check('rosa' in sv['cosm'] and sv['trail']=='rosa' and sv['spent']==120,'comprar Confeti rosa: 120 gastadas y puesto')
    pg.click('#accAct .cBuy');pg.wait_for_timeout(200)
    sv=pg.evaluate('TR.save')
    check(sv['outfit']=='corazon' and sv['spent']==270,'comprar Corazón: puesto')
    # hoodie solo con Sofi
    names=[]
    for _ in range(4): pg.click('#accNext');pg.wait_for_timeout(80);names.append(pg.inner_text('#accVal'))
    check(any('Hoodie' in n for n in names),'con Sofi aparece el hoodie')
    seed(pg,{'total':3000,'owned':['sofi','deisy','leandro','nora','cinthia'],'cosm':['default','none','hoodie'],'outfit':'hoodie','char':'deisy'})
    names=[]
    for _ in range(4): pg.click('#accNext');pg.wait_for_timeout(80);names.append(pg.inner_text('#accVal'))
    check(not any('Hoodie' in n for n in names),'con Deisy el hoodie no aparece')
    # ---------- juego ----------
    def run(ch,extra={}):
        d={'total':3000,'owned':['sofi','deisy','leandro','nora','cinthia'],'char':ch,'cosm':['default','none','rosa'],'trail':'rosa'};d.update(extra);seed(pg,d)
        pg.click('#playBtn');pg.wait_for_timeout(250);pg.evaluate('TR.hold()')
    run('cinthia')
    check(pg.evaluate('TR.hearts')==1 and pg.is_visible('#hHeart') and pg.evaluate('TR.pow.type')=='','Cinthia arranca con un corazón (y sin escudo)')
    pg.wait_for_timeout(300);pg.screenshot(path=f'{OUT}/02_corazon.png')
    pg.evaluate('TR.cake(80)');pg.wait_for_timeout(900)
    check(pg.evaluate('TR.hearts')==0 and pg.evaluate('TR.dina.stage')==0 and not pg.is_visible('#hHeart'),'el choque gasta el corazón y Dina no aparece')
    run('sofi')
    pg.evaluate('TR.setDist(800)');pg.evaluate('TR.cake(80)');pg.wait_for_timeout(900)
    check(pg.evaluate('TR.dina.calm')<=420 and pg.evaluate('TR.dina.calm')>330,f"Sofi: Dina se cansa 2 s antes (calma {pg.evaluate('TR.dina.calm')})")
    check(pg.evaluate('TR.speed')<7.5,'Sofi ya no corre más rápido')
    # escudo de 2 choques visible
    run('deisy',{'up':{'escudo':4}})
    pg.evaluate("TR.power('escudo')");pg.wait_for_timeout(200)
    check(pg.inner_text('#hPowEm')=='🛡️×2','escudo al máximo: el marcador dice 🛡️×2')
    pg.screenshot(path=f'{OUT}/03_escudo2.png')
    pg.evaluate('TR.cake(80)');pg.wait_for_timeout(900)
    check(pg.inner_text('#hPowEm')=='🛡️' and pg.evaluate('TR.pow.hits')==1,'después de un choque queda un anillo (🛡️)')
    # dulces: 1000, 2500, 4500
    run('sofi')
    pg.evaluate('TR.setDist(990)');pg.wait_for_timeout(200)
    check(pg.evaluate('TR.state')=='playing','a los 990 m todavía no hay dulce')
    pg.wait_for_timeout(500)
    check(pg.evaluate('TR.state')=='cards','a los 1000 m aparece el primer dulce')
    pg.wait_for_timeout(500);pg.evaluate('TR.pick(0)');pg.wait_for_timeout(100)
    pg.evaluate('TR.setDist(1980)');pg.wait_for_timeout(200)
    check(pg.evaluate('TR.state')=='playing','a los 1980 m todavía no')
    pg.wait_for_timeout(700)
    check(pg.evaluate('TR.state')=='cards','a los 2000 m el segundo')
    pg.wait_for_timeout(500);pg.evaluate('TR.pick(0)');pg.wait_for_timeout(100)
    pg.evaluate('TR.setDist(3000)');pg.wait_for_timeout(300)
    check(pg.evaluate('TR.state')=='playing','a los 3000 m no hay dulce (es de noche: el tercero sale al amanecer, a los 4000)')
    pg.evaluate('TR.setDist(3990)');pg.wait_for_timeout(500)
    check(pg.evaluate('TR.state')=='cards','a los 4000 m (amanecer) el tercero')
    # corazón extra como dulce
    run('sofi')
    pg.evaluate('TR.D.corazon=0');pg.evaluate('TR.setNextCard(0)');pg.wait_for_timeout(600)
    opts=pg.locator('.dulce .dt').all_inner_texts()
    check(not any('Curita' in o for o in opts),'ya no hay curita')
    # halloween: se prende con la temporada y se apaga en ajustes
    seed(pg,{'total':800})
    pg.evaluate("TR.setSeason('halloween')");pg.wait_for_timeout(200)
    check(pg.evaluate("document.body.dataset.season")=='halloween','en temporada se ve Halloween')
    names=[]
    for _ in range(5): pg.click('#accNext');pg.wait_for_timeout(60);names.append(pg.inner_text('#accVal'))
    check(any('bruja' in n for n in names),'en Halloween se puede comprar el sombrero de bruja')
    pg.click('#setBtn');pg.click('#setSeason');pg.wait_for_timeout(150)
    check(pg.evaluate("document.body.dataset.season")=='' and not pg.evaluate('TR.save.set.seasonal'),'Ajustes: apagar los temas de temporada')
    pg.click('#setBack')
    names=[]
    for _ in range(5): pg.click('#accNext');pg.wait_for_timeout(60);names.append(pg.inner_text('#accVal'))
    check(not any('bruja' in n for n in names),'con el tema apagado no aparece el sombrero (si no lo compraste)')
    pg.evaluate("TR.setSeason('')")
    # confeti en partida
    pg.evaluate("TR.pick(0)");pg.wait_for_timeout(800)
    pg.screenshot(path=f'{OUT}/04_confeti.png')
    b.close()
finally: srv.terminate()
print('\n',len(ok),'bien,',len(errors),'problemas')
for e in errors: print(' -',e)
