# MeshMCP Quick Start

## Installation (3 steps)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Playwright browser
playwright install chromium

# 3. Test the server
python3 test_mcp.py
```

## VS Code Configuration

Add to `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "mesh-design-system": {
      "command": "python3",
      "args": ["main.py"],
      "cwd": "/Users/luke.ylias/Documents/GitHub/MeshMCP"
    }
  }
}
```

**Then restart VS Code.**

## Available Tools in Claude Code

| Tool | Example Usage |
|------|---------------|
| `list_components` | "List all Mesh components" |
| `get_component_details` | "Get details for the Button component" |
| `get_design_tokens` | "Show me the Mesh color tokens" |
| `generate_placeholder_data` | "Generate 5 sample member records" |
| `search_components_by_use_case` | "Find components for building a data table" |
| `generate_prototype_code` | "Generate a form component for member signup" |

## File Structure

```
MeshMCP/
├── main.py                    # stdio MCP server
├── requirements.txt           # Dependencies
├── test_mcp.py               # Test script
├── README.md                  # Main documentation
├── SETUP.md                   # Full setup guide
├── QUICK_START.md             # This file
├── scrapers/
│   └── mesh_scraper.py       # Web scraping
├── cache/
│   └── cache_manager.py      # Caching layer
├── generators/
│   └── data_generator.py     # Data generation
└── models/
    └── mcp_models.py         # Data models
```

## Troubleshooting

**Server not connecting?**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Verify MCP installed
pip list | grep mcp

# Check VS Code logs
# Command Palette → "Developer: Show Logs" → Extension Host
```

**Cache issues?**
```bash
# Clear cache
rm -rf cache_data/
```

**Playwright errors?**
```bash
# Reinstall browsers
playwright install --force chromium
```

## What Changed from HTTP Version

| Aspect | Before | After |
|--------|--------|-------|
| **Transport** | HTTP (port 8000) | stdio |
| **Framework** | FastAPI + uvicorn | FastMCP |
| **Entry Point** | `uvicorn.run(app)` | `mcp.run()` |
| **Tool Decorator** | `@app.post("/tools/{name}")` | `@mcp.tool()` |
| **Return Type** | Pydantic models | JSON strings |
| **Errors** | `HTTPException` | JSON error objects |

## What Stayed the Same ✅

- All 6 tools with same functionality
- Web scraping with Playwright
- File-based caching with TTL
- Australian insurance data generation
- Error handling and logging
- Component search logic
- Code generation templates

---

**Ready to use!** Just configure in VS Code and ask Claude to use the tools.
