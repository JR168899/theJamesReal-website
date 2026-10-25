# James Real

Luxury lifestyle brand website, with a proposed San Francisco headquarters, six lifestyle worlds, a journal, prepared recipe selections, and A1–C2 English cards.

Static output: `dist/`. No install or build is required to serve it. Use `python3 -m http.server 4173 --directory dist` locally. See `MIGRATION.md` for content provenance, original archives, database storage, domain setup, and the live-market limitation.

The content preparation tools are explicit authoring/build steps, never run by page visits or on a daily GitHub schedule:

1. `python3 tools/build_calendar.py`
2. `python3 tools/build_illustrations.py`
3. `python3 tools/render_cards.py`

The Neon synchronization tool accepts its privileged connection through hidden stdin. Credentials never belong in this repository or frontend output.
