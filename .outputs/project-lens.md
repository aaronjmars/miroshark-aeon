*New Article: Your OG Image Is Now Your UI*

The 1200×630 social share card used to be metadata — a PNG stuffed in a `<meta>` tag for Messenger unfurls. In 2026 it's load-bearing UI. MiroShark's Public Gallery merged today (PR #43) rides the share card PNG that merged yesterday (PR #42): one renderer, one on-disk cache, three consumption surfaces (social unfurl, embed preview, gallery thumbnail). That's why a 1,536-line gallery with zero dependencies could ship twenty-four hours after the image endpoint it rides on.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-04-23.md
