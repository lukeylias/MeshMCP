"""
Web scraping module for Mesh Design System
Handles scraping of components, documentation, and design tokens
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import httpx
from playwright.async_api import async_playwright, Page
import re
import json

logger = logging.getLogger(__name__)

class MeshScraper:
    """Scraper for Mesh Design System components and documentation"""
    
    def __init__(self):
        self.base_url = "https://www.meshdesignsystem.com"
        self.storybook_url = "https://storybook.meshdesignsystem.com"  # Adjust as needed
        self.design_tokens_url = f"{self.base_url}/design-tokens/tokens-reference"
        self.timeout = 30000  # 30 seconds
        
    async def scrape_components_list(self) -> List[str]:
        """Scrape the list of all available components"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Navigate to main components page
                await page.goto(f"{self.base_url}/components", timeout=self.timeout)
                await page.wait_for_load_state('networkidle')
                
                # Extract component names from navigation or component grid
                component_links = await page.query_selector_all('[href*="/components/"]')
                components = []
                
                for link in component_links:
                    href = await link.get_attribute('href')
                    text = await link.text_content()
                    
                    if href and '/components/' in href and text:
                        # Extract component name from URL or text
                        component_name = text.strip()
                        if component_name and component_name not in components:
                            components.append(component_name)
                
                await browser.close()
                
                # If we didn't find components via navigation, try alternative methods
                if not components:
                    components = await self._scrape_components_alternative(page)
                
                # Fallback to hardcoded list from PRD if scraping fails
                if not components:
                    logger.warning("Falling back to hardcoded component list from PRD")
                    components = [
                        "Accordion", "Alert", "Autocomplete", "Button", "Card", 
                        "Checkbox", "Checkbox Group", "Copy", "Date Picker", 
                        "Date Textbox", "Divider", "Error Template", "Expander", 
                        "Expander Group", "Feature Panel", "File Upload", "Footer", 
                        "Fonts", "Form", "Form Control", "Grow Layout", "Header", 
                        "Header Footer Layout", "Heading", "Hero Panel", "Icons", 
                        "Info Box", "Link", "Loader", "Logo", "Modal", "ModeProvider", 
                        "Overlay", "Product Card", "Progress Stepper", "Radio", 
                        "Radio Button", "Radio Group", "React HTML", "Select", 
                        "Simple Table", "Skip Link", "Table", "Tabs", "Tag", 
                        "Textarea", "Textbox", "Theme", "Tooltip", "Utility Button", 
                        "Villain Panel"
                    ]
                
                logger.info(f"Found {len(components)} components")
                return components
                
        except Exception as e:
            logger.error(f"Error scraping components list: {str(e)}")
            raise
    
    async def _scrape_components_alternative(self, page: Page) -> List[str]:
        """Alternative method to scrape components if primary method fails"""
        try:
            # Try to find components in the page content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            components = []
            
            # Look for common patterns that might indicate component names
            # This is a fallback and might need adjustment based on actual site structure
            for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'a', 'span']):
                text = element.get_text(strip=True)
                # Simple heuristic to identify component names
                if text and len(text) < 50 and any(word in text.lower() for word in ['button', 'card', 'input', 'modal', 'tab']):
                    if text not in components:
                        components.append(text)
            
            return components
            
        except Exception as e:
            logger.error(f"Error in alternative component scraping: {str(e)}")
            return []
    
    async def scrape_component_details(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Scrape detailed information for a specific component"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Try multiple URL patterns for the component
                possible_urls = [
                    f"{self.base_url}/components/{component_name.lower().replace(' ', '-')}",
                    f"{self.base_url}/components/{component_name.lower().replace(' ', '_')}",
                    f"{self.storybook_url}/?path=/docs/{component_name.lower().replace(' ', '-')}",
                ]
                
                component_details = None
                
                for url in possible_urls:
                    try:
                        await page.goto(url, timeout=self.timeout)
                        await page.wait_for_load_state('networkidle')
                        
                        # Check if page loaded successfully (not 404)
                        if page.url != url or "404" in await page.title():
                            continue
                            
                        component_details = await self._extract_component_details(page, component_name)
                        if component_details:
                            break
                            
                    except Exception as e:
                        logger.debug(f"Failed to load {url}: {str(e)}")
                        continue
                
                await browser.close()
                
                return component_details
                
        except Exception as e:
            logger.error(f"Error scraping component details for {component_name}: {str(e)}")
            return None
    
    async def _extract_component_details(self, page: Page, component_name: str) -> Dict[str, Any]:
        """Extract component details from the current page"""
        try:
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            details = {
                "name": component_name,
                "description": "",
                "props": {},
                "codeExamples": [],
                "storybookUrl": page.url,
                "designGuidance": ""
            }
            
            # Extract description
            description_selectors = [
                'p:first-of-type',
                '.description',
                '[class*="description"]',
                'h1 + p',
                'h2 + p'
            ]
            
            for selector in description_selectors:
                desc_element = soup.select_one(selector)
                if desc_element:
                    details["description"] = desc_element.get_text(strip=True)
                    break
            
            # Extract props information
            # Look for prop tables or prop documentation
            prop_tables = soup.find_all('table')
            for table in prop_tables:
                headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
                if any(header in ['prop', 'property', 'name'] for header in headers):
                    props = self._extract_props_from_table(table)
                    details["props"].update(props)
            
            # Extract code examples
            code_blocks = soup.find_all(['pre', 'code'])
            for code_block in code_blocks:
                code_text = code_block.get_text(strip=True)
                if len(code_text) > 10 and component_name.lower() in code_text.lower():
                    details["codeExamples"].append(code_text)
            
            # Extract design guidance
            guidance_selectors = [
                '.guidance',
                '.guidelines',
                '[class*="guidance"]',
                '[class*="guideline"]'
            ]
            
            for selector in guidance_selectors:
                guidance_element = soup.select_one(selector)
                if guidance_element:
                    details["designGuidance"] = guidance_element.get_text(strip=True)
                    break
            
            return details
            
        except Exception as e:
            logger.error(f"Error extracting component details: {str(e)}")
            return None
    
    def _extract_props_from_table(self, table) -> Dict[str, Any]:
        """Extract props information from an HTML table"""
        props = {}
        try:
            rows = table.find_all('tr')
            if not rows:
                return props
                
            # Get headers
            header_row = rows[0]
            headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
            
            # Map common header names
            name_idx = next((i for i, h in enumerate(headers) if h in ['name', 'prop', 'property']), -1)
            type_idx = next((i for i, h in enumerate(headers) if h in ['type', 'data type']), -1)
            desc_idx = next((i for i, h in enumerate(headers) if h in ['description', 'desc']), -1)
            default_idx = next((i for i, h in enumerate(headers) if h in ['default', 'default value']), -1)
            
            # Extract prop rows
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                    
                prop_info = {}
                
                if name_idx >= 0 and name_idx < len(cells):
                    prop_name = cells[name_idx].get_text(strip=True)
                    if not prop_name:
                        continue
                        
                    if type_idx >= 0 and type_idx < len(cells):
                        prop_info['type'] = cells[type_idx].get_text(strip=True)
                    
                    if desc_idx >= 0 and desc_idx < len(cells):
                        prop_info['description'] = cells[desc_idx].get_text(strip=True)
                    
                    if default_idx >= 0 and default_idx < len(cells):
                        prop_info['default'] = cells[default_idx].get_text(strip=True)
                    
                    props[prop_name] = prop_info
                    
        except Exception as e:
            logger.error(f"Error extracting props from table: {str(e)}")
            
        return props
    
    async def scrape_design_tokens(self, token_type: str = "all") -> Dict[str, Any]:
        """Scrape design tokens from the design tokens reference page"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(self.design_tokens_url, timeout=self.timeout)
                await page.wait_for_load_state('networkidle')
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                tokens = {}
                
                if token_type == "all" or token_type == "colors":
                    tokens["colors"] = await self._extract_color_tokens(soup)
                
                if token_type == "all" or token_type == "typography":
                    tokens["typography"] = await self._extract_typography_tokens(soup)
                
                if token_type == "all" or token_type == "spacing":
                    tokens["spacing"] = await self._extract_spacing_tokens(soup)
                
                await browser.close()
                
                return tokens
                
        except Exception as e:
            logger.error(f"Error scraping design tokens: {str(e)}")
            # Return basic fallback tokens
            return {
                "colors": {"primary": "#0066CC", "secondary": "#6C757D", "success": "#28A745"},
                "typography": {"fontFamily": "Inter, system-ui, sans-serif"},
                "spacing": {"small": "8px", "medium": "16px", "large": "24px"}
            }
    
    async def _extract_color_tokens(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract color tokens from the page"""
        colors = {}
        
        # Look for color swatches or color definitions
        color_elements = soup.find_all(['div', 'span'], class_=re.compile(r'color|swatch', re.I))
        
        for element in color_elements:
            # Try to extract color name and value
            color_name = element.get_text(strip=True)
            style = element.get('style', '')
            
            # Extract hex colors from style attribute
            hex_match = re.search(r'#[0-9A-Fa-f]{6}', style)
            if hex_match and color_name:
                colors[color_name] = hex_match.group(0)
        
        return colors if colors else {"primary": "#0066CC", "secondary": "#6C757D"}
    
    async def _extract_typography_tokens(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract typography tokens from the page"""
        typography = {}
        
        # Look for typography-related elements
        typo_elements = soup.find_all(['div', 'section'], class_=re.compile(r'typography|font', re.I))
        
        for element in typo_elements:
            text = element.get_text(strip=True)
            # Extract font families, sizes, etc.
            if 'font-family' in text.lower():
                # Basic extraction - would need refinement based on actual structure
                typography["fontFamily"] = "Inter, system-ui, sans-serif"
        
        return typography if typography else {"fontFamily": "Inter, system-ui, sans-serif"}
    
    async def _extract_spacing_tokens(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract spacing tokens from the page"""
        spacing = {}
        
        # Look for spacing-related elements
        spacing_elements = soup.find_all(['div', 'section'], class_=re.compile(r'spacing|margin|padding', re.I))
        
        for element in spacing_elements:
            text = element.get_text(strip=True)
            # Extract spacing values - would need refinement based on actual structure
            if any(unit in text for unit in ['px', 'rem', 'em']):
                # Basic extraction
                numbers = re.findall(r'\d+(?:px|rem|em)', text)
                for i, num in enumerate(numbers[:3]):
                    spacing_names = ['small', 'medium', 'large']
                    if i < len(spacing_names):
                        spacing[spacing_names[i]] = num
        
        return spacing if spacing else {"small": "8px", "medium": "16px", "large": "24px"}