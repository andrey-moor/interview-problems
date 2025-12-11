# API Design Document

**TODO: Document your API design here before implementing.**

## Overview

Describe your sync protocol at a high level. What's the flow?

## Endpoints

### GET /health

Health check for Kubernetes probes.

**Response:**
```json
{
  "status": "healthy",
  "tree_file_count": 416,
  "tree_hash": "abc123..."
}
```

### GET /tree

Get the full Merkle tree.

**Response:**
```json
{
  "tree": {"file/path": "hash", ...},
  "tree_hash": "abc123...",
  "file_count": 416
}
```

---

## TODO: Add your additional endpoints below

Consider:
- How does client check if it needs to sync? (without downloading full tree)
- How does client get only what changed?
- What data does the client send vs. what does it receive?

### Example: GET /tree/hash

_Describe purpose..._

**Response:**
```json
{
  ...
}
```

### Example: POST /tree/diff

_Describe purpose..._

**Request:**
```json
{
  ...
}
```

**Response:**
```json
{
  ...
}
```

---

## Sync Flow

Describe the step-by-step flow:

1. Client starts with no local tree
2. Client calls GET /tree to get initial state
3. ...
4. ...

## Edge Cases

- What if client has never synced before?
- What if network fails mid-sync?
- What if tree is very large (1M files)?

## Design Decisions

Document any important decisions and why you made them:

- Why did you choose X over Y?
- What tradeoffs did you consider?
