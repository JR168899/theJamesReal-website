# theJamesReal.com migration

Target repository: https://github.com/JR168899/theJamesReal-website
Preferred host: a static host connected to this repository; `vercel.json` declares `dist`.
Domain registrar reported by owner: Squarespace. Authoritative DNS currently reports Cloudflare. Keep mail records and nameservers intact; attach the verified host's www record in that DNS zone only after a working deployment is confirmed.

## Runtime

The site is static. Prepared English lessons, recipe editions, illustrations, and SVG cards are local files under `dist/data` and `dist/assets`. Opening them does not call an LLM, GitHub API, or recipe-generation service. PNG export and device speech run in the browser. Existing remote recipe photographs retain attribution. Optional translation is disabled on recipes and English.

## Content

English: 2026-10-06 to 2026-12-31, 87 dates × 6 levels × 11 cards = 5,742 complete dated card files. Original October 11–12 course texts retained; other dates use a twelve-theme spiral curriculum and clearly labelled review stages, prepared October 24. This is not 5,742 entirely different source lessons.

Recipes: 2026-10-08 to 2026-12-31, 85 dated editions, 20 dishes per edition, drawn from the preserved 80-recipe collection. Repeated selections are labelled; no claim of twenty new recipes per day. Original quantities and methods remain. New recipes have not been kitchen-tested.

All 148 original reference content files are preserved byte-for-byte, with hashes in the migration archive. Original mixed-level lesson cards and illustrations remain.

Neon public-content branch: project `noisy-hill-90788675`, branch `br-wild-morning-b53ajkcu`. Schema `jamesreal_content`. Content exports need no database credentials in the browser. Do not commit a connection string. Do not export the separate realfamily subscriber tables.

## Markets

The page is a Google Finance directory for the existing 14 markets, without AI analysis or stale numeric quotes. On-page live quote redistribution is not enabled: Google Finance's published terms restrict commercial redistribution without permission. A licensed feed or written permission is required to show continually updated numbers within this site. All supported entries link to Google Finance; coverage and delays vary.

## Assets

Headquarters scenes are generated concepts, not a commissioned project or existing James Real building. The original full-tower image was edited for a clear sunset and then for more natural photographic materials and lighting. No claim of an architect's commission is made. Source prompt and asset paths are in the migration handoff.

## Production deployment — 2026-10-25
The owner approved moving www.thejamesreal.com from Sites to GitHub Pages. Cloudflare www CNAME now targets jr168899.github.io (DNS only). GitHub Pages uses .github/workflows/publish.yml; every push to main deploys dist/. The original Sites deployment remains a backup. Keep database credentials outside the repository.
