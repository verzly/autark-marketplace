# Autark Marketplace

This repository contains manifests for apps that Autark installs and runs. Autark is the only client.

Autark clones this repository; a merged PR reaches every user on their next manual refresh.

`versions.json` caches the latest upstream versions so Autark can check for updates without querying each provider per app. A daily GitHub Actions workflow refreshes it.

Each app declares its source: `upstream` (GitHub `owner/repo`, latest release) by default, or an optional `version_source` such as `github:owner/repo` or `pypi:package`. Unsloth uses `pypi:unsloth` because its app version is the `unsloth` Python package version; the bundled llama.cpp prebuilt tag is not part of that number. Unsloth records it as `release_tag` in `<studio_home>/llama.cpp/UNSLOTH_PREBUILT_INFO.json`, taken from the `unslothai/llama.cpp` releases, and the app version line shows it as `... | llama.cpp b<number>`.

| App | Version | License | Source |
| --- | --- | --- | --- |
| Unsloth Studio | 2026.11.2 | AGPL-3.0 | https://github.com/unslothai/unsloth |
| [Mira](apps/mira/README.md) | 2026.11.4 | Apache-2.0 | https://github.com/miracodeai/mira |
| [Hindsight](apps/hindsight/README.md) | 2026.11.28 | MIT | https://github.com/vectorize-io/hindsight |
| [Hindsight Control Plane](apps/hindsight-control-plane/README.md) | 2026.11.2 | ISC | https://github.com/vectorize-io/hindsight |
| [Hindsight Obsidian Sync](apps/hindsight-obsidian-sync/README.md) | 2026.11.1 | MIT | https://hindsight.vectorize.io |
| [Hindsight Docs Sync](apps/hindsight-docs-sync/README.md) | 2026.11.0 | MIT | https://github.com/verzly/hindsight-docs-sync |
| [MntWatch](apps/mntwatch/README.md) | 2026.11.1 | MIT | https://github.com/BoazCohenJ/MntWatch |

## Adding an app

Read [`docs/marketplace-v1.md`](https://github.com/verzly/autark/blob/master/docs/marketplace-v1.md) in the Autark repository. Copy `apps/unsloth-studio/app.json`, bump `version` on behavior changes, and keep all side effects inside the app folder.

## Requirements

Use public HTTPS sources. Do not require admin rights or global installs.

## License

The manifests are MIT-licensed. Each app keeps its own license, listed in its manifest.
