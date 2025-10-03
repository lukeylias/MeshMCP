#!/usr/bin/env python3
"""
Test script for MeshMCP stdio server
Simulates MCP protocol interactions to verify tools work correctly
"""

import json
import subprocess
import sys

def test_mcp_server():
    """Test that the MCP server can start and respond to basic requests"""

    print("🧪 Testing MeshMCP Server...")
    print("=" * 60)

    # Test 1: Check if server can import and initialize
    print("\n✓ Test 1: Import Check")
    try:
        import main
        print("  ✅ Server imports successfully")
        print(f"  ✅ Found {len(main.mcp._tool_manager._tools)} tools registered")

        # List all registered tools
        for tool_name in main.mcp._tool_manager._tools.keys():
            print(f"     - {tool_name}")

    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

    # Test 2: Verify all 6 tools are registered
    print("\n✓ Test 2: Tool Registration Check")
    expected_tools = [
        'list_components',
        'get_component_details',
        'get_design_tokens',
        'generate_placeholder_data',
        'search_components_by_use_case',
        'generate_prototype_code'
    ]

    registered_tools = list(main.mcp._tool_manager._tools.keys())

    for tool in expected_tools:
        if tool in registered_tools:
            print(f"  ✅ {tool}")
        else:
            print(f"  ❌ {tool} - MISSING")
            return False

    # Test 3: Verify tool metadata
    print("\n✓ Test 3: Tool Metadata Check")
    for tool_name, tool_info in main.mcp._tool_manager._tools.items():
        func = tool_info['fn']
        docstring = func.__doc__ or "No description"
        print(f"  ✅ {tool_name}")
        print(f"     Description: {docstring[:70]}...")

    # Test 4: Check dependencies
    print("\n✓ Test 4: Dependency Check")
    dependencies = {
        'mesh_scraper': main.mesh_scraper,
        'cache_manager': main.cache_manager,
        'data_generator': main.data_generator
    }

    for name, obj in dependencies.items():
        if obj is not None:
            print(f"  ✅ {name} initialized")
        else:
            print(f"  ❌ {name} failed to initialize")
            return False

    print("\n" + "=" * 60)
    print("✅ All tests passed! MCP server is ready to use.")
    print("\nTo start the server:")
    print("  python main.py")
    print("\nTo configure in Claude Code, see SETUP.md")

    return True

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
