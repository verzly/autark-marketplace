# Mira

Self-hosted AI code review with repository indexing, vulnerability scanning, custom rules and a dashboard. The review engine and the dashboard stay on this machine; the LLM is whatever OpenAI-compatible endpoint you configure.

Upstream: [miracodeai/mira](https://github.com/miracodeai/mira) (Apache-2.0, alpha)

## What Autark installs

The recipe is native Windows only: no Docker, no WSL, no global PostgreSQL and no administrator rights.

| Part | Where it comes from |
| --- | --- |
| Python 3.12, uv, Node.js 22 | mise, scoped to this app |
| Mira source | `git clone` of the upstream default branch into `<app>/source` |
| Python packages | editable install of `.[serve]` in `<app>/venv`, plus `pg0-embedded` |
| Dashboard | built by `npm ci` + `npm run build` in `source/ui/mira` and served from `source/ui/mira/dist` |
| PostgreSQL | pg0, with the instance data under `<app>/pg0` (like Hindsight) |

Node is only used for the dashboard build. PostgreSQL binaries are extracted into `<app>/pg0/installation` by default; the **Move to Autark / Move into the app** buttons on the settings page switch that payload between this app and Autark's shared copy. The databases always stay inside this app.

## How it starts

Autark launches a small Python bootstrap in the app's venv. It:

1. points `PG0_EXECUTABLE` at Autark's pg0 shim when that file exists (otherwise the bundled pg0 binary),
2. starts the `mira` pg0 instance on the configured PostgreSQL port (pg0 falls back to a free port and the real port is used),
3. exports the instance URI as `DATABASE_URL`,
4. writes `<app>/user-data/mira.yaml` with the configured `llm.base_url` and `llm.model`,
5. reads the secret files and exports `OPENROUTER_API_KEY`, `ADMIN_PASSWORD` and the GitHub App values,
6. runs `mira serve --host 127.0.0.1 --port <Port>`.

Mira then creates its schema in the `mira` database. SQLite is not used in this configuration.

## Settings

## Source versions

Autark offers the latest release (`v0.11.1`, from `versions.json`), `main` as a preview, or a custom tag. Changing the source version requires reinstalling Mira. The recipe branch remains `main`.

| Setting | Purpose |
| --- | --- |
| Port | Dashboard and API port, default `8000` |
| PostgreSQL port | Port for the app-local instance, default `55432` |
| pg0 binaries folder | PostgreSQL payload; app-local by default, shareable through the migration buttons |
| LLM base URL | OpenAI-compatible endpoint, default OpenRouter |
| LLM model | Model used for review, indexing and security passes |
| LLM API key file | Text file with the provider key; Autark settings are not secret storage |
| Dashboard admin password file | Optional. Blank makes Mira generate a random password on first start |
| GitHub App ID / private key file / webhook secret file | Optional GitHub App integration |

Mira writes a generated admin password to `<app>/user-data/indexes/initial_admin_password` when no admin password file is set. Change the password in the dashboard and set the file to keep it stable across starts.

Secrets are read at launch and passed as environment variables. They are never written into `app.json`, `mira.yaml` or the app output.

## GitHub integration

Mira exposes the GitHub App webhook at `/github/webhook`. Fill the three GitHub settings and expose that path to GitHub, for example through a tunnel. The dashboard's GitHub sign-in uses the same GitHub App.

Without the GitHub settings the dashboard and the local review CLI still work. Local review uses the app's own terminal:

```
<app>/venv/Scripts/mira.exe review --base main
```

## Data and updates

| Path | Content |
| --- | --- |
| `<app>/pg0/instances/mira` | PostgreSQL data directory (reviews, repositories, settings) |
| `<app>/pg0/installation` | PostgreSQL binaries (or the shared copy in `<root>/runtime/pg0/installation`) |
| `<app>/user-data/indexes` | Repository indexes and the generated admin password |
| `<app>/source` | Upstream checkout |
| `<app>/venv` | Python environment |

An update re-clones the source, reinstalls the Python packages and rebuilds the dashboard. The database and `user-data` are kept. A failed install leaves them untouched. Uninstalling the app from Autark removes the launcher entry; delete the app folder to remove the database and indexes.

## pg0 dependency

The recipe declares `requirements.pg0`. While Mira is installed Autark refuses to remove its pg0 executable and lists Mira among the blocking apps, even when Mira is stopped. Mira still falls back to the bundled pg0 binary when Autark's copy is missing, so an uninstalled pg0 does not break the app, it only changes which binary is used.

## Limits

- Upstream Mira is alpha software; the recipe follows its default branch, so a new upstream release can change behaviour before this recipe is republished.
- The recipe has not been installed or started in this repository. The first real installation verifies the Vue/React dashboard build and the pg0 bootstrap on the user's machine.
- A public webhook endpoint is the user's responsibility; Autark does not create tunnels.
- The dashboard password reset, backup and restore of `<app>/pg0` and `<app>/user-data` are manual.
