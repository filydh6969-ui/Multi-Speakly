# Kitty-Speakly

1. Crea un repositorio en GitHub y sube todo el contenido de esta carpeta (incluida `.github`).
2. Ve a la pestaña **Actions** → **Build APK** (se ejecuta solo al subir; si no, pulsa **Run workflow**).
3. Cuando termine (3–5 min), entra al run y descarga **Speakly-APK** en *Artifacts*.
4. Descomprime el zip, pasa `app-debug.apk` a tu Android e instálalo (permite "orígenes desconocidos").

La app vive en `www/index.html`. Edítala, haz commit y GitHub generará un APK nuevo.

## Mascota 3D
El workflow copia `three.min.js` (Three.js r149) a `www/` en cada compilación. Si ese paso falla, la app usa la mascota 2D de respaldo.
