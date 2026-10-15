# Design

## Idea
An editorial page about a person, not a product page. It should feel like a well set magazine profile: one column of text, generous margins, rules between sections, nothing that moves.

## Type
- **Headings: Newsreader** (Production Type, open source). A text serif drawn for reading on screens, with real character in the bold weights. It gives the name weight and warmth, and a serif reads as "doctor and writer" rather than "startup landing page".
- **Body: Source Sans 3** (Adobe, open source). A humanist sans with open letter shapes. It stays clear at small sizes on cheap Android screens, which is where most Indian readers will open this.
- Both are self-hosted (5 files, about 100 KB total, Latin subset only). No Google Fonts request, nothing leaves the domain.
- Avoided on purpose: Inter, Geist, Space Grotesk.

## Colour
| Token | Hex | Use |
|---|---|---|
| paper | #F5F0E6 | Background. Warm off-white, never pure white |
| ink | #1E1A16 | Text |
| muted | #5B5248 | Secondary text, nav |
| rule | #D8CDBB | Hairlines between sections |
| accent | #8A3A1E | Links and the one highlight. A burnt sienna: warm, serious, and far from the clinical blue every dental AI company uses |

All text combinations pass WCAG AA (ink on paper is about 15:1, accent on paper about 7:1).

## Layout
- One reading column (38rem) inside a 62rem frame. The right side stays empty on desktop and will take the headshot once real photos arrive.
- Sections are separated by thin rules, not cards. Lists are rows, not grids. No three-across features, no bento.
- No shadows, gradients, glows, emojis, icon sets, or hover animations. Link hover only thickens the underline, with no transition.

## Performance
- Zero JavaScript. One 5 KB stylesheet. JSON-LD is data, not code.
- Lighthouse (local, 2026-10-15): 100 / 100 / 100 / 100 on /, /about and /work.

## Stack: why plain HTML from a small Python script
Astro would work, but it adds a Node toolchain, a lockfile and upgrades to maintain for nine pages. A 250 line standard library script does the same job: shared header and footer, one Person JSON-LD source of truth on every page, sitemap, robots and IndexNow. Anyone can read it, and it will still build in ten years. If the writing section grows past a few dozen articles, revisit this.
