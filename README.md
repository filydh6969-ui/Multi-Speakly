# Kitty-Speakly

## Compilar el APK en GitHub
1. Sube TODO el contenido de esta carpeta (incluida `.github` y `blender`) a la raíz de tu repositorio.
2. Pestaña **Actions** → **Build APK** → **Run workflow** (o se ejecuta solo al hacer commit).
3. Espera 8–12 min. Cuando termine, abre el run y descarga en *Artifacts*:
   - **Speakly-APK**: el APK.
   - **Mascota-Blender**: `mascot.blend` (se abre en Blender) y `mascot.glb`.
4. Si el paso **Crear mascota 3D con Blender** sale con advertencia, la app usa el gatito 3D simple.

La mascota se genera con `blender/build_mascot.py`.
