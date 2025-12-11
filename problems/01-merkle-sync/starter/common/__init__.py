"""Common utilities for Merkle tree sync."""

try:
    from .merkle_tree import (
        MerkleTree,
        MerkleTreeManager,
        ChangeSet,
        build_tree,
        detect_changes,
        tree_hash,
    )

    from .sample_data import (
        get_tree_v1,
        get_tree_v2,
        get_expected_changes,
        get_tree_stats,
        TREE_V1,
        TREE_V2,
    )
except ImportError:
    from merkle_tree import (
        MerkleTree,
        MerkleTreeManager,
        ChangeSet,
        build_tree,
        detect_changes,
        tree_hash,
    )

    from sample_data import (
        get_tree_v1,
        get_tree_v2,
        get_expected_changes,
        get_tree_stats,
        TREE_V1,
        TREE_V2,
    )

__all__ = [
    "MerkleTree",
    "MerkleTreeManager",
    "ChangeSet",
    "build_tree",
    "detect_changes",
    "tree_hash",
    "get_tree_v1",
    "get_tree_v2",
    "get_expected_changes",
    "get_tree_stats",
    "TREE_V1",
    "TREE_V2",
]
