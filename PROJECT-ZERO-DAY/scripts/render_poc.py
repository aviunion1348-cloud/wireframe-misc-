#!/usr/bin/env python3
"""Render a 60-second, stylized 2D motion-animation proof of concept.

This is a deliberately disclosed fallback, not live-action, Blender 3D,
photorealistic footage, or the completed feature. Every video frame is freshly
drawn from animated character poses, hand movement, changing software UI, and
a camera move; no still image is panned/zoomed to simulate performance.

Runtime dependencies are installed outside the repository:
  PYTHONPATH=/tmp/zero-day-py
  FFMPEG_BINARY=/tmp/zero-day-py/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
"""
from __future__ import annotations

import argparse
import math
import os
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
CINEMA_H = 536  # 2.388:1 active picture in a 16:9 frame
BAR_TOP = (H - CINEMA_H) // 2
FPS = 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT)
    return ImageFont.truetype(path, size=size)


def clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def smooth(a: float, b: float, x: float) -> float:
    u = clamp01((x - a) / (b - a))
    return u * u * (3.0 - 2.0 * u)


def mix(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


def draw_gradient(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], top, bottom) -> None:
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        q = (y - y0) / span
        c = tuple(round(mix(top[k], bottom[k], q)) for k in range(3))
        draw.line((x0, y, x1, y), fill=c)


def draw_background(im: Image.Image, t: float) -> None:
    d = ImageDraw.Draw(im, "RGB")
    draw_gradient(d, (0, 0, W - 1, CINEMA_H - 1), (35, 42, 46), (53, 56, 52))

    # Window and a quiet, fictional industrial city at night.
    d.rounded_rectangle((38, 32, 435, 327), radius=5, fill=(14, 22, 29), outline=(116, 122, 119), width=3)
    draw_gradient(d, (45, 39, 428, 320), (34, 50, 61), (88, 89, 77))
    d.rectangle((45, 224, 428, 320), fill=(29, 42, 47))
    city = [(60, 180, 110, 320), (116, 150, 171, 320), (178, 205, 235, 320),
            (245, 169, 290, 320), (300, 133, 351, 320), (358, 197, 416, 320)]
    for i, (x0, y0, x1, y1) in enumerate(city):
        d.rectangle((x0, y0, x1, y1), fill=(38 + i % 3 * 2, 48 + i % 2 * 4, 52 + i % 3 * 2))
        for yy in range(y0 + 12, y1 - 8, 19):
            for xx in range(x0 + 8, x1 - 4, 15):
                lit = ((xx * 7 + yy * 11 + i * 13) % 9) in (0, 3)
                if lit:
                    col = (176, 157, 111) if (xx + yy) % 2 else (100, 153, 161)
                    d.rectangle((xx, yy, xx + 4, yy + 6), fill=col)
    d.line((235, 39, 235, 320), fill=(112, 117, 114), width=3)
    d.line((46, 179, 428, 179), fill=(108, 115, 114), width=2)
    d.line((47, 317, 427, 317), fill=(177, 175, 159), width=4)

    # Wall panels, acoustic treatment, framed site map and practical ceiling light.
    d.rectangle((445, 35, 1260, 332), fill=(51, 56, 54))
    for x in (474, 516, 558, 1178, 1220):
        d.line((x, 45, x, 327), fill=(61, 66, 63), width=2)
    d.rounded_rectangle((485, 67, 584, 143), radius=3, fill=(40, 46, 45), outline=(94, 99, 95), width=2)
    d.line((498, 87, 571, 87), fill=(109, 123, 116), width=2)
    d.line((498, 100, 558, 100), fill=(85, 111, 111), width=2)
    d.line((498, 113, 568, 113), fill=(101, 105, 93), width=2)
    # Practical light source and bounce.
    d.rounded_rectangle((670, 25, 1015, 35), radius=5, fill=(197, 189, 161))
    d.rectangle((681, 35, 1002, 39), fill=(118, 116, 99))
    # Office plant with offset, individually drawn leaves.
    d.rounded_rectangle((1150, 283, 1215, 334), radius=7, fill=(91, 72, 58))
    for i in range(7):
        sway = math.sin(t * 0.65 + i * 0.7) * 3
        x = 1181 + int(math.cos(i * 0.9) * (12 + i % 3 * 4) + sway)
        y = 285 - int(i * 11)
        d.line((1180, 306, x, y), fill=(73, 112, 84), width=3)
        d.ellipse((x - 10, y - 6, x + 10, y + 7), fill=(65, 99, 73), outline=(83, 118, 89))

    # Floor and practical light pools.
    d.rectangle((0, 327, W, CINEMA_H), fill=(40, 44, 42))
    d.line((0, 328, W, 328), fill=(90, 92, 83), width=2)
    for x in range(30, W, 120):
        d.line((x, 330, x - 16, CINEMA_H), fill=(45, 49, 46), width=1)


def draw_desk_and_props(im: Image.Image, t: float) -> None:
    d = ImageDraw.Draw(im, "RGB")
    # Desk, front fascia, monitor stand, laptop dock.
    d.polygon([(270, 354), (1199, 354), (1245, 384), (300, 384)], fill=(106, 87, 70), outline=(139, 117, 94))
    d.polygon([(300, 384), (1245, 384), (1231, 432), (300, 432)], fill=(67, 59, 51), outline=(89, 78, 67))
    d.polygon([(315, 432), (345, 432), (353, 518), (330, 518)], fill=(54, 51, 46))
    d.polygon([(1160, 432), (1190, 432), (1200, 518), (1173, 518)], fill=(54, 51, 46))
    d.polygon([(914, 342), (1040, 342), (1054, 356), (900, 356)], fill=(45, 48, 47))
    d.rectangle((968, 326, 985, 350), fill=(53, 56, 54))

    # Keyboard and a paper incident notebook.
    d.rounded_rectangle((696, 361, 854, 385), radius=5, fill=(35, 39, 40), outline=(119, 119, 106), width=2)
    for row in range(2):
        for col in range(11):
            x = 706 + col * 13
            y = 367 + row * 8
            d.rounded_rectangle((x, y, x + 9, y + 4), radius=1, fill=(108, 112, 105))
    d.rounded_rectangle((338, 346, 438, 363), radius=2, fill=(179, 168, 143), outline=(91, 82, 70), width=1)
    d.line((349, 351, 421, 351), fill=(93, 94, 85), width=1)
    d.line((349, 356, 411, 356), fill=(93, 94, 85), width=1)
    d.line((349, 360, 417, 360), fill=(93, 94, 85), width=1)
    d.ellipse((455, 350, 484, 379), fill=(47, 48, 46), outline=(141, 132, 112), width=2)
    d.arc((459, 346, 480, 359), 180, 355, fill=(142, 135, 117), width=2)
    # Coffee ring, not a brand.
    d.ellipse((1133, 357, 1158, 377), outline=(155, 143, 116), width=2)


_STATIC_STAGE: Image.Image | None = None


def static_stage() -> Image.Image:
    """Cache set dressing; the character, camera, and software UI still animate per frame."""
    global _STATIC_STAGE
    if _STATIC_STAGE is None:
        stage = Image.new("RGB", (W, CINEMA_H), (30, 36, 38))
        draw_background(stage, 0.0)
        draw_desk_and_props(stage, 0.0)
        _STATIC_STAGE = stage
    return _STATIC_STAGE


def draw_screen(im: Image.Image, t: float, cursor: tuple[float, float]) -> None:
    d = ImageDraw.Draw(im, "RGB")
    # Perspective monitor body, bevel, stand and screen glass.
    d.polygon([(814, 64), (1179, 82), (1181, 323), (814, 310)], fill=(19, 23, 25), outline=(119, 124, 119))
    d.polygon([(826, 77), (1167, 92), (1168, 307), (826, 296)], fill=(18, 25, 30))
    d.polygon([(826, 77), (1167, 92), (1168, 307), (826, 296)], outline=(82, 92, 94))
    # UI panel, slightly skewed with the screen.
    d.polygon([(838, 88), (1157, 101), (1158, 295), (838, 284)], fill=(25, 34, 40))
    d.polygon([(838, 88), (1157, 101), (1158, 121), (838, 108)], fill=(35, 47, 55))
    d.text((848, 91), "TERN  /  RELAY", font=font(12, bold=True), fill=(222, 228, 224))
    d.text((1041, 94), "prod  •  21:14Z", font=font(9, mono=True), fill=(163, 181, 178))
    d.line((840, 124, 1155, 136), fill=(56, 69, 73), width=1)

    # Status tiles stay intentionally legible: liveness is green while business work backs up.
    d.rounded_rectangle((846, 132, 973, 169), radius=4, fill=(37, 64, 55), outline=(72, 123, 95))
    d.text((854, 136), "READY 200", font=font(12, bold=True), fill=(163, 222, 181))
    d.text((854, 152), "/readyz  db + broker", font=font(8, mono=True), fill=(176, 195, 184))
    d.rounded_rectangle((982, 132, 1149, 169), radius=4, fill=(39, 48, 51), outline=(74, 87, 88))
    d.text((990, 136), "p99  94 ms", font=font(12, bold=True), fill=(171, 211, 187))
    d.text((990, 152), "ingress only", font=font(8, mono=True), fill=(158, 174, 173))

    if t < 23:
        d.text((848, 178), "RELEASE 4.18  /  CANARY 5%", font=font(9, mono=True), fill=(213, 219, 215))
        d.text((849, 194), "CI   PASS", font=font(10, bold=True), fill=(141, 212, 164))
        d.text((916, 194), "deploy artifact: sha-71c4", font=font(8, mono=True), fill=(156, 173, 173))
        # Progress line, with a real time-varying reveal.
        d.rounded_rectangle((849, 215, 1147, 224), radius=4, fill=(47, 58, 60))
        p = 0.14 + 0.40 * smooth(1, 19, t)
        d.rounded_rectangle((849, 215, 849 + int(298 * p), 224), radius=4, fill=(85, 162, 128))
        d.text((849, 233), "source events", font=font(8, mono=True), fill=(143, 158, 158))
        d.text((1010, 233), "actions sent", font=font(8, mono=True), fill=(143, 158, 158))
        d.text((849, 249), "1,204", font=font(12, mono=True, bold=True), fill=(216, 223, 216))
        d.text((1010, 249), "1,204", font=font(12, mono=True, bold=True), fill=(216, 223, 216))
        d.text((849, 270), "receipt sample  /  no provider retry observed", font=font(8, mono=True), fill=(143, 164, 157))
    elif t < 34:
        q = int(mix(184, 19408, smooth(23, 33, t)))
        age_s = int(mix(8, 372, smooth(23, 33, t)))
        age_label = f"{age_s:02d}s" if age_s < 60 else f"{age_s // 60}m {age_s % 60:02d}s"
        d.text((848, 178), "ASYNC ACTION QUEUE", font=font(9, mono=True), fill=(213, 219, 215))
        d.text((849, 193), f"depth   {q:>6,}", font=font(12, mono=True, bold=True), fill=(232, 174, 104))
        d.text((1016, 193), f"age   {age_label}", font=font(10, mono=True), fill=(224, 184, 120))
        # Rising queue graph while the green HTTP health tile remains green.
        pts = []
        for i in range(18):
            xx = 851 + i * 16
            base = 260 - i * 1.2
            rise = max(0, i - 5) ** 1.55 * 0.95 * smooth(23, 33, t)
            jitter = math.sin(i * 2.1 + t) * 2
            pts.append((xx, int(base - rise + jitter)))
        d.line(pts, fill=(226, 150, 95), width=3)
        d.line((848, 263, 1146, 263), fill=(59, 68, 70), width=1)
        d.text((848, 276), "acknowledged at ingress  ≠  action complete", font=font(7, mono=True), fill=(179, 187, 177))
        if t > 27:
            d.rounded_rectangle((1091, 174, 1146, 187), radius=3, fill=(105, 75, 43))
            d.text((1098, 176), "LAG ↑", font=font(8, bold=True), fill=(250, 204, 129))
    elif t < 48:
        d.text((848, 178), "TRACE / dispatch.materialize", font=font(9, mono=True), fill=(211, 221, 215))
        d.text((849, 194), "source_event_id  alarm-77", font=font(8, mono=True), fill=(176, 204, 193))
        d.text((849, 210), "delivery_id      d-A1", font=font(8, mono=True), fill=(215, 218, 204))
        d.text((849, 225), "POST /actions     timeout 2000ms", font=font(8, mono=True), fill=(229, 167, 110))
        d.line((849, 240, 1145, 240), fill=(59, 71, 74), width=1)
        d.text((849, 247), "source_event_id  alarm-77", font=font(8, mono=True), fill=(176, 204, 193))
        d.text((849, 263), "delivery_id      d-B2", font=font(8, mono=True), fill=(231, 175, 121))
        d.text((849, 278), "receipt 201      +1.7s after timeout", font=font(7, mono=True), fill=(225, 183, 119))
        if t > 40:
            d.rounded_rectangle((1050, 175, 1147, 189), radius=3, fill=(78, 49, 46))
            d.text((1057, 177), "DUPLICATE?", font=font(7, bold=True), fill=(235, 152, 135))
    else:
        d.text((848, 178), "INCIDENT ACTION", font=font(9, mono=True), fill=(211, 221, 215))
        d.text((849, 195), "Pause downstream dispatch?", font=font(11, bold=True), fill=(230, 231, 220))
        d.text((849, 216), "raw intake remains durable", font=font(8, mono=True), fill=(171, 194, 182))
        d.rounded_rectangle((849, 240, 1145, 274), radius=4, fill=(92, 57, 49), outline=(165, 106, 80), width=2)
        d.text((867, 249), "CONFIRM HOLD", font=font(12, bold=True), fill=(250, 215, 188))
        if t >= 53:
            d.rectangle((838, 88, 1158, 295), fill=(24, 39, 39))
            d.text((852, 115), "OUTBOUND PUBLISHER: PAUSED", font=font(12, mono=True, bold=True), fill=(228, 186, 126))
            d.text((852, 147), "RAW INTAKE: PRESERVED", font=font(12, mono=True), fill=(160, 222, 180))
            d.text((852, 179), "OUTBOUND REQUESTS: 0", font=font(11, mono=True), fill=(203, 216, 208))
            d.text((852, 222), "source timeline retained", font=font(9, mono=True), fill=(151, 177, 169))
            d.text((852, 255), "operator confirmation required", font=font(8, mono=True), fill=(156, 178, 169))

    # Subtle translucent glass reflection; preserve the legibility of the interface.
    reflection = Image.new("RGBA", (W, CINEMA_H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(reflection)
    rd.polygon([(844, 91), (858, 92), (928, 286), (913, 285)], fill=(138, 174, 184, 24))
    im.paste(Image.alpha_composite(im.convert("RGBA"), reflection).convert("RGB"))
    d = ImageDraw.Draw(im, "RGB")
    d.line((817, 314, 1180, 327), fill=(107, 111, 105), width=2)
    # Moving pointer, tied to the animated mouse hand beat.
    mx, my = cursor
    if t >= 43:
        d.polygon([(int(mx), int(my)), (int(mx), int(my + 13)), (int(mx + 4), int(my + 10)),
                   (int(mx + 8), int(my + 17)), (int(mx + 11), int(my + 15)),
                   (int(mx + 7), int(my + 8)), (int(mx + 14), int(my + 8))],
                  fill=(246, 246, 232), outline=(28, 32, 33))


def draw_character(im: Image.Image, t: float) -> tuple[float, float]:
    d = ImageDraw.Draw(im, "RGB")
    anomaly = smooth(24.2, 27.0, t)
    investigate = smooth(34.8, 39.0, t)
    decide = smooth(48.0, 53.5, t)
    breathe = math.sin(t * 1.7) * 1.8
    lean = 13.0 * anomaly + 9.0 * investigate - 12.0 * smooth(54.0, 59.0, t)
    head_x = 588 + lean
    head_y = 143 + breathe

    # Chair silhouette and back cushion.
    d.rounded_rectangle((480, 234, 574, 366), radius=23, fill=(38, 45, 46), outline=(77, 84, 82), width=3)
    d.ellipse((508, 348, 565, 395), fill=(40, 46, 45), outline=(79, 84, 81), width=2)

    # Torso: tailored rust-colored overshirt over a dark base, with soft shadow planes.
    body_left = 526 + int(lean * 0.45)
    body_right = 654 + int(lean * 0.55)
    d.polygon([(body_left + 20, 226 + breathe), (body_left + 55, 215 + breathe),
               (body_right - 16, 224 + breathe), (body_right + 1, 348),
               (body_right - 10, 370), (body_left - 6, 370), (body_left - 19, 324)],
              fill=(119, 69, 57), outline=(57, 45, 41))
    d.polygon([(body_left + 36, 230 + breathe), (body_left + 65, 221 + breathe),
               (body_left + 78, 359), (body_left + 42, 365)], fill=(148, 82, 65))
    d.polygon([(body_right - 35, 232 + breathe), (body_right - 10, 225 + breathe),
               (body_right + 1, 348), (body_right - 8, 369), (body_right - 37, 358)], fill=(94, 58, 52))
    d.line((body_left + 71, 230, body_left + 82, 356), fill=(192, 133, 104), width=2)
    d.ellipse((body_left + 74, 268, body_left + 81, 275), fill=(210, 178, 132))
    d.ellipse((body_left + 77, 306, body_left + 84, 313), fill=(210, 178, 132))

    # Neck and visible collar.
    d.polygon([(head_x - 17, head_y + 52), (head_x + 22, head_y + 50),
               (head_x + 30, head_y + 102), (head_x - 14, head_y + 105)], fill=(177, 119, 92))
    d.polygon([(head_x - 35, 225 + breathe), (head_x - 10, 216 + breathe),
               (head_x + 2, 242), (head_x - 18, 255)], fill=(189, 151, 116))
    d.polygon([(head_x + 2, 242), (head_x + 20, 217 + breathe),
               (head_x + 43, 229 + breathe), (head_x + 20, 257)], fill=(135, 91, 72))

    # Arms pose around keyboard/mouse. The wrist travels from keyboard to mouse during the hold decision.
    shoulder = (body_right - 18, 248 + int(breathe))
    typing = 1.0 - smooth(24.0, 27.0, t)
    mouse_move = smooth(45.5, 50.5, t)
    keyboard_wrist = (780 + int(2 * math.sin(t * 9.0)), 344 + int(3 * math.sin(t * 13.0)) if t < 25 else 346)
    mouse_wrist = (859 + int(12 * math.sin(t * 2.8)), 346 + int(2 * math.sin(t * 4.0)))
    wrist = (mix(keyboard_wrist[0], mouse_wrist[0], mouse_move), mix(keyboard_wrist[1], mouse_wrist[1], mouse_move))
    elbow = (706 + int(lean * 0.45), 294 - int(investigate * 10) + int(2 * math.sin(t * 1.2)))
    sleeve_end = (elbow[0], elbow[1] + 3)
    # Far arm, mostly resting at desk.
    d.line(((body_left + 37, 247), (body_left + 12, 293), (690, 345)), fill=(112, 66, 55), width=30, joint="curve")
    d.line(((body_left + 35, 248), (body_left + 14, 294), (687, 343)), fill=(151, 87, 68), width=21, joint="curve")
    d.ellipse((678, 336, 704, 354), fill=(185, 126, 97), outline=(80, 58, 49), width=2)
    for k in range(3):
        y = 343 + k * 3
        d.line((695, y, 714 + k * 4, y + 3), fill=(174, 116, 89), width=3)

    # Near sleeve, forearm and live hand pose.
    d.line((shoulder, sleeve_end), fill=(93, 57, 50), width=35, joint="curve")
    d.line((shoulder, sleeve_end), fill=(142, 78, 62), width=26, joint="curve")
    d.line((sleeve_end, elbow), fill=(151, 91, 71), width=21, joint="curve")
    d.line((elbow, (wrist[0] - 10, wrist[1])), fill=(190, 130, 99), width=17, joint="curve")
    d.ellipse((wrist[0] - 14, wrist[1] - 8, wrist[0] + 14, wrist[1] + 8), fill=(194, 135, 103), outline=(91, 64, 51), width=2)
    # Fingers tap the keys, then extend toward the hold control.
    finger = math.sin(t * 12.5) * 3 * typing
    if t < 47:
        for i in range(4):
            x = int(wrist[0] - 8 + i * 5)
            yy = int(wrist[1] + 4 + (finger if i % 2 == 0 else -finger))
            d.line((x, yy, x + 4, yy + 8), fill=(210, 153, 117), width=3)
    else:
        reach = smooth(47, 52, t)
        d.line((int(wrist[0]), int(wrist[1]), int(wrist[0] + 12 * reach), int(wrist[1] - 12 * reach)), fill=(205, 148, 113), width=4)
        d.ellipse((int(wrist[0] + 8 * reach), int(wrist[1] - 15 * reach),
                   int(wrist[0] + 15 * reach), int(wrist[1] - 8 * reach)), fill=(227, 177, 136))

    # Face and hair are drawn last over neck/collar; restrained eye and head movements sell the realization.
    d.ellipse((head_x - 40, head_y - 13, head_x + 37, head_y + 73), fill=(185, 128, 100), outline=(75, 53, 45), width=2)
    d.polygon([(head_x + 6, head_y + 5), (head_x + 39, head_y + 23),
               (head_x + 54, head_y + 38), (head_x + 37, head_y + 45),
               (head_x + 21, head_y + 38)], fill=(184, 124, 96), outline=(86, 56, 46))
    # Monitor light on the nose/cheek; the office practical remains visible.
    d.ellipse((head_x + 5, head_y + 25, head_x + 35, head_y + 52), fill=(191, 145, 114))
    d.ellipse((head_x - 43, head_y + 21, head_x - 25, head_y + 44), fill=(178, 117, 91), outline=(82, 58, 48), width=2)
    # Hair cap, fringe and a tied-back section.
    d.pieslice((head_x - 46, head_y - 28, head_x + 40, head_y + 51), 180, 355, fill=(37, 34, 33), outline=(24, 25, 25))
    d.polygon([(head_x - 43, head_y + 8), (head_x - 19, head_y - 22),
               (head_x + 15, head_y - 21), (head_x + 36, head_y + 2),
               (head_x + 17, head_y + 15), (head_x - 5, head_y + 6),
               (head_x - 28, head_y + 20)], fill=(39, 35, 33))
    d.line((head_x - 29, head_y - 8, head_x - 11, head_y + 12), fill=(74, 61, 54), width=2)
    d.line((head_x - 15, head_y - 15, head_x + 1, head_y + 8), fill=(65, 54, 48), width=2)
    d.ellipse((head_x - 50, head_y + 5, head_x - 33, head_y + 23), fill=(42, 38, 36))

    # Eye line: stops scanning when the anomaly appears; one timed blink.
    blink = max(math.exp(-((t - q) / 0.12) ** 2) for q in (8.0, 17.1, 28.2, 42.5, 57.0))
    eye_y = head_y + 28 + int(anomaly * 1.0)
    eye_x = head_x + 20
    d.line((eye_x - 7, eye_y - 10, eye_x + 11, eye_y - 12), fill=(61, 44, 38), width=3)
    if blink > 0.82:
        d.line((eye_x - 3, eye_y, eye_x + 7, eye_y), fill=(56, 42, 38), width=2)
    else:
        d.ellipse((eye_x - 4, eye_y - 3, eye_x + 8, eye_y + 4), fill=(233, 218, 194))
        gaze = int(2 * math.sin(t * 1.7) + anomaly * 2)
        d.ellipse((eye_x + gaze, eye_y - 2, eye_x + gaze + 4, eye_y + 3), fill=(51, 44, 39))
        d.ellipse((eye_x + gaze + 1, eye_y - 1, eye_x + gaze + 2, eye_y), fill=(240, 229, 208))
    d.line((head_x + 42, head_y + 56, head_x + 50, head_y + 57), fill=(108, 67, 57), width=2)
    # Subtle cheek highlight and hair strands, not artificial grain.
    d.arc((head_x + 7, head_y + 33, head_x + 36, head_y + 60), 200, 285, fill=(213, 164, 126), width=2)
    d.line((head_x - 37, head_y + 4, head_x - 28, head_y + 36), fill=(80, 65, 58), width=1)

    # Small serial-coded lapel pin is a repeatable costume cue.
    d.ellipse((body_right - 31, 267, body_right - 24, 274), fill=(197, 170, 124))
    return wrist


def camera_for_time(t: float) -> tuple[float, float, float]:
    if t < 12:
        p = smooth(0, 12, t)
        return 640 + 18 * p, 268, mix(0.98, 1.05, p)
    if t < 24:
        p = smooth(12, 24, t)
        return mix(960, 985, p), mix(230, 229, p), mix(1.15, 1.32, p)
    if t < 35:
        p = smooth(24, 35, t)
        return mix(604, 617, p), 202, mix(1.35, 1.52, p)
    if t < 48:
        p = smooth(35, 48, t)
        return mix(884, 930, p), mix(231, 235, p), mix(1.27, 1.40, p)
    p = smooth(48, 60, t)
    return mix(932, 860, p), mix(229, 244, p), mix(1.42, 1.13, p)


def camera_transform(content: Image.Image, t: float) -> Image.Image:
    cx, cy, zoom = camera_for_time(t)
    a = 1.0 / zoom
    tx = cx - W * 0.5 * a
    ty = cy - CINEMA_H * 0.5 * a
    return content.transform((W, CINEMA_H), Image.Transform.AFFINE,
                             (a, 0.0, tx, 0.0, a, ty),
                             resample=Image.Resampling.BICUBIC,
                             fillcolor=(9, 13, 16))


def draw_frame(t: float) -> bytes:
    content = static_stage().copy()
    draw_character(content, t)
    # Cursor is positioned on the UI confirm control; it travels from keyboard to the button.
    cursor_x = mix(1015, 896, smooth(43, 51, t))
    cursor_y = mix(224, 257, smooth(43, 51, t))
    draw_screen(content, t, (cursor_x, cursor_y))

    # Warm practical bounce on the desk and a monitor reflection on the side of Mara's face.
    d = ImageDraw.Draw(content, "RGB")
    d.ellipse((24, 425, 347, 560), fill=(52, 52, 45))
    # Very restrained status tick: visual punctuation, not a fake full-screen infographic.
    if 24 < t < 31:
        alpha = 0.4 + 0.4 * math.sin((t - 24) * 4.0)
        col = (int(152 + 44 * alpha), int(96 + 32 * alpha), 57)
        d.ellipse((1171, 108, 1181, 118), fill=col)

    shot = camera_transform(content, t)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(shot, (0, BAR_TOP))
    # A truthful proof-of-concept label lives in the lower matte, never over the action.
    if t >= 57.5:
        footer = ImageDraw.Draw(canvas)
        footer.text((24, H - 23), "60-SECOND STYLIZED 2D PROOF OF CONCEPT  •  NOT THE FINISHED FILM",
                    font=font(10, mono=True), fill=(173, 178, 171))
    return canvas.tobytes()


def write_soundscape(path: Path, duration: float, sample_rate: int = 48_000) -> None:
    n = int(duration * sample_rate)
    t = np.arange(n, dtype=np.float32) / sample_rate
    rng = np.random.default_rng(418)

    # Original synthesized room tone: low HVAC bed and a quiet, non-copyrighted tonal score.
    hum = (0.014 * np.sin(2 * np.pi * 58.0 * t + 0.1) +
           0.006 * np.sin(2 * np.pi * 116.0 * t + 0.4) +
           0.003 * np.sin(2 * np.pi * 174.0 * t + 1.1))
    slow_noise_src = rng.normal(0, 1, max(2, int(duration * 750))).astype(np.float32)
    slow_grid = np.linspace(0, duration, len(slow_noise_src), endpoint=False)
    room_noise = np.interp(t, slow_grid, slow_noise_src).astype(np.float32) * 0.005
    # Sparse three-note pad, barely audible below the room and performance.
    pad_gate = np.clip((t - 8.0) / 7.0, 0, 1) * np.clip((duration - t) / 8.0, 0, 1)
    trem = 0.72 + 0.28 * np.sin(2 * np.pi * 0.12 * t)
    pad = pad_gate * trem * (0.007 * np.sin(2 * np.pi * 110.0 * t) +
                             0.005 * np.sin(2 * np.pi * 146.83 * t + 0.3) +
                             0.004 * np.sin(2 * np.pi * 174.61 * t + 0.8))
    mono = hum + room_noise + pad

    def add_transient(at: float, freq: float, amp: float, decay: float, noise_mix: float = 0.15) -> None:
        start = int(at * sample_rate)
        length = min(int(0.16 * sample_rate), n - start)
        if start < 0 or length <= 0:
            return
        x = np.arange(length, dtype=np.float32) / sample_rate
        env = np.exp(-x * decay)
        burst = np.sin(2 * np.pi * freq * x) + noise_mix * rng.normal(0, 1, length).astype(np.float32)
        mono[start:start + length] += amp * env * burst

    # Light, irregular keyboard foley only while Mara is typing.
    click_times = np.arange(0.55, 23.8, 0.31) + rng.uniform(-0.07, 0.07, len(np.arange(0.55, 23.8, 0.31)))
    for i, at in enumerate(click_times):
        add_transient(float(at), float(1450 + (i % 5) * 170), 0.026, 74.0, 0.55)
    # Distinct restrained anomaly alerts; no alarm siren.
    for at, f0 in ((25.1, 784.0), (36.2, 659.0), (36.36, 880.0)):
        add_transient(at, f0, 0.075, 18.0, 0.03)
    # Mouse/button sounds for the hold decision.
    add_transient(50.8, 560.0, 0.045, 95.0, 0.8)
    add_transient(53.7, 480.0, 0.052, 88.0, 0.7)

    # Soft stereo width; all audio is generated here, without recorded samples.
    left = mono.copy()
    right = mono.copy()
    delay = int(0.011 * sample_rate)
    right[delay:] += mono[:-delay] * 0.08
    fade_in = np.clip(t / 1.2, 0, 1)
    fade_out = np.clip((duration - t) / 1.6, 0, 1)
    fade = np.minimum(fade_in, fade_out)
    stereo = np.stack((left * fade, right * fade), axis=1)
    peak = float(np.max(np.abs(stereo)))
    # Bring the quiet procedural mix up to a conservative -12 dBFS peak target
    # while capping gain so a short diagnostic render cannot over-amplify noise.
    if peak > 0.0:
        stereo *= min(3.0, 0.25 / peak)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())


def render(output: Path, seconds: int, ffmpeg: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if seconds < 5 or seconds > 120:
        raise ValueError("Duration must be between 5 and 120 seconds")
    frame_count = seconds * FPS
    with tempfile.TemporaryDirectory(prefix="project-zero-day-poc-") as td:
        wav_path = Path(td) / "soundscape.wav"
        log_path = Path(td) / "ffmpeg.log"
        write_soundscape(wav_path, seconds)
        cmd = [
            ffmpeg, "-hide_banner", "-loglevel", "warning", "-y",
            "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{W}x{H}",
            "-framerate", str(FPS), "-i", "pipe:0",
            "-i", str(wav_path),
            "-map", "0:v:0", "-map", "1:a:0",
            "-frames:v", str(frame_count), "-r", str(FPS), "-fps_mode", "cfr",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", str(seconds), "-movflags", "+faststart",
            "-metadata", "title=PROJECT ZERO-DAY: THE LAST DEPLOY — Proof of Concept",
            "-metadata", "comment=Stylized 2D animation proof of concept; not the finished film",
            str(output),
        ]
        with log_path.open("wb") as log:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log)
            assert proc.stdin is not None
            try:
                for i in range(frame_count):
                    t = i / FPS
                    proc.stdin.write(draw_frame(t))
                    if (i + 1) % 240 == 0:
                        print(f"Rendered {i + 1}/{frame_count} frames ({(i + 1) / FPS:.1f}s)", flush=True)
                proc.stdin.close()
                code = proc.wait()
            except BaseException:
                proc.kill()
                proc.wait()
                raise
        if code != 0:
            raise RuntimeError(f"FFmpeg exited {code}; see {log_path}")
    if not output.exists() or output.stat().st_size < 100_000:
        raise RuntimeError("Render output missing or unexpectedly small")
    print(f"Rendered {output} ({output.stat().st_size:,} bytes, {seconds}s target, {frame_count} frames)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4")
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--ffmpeg", default=os.environ.get("FFMPEG_BINARY", ""))
    args = parser.parse_args()
    if not args.ffmpeg:
        try:
            import imageio_ffmpeg
            args.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception as exc:
            raise SystemExit("Set FFMPEG_BINARY or install imageio-ffmpeg in the active Python environment") from exc
    render(args.output.resolve(), args.seconds, args.ffmpeg)


if __name__ == "__main__":
    main()
