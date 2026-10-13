---
name: consistent-character-images
description: For ONE character or object (e.g. a dog called Coco), write the full set of image-generation prompts for its reference images, one prompt per view (front, back, left side, right side, three-quarter) and one per view for each useful expression (neutral, happy, sad, angry, surprised, curious, talking ...), each producing one clean image on a plain neutral background that contrasts with the character, precisely matching the reference photos. Real characters start from reference photos; imaginary ones from a description and an anchor image. The images then serve as references for a video model. Dogs and animals first, people and objects too; any image model or platform (Seedream, Nano Banana, GPT Image, Higgsfield Soul 2.0, our own), no Soul ID needed. Never a video prompt, a scene or a multi-character set.
---

# Consistent character images

**Input:** one character or object, usually with reference photos. **Output:** every prompt needed to
make its reference images, one image per prompt:

- one prompt per **view**: front, back, left side, right side, three-quarter;
- one prompt per view for each **expression**: neutral, happy, sad, angry, surprised, curious, and
  talking if the character speaks (more on request).

For Coco with the defaults that is 5 views × 7 expressions = 35 prompts. The finished images become
Coco's references for a video model later (`timed-video-prompts`).

**Not this skill:** a video prompt, a scene with the character acting, several characters at once, or a
multi-panel sheet. One character per run; one view and one expression per image.

Write every prompt in English; talk to J in his language.

## 1. Start from the reference photos

**Real character (the usual case):** the photos are the truth. Before writing anything, look at every
photo and write down precisely what is there; never invent a detail the photos do not show.
- **Animal:** species and breed or mix, size and build, coat colour, length and texture, every marking
  and which side it is on, eye colour, ear set, nose colour, tail shape and length (not its position: where the ears and tail sit belongs to the expression), collar and tag.
- **Person:** face shape, eyes, nose, lips, skin tone, hair colour, length, texture and style, build,
  and every garment, shoe and accessory with its colour.
- **Object:** shape, size, colours, materials, finish, printed marks.

Pick the 4-6 best photos to attach to every prompt. Good photos: only this subject, sharp, eyes visible,
at least 1024 px, no filters, front, three-quarters and both sides (markings differ by side), mouth
closed and open. If the photos miss a side or a detail, say so: the prompt for that view will be a
guess until a photo exists.

**Imaginary character (no photos):** the description carries everything. The first prompt (front,
neutral) makes the **anchor image**; generate it, let J approve it, then attach it to every other
prompt. From then on the anchor is the character's reference photo.

## 2. Write the character file

```json
{
  "name": "Coco", "handle": "coco", "kind": "animal", "species": "dog",
  "tone": "light",
  "references": ["coco_photo_1.jpg", "coco_photo_2.jpg", "coco_photo_3.jpg", "coco_photo_4.jpg"],
  "identity": "<the precise description from section 1, one paragraph>",
  "drift": "<the 2-3 details most likely to change between images, e.g. the patch on the LEFT ear only>",
  "views": ["front", "back", "left", "right", "three_quarter_left"],
  "expressions": ["neutral", "happy", "sad", "angry", "surprised", "curious", "talking"]
}
```

- `kind`: `animal`, `person` or `object` (objects get views only, no expressions).
- `tone`: the subject's main colour, `light`, `mid` or `dark`. It picks a plain backdrop that contrasts
  with it: light subject on mid-dark slate grey, mid on light cool grey, dark on light warm grey.
- `references`: empty for an imaginary character.
- Extra views: `three_quarter_right`, `face` (a close-up, useful for expressions and lip sync).
- Extra expressions: `scared`, `excited`, `sleepy`; anything else goes in `custom_expressions` with its
  body-language description.

`examples/coco.json` is a complete one.

## 3. Generate the prompts

```
python3 scripts/view_prompts.py coco.json          # Markdown, to read and copy
python3 scripts/view_prompts.py coco.json --json   # JSON, for batch runs or our own platform
```

The script refuses a file with a missing field, an unknown view or expression, or a tone that is not
light, mid or dark. Every prompt shares the same wording; only the view line and the expression line
change. That shared wording is what keeps the character identical, so do not hand-edit single prompts:
change the character file and run it again. `examples/coco-prompts.md` is the full output for Coco.

Each prompt carries, in order: the view, the expression written as body language, the identity text
(introduced by "the dog in the attached reference photos, reproduced exactly"), the details to keep
exactly, full-body framing with space around it, the plain contrasting backdrop with soft even light
and a gentle rim light, camera at eye level with an 85mm lens, and "photorealistic, tack sharp,
colours true to the reference; only this one dog, no text, no props".

**Expressions are body language**, because image models draw "a sad dog" as stock. The script's
table: happy = soft eyes, open relaxed mouth, tongue slightly out, tail mid-wag; sad = head hanging
low, ears flat back, eyes looking up mournfully, tail down, shoulders slumped (milder wording came out
looking neutral in the test); angry = muzzle wrinkled, front teeth showing, ears
pinned, body stiff; surprised = eyes wide, ears up, mouth slightly open; curious = head tilted, ears
up; talking = mouth half open mid-word, real dog mouth, no human lips. From behind, the mood shows in
ears, tail and posture.

## 4. Run them

- Same model and settings for the whole set (1:1 or 16:9, 2k). Attach the reference photos (or the
  anchor) to every prompt.
- Imaginary character: prompt 1 first, approval, then the rest with the anchor attached.
- On Magnific: `images_generate`, `mode: seedream-5-pro`, references of type `image`; 100 credits per
  image at 2k (2026-10-13), so a 35-image set costs about 3,500. Check `simulate_cost` first.
- On any other platform or our own: the same prompts; only how photos are attached changes.

## 5. Check every image before keeping it

- **It is the same character as the references:** each drift detail, markings on the correct side, eye
  and nose colour, ears, collar and tag, outfit.
- **The view is the one asked for:** left profile shows the left side with the head to frame left.
- **The expression reads**, and anatomy is right: four legs, one tail, paws not hands, correct teeth.
- **Clean:** plain backdrop, whole body in frame, nothing else, no text.

Generate again with the same prompt at most twice. Then fix:
- **One detail wrong:** a surgical edit with that image as the only input: "Change ONLY <the detail>.
  Keep everything else exactly unchanged."
- **Keeps drifting:** attach the best image so far alongside the photos, or switch model (Nano Banana
  Pro for the highest fidelity).

If you cannot look at the image, say so instead of passing it.

## 6. Trained identities (optional)

Soul ID, a LoRA or a platform "character" can be trained from the same photos once a character recurs
a lot. Higgsfield's Soul ID is documented for people's faces; whether it holds a dog is UNTESTED. Use
one only if a side-by-side test against this method shows it wins.

## 7. Tested

2026-10-13, Seedream 5 Pro on Magnific, imaginary Coco, no photos: see `examples/coco-test.md`.

## Files

- `scripts/view_prompts.py`: character file → every view and expression prompt.
- `examples/coco.json`, `examples/coco-prompts.md`: a complete character file and its 35 prompts.
- `examples/coco-test.md` and its images: what four of those prompts produced.
- `references/sources.md`: which Higgsfield skills this draws on, and what was taken and left.
- `sources/higgsfield-ai-skills/`: the eight original Higgsfield skills, unmodified. Not loaded as
  skills.
