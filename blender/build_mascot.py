# Kitty-Speakly: genera el gatito 3D con esqueleto y 5 animaciones, y exporta mascot.blend y mascot.glb
# Uso (sin abrir Blender):  blender -b --python build_mascot.py -- carpeta_salida
# Uso (con Blender abierto): pestaña Scripting > Open > build_mascot.py > Run Script
import bpy, sys, math, os
from mathutils import Vector, Quaternion
out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else os.path.expanduser("~/mascota_salida")
os.makedirs(out, exist_ok=True)
if bpy.app.background:
    bpy.ops.wm.read_factory_settings(use_empty=True)
else:
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.context.scene.render.fps = 24

def mat(name, h, rough=.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    c = [(((h >> s) & 255) / 255) ** 2.2 for s in (16, 8, 0)]
    b.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1); b.inputs["Roughness"].default_value = rough
    return m
M = {k: mat(k, v) for k, v in dict(fur=0x857b6c, dark=0x4b453d, white=0xfafafa, pink=0xd8a39f, nose=0xc98a87, green=0x8f9a3c, eye=0x111318, mouth=0x6b2a33, brown=0xa07a5a, collar=0xee5fa7, collar2=0xd6428a, silver=0xaeb3c0, whisk=0xc9c9c9).items()}

# ---------- Piezas (cada una pegada a un hueso) ----------
parts = []
def part(kind, bone, m, loc, sc, rot=(0, 0, 0), r=.4, d=.7):
    if kind == "s": bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=1, location=loc)
    elif kind == "c": bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r, depth=d, location=loc)
    elif kind == "t": bpy.ops.mesh.primitive_torus_add(major_segments=40, minor_segments=12, major_radius=r, minor_radius=d, location=loc)
    else: bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=.006, depth=.9, location=loc)
    o = bpy.context.object; o.scale = sc; o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if kind in ("s", "c", "t"): bpy.ops.object.shade_smooth()
    o.data.materials.append(m)
    o.vertex_groups.new(name=bone).add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')
    parts.append(o)

# Gato de pie sobre dos patas, estilo mascota
tp = [(.25, .5, .8), (.7, .55, .85), (1.05, .45, 1.1), (1.2, .25, 1.45), (1.2, .05, 1.8), (1.05, -.05, 2.05), (.9, -.05, 2.2)]
def hy(x, z): return -.68 * math.sqrt(max(.01, 1 - (x / .78) ** 2 - ((z - 2.9) / .66) ** 2))
def tx(z, y): return .62 * math.sqrt(max(.01, 1 - ((z - 1.15) / .8) ** 2 - (y / .52) ** 2))
F, D, W = M["fur"], M["dark"], M["white"]
# torso: caderas, pecho y babero blanco
part("s", "body", F, (0, 0, 1.15), (.62, .52, .8)); part("s", "body", F, (0, 0, 1.75), (.52, .44, .58))
part("s", "body", W, (0, -.3, 1.5), (.4, .28, .9))
for z in (.7, .95, 1.2, 1.45):
    for s in (-1, 1): part("s", "body", D, (s * tx(z, -.12), -.12, z), (.045, .2, .055))
for z in (1.9, 2.05):
    for s in (-1, 1): part("s", "body", D, (s * .5 * math.sqrt(max(.01, 1 - ((z - 1.75) / .58) ** 2 - .074)), -.12, z), (.04, .18, .05))
# cuello y cabeza
part("s", "head", F, (0, 0, 2.3), (.42, .38, .32)); part("s", "head", F, (0, 0, 2.9), (.78, .68, .66))
part("s", "head", W, (0, -.5, 2.62), (.44, .34, .32)); part("s", "head", W, (0, -.56, 3.15), (.1, .12, .34))
part("s", "head", M["nose"], (0, -.82, 2.72), (.09, .06, .065)); part("s", "head", M["brown"], (.18, -.76, 2.6), (.1, .05, .08))
part("s", "mouth", M["mouth"], (0, -.74, 2.52), (.15, .05, .014))
for x, z in ((.2, 3.3), (.34, 3.22), (-.2, 3.3), (-.34, 3.22)): part("s", "head", D, (x, hy(x, z) + .01, z), (.035, .06, .17))
# collar rosa con huellitas, hebilla y argolla
part("t", "head", M["collar"], (0, 0, 2.28), (1, .92, 1), r=.43, d=.065)
part("s", "head", M["collar2"], (0, -.46, 2.28), (.1, .045, .085))
part("t", "head", M["silver"], (-.32, -.34, 2.28), (1, 1, 1), (math.pi / 2, 0, .5), r=.06, d=.014)
for x in (-.18, -.06, .12, .24): part("s", "head", M["white"], (x, -math.sqrt(max(.01, .43 ** 2 - x * x)) * .92 - .01, 2.28), (.032, .012, .032))
for s, n in ((-1, "L"), (1, "R")):
    part("c", "ear" + n, F, (s * .5, 0, 3.62), (1, 1, 1), (0, s * .2, 0), r=.34, d=.8)
    part("c", "ear" + n, M["pink"], (s * .5, -.09, 3.58), (1, 1, 1), (0, s * .2, 0), r=.21, d=.6)
    part("s", "eye" + n, M["dark"], (s * .3, -.6, 2.98), (.2, .08, .235))
    part("s", "eye" + n, M["green"], (s * .3, -.65, 2.98), (.17, .08, .2))
    part("s", "eye" + n, M["eye"], (s * .3, -.71, 2.98), (.095, .045, .14))
    part("s", "eye" + n, M["white"], (s * .34, -.75, 3.06), (.04, .025, .04))
    part("s", "brow" + n, D, (s * .31, -.55, 3.2), (.15, .035, .035))
    for z in (2.78, 2.92):
        part("s", "head", D, (s * .78 * math.sqrt(max(.01, 1 - ((z - 2.9) / .66) ** 2 - .086)), -.2, z), (.04, .2, .035))
    for j in (-1, 0, 1): part("y", "head", M["whisk"], (s * .95, -.5, 2.7 + j * .08), (1, 1, 1), (0, math.pi / 2, s * .1 * j))
    # brazos: hombro, brazo, codo, antebrazo blanco y patita (esferas que se solapan para ocultar la articulacion)
    part("s", "up" + n, F, (s * .62, 0, 1.95), (.25, .25, .25)); part("s", "up" + n, F, (s * .66, 0, 1.58), (.17, .17, .42))
    part("s", "up" + n, F, (s * .68, 0, 1.2), (.17, .17, .17))
    part("s", "fore" + n, W, (s * .68, 0, .92), (.15, .15, .34)); part("s", "fore" + n, W, (s * .68, -.06, .62), (.2, .23, .17))
    part("s", "fore" + n, M["pink"], (s * .68, -.2, .6), (.08, .04, .06))
    # piernas y pies
    part("s", "foot" + n, F, (s * .32, 0, .78), (.27, .27, .5)); part("s", "foot" + n, W, (s * .32, -.03, .4), (.22, .22, .32))
    part("s", "foot" + n, W, (s * .32, -.2, .14), (.27, .42, .14)); part("s", "foot" + n, D, (s * .57, -.02, .85), (.04, .18, .05))
for i in range(6):
    r = .15 - .01 * i
    part("s", "tail%d" % i, D if (i % 2 or i == 5) else F, tp[i], (r, r, r))
bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
mesh = bpy.context.object; mesh.name = "Kitty"

# ---------- Esqueleto ----------
B = [("root", (0, 0, 0), (0, 0, .25), None), ("body", (0, 0, .3), (0, 0, 2.1), "root"), ("head", (0, 0, 2.2), (0, 0, 3.5), "body"),
     ("mouth", (0, -.7, 2.55), (0, -.7, 2.75), "head")]
for s, n in ((-1, "L"), (1, "R")):
    B += [("ear" + n, (s * .5, 0, 3.3), (s * .5, 0, 3.95), "head"), ("eye" + n, (s * .3, -.62, 2.85), (s * .3, -.62, 3.05), "head"),
          ("brow" + n, (s * .31, -.6, 3.18), (s * .31, -.6, 3.3), "head"), ("up" + n, (s * .62, 0, 1.95), (s * .68, 0, 1.2), "body"),
          ("fore" + n, (s * .68, 0, 1.2), (s * .68, 0, .6), "up" + n), ("foot" + n, (s * .32, 0, .8), (s * .32, 0, .15), "root")]
for i in range(6): B.append(("tail%d" % i, tp[i], tp[i + 1], "body" if i == 0 else "tail%d" % (i - 1)))
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.object; arm.name = "Rig"; ad = arm.data
for e in list(ad.edit_bones): ad.edit_bones.remove(e)
for n, h, t, p in B:
    e = ad.edit_bones.new(n); e.head = Vector(h); e.tail = Vector(t)
    if p: e.parent = ad.edit_bones[p]
bpy.ops.object.mode_set(mode='OBJECT')
mesh.parent = arm
mod = mesh.modifiers.new("Arm", 'ARMATURE'); mod.object = arm

# ---------- Animaciones ----------
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
ALL = [b[0] for b in B]
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
PB = arm.pose.bones
def base(): return {n: [[], (0, 0, 0), (1, 1, 1)] for n in ALL}
def up(d, n, a): d[n][0].append((Y, -a if n.endswith("R") else a))
def setb(n, r, l, s, f):
    pb = PB[n]; m3 = pb.bone.matrix_local.to_3x3().inverted(); q = Quaternion((1, 0, 0, 0))
    for ax, a in r: q = q @ Quaternion(m3 @ Vector(ax), a)
    pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = q; pb.location = m3 @ Vector(l); pb.scale = Vector(s)
    for p in ("rotation_quaternion", "location", "scale"): pb.keyframe_insert(p, frame=f)
S = math.sin; C = math.cos; PI = math.pi
def idle(t, u):
    d = base(); w = 2 * PI * u; s2 = S(2 * w)
    d["body"][2] = (1, 1 + .02 * s2, 1)
    d["head"][0] += [(Z, .25 * S(w)), (Y, .04 * S(2 * w + 1)), (X, .03 * s2)]
    for n in "LR":
        up(d, "up" + n, .12 + .03 * s2)
        d["ear" + n][0].append((Y, (1 if n == "R" else -1) * .12 * max(0, S(3 * w)) ** 4))
        d["eye" + n][2] = (1, .1 if .66 < u < .70 else 1, 1)
    for i in range(6): d["tail%d" % i][0].append((Z, .22 * S(2 * w - i * .55)))
    return d
def wave(t, u):
    d = base(); e = max(0, min(1, u / .15, (1 - u) / .15))
    up(d, "upR", 2.5 * e + .12 * (1 - e)); d["foreR"][0].append((Y, .7 * S(t * 9) * e)); up(d, "upL", .12)
    d["head"][0] += [(Z, .15 * S(t * 3) * e), (Y, .08 * e)]
    for n in "LR": d["brow" + n][1] = (0, 0, .1 * e)
    d["mouth"][2] = (1, 1 + 5 * e, 1)
    for i in range(6): d["tail%d" % i][0].append((Z, .3 * S(t * 8 - i * .55)))
    return d
def cheer(t, u):
    d = base(); j = (t % .75) / .75
    sy = 1 - .14 * max(0, 1 - j / .15) - .12 * max(0, (j - .88) / .12) + .1 * S(PI * j); k = 1 / math.sqrt(sy)
    d["root"][1] = (0, 0, max(0, S(PI * j)) * .7); d["body"][2] = (k, sy, k)
    for n in "LR":
        sg = 1 if n == "R" else -1
        up(d, "up" + n, 2.8 + .2 * S(16 * t)); d["fore" + n][0].append((Y, .15 * sg)); d["eye" + n][2] = (1, .25, 1)
        d["brow" + n][1] = (0, 0, .1); d["ear" + n][0].append((Y, sg * .4))
    d["mouth"][2] = (1, 12, 1); d["head"][0].append((X, -.2))
    for i in range(6): d["tail%d" % i][0].append((Z, .4 * S(8 * t - i * .55)))
    return d
def sad(t, u):
    d = base(); e = min(1, u / .3)
    d["head"][0] += [(X, .55 * e), (Y, .12 * e)]; d["root"][1] = (0, 0, -.06 * e); d["body"][2] = (1, 1 - .05 * e, 1)
    for n in "LR":
        sg = 1 if n == "R" else -1
        up(d, "up" + n, .12 - .08 * e); d["eye" + n][2] = (1, 1 - .4 * e, 1)
        d["ear" + n][0].append((Y, -sg * .7 * e)); d["brow" + n][0].append((Y, sg * .35 * e))
    for i in range(6): d["tail%d" % i][0].append((X, -.35 * e))
    return d
def dance(t, u):
    d = base(); b = 2 * PI * t
    d["root"][1] = (0, 0, abs(S(b)) * .35); d["body"][0].append((Z, .35 * S(b / 2))); d["body"][2] = (1, 1 + .06 * C(2 * b), 1)
    up(d, "upL", 1.9 + S(b)); up(d, "upR", 1.9 - S(b))
    for n in "LR":
        d["fore" + n][0].append((Y, .4 + .4 * S(b))); d["eye" + n][2] = (1, .8, 1); d["brow" + n][1] = (0, 0, .1)
        d["ear" + n][0].append((Y, (1 if n == "R" else -1) * .3 * S(2 * b)))
    d["head"][0] += [(Y, .25 * S(b)), (X, abs(S(b)) * .1), (Z, .3 * S(b / 2))]
    d["mouth"][2] = (1, 7, 1); d["footL"][1] = (0, 0, max(0, S(b)) * .2); d["footR"][1] = (0, 0, max(0, -S(b)) * .2)
    for i in range(6): d["tail%d" % i][0].append((Z, .4 * S(2 * b - i * .55)))
    return d
for name, n, fn in (("Idle", 96, idle), ("Wave", 72, wave), ("Cheer", 54, cheer), ("Sad", 60, sad), ("Dance", 48, dance)):
    act = bpy.data.actions.new(name); act.use_fake_user = True
    arm.animation_data_create(); arm.animation_data.action = act
    for pb in PB:
        pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0); pb.scale = (1, 1, 1)
    for f in range(n + 1):
        for bn, (r, l, s_) in fn(f / 24, f / n).items(): setb(bn, r, l, s_, f + 1)
bpy.ops.object.mode_set(mode='OBJECT')
adata = arm.animation_data; adata.action = None
for a in bpy.data.actions:
    tr = adata.nla_tracks.new(); tr.name = a.name; tr.strips.new(a.name, 1, a)

# ---------- Exportar ----------
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "mascot.blend"))
import addon_utils
for mod in ("io_scene_gltf2",):
    try:
        addon_utils.enable(mod, default_set=True, persistent=True); print("Addon activado:", mod)
    except Exception as e:
        print("No se pudo activar", mod, repr(e))
print("Operador gltf disponible:", hasattr(bpy.ops.export_scene, "gltf"))
kw = dict(filepath=os.path.join(out, "mascot.glb"), export_format='GLB', export_skins=True, export_animations=True)
ok = False
for extra in ({}, {"export_nla_strips": True}, {"export_animation_mode": "NLA_TRACKS"}):
    try:
        bpy.ops.export_scene.gltf(**kw, **extra); ok = True; print("EXPORT OK con", extra); break
    except Exception as e:
        print("EXPORT FALLO con", extra, "->", repr(e))
if not ok: raise SystemExit("No se pudo exportar el GLB")
print("LISTO:", out)
