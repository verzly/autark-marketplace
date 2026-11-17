# Autark Marketplace

This repository contains manifests for apps that Autark installs and runs. Autark is the only client.

Autark clones this repository; a merged PR reaches every user on their next manual refresh.

| App | Version | License | Source |
| --- | --- | --- | --- |
| Unsloth Studio | 2026.11.0 | AGPL-3.0 | https://github.com/unslothai/unsloth |

## Adding an app

Read [`docs/marketplace-v1.md`](https://github.com/verzly/autark/blob/master/docs/marketplace-v1.md) in the Autark repository. Copy `apps/unsloth-studio/app.json`, bump `version` on behavior changes, and keep all side effects inside the app folder.

## Requirements

Use public HTTPS sources. Do not require admin rights or global installs.

## License

The manifests are MIT-licensed. Each app keeps its own license, listed in its manifest.
