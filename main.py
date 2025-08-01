#!/usr/bin/env python3
"""
MCP Server for Mesh Design System
Provides AI assistants access to Mesh components and design tokens
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
import asyncio
from datetime import datetime, timedelta

from scrapers.mesh_scraper import MeshScraper
from cache.cache_manager import CacheManager
from models.mcp_models import MCPManifest, MCPTool, MCPInvokeRequest, MCPInvokeResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mesh Design System MCP Server",
    description="Model Context Protocol server for AI assistant integration with Mesh Design System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Initialize services
mesh_scraper = MeshScraper()
cache_manager = CacheManager()

# MCP Tools Definition
MCP_TOOLS = [
    MCPTool(
        name="listComponents",
        description="Provides a comprehensive list of all available UI components in the Mesh Design System",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ),
    MCPTool(
        name="getComponentDetails", 
        description="Fetches detailed information for a specific component",
        inputSchema={
            "type": "object",
            "properties": {
                "componentName": {
                    "type": "string",
                    "description": "Name of the component to get details for"
                }
            },
            "required": ["componentName"]
        }
    ),
    MCPTool(
        name="getDesignTokens",
        description="Provides core design tokens (colors, typography, spacing)",
        inputSchema={
            "type": "object", 
            "properties": {
                "tokenType": {
                    "type": "string",
                    "description": "Type of tokens to retrieve (optional)",
                    "enum": ["colors", "typography", "spacing", "all"]
                }
            },
            "required": []
        }
    )
]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Mesh Design System MCP Server", "status": "running", "version": "1.0.0"}

@app.get("/tools")
async def get_tools() -> MCPManifest:
    """Returns the MCP manifest with available tools"""
    logger.info("Returning MCP tools manifest")
    return MCPManifest(tools=MCP_TOOLS)

@app.post("/tools/{tool_name}/invoke")
async def invoke_tool(tool_name: str, request: MCPInvokeRequest) -> MCPInvokeResponse:
    """Execute a specific MCP tool"""
    logger.info(f"Invoking tool: {tool_name} with args: {request.arguments}")
    
    try:
        if tool_name == "listComponents":
            result = await handle_list_components()
        elif tool_name == "getComponentDetails":
            component_name = request.arguments.get("componentName")
            if not component_name:
                raise HTTPException(status_code=400, detail="componentName is required")
            result = await handle_get_component_details(component_name)
        elif tool_name == "getDesignTokens":
            token_type = request.arguments.get("tokenType", "all")
            result = await handle_get_design_tokens(token_type)
        else:
            raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
        return MCPInvokeResponse(content=[{"type": "text", "text": str(result)}])
        
    except Exception as e:
        logger.error(f"Error invoking tool {tool_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {str(e)}")

async def handle_list_components() -> List[str]:
    """Handle listComponents tool execution"""
    cache_key = "mesh_components_list"
    
    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info("Returning cached components list")
        return cached_result
    
    # Scrape components if not cached
    logger.info("Scraping components list from Mesh Design System")
    components = await mesh_scraper.scrape_components_list()
    
    # Cache the result
    await cache_manager.set(cache_key, components, ttl=3600)  # 1 hour TTL
    
    return components

async def handle_get_component_details(component_name: str) -> Dict[str, Any]:
    """Handle getComponentDetails tool execution"""
    cache_key = f"mesh_component_{component_name.lower()}"
    
    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached details for component: {component_name}")
        return cached_result
    
    # Scrape component details if not cached
    logger.info(f"Scraping details for component: {component_name}")
    details = await mesh_scraper.scrape_component_details(component_name)
    
    if not details:
        raise HTTPException(status_code=404, detail=f"Component '{component_name}' not found")
    
    # Cache the result
    await cache_manager.set(cache_key, details, ttl=7200)  # 2 hours TTL
    
    return details

async def handle_get_design_tokens(token_type: str = "all") -> Dict[str, Any]:
    """Handle getDesignTokens tool execution"""
    cache_key = f"mesh_design_tokens_{token_type}"
    
    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached design tokens for type: {token_type}")
        return cached_result
    
    # Scrape design tokens if not cached
    logger.info(f"Scraping design tokens for type: {token_type}")
    tokens = await mesh_scraper.scrape_design_tokens(token_type)
    
    # Cache the result
    await cache_manager.set(cache_key, tokens, ttl=7200)  # 2 hours TTL
    
    return tokens

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)