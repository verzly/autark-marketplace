# Hindsight

Windows x86_64, Docker-free Hindsight API using Python 3.12, ONNX embeddings, FlashRank and embedded PostgreSQL/pgvector via pg0. No CUDA or PyTorch is required by this recipe. The embedded database is intended for local development, not a production deployment.

## Setup

1. Install Hindsight in Autark. Autark installs app-local Python and uv, creates `venv`, and installs Hindsight API Slim 1.3.0, FlashRank 0.2.10, pg0-embedded 0.17.0 and python-dotenv >=1.2.0.
2. Start an OpenAI-compatible LLM server separately, for example Unsloth at `http://127.0.0.1:8888/v1`.
3. Set **LLM base URL** and **LLM model ID** in Hindsight's Autark settings. The default model ID, `gpt-oss-20b`, must match the model actually served.
4. Create `<Autark root>/apps/hindsight/llm-api-key.txt` containing only the LLM API key, encoded as UTF-8. Alternatively, type the full path to an existing key file into **LLM API key file**. Do not paste the key into Autark settings. If your local endpoint ignores authentication, use a nonempty placeholder such as `local`.
5. Start Hindsight. The default API address is `http://127.0.0.1:8890`; **Open** shows the API documentation at `/docs`.

The first start downloads embedding and reranker models and initializes PostgreSQL. Allow extra time and disk space. An LLM connection is required for memory operations; a running API alone does not establish that the LLM works.

The API binds only to `127.0.0.1`. This recipe does not enable API authentication. Do not expose it through a public proxy or port forward. The LLM key authenticates Hindsight to the LLM, not clients to Hindsight. Memory content is sent to the configured LLM endpoint.

## Configuration

Use Hindsight's app settings in Autark, then restart Hindsight to apply changes. Autark passes the selected values as child-process environment variables at launch; no `.env` file is needed or loaded. `PYTHON_DOTENV_DISABLED=1` prevents a discovered `.env` from replacing the selected endpoint, key or other settings.

Use **Test** beside LLM base URL to check endpoint reachability and **Check** beside model ID to confirm the model is listed.

The settings expose every Hindsight value supplied by this recipe: API port, database URL, LLM provider/base URL/model/key-file path/concurrency/timeout/retries/global and per-operation (retain, consolidation, reflect) reasoning effort/output language, retain timeout, embedding provider/ONNX model/dimensions, and reranker provider/FlashRank cache folder. Defaults remain OpenAI-compatible LLM, one concurrent request, ONNX `intfloat/multilingual-e5-small` with 384 dimensions, FlashRank and `pg0://hindsight`. This is not a settings editor for every option supported by upstream Hindsight.

The installed dependencies support the default providers. Selecting another provider may require additional packages and configuration. Settings are not secret storage: keep the LLM key in its separate file, and do not put credentials in the database URL. Selecting another database URL does not migrate existing data.

Existing installations must run **Update** once to ensure python-dotenv supports the disable flag. The file picker for **LLM API key file** needs an Autark build that accepts the `file` setting kind; older builds reject the manifest. The loopback bind address and app-local pg0/Hugging Face/uv infrastructure paths remain fixed by the recipe.

## Files and updates

By default, all recipe-managed runtime files stay under `<Autark root>/apps/hindsight`:

- `venv`: Python packages.
- `pg0`: database files, instance metadata and extracted PostgreSQL binaries.
- `cache`: Hugging Face, FlashRank and uv caches.
- `llm-api-key.txt`: default secret file; protect it with appropriate filesystem permissions.

An explicitly selected external key file is read only. A custom database URL or FlashRank cache folder changes where those files are stored. The recipe does not edit OpenCode configuration, global environment variables or existing Hindsight installations. It does not import data from `~/.pg0` or `~/.hindsight`.

Stop Hindsight before backing up `pg0`. Keep a separate copy of the key file. Removing the app folder deletes its database and local secrets. Back up before updating; package pins do not freeze every transitive dependency.

Embeddings use `intfloat/multilingual-e5-small` with 384 dimensions. Changing the embedding model for existing data requires re-embedding; matching dimensions alone is not sufficient.

## OpenCode

Keep the existing Hindsight plugin and configure its documented self-hosted API URL as `http://127.0.0.1:8890` (or the chosen port). The plugin needs the Hindsight API address, not the LLM address or the LLM key. Preserve the rest of your configuration.

For a client inside WSL, verify that it can reach the Windows loopback API. Connectivity depends on WSL networking; this recipe does not change it or widen the API bind address.

The optional Hindsight Control Plane is not installed. Its usual port, `9999`, is separate from the API port.

## Upstream references

- [Installation](https://hindsight.vectorize.io/developer/installation)
- [Configuration](https://hindsight.vectorize.io/developer/configuration)
- [Hindsight v1.3.0](https://github.com/vectorize-io/hindsight/tree/v1.3.0)
- [pg0 runtime paths](https://github.com/vectorize-io/pg0)
## Shared pg0 binaries

The embedded PostgreSQL binaries stay in this app by default (`<app>/pg0/installation`). Sharing Autark's copy (`<root>/runtime/pg0/installation`) is opt-in through the migration buttons, because pg0 extracts the payload without a cross-process lock: two apps starting at the same time against an empty shared folder could publish a partial installation. The migration copies the folder while the app is stopped. Each app always keeps its own databases under `<app>/pg0`.

Existing installs that still hold their own copy can switch with the **Move to Autark** button on the app settings page. Autark stops the app, backs up the folder under `<root>/backups/pg0/`, copies it to the new place and records the setting. **Move into the app** does the same in reverse. The old copy is never deleted automatically.
## Using Autark's pg0 executable

When Autark has pg0 installed as a built-in tool (`<root>/runtime/mise-data/shims/pg0.exe`), the launch command points `PG0_EXECUTABLE` at it. The bundled copy inside this app is then unused. Without that file the app keeps using its own bundled `pg0.exe`, so nothing breaks.

Recipe `2026.11.8` declares this host-executable use with `requirements.pg0: true`. Autark blocks removal of its pg0 while Hindsight is installed, even when stopped, and shows Hindsight in the blocking-app list. This protection is independent of the PostgreSQL binaries folder: choosing an app-local payload does not mean the app uses its bundled executable. Refresh the marketplace to select the newer stable recipe; pinned previews retain their own recipe declaration.

## Knowledge banks

Hindsight 1.3.0 ships knowledge banks: persistent, searchable reference collections separate from a memory bank. They are enabled by default. Autark defaults `HINDSIGHT_API_KB_EMBEDDINGS_PROVIDER` to `text`, which reuses this app's ONNX embeddings, so documents and markdown work without extra packages or an API key.

- `local` embeddings (EmbeddingGemma, multimodal) need the torch/sentence-transformers stack, which this recipe does not install.
- `openai`, `gemini`, `voyage` and `cohere` need their own provider key.
- Knowledge banks are used by **reflect**, not by memory recall or the coding agent's automatic session recall. Ask a reflect question, or search the bank directly.
- Create and fill banks in the **Hindsight Control Plane** app (a separate marketplace app; point its API URL at this app's port) or through the Hindsight API. Then link them under a memory bank's Bank Configuration. Re-uploading with the same `document_id` replaces the document; it is not model training and does not rewrite content.
- With the `openai` (or `gemini`, `voyage`, `cohere`) provider, set the knowledge bank embeddings base URL and key file settings; they map to `HINDSIGHT_API_KB_EMBEDDINGS_BASE_URL` and `HINDSIGHT_API_KB_EMBEDDINGS_API_KEY` at launch. `text` needs neither.
- The recipe installs no `hindsight` CLI entry point, so the upstream `hindsight bank set-config` command is not available here; use the dashboard or the API instead.

Recipe `2026.11.9` adds the knowledge bank settings.

## Reflect and mental model tuning

Local reasoning models routinely exceed the upstream 300 second reflect limit. The recipe exposes these settings (defaults are a starting point, not a requirement):

| Setting | Default | Effect |
| --- | --- | --- |
| Reflect wall-clock limit | 1800 s | Total time for one reflect or mental model refresh; `0` disables the limit |
| Reflect LLM timeout | 300 s | One LLM call inside reflect |
| Reflect context budget | 24000 tokens | Accumulated context across iterations; keep it below the served model's window |
| Reflect maximum iterations | 10 | Agent iterations per reflect |
| Mental model refresh LLM timeout | 600 s | One refresh LLM call |
| Mental model refresh reasoning effort | low | Only sent when the provider supports it |
| Mental model refresh concurrency | 1 | Parallel refresh calls; keep 1 for one local server |
| Mental model refresh retries | 2 | Retries per refresh call |

If a refresh stops with `OutputTooLongError`, no explicit `HINDSIGHT_API_REFLECT_MAX_COMPLETION_TOKENS` is set by this recipe; the model server's own output and context limits still apply. Recipe `2026.11.10` adds these settings.
