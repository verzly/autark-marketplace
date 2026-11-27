# Autark Marketplace

This repository contains manifests for apps that Autark installs and runs. Autark is the only client.

Autark clones this repository; a merged PR reaches every user on their next manual refresh.

`versions.json` caches latest GitHub release tags for apps. A daily GitHub Actions workflow refreshes it, so Autark can check for updates without querying GitHub per app.

| App | Version | License | Source |
| --- | --- | --- | --- |
| Unsloth Studio | 2026.11.2 | AGPL-3.0 | https://github.com/unslothai/unsloth |
| [Mira](apps/mira/README.md) | 2026.11.1 | Apache-2.0 | https://github.com/miracodeai/mira |
| [Hindsight](apps/hindsight/README.md) | 2026.11.8 | MIT | https://github.com/vectorize-io/hindsight |
| [Hindsight Control Plane](apps/hindsight-control-plane/README.md) | 2026.11.2 | ISC | https://github.com/vectorize-io/hindsight |
| [Hindsight Obsidian Sync](apps/hindsight-obsidian-sync/README.md) | 2026.11.1 | MIT | https://hindsight.vectorize.io |

## Adding an app

Read [`docs/marketplace-v1.md`](https://github.com/verzly/autark/blob/master/docs/marketplace-v1.md) in the Autark repository. Copy `apps/unsloth-studio/app.json`, bump `version` on behavior changes, and keep all side effects inside the app folder.

## Requirements

Use public HTTPS sources. Do not require admin rights or global installs.

## License

The manifests are MIT-licensed. Each app keeps its own license, listed in its manifest.
