#!/usr/bin/env python3
"""
MCP Server for Mesh Design System
Provides AI assistants access to Mesh components and design tokens
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, List, Any
import logging
import json

from scrapers.mesh_scraper import MeshScraper
from cache.cache_manager import CacheManager
from generators.data_generator import DataGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Mesh Design System")

# Initialize services
mesh_scraper = MeshScraper()
cache_manager = CacheManager()
data_generator = DataGenerator()

# Tool 1: List Components
@mcp.tool()
async def list_components() -> str:
    """Provides a comprehensive list of all available UI components in the Mesh Design System"""
    cache_key = "mesh_components_list"

    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info("Returning cached components list")
        return json.dumps(cached_result, indent=2)

    # Scrape components if not cached
    logger.info("Scraping components list from Mesh Design System")
    components = await mesh_scraper.scrape_components_list()

    # Cache the result
    await cache_manager.set(cache_key, components, ttl=3600)  # 1 hour TTL

    return json.dumps(components, indent=2)

# Tool 2: Get Component Details
@mcp.tool()
async def get_component_details(component_name: str) -> str:
    """Fetches detailed information for a specific component including props, examples, and design guidance"""
    cache_key = f"mesh_component_{component_name.lower()}"

    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached details for component: {component_name}")
        return json.dumps(cached_result, indent=2)

    # Scrape component details if not cached
    logger.info(f"Scraping details for component: {component_name}")
    details = await mesh_scraper.scrape_component_details(component_name)

    if not details:
        return json.dumps({"error": f"Component '{component_name}' not found"}, indent=2)

    # Cache the result
    await cache_manager.set(cache_key, details, ttl=7200)  # 2 hours TTL

    return json.dumps(details, indent=2)

# Tool 3: Get Design Tokens
@mcp.tool()
async def get_design_tokens(token_type: str = "all") -> str:
    """Provides core design tokens (colors, typography, spacing) from the Mesh Design System"""
    cache_key = f"mesh_design_tokens_{token_type}"

    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached design tokens for type: {token_type}")
        return json.dumps(cached_result, indent=2)

    # Scrape design tokens if not cached
    logger.info(f"Scraping design tokens for type: {token_type}")
    tokens = await mesh_scraper.scrape_design_tokens(token_type)

    # Cache the result
    await cache_manager.set(cache_key, tokens, ttl=7200)  # 2 hours TTL

    return json.dumps(tokens, indent=2)

# Tool 4: Generate Placeholder Data
@mcp.tool()
async def generate_placeholder_data(data_type: str, count: int = 10) -> str:
    """Generate realistic placeholder data for insurance/healthcare prototyping (members, policies, claims, providers)"""
    cache_key = f"placeholder_data_{data_type}_{count}"

    # Check cache first (shorter TTL for placeholder data)
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached placeholder data for type: {data_type}, count: {count}")
        return json.dumps(cached_result, indent=2)

    # Generate new data
    logger.info(f"Generating placeholder data for type: {data_type}, count: {count}")
    try:
        data = data_generator.generate_data(data_type, count)

        # Cache the result with shorter TTL (30 minutes)
        await cache_manager.set(cache_key, data, ttl=1800)

        return json.dumps(data, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)
    except Exception as e:
        logger.error(f"Error generating placeholder data: {str(e)}")
        return json.dumps({"error": f"Data generation failed: {str(e)}"}, indent=2)

# Tool 5: Search Components By Use Case
@mcp.tool()
async def search_components_by_use_case(use_case: str) -> str:
    """Find relevant Mesh components for specific UI patterns and use cases (e.g., tables, forms, dashboards)"""
    cache_key = f"use_case_search_{use_case.lower().replace(' ', '_')}"

    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached component suggestions for use case: {use_case}")
        return json.dumps(cached_result, indent=2)

    # Generate component suggestions
    logger.info(f"Searching components for use case: {use_case}")
    suggestions = await _search_components_by_use_case(use_case)

    # Cache the result
    await cache_manager.set(cache_key, suggestions, ttl=3600)

    return json.dumps(suggestions, indent=2)

async def _search_components_by_use_case(use_case: str) -> List[Dict[str, Any]]:
    """Internal logic for component search by use case"""
    use_case_lower = use_case.lower()
    
    # Pre-defined use case mappings
    use_case_mappings = {
        "table": {
            "components": ["Table", "Simple Table", "Button", "Select", "Input"],
            "description": "Data display with optional filtering and actions"
        },
        "filter": {
            "components": ["Select", "Input", "Checkbox", "Button", "Date Picker"],
            "description": "Filtering and search controls"
        },
        "form": {
            "components": ["Form", "Form Control", "Input", "Select", "Checkbox", "Button", "Textarea"],
            "description": "User input and data collection"
        },
        "dashboard": {
            "components": ["Card", "Container", "Grid", "Stats", "Progress", "Button"],
            "description": "Overview and summary displays"
        },
        "navigation": {
            "components": ["Header", "Menu", "Breadcrumb", "Tabs", "Link"],
            "description": "Site navigation and wayfinding"
        },
        "search": {
            "components": ["Input", "Button", "Card", "Select", "Autocomplete"],
            "description": "Search interfaces and results"
        },
        "layout": {
            "components": ["Container", "Grid", "Stack", "Section", "Divider"],
            "description": "Page structure and organization"
        },
        "modal": {
            "components": ["Modal", "Button", "Form", "Card"],
            "description": "Overlays and dialog boxes"
        },
        "list": {
            "components": ["Card", "Stack", "Button", "Tag", "Divider"],
            "description": "Item lists and collections"
        },
        "upload": {
            "components": ["File Upload", "Button", "Progress", "Alert"],
            "description": "File handling and upload interfaces"
        }
    }
    
    suggestions = []
    
    # Find matching use cases
    for pattern, mapping in use_case_mappings.items():
        if pattern in use_case_lower:
            score = 1.0  # Exact match
            for component in mapping["components"]:
                suggestions.append({
                    "name": component,
                    "description": mapping["description"],
                    "relevanceScore": score,
                    "reason": f"Commonly used in {pattern} interfaces"
                })
            break
    
    # If no exact match, try keyword matching
    if not suggestions:
        keyword_mappings = {
            "data": ["Table", "Simple Table", "Card"],
            "input": ["Input", "Form", "Select", "Textarea"], 
            "button": ["Button", "Utility Button"],
            "display": ["Card", "Alert", "Info Box"],
            "select": ["Select", "Dropdown", "Autocomplete"],
            "date": ["Date Picker", "Date Textbox"],
            "text": ["Input", "Textarea", "Heading"],
            "grid": ["Table", "Container", "Grid"],
            "chart": ["Progress", "Stats"],
            "menu": ["Header", "Tabs", "Navigation"]
        }
        
        for keyword, components in keyword_mappings.items():
            if keyword in use_case_lower:
                for component in components:
                    suggestions.append({
                        "name": component,
                        "description": f"Relevant for {keyword}-related interfaces",
                        "relevanceScore": 0.7,
                        "reason": f"Contains keyword: {keyword}"
                    })
    
    # If still no matches, provide general suggestions
    if not suggestions:
        general_components = ["Container", "Card", "Button", "Input", "Select"]
        for component in general_components:
            suggestions.append({
                "name": component,
                "description": "General-purpose component",
                "relevanceScore": 0.3,
                "reason": "Commonly used component"
            })
    
    # Remove duplicates and sort by relevance score
    unique_suggestions = {}
    for suggestion in suggestions:
        name = suggestion["name"]
        if name not in unique_suggestions or unique_suggestions[name]["relevanceScore"] < suggestion["relevanceScore"]:
            unique_suggestions[name] = suggestion
    
    return sorted(unique_suggestions.values(), key=lambda x: x["relevanceScore"], reverse=True)

# Tool 6: Generate Prototype Code
@mcp.tool()
async def generate_prototype_code(description: str, components: List[str] = [], include_data: bool = True) -> str:
    """Generate complete React component code using Mesh components based on a description"""
    cache_key = f"prototype_code_{description.lower().replace(' ', '_')}_{len(components)}_{include_data}"

    # Check cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        logger.info(f"Returning cached prototype code for: {description}")
        return cached_result

    # Generate new code
    logger.info(f"Generating prototype code for: {description}")
    code = await _generate_prototype_code(description, components, include_data)

    # Cache the result
    await cache_manager.set(cache_key, code, ttl=3600)

    return code

async def _generate_prototype_code(description: str, components: List[str], include_data: bool = True) -> str:
    """Internal logic for prototype code generation"""
    description_lower = description.lower()
    
    # Determine component type based on description
    if any(keyword in description_lower for keyword in ["table", "list", "data"]):
        return _generate_table_component(components, include_data)
    elif any(keyword in description_lower for keyword in ["form", "input", "submit"]):
        return _generate_form_component(components, include_data)
    elif any(keyword in description_lower for keyword in ["dashboard", "summary", "overview"]):
        return _generate_dashboard_component(components, include_data)
    else:
        return _generate_generic_component(description, components, include_data)

def _generate_table_component(components: List[str], include_data: bool = True) -> str:
    """Generate a table component with filtering"""
    data_import = ""
    data_code = ""
    
    if include_data:
        data_import = "import { useState, useEffect } from 'react';"
        data_code = """
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    // Placeholder data - replace with actual API call
    const mockData = [
      { id: 1, name: 'John Smith', policy: 'Gold Hospital', status: 'Active', premium: 299 },
      { id: 2, name: 'Sarah Jones', policy: 'Silver Extras', status: 'Active', premium: 189 },
      { id: 3, name: 'Mike Wilson', policy: 'Bronze Combined', status: 'Suspended', premium: 159 },
    ];
    setData(mockData);
    setFilteredData(mockData);
  }, []);

  useEffect(() => {
    if (filter) {
      setFilteredData(data.filter(item => 
        item.name.toLowerCase().includes(filter.toLowerCase()) ||
        item.policy.toLowerCase().includes(filter.toLowerCase())
      ));
    } else {
      setFilteredData(data);
    }
  }, [filter, data]);"""
    
    return f"""import React from 'react';
{data_import}
import {{ Table, Select, Button, Input, Container }} from '@nib/mesh-ds-react';

const DataTableComponent = () => {{{data_code}

  const handleFilterChange = (event) => {{
    setFilter(event.target.value);
  }};

  const columns = [
    {{ key: 'name', title: 'Name' }},
    {{ key: 'policy', title: 'Policy Type' }},
    {{ key: 'status', title: 'Status' }},
    {{ key: 'premium', title: 'Premium ($)' }},
  ];

  return (
    <Container>
      <div style={{{{ marginBottom: 16 }}}}>
        <Input
          placeholder="Search members..."
          value={{filter}}
          onChange={{handleFilterChange}}
        />
      </div>
      <Table
        columns={{columns}}
        data={{filteredData}}
        pagination
      />
    </Container>
  );
}};

export default DataTableComponent;"""

def _generate_form_component(components: List[str], include_data: bool = True) -> str:
    """Generate a form component with validation"""
    state_code = ""
    
    if include_data:
        state_code = """
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    policyType: '',
    category: ''
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Form submitted:', formData);
    // Add your submission logic here
  };"""
    
    return f"""import React{{ useState }} from 'react';
import {{ Form, FormControl, Input, Select, Button, Container }} from '@nib/mesh-ds-react';

const FormComponent = () => {{{state_code}

  const policyOptions = [
    {{ value: 'hospital', label: 'Hospital Cover' }},
    {{ value: 'extras', label: 'Extras Cover' }},
    {{ value: 'combined', label: 'Hospital + Extras' }}
  ];

  const categoryOptions = [
    {{ value: 'basic', label: 'Basic' }},
    {{ value: 'bronze', label: 'Bronze' }},
    {{ value: 'silver', label: 'Silver' }},
    {{ value: 'gold', label: 'Gold' }}
  ];

  return (
    <Container>
      <Form onSubmit={{handleSubmit}}>
        <FormControl label="First Name" required>
          <Input
            value={{formData.firstName}}
            onChange={{(e) => handleChange('firstName', e.target.value)}}
            placeholder="Enter first name"
          />
        </FormControl>
        
        <FormControl label="Last Name" required>
          <Input
            value={{formData.lastName}}
            onChange={{(e) => handleChange('lastName', e.target.value)}}
            placeholder="Enter last name"
          />
        </FormControl>
        
        <FormControl label="Email" required>
          <Input
            type="email"
            value={{formData.email}}
            onChange={{(e) => handleChange('email', e.target.value)}}
            placeholder="Enter email address"
          />
        </FormControl>
        
        <FormControl label="Policy Type" required>
          <Select
            options={{policyOptions}}
            value={{formData.policyType}}
            onChange={{(value) => handleChange('policyType', value)}}
            placeholder="Select policy type"
          />
        </FormControl>
        
        <FormControl label="Category">
          <Select
            options={{categoryOptions}}
            value={{formData.category}}
            onChange={{(value) => handleChange('category', value)}}
            placeholder="Select category"
          />
        </FormControl>
        
        <Button type="submit" variant="primary">
          Submit Application
        </Button>
      </Form>
    </Container>
  );
}};

export default FormComponent;"""

def _generate_dashboard_component(components: List[str], include_data: bool = True) -> str:
    """Generate a dashboard component with summary cards"""
    return f"""import React from 'react';
import {{ Card, Container, Grid, Stats, Button }} from '@nib/mesh-ds-react';

const DashboardComponent = () => {{
  const stats = [
    {{ title: 'Total Members', value: '12,543', change: '+5.2%' }},
    {{ title: 'Active Policies', value: '9,876', change: '+2.1%' }},
    {{ title: 'Claims This Month', value: '1,234', change: '-1.5%' }},
    {{ title: 'Revenue YTD', value: '$2.4M', change: '+8.7%' }}
  ];

  return (
    <Container>
      <Grid columns={{4}} gap="medium">
        {{stats.map((stat, index) => (
          <Card key={{index}}>
            <Stats
              title={{stat.title}}
              value={{stat.value}}
              change={{stat.change}}
            />
          </Card>
        ))}}
      </Grid>
      
      <Grid columns={{2}} gap="large" style={{{{ marginTop: 24 }}}}>
        <Card>
          <h3>Recent Claims</h3>
          <p>Claims processing summary and recent activity</p>
          <Button variant="secondary">View All Claims</Button>
        </Card>
        
        <Card>
          <h3>Member Activity</h3>
          <p>Member engagement and policy updates</p>
          <Button variant="secondary">View Member Reports</Button>
        </Card>
      </Grid>
    </Container>
  );
}};

export default DashboardComponent;"""

def _generate_generic_component(description: str, components: List[str], include_data: bool = True) -> str:
    """Generate a generic component based on description"""
    component_imports = ", ".join(components) if components else "Container, Card, Button"
    
    return f"""import React from 'react';
import {{ {component_imports} }} from '@nib/mesh-ds-react';

const CustomComponent = () => {{
  // Component for: {description}
  
  return (
    <Container>
      <Card>
        <h2>Custom Component</h2>
        <p>Generated component for: {description}</p>
        <Button variant="primary">Action Button</Button>
      </Card>
    </Container>
  );
}};

export default CustomComponent;"""

# Entry point for stdio-based MCP server
if __name__ == "__main__":
    mcp.run()