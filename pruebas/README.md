# Pruebas automáticas

Necesitan Python 3 con Playwright:

```
pip install playwright
playwright install chromium
```

Se corren desde la carpeta del juego:

| Prueba | Qué revisa |
| --- | --- |
| `python3 pruebas/tamanos.py` | 15 tamaños de pantalla (compu, tablet y celulares parados y acostados): que nada se encime, se corte ni haya que deslizar, en el menú, los ajustes, la ayuda, la Pastelería, los logros, el ranking, las novedades, los dulces, ¡Una más! y la pantalla de Dina. Las capturas quedan en `pruebas/capturas/`. |
| `python3 pruebas/juego.py` | Compras, cosméticos, habilidades, corazones, escudo doble, dulces (en qué metros salen), Halloween y su ajuste. |
| `python3 pruebas/simular.py 40` | Juega solo 40 partidas por perfil (novata, normal, buena, experta y experta con todo comprado) y resume metros, frutillas, minutos y dulces. Sirve para ajustar la dificultad y los precios. |

`simular.py` acepta cambios de equilibrio para probar sin tocar el código, por ejemplo:

```
python3 pruebas/simular.py 30 '{"slowGain": 0.5, "gapMin": 0.7}'
```

Los valores que se pueden cambiar están en `BAL` dentro de `index.html`.

El juego tiene un acceso para pruebas que solo se activa con `#prueba` al final de la dirección (`window.TR`). Sin eso no cambia nada.
