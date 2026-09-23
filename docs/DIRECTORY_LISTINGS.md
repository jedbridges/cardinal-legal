# Getting Cardinal into the places assistants read

Compiled 2026-09-23.

## Why this and not more pages

Asked "distraction-free Bible app, no streaks", an assistant returned Cardinal's
positioning almost word for word and never named the app. It was quoting
faith.tools, where Cardinal sits at entry 97 of about 100. Asked about Cardinal
directly, assistants answer from the App Store listing and get it wrong,
confidently listing the NIV and the ESV as available translations.

So the citation surface for this category is third-party directories and
roundups. `/llms.txt` is not what is being read. Twelve of those pages were
checked; Cardinal appears on two.

## Where Cardinal already is

| Site | Standing | Worth doing |
| --- | --- | --- |
| [faith.tools](https://faith.tools/bible) | Listed, entry ~97 of ~100 | Their copy is accurate. Ask them to re-check it against 2.70.0, since the listing predates Journeys and Studies. |
| [learnofchrist.com](https://learnofchrist.com/directory/best-bible-apps) | Reviewed, position 8 of 28, rated 4.9, "an unusually coherent Apple-only Bible reader" | Already the best placement Cardinal has. Leave it. |

## Where it is absent

Checked 2026-09-23, zero occurrences of "cardinal" in the served HTML of each.

| Site | Mechanism | Account | Cost |
| --- | --- | --- | --- |
| [alternativeto.net](https://alternativeto.net/software/youversion/) | "Add Alternatives" on each competitor page. Add Cardinal as an alternative to YouVersion, Bible Gateway, Dwell and Blue Letter Bible. | Yes, free | Free |
| [christianappreviews.com](https://christianappreviews.com/submit) | Editorial review, then claim the listing | Yes | **$29 (2 weeks) or $99 (3 days)**, refunded if not approved |
| [bibleinyear.com](https://bibleinyear.com/blog/best-bible-apps) | Editorial, contact the author | No | Free |
| [theleadpastor.com](https://theleadpastor.com/tools/best-bible-apps/) | Editorial roundup, pitch the editor | No | Free, though this one reads like it takes affiliate placements |
| [warmpeach.com](https://www.warmpeach.com/blog/best-bible-apps) | Editorial, two relevant roundups | No | Free |
| [faithwall.app](https://faithwall.app/blog/best-free-bible-app-iphone) | Editorial, single author (Karol Billik) | No | Free |
| [chmeetings.com](https://www.chmeetings.com/blog/best-bible-apps/) | Editorial, church-software company blog | No | Free |
| [appstoretracker.com](https://www.appstoretracker.com/best/bible-apps) | Appears to be generated from App Store data | No | Free, may self-correct as ratings grow |
| [appshunter.io](https://appshunter.io/ios/topics/bible-study) | Generated from App Store data | No | Free |
| [mobileappdaily.com](https://www.mobileappdaily.com/products/best-bible-app) | Editorial | No | Likely paid placement |
| Bibles.com / .BIBLE Registry | American Bible Society directory, community submissions and upvotes | Probably | Free |

Do the free editorial ones and AlternativeTo first. AlternativeTo is the single
highest-value target: it was cited four times over in one answer, its pages rank
for "YouVersion alternative", and it costs nothing but an account.

Hold the two paid ones until the free ones have been tried. ChristianAppReviews
refunds if not approved, so the $29 tier is a low-risk test rather than a
gamble, but it should not be first.

## The facts any listing needs

All verified against 2.70.0 and the App Store on 2026-09-23. Keep these in sync;
a directory that publishes a wrong translation list is worse than no listing.

- App Store: `https://apps.apple.com/us/app/cardinal-bible/id6758185643`
- Website: `https://cardinalbible.app`
- Platforms: iPhone, iPad, Apple Watch. iOS 17.0 or later. No Android, no web.
- Price: free to download and to use. Cardinal Pro is $2.99/month or $19.99/year.
- Rating: 5.0 from 14 ratings. First released 2026-01-28.
- Translations: 17, of which 13 are free. 8 are bundled and work fully offline.
  The 4 Pro ones (NKJV, NASB, CSB, NLT) are publisher-licensed and stream-only.
  **Not the NIV and not the ESV.** Correct this wherever it appears.
- Interface languages: 9.
- No account and no sign-in, ever. Reading is never gated.

## Tagline, 12 words

A Bible app built for being alone with Scripture. No feed, no streaks.

## Short description, about 50 words

Cardinal is a Bible app for iPhone, iPad and Apple Watch, built for one person
alone with the text. No feed, no streaks, no badges, no account. Reading is free
and always will be. It also holds a guided quiet time, Scripture memory, audio,
word study and sermon prep.

## Long description, about 150 words

Cardinal exists because Bible apps became social platforms. It was built for
being alone with Scripture, for as long as you want to stay there, and
everything in it is judged by whether it helps you read or pulls you away.

There is no feed, no streak, no badge and no account. Reading is free and always
will be: eight translations are bundled and work fully offline, including
search, with five more free once downloaded.

Beyond reading it holds a guided quiet time of about fifteen minutes, Scripture
memory with more than fifty curated packs, Scripture read aloud by six
narrators, Greek and Hebrew word study with a tappable interlinear, a
cross-reference map, side-by-side translation comparison, and sermon prep
structured the way sermons are actually preached.

Cardinal Pro ($2.99/month) covers four publisher-licensed translations and AI
answers beyond the free monthly allowance. Every AI answer cites its verses and
is honest about uncertainty. Reading is never gated.

## What to lead with when pitching an editor

faith.tools publishes its criteria, and the common failures it names are the
things Cardinal is unusually good at. Lead with these, because they are what a
careful reviewer is checking and most submissions cannot answer them:

- **Translations are cited and licensed properly.** Publisher text is
  stream-only and never cached or indexed, which is why offline search falls
  back to a public-domain translation rather than quietly indexing licensed text.
- **The AI has guardrails.** Publisher-licensed translation text is never sent
  to the model. Answers cite their verses and say when they are uncertain. A
  test in the app's repo enforces that bundled prose quotes a public-domain
  translation verbatim rather than paraphrasing Scripture.
- **Pricing is unambiguous.** One subscription, one price, and reading is never
  behind it.
- **No account, no analytics on the reader's behaviour inside Scripture.**
- **Current Apple design**, iOS 26 Liquid Glass, with a widget and a watchOS app.
