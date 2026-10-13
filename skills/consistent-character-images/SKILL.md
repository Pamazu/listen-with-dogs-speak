---
name: consistent-character-images
description: Make still images of the SAME character (a dog or any animal first, a person too) in new scenes, outfits, moods and styles, on any image model or platform (Seedream, Nano Banana, GPT Image, Higgsfield Soul 2.0, our own platform) WITHOUT needing a trained identity such as Soul ID. Covers the reference-photo set, character sheets, the identity-lock prompt block, scene prompts, expressions as body language, surgical edits, variants, style keys and the check after each render. Use whenever a recurring character must look like itself across images, when a Soul 2.0-style shoot is wanted on a platform without Soul, when preparing start frames for video, or when a generated character drifted.
---

# Consistent character images

The job a trained-identity model does (Higgsfield's Soul ID + Soul 2.0, a LoRA, a platform
"character"): the same character, recognisable in every new image. This skill does that job with
what every modern image model accepts, reference images plus a fixed text block, so it runs on any
platform and on our own. A trained identity is an optional extra (section 9), never a requirement.

It is written animal-first, because our work is mostly dogs. Each block has a person variant.

Write every generation prompt in English; talk to J in his language.

## 0. Rules that always hold

- **Identity comes from three things, every time**: the reference photos, the identity-lock block
  (section 3) pasted unchanged, and a check of the result (section 7). Leave out one and the
  character drifts.
- **One file per character is the source of truth**: its reference photos and its identity text live
  in one folder (in a project repo: `characters/<name>/`). Prompts copy from it; nobody edits identity
  inside a single prompt.
- **Name every reference in the first line** of the prompt (section 4). Models that see four
  unlabelled images guess which one is the dog.
- **One prompt per variant.** When variants must differ (concept, expression, camera), write one
  prompt each and keep references and settings fixed. A "make 4" count gives paraphrases, not choices.
- **Write what you want, not what you fear**: "tack sharp" instead of "no blur", "an empty street"
  instead of "no people". Negatives only as a short tail.
- **Check the price first** where the platform allows (Magnific `simulate_cost`); draft cheap, final
  once.
- **Never** a real public figure, a trademarked or branded character, or a real person's face without
  their consent.

## 1. The reference photo set

The photos ARE the identity. Spend time here; it is cheaper than any number of retries.

**How many:** 8-12 is the sweet spot, 5 the minimum. A prompt can take only the model's reference
limit (Seedream 5 Pro: up to 10; Seedance 2.5 video: up to 30), so keep a **core set of 4-6** for
prompts and the full set for training or for picking.

**Each photo:** one animal only, sharp, eyes visible, at least 1024 px on the short side, no filters,
no heavy compression.

**Variety (this is what makes it work):**
- **Angles:** front, three-quarter left, three-quarter right, both profiles, slightly from above and
  from below.
- **Both sides of the body.** Markings are rarely symmetrical; a patch on the left flank must be seen
  on the left.
- **Distances:** head, head and shoulders, full body standing, sitting, lying down.
- **Mouth:** closed, open and relaxed, panting, and one mid-bark or "talking" if the character will
  speak in video.
- **Light:** indoor and outdoor, soft and hard.

**Dog details the set must show clearly:** coat colour, length and texture; every marking and its
side; eye colour (and heterochromia); nose colour; ear set and carriage (up, folded, one of each);
muzzle length; tail shape and carriage; paws and their colour; size against something known; the
collar and tag if it is part of the look.

**Avoid:** other animals or people in frame, costumes, hats or bandanas the character does not
normally wear, a fresh grooming cut unless that is the canonical look, motion blur, the same pose
repeated.

**Date the set.** Puppies change month to month and coats change with seasons; when the real dog
changes, make a new set and say which clips used which.

**For a person:** the same, minus coat and tail: clear face, no sunglasses or hats over the face,
neutral, smiling and talking expressions, head shot to full body, no group photos, no heavy make-up
they do not normally wear.

## 2. The character sheet (when photos are not enough or the character is invented)

Make one sheet, approve it once, then cut it into separate files that become the character's
reference images. Never regenerate it per scene.

```
Character reference sheet of ONE dog, <identity text from section 3>. Five views of the same dog
side by side on a plain light-grey studio background, identical soft even lighting in every view:
front view sitting, three-quarter view standing, left profile standing, right profile standing,
close-up of the face with the mouth slightly open. Same scale in every view, whole body visible,
tack sharp, photographic. No text, no labels, no props.
```

- **From real photos:** attach the best 4-6 photos and add a first line naming them (section 4) and
  "match this exact dog".
- **Invented dog:** describe it with the identity text; generate several sheets and let J pick one.
- **Illustrated or mascot dog:** add the style descriptor (section 8) and end with "illustrated, not a
  photo".
- Use the image model `best-model-per-job` names for character sheets; Seedream 5 Pro and Nano Banana
  are the candidates (character reference type on Magnific), UNTESTED against each other for dogs.

## 3. The identity-lock block

Written once per character, in its folder, pasted unchanged into every prompt.

**Animal:**
```
CHARACTER 1: <Name>, the dog in reference images 1-4. IDENTITY LOCK: reproduce this exact dog,
a photographic identity match: <breed or mix>, <size and build>, <head and muzzle shape>,
<eye colour and shape>, <ear set and carriage>, <nose colour>, <coat colour, length and texture>,
<each marking and its side>, <tail shape and carriage>, <collar and tag>. Do not turn it into a
generic or "average" dog of the breed, do not beautify, re-colour or restyle it. Real dog anatomy:
four legs, paws, a dog's mouth and teeth.
```

**Person:**
```
CHARACTER 1: <Name>, the person in reference images 1-3. IDENTITY LOCK: reproduce this exact person
with a photographic identity match: same bone structure, eye shape, nose, lips, jawline, skin tone,
hairline and hair texture. Do not beautify, average or restyle the face.
```

Up to three characters per image is the practical limit; each gets its own numbered block.

## 4. The scene prompt (the Soul 2.0-style still)

Assemble in this order. The fixed blocks (manifest, identity, style) are pasted unchanged; the
scene part stays short, because long free text makes models drift.

1. **Reference manifest**, first line whenever two or more images are attached:
   `IMAGE REFERENCES: images 1-4 = BISCUIT (dog); image 5 = the kitchen; image 6 = style only.`
   On platforms that use handles, the handle names do this job (`@biscuit_front`).
2. **Format:** "<aspect>, single photograph" (or the illustration style).
3. **Scene:** one clear moment: who, doing what, where. One sentence or two.
4. **Characters:** the identity-lock block(s), then the expression (section 5) and pose.
5. **Key elements:** only props that matter to the moment.
6. **Location:** place, time of day, weather. For an existing place, a location reference image.
7. **Composition:** where the character sits in frame (a third, centred), how large, camera height.
   For dogs, camera at the dog's eye level unless the shot is about looking down at it.
8. **Light:** direction and quality ("soft window light from the left, warm rim on the fur").
9. **Look / grade:** the style descriptor (section 8) or a short photographic look ("clean editorial
   photograph, 50mm, shallow depth of field, rich natural colour").
10. **Text:** "No text, no watermark" unless text is wanted.

**Editorial and social looks** (what Soul 2.0 is known for): pick one and keep it for a series:
candid phone photo (natural light, slight grain, eye-level, imperfect framing); clean editorial
(studio or styled set, controlled light, magazine framing); cinematic still (wide lens, motivated
light, film-like colour); lifestyle (a real home or street, the character mid-action).

**Locations without the character:** make empty location plates separately ("an empty sunlit
kitchen, morning, nobody in frame"), approve them, then use them as location references. The place
then stays the same across a series.

## 5. Expressions are body language

Models render "a sad dog" or "a happy dog" as stock. Describe the body instead:

| Wanted | Write |
|---|---|
| Happy | soft eyes, mouth open and relaxed, tongue slightly out, ears loose, tail mid-wag |
| Alert | ears forward, mouth closed, head up, weight forward, eyes on one point |
| Curious | head tilted to one side, ears up, mouth closed |
| Sorry / guilty | head low, ears back, eyes looking up, tail low |
| Excited | play bow, front legs down, rear up, tail high, mouth open |
| Calm | lying down, eyes half-closed, chin on paws |
| Proud | sitting tall, chest out, head up, mouth closed |
| Suspicious | head slightly turned, eyes to the side, mouth closed |
| Talking | mouth mid-word, jaw half open, eyes on the listener |

For a person: name the emotion and one physical cue ("shock: eyebrows up, mouth open").

## 6. Edits and variants

- **With a reference image, describe the change, not the image again.** "Make it a snowy evening" beats
  re-describing the whole dog.
- **Surgical edit** (one thing changes, everything else stays), with the picked image as the only
  input:
  ```
  Change ONLY <the expression to: ears back, head tilted / the background to: a park at dusk>.
  Keep the dog's identity, coat, markings, pose, collar, framing, lighting and everything else
  exactly unchanged.
  ```
  One scope per edit: expression, background, background colour, light colour, an outfit or
  accessory. Each accepted edit becomes the source for the next one. Never regenerate the whole
  image for a small change.
- **Variants:** same references and settings, one line different (expression, camera height, time of
  day). Name each variant by what differs ("curious / low angle").

## 7. Check every result before showing it

- The character matches the references: markings on the right side, eye and nose colour, ears, tail,
  collar.
- Anatomy: four legs, one tail, paws (not hands), the right number of toes and teeth showing.
- No stray text, logos or watermark; any wanted text spelled exactly.
- The expression reads at thumbnail size.

On a failure, retry the same prompt at most twice; after that, change the prompt (more references,
a shorter scene, a firmer identity line) or the model. If you cannot look at the image, say so
instead of passing it.

## 8. Illustrated and mascot characters

- **Style descriptor:** one line describing render style, palette, line and finish, pasted into every
  prompt. End illustrated styles with "illustrated, not a photo".
- **Style key:** one approved image that shows the style, attached to every prompt as a style
  reference. With a style reference, say: "Take only the render style and colour of the style image;
  never copy its characters, text or objects."
- **Mascot key:** `<style>. Full-body character: <Name>, a <breed> narrator, expressive, clear
  readable silhouette, looking at camera, centred, simple background. Recurring-character design.
  No text.` Approve it, then it is the mascot's reference image.

## 9. Trained identities (optional)

Soul ID, a LoRA, or a platform "character" can sharpen identity once a character recurs a lot.
Higgsfield's Soul ID is documented for people's faces (5-20 face photos); whether it holds a dog is
UNTESTED. Use one only where the platform is already in use and a side-by-side test against the
reference-image method (same prompts, same scenes) shows it wins. The photo set from section 1 is
what any of them trains on, so it is never wasted.

## 10. Where to run it now

- **Magnific (J's account):** `images_generate` with `references` of type `character` (identity),
  `image` (location), `style` (style key). Models listing `character_consistency`: Seedream 5 Pro
  (the catalog's default), Nano Banana Pro (fidelity on finals); Nano Banana 2 Lite for cheap drafts.
- **Higgsfield:** the same blocks work in Soul 2.0, Seedream or Nano Banana prompts; add a Soul ID only
  per section 9.
- **Dreamina, our own platform, a raw API:** the same blocks; only how images are attached changes.
- Which model wins for dogs is UNTESTED: run the same 3 scenes on the candidates and record the winner
  in `0_Global/reference/best-model-per-job.md`.

For video of the same character, the approved stills become start frames or references in
`timed-video-prompts`.

## Files

- `references/sources.md`: which Higgsfield skills this draws on, what was taken, what was left, and
  their licence.
- `sources/higgsfield-ai-skills/`: the eight original Higgsfield skills, unmodified, for comparison.
  Not loaded as skills.
