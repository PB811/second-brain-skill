---
title: "<Flow name> Flow"
tags: [flow]
substrate: cbm
updated: <YYYY-MM-DD>
---
# <Flow name> Flow

> One-line summary: what goes in, what comes out.

**Trigger:** <queue / HTTP route / CLI>
**Entrypoint:** `qualified.name` (`file:line`)
**Output:** <where the result goes>

## Diagram
```mermaid
flowchart TD
  A[Input] --> B{Decision}
  B -->|case| C[Step]
```

## Steps
| # | Step | Code (`qualified_name`) | Notes |
| --- | --- | --- | --- |
| 1 |  |  |  |

## Decision points
- **<a branch>:** condition → route. See [[decisions/...]].

## Related
- [[architecture/overview]]
