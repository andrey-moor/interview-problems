"""
Integration Tests for Merkle Tree Sync - SKELETON

TODO: Implement tests that verify your sync implementation works.

Test scenarios to cover:
1. Initial sync - client fetches tree for the first time
2. No changes - client checks and server hasn't changed
3. Server updated - client detects changes and syncs
4. Verify changes - confirm the changeset is correct

Hints:
- You can use the /debug/update-tree endpoint to simulate server changes
- The sample_data module has expected changes you can verify against
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "starter" / "common"))
sys.path.insert(0, str(Path(__file__).parent / "starter" / "client"))

import pytest

from merkle_tree import tree_hash
from sample_data import get_tree_v1, get_tree_v2, get_expected_changes
from sync_client import MerkleSyncClient


# Server URL - change if running on different port
SERVER_URL = "http://localhost:8000"


class TestMerkleSync:
    """Integration tests for Merkle tree synchronization."""

    @pytest.fixture
    def client(self):
        """Create a fresh sync client for each test."""
        return MerkleSyncClient(SERVER_URL)

    @pytest.fixture
    def reset_server(self, client):
        """Reset server to v1 tree before each test."""
        import httpx
        httpx.post(f"{SERVER_URL}/debug/reset-tree")
        yield
        # Could also reset after test if needed

    # ========================================================================
    # Test Cases - TODO: Implement these
    # ========================================================================

    def test_initial_sync(self, client, reset_server):
        """
        Test: Client can fetch tree for the first time.

        Steps:
        1. Client has no local tree
        2. Client syncs with server
        3. Client now has the server's tree

        Verify:
        - Local tree is not empty after sync
        - Local tree hash matches server tree hash
        """
        # TODO: Implement this test
        pytest.skip("TODO: Implement test_initial_sync")

    def test_already_in_sync(self, client, reset_server):
        """
        Test: Client correctly detects when already in sync.

        Steps:
        1. Client syncs (gets current tree)
        2. Server doesn't change
        3. Client checks is_in_sync()

        Verify:
        - is_in_sync() returns True
        """
        # TODO: Implement this test
        pytest.skip("TODO: Implement test_already_in_sync")

    def test_detect_server_changes(self, client, reset_server):
        """
        Test: Client detects when server has changed.

        Steps:
        1. Client syncs (gets v1 tree)
        2. Server updates to v2 tree
        3. Client checks is_in_sync()

        Verify:
        - is_in_sync() returns False
        """
        # TODO: Implement this test
        pytest.skip("TODO: Implement test_detect_server_changes")

    def test_sync_after_server_update(self, client, reset_server):
        """
        Test: Client correctly syncs after server update.

        Steps:
        1. Client syncs (gets v1 tree)
        2. Server updates to v2 tree
        3. Client syncs again

        Verify:
        - Sync returns a ChangeSet with the correct changes
        - Local tree now matches v2
        """
        # TODO: Implement this test
        pytest.skip("TODO: Implement test_sync_after_server_update")

    def test_changeset_accuracy(self, client, reset_server):
        """
        Test: ChangeSet accurately reflects what changed.

        Steps:
        1. Client syncs (gets v1 tree)
        2. Server updates to v2 tree
        3. Client syncs and gets ChangeSet

        Verify:
        - Modified files match expected
        - Added files match expected
        - Deleted files match expected
        """
        # TODO: Implement this test
        #
        # Hint: Use get_expected_changes() from sample_data
        # to verify the changeset is correct
        #
        pytest.skip("TODO: Implement test_changeset_accuracy")


# ============================================================================
# Helper for running tests
# ============================================================================

if __name__ == "__main__":
    # Run with: python test_sync.py
    # Or: pytest test_sync.py -v
    pytest.main([__file__, "-v"])
