# Technical Interview: Merkle Tree Sync Protocol

**Duration**: 60 minutes
**Format**: AI-assisted coding - use any AI tools you prefer (Claude, Copilot, ChatGPT, etc.)

---

## Before You Start

**We're evaluating not just your solution, but how you approach the problem.**

Take a few minutes to:
1. Read through this problem and the starter code
2. Think about your approach
3. Plan before you code

Feel free to ask clarifying questions at any time.

---

## Context

You're joining a team that builds a **code analysis platform**. The system maintains a "code graph" - a searchable index of source code entities. Graph processing is expensive and runs on **Kubernetes servers**, but clients need **fast local access**.

We track file changes using a **Merkle tree** - a data structure where each file maps to its content hash:

```python
# Merkle tree = {file_path: sha256_hash}
{
    "src/main.py": "a1b2c3d4...",
    "src/utils.py": "b2c3d4e5...",
}
```

When hashes differ, we know content changed. This enables efficient sync.

---

## Your Task

Design and implement a **sync protocol** between a Kubernetes server and Python client.

### What's Provided (`starter/` directory)

```
starter/
├── common/
│   ├── merkle_tree.py      # MerkleTreeManager - builds trees, detects changes
│   ├── sample_data.py      # Pre-computed test trees from real repo
│   └── mcp_sdk_tree.json   # Real Merkle tree (~400 files)
├── server/
│   ├── main.py             # FastAPI skeleton (some endpoints done)
│   ├── k8s/                # Kubernetes manifests
│   └── Dockerfile
├── client/
│   └── sync_client.py      # Client skeleton (methods to implement)
└── test_sync.py            # Test skeleton
```

### What You Build

1. **API Design** (`api_design.md`) - Document your endpoints
2. **Server** - Add endpoints for efficient sync
3. **Client** - Implement the sync methods
4. **Tests** - Verify it works

---

## Requirements

### Server (FastAPI + Kubernetes)
- Expose REST endpoints for Merkle tree sync
- Support efficient sync (not just full tree download every time)
- K8s manifests for deployment

### Client (Python)
Implement `MerkleSyncClient` with:
- `fetch_full_tree()` - Get the complete tree
- `is_in_sync()` - Check if local matches server (efficiently!)
- `sync()` - Sync and return what changed
- `detect_local_changes(repo_path)` - Compare filesystem to stored tree

### Tests
- At minimum: initial sync, detect changes, verify changeset

---

## Hints

1. **Read the starter code first** - `MerkleTreeManager` already handles tree building and change detection
2. **The key question**: How does the client know if it needs to sync *without* downloading the entire tree?
3. **`tree_hash()`** - There's a helper that computes a single hash of the whole tree
4. **Sample data** - Use `get_tree_v1()`, `get_tree_v2()`, and `get_expected_changes()` for testing

---

## Running the Code

```bash
# Install dependencies
pip install -r starter/server/requirements.txt
pip install -r starter/client/requirements.txt
pip install pytest httpx

# Start the server
cd starter/server
python main.py

# Run tests (in another terminal)
pytest test_sync.py -v
```

---

## Deliverables

| File | What to do |
|------|------------|
| `api_design.md` | Document your API design |
| `starter/server/main.py` | Add sync endpoints |
| `starter/client/sync_client.py` | Implement client methods |
| `test_sync.py` | Add integration tests |

---

## Time Management Suggestion

| Phase | Time |
|-------|------|
| Read & Plan | 5-10 min |
| API Design | 5-10 min |
| Server | 15-20 min |
| Client | 15-20 min |
| Tests | 5-10 min |

---

## Extension Topics (if time permits)

- How would this scale to 1M files?
- How would you handle conflicts?
- How would you add authentication?
- How would you shard across multiple pods?
