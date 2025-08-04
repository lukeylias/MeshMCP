"""
Pydantic models for Model Context Protocol (MCP) data structures
"""

from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class MCPTool(BaseModel):
    """Represents an MCP tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPManifest(BaseModel):
    """MCP manifest containing available tools"""
    tools: List[MCPTool]

class MCPInvokeRequest(BaseModel):
    """Request structure for tool invocation"""
    arguments: Dict[str, Any] = {}

class MCPInvokeContent(BaseModel):
    """Content structure for MCP responses"""
    type: str
    text: str

class MCPInvokeResponse(BaseModel):
    """Response structure for tool invocation"""
    content: List[MCPInvokeContent]

class ComponentDetails(BaseModel):
    """Detailed information about a Mesh component"""
    name: str
    description: str
    props: Dict[str, Any]
    codeExamples: List[str]
    storybookUrl: str
    designGuidance: str

class DesignTokens(BaseModel):
    """Design tokens structure"""
    colors: Optional[Dict[str, Any]] = None
    typography: Optional[Dict[str, Any]] = None
    spacing: Optional[Dict[str, Any]] = None
    other: Optional[Dict[str, Any]] = None

class PlaceholderDataRequest(BaseModel):
    """Request for placeholder data generation"""
    dataType: str
    count: int = 10

class ComponentSearchRequest(BaseModel):
    """Request for component search by use case"""  
    useCase: str

class PrototypeCodeRequest(BaseModel):
    """Request for prototype code generation"""
    description: str
    components: List[str] = []
    includeData: bool = True

class ComponentSuggestion(BaseModel):
    """Component suggestion with relevance score"""
    name: str
    description: str
    relevanceScore: float
    reason: str