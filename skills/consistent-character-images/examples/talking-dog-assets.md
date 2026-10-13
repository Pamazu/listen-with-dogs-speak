# Example output: assets for "Biscuit asks for the walk"

This is what the skill hands back for a brief like "Biscuit, a golden retriever, sits in the kitchen
and asks for his walk". Image prompts only; the video prompt is written afterwards with
`timed-video-prompts`, attaching the three saved files.

Assets: `@char_biscuit` (dog sheet), `@char_biscuit_mouth` (mouth sheet, because he talks),
`@loc_kitchen` (location).

---

@char_biscuit: dog reference sheet
Model: Seedream 5 Pro on Magnific · 16:9 · 2k
Attach: none (invented dog)
Save as: characters/biscuit/char_biscuit.png
Prompt:
```
Animal reference sheet for an AI video: one photograph divided into three equal vertical panels
side by side, separated by thin straight gaps, all on the same seamless light-grey studio background
with soft, even, shadowless studio light, identical in every panel.
Panel 1 (left): close-up of Biscuit's head and shoulders, face straight on, eyes open and looking into
the lens, mouth closed, ears relaxed.
Panel 2 (centre): the same dog, full body standing in left profile, the whole body, legs, paws and tail
inside the frame.
Panel 3 (right): the same dog, full body standing in right profile, the whole body, legs, paws and tail
inside the frame.
Biscuit is a medium-sized golden retriever with a wavy honey-gold coat, a paler cream chest and
feathering on the legs, dark brown eyes, soft folded ears, a black nose, a white blaze only on the left
side of the muzzle, and a red leather collar with a round brass tag.
The exact same dog in all three panels: identical coat colour, the white blaze on the left side of the
muzzle, the same collar and the same size. Photorealistic, tack-sharp fur detail. No text, no labels,
no props, no other animals or people.
```
Result of this exact prompt: `char_biscuit_test.jpg`. Layout, coat, collar and the blaze's side held;
the head reads slightly narrower in the profiles than in the close-up, so it fails the "same dog in
every panel" check by a little. Fix: generate panel 1 alone, then each profile with panel 1 attached.

---

@char_biscuit_mouth: mouth sheet
Model: Seedream 5 Pro on Magnific · 16:9 · 2k
Attach: char_biscuit.png (the approved sheet)
Save as: characters/biscuit/char_biscuit_mouth.png
Prompt:
```
Mouth reference sheet for an AI video of a talking dog: one photograph divided into three equal
vertical panels side by side, the same seamless light-grey studio background and soft even studio
light in each. All three panels are the same close-up of the dog in the attached reference image,
face straight on, eyes open and looking into the lens.
Panel 1: mouth closed. Panel 2: mouth half open as if in the middle of a word, tongue visible.
Panel 3: mouth wide open as if barking.
The exact same dog, head size and position in all three panels; only the mouth changes. A real dog's
mouth, teeth and tongue, no human lips. Photorealistic, tack sharp. No text, no labels.
```

---

@loc_kitchen: location
Model: Seedream 5 Pro on Magnific · 16:9 · 2k
Attach: none
Save as: locations/loc_kitchen.png
Prompt:
```
Location reference photo for an AI video, 16:9: a bright family kitchen, seen from a dog's eye level
about 50 cm above the floor, 24mm wide lens, facing a closed white kitchen door with a red dog lead
hanging on a hook beside it. Morning, warm sunlight from a window on the right. Light wooden floor,
white cabinets on the left, a water bowl on the floor by the cabinets. Completely empty of people and
animals. Photorealistic, rich natural colour, tack sharp. No text.
```
