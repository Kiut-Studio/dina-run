// Copia sin conexión de Dina Run (antes Sofi Runner; el prefijo de caché queda igual).
// Ojo: este juego comparte el sitio (kiut-studio.github.io) con Dina Beat,
// así que solo borra sus propias cachés (las que empiezan con PRE), nunca las del otro juego.
const PRE='sofi-runner-';
const C=PRE+'v7';
const FILES=["./", "index.html", "manifest.json", "icon-192.png", "icon-512.png", "favicon-32.png", "assets/cinthia.webp", "assets/deisy.webp", "assets/dina.webp", "assets/dina_calabaza.webp", "assets/dina_avatar.webp", "assets/dina_anim.webp", "assets/frutilla.webp", "assets/kampito.webp", "assets/kampito_tropical.webp", "assets/kampito_verde.webp", "assets/leandro.webp", "assets/nora.webp", "assets/nubes.webp", "assets/pancito.webp", "assets/sofi.webp", "assets/sofi_hoodie.webp", "assets/sofi_alicia.webp", "assets/torta.webp", "assets/dina_bruja.webp", "assets/dina_brujito.webp", "assets/dina_vampiro.webp", "assets/hw_pocion_verde.webp", "assets/hw_pocion_violeta.webp", "assets/hw_pocion_naranja.webp", "assets/hw_caramelo_verde.webp", "assets/hw_chupetin.webp", "assets/hw_candy_corn.webp", "assets/hw_gomita.webp", "assets/hw_bombon.webp", "assets/hw_caramelo_violeta.webp"];
// cache:'reload' baja cada archivo de nuevo (sin copias viejas del navegador) al instalar una versión nueva
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(FILES.map(f=>new Request(f,{cache:'reload'})))));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith(PRE)&&k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin) return;
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp));return res})));
});
