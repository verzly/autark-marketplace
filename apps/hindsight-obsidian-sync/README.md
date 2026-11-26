# Hindsight Obsidian Sync

Headless sync of an Obsidian vault into a Hindsight bank. It runs the `hindsight-obsidian-sync` CLI from `@vectorize-io/hindsight-obsidian`, so the Obsidian app is not needed.

The app installs the package into its own folder and runs it with the Node version Autark manages. No global install is required.

## What it does

- **Start** keeps `reconcile --watch` running: notes that change are retained again and deleted notes are pruned.
- **Sync vault now** runs one `reconcile` and exits, which fits a manual refresh or an external scheduler.
- The sync index lives in `~/.hindsight/obsidian/`, outside the vault, so Obsidian Sync never copies it. Deleting that file forces a full reingest.

## Settings

| Setting | Env | Default |
| --- | --- | --- |
| Vault folder | `--vault` | empty, required |
| Hindsight bank | `--bank` | `obsidian` |
| Hindsight API URL | `HINDSIGHT_API_URL` | `http://127.0.0.1:8890` |
| API token | `HINDSIGHT_API_TOKEN` | empty |
| Fact date source | `--timestamp-from` | `created` |

The token is passed in the environment, so it does not appear in the process command line. It is stored in this app's `settings.json` like every other app setting.

## Running next to the plugin

The CLI drives the same sync engine as the Obsidian plugin and produces identical document ids, scope tags and prune ownership. Keep the two configurations identical (folders, bank, vault name, document-id prefix, observation scopes, excluded tags, retain strategy, timestamp source). Each frontend keeps its own index and prunes only what that index tracks, so a mismatched folder or id scope could let one prune documents the other owns.

## Limits

This recipe exposes the flags that a managed app needs. The remaining CLI flags (`--include`, `--exclude`, `--exclude-tag`, `--retain-strategy`, `--vault-name`, `--prefix-doc-id`, `--observation-scopes`, `--index`) are not settings yet; run the CLI from the Autark terminal when you need them.

## License

The package is MIT-licensed. The manifest in this folder is MIT-licensed too.
