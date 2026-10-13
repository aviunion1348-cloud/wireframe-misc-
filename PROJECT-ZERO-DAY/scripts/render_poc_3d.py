#!/usr/bin/env python3
"""Render a CPU-only 60-second, genuinely 3D procedural-animation POC.

Panda3D's TinyDisplay software renderer draws actual 3D meshes offscreen. The
engineer, room, monitor and desk props are procedural geometry; joints/limbs,
head pose, gaze, hands, interface text and camera all animate over time. This is
not live-action or photoreal, and is not the feature film.

Runtime tools are installed outside the repository:
  PYTHONPATH=/tmp/zero-day-py
  FFMPEG_BINARY=/tmp/zero-day-py/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
"""
from __future__ import annotations

import argparse
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from panda3d.core import (
    Geom, GeomNode, GeomTriangles, GeomVertexData, GeomVertexFormat,
    GeomVertexWriter, NodePath, PNMImage, TextNode, Vec3, loadPrcFileData,
)

W, H = 1280, 720
FPS = 24
ACTIVE_H = 536
MATTE_TOP = (H - ACTIVE_H) // 2
PROJECT = Path(__file__).resolve().parents[1]
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def smooth(a: float, b: float, x: float) -> float:
    u = max(0.0, min(1.0, (x - a) / (b - a)))
    return u * u * (3.0 - 2.0 * u)


def mix(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


class Scene:
    def __init__(self) -> None:
        # TinyDisplay provides a CPU software 3D renderer; no X server/GPU is required.
        loadPrcFileData("", "load-display p3tinydisplay")
        loadPrcFileData("", "window-type offscreen")
        loadPrcFileData("", f"win-size {W} {H}")
        loadPrcFileData("", "audio-library-name null")
        loadPrcFileData("", "notify-level fatal")
        loadPrcFileData("", "framebuffer-multisample 0")
        from direct.showbase.ShowBase import ShowBase

        self.base = ShowBase(windowType="offscreen")
        self.base.setBackgroundColor(0.0, 0.0, 0.0, 1.0)
        self.base.camLens.setFov(52)
        self.base.camLens.setAspectRatio(W / ACTIVE_H)
        region = self.base.cam.node().getDisplayRegion(0)
        bottom = MATTE_TOP / H
        region.setDimensions(0.0, 1.0, bottom, 1.0 - bottom)
        region.setClearColorActive(True)
        region.setClearColor((0.014, 0.021, 0.029, 1.0))
        self.sphere_format = GeomVertexFormat.getV3c4()
        self.box_format = GeomVertexFormat.getV3c4()
        self.sphere_template = self._make_sphere_template()
        self.cube_template = self._make_cube_template()
        self.root = self.base.render
        self._build_room()
        self._build_character()
        self._build_ui()
        self.base.graphicsEngine.renderFrame()
        self.base.graphicsEngine.renderFrame()
        if self.base.win is None or self.base.win.getXSize() != W or self.base.win.getYSize() != H:
            raise RuntimeError("Panda3D did not create the requested 1280x720 offscreen buffer")

    @staticmethod
    def _shade(base: tuple[float, float, float], normal: Vec3) -> tuple[float, float, float, float]:
        light = Vec3(0.30, -0.64, 0.70)
        light.normalize()
        lambert = max(0.0, normal.dot(light))
        # Baked, soft key/fill response for TinyDisplay, whose renderer has no GPU shader path.
        illumination = 0.30 + 0.70 * lambert
        return tuple(max(0.0, min(1.0, c * illumination)) for c in base) + (1.0,)

    def _make_sphere_template(self):
        rings, slices = 16, 24
        vdata = GeomVertexData("sphere", self.sphere_format, Geom.UHStatic)
        vw, cw = GeomVertexWriter(vdata, "vertex"), GeomVertexWriter(vdata, "color")
        for i in range(rings + 1):
            phi = math.pi * i / rings
            z, radius = math.cos(phi), math.sin(phi)
            for j in range(slices + 1):
                theta = 2.0 * math.pi * j / slices
                n = Vec3(radius * math.cos(theta), radius * math.sin(theta), z)
                vw.addData3f(n)
                cw.addData4f(*self._shade((1.0, 1.0, 1.0), n))
        tris = GeomTriangles(Geom.UHStatic)
        stride = slices + 1
        for i in range(rings):
            for j in range(slices):
                a, b = i * stride + j, (i + 1) * stride + j
                tris.addVertices(a, b, a + 1)
                tris.addVertices(a + 1, b, b + 1)
        tris.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(tris)
        node = GeomNode("sphere-template")
        node.addGeom(geom)
        return NodePath(node)

    def _make_cube_template(self):
        faces = [
            ((1,0,0), [(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),
            ((-1,0,0), [(-1,1,-1),(-1,-1,-1),(-1,-1,1),(-1,1,1)]),
            ((0,1,0), [(1,1,-1),(-1,1,-1),(-1,1,1),(1,1,1)]),
            ((0,-1,0), [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1)]),
            ((0,0,1), [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),
            ((0,0,-1), [(-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1)]),
        ]
        vdata = GeomVertexData("box", self.box_format, Geom.UHStatic)
        vw, cw = GeomVertexWriter(vdata, "vertex"), GeomVertexWriter(vdata, "color")
        tris = GeomTriangles(Geom.UHStatic)
        idx = 0
        for normal, corners in faces:
            n = Vec3(*normal)
            color = self._shade((1.0, 1.0, 1.0), n)
            for corner in corners:
                vw.addData3f(*corner)
                cw.addData4f(*color)
            tris.addVertices(idx, idx + 1, idx + 2)
            tris.addVertices(idx, idx + 2, idx + 3)
            idx += 4
        tris.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(tris)
        node = GeomNode("box-template")
        node.addGeom(geom)
        return NodePath(node)

    def ellipsoid(self, parent, name, pos, scale, color):
        node = self.sphere_template.copyTo(parent)
        node.setName(name)
        node.setPos(*pos)
        node.setScale(*scale)
        node.setColorScale(*color, 1.0)
        node.setTwoSided(True)
        return node

    def box(self, parent, name, pos, scale, color):
        node = self.cube_template.copyTo(parent)
        node.setName(name)
        node.setPos(*pos)
        node.setScale(*scale)
        node.setColorScale(*color, 1.0)
        node.setTwoSided(True)
        return node

    def _build_room(self) -> None:
        box = self.box
        # Matte night office, dimensional desk and physical monitor.
        box(self.root, "floor", (0, 1, -0.10), (8, 7, 0.10), (0.15, 0.17, 0.17))
        box(self.root, "back-wall-left", (-4.6, 2.7, 2.8), (3.4, 0.10, 2.8), (0.23, 0.25, 0.24))
        box(self.root, "back-wall-right", (3.2, 2.7, 2.8), (3.5, 0.10, 2.8), (0.23, 0.25, 0.24))
        box(self.root, "wall-above-window", (-0.7, 2.7, 4.85), (2.5, 0.10, 0.75), (0.23, 0.25, 0.24))
        box(self.root, "wall-under-window", (-0.7, 2.7, 0.65), (2.5, 0.10, 0.65), (0.18, 0.20, 0.19))
        box(self.root, "window-night", (-0.7, 2.54, 2.75), (2.42, 0.018, 1.42), (0.045, 0.085, 0.13))
        buildings = [(-2.55, 2.48, .34, .80), (-2.04, 2.70, .42, 1.35),
                     (-1.43, 2.54, .38, .92), (-.94, 2.74, .42, 1.45),
                     (-.35, 2.52, .42, .92), (.18, 2.69, .35, 1.25)]
        for i, (x, z, width, height) in enumerate(buildings):
            self.box(self.root, f"city-tower-{i}", (x, 2.49, z), (width, .03, height),
                     (.09 + .01 * (i % 2), .13, .17 + .01 * (i % 3)))
            for r in range(4):
                for c in range(2):
                    lx = x - width * .50 + .09 + c * .15
                    lz = z - height * .44 + r * .22
                    self.box(self.root, f"city-window-{i}-{r}-{c}", (lx, 2.44, lz), (.025, .012, .035),
                             (.72, .62, .40) if (i + r + c) % 3 else (.30, .55, .62))
        for x in (-3.12, 1.72):
            box(self.root, "window-frame-vertical", (x, 2.43, 2.75), (.045, .035, 1.47), (.44, .47, .45))
        box(self.root, "window-frame-horizontal", (-.70, 2.42, 2.75), (2.48, .035, .035), (.44, .47, .45))
        # Desk top, legs, and front edge.
        box(self.root, "desk-top", (.12, .12, 1.02), (2.72, .82, .105), (.38, .27, .19))
        box(self.root, "desk-front", (.12, -.70, .80), (2.70, .07, .22), (.23, .20, .17))
        for x in (-2.25, 2.45):
            box(self.root, "desk-leg", (x, .20, .42), (.08, .72, .47), (.19, .18, .15))
        # Chair and cushion.
        box(self.root, "chair-back", (-1.25, 1.07, 1.48), (.52, .14, .58), (.10, .12, .12))
        box(self.root, "chair-seat", (-1.25, .90, .86), (.50, .48, .10), (.12, .13, .13))
        # Monitor housing, glass, pedestal and status indicator.
        box(self.root, "monitor-case", (1.22, .58, 2.08), (.91, .13, .57), (.045, .05, .055))
        box(self.root, "monitor-bezel", (1.22, .433, 2.08), (.83, .016, .49), (.055, .07, .075))
        box(self.root, "monitor-screen", (1.22, .411, 2.08), (.785, .009, .445), (.022, .039, .047))
        box(self.root, "monitor-neck", (1.22, .58, 1.43), (.095, .12, .31), (.11, .12, .12))
        box(self.root, "monitor-foot", (1.22, .49, 1.16), (.48, .26, .055), (.10, .11, .11))
        self.box(self.root, "keyboard", (-.19, -.27, 1.15), (.49, .19, .035), (.06, .07, .07))
        self.box(self.root, "mouse", (.79, -.24, 1.15), (.12, .17, .055), (.12, .13, .12))
        # Individual keycaps and an unbranded paper note.
        for row in range(4):
            for col in range(13):
                x = -.62 + col * .072
                y = -.38 + row * .073
                self.box(self.root, f"key-{row}-{col}", (x, y, 1.193), (.025, .023, .008),
                         (.32, .34, .32))
        self.box(self.root, "notebook", (-2.12, -.21, 1.14), (.25, .17, .012), (.70, .65, .53))
        # Cup and understated leafy plant for depth cues.
        self.ellipsoid(self.root, "coffee-cup", (2.05, -.22, 1.23), (.10, .10, .15), (.30, .25, .20))
        self.ellipsoid(self.root, "cup-rim", (2.05, -.22, 1.37), (.085, .085, .018), (.57, .50, .39))
        for i in range(5):
            x = 2.68 + math.sin(i * 1.4) * .20
            z = 1.55 + i * .20
            self.ellipsoid(self.root, f"plant-leaf-{i}", (x, 1.40, z), (.12, .08, .28), (.16, .31, .21))
        # A low, warm practical above the workstation.
        box(self.root, "ceiling-practical", (.40, 1.8, 4.85), (1.25, .08, .035), (.75, .67, .45))

    def _build_character(self) -> None:
        self.character = self.root.attachNewNode("Mara-procedural-3D-rig")
        self.body_root = self.character.attachNewNode("torso-root")
        # Charcoal overshirt with rust tee/collar visible at the front.
        self.ellipsoid(self.body_root, "jacket-torso", (0, 0, 0), (.42, .30, .52), (.17, .19, .18))
        self.ellipsoid(self.body_root, "rust-tee", (0, -.287, .13), (.22, .035, .36), (.54, .20, .14))
        self.ellipsoid(self.body_root, "collar-left", (-.11, -.315, .38), (.105, .028, .065), (.63, .46, .33))
        self.ellipsoid(self.body_root, "collar-right", (.11, -.315, .38), (.105, .028, .065), (.63, .46, .33))
        for z in (-.02, .20):
            self.ellipsoid(self.body_root, "jacket-button", (.17, -.315, z), (.025, .018, .025), (.68, .54, .33))
        self.ellipsoid(self.body_root, "neck", (0, -.02, .47), (.14, .14, .22), (.60, .38, .29))
        self.head = self.body_root.attachNewNode("head-joint")
        self.face = self.ellipsoid(self.head, "face", (0, 0, .77), (.31, .27, .39), (.65, .43, .32))
        self.ellipsoid(self.head, "hair-cap", (0, .025, 1.01), (.33, .29, .22), (.055, .047, .043))
        self.ellipsoid(self.head, "hair-back", (0, .16, .78), (.31, .20, .32), (.045, .039, .037))
        self.ellipsoid(self.head, "low-tied-hair", (-.03, .30, .69), (.12, .15, .14), (.052, .044, .04))
        self.eyes = []
        self.pupils = []
        for ex in (-.115, .105):
            eye = self.ellipsoid(self.head, "eye", (ex, -.246, .79), (.055, .036, .061), (.91, .85, .71))
            pupil = self.ellipsoid(self.head, "pupil", (ex + .025, -.279, .787), (.022, .015, .032), (.035, .029, .024))
            self.ellipsoid(self.head, "eyebrow", (ex, -.251, .89), (.070, .023, .021), (.08, .055, .046))
            self.eyes.append(eye)
            self.pupils.append(pupil)
        self.ellipsoid(self.head, "nose", (.065, -.274, .72), (.045, .052, .062), (.58, .36, .27))
        self.ellipsoid(self.head, "mouth", (.09, -.264, .62), (.068, .018, .012), (.25, .10, .08))
        self.ellipsoid(self.head, "ear-left", (-.31, .0, .76), (.06, .09, .09), (.58, .37, .29))
        self.ellipsoid(self.head, "ear-right", (.31, .0, .76), (.06, .09, .09), (.58, .37, .29))
        self.shoulder_left = (-.34, -.04, .27)
        self.shoulder_right = (.34, -.04, .27)
        self.upper_left = self.ellipsoid(self.character, "upper-arm-far", (0,0,0), (.13,.40,.13), (.18,.20,.19))
        self.lower_left = self.ellipsoid(self.character, "forearm-far", (0,0,0), (.09,.35,.09), (.62,.40,.30))
        self.upper_right = self.ellipsoid(self.character, "upper-arm-near", (0,0,0), (.15,.40,.15), (.17,.19,.18))
        self.lower_right = self.ellipsoid(self.character, "forearm-near", (0,0,0), (.095,.35,.095), (.62,.40,.30))
        self.hand_left = self.ellipsoid(self.character, "hand-far", (0,0,0), (.12,.11,.06), (.65,.43,.32))
        self.hand_right = self.ellipsoid(self.character, "hand-near", (0,0,0), (.125,.11,.06), (.65,.43,.32))
        self.fingers = []
        for near in (False, True):
            group = []
            for i in range(4):
                group.append(self.ellipsoid(self.character, "finger", (0,0,0), (.022,.085,.022), (.65,.43,.32)))
            self.fingers.append(group)
        self.head_glance = 0.0

    def _build_ui(self) -> None:
        self.ui_text = []
        font = self.base.loader.loadFont(FONT_MONO)
        if font is None:
            font = self.base.loader.loadFont("cmr12.egg")
        rows_z = (2.38, 2.19, 2.00, 1.81, 1.65)
        for i, z in enumerate(rows_z):
            tn = TextNode(f"screen-row-{i}")
            tn.setText("")
            tn.setFont(font)
            tn.setAlign(TextNode.ALeft)
            tn.setTextColor(.72, .80, .76, 1)
            np = self.root.attachNewNode(tn)
            np.setPos(.50, .398, z)
            np.setScale(.092 if i == 0 else .077)
            self.ui_text.append((tn, np))
        self.cursor = self.ellipsoid(self.root, "screen-cursor", (1.25, .385, 1.80), (.035,.012,.045), (.94,.92,.80))
        self.cursor.hide()
        self._last_ui_key = None

    @staticmethod
    def _screen_state(t: float) -> tuple[list[str], list[tuple[float,float,float,float]]]:
        white = (.80,.86,.82,1)
        green = (.38,.82,.55,1)
        amber = (.89,.61,.31,1)
        muted = (.54,.63,.61,1)
        if t < 23:
            stage = min(4, int(t / 5.5) + 1)
            lines = ["TERN / RELAY", "READY 200   p99 94ms", f"rollout stage {stage}/4",
                     "CANARY 5%    CI PASS", "receipt sample 1204/1204"]
            colors = [white, green, muted, green, muted]
        elif t < 34:
            q = int(mix(184,19408,smooth(23,33,t)))
            age = int(mix(8,372,smooth(23,33,t)))
            age_text = f"{age:02d}s" if age < 60 else f"{age//60}m {age%60:02d}s"
            lines = ["ASYNC ACTION QUEUE", "READY 200   p99 94ms", f"depth {q:>6,} age {age_text}",
                     "queue oldest is rising", "ingress ack != action complete"]
            colors = [white, green, amber, amber, muted]
        elif t < 48:
            lines = ["TRACE dispatch.materialize", "source alarm-77 / d-A1", "POST timeout 2000ms",
                     "source alarm-77 / d-B2", "receipt 201 / +1.7s late"]
            colors = [white, muted, amber, amber, amber]
        elif t < 53:
            lines = ["INCIDENT ACTION", "Pause outbound dispatch?", "raw intake stays durable",
                     "operator confirmation required", "CONFIRM HOLD  >"]
            colors = [white, amber, green, muted, amber]
        else:
            lines = ["OUTBOUND PUBLISHER: PAUSED", "RAW INTAKE: PRESERVED", "OUTBOUND REQUESTS: 0",
                     "source timeline retained", "operator confirmation required"]
            colors = [amber, green, white, muted, muted]
        return lines, colors

    def _place_segment(self, node, a, b, radius: float) -> None:
        a, b = Vec3(*a), Vec3(*b)
        delta = b - a
        node.setPos((a + b) * .5)
        node.setScale(radius, max(.06, delta.length() * .5), radius)
        node.lookAt(b)

    def update(self, t: float) -> None:
        typing = 1.0 - smooth(23.0, 27.0, t)
        anomaly = smooth(24.0, 28.0, t)
        inspect = smooth(34.0, 39.0, t)
        reach = smooth(46.0, 51.0, t)
        settle = smooth(54.0, 59.0, t)
        breath = math.sin(t * 1.55) * .018
        lean = .10 * anomaly + .07 * inspect - .08 * settle
        base_x, base_y = -1.25, .91
        self.character.setPos(base_x, base_y, 0)
        self.body_root.setPos(0, 0, 1.48 + breath)
        self.body_root.setH(-4.0 + 7.0 * inspect)
        self.head.setPos(0, 0, .04 * inspect)
        self.head.setH(20 + 24 * anomaly + 12 * inspect - 15 * settle)
        self.head.setP(-3 + 5 * anomaly + 3 * inspect)
        blink = max(math.exp(-((t - b) / .11) ** 2) for b in (8.0,17.1,28.2,42.5,57.0))
        for eye in self.eyes:
            eye.setScale(.055,.036,max(.008,.061*(1-blink)))
        for pupil in self.pupils:
            pupil.setX(pupil.getX() + .0)  # retain its rigged eye position
        # Arms are individual 3D ellipsoidal bones repositioned between live joint targets.
        shoulders = [(-.34,-.03,1.75+breath),(.34,-.03,1.75+breath)]
        elbows = [(-.10,-.54,1.40-.06*anomaly),(.62,-.55,1.42-.10*inspect)]
        wrist_far = (.78,-1.16,1.22 + .025*math.sin(t*11.0)*typing)
        wrist_near = (mix(1.15,2.04,reach),-1.15,1.21 + .025*math.sin(t*13.0)*typing)
        wrists = [wrist_far,wrist_near]
        nodes = [(self.upper_left,self.lower_left,self.hand_left),
                 (self.upper_right,self.lower_right,self.hand_right)]
        for i,(upper,lower,hand) in enumerate(nodes):
            self._place_segment(upper,shoulders[i],elbows[i],.135 if i==0 else .145)
            self._place_segment(lower,elbows[i],wrists[i],.092 if i==0 else .098)
            hand.setPos(*wrists[i])
            hand.setH(-5 + 8*reach)
            for k,finger in enumerate(self.fingers[i]):
                tap = math.sin(t*12.5 + k*1.3) * .025 * typing
                fx = wrists[i][0] - .07 + k*.045
                fy = wrists[i][1] - .09
                fz = wrists[i][2] - .01 + tap
                finger.setPos(fx,fy,fz)
                finger.setH(-3 + 12*reach)
        # Hand/cursor converge on the hold control. The on-screen cursor follows the gesture.
        self.cursor.setPos(mix(1.68,1.34,reach),.385,mix(1.85,1.71,reach))
        if t >= 43:
            self.cursor.show()
        else:
            self.cursor.hide()
        # Soft posture response: lean into evidence, then settle into an unresolved hold.
        self.body_root.setX(lean)
        key = int(t * 2)
        if key != self._last_ui_key:
            lines, colors = self._screen_state(t)
            for (tn,_), line, color in zip(self.ui_text,lines,colors):
                tn.setText(line)
                tn.setTextColor(*color)
            self._last_ui_key=key
        # Motivated, continuous dolly/pan between the workstation and monitor.
        if t < 12:
            u=smooth(0,12,t)
            p0=(0.0,-8.2,3.05); p1=(.10,-7.8,2.92); q0=(0,.45,1.60); q1=(.1,.48,1.68)
        elif t < 24:
            u=smooth(12,24,t)
            p0=(.10,-7.8,2.92); p1=(.15,-6.6,2.70); q0=(.1,.48,1.68); q1=(.2,.50,1.78)
        elif t < 35:
            u=smooth(24,35,t)
            p0=(.15,-6.6,2.70); p1=(.42,-5.9,2.62); q0=(.2,.50,1.78); q1=(.42,.48,1.85)
        elif t < 48:
            u=smooth(35,48,t)
            p0=(.42,-5.9,2.62); p1=(.74,-5.7,2.55); q0=(.42,.48,1.85); q1=(.78,.45,1.92)
        else:
            u=smooth(48,60,t)
            p0=(.74,-5.7,2.55); p1=(.08,-8.0,2.92); q0=(.78,.45,1.92); q1=(.08,.48,1.68)
        cam=tuple(mix(a,b,u) for a,b in zip(p0,p1))
        look=tuple(mix(a,b,u) for a,b in zip(q0,q1))
        self.base.camera.setPos(*cam)
        self.base.camera.lookAt(*look)

    def render_frame(self, t: float, out_path: Path) -> None:
        self.update(t)
        self.base.graphicsEngine.renderFrame()
        self.base.graphicsEngine.renderFrame()
        image = PNMImage()
        if not self.base.win.getScreenshot(image):
            raise RuntimeError(f"TinyDisplay could not capture frame at t={t:.3f}s")
        if image.getXSize() != W or image.getYSize() != H:
            raise RuntimeError(f"Unexpected screenshot size {image.getXSize()}x{image.getYSize()}")
        temp = out_path.with_suffix(".tmp.png")
        image.write(str(temp))
        with Image.open(temp) as im:
            canvas=im.convert("RGB")
        temp.unlink(missing_ok=True)
        if t >= 57.5:
            draw=ImageDraw.Draw(canvas)
            f=ImageFont.truetype(FONT_MONO,10)
            draw.text((24,H-23),"60-SECOND 3D PROCEDURAL PROOF OF CONCEPT  •  NOT THE FINISHED FILM",font=f,fill=(177,183,177))
        canvas.save(out_path,optimize=False)

    def close(self) -> None:
        self.base.destroy()


def render(output: Path, seconds: int, ffmpeg: str) -> None:
    if seconds < 5 or seconds > 120:
        raise ValueError("Duration must be between 5 and 120 seconds")
    if not Path(ffmpeg).is_file():
        raise FileNotFoundError(f"FFmpeg executable not found: {ffmpeg}")
    output.parent.mkdir(parents=True,exist_ok=True)
    sys.dont_write_bytecode = True
    sys.path.insert(0,str(PROJECT/"scripts"))
    import render_poc
    frame_count=seconds*FPS
    with tempfile.TemporaryDirectory(prefix="zero-day-3d-") as td:
        temp=Path(td)
        frames=temp/"frames"
        frames.mkdir()
        wav=temp/"soundscape.wav"
        render_poc.write_soundscape(wav,seconds)
        scene=Scene()
        try:
            for i in range(frame_count):
                t=i/FPS
                scene.render_frame(t,frames/f"frame_{i:06d}.png")
                if (i+1)%120==0:
                    print(f"Rendered {i+1}/{frame_count} frames ({(i+1)/FPS:.1f}s)",flush=True)
        finally:
            scene.close()
        cmd=[ffmpeg,"-hide_banner","-loglevel","warning","-y",
             "-framerate",str(FPS),"-start_number","0","-i",str(frames/"frame_%06d.png"),
             "-i",str(wav),"-map","0:v:0","-map","1:a:0",
             "-frames:v",str(frame_count),"-r",str(FPS),"-fps_mode","cfr",
             "-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",
             "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",
             "-t",str(seconds),"-movflags","+faststart",
             "-metadata","title=PROJECT ZERO-DAY: THE LAST DEPLOY — 3D Proof of Concept",
             "-metadata","comment=CPU-rendered procedural 3D performance proof; not the finished film",
             str(output.resolve())]
        proc=subprocess.run(cmd,capture_output=True,text=True)
        if proc.returncode:
            raise RuntimeError(f"FFmpeg failed with {proc.returncode}: {proc.stderr[-4000:]}")
    if not output.exists() or output.stat().st_size < 100_000:
        raise RuntimeError("3D render output missing or unexpectedly small")
    print(f"Rendered {output.resolve()} ({output.stat().st_size:,} bytes, {seconds}s target, {frame_count} frames)")


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=PROJECT/"renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4")
    parser.add_argument("--seconds",type=int,default=60)
    parser.add_argument("--ffmpeg",default=os.environ.get("FFMPEG_BINARY", ""))
    args=parser.parse_args()
    if not args.ffmpeg:
        import imageio_ffmpeg
        args.ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    render(args.output, args.seconds, args.ffmpeg)


if __name__ == "__main__":
    main()
