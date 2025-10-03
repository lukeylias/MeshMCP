# MeshMCP - Mesh Design System MCP Server

A stdio-based Model Context Protocol (MCP) server that provides Claude Code (VS Code) access to the Mesh Design System components, design tokens, and prototyping tools.

## Features

- 🎨 **Component Discovery** - List all Mesh Design System components
- 📋 **Component Details** - Get props, examples, and design guidance
- 🎨 **Design Tokens** - Access colors, typography, and spacing tokens
- 🔄 **Placeholder Data** - Generate realistic insurance/healthcare test data
- 🔍 **Use Case Search** - Find components for specific UI patterns
- 💻 **Code Generation** - Generate React prototype code with Mesh components
- ⚡ **Smart Caching** - File-based caching with TTL for performance

## Quick Start

### 1. Install Dependencies

**⚠️ Dependencies Fixed!** See [INSTALL.md](INSTALL.md) for detailed installation instructions.

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Test the Server
```bash
python3 test_mcp.py
```

### 3. Configure in VS Code

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

**Restart VS Code** and start using the tools with Claude!

## Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `list_components` | Lists all Mesh components | "List all Mesh components" |
| `get_component_details` | Get component props & examples | "Get details for Button component" |
| `get_design_tokens` | Retrieve design tokens | "Show me Mesh color tokens" |
| `generate_placeholder_data` | Generate test data | "Generate 5 member records" |
| `search_components_by_use_case` | Find components for use cases | "Components for a data table" |
| `generate_prototype_code` | Generate React code | "Create a member signup form" |

## Project Structure

```
MeshMCP/
├── main.py                    # FastMCP server entry point
├── requirements.txt           # Python dependencies
├── test_mcp.py               # Test script
├── SETUP.md                  # Detailed setup guide
├── QUICK_START.md            # Quick reference
├── scrapers/
│   └── mesh_scraper.py       # Web scraping with Playwright
├── cache/
│   └── cache_manager.py      # File-based caching
├── generators/
│   └── data_generator.py     # Placeholder data generation
└── models/
    └── mcp_models.py         # Pydantic models
```

## How It Works

```
Claude Code (VS Code)
    ↓ stdio (JSON-RPC)
FastMCP Server (main.py)
    ↓
┌─────────────────────────────┐
│  mesh_scraper.py (Playwright)│ → Mesh Design System
│  cache_manager.py (File)    │ → cache_data/
│  data_generator.py (Faker)  │ → Test data
└─────────────────────────────┘
```

## Troubleshooting

**Server not connecting?**
```bash
# Verify installation
python3 test_mcp.py

# Check MCP package
pip list | grep mcp
```

**Cache issues?**
```bash
# Clear cache (will regenerate)
rm -rf cache_data/
```

**Playwright errors?**
```bash
# Reinstall browsers
playwright install --force chromium
```

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Installation & configuration in 3 steps
- **[SETUP.md](SETUP.md)** - Complete setup guide with troubleshooting

## Tech Stack

- **MCP SDK** - Model Context Protocol for Claude integration
- **Playwright** - Web scraping for component data
- **Faker** - Realistic Australian insurance data generation
- **Pydantic** - Data validation
- **aiofiles** - Async file operations for caching

## License

See LICENSE file for details.
