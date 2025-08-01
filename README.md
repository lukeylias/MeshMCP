# Mesh Design System MCP Server

A Model Context Protocol (MCP) server that provides AI assistants access to the Mesh Design System components and design tokens.

## Overview

This MCP server acts as a bridge between AI-powered development tools (like Cursor.ai) and the Mesh Design System, enabling AI assistants to natively understand and utilize Mesh components.

## Features

- **Component Discovery**: Lists all available UI components in the Mesh Design System
- **Component Details**: Provides comprehensive information about specific components including props, usage guidelines, and code examples
- **Design Tokens**: Access to core design tokens (colors, typography, spacing)
- **Caching**: Intelligent caching system to optimize performance and reduce scraping overhead
- **Docker Support**: Containerized deployment for easy scaling

## MCP Tools

### 1. `listComponents`

Returns a list of all available components in the Mesh Design System.

**Input**: None
**Output**: JSON array of component names

### 2. `getComponentDetails`

Fetches detailed information for a specific component.

**Input**:

- `componentName` (string): Name of the component

**Output**: JSON object containing:

- `name`: Component name
- `description`: Component description and usage
- `props`: Mapping of prop names to their types, descriptions, and defaults
- `codeExamples`: Array of code snippets
- `storybookUrl`: Direct link to Storybook page
- `designGuidance`: Usage guidelines

### 3. `getDesignTokens`

Provides core design tokens.

**Input**:

- `tokenType` (optional string): Type of tokens ("colors", "typography", "spacing", or "all")

**Output**: JSON object with design tokens

## Installation

### Local Development

1. Clone the repository:

```bash
git clone <repository-url>
cd MeshMCP
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:

```bash
playwright install chromium
```

4. Run the server:

```bash
python main.py
```

The server will be available at `http://localhost:8000`

### Docker Deployment

1. Build and run with Docker Compose:

```bash
docker-compose up --build
```

2. Or build and run manually:

```bash
docker build -t mesh-mcp-server .
docker run -p 8000:8000 mesh-mcp-server
```

## API Endpoints

- **GET /**: Health check endpoint
- **GET /tools**: Returns the MCP manifest with available tools
- **POST /tools/{tool_name}/invoke**: Execute a specific MCP tool

## Usage with AI Assistants

### Cursor.ai Integration

1. Configure Cursor.ai to connect to the MCP server endpoint: `http://localhost:8000`
2. The AI assistant can now use the tools to:
   - Discover available Mesh components
   - Get detailed component information
   - Access design tokens for consistent styling

### Example Queries

- "What components are available in the Mesh Design System?"
- "Show me the props for the Button component"
- "What are the available color tokens?"
- "Generate a form using Mesh components"

## Configuration

Environment variables:

- `LOG_LEVEL`: Logging level (default: INFO)
- `CACHE_TTL`: Cache TTL in seconds (default: 3600 for components list, 7200 for details)

## Caching

The server implements intelligent caching:

- Components list: 1 hour TTL
- Component details: 2 hours TTL
- Design tokens: 2 hours TTL
- Cache stored in `cache_data/` directory
- Automatic cleanup of expired entries

## Error Handling

The server includes robust error handling for:

- Component not found scenarios
- Web scraping failures
- Invalid input parameters
- Network timeout issues

## Development

### Project Structure

```
MeshMCP/
├── main.py                 # FastAPI application entry point
├── models/
│   ├── __init__.py
│   └── mcp_models.py      # Pydantic models for MCP
├── scrapers/
│   ├── __init__.py
│   └── mesh_scraper.py    # Web scraping logic
├── cache/
│   ├── __init__.py
│   └── cache_manager.py   # Caching system
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md            # This file
```

### Testing

Test the server endpoints:

```bash
# Health check
curl http://localhost:8000/

# Get available tools
curl http://localhost:8000/tools

# List components
curl -X POST http://localhost:8000/tools/listComponents/invoke \
  -H "Content-Type: application/json" \
  -d '{"arguments": {}}'

# Get component details
curl -X POST http://localhost:8000/tools/getComponentDetails/invoke \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"componentName": "Button"}}'
```
