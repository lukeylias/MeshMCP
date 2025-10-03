"""
Pydantic models for data structures
Note: MCP protocol models are now handled by the FastMCP library
These models are kept for internal data validation
"""

from pydantic import BaseModel
from typing import Dict, List, Any, Optional

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