# Riser Studio

Electrical building services single-line diagrams, MSB elevations and distribution board schedules.

## Windows desktop app

[Download the latest complete Windows desktop ZIP](https://github.com/harryfiny-hash/SLD/releases/latest/download/Riser-Studio-Windows.zip).

Extract the entire ZIP into a new folder, then open **Riser-Studio.exe**. Keep all bundled files together. No browser, Node.js installation or internet connection is needed. Save and reopen independent `.riser` project files with File → Save / Open. The portable build is unsigned; Windows launch testing is not automated.

The first download becomes available after the **Build Windows desktop download** workflow succeeds. Every push to `main` builds a new complete release.

## Web app

Once Pages is enabled, the app is available at https://harryfiny-hash.github.io/SLD/.

One-time setup: Settings → Pages → Build and deployment → Source → **GitHub Actions**. Then run or rerun **Publish web app** under Actions. Subsequent pushes publish automatically.

## Included features

- Editable levels, equipment and supply connections; drag placement with labels.
- MSB sections, breakers inside the enclosure, busbar junctions and fire circuit colouring.
- Cable references and schedules, sizing profiles, metering and cable-size visibility checkbox.
- MSB elevation planning and 36/72-way distribution board schedules.
- A0/A1/A3/A4 sheets, title blocks, PDF/SVG/DXF exports and Excel exchange.
- Project save/open, undo/redo, templates, manufacturer presets and design checks.

Cable sizing, protection and board elevations require engineering verification. Published device data does not constitute approval of an assembled switchboard. CAD export is DXF; use AutoCAD to save as DWG.

## Source and builds

`dist/index.html` is the self-contained app. `desktop/` contains Electron integration and the Windows packager. `scripts/` contains checks and supporting source. The inline copy of `scripts/studio-upgrade.js` in the app must be kept in sync when editing it.

Build with Node.js 24 and Python 3:

```sh
python desktop/fetch-runtime.py build/runtime
python desktop/package-windows.py build/runtime build/Riser-Studio-Windows.zip
```

The packager verifies the pinned Electron checksum and checks the actual packaged JavaScript syntax. Third-party licence notices are bundled with the app.
