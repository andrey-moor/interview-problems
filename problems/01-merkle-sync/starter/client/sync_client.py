"""
Merkle Tree Sync Client - SKELETON

TODO: Implement the client for syncing Merkle trees with the server.

This client should:
1. Fetch the Merkle tree from the server
2. Store it locally (in memory or file)
3. Detect if local copy is out of sync with server
4. Sync efficiently (ideally not full tree every time)
5. Detect local filesystem changes (compare with local tree)

Hints:
- Use the provided MerkleTreeManager for tree operations
- Consider: What's the minimum data needed to check if sync is required?
- Consider: How do you handle first-time sync vs. incremental sync?
"""

import sys
from pathlib import Path
from typing import Optional

# Add common module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

import httpx  # or use requests if you prefer

from merkle_tree import MerkleTree, MerkleTreeManager, ChangeSet, tree_hash


class MerkleSyncClient:
    """
    Client for syncing Merkle trees with a remote server.

    Example usage:
        client = MerkleSyncClient("http://localhost:8000")

        # Initial sync
        client.sync()

        # Check if we need to sync
        if not client.is_in_sync():
            changes = client.sync()
            print(f"Synced {changes.total_changes} changes")

        # Detect local filesystem changes
        local_changes = client.detect_local_changes("/path/to/repo")
    """

    def __init__(self, server_url: str):
        """
        Initialize the sync client.

        Args:
            server_url: Base URL of the Merkle sync server (e.g., "http://localhost:8000")
        """
        self.server_url = server_url.rstrip("/")
        self.local_tree: MerkleTree = {}
        self.local_tree_hash: str = ""
        self.manager = MerkleTreeManager()

    def fetch_full_tree(self) -> MerkleTree:
        """
        Fetch the complete Merkle tree from the server.

        Returns:
            The server's current Merkle tree

        Raises:
            httpx.HTTPError: If the request fails
        """
        # TODO: Implement this method
        #
        # Hint: Use the /tree endpoint from the server
        #
        raise NotImplementedError("TODO: Implement fetch_full_tree")

    def is_in_sync(self) -> bool:
        """
        Check if the local tree is in sync with the server.

        This should be efficient - ideally just comparing hashes,
        not downloading the entire tree.

        Returns:
            True if local tree matches server tree, False otherwise
        """
        # TODO: Implement this method
        #
        # Hint: You might want to add a /tree/hash endpoint to the server
        # that returns just the hash, not the full tree
        #
        raise NotImplementedError("TODO: Implement is_in_sync")

    def sync(self) -> ChangeSet:
        """
        Sync the local tree with the server.

        This should:
        1. Detect what changed on the server
        2. Update the local tree
        3. Return what changed

        Returns:
            ChangeSet describing what changed during sync
        """
        # TODO: Implement this method
        #
        # Consider two approaches:
        # 1. Simple: Always fetch full tree, compute diff locally
        # 2. Efficient: Ask server for diff based on our current hash
        #
        raise NotImplementedError("TODO: Implement sync")

    def detect_local_changes(self, repo_path: str) -> ChangeSet:
        """
        Detect changes between local filesystem and stored tree.

        This is useful for detecting if a client has local modifications
        that haven't been synced to the server.

        Args:
            repo_path: Path to the local repository

        Returns:
            ChangeSet describing differences between filesystem and stored tree
        """
        # TODO: Implement this method
        #
        # Hint: Use self.manager.build_merkle_tree() to scan the filesystem
        # then self.manager.detect_changes() to compare with self.local_tree
        #
        raise NotImplementedError("TODO: Implement detect_local_changes")

    def get_local_tree(self) -> MerkleTree:
        """Get the currently stored local tree."""
        return self.local_tree.copy()

    def get_local_tree_hash(self) -> str:
        """Get the hash of the local tree."""
        return self.local_tree_hash


# ============================================================================
# CLI for testing
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Merkle Tree Sync Client")
    parser.add_argument("--server", default="http://localhost:8000", help="Server URL")
    parser.add_argument("--action", choices=["sync", "check", "local"], default="sync")
    parser.add_argument("--repo", help="Local repo path (for 'local' action)")

    args = parser.parse_args()

    client = MerkleSyncClient(args.server)

    if args.action == "sync":
        print(f"Syncing with {args.server}...")
        changes = client.sync()
        print(f"Sync complete: {changes.total_changes} changes")
        print(f"  Modified: {len(changes.modified)}")
        print(f"  Added: {len(changes.added)}")
        print(f"  Deleted: {len(changes.deleted)}")

    elif args.action == "check":
        print(f"Checking sync status with {args.server}...")
        if client.is_in_sync():
            print("Local tree is in sync with server")
        else:
            print("Local tree is OUT OF SYNC with server")

    elif args.action == "local":
        if not args.repo:
            print("Error: --repo required for 'local' action")
            sys.exit(1)
        print(f"Detecting local changes in {args.repo}...")
        changes = client.detect_local_changes(args.repo)
        print(f"Local changes: {changes.total_changes} total")
