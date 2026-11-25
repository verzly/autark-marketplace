# Hindsight Control Plane

Web interface for a running Hindsight API. Windows x86_64, no Docker, no build step: the npm
package ships a prebuilt Next.js standalone server.

## Setup

1. Install and start the **Hindsight** app first. This interface only reads from its API.
2. Install this app in Autark. Autark installs Node 22 and the `@vectorize-io/hindsight-control-plane`
   npm package into this app's folder, with the npm cache kept there as well.
3. If Hindsight uses a non-default port, set **Hindsight API URL** to match, for example
   `http://127.0.0.1:8890`.
4. Start this app and press **Open**. The interface listens on `http://127.0.0.1:9990` by default.

## Behaviour

- Both ports are loopback only. This recipe adds no authentication in front of the interface, so do
  not expose it through a public proxy or port forward.
- The package version is pinned (`1.3.0`) to match the Hindsight API recipe. Update this app when the
  API app moves to a newer version.
- Everything stays under `<Autark root>/apps/hindsight-control-plane`: `node_modules`, the npm cache
  and the Next.js build output.
- Two processes run side by side: the Hindsight API (Python) and this interface (Node). This app does
  not start the API for you.
