---
name: Feedback
description: Coding preferences and collaboration style Nick has expressed
type: feedback
---

**Keep queries, routes, and utils strictly separated.** `queries/` is DB-only, `routers/` is routing-only, business logic goes in `utils.py`.
**Why:** Nick explicitly wants this separation and will push back if logic leaks into the wrong layer.
**How to apply:** Never put computation in a query file or a route handler. Pure functions belong in utils.

**Hard-code constants with a named variable rather than avoiding them.** E.g. `PLAYOFF_CUTOFF = 3` with a comment about when to update, rather than trying to make it dynamic prematurely.
**Why:** Nick prefers pragmatic over over-engineered. He'll update it when the time comes.
**How to apply:** When something is "good enough for now," name it clearly and move on.

**Always use both published and running clock together for live games.** `publishedclock` for period name, status, and ProgressString; `runningclock` for clock minutes/seconds and the `Running` bool.
**Why:** The two clocks serve different purposes — runningclock ticks in real time, publishedclock has richer metadata.
**How to apply:** Never drop one for the other; merge them per game_id.

**Mock data for UI testing should be clearly marked `// TEMP:` and reverted before merging.**
**Why:** Nick is disciplined about not merging test scaffolding.
**How to apply:** Always add a comment and offer to revert before PR time.
