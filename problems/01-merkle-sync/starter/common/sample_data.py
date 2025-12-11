"""
Sample Data for Testing - PROVIDED CODE

Pre-computed Merkle trees from the MCP Python SDK repository.
Use these for testing your sync implementation without needing
to clone the actual repository.

The trees represent:
- TREE_V1: Initial state of the repository
- TREE_V2: State after some simulated changes (modified, added, deleted files)
"""

import json
from pathlib import Path

# Handle both relative and absolute imports
try:
    from .merkle_tree import MerkleTree, ChangeSet, tree_hash
except ImportError:
    from merkle_tree import MerkleTree, ChangeSet, tree_hash

# Load the real tree from JSON (generated from MCP Python SDK)
_DATA_DIR = Path(__file__).parent
_TREE_FILE = _DATA_DIR / "mcp_sdk_tree.json"


def _load_base_tree() -> MerkleTree:
    """Load the base tree from JSON file."""
    if _TREE_FILE.exists():
        with open(_TREE_FILE) as f:
            return json.load(f)
    else:
        # Fallback minimal tree for testing without the JSON file
        return {
            "src/mcp/__init__.py": "a" * 64,
            "src/mcp/server/__init__.py": "b" * 64,
            "src/mcp/client/__init__.py": "c" * 64,
            "tests/conftest.py": "d" * 64,
            "README.md": "e" * 64,
            "pyproject.toml": "f" * 64,
        }


# V1: Base state (real MCP SDK tree or fallback)
TREE_V1: MerkleTree = _load_base_tree()

# V2: Simulated changes from V1
# - Modified: README.md, src/mcp/__init__.py (hash changed)
# - Added: src/mcp/new_feature.py, docs/sync_protocol.md
# - Deleted: RELEASE.md (if exists)
TREE_V2: MerkleTree = TREE_V1.copy()

# Simulate modifications (change hashes)
if "README.md" in TREE_V2:
    TREE_V2["README.md"] = "modified_" + "0" * 55  # New hash
if "src/mcp/__init__.py" in TREE_V2:
    TREE_V2["src/mcp/__init__.py"] = "modified_" + "1" * 55

# Simulate additions
TREE_V2["src/mcp/new_feature.py"] = "newfile_" + "a" * 56
TREE_V2["docs/sync_protocol.md"] = "newfile_" + "b" * 56

# Simulate deletion
if "RELEASE.md" in TREE_V2:
    del TREE_V2["RELEASE.md"]


def get_tree_v1() -> MerkleTree:
    """Get the initial (v1) tree state."""
    return TREE_V1.copy()


def get_tree_v2() -> MerkleTree:
    """Get the updated (v2) tree state with changes."""
    return TREE_V2.copy()


def get_expected_changes() -> ChangeSet:
    """
    Get the expected changes from v1 to v2.

    Returns:
        ChangeSet with the known differences between v1 and v2
    """
    modified = []
    added = []
    deleted = []

    v1_files = set(TREE_V1.keys())
    v2_files = set(TREE_V2.keys())

    # Find modified (in both, hash changed)
    for f in v1_files & v2_files:
        if TREE_V1[f] != TREE_V2[f]:
            modified.append(f)

    # Find added (only in v2)
    added = list(v2_files - v1_files)

    # Find deleted (only in v1)
    deleted = list(v1_files - v2_files)

    return ChangeSet(
        modified=sorted(modified),
        added=sorted(added),
        deleted=sorted(deleted)
    )


def get_tree_stats() -> dict:
    """Get statistics about the sample trees."""
    return {
        "v1_file_count": len(TREE_V1),
        "v2_file_count": len(TREE_V2),
        "v1_tree_hash": tree_hash(TREE_V1),
        "v2_tree_hash": tree_hash(TREE_V2),
        "expected_changes": get_expected_changes().total_changes,
    }


# Quick verification when module loads
if __name__ == "__main__":
    stats = get_tree_stats()
    print(f"Tree V1: {stats['v1_file_count']} files, hash={stats['v1_tree_hash'][:16]}...")
    print(f"Tree V2: {stats['v2_file_count']} files, hash={stats['v2_tree_hash'][:16]}...")

    changes = get_expected_changes()
    print(f"\nExpected changes from V1 → V2:")
    print(f"  Modified: {len(changes.modified)} files")
    print(f"  Added: {len(changes.added)} files")
    print(f"  Deleted: {len(changes.deleted)} files")
