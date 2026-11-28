# MntWatch

Watches host folders and bridges file changes into Windows Subsystem for Linux distros. The binary is installed and updated with [bin](https://github.com/marcosnils/bin), which Autark ships as a built-in tool, so nothing is installed globally.

## What it does

- **Start** reads the folder list, groups the folders by the distros selected next to them, and runs one `MntWatch.exe --run <folder>... --distro <name>` per distro.
- **Stop** kills that process tree, so every watcher the app started stops with it. MntWatch has no graceful shutdown command.
- **Update** re-runs the setup step, which fetches the latest release with `bin install --force`.
- **Update binary** runs `bin update mntwatch` directly, the same command the built-in tools list offers for a bin-managed binary.

`All` follows the distros `wsl.exe -l -q` reports at start, so a distro installed later needs an app restart. A folder without a selected distro is skipped, and a folder that no longer exists is reported and skipped.

## Requirements

- Windows Subsystem for Linux with at least one distro installed.
- The `bin` built-in tool. Install it once from **Built-in tools → bin.exe → Install**; the MntWatch setup step fails without it.

## Settings

| Setting | Env | Default |
| --- | --- | --- |
| Folders | `AUTARK_MNTWATCH_FOLDERS` | empty |

The folders setting is a list. Every entry holds a host path and the distros it is bridged into; the selection is either `all` or one or more distro names. The list reaches the launcher as JSON in `AUTARK_MNTWATCH_FOLDERS`, so no folder path appears on a command line.

## Files

| Path | Content |
| --- | --- |
| `<root>/bin/mntwatch.exe` | Binary installed by bin |
| `<root>/runtime/bin-config` | bin configuration shared by the host and the app |

MntWatch itself keeps no configuration file; the folder list lives in this app's `settings.json`.

## Limits

- The recipe starts the watchers, not the MntWatch tray. Console mode with `--run` is what a managed app can stop reliably.
- Only the folders and distro selection are exposed as settings. Other MntWatch flags stay available from the Autark terminal.

## License

MntWatch is MIT-licensed. The manifest in this folder is MIT-licensed too.
