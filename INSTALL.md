# Installation Guide - MeshMCP

## Fixed Dependency Issues ✅

The requirements.txt has been updated with compatible versions:
- **fastmcp** - Simplified MCP SDK for stdio servers
- **httpx** - Updated to >=0.27.0 for async HTTP
- **pydantic** - Pinned to 2.x to avoid breaking changes
- All dependencies now use flexible version ranges

## Installation Options

### Option 1: Fresh Virtual Environment (Recommended)

```bash
# Navigate to project
cd /Users/luke.ylias/Documents/GitHub/MeshMCP

# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Test installation
python3 test_mcp.py
```

### Option 2: Upgrade Existing Environment

```bash
# Navigate to project
cd /Users/luke.ylias/Documents/GitHub/MeshMCP

# Upgrade all dependencies
pip install -r requirements.txt --upgrade

# Verify Playwright
playwright install chromium

# Test installation
python3 test_mcp.py
```

### Option 3: Clean Install (If Issues Persist)

```bash
# Uninstall all packages
pip freeze | xargs pip uninstall -y

# Reinstall from requirements.txt
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Test installation
python3 test_mcp.py
```

## Verify Installation

Run the test script to verify all tools are working:

```bash
python3 test_mcp.py
```

Expected output:
```
🧪 Testing MeshMCP Server...
============================================================

✓ Test 1: Import Check
  ✅ Server imports successfully
  ✅ Found 6 tools registered
     - list_components
     - get_component_details
     - get_design_tokens
     - generate_placeholder_data
     - search_components_by_use_case
     - generate_prototype_code

✓ Test 2: Tool Registration Check
  ✅ list_components
  ✅ get_component_details
  ✅ get_design_tokens
  ✅ generate_placeholder_data
  ✅ search_components_by_use_case
  ✅ generate_prototype_code

✓ Test 3: Tool Metadata Check
  ✅ list_components
     Description: Provides a comprehensive list of all available UI components...
  ...

✓ Test 4: Dependency Check
  ✅ mesh_scraper initialized
  ✅ cache_manager initialized
  ✅ data_generator initialized

============================================================
✅ All tests passed! MCP server is ready to use.
```

## Updated requirements.txt

```txt
# MCP SDK (FastMCP for simplified stdio server)
fastmcp>=0.2.0

# Async and HTTP
httpx>=0.27.0
aiofiles>=23.2.0

# Web scraping
playwright>=1.40.0
beautifulsoup4>=4.12.0

# Data validation and generation
pydantic>=2.5.0,<3.0.0
faker>=22.0.0
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastmcp'`
**Solution:**
```bash
pip install fastmcp --upgrade
```

### Issue: `ModuleNotFoundError: No module named 'httpx'`
**Solution:**
```bash
pip install httpx --upgrade
```

### Issue: Playwright browser not found
**Solution:**
```bash
playwright install chromium --force
```

### Issue: Pydantic version conflicts
**Solution:**
```bash
pip install "pydantic>=2.5.0,<3.0.0" --force-reinstall
```

### Issue: Import errors persist
**Solution:** Use a fresh virtual environment (Option 1 above)

## Next Steps

After successful installation:

1. **Configure in VS Code** - See [SETUP.md](SETUP.md) for configuration
2. **Test with Claude** - Restart VS Code and test the tools
3. **Review docs** - Check [README.md](README.md) for usage examples

## Dependencies Explained

| Package | Purpose | Version |
|---------|---------|---------|
| `fastmcp` | MCP stdio server framework | ≥0.2.0 |
| `httpx` | Async HTTP client for scraping | ≥0.27.0 |
| `aiofiles` | Async file operations for caching | ≥23.2.0 |
| `playwright` | Browser automation for scraping | ≥1.40.0 |
| `beautifulsoup4` | HTML parsing | ≥4.12.0 |
| `pydantic` | Data validation | 2.5.0-2.x |
| `faker` | Test data generation | ≥22.0.0 |
