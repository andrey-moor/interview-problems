"""
Merkle Tree Sync Server - SKELETON

TODO: Implement the REST API for Merkle tree synchronization.

This server should:
1. Store a Merkle tree in memory (pre-loaded from sample data)
2. Expose endpoints for clients to sync their local trees
3. Support efficient sync (not just full tree downloads every time)

Hints:
- The sample data is pre-loaded for you
- Consider: How does a client know if it needs to sync?
- Consider: How can you send only what changed?
"""

import sys
from pathlib import Path

# Add common module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from merkle_tree import MerkleTree, ChangeSet, tree_hash
from sample_data import get_tree_v1, get_tree_v2

app = FastAPI(
    title="Merkle Tree Sync Server",
    description="Server for syncing Merkle trees between client and server",
    version="1.0.0",
)

# ============================================================================
# Server State
# ============================================================================

# The server's current Merkle tree (start with v1, can be "updated" to v2)
SERVER_TREE: MerkleTree = get_tree_v1()


# ============================================================================
# Pydantic Models for API
# ============================================================================

class HealthResponse(BaseModel):
    status: str
    tree_file_count: int
    tree_hash: str


class TreeResponse(BaseModel):
    tree: dict[str, str]
    tree_hash: str
    file_count: int


# TODO: Add more models as needed for your API design


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Kubernetes probes."""
    return HealthResponse(
        status="healthy",
        tree_file_count=len(SERVER_TREE),
        tree_hash=tree_hash(SERVER_TREE),
    )


@app.get("/tree", response_model=TreeResponse)
async def get_full_tree():
    """
    Get the complete Merkle tree.

    This is a simple but inefficient approach - consider adding
    more sophisticated endpoints for delta sync.
    """
    return TreeResponse(
        tree=SERVER_TREE,
        tree_hash=tree_hash(SERVER_TREE),
        file_count=len(SERVER_TREE),
    )


# TODO: Implement additional endpoints for efficient sync
#
# Ideas to consider:
# - GET /tree/hash - Just get the tree hash (for quick sync check)
# - POST /tree/diff - Send client's tree hash, get back changes
# - GET /tree/files?paths=... - Get specific file hashes
#
# Your API design should go in api_design.md


# ============================================================================
# Debug/Test Endpoints (for interview simulation)
# ============================================================================

@app.post("/debug/update-tree")
async def update_server_tree():
    """
    Simulate a server-side update by switching to v2 tree.

    This is for testing - in production, the tree would be updated
    by the actual code graph processing system.
    """
    global SERVER_TREE
    SERVER_TREE = get_tree_v2()
    return {
        "message": "Server tree updated to v2",
        "file_count": len(SERVER_TREE),
        "tree_hash": tree_hash(SERVER_TREE),
    }


@app.post("/debug/reset-tree")
async def reset_server_tree():
    """Reset server tree back to v1."""
    global SERVER_TREE
    SERVER_TREE = get_tree_v1()
    return {
        "message": "Server tree reset to v1",
        "file_count": len(SERVER_TREE),
        "tree_hash": tree_hash(SERVER_TREE),
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
