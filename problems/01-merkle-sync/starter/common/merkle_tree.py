"""
Merkle Tree Manager - PROVIDED CODE (do not modify)

This module provides efficient file change detection using content hashes.
Use this as a building block for your sync implementation.
"""

import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class ChangeSet:
    """Represents detected changes between two Merkle trees."""

    modified: list[str]  # Files with different hashes (exist in both, hash changed)
    added: list[str]     # Files only in new tree
    deleted: list[str]   # Files only in old tree

    @property
    def has_changes(self) -> bool:
        """Check if any changes were detected."""
        return bool(self.modified or self.added or self.deleted)

    @property
    def total_changes(self) -> int:
        """Total number of changed files."""
        return len(self.modified) + len(self.added) + len(self.deleted)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ChangeSet":
        """Create from dictionary."""
        return cls(
            modified=data.get("modified", []),
            added=data.get("added", []),
            deleted=data.get("deleted", [])
        )


# Type alias for clarity
MerkleTree = dict[str, str]  # {file_path: sha256_hash}


class MerkleTreeManager:
    """
    Manages Merkle trees for efficient change detection.

    A Merkle tree in this context is a flat dictionary mapping file paths
    to their SHA-256 content hashes. This enables O(1) lookups and simple
    change detection via set operations.

    Example usage:
        manager = MerkleTreeManager()

        # Build tree from filesystem
        tree = manager.build_merkle_tree("/path/to/repo")

        # Later, detect changes
        new_tree = manager.build_merkle_tree("/path/to/repo")
        changes = manager.detect_changes(tree, new_tree)

        if changes.has_changes:
            print(f"Modified: {changes.modified}")
            print(f"Added: {changes.added}")
            print(f"Deleted: {changes.deleted}")
    """

    # Directories to always exclude
    EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".tox", ".mypy_cache"}

    # File patterns to exclude
    EXCLUDED_EXTENSIONS = {".pyc", ".pyo", ".so", ".dylib", ".dll"}

    def __init__(self, excluded_dirs: Optional[set[str]] = None):
        """
        Initialize the Merkle tree manager.

        Args:
            excluded_dirs: Additional directories to exclude (optional)
        """
        self.excluded_dirs = self.EXCLUDED_DIRS.copy()
        if excluded_dirs:
            self.excluded_dirs.update(excluded_dirs)

    def build_merkle_tree(self, repo_path: str, max_workers: int = 4) -> MerkleTree:
        """
        Build a Merkle tree for the given directory.

        Walks the directory tree, computes SHA-256 hash for each file,
        and returns a dictionary mapping relative paths to hashes.

        Args:
            repo_path: Path to the repository/directory root
            max_workers: Number of parallel workers for file hashing

        Returns:
            Dict mapping relative file paths to their SHA-256 hashes
        """
        files_to_hash = self._find_files(repo_path)
        return self._hash_files_parallel(files_to_hash, max_workers)

    def _find_files(self, repo_path: str) -> list[tuple[str, str]]:
        """Find all files to include in the tree."""
        repo_path = Path(repo_path).resolve()
        files_to_process = []

        for root, dirs, files in os.walk(repo_path):
            # Filter out excluded directories (modifies in-place)
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]

            for file in files:
                # Skip excluded extensions
                if any(file.endswith(ext) for ext in self.EXCLUDED_EXTENSIONS):
                    continue

                file_path = Path(root) / file
                rel_path = file_path.relative_to(repo_path)
                files_to_process.append((str(file_path), str(rel_path)))

        return files_to_process

    def _hash_files_parallel(self, files: list[tuple[str, str]], max_workers: int) -> MerkleTree:
        """Hash files in parallel using ThreadPoolExecutor."""
        file_hashes = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {
                executor.submit(self._hash_file, abs_path): rel_path
                for abs_path, rel_path in files
            }

            for future in as_completed(future_to_path):
                rel_path = future_to_path[future]
                try:
                    file_hash = future.result()
                    if file_hash:
                        file_hashes[rel_path] = file_hash
                except Exception:
                    pass  # Skip files that can't be hashed

        return file_hashes

    def _hash_file(self, file_path: str) -> Optional[str]:
        """Compute SHA-256 hash of a single file."""
        try:
            hasher = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None

    def detect_changes(self, old_tree: MerkleTree, new_tree: MerkleTree) -> ChangeSet:
        """
        Detect changes between two Merkle trees.

        Compares the old and new trees to find:
        - Modified files: exist in both but hash changed
        - Added files: only in new tree
        - Deleted files: only in old tree

        Args:
            old_tree: Previous tree state
            new_tree: Current tree state

        Returns:
            ChangeSet with categorized changes
        """
        old_files = set(old_tree.keys())
        new_files = set(new_tree.keys())

        # Files in both trees with different hashes
        modified = [
            f for f in old_files & new_files
            if old_tree[f] != new_tree[f]
        ]

        # Files only in new tree
        added = list(new_files - old_files)

        # Files only in old tree
        deleted = list(old_files - new_files)

        return ChangeSet(modified=modified, added=added, deleted=deleted)

    @staticmethod
    def compute_tree_hash(tree: MerkleTree) -> str:
        """
        Compute a single hash representing the entire tree state.

        Useful for quick equality checks - if tree hashes match,
        the trees are identical (no need to compare file-by-file).

        Args:
            tree: Merkle tree to hash

        Returns:
            SHA-256 hash of the serialized tree
        """
        # Sort keys for deterministic serialization
        serialized = json.dumps(tree, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def save_tree(self, tree: MerkleTree, file_path: str) -> None:
        """Save a Merkle tree to a JSON file."""
        with open(file_path, "w") as f:
            json.dump(tree, f, indent=2, sort_keys=True)

    def load_tree(self, file_path: str) -> MerkleTree:
        """Load a Merkle tree from a JSON file."""
        try:
            with open(file_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


# Convenience functions for simple use cases

def build_tree(path: str) -> MerkleTree:
    """Build a Merkle tree from a directory path."""
    return MerkleTreeManager().build_merkle_tree(path)


def detect_changes(old: MerkleTree, new: MerkleTree) -> ChangeSet:
    """Detect changes between two trees."""
    return MerkleTreeManager().detect_changes(old, new)


def tree_hash(tree: MerkleTree) -> str:
    """Compute hash of entire tree for quick comparison."""
    return MerkleTreeManager.compute_tree_hash(tree)
