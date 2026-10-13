---
name: timed-video-prompts
description: Write, check and revise timecoded video-generation prompts for ANY video model or platform (Seedance 2.x on Magnific, Dreamina or Higgsfield, Kling, Veo, our own platform): multi-shot clips with fixed dialogue, consistent characters WITHOUT a trained identity (no Soul ID needed), talking animals, voice and lip sync, match cuts, fixed positions and reframe passes. Use whenever a clip has to be generated from a prompt, a character must look the same across clips, a generated take came back wrong, or a prompt must be moved from one model or platform to another.
---

# Timed video prompts

One clip is planned once, in a platform-neutral **clip spec**, then rendered into the prompt and
attachments a given model accepts. The plan never depends on one platform's features: a trained
identity (Higgsfield Soul ID, a Kling element) is an optional extra a platform adapter may attach,
never something the method needs. The same spec drives Magnific, Dreamina, Higgsfield, a raw API or
our own platform.

Chat with J in his language; write every generation prompt in English unless asked otherwise.

## 0. Rules that always hold

- **Plan in the spec, render per platform.** The spec (`examples/talking-dog.json` is a full one) holds
  assets, characters, positions, shots, lines, sound and the keep-consistent list. Run
  `scripts/clip_spec.py check SPEC --model <model>` before any paid generation and
  `scripts/clip_spec.py render SPEC --model <model> --platform <platform>` for the prompt and the
  attach list. A spec that fails the check is not generated.
- **Asset handles are the file's own name**: `@biscuit_front`, `@loc_kitchen`, never `@image1` or a
  slot number in the spec. If a platform's UI labels uploads itself, map handles to its labels at
  render time (see `references/platforms.md`), never in the spec.
- **Always deliver the full prompt**, never a diff or "same as before". Keep every earlier correction
  unless J removes it. Never bring back a cancelled version or invent story beats.
- **Lines are J's fixed text**: never add, drop or reorder words; each is spoken exactly once.
- **Check the price before you spend**: on Magnific, `simulate_cost` with the same arguments; draft
  at `Draft`/480p, render the final at 720p/1080p only once the draft is right.
- **A prompt guarantees nothing.** Report what the take actually did, not what the prompt asked for.

## 1. Workflow

1. **Collect**: script and lines with times, the asset files, aspect, duration, target model and
   platform, budget.
2. **Lock identity** for each character (section 3) before writing any shot.
3. **Write the spec.** Shots contiguous, each with its camera, who is in frame, `BACKGROUND`, timed
   action and lines.
4. **Check, then render** with `clip_spec.py`. Fix every error it prints.
5. **Draft, look, fix.** Generate a draft, watch it, write what broke in the spec's prompt file under
   "What came back", fix the spec with the failure table (section 7), re-check, re-render.
6. **Final render** at the delivery resolution. Save the kept take and the exact spec that made it.

## 2. Prompt architecture (the order `render` produces)

```
<One sentence: duration, aspect, what happens, the cut trick if any.>
<"Opens mid-situation ..." when the clip continues an earlier one.>

REFERENCES     each @handle: what it is, what to take, what to IGNORE (photo backdrop, people in a
               location plate, the colours of a blocking map). Say when a plate's angle IS shot 1's.
LOOK           lens family, colour intent, light per location.
CHARACTERS     name (its reference handles): the identity text word for word + how it speaks + one
               behaviour rule ("sits the whole time", "never laughs").
<PROP RULES>   e.g. how a phone is held and which side faces camera.
WHERE EVERYONE IS (fixed for the whole clip)
               per location: screen-left / centre / right from a named camera side, or clock-face
               seats; what is behind each of them.
SHOTS          <t0–t1>s: camera position, lens, the move that runs the whole shot. Who is where in
               THIS frame. BACKGROUND: what is behind each of them from this angle. Timed action.
               Timed lines with delivery and eye-line. How the shot ends or cuts.
SOUND          music policy, ambience per location (switching on cut frames), voice recording spec,
               "Lines, each spoken exactly once and nothing else:" list, the no-added-words tail.
KEEP CONSISTENT 8-14 one-line rules restating what models tend to break.
```

Geometry comes before action, every shot is self-contained, and the last block repeats the fragile
rules. This order works on every model tried so far; keep it when moving between platforms.

## 3. Identity without a trained ID

Use the highest rung available; stack rungs, they add up.

1. **Real photos as references.** For a real person or animal, 4-6 sharp photos: front, three-quarter,
   profile, full body, and one with the mouth open if it will speak. Plain light, no filters. These
   beat any trained ID for animals, which most trained-ID features are not built for.
2. **A generated reference sheet** for an invented character: make a turnaround (front, three-quarter,
   profile, full body, mouth open), approve it once, save the views as files. From then on they are the
   character's photos; never regenerate them per clip. The photo-set rules, the sheet prompt and the
   identity-lock block are in `consistent-character-images` (sections 1-3).
3. **The identity text**, one paragraph per character (species/build, colouring, markings and where,
   eyes, ears/hair, clothing or collar, one personality line), pasted word for word into every prompt
   from one file. Changing it means changing the file, never one prompt.
4. **A start frame** when one shot must match exactly: generate the first frame as a still with the
   references (`consistent-character-images`), approve it, then animate it. On Seedance a start frame
   and reference images exclude each other: start frame for one tightly held shot, references for
   multi-shot clips. **With a start frame, the prompt describes the motion, not the picture**: the
   model already has the frame, so spend the words on camera move, action, lines and sound, and keep
   only a one-line identity reminder.
5. **Chaining**: the last frame of clip N is the start frame of clip N+1 when clips must join.
6. **A platform's trained ID** (Soul ID, a Kling element), only if that platform is in use and a test
   shows it beats rungs 1-4 for this character. The spec still names the character by handle; the
   platform adapter decides whether to attach photos or the trained ID.

## 4. Shot-writing rules

- **First frame stated outright**: "THE VERY FIRST FRAME IS ..." and, when a plate defines the angle,
  "exactly the angle of @loc_x". An establishing wide is its own 1-1.5 s shot with a hard cut.
- **Every shot names** camera position, lens (16-28 mm wides for energy, 35-50 mm for faces), the move
  (push-in, orbit, travel, pull-back) and that the move never stops for a line.
- **Every shot has `BACKGROUND:`**, what is behind each visible character from this angle. It is the
  cheapest way to make positions stick.
- **Off-frame characters are named as out of frame**, never left implied.
- **Every beat has a time**: a look, a grab, a tap, a head turn. Lines get start-end; a line never
  spills across a cut unless the cut depends on it.
- **Hands and props per shot**: what is in each hand from the shot's first frame.
- **Write positives**; negations only as a short tail ("no dissolve, no flash, no morph"). Do not ban a
  look J chose (film grain, a grade) to fix an unrelated fault.
- **Groups** (a band, a crowd): exactly where, facing which way, "keeps playing the whole time on
  screen", "never walks off".

## 5. Transitions

- **Match cut on an action** (a tap, a bite): "Same lens, same angle, same size in frame, same pose,
  same move continuing without a stop. BACKGROUND now: ...". The reaction to the new place comes after
  the cut, with its own time. Ambience and diegetic music switch on the cut frame.
- **Hidden cut under full occlusion**: the camera slides behind a near shoulder until fabric fills the
  whole frame, the world changes inside it, and the camera comes out at the same speed into the new
  place. Drifts more often than a match cut; prefer match cuts when reliability matters.
- **Foreground wipe**: an opaque shape crosses the frame and the next place appears around its edges.
- **Objects that leave with the world** (a plate, a fork) vanish "only on the cut, never before".

## 6. Voice, lip sync and talking animals

- **Two routes, pick per clip:**
  - *Native audio*: models such as Seedance 2.x generate the voice and lip movement in one pass from
    the lines in the prompt. Fastest; the voice can differ between clips.
  - *Fixed voice*: record or generate the line first (a voice per character, e.g. ElevenLabs), then
    either pass it as an **audio reference** (Seedance accepts audio references; limits in
    `references/platforms.md`) or lip-sync the finished video to it with the platform's lip-sync tool.
    Use this when a character must sound the same in every clip.
- **Voice first, then picture** for anything longer than one clip: generate every voice take first,
  with the same voice, one take per clip; regenerate only a failed or too-long take; then size each
  clip to its take. About 20-24 spoken words fill an 8-9 s take inside a 10 s clip.
- **Narration over picture** (a narrator, not the character speaking): keep all words out of the video
  prompt; the clip's audio is ambience only and nobody's mouth moves.
- **Voice spec in the SOUND block**: "clean, close, dry studio dialogue recording; no echo, no noise;
  the microphone never appears".
- **Delivery per line**: tempo, emotion, eye-line ("looking straight into the lens"), physical state.
- **Interruptions**: put the interrupter's first word inside the other's gesture; forbid a gap.
- **Talking animals**: say how the mouth moves ("a real dog's jaw and tongue move with the words, no
  human lips or teeth"), keep the animal's own body language (ears, tail, head tilt) as the emotion,
  give a mouth-open reference photo, keep lines short (under ~3 s each), and say "eyes open for the
  whole clip". Animal lip sync is the least proven part of this method: test it on a draft first.

## 7. Failure → fix

| Symptom in the take | Fix in the spec |
|---|---|
| Opens on the wrong shot | Explicit first-frame sentence + "never opens on ..." in KEEP CONSISTENT; the wide as its own shot |
| Characters swap places between shots | WHERE EVERYONE IS + `BACKGROUND:` in every shot + "behind each of them" lines |
| Character drifts (coat, face, markings) | More reference views (section 3); identity text restated in KEEP CONSISTENT; shorter shots; start frame for the worst shot |
| Washed-out colour | Remove film-emulation words; "clean modern digital look, deep clean blacks, saturated like the references" |
| Eyes closed | "eyes OPEN for the entire shot, pupils visible" + a KEEP CONSISTENT line |
| Line said twice, or to the wrong character | Address and eye-line in the shot; one canonical lines list; "the line is not repeated" after a cut |
| Animal mouth looks human, or does not move | The talking-animal sentence (section 6); a mouth-open reference; shorter line; try the fixed-voice route |
| Voice changes between clips | Fixed-voice route with an audio reference |
| Group stands still or walks off | Exact placement + "keeps playing every moment on screen", "never walks" |
| Prop appears or vanishes early | Per-shot hand inventory; "only on the cut, never before" |
| Model ignores a blocking map | Bind each map colour to a character handle; separate geometry (map) from appearance (photos) |
| Occlusion transition drifts | Check the camera path and full coverage first; offer a match cut only if J wants to change method |

Add a row whenever a take breaks in a new way and a fix is proven.

## 8. Variants

- **Shorter clip** (drop a shot): delete it in the spec, shift every later time, re-state the first
  frame, re-check.
- **Retake fragment** (2-3 shots): same header blocks trimmed to that location, opening
  "mid-situation", same lines and positions as the master.
- **Translated prompt**: a full translation of the current master, updated on every edit.
- **Looser positions** on request: remove the positional words for that character, add "each keeps the
  place of their first shot".

## 9. Blocking maps

For seating and table layouts, generate a placement map first: thin outlines on white, one muted
colour per figure, furniture in light grey, no faces, no labels unless asked. Choose its view from the
shot (top-down for an overhead shot). Exact counts of settings and shared plates (a shared plate is not
a seat). In the video prompt the map gives positions only; the photos give identity, clothes and
light; bind each colour to a character handle. A map is an asset only once it is generated and saved.

## 10. Reframe (16:9 → 9:16 or 1:1) by outpainting

Analyse the final edit first (`ffprobe`, scene cuts, a 1 fps contact sheet). The prompt: fit the whole
source to the output width, fixed scale and centre in every frame, generate equal bands above and below
only, the source composition stays the output composition, seams invisible, no zoom, crop, pan, blur or
mirror fill. Bands hold environment only: no new people, hands, faces, animals, text or logos. Hard
cuts change the bands on the same frame. Audio: the source track passes through, nothing generated.
Band height = (output height − output width × 9/16) / 2: 656 px each for 1080×1920, about 236 px for
1080×1080. If the tool still crops or moves the source, its fit setting overrides the prompt; replace
the audio in the edit as the safe fallback.

## Files

- `scripts/clip_spec.py`: `check` and `render` a clip spec; model limits and platform syntax live in
  its `MODELS` and `PLATFORMS` tables (add a platform or model there, never in the spec).
- `examples/talking-dog.json`: a complete one-shot spec with a talking dog.
- `references/platforms.md`: how each platform takes references, audio and lip sync, its limits and
  measured prices.
- `sources/higgsfield-timed-prompts/SKILL.md`: the original skill J supplied, unmodified, kept for
  comparison. Not loaded as a skill.

For illustrated or mascot characters (a style descriptor and one style-key image on every clip), see
`consistent-character-images` section 8.

Adapted from `higgsfield-timed-prompts` (a skill J supplied on 2026-10-13; author and licence
unknown). This rewritten version is ours and may be shared; the verbatim original in `sources/` stays
in the private brain and is never copied into a public repo. Video lessons
from Higgsfield's MIT-licensed skills repo (start-frame prompts, voice first, narration mode) are
listed in `consistent-character-images/references/sources.md`.
