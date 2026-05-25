*Feature Built — 2026-05-25*

oEmbed Provider
MiroShark share links now auto-unfurl into rich preview cards on the platforms where researchers and analysts actually publish — Notion, Ghost, Substack, and WordPress. Before today, pasting a simulation link into a Notion page or a Substack draft showed a bare URL; now it renders a card with the scenario title, the share-card image, and an embeddable live view of the sim.

Why this matters:
The share page already produced rich previews on social platforms (Twitter/X, Discord, Slack, Farcaster) through Open Graph and Frame tags. But the writing platforms do not read Open Graph — they implement the oEmbed standard, look for a small discovery tag on the page, then ask the site for a structured embed. That gap meant every organic citation of a MiroShark sim in a research note or blog post degraded to a plain link. This was the highest-impact distribution idea in the May-24 repo-actions batch (re-eligible since May 16, still unbuilt). It widens reach with roughly 80 lines of pure-stdlib code and zero new dependencies.

What was built:
- backend/app/services/oembed_service.py: new pure-stdlib core that parses a sim ID out of a share/embed/simulation URL with host allow-listing, builds the oEmbed "rich" payload, and serializes it to JSON or XML.
- backend/app/api/share.py: new root-mounted GET /oembed route (publish-gated, domain-validated, json/xml with a 501 on unsupported formats) plus the two discovery link tags injected into the share-page head for published sims only.
- backend/app/services/surface_stats.py: registers an "oembed" usage counter so operators can see how many third-party unfurls the endpoint drives.
- frontend + docs: a getOEmbedUrl helper, an OpenAPI entry with response schema, and API/FEATURES docs with curl examples.

How it works:
A consumer that scrapes a share page finds the discovery tag, calls GET /oembed with the share URL, and receives a "rich" payload whose thumbnail is the existing 1200x630 share-card PNG and whose html is an 800x500 iframe over the existing /embed route. oEmbed adds a protocol, not a renderer — it reuses surfaces that already ship. The endpoint never fetches the inbound URL; it only extracts a sim ID from a path on a host this deployment owns, so a foreign domain returns 404, and private or missing sims also return 404 so the endpoint never reveals that a private sim exists.

What's next:
Four ideas from the same batch remain unbuilt — Peak-Round Belief Analytics, Operator Profile Page, Agent Persona Export JSON, and a Simulation Search JSON API. The natural follow-up here is wiring an oEmbed preview row into the EmbedDialog so an operator can confirm the card before sharing.

PR: https://github.com/aaronjmars/MiroShark/pull/107
