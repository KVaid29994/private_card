# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A self-contained wedding invitation card for Kashish & Megha (26 November 2026). Everything — HTML, CSS, JavaScript, and the two embedded images — lives in a single file: `wedding-card.html`. There is no build step, no package manager, and no framework.

## Running locally

Open in a browser directly, or via a local HTTP server (required if anything uses `fetch`):

```powershell
python -m http.server 5500 --directory "<path-to-wedding-card-demo>"
# then open http://localhost:5500/wedding-card.html
```

Adjust the path to match the folder location on your machine.

VS Code Simple Browser: `Ctrl+Shift+P` → `Simple Browser: Show` → enter the localhost URL.

## File structure

| File | Purpose |
|---|---|
| `wedding-card.html` | Entire app — CSS, JS, and base64 images all inline |
| `bride_groom first page-Photoroom.png` | Chibi couple illustration (embedded as data URI in the HTML) |
| `couple_scooter_cutout.png` | Scooter photo for the journey screen (embedded as data URI) |
| `image_1788531523474862_nobg.png` | Additional cutout image (embed as data URI if used) |

**Do not** embed new images manually — use a Python script to base64-encode and splice them in (see the existing pattern in the file), or use `btoa` from the browser console.

## Screen architecture

The card has four full-screen layers stacked via `position: fixed; inset: 0`:

| Screen | ID | z-index | Trigger |
|---|---|---|---|
| 1 — Envelope | `envelopeScreen` | 20 | Click/tap → four flaps peel open, then `leaving` class slides it away |
| 2 — Journey (scooter) | `journeyScreen` | 10 | Appears after envelope leaves; tap advances |
| 3 — Invitation card | `cardScreen` | 10 | Auto-advances after 5.2 s via `dwellTimes` |
| 4 — Celebration events | `eventsScreen` | 10 | Final screen, no auto-advance |

Screens 2–4 are managed by `goToStory(idx)` in JS. The active screen gets class `active`; the departing one gets `leaving`. The `storyIds` array and `dwellTimes` array drive all transitions — to add a screen, push to both arrays and add the HTML element.

## Animation system

All text on story screens uses a **paused-until-active** pattern:

```css
.reveal { opacity: 0; animation: fadeUp 0.85s forwards; animation-play-state: paused; }
.story-screen.active .reveal { animation-play-state: running; }
```

- Timing is controlled entirely by `animation-delay` inline styles on each element.
- Overriding the animation for a specific element: set `animation-name !important` on a more-specific rule (e.g. `.jn-word` overrides `fadeUp` with `nameReveal`).
- The `tap-hint` element uses an `animationend` listener (`startTapHintPulse`) to add a pulse class only after its reveal finishes.
- `.story-screen.leaving .tap-hint` hides the hint instantly (`opacity: 0 !important`) so it doesn't bleed through the 0.6 s screen fade.

## Key design tokens

| Token | Value |
|---|---|
| Background | `#0C1628` (midnight navy) |
| Card surface | `#192035` |
| Gold accent | `#C4A04A` |
| Cream text | `#F5EDE0` |
| Envelope red | `#CF1535` (flap), `#9E0E26` / `#8A0B20` (side folds) |

Fonts loaded from Google Fonts: `Cormorant Garamond` (display, italic), `Jost` (utility labels), and `Caveat` (handwriting accent). Always provide serif/system fallbacks.

## Container query units

Layout uses `cqw` (container query width) units throughout — the `#stage` element is the query container. This keeps all sizing proportional to the card's rendered width regardless of viewport size.
