"""Build /bible-characters/ from the app's own Threads content.

The page must not be edited by hand: it is generated so it cannot drift from
what ships in the app. Add or change a life in CanonStories.json, run this,
commit the result.

    python3 scripts/build-bible-characters.py ../Cardinal-Bible-Companion-

The single argument is a checkout of the app repo. Every book id used by a
beat must be in BOOK below, and the script fails loudly if one is not, rather
than rendering "book7" onto a live page.
"""

import json, html, pathlib, sys

APP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "../Cardinal-Bible-Companion-")
SRC = str(APP / "Cardinal/Resources/CanonStories.json")
OUT = str(pathlib.Path(__file__).resolve().parent.parent / "bible-characters/index.html")
d = json.load(open(SRC, encoding="utf-8"))

BOOK = {1:"Genesis",2:"Exodus",6:"Joshua",7:"Judges",8:"Ruth",9:"1 Samuel",10:"2 Samuel",
        11:"1 Kings",16:"Nehemiah",17:"Esther",18:"Job",19:"Psalms",21:"Ecclesiastes",
        24:"Jeremiah",27:"Daniel",28:"Hosea",32:"Jonah",40:"Matthew",42:"Luke",43:"John",
        44:"Acts",47:"2 Corinthians",48:"Galatians",50:"Philippians",58:"Hebrews"}
missing = {b["anchor"]["bookId"] for s in d["stories"] for b in s["beats"]} - set(BOOK)
assert not missing, f"unmapped book ids: {missing}"

themes = {t["id"]: t for t in d["themes"]}
stories = d["stories"]

def esc(s):
    return (html.escape(s, quote=False)
            .replace("'", "&rsquo;").replace('"', "&ldquo;", 1))

def plain(s):
    return html.escape(s, quote=False).replace("'", "&rsquo;")

def books_for(s):
    seen = []
    for b in s["beats"]:
        n = BOOK[b["anchor"]["bookId"]]
        if n not in seen:
            seen.append(n)
    return seen

# ---- theme index: who sits under each -------------------------------------
theme_blocks = []
for tid, t in themes.items():
    under = [s for s in stories if tid in s["themes"]]
    links = ", ".join(f'<a href="#{s["id"]}">{plain(s["character"])}</a>' for s in under)
    theme_blocks.append(
        f'      <h3 id="t-{tid}">{plain(t["name"])}</h3>\n'
        f'      <p class="blurb">{plain(t["blurb"])}</p>\n'
        f'      <p>{links}.</p>')

# ---- the twenty-four -------------------------------------------------------
life_blocks = []
for s in sorted(stories, key=lambda s: s["character"]):
    bks = ", ".join(books_for(s))
    tnames = ", ".join(themes[t]["name"] for t in s["themes"])
    life_blocks.append(
        f'        <div class="life" id="{s["id"]}">\n'
        f'          <h3>{plain(s["character"])}</h3>\n'
        f'          <p class="arc">{plain(s["theme"])}</p>\n'
        f'          <p class="meta">{plain(s["era"])} &middot; {bks} &middot; {tnames}</p>\n'
        f'          <p>{plain(s["summary"])}</p>\n'
        f'        </div>')

# ---- structured data -------------------------------------------------------
item_list = {
  "@type": "ItemList",
  "name": "Twenty-four lives of Scripture, sorted by what they were facing",
  "numberOfItems": len(stories),
  "itemListOrder": "https://schema.org/ItemListUnordered",
  "itemListElement": [
    {"@type": "ListItem", "position": i + 1,
     "name": f'{s["character"]}: {s["theme"]}',
     "description": f'{s["summary"]} {s["era"]}. Read in {", ".join(books_for(s))}. '
                    f'Themes: {", ".join(themes[t]["name"] for t in s["themes"])}.',
     "url": f'https://cardinalbible.app/bible-characters/#{s["id"]}'}
    for i, s in enumerate(sorted(stories, key=lambda s: s["character"]))]}

def under(tid):
    return ", ".join(s["character"] for s in stories if tid in s["themes"])

faq = {"@type": "FAQPage", "mainEntity": [
  {"@type": "Question", "name": "Which people in the Bible struggled with fear?",
   "acceptedAnswer": {"@type": "Answer", "text":
     f'{under("fear")}. Each is told as the handful of moments that made the life, '
     'and each moment carries the verses it rests on.'}},
  {"@type": "Question", "name": "Which people in the Bible went through grief?",
   "acceptedAnswer": {"@type": "Answer", "text":
     f'{under("grief")}. Grief here means when something does not come back, rather '
     'than a passing sadness.'}},
  {"@type": "Question", "name": "Who in the Bible had to wait a long time?",
   "acceptedAnswer": {"@type": "Answer", "text":
     f'{under("waiting")}. Waiting is the theme for the years that do not look like '
     'anything: Abraham on a promise, Hannah on a prayer, Joseph on thirteen years.'}},
  {"@type": "Question", "name": "How are these Bible characters organised?",
   "acceptedAnswer": {"@type": "Answer", "text":
     'By what each life was about rather than alphabetically or by book, under eight '
     'themes: fear, loneliness, grief, shame, waiting, purpose, belonging and mercy. '
     'Every one of the twenty-four sits under two or three of them.'}}]}

graph = {"@context": "https://schema.org", "@graph": [
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Cardinal", "item": "https://cardinalbible.app/"},
    {"@type": "ListItem", "position": 2, "name": "Bible characters",
     "item": "https://cardinalbible.app/bible-characters/"}]},
  {"@type": "Article",
   "headline": "Bible characters, sorted by what they were facing",
   "description": "Twenty-four lives of Scripture grouped under fear, loneliness, "
                  "grief, shame, waiting, purpose, belonging and mercy, with where to "
                  "read each one.",
   "url": "https://cardinalbible.app/bible-characters/",
   "mainEntityOfPage": "https://cardinalbible.app/bible-characters/",
   "image": "https://cardinalbible.app/img/thread-flyover.webp",
   "author": {"@type": "Organization", "name": "Cardinal", "url": "https://cardinalbible.app/"},
   "publisher": {"@type": "Organization", "name": "Cardinal", "url": "https://cardinalbible.app/"},
   "inLanguage": "en", "isAccessibleForFree": True},
  item_list, faq]}

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Bible Characters, Sorted by What They Were Facing &middot; Cardinal</title>
  <meta name="description" content="Twenty-four lives of Scripture grouped by fear, loneliness, grief, shame, waiting, purpose, belonging and mercy. Who in the Bible faced what you are facing, and where to read it." />
  <link rel="canonical" href="https://cardinalbible.app/bible-characters/" />
  <meta name="theme-color" content="#FAF7F2" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />

  <meta property="og:title" content="Bible Characters, Sorted by What They Were Facing" />
  <meta property="og:description" content="Twenty-four lives of Scripture, grouped by what each one was about rather than by name." />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://cardinalbible.app/bible-characters/" />
  <meta property="og:image" content="https://cardinalbible.app/img/og.png" />
  <meta property="og:site_name" content="Cardinal" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Bible Characters, Sorted by What They Were Facing" />
  <meta name="twitter:image" content="https://cardinalbible.app/img/og.png" />

  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="stylesheet" href="/css/pages.css" />
  <style>
    /* Twenty-four entries of the same shape. A typographic block rather than a
       card: a border and a fill around each would make this page a grid of
       boxes, and the list is the content. */
    .lives {{ display: grid; gap: var(--s-6); margin: var(--s-6) 0 var(--s-7); }}
    .lives .life {{ padding-top: 0; }}
    .life {{ max-width: 68ch; }}
    .life h3 {{ margin: 0 0 var(--s-1); scroll-margin-top: var(--s-5); }}
    .life .arc {{
      font-family: var(--font-display);
      font-style: italic; font-size: 1.08rem;
      color: var(--ink-2); margin: 0 0 var(--s-2);
    }}
    .life .meta {{
      font-family: var(--font-ui);
      font-size: 13.5px; color: var(--muted);
      margin: 0 0 var(--s-2); line-height: 1.5;
    }}
    .life p:last-child {{ margin-bottom: 0; }}
    .blurb {{ color: var(--ink-2); font-style: italic; margin-bottom: var(--s-2); }}
    .themes h3 {{ scroll-margin-top: var(--s-5); }}
  </style>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<div class="wrap">
  <header class="top">
    <a class="brand" href="/">Cardinal</a>
    <a class="btn btn-primary" href="https://apps.apple.com/app/id6758185643">
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
      Download
    </a>
  </header>

  <main id="main" tabindex="-1">
    <nav class="crumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Cardinal</a></li>
        <li><span aria-current="page">Bible characters</span></li>
      </ol>
    </nav>

    <h1>Bible characters, sorted by <em>what they were facing.</em></h1>
    <p class="lede">Most lists of Bible characters are alphabetical, or by book, or by how important the person was. This one is sorted by what the life was actually about, because that is usually what sends someone looking. Twenty-four of them, with where to read each.</p>
    <p class="byline">Written by the person who builds Cardinal. Every reference is checked against the Bible text itself.</p>

    <article>
    <section class="themes" aria-labelledby="themes-h">
      <h2 id="themes-h">Find one by what you are carrying</h2>
      <p>Eight themes, and every life sits under two or three of them. A person who waited was usually also afraid.</p>

{chr(10).join(theme_blocks)}
    </section>

    <section aria-labelledby="lives-h">
      <h2 id="lives-h">The twenty-four lives</h2>
      <p>Each line is the whole arc in one sentence, with the period it traditionally sits in and the books to read it in. Dates before the monarchy are traditional rather than settled.</p>

      <div class="lives">
{chr(10).join(life_blocks)}
      </div>
    </section>

    <section aria-labelledby="how-h">
      <h2 id="how-h">Why sort them this way</h2>
      <p>Somebody looking up Esther rarely wants a biography. They want the part where she has to walk into a room that might kill her, because they have a version of that room in front of them on Tuesday. Sorting by name assumes you already know which name you need, which is exactly what you do not know when you are in the middle of something.</p>
      <p>So the arc comes first and the person comes second. &ldquo;The room you are afraid to walk into&rdquo; leads to Esther. &ldquo;Burned out under a tree&rdquo; leads to Elijah. &ldquo;Four days too late&rdquo; leads to Martha, who is standing outside a tomb.</p>

      <div class="note">
        <h3>This is Threads in Cardinal</h3>
        <p>In the app each of these is a flyover: the life told as a handful of moments, plotted across a strip of the whole Bible so you can see how far apart they really fall. Abraham&rsquo;s last moment is in Hebrews, written some two thousand years after the rest of him, and the strip shows that distance rather than tidying it away.</p>
        <p>A hundred and forty moments across the twenty-four. Every one carries the verses it rests on, which open into the reader. It is free, it needs no account, and it works with no connection.</p>
      </div>
    </section>

    </article>

    <section class="cta" aria-labelledby="cta-h">
      <h2 id="cta-h">Read them in the app.</h2>
      <p>Cardinal is free to download and free to use, with no account and no sign-in. Threads is free too, and so is the Bible it sends you to.</p>
      <p><a class="btn btn-primary" href="https://apps.apple.com/app/id6758185643">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
        Download on the App Store
      </a></p>
      <p class="fine">iPhone, iPad and Apple Watch. Requires iOS 17 or later.</p>
    </section>

    <nav class="next" aria-labelledby="next-h">
      <h2 id="next-h">Read next</h2>
      <ul>
        <li><a href="/quiet-time/"><strong>How to start a daily quiet time</strong><span>A method in six steps that works with any Bible, on paper or not.</span></a></li>
        <li><a href="/bible-app-no-ads/"><strong>A Bible app with no ads, no account and no feed</strong><span>What Cardinal leaves out on purpose, and what stays free.</span></a></li>
        <li><a href="/offline-bible-app/"><strong>A Bible app that really works offline</strong><span>Which translations live on your phone, and the four that never can.</span></a></li>
      </ul>
    </nav>
  </main>

  <footer class="site">
    <nav class="foot-grid" aria-label="Footer">
      <div>
        <h2>Cardinal</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/#read">Read</a></li>
          <li><a href="/#ask">Ask</a></li>
          <li><a href="/#quiet-time">Reflect</a></li>
          <li><a href="/#memorize">Memorize</a></li>
          <li><a href="/#threads">Threads</a></li>
          <li><a href="/#journeys">Journeys</a></li>
          <li><a href="/#pricing">What&rsquo;s free</a></li>
        </ul>
      </div>
      <div>
        <h2>Articles</h2>
        <ul>
          <li><a href="/offline-bible-app/">Offline reading</a></li>
          <li><a href="/bible-app-no-ads/">No ads, no account</a></li>
          <li><a href="/quiet-time/">Quiet time guide</a></li>
          <li><a href="/bible-characters/">Bible characters</a></li>
        </ul>
      </div>
      <div>
        <h2>Help</h2>
        <ul>
          <li><a href="/support.html">Support</a></li>
          <li><a href="https://apps.apple.com/app/id6758185643">App Store</a></li>
        </ul>
      </div>
      <div>
        <h2>Legal</h2>
        <ul>
          <li><a href="/privacy-policy.html">Privacy policy</a></li>
          <li><a href="/terms-of-use.html">Terms of use</a></li>
        </ul>
      </div>
    </nav>
    <div class="foot-base">
      <div>&copy; <span id="year">2026</span> Cardinal</div>
      <div>A Bible app for iPhone, iPad and Apple Watch.</div>
    </div>
  </footer>
</div>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>

<script type="application/ld+json">
{json.dumps(graph, indent=2, ensure_ascii=False)}
</script>

</body>
</html>
'''

open(OUT, "w", encoding="utf-8").write(PAGE)
print("wrote", OUT, len(PAGE), "chars")
