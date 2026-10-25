"""Simula muchas partidas con jugadores automáticos de distinta habilidad y resume los resultados.

Uso:  python3 pruebas/simular.py [partidas_por_perfil]
Necesita Python con Playwright (pip install playwright && playwright install chromium).
"""
import subprocess, time, sys, os, json, statistics as st
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
BAL = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
PORT = 8790

# sd: error de tiempo en cuadros (1/60 s); miss: probabilidad de no saltar una torta
PERFILES = {
    'novata':  dict(sd=7,   miss=.05),
    'normal':  dict(sd=4.5, miss=.02),
    'buena':   dict(sd=3,   miss=.008),
    'experta': dict(sd=1.8, miss=.002),
    'experta + todo': dict(sd=1.8, miss=.002, char='cinthia', pay=True,
                            up={'iman': 4, 'escudo': 4, 'pan': 4, 'dina': 4}),
}

def pct(v, p):
    v = sorted(v); return v[min(len(v) - 1, int(len(v) * p))]

def main():
    srv = subprocess.Popen(['python3', '-m', 'http.server', str(PORT)], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    out = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={'width': 1100, 'height': 720})
            pg.goto(f'http://localhost:{PORT}/index.html#prueba'); pg.wait_for_timeout(1500)
            if BAL: pg.evaluate('b=>Object.assign(TR.BAL,b)', BAL)
            for name, cfg in PERFILES.items():
                rs = []
                for i in range(N):
                    rs.append(pg.evaluate('c=>TR.simRun(c)', dict(cfg, max=216000)))
                m = [r['m'] for r in rs]; f = [r['fru'] for r in rs]; mins = [r['min'] for r in rs]
                out[name] = dict(
                    metros_mediana=st.median(m), metros_p10=pct(m, .1), metros_p90=pct(m, .9),
                    frutillas_mediana=st.median(f), frutillas_p90=pct(f, .9),
                    minutos_mediana=st.median(mins), dulces_mediana=st.median([r['cards'] for r in rs]),
                    llegaron_al_tope=sum(r['timeout'] for r in rs))
                o = out[name]
                print(f"{name:16} metros {o['metros_p10']:>6}/{o['metros_mediana']:>7.0f}/{o['metros_p90']:>6} "
                      f"(p10/mediana/p90) · frutillas {o['frutillas_mediana']:>6.0f} (p90 {o['frutillas_p90']}) · "
                      f"{o['minutos_mediana']} min · dulces {o['dulces_mediana']} · sin morir en 60 min: {o['llegaron_al_tope']}/{N}",
                      flush=True)
            b.close()
    finally:
        srv.terminate()
    return out

if __name__ == '__main__':
    main()
