#!/usr/bin/env python3
"""Write every view and expression prompt for ONE character or object.

Reads a character file (JSON) and prints one image-generation prompt per view
(front, back, left side, right side, three-quarter), then one per view for each
expression. Every prompt shares the same wording; only the view and expression
lines change, which is what keeps the character identical across images.

  view_prompts.py CHARACTER.json            # Markdown, for a person to copy
  view_prompts.py CHARACTER.json --json     # JSON, for batch runs or our own platform

Exit 0 = written; 1 = the character file has errors; 2 = bad usage.
"""
import argparse
import json
import sys

VIEWS = {
    "front": "seen straight from the front, facing the camera, body square to the camera, head level",
    "back": "seen straight from behind, the back of the head and the back toward the camera",
    "left": "in left profile: side-on, the {s}'s left side toward the camera, head pointing to the left of the frame",
    "right": "in right profile: side-on, the {s}'s right side toward the camera, head pointing to the right of the frame",
    "three_quarter_left": "in a three-quarter view from the front-left: body turned about 45 degrees so the face and the {s}'s left side are both visible, head toward the left of the frame and the body extending back toward the right of the frame, the {s}'s left shoulder nearest the camera and the right shoulder turned away",
    "three_quarter_right": "in a three-quarter view from the front-right: body turned about 45 degrees so the face and the {s}'s right side are both visible, head toward the right of the frame and the body extending back toward the left of the frame, the {s}'s right shoulder nearest the camera and the left shoulder turned away",
    "face": "close-up of the face and neck, seen straight from the front, looking into the lens",
}
DEFAULT_VIEWS = ["front", "back", "left", "right", "three_quarter_left"]

EXPRESSIONS = {
    "animal": {
        "neutral": "Neutral, relaxed: mouth closed, ears in their natural resting position, eyes calm and open, tail relaxed",
        "happy": "Happy: soft eyes, mouth open and relaxed with the tongue slightly out, ears relaxed, tail up mid-wag",
        "sad": "Clearly sad and dejected: head hanging low below the shoulders, ears drooping flat back against the head, eyes looking up mournfully from under the brow, mouth closed, tail hanging down between the hind legs, shoulders slumped",
        "angry": "Angry: muzzle wrinkled, lips pulled back showing the front teeth, hard stare, ears pinned, body stiff and leaning forward, tail stiff",
        "surprised": "Surprised: eyes wide, ears fully up and forward, mouth slightly open, head pulled back a little",
        "curious": "Curious: head tilted to one side, ears up and forward, mouth closed, eyes bright",
        "scared": "Scared: ears flat back, body crouched low, tail tucked between the hind legs, eyes wide showing some white",
        "excited": "Excited: play bow, front legs down and rear up, mouth open, tail high",
        "talking": "Talking: mouth half open as if in the middle of a word, tongue visible, ears forward, eyes on the listener; a real animal's mouth and teeth, no human lips",
        "sleepy": "Sleepy: eyes half closed, ears relaxed, head low",
    },
    "person": {
        "neutral": "Neutral: relaxed face, mouth closed, calm open eyes",
        # Never "cheeks lifted" here: a model then draws round apple cheeks and a full grin, which was J's
        # own complaint on 18 Oct. How THIS person smiles comes from the character file's `smile`.
        "happy": "Happy: a genuine smile, in this person's own way of smiling as in the reference photos",
        "sad": "Sad: brows drawn up in the middle, mouth corners down, eyes lowered",
        "angry": "Angry: brows pulled down and together, lips pressed tight, hard stare",
        "surprised": "Surprised: eyebrows raised high, eyes wide, mouth open",
        "curious": "Curious: head tilted slightly, one eyebrow raised, a slight smile",
        "scared": "Scared: eyes wide, brows raised and pulled together, mouth tense and slightly open",
        "excited": "Excited: big open smile, eyes wide and bright",
        "talking": "Talking: mouth half open mid-sentence, natural relaxed face",
        "sleepy": "Sleepy: heavy half-closed eyelids, relaxed mouth",
    },
}
DEFAULT_EXPRESSIONS = ["neutral", "happy", "sad", "angry", "surprised", "curious"]

# Backdrop chosen for contrast with the subject's main tone, always plain and neutral.
BACKDROPS = {
    "light": "a plain seamless mid-dark slate-grey studio backdrop",
    "mid": "a plain seamless light cool-grey studio backdrop",
    "dark": "a plain seamless light warm-grey studio backdrop",
}
DETAIL = {"animal": "fur", "person": "skin, hair and fabric", "object": "surface and material"}

# How much of the subject each view shows. A person's face is too small to judge at full body, so
# people default to waist-up; the `face` view is always a close-up.
FRAMING = {
    "full_body": "Full body, the whole {s} inside the frame with clear space around it",
    "waist_up": "Framed from the waist up, the head and shoulders well inside the frame with space above the head",
    "head_shoulders": "Framed head and shoulders, the whole head inside the frame with space above it",
}
DEFAULT_FRAMING = {"animal": "full_body", "person": "waist_up", "object": "full_body"}

# The identity lock: what a model must not "improve". Earned from the Higgsfield thumbnail skill's
# IDENTITY LOCK (people) and the Coco test (animals).
LOCK = {
    # Video-Editor 1's read of round 6 (18 Oct): every picture separated the brows, narrowed and
    # rejuvenated the face and retouched the skin, and the face-embedding gate saw none of it.
    "person": "Do not beautify, smooth, slim, narrow, de-age or restyle the face: the same bone structure and face "
              "width, eye shape, nose, lips, jawline, the eyebrows' exact shape, thickness and the gap between them, "
              "the real skin tone and texture with its natural unevenness (no retouching), hairline and hair texture "
              "as the reference.",
    # Naming a breed pulls in that breed's typical anatomy (Coco, 18 Oct: dewclaws and a long tail came back
    # in every image while the prompt said "of its breed"); describe the body, never the breed.
    "animal": "Do not beautify, average or restyle it: the same head shape, markings, size and "
              "proportions as the reference.",
    "object": "The same shape, proportions, colours and printed marks as the reference.",
}


def errors(c):
    e = []
    for k in ("name", "handle", "kind", "identity", "tone"):
        if not c.get(k):
            e.append(f"missing '{k}'")
    if c.get("kind") not in ("animal", "person", "object"):
        e.append("kind must be animal, person or object")
    if c.get("kind") == "animal" and not c.get("species"):
        e.append("an animal needs 'species' (dog, cat ...)")
    if c.get("tone") not in BACKDROPS:
        e.append("tone must be light, mid or dark (the subject's main colour), to pick a contrasting backdrop")
    if c.get("framing") and c["framing"] not in FRAMING:
        e.append(f"framing must be one of {', '.join(FRAMING)}")
    for v in c.get("views", []):
        if v not in VIEWS:
            e.append(f"unknown view '{v}' (known: {', '.join(VIEWS)})")
    kind = c.get("kind") if c.get("kind") in EXPRESSIONS else "animal"
    for x in c.get("expressions", []):
        if x not in EXPRESSIONS[kind] and not isinstance(c.get("custom_expressions", {}).get(x), str):
            e.append(f"unknown expression '{x}': add it to custom_expressions with its body-language description")
    for k in ("glasses", "smile", "hair"):
        if k in c and (not isinstance(c[k], str) or not c[k].strip()):
            e.append(f"'{k}' must be a non-empty description")
    if c.get("glasses") == "none" and "glasses" in (c.get("identity", "") + " " + c.get("drift", "")).lower():
        e.append("'glasses' is none but identity or drift still mentions glasses: say it once, in 'glasses'")
    for x in c.get("held_expressions", []):
        if x not in c.get("expressions", []):
            e.append(f"held expression '{x}' is not in expressions")
    return e


# Expressions where the mouth shows how this person smiles, so the character file's `smile` goes in.
SMILING = {"happy", "excited", "curious", "laughing"}


def prompt(c, view, expr, anchor):
    kind = c["kind"]
    s = c.get("species") or ("person" if kind == "person" else "object")
    name = c["name"]
    refs = c.get("references") or []
    if refs:
        looks = "as they look there" if kind == "person" else "as it looks there"
        source = f"The {s} in the attached reference photos, reproduced exactly {looks}, every detail the same: "
    elif anchor:
        source = ""
    else:
        source = f"The {s} in the attached anchor image ({c['handle']}_front_neutral), reproduced exactly, every detail the same: "
    lines = [f"Reference image of {name} for an AI video: one {s}, {VIEWS[view].format(s=s)}."]
    if expr:
        table = {**EXPRESSIONS.get(kind, {}), **c.get("custom_expressions", {})}
        text = table[expr]
        # A fixed carriage (e.g. a tail that always hangs) wins over the mood table's generic tail
        # (Coco, 18 Oct: "tail up mid-wag" made her tail curve up while the identity said it hangs).
        if c.get("tail_carriage") and kind == "animal":
            import re as _re
            text = _re.sub(r",?\s*tail[^,;]*", "", text).rstrip(", ")
            text += f"; tail as always: {c['tail_carriage'].strip().rstrip('.')}"
        if view == "back" and kind == "animal":
            text += "; seen from behind, the mood shows in the ears, tail and posture"
        lines.append(text + ".")
        if c.get("smile") and expr in SMILING:
            lines.append(f"Smile exactly the way this person smiles: {c['smile'].strip().rstrip('.')}.")
    lines.append(source + c["identity"].strip())
    if c.get("hair"):
        # The cut the person chose can differ from their photos (J, 18 Oct: "I don't have a clean hair cut now").
        lines.append(f"Hair: {c['hair'].strip().rstrip('.')}; this haircut wins over the hair length and style in the "
                     f"reference photos, which set only the hair colour, texture and hairline.")
    if c.get("glasses") == "none":
        lines.append("No glasses: no frames or eyewear of any kind.")
    elif c.get("glasses"):
        lines.append(f"Glasses: {c['glasses'].strip().rstrip('.')}.")
    if c.get("drift"):
        lines.append(f"Keep exactly: {c['drift']}.")
    lines.append(LOCK[kind].format(s=s))
    framing = c.get("framing") or DEFAULT_FRAMING[kind]
    frame = ("Close-up framing with the whole head inside the frame" if view == "face"
             else FRAMING[framing].format(s=s))
    lines.append(f"{frame}, on {BACKDROPS[c['tone']]}: plain, evenly lit, no texture, objects or gradients. "
                 f"Soft even studio light with a gentle rim light, so the {s} stands out with strong, clean contrast "
                 f"against the background. Camera at the {s}'s eye level, 85mm lens, no distortion.")
    truth = "colours exactly as described" if anchor else "colours true to the reference"
    lines.append(f"Photorealistic, tack-sharp {DETAIL[kind]} detail, {truth}. "
                 f"Only this one {s}; no text, no labels, no props, nobody else.")
    return " ".join(lines)


def build(c):
    views = c.get("views") or DEFAULT_VIEWS
    exprs = [] if c["kind"] == "object" else (c.get("expressions") or DEFAULT_EXPRESSIONS)
    # An expression no real photo shows (J has no photo laughing) is a guess the likeness gate cannot check: held.
    exprs = [x for x in exprs if x not in c.get("held_expressions", [])]
    base = "neutral" if "neutral" in exprs else None
    imaginary = not c.get("references")
    out = []
    order = [(v, base) for v in views] + [(v, x) for x in exprs if x != base for v in views]
    for i, (v, x) in enumerate(order, 1):
        anchor = imaginary and v == views[0] and x == base and i == 1
        fid = f"{c['handle']}_{v}" + (f"_{x}" if x else "")
        attach = (c.get("references") or []) if not imaginary else ([] if anchor else [f"{c['handle']}_{views[0]}" + (f"_{base}" if base else "") + ".png"])
        out.append({"n": i, "file": fid + ".png", "view": v, "expression": x or "", "anchor": anchor,
                    "attach": attach, "prompt": prompt(c, v, x, anchor)})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("character")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.character, encoding="utf-8") as f:
        c = json.load(f)
    errs = errors(c)
    for e in errs:
        print(f"ERROR {e}", file=sys.stderr)
    if errs:
        return 1
    items = build(c)
    held = c.get("held_expressions", [])
    if a.json:
        json.dump({"character": c["name"], "prompts": items, "held": held}, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 0
    imaginary = not c.get("references")
    print(f"# {c['name']}: {len(items)} view prompts\n")
    if held:
        print(f"Held until a real photo shows it: {', '.join(held)}.\n")
    print("Attach the reference photos to every prompt." if not imaginary else
          f"Imaginary character: generate prompt 1 first, approve it, then attach it to every other prompt.")
    print("Use the same model and settings for all of them (16:9 or 1:1, 2k).\n")
    for it in items:
        title = f"{it['n']}. {it['file']}" + ("  (anchor: generate first)" if it["anchor"] else "")
        print(f"## {title}\nAttach: {', '.join(it['attach']) or 'nothing'}\n\n```\n{it['prompt']}\n```\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
