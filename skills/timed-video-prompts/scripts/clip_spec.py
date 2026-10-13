#!/usr/bin/env python3
"""Check a clip spec and turn it into a prompt for any video model.

A clip spec (JSON) is the platform-neutral plan of one clip: assets, characters,
positions, timed shots, lines, sound and the keep-consistent list. This script
checks it and renders the prompt text plus the list of files to attach, for a
given platform syntax and model limits. Our own platform can read the same JSON.

  clip_spec.py check  SPEC.json [--model seedance-2.5]
  clip_spec.py render SPEC.json [--model seedance-2.5] [--platform magnific] [--out PROMPT.txt]

Exit 0 = clean; 1 = the spec has errors (printed one per line); 2 = bad usage.
"""
import argparse
import json
import re
import sys

# Limits per model, measured from the Magnific catalog 2026-10-13 (video_models_list).
# "images" counts image + character references together. None = no known limit.
MODELS = {
    "seedance-2.5": {"images": 30, "video": 10, "audio": 10, "min_s": 4, "max_s": 30, "prompt": 10000},
    "seedance-2.0": {"images": 9, "video": 3, "audio": 3, "min_s": 4, "max_s": 15, "prompt": 40000},
    "seedance-2.0-fast": {"images": 9, "video": 3, "audio": 3, "min_s": 4, "max_s": 15, "prompt": 40000},
    "generic": {"images": None, "video": None, "audio": None, "min_s": None, "max_s": None, "prompt": None},
}

# How each platform names an attached file inside the prompt text, and what
# reference type each asset kind is sent as (Magnific `references[].type`).
PLATFORMS = {
    "generic": {"handle": "@{h}"},
    "higgsfield": {"handle": "@{h}"},
    "dreamina": {"handle": "@{h}"},  # Dreamina's @ picker labels uploads itself: match its labels, see platforms.md
    "magnific": {"handle": "@{h}"},
}
REF_TYPE = {"character": "character", "location": "image", "prop": "image", "map": "image",
            "style": "style", "image": "image", "video": "video", "audio": "audio"}
VISUAL = {"character", "location", "prop", "map", "style", "image"}
HANDLE_RE = re.compile(r"@([A-Za-z0-9_]+)")


def fmt_t(t):
    return f"{t:.1f}".rstrip("0").rstrip(".") if t != int(t) else f"{int(t)}.0"


def check(spec, model):
    errs = []
    lim = MODELS[model]
    dur = spec.get("duration")
    assets = {a["handle"]: a for a in spec.get("assets", [])}
    names = {c["name"] for c in spec.get("characters", [])}
    shots = spec.get("shots", [])
    if not isinstance(dur, (int, float)) or dur <= 0:
        errs.append("duration: missing or not a positive number")
    if not shots:
        errs.append("shots: none")
    prev_end = 0.0
    for i, s in enumerate(shots, 1):
        if abs(s["start"] - prev_end) > 1e-6:
            errs.append(f"shot {i}: starts at {s['start']}s but the previous shot ends at {prev_end}s")
        if s["end"] <= s["start"]:
            errs.append(f"shot {i}: ends before it starts")
        if not s.get("background"):
            errs.append(f"shot {i}: no BACKGROUND (what is behind each visible character)")
        for ln in s.get("lines", []):
            if ln["who"] not in names:
                errs.append(f"shot {i}: line by '{ln['who']}', who is not in characters")
            if ln["start"] < s["start"] or ln.get("end", ln["start"]) > s["end"]:
                errs.append(f"shot {i}: line \"{ln['text'][:30]}\" spills outside {s['start']}–{s['end']}s")
        prev_end = s["end"]
    if shots and isinstance(dur, (int, float)) and abs(prev_end - dur) > 1e-6:
        errs.append(f"shots end at {prev_end}s but duration is {dur}s")
    for c in spec.get("characters", []):
        if not c.get("identity"):
            errs.append(f"character {c['name']}: no identity text (it is pasted word for word into every prompt)")
        for h in c.get("assets", []) + ([c["voice_asset"]] if c.get("voice_asset") else []):
            if h not in assets:
                errs.append(f"character {c['name']}: asset @{h} is not in assets")
    text = json.dumps(spec, ensure_ascii=False)
    for h in sorted(set(HANDLE_RE.findall(text))):
        if h not in assets:
            errs.append(f"@{h} is used in the text but is not in assets")
    counts = {"images": 0, "video": 0, "audio": 0}
    for a in assets.values():
        k = a.get("kind", "image")
        counts["images" if k in VISUAL else k if k in ("video", "audio") else "images"] += 1
    for k, n in counts.items():
        if lim[k] is not None and n > lim[k]:
            errs.append(f"{n} {k} references, but {model} accepts {lim[k]}")
    if lim["min_s"] and isinstance(dur, (int, float)) and not lim["min_s"] <= dur <= lim["max_s"]:
        errs.append(f"duration {dur}s is outside {model}'s {lim['min_s']}–{lim['max_s']}s")
    if spec.get("start_frame") and assets:
        errs.append("start_frame and references together: Seedance accepts one or the other, not both")
    return errs


def render(spec, platform):
    h = lambda name: PLATFORMS[platform]["handle"].format(h=name)
    sub = lambda s: HANDLE_RE.sub(lambda m: h(m.group(1)), s or "")
    out = [sub(spec["logline"])]
    if spec.get("opens"):
        out.append(sub(spec["opens"]))
    if spec.get("assets"):
        out.append("\nREFERENCES")
        for a in spec["assets"]:
            line = f"{h(a['handle'])}: {a['role']}"
            if a.get("ignore"):
                line += f" Ignore {a['ignore']}"
            out.append(sub(line))
    if spec.get("look"):
        out += ["\nLOOK", sub(spec["look"])]
    out.append("\nCHARACTERS")
    for c in spec["characters"]:
        refs = ", ".join(h(x) for x in c.get("assets", []))
        out.append(" ".join(x for x in [f"{c['name']}{f' ({refs})' if refs else ''}:", c["identity"],
                                        c.get("voice", ""), c.get("rule", "")] if x))
    for r in spec.get("rules", []):
        out += [f"\n{r['name'].upper()}", sub(r["text"])]
    if spec.get("positions"):
        out.append("\nWHERE EVERYONE IS (fixed for the whole clip)")
        for p in spec["positions"]:
            out.append(sub(p["layout"]))
            for who, behind in p.get("behind", {}).items():
                out.append(sub(f"Behind {who}: {behind}"))
    out.append("\nSHOTS")
    for s in spec["shots"]:
        parts = [f"{fmt_t(s['start'])}–{fmt_t(s['end'])}s: {s['camera']}", s.get("frame", ""),
                 f"BACKGROUND: {s['background']}", s.get("action", "")]
        for ln in s.get("lines", []):
            t = fmt_t(ln["start"]) + (f"–{fmt_t(ln['end'])}" if ln.get("end") else "")
            parts.append(f"{t}s {ln['who']}{', ' + ln['delivery'] if ln.get('delivery') else ''}: \"{ln['text']}\"")
        if s.get("cut"):
            parts.append(s["cut"])
        out.append(sub(" ".join(p.strip() for p in parts if p and p.strip())))
    snd = spec.get("sound", {})
    out.append("\nSOUND")
    out.append(sub(" ".join(x for x in [snd.get("music", "No music."), snd.get("ambience", ""), snd.get("voice", "")] if x)))
    lines = [ln for s in spec["shots"] for ln in s.get("lines", [])]
    if lines:
        out.append("Lines, each spoken exactly once and nothing else:")
        for ln in lines:
            t = fmt_t(ln["start"]) + (f"–{fmt_t(ln['end'])}" if ln.get("end") else "")
            out.append(f"{t}s {ln['who']} \"{ln['text']}\"")
        out.append(snd.get("tail", "No added words, interjections, laughter or background score."))
    if spec.get("keep"):
        out.append("\nKEEP CONSISTENT")
        out += [f"- {sub(k)}" for k in spec["keep"]]
    prompt = "\n".join(out).strip() + "\n"
    attach = [{"handle": a["handle"], "file": a["file"], "type": REF_TYPE.get(a.get("kind", "image"), "image")}
              for a in spec.get("assets", [])]
    return prompt, attach


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["check", "render"])
    ap.add_argument("spec")
    ap.add_argument("--model", default="generic", choices=sorted(MODELS))
    ap.add_argument("--platform", default="generic", choices=sorted(PLATFORMS))
    ap.add_argument("--out")
    a = ap.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    errs = check(spec, a.model)
    for e in errs:
        print(f"ERROR {e}", file=sys.stderr)
    if errs:
        return 1
    if a.cmd == "check":
        print(f"OK {a.spec}: {len(spec['shots'])} shots, {spec['duration']}s, {len(spec.get('assets', []))} references ({a.model})")
        return 0
    prompt, attach = render(spec, a.platform)
    lim = MODELS[a.model]["prompt"]
    if lim and len(prompt) > lim:
        print(f"ERROR prompt is {len(prompt)} characters, {a.model} accepts {lim}", file=sys.stderr)
        return 1
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(prompt)
    else:
        sys.stdout.write(prompt)
    print(f"\nATTACH ({len(prompt)} chars): " + json.dumps(attach, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
