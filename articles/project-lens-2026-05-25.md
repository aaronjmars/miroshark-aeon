# You Can Build an Integration, or You Can Speak a Protocol

In March 2008, four people who were building the early embeddable web — Cal Henderson at Flickr, Leah Culver and Mike Malone at the social app Pownce, and Richard Crowley — wrote down a small specification to solve an annoying problem. The web was filling up with things worth embedding: photos, the new thing called YouTube videos, audio players. But every site that wanted to show one of those things inside its own pages had to hand-write the embed code for every source it supported. Paste a Flickr link into your blog and nothing happened. Someone had to teach the blog about Flickr, and Vimeo, and SlideShare, one integration at a time.

Their fix was a protocol called oEmbed, version 1.0, published on March 21, 2008. It is still, eighteen years later, the quiet machinery behind almost every time you paste a link somewhere and it blooms into a card or a video player. It is worth understanding, because the design decision at its center keeps getting rediscovered — and a simulation tool merged its own implementation of it this week.

## The inversion hiding in a link tag

Here is what oEmbed actually does, in plain terms. A *provider* — the site that owns the content — leaves a note in the HTML head of its pages. The note is a `<link>` tag that says, in effect, "if you want to embed this, don't scrape me, just ask here." The spec is precise about the form: `<link rel="alternate" type="application/json+oembed" href="...">`, with a sibling tag for XML.

A *consumer* — the site that wants to show the content — fetches the page, finds that note, and makes a plain HTTP GET to the address it points to. Back comes a small JSON object. If the type is `rich` — the catch-all the spec defines for "rich HTML content that does not fall under one of the other categories" — the object contains the exact `html` to drop in, plus a `width` and `height`.

The thing to notice is *who does the work*. The consumer asks; the provider answers. The platform displaying your content writes the fetching, parsing, and rendering code. You, the source, only have to leave the note and be ready to answer. This is why pasting a link into WordPress just works: since version 4.4 in December 2015, every WordPress site is itself an oEmbed provider, exposing an endpoint at `/wp-json/oembed/1.0/embed`, and every WordPress site is a consumer that knows how to ask. Notion, Ghost, and Substack read the same notes. None of them coordinated with each other. They all just speak the protocol.

## MiroShark added the note this week

MiroShark is a tool for running multi-agent simulations — "simulate anything, for \$1 and less than 10 minutes," in its own description. Each finished simulation already had a public share page and an embeddable card. What it did not have was a way for the writing platforms — the places people actually paste links — to display that card automatically. Pasting a MiroShark link into Substack gave you a bare URL.

On May 25 it merged PR #107, an oEmbed provider. The change is small and almost entirely the absence of new machinery. It adds one root-mounted endpoint, `GET /oembed?url=&format=`, and injects the two discovery `<link>` tags into the head of each published simulation's share page. That is the whole interface. Paste a published MiroShark simulation into Notion, Ghost, Substack, or WordPress now, and the platform finds the note, asks the endpoint, and unfurls a card on its own.

## The part that isn't obvious

Two details make this more than a feature checkbox.

The first is what oEmbed replaces. MiroShark, like most sites, already had Open Graph meta tags — the `og:image` and `og:title` that produce link previews. But Open Graph is *passive*: it hands over a picture and a title and hopes the other platform renders them tastefully. oEmbed is an *active handshake* — the consumer requests, and the provider returns the exact embeddable HTML it wants used. That is the difference between leaving a photo on the table and being asked, specifically, "how should I show this?" and getting to answer.

The second is that the new endpoint builds nothing new to show. Its `rich`-type response is assembled from surfaces MiroShark already shipped: the existing `share-card.png` as the thumbnail, and the existing `/embed/<id>` iframe as the `html`. The implementation — `oembed_service.py` — is pure standard library, regular expressions and `urllib` and `ElementTree`, with 18 offline tests and zero new dependencies. It is a protocol adapter bolted onto renderers that already existed, not a fifth way to draw the same chart. It registers as the project's 21st distinct output surface while adding almost no surface to maintain.

And it is careful about the one risk in answering arbitrary requests. The endpoint never dereferences the URL you hand it — a foreign domain returns a flat 404, and a private or missing simulation returns 404 too, so the provider never even confirms that a private simulation exists. It answers only for the links it owns.

## What it means to be legible instead of integrated

The standing temptation, when you want your thing to appear inside someone else's product, is to *build the integration*: get an API key, write to their plugin directory, track their version changes, maintain the connector forever. Integrations rot. Each one is a relationship you have to keep alive.

A protocol is the opposite bet. You implement it once and you are legible to everyone who already speaks it — including platforms that do not exist yet, which will ship knowing how to ask and find your note waiting. The marginal cost of the fiftieth consumer is zero, because you never had to know about the fiftieth consumer. For a project run by one person and an agent shipping daily, that asymmetry is the point: the cheapest distribution is the kind where someone else's software does the rendering, and all you had to do was be legible to it.

The four people who wrote oEmbed in 2008 understood this. Eighteen years later it is still the smarter half of the build-versus-speak choice — and still the half most software skips.

---
*Sources: [oEmbed specification](https://oembed.com/), [Leah Culver — Wikipedia](https://en.wikipedia.org/wiki/Leah_Culver), [WordPress 4.4 oEmbed — WP Tavern](https://wptavern.com/wordpress-4-4-streamlines-content-sharing), [WordPress oEmbed — Developer Handbook](https://developer.wordpress.org/advanced-administration/wordpress/oembed/), [MiroShark PR #107](https://github.com/aaronjmars/MiroShark/pull/107)*
