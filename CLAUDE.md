# CLAUDE.md

## Project Overview

A curated, community-maintained list of integrations and tools that use the DeepSeek API. This is a documentation-only repository — no runnable code, no build system.

## Repository Structure

```
README.md          # Primary English list (source of truth)
README_cn.md       # Simplified Chinese translation
README_zh_tw.md    # Traditional Chinese translation
README_ja.md       # Japanese translation
README_es.md       # Spanish translation
docs/              # Per-integration assets (logos, screenshots, sub-READMEs)
  <tool-name>/
    README.md      # Integration-specific guide
    assets/        # Icons and images referenced from main README
```

## Contributing

When adding a new integration:

1. Add a row to the appropriate table in **all five README files** — keep translations in sync.
2. Place any logo/screenshot under `docs/<tool-name>/assets/`.
3. If the integration needs detailed setup steps, create `docs/<tool-name>/README.md` and link to it from the table.

Table format (HTML `<table>` rows):
```html
<tr>
  <td><img src="docs/<tool>/assets/logo.png" width="64" /></td>
  <td><a href="...">Tool Name</a></td>
  <td>One-sentence description.</td>
</tr>
```

## Conventions

- Keep entries in alphabetical order within each category.
- Images must be hosted in this repo (`docs/`) or at a stable external URL — no hotlinking to CI artifacts.
- Do not add entries for tools that are not publicly available or that only plan to support DeepSeek.
- Avoid editing README files other than to add/update entries; structural changes need broader discussion.
