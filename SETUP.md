# MeshMCP Setup Guide - Stdio-based MCP Server

## Overview
Your MeshMCP server has been converted from HTTP/FastAPI to a stdio-based MCP server compatible with Claude Code in VS Code.

## What Changed

### ✅ Converted Components
- **Transport Layer**: FastAPI/HTTP → stdio using FastMCP
- **Main Entry**: [main.py](main.py) - Converted all 6 tools to use `@mcp.tool()` decorators
- **Dependencies**: [requirements.txt](requirements.txt) - Removed FastAPI/uvicorn, added `mcp` SDK

### ✅ Preserved Components (Unchanged)
- [scrapers/mesh_scraper.py](scrapers/mesh_scraper.py) - All scraping logic intact
- [cache/cache_manager.py](cache/cache_manager.py) - File-based caching intact
- [generators/data_generator.py](generators/data_generator.py) - Data generation intact
- All business logic, caching, and error handling preserved

## Installation

### 1. Install Python Dependencies
```bash
cd /Users/luke.ylias/Documents/GitHub/MeshMCP
pip install -r requirements.txt
```

### 2. Install Playwright Browsers (for web scraping)
```bash
playwright install chromium
```

### 3. Test the Server Locally
```bash
python main.py
```
The server will run in stdio mode, waiting for MCP protocol messages on stdin.

## Configure Claude Code in VS Code

### Option 1: User-level Configuration (Recommended)
Add to your `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "mesh-design-system": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/Users/luke.ylias/Documents/GitHub/MeshMCP"
    }
  }
}
```

### Option 2: Project-level Configuration
Use the [claude_desktop_config.json](claude_desktop_config.json) file included in this directory as a reference.

### Restart VS Code
After configuration, restart VS Code for changes to take effect.

## Available Tools

Your MCP server provides 6 tools to Claude:

1. **list_components** - Lists all Mesh Design System components
2. **get_component_details** - Fetches details for a specific component (props, examples, guidance)
3. **get_design_tokens** - Retrieves design tokens (colors, typography, spacing)
4. **generate_placeholder_data** - Generates realistic insurance/healthcare test data (members, policies, claims, providers)
5. **search_components_by_use_case** - Finds relevant components for UI patterns (tables, forms, dashboards, etc.)
6. **generate_prototype_code** - Generates React component code using Mesh components

## Testing the Integration

Once configured in Claude Code:

1. Open VS Code with Claude Code extension installed
2. Start a conversation with Claude
3. Ask Claude to: "List all available Mesh components"
4. Claude should invoke your `list_components` tool automatically

## Troubleshooting

### Server not connecting
- Check that Python path is correct: `which python`
- Verify dependencies installed: `pip list | grep mcp`
- Check VS Code extension logs for errors

### Playwright errors
- Run: `playwright install chromium`
- Ensure you have sufficient disk space

### Cache issues
- Clear cache directory: `rm -rf cache_data/`
- Cache will regenerate on next request

## Architecture

```
Claude Code (VS Code)
    ↓ stdio (JSON-RPC)
FastMCP Server (main.py)
    ↓ async function calls
┌─────────────────────────────┐
│  mesh_scraper.py (Playwright)│ → Mesh Design System website
│  cache_manager.py (File cache)│ → cache_data/
│  data_generator.py (Faker)   │ → Placeholder data
└─────────────────────────────┘
```

## Next Steps

1. Test all 6 tools through Claude Code
2. Adjust cache TTLs in [main.py](main.py) if needed (currently 1-2 hours)
3. Monitor logs for scraping errors
4. Update fallback component list in [mesh_scraper.py](scrapers/mesh_scraper.py:60) if Mesh Design System adds new components

## Notes

- All existing business logic preserved
- Caching layer still active (cache_data/ directory)
- Error handling maintained (returns JSON errors instead of HTTP exceptions)
- Tool descriptions embedded in docstrings for Claude to understand
