# Teaching site builder (slides + speaker notes)

Builds the markdown in `site/` into `_site/` (gitignored) and deploys it to GitHub Pages
with `.github/workflows/site.yml`. Every page carries `<meta name="robots" content="noindex">`.

```bash
uv run --with markdown --with pymdown-extensions --with pygments python scripts/site/build.py
python -m http.server -d _site 8000      # then open http://localhost:8000/
```

## Layout

| Source | Output |
| --- | --- |
| `site/index.md` | `/` (plain markdown page) |
| `site/<module>/slides.md` | `/<module>/` slides page, plus `/<module>/notes/` speaker notes |
| `site/<module>/assets/*` | `/<module>/assets/*` - put slide images (SVG, PNG, JPG) here |

The notes page is generated but never linked from any page. Share its URL privately.
A module with no `@slide` lines gets a page with no deck and no notes page.

## Slide syntax

A line that starts with `@` is a directive. Everything before the first `@slide` is the module
title (`# Title`) and an optional intro, shown above the slides.

| Directive | Where | Meaning |
| --- | --- | --- |
| `@slide Title` | starts a slide | required, one line |
| `@idea One sentence.` | slide | the one big idea (optional, once) |
| `@image assets/x.svg \| Alt text` | slide | optional, once. **Alt text after the `\|` is required**; the build fails without it. File must exist under the module folder |
| `- bullet` | slide | optional, at most 5 per slide |
| `@source Where this came from` | slide | optional small footnote |
| `@notes` | starts speaker notes | everything after it, until the next `@slide`, is notes (markdown: bullets, paragraphs, code fences) |
| `@time 9:42` | inside notes | 24-hour H:MM in **US Central (America/Chicago)**. Shown on the notes page as "Should be here by 9:42", and as minutes ahead/behind in the speaker window (see Pace modes) |

Inline markdown (`code`, **bold**, *italic*, links) works in titles, ideas, bullets and sources.
Any other text between `@slide` and `@notes` is a build error, so notes can never leak onto a slide.
Notes are never rendered on the slides page. The slide number is drawn on every slide.

### Full example

```
# Foundations: agents, tasks, and crews

Optional intro paragraph, shown above the slides (not on a slide).

@slide An agent is a role with a goal
@idea Think of a new hire: a job title, a clear goal, and a bit of background.
- Role: who the agent is
- Goal: what it is trying to get done
- Backstory: how it should approach the work
@source Northwind Auto Finance sample data, not real customer information
@notes
- Open with the new-hire analogy.
- Ask the room one question, take one answer.
@time 9:42

@slide A crew runs agents in order
@idea Each agent does one small job and hands its result to the next.
@image assets/sequential-crew.svg | Three boxes in a row: intake agent, policy agent, reply agent, joined by arrows.
@notes
Walk the arrows left to right.
@time 9:58
```

## Using it

Slides page: **Present** button or `P` for full screen, one slide at a time. Next: arrow right/down,
space, PageDown (most clickers send PageUp/PageDown). Previous: arrow left/up, PageUp, Shift+space. `Home`/`End` first/last. Type a number
then `Enter` to jump. `B` or `.` blanks the screen to black and `W` to white; press the same key again to come back (any navigation key also returns, and `Esc` returns before it exits). `Esc` exits (first press clears a half-typed number). Out of present mode the page
scrolls, with a left list of slide titles.

Speaker view: `S` (or the button) opens the notes page in a popup in follow mode. It follows the slide
via BroadcastChannel (same browser, same origin), shows the next slide's title, a clock, a timer, and
pace against `@time` (see Pace modes). Its Previous/Next/jump also drive the slides window. Open it before presenting.

Notes page on an iPad: open `/<module>/notes/` directly. It lists every slide with a mini preview,
notes and timing; large Previous/Next buttons and a jump box. Cross-device follow is not possible
(BroadcastChannel is per browser), so on the iPad you tap through yourself.

## Pace modes (speaker view)

`@time` values are written in Central time, so the pace line has a mode switch next to the timer:

- **Rehearsal** - targets are relative to the timer. Press Start on the first slide; the first slide with an
  `@time` is 0:00 elapsed and every other target is offset from it (a slide at 9:58 when the first is 9:42
  is due at 16:00 elapsed). Until the timer has been started the line says so. Works in any time zone, any day.
- **Live (CT clock)** - targets are compared to the America/Chicago wall clock, whatever the laptop's time
  zone is set to. The clock readout switches to Central time and is labelled CT.

Default is Rehearsal, except when today is 2026-11-04 in America/Chicago, when it is Live. Your choice is
remembered in `localStorage` (key `workshop-pace-mode`, per browser; if storage is blocked the default is used).
