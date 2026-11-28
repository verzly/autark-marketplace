# Hindsight Docs Sync

Downloads documentation repositories, converts them to Markdown, and ingests them into a Hindsight knowledge bank. The CLI is a release binary installed by `bin`; it keeps a local snapshot so a failed sync can be retried without downloading again.

The repository ships no documentation. The built-in source catalogue lives in this marketplace app and is written to the app's user-data folder on install and update.

## Operations

- **Start** runs Download and Sync once, then exits. The app is a one-shot CLI, not a server.
- **Download** fetches the configured repositories and publishes a new snapshot.
- **Sync** uploads the existing snapshot. Run it again after a failed sync; already ingested documents are skipped.

## Settings

| Setting | Env | Default |
| --- | --- | --- |
| Hindsight API URL | `HINDSIGHT_URL` | `http://127.0.0.1:8890` |
| API token | `HINDSIGHT_API_KEY` | empty |
| Knowledge bank | `DOCS_SYNC_BANK` | `docs` |
| Built-in sources file | `DOCS_SYNC_BUILTIN` | `<data>/builtin-sources.json` |
| Local sources file | `DOCS_SYNC_LOCAL` | `<data>/sources.json` |
| Disabled sources | `DOCS_SYNC_DISABLE` | empty |
| Conversion workers | `DOCS_SYNC_WORKERS` | `4` |
| Documents per request | `DOCS_SYNC_BATCH_SIZE` | `2` |
| Requests per second | `DOCS_SYNC_RPS` | `4` |

`<data>` is this app's `user-data` folder.

## Source lists

The built-in list is merged with the local list by `id`; a local entry replaces the built-in one. `Disabled sources` removes ids from either list. Set **Built-in sources file** to an empty value to use local sources only, or point **Local sources file** at your own JSON list.

Local entries can use `repo`, `website` or `local` (a folder under `<data>`). Files under `<data>/custom` feed the built-in `custom` source; the rest of the catalogue is public documentation repositories.

## Files and limits

- `documents` holds the published snapshot and `manifest.json`.
- `.cache` holds Git clones and converted files; deleting it forces a fresh clone and conversion.
- The snapshot is published atomically, so a failed download keeps the previous one.
- API requests are paced at four per second by default. `429` and `5xx` responses retry with exponential backoff and jitter, honouring `Retry-After` up to 60 seconds. A failed batch retries one document at a time.
- Pruning runs only after every desired document is `ready`. Without **Replace all**, it removes only documents carrying this app's `docs-sync-v1` prefix.

## Requirements

[git](https://github.com/git-for-windows/git) and [pandoc](https://pandoc.org/) are installed with Autark's mise. Hindsight must be running with knowledge banks enabled, which is the default in the Hindsight app.

## License

The CLI is MIT-licensed. The manifest in this folder is MIT-licensed too.
