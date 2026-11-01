# Design audit: AI-slop tells (October 2026)

The site was checked against the tell lists people currently use to spot a
generated page: Impeccable's 46-pattern slop catalog, the open-source
ai-design-checker (14 patterns), unslop-ui / vibecoded-design-tells, The
Fountain Institute's "7 signs a UI has been vibe coded", and the Hacker News
and Product Hunt threads on the same question. Below is what Cardinal tripped,
what changed, and what was kept on purpose.

## What the site tripped, and the fix

| Tell | Where it was | Fix |
|---|---|---|
| Italic accent phrase in a headline ("hero font mix") | 20 headings on the home page, every hero test arm, five article h1s, the characters generator | All headings set roman. `h1 em, h2 em` forced to `font-style: normal` so it cannot creep back. |
| Repeated section kicker labels (tiny tracked red capitals over every heading) | 9 chapters | Replaced by side heads: the feature name hangs in the left margin in the text face, sentence case, under a hairline. Inline above the heading on phones. |
| Cream / beige "tasteful" palette plus paper grain | Whole site | Bright bone paper `#FAFAF7`, true ink `#141414`, one rubric red `#B01F29`. Grain removed. |
| Cards for every block, large radii | Bands, tiles, reviews, plans, FAQ, quote card, support form | No cards. Sections open on a full-width hairline; lists sit between rules, like a book. |
| Icon tile stacked above heading, identical card grid | "Everything else" (6 tiles) | A two-column definition list, no icons. |
| Stat banner / hero metric (giant "5.0" and animated stars) | Reviews | One plain sentence: "Rated 5.0 from 13 ratings on the App Store." |
| Pills and badges | Translation chips, theme chips | Ruled column lists; themes folded into the sentence that names them. |
| FAQ accordion with plus signs | Home page | All ten answers open, question beside answer. |
| Coloured glow on the button, hover lift, magnetic cursor pull | Every primary button | Capsule button in the app's Liquid Glass style, tinted red: thin specular edge, soft lens shading, a neutral drop shadow (no coloured glow), and a small press-in on tap. No hover lift. |
| Image hover transform, bounce/overshoot easing | Showcase, tiles, review cards, star animation | Removed. |
| Fade-up on scroll, staggered deal-ins, headline line reveal, blur-in hero, parallax drift, scroll progress bar | Throughout | Removed. The only motion left is the highlighter drawing once, because it is the app's own gesture. |
| Glassmorphism | Sticky section bar (48px backdrop blur) | Solid paper with a rule. |
| Self-quoting pull quote ("A promise in the source code") | Quote card | Removed; the same line already lives in the Notes section. |
| Aphoristic cadence and contrast tics | "That is the whole app. Everything else was left out on purpose." "You are not the product being sold." 13 uses of "rather than" on the home page | Rewritten into plain statements of fact. "Rather than" cut to the places where the contrast carries meaning. |

## What was already right and kept

- No em dashes anywhere.
- No Inter, no purple, no gradient text, no emoji icons, no 01/02/03 markers.
- System serif (New York on Apple devices), so the page is set in the app's own type.
- Real product screenshots, specific copy, honest limits (Pro translations need a connection, Korean has no licensed Bible yet).
- The red "No" ledger: it is specific to Cardinal's position, not a template device.

## What was deliberately not changed

- Hero headline and lede wording. They are live A/B arms (see EXPERIMENTS.md); changing words mid-round would spoil the test. Only the italic styling was removed, equally for every arm.
- FAQ answer wording on the home page. It mirrors the FAQPage JSON-LD and must stay in step with it.
- Italics inside article body text where they mark a sentence someone says or prays (quiet-time, sermon-notes). That is the standard typographic use, not decoration.

## Rules going forward

1. Headings are roman. No accent word in italic, colour or a second face.
2. No label above a heading that repeats what the heading is about.
3. No card unless the thing is genuinely an object (a form field is; a paragraph is not).
4. Red is rubrication: links, the one button, the side heads, the "No" column, the drop cap. Nothing else.
5. Nothing animates on scroll. Nothing lifts on hover.
7. Buttons are Liquid Glass capsules because the app's controls are. That is the one place glass is allowed: it matches the product, it is not decoration.
6. Write the fact. If a sentence works as a slogan, it probably needs rewriting.
