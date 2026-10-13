---
name: consistent-character-images
description: Write IMAGE-generation prompts that produce reference sheets (one image per character, animal, group, prop or location, saved as @char_x / @loc_x / @prop_x) to attach later to a VIDEO model so every clip keeps the same characters. Dogs and other animals first, people too; works on any image model or platform (Seedream, Nano Banana, GPT Image, Higgsfield Soul 2.0, our own platform), no Soul ID needed. Use when a video project needs its character, prop or location references made, when a Soul 2.0-style character reference is wanted on any platform, or when a reference sheet came back inconsistent. Output is image prompts only, never a video prompt or a story scene (that is timed-video-prompts, which uses these sheets).
---

# Consistent character images: reference sheets for video

This skill turns a brief or script into **one image-generation prompt per asset**. Each prompt makes a
reference sheet: the same character shown in a few clean views on a plain studio background, or an
empty location, or a prop from several sides. The saved sheets are attached to a video model later,
named by their handles (`@char_biscuit`, `@loc_kitchen`, `@prop_ball`), and the video prompt
(`timed-video-prompts`) refers to them.

## 0. What this skill produces, and what it never produces

**Produces:** a list of assets, and for each asset one block in this format:

````
@char_biscuit: dog reference sheet
Model: an image model that accepts reference images (on Magnific: Seedream 5 Pro) · 16:9 · 2k
Attach: biscuit_photo_1.jpg … biscuit_photo_4.jpg   (real dog only; "none" for an invented one)
Save as: characters/biscuit/char_biscuit.png
Prompt:
```
<the image prompt, from the templates in section 3>
```
````

**Never produces:** a video prompt, a shot list, camera moves, dialogue, sound, or a picture of the
characters acting in the story. Those belong to `timed-video-prompts`, which takes these sheets as its
references. If asked for a scene, make the sheets first and hand over to that skill.

Write every prompt in English; talk to J in his language.

## 1. Make the asset list first

Read the brief or script and list everything that must look the same from clip to clip:

| Kind | Handle | One sheet shows |
|---|---|---|
| Person | `@char_<name>` | face close-up + full body front + full body back |
| Animal | `@char_<name>` | face close-up + both full-body profiles (or a sitting three-quarter view) |
| Talking animal, extra | `@char_<name>_mouth` | face close-up with mouth closed, half open, wide open |
| Group (a band, a team) | `@char_<group>` | every member, full body, side by side, facing camera |
| Prop | `@prop_<name>` | front + back + three-quarter |
| Location | `@loc_<name>` | one wide empty view from the first shot's camera angle |

Handles are lowercase with underscores, the same as the saved file name. One sheet per handle; a
character who changes clothes gets a second handle (`@char_mika_coat`).

## 2. Where identity comes from

- **A real animal or person:** attach 4-6 of the best photos (section 5) and say "the dog in the
  attached photos" in the prompt. The photos lead; the text confirms.
- **Invented:** the identity text below carries everything. Generate 2-4 sheets and let J pick one;
  from then on that sheet IS the character, never regenerated per clip.

**Identity text**, written once per character and pasted unchanged into its sheet prompt:

- **Animal:** `<Name> is a <size> <breed or mix> with a <coat colour, length, texture> coat,
  <each marking and which side it is on>, <eye colour> eyes, <ear set>, a <nose colour> nose,
  <tail shape>, and <collar and tag>.`
- **Person:** `<Name> is a <age range> <build> person with <skin tone>, <face shape, eye shape,
  nose, lips>, <hair colour, length, texture, style>, wearing <every garment with colour and fit,
  shoes, glasses, jewellery>.`

## 3. Sheet prompt templates

All sheets: one photograph, **16:9**, plain seamless light-grey studio background, soft even light,
identical in every panel, nothing else in frame, no text. The panels must show the SAME character:
say so, and name the detail most likely to drift (a marking's side, glasses, a logo).

**Animal (dog, cat, any pet):**
```
Animal reference sheet for an AI video: one photograph divided into three equal vertical panels
side by side, separated by thin straight gaps, all on the same seamless light-grey studio background
with soft, even, shadowless studio light, identical in every panel.
Panel 1 (left): close-up of <Name>'s head and shoulders, face straight on, eyes open and looking into
the lens, mouth closed, ears relaxed.
Panel 2 (centre): the same <animal>, full body standing in left profile, the whole body, legs, paws
and tail inside the frame.
Panel 3 (right): the same <animal>, full body standing in right profile, the whole body, legs, paws
and tail inside the frame.
<identity text>
The exact same <animal> in all three panels: identical coat colour, <the drift-prone detail>, the same
collar and the same size. Photorealistic, tack-sharp fur detail. No text, no labels, no props, no
other animals or people.
```
Both profiles because markings are rarely symmetrical. If the animal's markings are the same on both
sides, panel 3 may be "sitting, three-quarter view" instead (as in a cat sheet).

**Talking animal, mouth sheet** (helps lip sync): three face close-ups straight on, same light and
background: "mouth closed", "mouth half open as if mid-word, tongue visible", "mouth wide open as if
barking". Real animal mouth and teeth, no human lips.

**Person:**
```
Character reference sheet for an AI video: one photograph divided into three vertical panels side by
side, all on the same seamless light-grey studio background with soft, even studio light, identical in
every panel.
Panel 1 (left, widest): head-and-shoulders close-up of <Name>, facing the camera, <neutral / light
smile>.
Panel 2 (centre): the same person, full body from head to shoes, facing the camera, standing straight,
arms relaxed at the sides.
Panel 3 (right): the same person, full body seen from behind, the same stance.
<identity text, including the full outfit>
The same person, outfit and scale in all three panels. Photorealistic, tack sharp, natural skin
texture. No text, no labels, no props, nobody else.
```

**Group:**
```
Reference photo of <the group> for an AI video, 16:9: all <N> members standing side by side in one row,
full body from head to shoes, facing the camera, evenly spaced, nobody overlapping, <setting: plain
light-grey studio, or the scene's location if they only ever appear there>, soft even light.
From left to right: <member 1: build, face, hair, outfit, what they hold>; <member 2: ...>; ...
Everyone fully visible. Photorealistic, tack sharp. No text, no labels, nobody else.
```

**Prop:**
```
Product reference sheet for an AI video: one photograph divided into three panels side by side, the
same seamless light-grey studio background and soft even light in each.
Panel 1: <the prop> from the front. Panel 2: the same <prop> from the back. Panel 3: the same <prop> in
a three-quarter view.
<exact shape, size, colours, materials, finish, any markings or our own logo>.
The identical object in all three panels. Photorealistic, tack sharp. No text except <the prop's own
printed text, spelled exactly>, no hands, nothing else.
```

**Location:**
```
Location reference photo for an AI video, 16:9: <the place>, seen from <the camera position and height
of the first shot>, <lens, e.g. 24mm wide>. <Time of day and light.> Dressed exactly as the scene
needs: <furniture, the number of chairs and place settings, key objects and where they stand>.
Completely empty of people and animals. Photorealistic, rich natural colour, tack sharp. No text.
```

## 4. Check every sheet before saving it

- **Same character in every panel.** The most common failure is a slightly different animal or face in
  one panel: compare markings, the side they are on, eye colour, ears, collar, glasses, outfit.
- **Matches the photos** (real subject) or the identity text (invented).
- **Clean sheet:** plain grey background, whole body in the full-body panels, nothing cropped, no
  props, no extra people or animals, no text or labels.
- **Anatomy:** four legs and one tail; paws, not hands; the right number of fingers on a person.

On a failure, generate again with the same prompt at most twice. Then fix it:
- **One panel wrong:** a surgical edit with the sheet as the only input: "Change ONLY panel 3 so the
  dog matches panels 1 and 2: <the detail>. Keep everything else exactly unchanged."
- **Panels keep disagreeing:** generate panel 1 alone, approve it, then generate each other view with
  panel 1 attached as the reference, and join the panels side by side (`ffmpeg -i a.png -i b.png -i
  c.png -filter_complex hstack=3 sheet.png`).

If you cannot look at the image, say so instead of passing it.

## 5. Photos of a real animal (the input for section 2)

8-12 photos, at least 5; keep the best 4-6 for attaching. Each: only this animal, sharp, eyes visible,
at least 1024 px, no filters. Cover: front, both three-quarters, both profiles (markings differ by
side), head, full body standing, sitting and lying, mouth closed and open (and mid-bark if it will
talk), indoor and outdoor light. Avoid costumes the animal does not normally wear, motion blur, other
animals, the same pose twice. Date the set; puppies and coats change. For a person: the same, with the
face clear, no sunglasses or hats over it, no group photos.

## 6. Illustrated or mascot characters

Add one style line to every sheet prompt ("hand-painted storybook gouache, soft textures, warm muted
palette, visible brush strokes, illustrated, not a photo") and, once a sheet is approved, attach it as
the style reference for the other sheets: "Take only the render style and colour of the style image;
never copy its characters, text or objects." Keep the same panel layout.

## 7. Trained identities (optional)

Soul ID, a LoRA or a platform "character" can be trained from the same photos once a character recurs a
lot. Higgsfield's Soul ID is documented for people's faces; whether it holds a dog is UNTESTED. Use one
only if a side-by-side test against the sheet method shows it wins.

## 8. Where to run it now

- **Magnific:** `images_generate`, `mode: seedream-5-pro` (the catalog's default for character
  consistency; 100 credits for one 16:9 2k sheet on 2026-10-13), real photos as `references` of type
  `image`. Nano Banana Pro for the highest fidelity on a final sheet. Check `simulate_cost` first.
- **Higgsfield, Dreamina, our own platform, a raw API:** the same prompts; only how photos are attached
  changes.
- Which model keeps a dog most consistent is UNTESTED: run the same sheet on the candidates and record
  the winner in `0_Global/reference/best-model-per-job.md`.

**Tested 2026-10-13:** the animal template above on Seedream 5 Pro (invented golden retriever, no
photos), one generation. Layout, coat, collar and the side of the blaze held; the head read slightly
narrower in the profiles than in the close-up, which the check in section 4 catches. Result:
`examples/char_biscuit_test.jpg`.

## Files

- `examples/talking-dog-assets.md`: a complete answer from this skill (dog sheet, mouth sheet,
  location), in the exact output format of section 0.
- `examples/char_biscuit_test.jpg`: what the animal template produced on Seedream 5 Pro.
- `references/sources.md`: which Higgsfield skills this draws on, and what was taken and left.
- `sources/higgsfield-ai-skills/`: the eight original Higgsfield skills, unmodified, for comparison.
  Not loaded as skills.
