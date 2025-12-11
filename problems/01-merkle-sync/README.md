# Merkle Tree Sync Interview

See `PROBLEM.md` for the problem statement.

## Quick Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify starter code works
cd starter/common
python3 -c "from sample_data import get_tree_stats; print(get_tree_stats())"

# Start the server (from problem directory)
cd ../server
python3 main.py

# In another terminal, run tests (from problem directory)
pytest test_sync.py -v
```

## Files

```
01-merkle-sync/
├── README.md              # This file
├── PROBLEM.md             # Problem statement
├── api_design.md          # Template for API design
├── requirements.txt       # Python dependencies
├── test_sync.py           # Test skeleton
└── starter/
    ├── common/
    │   ├── merkle_tree.py      # Core Merkle tree implementation
    │   ├── sample_data.py      # Test data
    │   └── mcp_sdk_tree.json   # Real tree from MCP Python SDK
    ├── server/
    │   ├── main.py             # FastAPI server skeleton
    │   ├── Dockerfile
    │   └── k8s/
    │       ├── deployment.yaml
    │       └── service.yaml
    └── client/
        └── sync_client.py      # Client skeleton
```

## Test Data

The sample data is generated from the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk):
- ~400 real files
- V1 tree: Original state
- V2 tree: Simulated changes (2 modified, 2 added, 1 deleted)
