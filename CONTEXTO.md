# Dina Run — contexto del proyecto

Documento para retomar el trabajo en cualquier conversación. Resume qué es el juego, cómo está hecho, qué se decidió y por qué, y qué sigue. Actualizarlo con cada versión.

Última actualización: 28/10/2026 · versión 0.9.4

## Qué es

**Nombre:** Dina Run (antes *Sofi Runner*, y antes de eso *Torta Runner+*). Leandro decidió centrar los juegos en la gata Dina, porque Sofi es solo uno de los personajes jugables. La serie es **Dina Run** (este runner) y **Dina Beat** (juego de ritmo, proyecto y repo aparte: `Kiut-Studio/dina-beat`; lee los personajes y suma frutillas a la bolsa de Dina Run porque comparten sitio). Lo interno no cambia para no perder progreso ni cachés: clave de guardado `sofiRunner.v1`, música `sofiRunner.music`, prefijo de caché `sofi-runner-`.

*Infinite runner* de un solo toque, cute, con estética de juego flash de chicas de los 2000. Se corre, se juntan frutillas, se esquivan porciones de torta y, si chocás, la gata **Dina** te persigue. Las frutillas se gastan en personajes, cosméticos y mejoras.

- **Autor:** Leandro (programación con asistencia de IA).
- **Dibujos, personajes y animación:** **Sofía** (Sofi). Todos los dibujos son suyos y están © Sofía; ella aceptó reutilizarlos en este juego.
- **Excepciones, siempre acreditadas:** el vestido de Alicia de Sofi y las pociones y golosinas de Halloween (`hw_*.webp`) se hicieron con ayuda de IA sobre dibujos de Sofía; las calabazas que se esquivan son un diseño provisorio hecho con código (`pumpkinCv` en `index.html`) hasta que Sofía pase su dibujo. Dina comiendo la calabaza (`dina_calabaza.webp`) era con IA hasta la 0.8; desde la 0.8.1 es un dibujo de Sofía (recortado de su fondo rosa), que también es el logo de Kiut Studio.
- **Personajes:** Sofi, Deisy, Leandro, Nora y Cinthia, más la gata Dina. Son la familia de Leandro.
- **Público:** cualquiera (amigos de la familia que lo probaron y les gustó). Se piensa a futuro en Play Store.

## De dónde viene

Es un desprendimiento de **Torta Runner** (`LeandroACasco/torta-runner`, versión 2.2), el juego de cumpleaños que Leandro hizo para Cinthia, con ranking familiar, caja fuerte en la nube y fiesta final. Ese juego **queda como está** y no se toca. Sofi Runner se probó primero con el nombre provisorio "Torta Runner+" (versiones 0.1 a 0.5).

Se quitó todo lo propio de la familia: fiesta final con la vela y el video, cumpleaños de la familia, ranking compartido en Google Sheets, caja fuerte, y el fondo de letras que decía "¡Feliz Cumpleaños Cinthia!".

## Cómo está hecho

- **Instalación como app:** Torta Runner, Dina Run y Dina Beat están en el mismo sitio (`kiut-studio.github.io`, salvo Torta Runner, que quedó en `leandroacasco.github.io`), cada uno en su carpeta. Cada `manifest.json` tiene su propio `id` y `scope` (`./`) y su ícono, para que el teléfono los instale aparte. Hasta la 0.7 los tres usaban el mismo ícono de Torta Runner y parecían el mismo; desde la 0.7.2 Dina Run usa a Dina comiendo la calabaza en un círculo rosa claro sobre fondo rosa (Leandro la eligió); desde la 0.8.1 con el dibujo de Sofía (`favicon-32.png` va sin círculo para que se entienda chiquito).

- **Web (HTML5 + canvas)**, todo el juego en `index.html`. Instalable como app (PWA) y pensado para GitHub Pages.
- El progreso se guarda en el dispositivo (`localStorage`, clave `sofiRunner.v1`). Desde la 0.9, con cuenta de Google, también va a la nube; desde la 0.9.1 el ranking y el desafío semanal son de todos, en la nube (ver **Cuenta de Google y nube** y **Ranking de todos**).
- **Comparte sitio con Dina Beat** (`kiut-studio.github.io`): por eso usa su propia clave de guardado y su `sw.js` solo borra sus propias cachés (las que empiezan con `sofi-runner-`). Al subir una versión nueva hay que subir el número de caché en `sw.js` (hoy `sofi-runner-v12`).
- Paso fijo de 60 actualizaciones por segundo (misma velocidad en pantallas de 60, 90 o 120 Hz). Física: gravedad 0,95, salto −17, doble salto −14.
- `#prueba` al final de la dirección activa `window.TR`, un acceso para las pruebas automáticas (incluye el simulador de partidas).

### Archivos

```
index.html        el juego completo
manifest.json     datos para instalarlo como app
sw.js             copia sin conexión (caché sofi-runner-v12)
icon-192.png, icon-512.png, favicon-32.png
assets/           dibujos de Sofía (WebP). dina_anim.webp: hoja con la caminata de Dina (2 cuadros) × 4 looks (sin disfraz, bruja, brujito, vampiro)
docs/             capturas para el README
pruebas/          pruebas automáticas y simulador (ver pruebas/README.md)
README.md, CHANGELOG.md, LICENSE (MIT solo para el código; dibujos © Sofía), CONTEXTO.md
```

## Cómo se juega hoy (0.7)

### Básico
- Tocar para saltar; tocar en el aire para el doble salto.
- **Frutilla** +1, **pancito con salame** +5 (más con mejoras).
- **Kampitos** (el jugo de la fiesta, sabores reales): 🟢 Green → imán (6 s), 🟡 Tropical → frutillas x2 (6 s), 🟠 Citrus → escudo (8 s o un choque; también espanta a Dina).
- **Dina:** el primer choque te hace tropezar y Dina te persigue; si chocás otra vez antes de que se canse, te alcanza.
- **Dina se ve así:** camina alternando los 2 cuadros de Sofía (cada 7 actualizaciones, con un saltito por paso). En cada persecución nueva se pone el siguiente look: los disfraces son de Halloween: solo aparecen con el tema prendido y solo los que ganaste en el pase (`save.dinaLooks`); rotan uno por persecución. Fuera de Halloween, o con *Temas de temporada* apagado, Dina va sin disfraz. (No hay un ajuste aparte: Leandro pidió que todo lo de Halloween vaya junto.) Los dibujos originales de los disfraces venían en una sola pose; el sombrero o la capa se recortaron y se pusieron sobre los dos cuadros (alineados por los ojos).
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
- Accesorios: Corazón 150, Hoodie rosa 200 (solo Sofi), Corona 300. **Del pase de Halloween** (no se compran): vestido de Alicia (solo Sofi), sombrero de bruja y confeti calabaza. En el carrusel se ven con la etiqueta 🎃 Nv N y tocándola se abre el pase.
- La ropa que cambia el dibujo entero (hoodie, Alicia) se marca en `ACCS` con `only` (personaje) e `img` (dibujo); `outfitImg()` la resuelve.
- **Cada personaje recuerda su accesorio** (`save.outfits`, por personaje; `equipAcc()` y `accFor()`). `save.outfit` es el del personaje elegido.
- Después de un choque el personaje parpadea con transparencia (antes era un rectángulo blanco que se notaba de noche).
- Confeti que sigue al personaje: Rosa 120, Menta 150, Cielo 150, Dorado 200, Arcoíris 250, Calabaza (pase de Halloween).
- Los de temporada solo se compran en su temporada; después quedan para siempre.

### Pase de Halloween
- Gratis. Suben de nivel los metros corridos en Halloween con el tema prendido (`passAdd` al terminar la partida). **Los premios no se dan solos:** al llegar a un nivel aparece un aviso y la etiqueta "🎁 ¡Premio en el pase!", y se reclaman con el botón ¡Reclamar! en la pantalla del pase (`passClaim`), que muestra el cartel de ¡Felicitaciones!. Se guarda en `save.pass` (`key` = halloween-año, `m`, `got`), así que vuelve a empezar cada año.
- 8 niveles (`PASS` en `index.html`): 400 m Dina bruja · 1500 m 100 🍓 · 3000 m confeti calabaza · 5000 m Dina brujito · 7500 m 200 🍓 · 10.000 m sombrero de bruja · 13.000 m Dina vampiro · 16.000 m vestido de Alicia.
- **Tope diario de 2500 m** (`PASS.daily`, `save.pass.day/dm`): el vestido de Alicia lleva como mínimo 7 días (Leandro pidió que lleve por lo menos una semana). Una jugadora normal (mediana 1332 m por partida, simulación de la 0.6) llega al tope en 2 o 3 partidas por día. Halloween dura del 15/10 al 2/11, así que hay que empezar a más tardar el 27/10 para completarlo.
- Migración 0.7 (`save.mig07`): si alguien tenía comprados el sombrero de bruja, el confeti calabaza o el vestido de Alicia (0.6 o versiones de prueba) sin haberlos reclamado en el pase, se le sacan y se le devuelven las frutillas.
- Se abre con el cartel naranja **Pase de Halloween** del menú, al lado del desafío de la semana (late, y salta cuando hay premio), o con la etiqueta en la pantalla de Dina.

### Música
- Cajita musical hecha con código (`RUN_MEL`). En Halloween suena otra melodía en La menor, un poco más lenta (`HW_MEL`, `HW_BASS`).

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
- **Halloween** (15/10 al 2/11): fondo violeta y naranja, murciélagos, calabazas en el piso, luna llena naranja de noche, **calabazas en vez de tortas** (Sofía no quería sombreros sobre las tortas; misma caja de choque, así que la dificultad no cambia; la mitad de las segundas y terceras de un grupo van sin carita), **pociones en vez de Kampitos** (verde imán, violeta x2, naranja escudo; `HW_POTION`), **golosinas en vez de pancitos** que rotan (`HW_CANDY`), Dina comiendo una calabaza en la pantalla final con textos de Halloween ("miau… ¡la calabaza era mía!"; fuera de Halloween, los originales), colores de la página en naranja y violeta, y sus dos cosméticos.
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
| 0.7 | Dina con la caminata de Sofía, Halloween completo (calabazas, pociones, golosinas, Dina con la calabaza, música) y Pase de Halloween con Alicia al final; accesorio por personaje |
| 0.7.1 | Nombre nuevo: Dina Run |
| 0.7.2 | Ícono propio (Dina comiendo la calabaza), `id` y `scope` propios para instalarse aparte; dirección nueva `/dina-run/` (sin redirección: Leandro les pasa el enlace nuevo a sus testers) |
| 0.7.3 | Arreglo para instalar (`id` absoluto) |
| 0.8 | Mudanza a Kiut Studio con el progreso |
| 0.8.1 | Dina con la calabaza dibujada por Sofía (ícono y pantalla final de Halloween) |
| 0.9 | Cuenta de Google y progreso en la nube (la misma de Dina Beat); las frutillas de Dina Beat en otra pestaña ya no se pisan |
| 0.9.1 | Ranking y desafío de la semana de todos, en Firestore, con primer nombre y foto de Google; se quitó el ranking del dispositivo |
| 0.9.2 | Ranking: sin "0 🍓" en récords viejos; reintento de la foto de Google |
| 0.9.3 | Nombre y foto de Google también en cuentas unidas desde anónimas (antes "Jugador") |
| 0.9.4 | Foto de Google sin cortar (las direcciones pasan de 500 letras; regla `f` hasta 2048); arranque en pestaña oculta |

- **Instalación (0.7.3 / 0.8.4):** el `id` del manifest es una ruta absoluta (`/dina-run/`, `/dina-beat/`). Antes era `./?app=…`: Leandro vio en Android "No se puede instalar esta app" con Dina Run. La sospecha es que el `id` viejo seguía ligado a la instalación de Sofi Runner (misma cadena `?app=sofi-runner`) o que Chrome lo resolvía distinto; con la ruta absoluta no hay ambigüedad. Íconos separados en `any` y `maskable`. En Chromium de escritorio el juego daba "instalable" igual. Si vuelve a pasar: desinstalar los íconos viejos (Sofi Runner) y probar con ⋮ → Agregar a pantalla principal. **No** borrar los datos del sitio en Chrome: borraría las frutillas de todos los juegos.

- **"No se puede instalar esta app" otra vez (28/10):** con Chrome actualizado, ni Dina Run, ni Dina Beat, ni Torta Runner se instalaban en el teléfono de Leandro. Chromium decía que los tres eran instalables; Squoosh y SVGOMG sí se instalaban. Con páginas de prueba en el hub se descartó todo: una copia idéntica de Dina Beat en otra carpeta, hasta con el mismo `id` o el mismo nombre, se instalaba. Era algo que Chrome había guardado trabado para esas carpetas. **Arreglo:** Chrome → Configuración → Configuración de sitios → Todos los sitios → `kiut-studio.github.io` → Borrar y restablecer, y después abrir el enlace viejo para volver a traer el progreso (la dirección vieja nunca se borra). **Nunca** hacerlo con `leandroacasco.github.io` mientras tenga frutillas sin mudar (y ahí vive Torta Runner).

## Kiut Studio y la mudanza (versión 0.8)
- Los juegos de Sofía y Leandro ahora son de la organización de GitHub **Kiut Studio** (`Kiut-Studio`; "kiut" es como ellos dicen *cute*; Sofía aprobó el nombre). Hub: `kiut-studio.github.io` (repo `Kiut-Studio/kiut-studio.github.io`). Torta Runner queda en la cuenta de Leandro (`leandroacasco.github.io/torta-runner/`) y aparece en el hub como edición especial.
- Repos: `Kiut-Studio/dina-run` y `Kiut-Studio/dina-beat`, publicados en `kiut-studio.github.io/dina-run/` y `/dina-beat/`. Como están en el mismo sitio, siguen compartiendo guardado (personajes y frutillas).
- **Mudanza del progreso:** el guardado vive por dirección, así que en la dirección vieja (`leandroacasco.github.io/dina-run/` y `/dina-beat/`) quedan repos chicos de mudanza en la cuenta de Leandro (`LeandroACasco/dina-run` y `dina-beat`): leen `sofiRunner.v1`, `sofiRunner.music`, `sofiSilbato.v1` y `tortaRunnerPlus.v1` y redirigen a la dirección nueva con `#mudanza=` (JSON en base64url; no pasa por ningún servidor). No borran nada de la dirección vieja. Su `sw.js` borra la copia sin conexión vieja y se da de baja.
- Al principio de `index.html` de cada juego (antes de cargar el guardado) hay un bloque que recibe `#mudanza=`; es el mismo en los dos juegos y trata las cuatro claves: Dina Run gana si trae más frutillas juntadas (`total`); Dina Beat gana si trae más estrellas, y las canciones compuestas se juntan por `id`; `sofiRunner.music` y `tortaRunnerPlus.v1` solo se escriben si no hay. Muestra un aviso arriba unos segundos y borra el `#` de la dirección. Repetir no duplica.
- Ojo: las páginas de mudanza se subieron antes que el receptor, así que quien entró por la dirección vieja entre el 26 y el 28/10 llegó sin su progreso. No se perdió nada: con volver a abrir el enlace viejo se lo trae.
- Las claves de guardado y el `id` de las apps (`/dina-run/`, `/dina-beat/`) no cambian. Al cambiar de dominio el teléfono las ve como apps nuevas: hay que instalarlas de nuevo desde la dirección nueva.
- Desde ahora Claude sube las versiones directo a GitHub (app de Claude instalada).

## Cuenta de Google y nube (versión 0.9)
- Mismo Firebase que Dina Beat: proyecto `kiut-studio` ("Kiut Studio Games", plan Spark gratis), Authentication con Google, Firestore en `southamerica-east1`. Dina Run tiene su propia app web registrada (`appId …335beb…`, la que pasó Leandro); el resto de `FB_CFG` es igual. Reglas: cada jugador lee y escribe solo `jugadores/{uid}`; no hizo falta cambiarlas.
- Código en `index.html`, bloque "☁️ nube" (antes del simulador). SDK 12.10.0 desde gstatic con `import()` dinámico: se carga solo al abrir ☁️ o al arrancar si ya usaste la cuenta (acá o en Dina Beat). Sin internet el juego sigue igual. Todo pasa por `cloud.api` {onUser, google, out, get, set}; las pruebas lo cambian por `window.CLOUD_MOCK`.
- **Documento compartido** `jugadores/{uid}`: Dina Run escribe solo `run` (su guardado sin lo del aparato) y `runAt`, con `mergeFields` (reemplaza esos dos campos enteros y no toca `beat`, `beatAt`, `nombre`, `personaje` de Dina Beat).
- **No viaja** (`DEVICE_ONLY`): `muted`, `set` (volúmenes, vibración, cuenta 3-2-1, temas, menos animaciones), `seenVersion`, `cloud`, y lo del ranking de este aparato: `rk` (lo último que se vio), `rkMine` y `wkSent` (lo que ya se subió desde acá).
- **Cómo se juntan** (`mergeSave`): `total`, `spent`, `best` y mejoras (`up`) el máximo; personajes, cosméticos, disfraces de Dina, `seen` y consejos juntados; logros juntados (con la fecha más vieja); números de `st` el máximo; pase del mismo año: metros el máximo y premios reclamados juntados; desafíos ganados (`wins`) juntados; tu mejor del desafío (`wkMine`) el máximo si es la misma semana; `bestRun` el de más metros. Personaje, accesorios, confeti y nombre: del guardado modificado último (`save.mod`, que se pone en cada `persist()`).
- Límite conocido: con el máximo, si se juega **a la vez** en dos teléfonos sin conexión, se pueden perder las frutillas del que ganó menos. Para jugar en uno por vez no pasa nada.
- **Cuándo sincroniza:** al entrar, al abrir el juego, al volver a la pestaña (si pasaron 5 min), al recuperar internet y con "🔄 Sincronizar ahora". Cada `persist()` sube a los 3 s. Nunca cambia el guardado en medio de una partida (`whenIdle`: espera al menú o la pantalla final). El simulador no sube nada (`simulating`).
- **Otra pestaña (pendiente viejo, resuelto):** Dina Run escucha el evento `storage` de `sofiRunner.v1`. Si el cambio no trae fecha nueva (`mod` igual), vino de Dina Beat: se suma la diferencia de frutillas (así no se pierden si acá también jugaste). Si trae fecha nueva, es otra pestaña de Dina Run y se junta como con la nube. Lo juntado se guarda una sola vez (no rebota entre pestañas).
- **Pantallas:** botón ☁️ arriba en el menú (primero del grupo de íconos): "☁️ Entrar" en pantallas de 480 px o más (clase `slim` debajo: solo ☁️) y la foto de la cuenta cuando entraste. Fila "☁️ Cuenta de Google" en ⚙️ Ajustes. Pantalla `#acct`: foto, nombre, correo, estado, "🔄 Sincronizar ahora" y "Salir" (el progreso sigue en el teléfono). El chip de abajo dice "Progreso guardado en la nube ☁️".
- **Borrar mi progreso con cuenta:** sale de la cuenta y borra solo el teléfono; lo de la nube queda a salvo (si no, la próxima sincronización lo traería de vuelta).
- Pruebas: `pruebas/nube.py` (nube falsa con varios teléfonos; 20 revisiones). `tamanos.py` también revisa la pantalla `#acct`.

## Ranking de todos (versión 0.9.1)
- Pedido de Leandro (28/10): con la cuenta ya hay foto y nombre, así que no hace falta escribir el nombre ni elegir un personaje como ícono. El sistema viejo (nombre escrito, ícono, ranking por dispositivo, `RANKING_URL` para un servidor) queda solo en Torta Runner. Decisiones de Leandro: ranking **de todos en la nube**; se muestra **solo el primer nombre** (menos datos personales, juegan chicos); **sin cuenta no se aparece**, pero se puede ver.
- **Lugares en Firestore:** `ranking/{uid}` {`n` primer nombre, `f` foto, `c` personaje del récord, `m` récord en metros, `fr` frutillas de esa partida, `l` logros, `g` desafíos ganados, `at`}; `semanas/{lunes, ej. S2026-10-26}/filas/{uid}` {`n`, `f`, `c`, `v` mejor valor de la semana, `r` id del desafío, `at`}.
- **Código** (bloque "ranking" en `index.html`): `rankPublish()` sube el récord si cambió algo (`rkMine` guarda lo último subido, para no gastar escrituras) y la fila de la semana si mejoró (`wkSent`); `rankFetch()` baja los 20 primeros de cada lista y el 1.º de la semana anterior; `myPlace()` cuenta cuántos tienen más metros (`getCountFromServer`) para mostrar "🏆 #N" al terminar y tu fila aunque estés más abajo del 20. Sin cuenta, para ver el ranking se usa una sesión anónima (invisible).
- **Quién ganó la semana:** el 1.º de `semanas/{anterior}`. Si sos vos, se anota en `save.wins` y sube a `g` ("🏆 ganó N desafíos"). Se marca con 👑 en las listas y en el cartel del desafío del menú (`save.rk.prev`).
- Se sube: al terminar cada partida, al entrar y al sincronizar. Se baja: al abrir 🏆 y al sincronizar.
- **Ojo, cuentas que empezaron anónimas** (miraron el ranking sin cuenta o jugaron desafíos de Dina Beat y después entraron con Google con `linkWithPopup`): Firebase deja vacíos `displayName` y `photoURL`; el nombre y la foto están en `providerData` (google.com). `mapUser` los toma de ahí y `fixProfile` los copia a la cuenta con `updateProfile` (al entrar y cada vez que se abre), así también los ve Dina Beat. Antes de la 0.9.3 esas cuentas salían como "Jugador" sin foto; se corrigen solas al volver a abrir el juego (`rankPublish` ve el cambio y vuelve a subir la fila). Dina Beat tiene el mismo detalle en su `mapUser` (campo `nombre`).
- **Fotos largas:** las direcciones de las fotos de Google (`lh3.googleusercontent.com/a-/…`) pueden pasar de 500 letras; hasta la 0.9.3 se cortaban en 500 y no cargaban. Desde la 0.9.4 van completas si miden hasta 2000 (si no, sin foto), y la regla `filaOk` acepta hasta 2048. `setRow()`: si Firebase rechaza la fila con foto (regla vieja), la sube sin foto y marca `rkMine.fNo`; se reintenta cada hora.
- **Arranque en pestaña oculta:** con tamaño cero, `draw()` no dibuja (antes `createLinearGradient` tiraba un error que cortaba el resto del código, incluida la nube).
- **Pantallas:** en la final, con cuenta, chip "🏆 #N" (tocándolo abre el ranking); sin cuenta, botón "☁️ Entrá con Google para aparecer en el ranking" (abre la cuenta y, al volver, sube y muestra el puesto). En 🏆, abajo: "Así aparecés: Nombre" con tu foto, o el botón Entrar con Google.
- El récord de antes de la 0.9.1 sube igual al entrar (`save.best`; las frutillas de esa partida no se sabían y van en 0, y desde la 0.9.2 no se muestran). Si la foto de Google no carga (Google a veces frena las fotos un momento), se reintenta una vez a los 1,2 s y después va el dibujo del personaje. Los datos viejos (`name`, `runs`, `avatars`, `wk`, `anonBest`, `logrosBy`, `champs…`, `prevWin…`, `pending`, `lastTop`, `lastWeek`) se borran al abrir.
- **Reglas de Firestore** (las agrega Leandro en la consola de Firebase, debajo de las de Dina Beat, dentro de `match /databases/{database}/documents { … }`). Validan que cada uno escriba solo su fila, solo con cuenta de Google, con los campos y tipos de arriba y un máximo de 1.000.000; no impiden un récord falso de alguien que toque el código, pero sí basura:
  ```
    // 🏆 Dina Run: ranking de todos (desde la 0.9.1)
    function esGoogle(uid) {
      return request.auth != null && request.auth.uid == uid
        && request.auth.token.firebase.sign_in_provider == 'google.com';
    }
    function filaOk(d) {
      return d.n is string && d.n.size() > 0 && d.n.size() <= 20
        && d.f is string && d.f.size() <= 2048
        && d.c is string && d.c.size() <= 20 && d.at is int;
    }
    match /ranking/{uid} {
      allow read: if request.auth != null;
      allow create, update: if esGoogle(uid) && filaOk(request.resource.data)
        && request.resource.data.keys().hasOnly(['n','f','c','m','fr','l','g','at'])
        && request.resource.data.m is int && request.resource.data.m >= 0 && request.resource.data.m <= 1000000
        && request.resource.data.fr is int && request.resource.data.l is int && request.resource.data.g is int;
    }
    match /semanas/{semana}/filas/{uid} {
      allow read: if request.auth != null;
      allow create, update: if esGoogle(uid) && filaOk(request.resource.data)
        && request.resource.data.keys().hasOnly(['n','f','c','v','r','at'])
        && request.resource.data.v is int && request.resource.data.v >= 0 && request.resource.data.v <= 1000000
        && request.resource.data.r is string;
    }
  ```
- Pruebas: `pruebas/nube.py` (ranking con tres cuentas y una sin cuenta, primer nombre, foto, puesto, desafío de la semana, ganador de la semana pasada); `tamanos.py` abre 🏆 con 10 jugadores y el panel de entrar.

## Pendientes e ideas

1. **Dibujo de la calabaza de Sofía:** cuando llegue, guardarlo en `assets/calabaza.webp`, sumarlo a `IMG_FILES` y a `sw.js`, y usarlo en `pumpkinCv()`.
2. Probarlo con amigos y ajustar precios y dificultad con lo que digan.
3. Dulces que se desbloquean con frutillas en la Pastelería.
4. Más temas de temporada (Navidad, verano, Pascua) y zonas nuevas, idealmente con fondos dibujados por Sofía.
5. Un mosaico de fondo nuevo de Sofía para reemplazar el de letras que se quitó.
6. Desafío semanal "sin mejoras" para que sea parejo. Si aparecen récords falsos: validar en el servidor (Cloud Functions, que necesita plan de pago) o un botón para que Leandro borre filas.
7. Play Store: envolver el HTML con Capacitor o TWA.
