#!/usr/bin/env python3
"""Validate preproduction documents only; this is not film/media QC."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "production"
SCRIPT = ROOT / "screenplay" / "Screenplay_v1.md"


def seconds_mmss(value: str) -> int:
    m, s = value.split(":")
    return int(m) * 60 + int(s)


def seconds_tc(value: str) -> int:
    h, m, s, frame = value.split(":")
    if frame != "00":
        raise AssertionError(f"Unexpected frame offset in whole-second plan: {value}")
    return int(h) * 3600 + int(m) * 60 + int(s)


def main() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    headings = re.findall(r"^### (\d+)\. .* \((\d{2}:\d{2})\)$", text, flags=re.M)
    ids = [int(scene_id) for scene_id, _ in headings]
    if ids != list(range(1, 45)):
        raise AssertionError(f"Expected scene IDs 1..44 in order; got {ids}")
    screenplay_durations = [seconds_mmss(d) for _, d in headings]
    if sum(screenplay_durations) != 1800:
        raise AssertionError(f"Screenplay target is {sum(screenplay_durations)} sec, not 1,800")

    with (PRODUCTION / "scene_manifest.csv").open(encoding="utf-8", newline="") as f:
        scenes = list(csv.DictReader(f))
    if len(scenes) != 44:
        raise AssertionError(f"Expected 44 scene rows, got {len(scenes)}")
    if [int(row["scene_id"]) for row in scenes] != ids:
        raise AssertionError("Scene manifest order/IDs differ from screenplay")
    if [int(row["target_duration_sec"]) for row in scenes] != screenplay_durations:
        raise AssertionError("Scene durations differ between screenplay and manifest")
    if seconds_tc(scenes[0]["target_start_tc"]) != 0:
        raise AssertionError("First scene does not begin at zero")
    if seconds_tc(scenes[-1]["target_end_tc"]) != 1800:
        raise AssertionError("Scene plan does not end at 30:00")
    if any(row["production_status"] != "PLANNED — NOT PRODUCED" for row in scenes):
        raise AssertionError("Scene rows must clearly remain unproduced")

    with (PRODUCTION / "shot_manifest.csv").open(encoding="utf-8", newline="") as f:
        shots = list(csv.DictReader(f))
    if len(shots) != 132:
        raise AssertionError(f"Expected 132 planned shots, got {len(shots)}")
    counts = Counter(row["scene_id"] for row in shots)
    if counts != Counter({f"{i:02d}": 3 for i in range(1, 45)}):
        raise AssertionError("Each scene must have exactly three planned shot rows")
    if sum(int(row["target_duration_sec"]) for row in shots) != 1800:
        raise AssertionError("Shot durations do not sum to 30:00")
    for row in shots:
        if row["production_status"] != "NOT PRODUCED — planned shot only":
            raise AssertionError(f"Shot {row['shot_id']} is not marked unproduced")
        if seconds_tc(row["target_end_tc"]) <= seconds_tc(row["target_start_tc"]):
            raise AssertionError(f"Non-positive planned duration in {row['shot_id']}")
        plan = row["camera_and_performance_plan"].lower()
        has_live_action = any(token in plan for token in ("moving", "manipulates", "breathing", "gesture"))
        if "performer" not in plan or not has_live_action:
            raise AssertionError(f"Missing live-action/performance plan in {row['shot_id']}")

    state = json.loads((PRODUCTION / "production_state.json").read_text(encoding="utf-8"))
    if state["planned_scope"]["target_runtime_seconds"] != 1800:
        raise AssertionError("Production state runtime differs")
    if state["planned_scope"]["produced_shot_count"] != 0:
        raise AssertionError("Production state must not claim produced footage")
    if state["delivery"]["master_path"] is not None or state["delivery"]["direct_download_url"] is not None:
        raise AssertionError("No master or download may be listed before one exists")
    if (ROOT / "film" / "Project_Zero_Day_4K.mp4").exists():
        raise AssertionError("Unexpected movie file exists; inspect it before updating status")

    print("PREPRODUCTION QA PASS")
    print("44 screenplay scenes; screenplay and scene manifest targets match at 1,800 seconds.")
    print("132 planned shots; three per scene; timecodes span 00:00:00:00–00:30:00:00.")
    print("Every scene/shot is marked not produced; production state lists no master or link.")
    print("This does not validate a movie: no footage, audio, rendered file, or playback exists.")


if __name__ == "__main__":
    main()
