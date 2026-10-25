# Sofi Runner — contexto del proyecto

Documento para retomar el trabajo en cualquier conversación. Resume qué es el juego, cómo está hecho, qué se decidió y por qué, y qué sigue. Actualizarlo con cada versión.

Última actualización: 25/10/2026 · versión 0.6

## Qué es

*Infinite runner* de un solo toque, cute, con estética de juego flash de chicas de los 2000. Se corre, se juntan frutillas, se esquivan porciones de torta y, si chocás, la gata **Dina** te persigue. Las frutillas se gastan en personajes, cosméticos y mejoras.

- **Autor:** Leandro (programación con asistencia de IA).
- **Dibujos, personajes y animación:** **Sofía** (Sofi). Todos los dibujos son suyos y están © Sofía; ella aceptó reutilizarlos en este juego.
- **Personajes:** Sofi, Deisy, Leandro, Nora y Cinthia, más la gata Dina. Son la familia de Leandro.
- **Público:** cualquiera (amigos de la familia que lo probaron y les gustó). Se piensa a futuro en Play Store.

## De dónde viene

Es un desprendimiento de **Torta Runner** (`LeandroACasco/torta-runner`, versión 2.2), el juego de cumpleaños que Leandro hizo para Cinthia, con ranking familiar, caja fuerte en la nube y fiesta final. Ese juego **queda como está** y no se toca. Sofi Runner se probó primero con el nombre provisorio "Torta Runner+" (versiones 0.1 a 0.5).

Se quitó todo lo propio de la familia: fiesta final con la vela y el video, cumpleaños de la familia, ranking compartido en Google Sheets, caja fuerte, y el fondo de letras que decía "¡Feliz Cumpleaños Cinthia!".

## Cómo está hecho

- **Web (HTML5 + canvas)**, todo el juego en `index.html`. Instalable como app (PWA) y pensado para GitHub Pages.
- Sin servidor: el progreso, el ranking y el desafío semanal se guardan solo en el dispositivo (`localStorage`, clave `sofiRunner.v1`).
- **Comparte sitio con el juego de la familia** (`leandroacasco.github.io`): por eso usa su propia clave de guardado y su `sw.js` solo borra sus propias cachés (las que empiezan con `sofi-runner-`). Al subir una versión nueva hay que subir el número de caché en `sw.js` (`sofi-runner-v1`, `v2`…).
- Paso fijo de 60 actualizaciones por segundo (misma velocidad en pantallas de 60, 90 o 120 Hz). Física: gravedad 0,95, salto −17, doble salto −14.
- `#prueba` al final de la dirección activa `window.TR`, un acceso para las pruebas automáticas (incluye el simulador de partidas).

### Archivos

```
index.html        el juego completo
manifest.json     datos para instalarlo como app
sw.js             copia sin conexión (caché sofi-runner-v1)
icon-192.png, icon-512.png, favicon-32.png
assets/           dibujos de Sofía (WebP)
docs/             capturas para el README
pruebas/          pruebas automáticas y simulador (ver pruebas/README.md)
README.md, CHANGELOG.md, LICENSE (MIT solo para el código; dibujos © Sofía), CONTEXTO.md
```

## Cómo se juega hoy (0.6)

### Básico
- Tocar para saltar; tocar en el aire para el doble salto.
- **Frutilla** +1, **pancito con salame** +5 (más con mejoras).
- **Kampitos** (el jugo de la fiesta, sabores reales): 🟢 Green → imán (6 s), 🟡 Tropical → frutillas x2 (6 s), 🟠 Citrus → escudo (8 s o un choque; también espanta a Dina).
- **Dina:** el primer choque te hace tropezar y Dina te persigue; si chocás otra vez antes de que se canse, te alcanza.
- **¡Una más!:** cuando Dina te alcanza, pagás frutillas para seguir, **una vez por partida**. 25 🍓 + 5 cada 100 m (tope 100). Se vence en 6 s.

### Frutillas
- Dos números que solo suben: `total` (todo lo juntado) y `spent` (lo gastado). Para gastar = total − spent.

### Personajes (500 🍓 cada uno, Sofi gratis) y habilidades
Ninguna habilidad cambia la velocidad, para que los récords se comparen parejo.

| Personaje | Habilidad |
| --- | --- |
| Sofi | 🏃 Escurridiza: Dina se cansa 2 s antes |
| Deisy | 🌟 Saltarina: salta más alto (−18,4 y −15) |
| Leandro | 💘 Corazón imán: imán chico siempre (radio 130) |
| Nora | 🧃 Sorpresas: Kampitos más seguido (espera ×0,7) |
| Cinthia | ❤️ Fiestera: arranca cada partida con un corazón |

### Cosméticos (se ven puestos antes de comprarlos)
- Accesorios: Corazón 150, Hoodie rosa 200 (solo Sofi), Corona 300, **Sombrero de bruja 250 (Halloween)**.
- Confeti que sigue al personaje: Rosa 120, Menta 150, Cielo 150, Dorado 200, Arcoíris 250, **Calabaza 200 (Halloween)**.
- Los de temporada solo se compran en su temporada; después quedan para siempre.

### Pastelería (mejoras para siempre, 4 niveles: 50, 120, 220, 350 🍓)
Imán 6 → 12 s · Escudo 8 → 14 s y, al máximo, 2 choques (se ve con dos anillos) · Pancito 5 → 10 🍓 · Dina se cansa 9 → 5 s.

### Día, noche y dulces
- Cada **1000 m** cambia el día (cielo rosa con las nubes de Sofía) y la noche (estrellas, luna, piso violeta).
- **Dulces:** al caer la primera noche (1000 m) y después en cada amanecer (2000, 4000, 6000…), se elige 1 de 3. Duran toda la partida y se acumulan. Máximo 8 por partida y 3 corazones a la vez.
- Los 12 dulces: Triple salto, Kampito eterno (+50 %), Kampitos por doquier (×2), Corazón extra, Tortas de pancito, Dina dormilona (−40 %), Imancito, Pancito doble, Escudo ya, Picante (todo ×2 pero +2 de velocidad, con trampa), Manzanilla (−1,2 de velocidad), Saltos de globo.
- **Corazones ❤️:** se guardan hasta que chocás; cada choque gasta uno en vez de tropezar. **Escudo 🛡️:** burbuja que dura unos segundos.

### Dificultad (equilibrio de la 0.6)
- La velocidad sube rápido hasta 13 y después sigue despacio hasta 17 (antes se frenaba en 13 y el juego dejaba de ponerse difícil).
- Con la distancia aparecen tortas dobles (desde 500 m), torres de dos tortas (desde 1500 m, piden doble salto) y tríos (desde 3000 m); el espacio entre tortas se achica hasta 9000 m.
- Calentamiento: los primeros 500 m tienen más espacio entre tortas y Dina se cansa en 4 s.
- Tropezar frena 1,6 y se recupera en 2 s (antes quedabas más lento y chocar terminaba ayudando).
- Dina nunca se cansa en menos de 4 s, y cada tropezón de la partida le suma 1 s (hasta 6).
- Los valores están en `BAL` dentro de `index.html`.

**Simulación (30 partidas por perfil, 0.6):**

| Perfil | Metros (p10 / mediana / p90) | Frutillas (mediana) | Minutos |
| --- | --- | --- | --- |
| Novata | 166 / 384 / 1656 | 18 | 0,2 |
| Normal | 762 / 1332 / 3887 | 88 | 0,6 |
| Buena | 629 / 4638 / 16556 | 374 | 1,7 |
| Experta | 3500 / 13993 / 33869 | 1220 | 3,9 |
| Experta con todo comprado | 6789 / 15193 / 38079 | 2203 | 4,1 |

Antes del equilibrio, la experta llegaba a una mediana de 51.000 m (y Leandro hizo 39.441 m y 16.147 frutillas en una partida). Ojo: el jugador automático es una aproximación; lo que valen son las pruebas con gente.

### Temas de temporada
- **Halloween** (15/10 al 2/11): fondo violeta y naranja, murciélagos, calabazas en el piso, luna llena naranja de noche, sombrero de bruja en las tortas, colores de la página en naranja y violeta, y sus dos cosméticos.
- Se activan solos por fecha y se pueden apagar en ⚙️ *Temas de temporada*.
- Para agregar uno: sumar a `SEASONS` (id, nombre, fechas), dibujarlo en `drawBG` y marcar sus cosméticos con `season`.

## Criterio de textos

- Se mantienen los **textos originales** del juego: "¡Uy! Te caíste" con su subtítulo, el globito de Dina ("miau… ¡la torta era mía!"), la pausa y los mensajes de la partida.
- Con texto completo: explicación de cada dulce y cada habilidad (además de su dato corto), ¡Una más! y el desafío semanal.
- Con íconos y etiquetas: los datos de la pantalla de Dina, la compra de personajes, las filas de cosméticos y la Pastelería.

## Diseño de pantallas

- Menú sin deslizar en ninguna pantalla: personaje al centro en un carrusel (los demás detrás, apagados), filas de accesorio 🎀 y confeti 🎊 con flechitas, ¡A CORRER! y la Pastelería. Ayuda en ❓; créditos, novedades, carrera de práctica y "Borrar mi progreso" en ⚙️.
- Antes de cada entrega se corren `pruebas/tamanos.py` (15 tamaños, que nada se encime, corte ni haya que deslizar) y `pruebas/juego.py`.

## Historial

| Versión | Qué trajo |
| --- | --- |
| 0.1 | Frutillas para gastar, Pastelería, ¡Una más! |
| 0.2 | Dulces (cada 400 m), habilidades, personajes a 500, carrusel |
| 0.3 | Cosméticos con vista previa, corazones, escudo doble visible, menú que entra en cualquier pantalla |
| 0.4 | Íconos y etiquetas en lo nuevo; arreglo de capas del carrusel |
| 0.5 | Día y noche cada 1000 m; fondo sin el saludo de cumpleaños |
| 0.6 | Nombre Sofi Runner, equilibrio con simulador, Halloween y temas de temporada |

## Pendientes e ideas

1. Subir el repositorio `sofi-runner` a GitHub y activar Pages.
2. Probarlo con amigos y ajustar precios y dificultad con lo que digan.
3. Dulces que se desbloquean con frutillas en la Pastelería.
4. Más temas de temporada (Navidad, verano, Pascua) y zonas nuevas, idealmente con fondos dibujados por Sofía.
5. Un mosaico de fondo nuevo de Sofía para reemplazar el de letras que se quitó.
6. Si crece: ranking en línea con un servidor de verdad y desafío semanal "sin mejoras" para que sea parejo.
7. Play Store: envolver el HTML con Capacitor o TWA.
