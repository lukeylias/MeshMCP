# MeshMCP Enhancement PRD

## Product Requirements Document for Prototyping Workflow Integration

### Overview

Enhance the existing MeshMCP server to become a comprehensive prototyping assistant that not only provides component information but actively generates realistic placeholder data and React prototype code for rapid UI mockup creation.

### Current State

- ✅ FastAPI-based MCP server with Docker support
- ✅ Component discovery and detailed component information
- ✅ Design token access
- ✅ Intelligent caching system
- ✅ Web scraping from Mesh Storybook

### Enhancement Goals

Transform MeshMCP from a read-only component reference into an active prototyping assistant that can generate working React code and realistic data for rapid concept validation.

---

## New Features

### 1. Placeholder Data Generation

**Requirement**: Generate realistic placeholder data tailored to nib's insurance/healthcare context.

**Implementation**:

- **Tool**: `generatePlaceholderData`
- **Data Types**: members, policies, claims, providers
- **Configurable**: count parameter (default: 10)
- **Realistic**: Australian names, insurance-specific terminology, realistic dates/amounts

**Input Schema**:

```json
{
  "dataType": "members|policies|claims|providers",
  "count": 10
}
```

**Output**: JSON array of realistic records with appropriate fields for each data type.

### 2. React Code Generation

**Requirement**: Generate complete, working React components using actual Mesh components.

**Implementation**:

- **Tool**: `generatePrototypeCode`
- **Templates**: Table with filters, forms, dashboards, generic layouts
- **Integration**: Uses existing component details from scraper
- **Smart**: Includes imports, state management, event handlers

**Input Schema**:

```json
{
  "description": "table with dropdown filters",
  "components": ["Table", "Select", "Button"],
  "includeData": true
}
```

**Output**: Complete React component code ready to use in prototyping workspace.

### 3. Use Case Component Search

**Requirement**: Intelligent component suggestions based on UI patterns and use cases.

**Implementation**:

- **Tool**: `searchComponentsByUseCase`
- **Mapping**: Pre-defined use case → component mappings
- **Smart Matching**: Keyword analysis and relevance scoring
- **Context Aware**: Insurance/healthcare specific suggestions

**Input Schema**:

```json
{
  "useCase": "data table with filtering and sorting"
}
```

**Output**: Ranked list of relevant components with descriptions and relevance scores.

---

## Technical Requirements

### Data Generation Logic

- **Member Data**: Realistic Australian names, email patterns, insurance statuses, join dates, premium amounts
- **Policy Data**: Insurance-specific policy types (Hospital, Extras, Combined), categories (Basic, Bronze, Silver, Gold), realistic premiums and excesses
- **Claims Data**: Healthcare claim types (Hospital, Dental, Optical), processing statuses, realistic amounts and dates
- **Provider Data**: Healthcare provider types, Australian locations, contact information

### Code Generation Templates

- **Table Component**: Includes filtering, state management, realistic column definitions
- **Form Component**: Input validation, controlled components, submission handling
- **Dashboard Component**: Grid layout, summary cards, data visualization placeholders
- **Generic Component**: Flexible template for custom requirements

### Use Case Mappings

Pre-define intelligent mappings for common patterns:

- "table with filters" → Table, Select, Input, Button
- "dashboard" → Card, Grid, Chart, Stats
- "form" → Input, Select, Checkbox, Button, TextArea
- "search interface" → Input, Button, Card, List
- "navigation" → Menu, Breadcrumb, Tabs

---

## API Enhancements

### New Endpoints

#### 1. Generate Placeholder Data

```
POST /tools/generatePlaceholderData/invoke
```

**Purpose**: Create realistic test data for prototypes
**Response**: JSON array of data records

#### 2. Generate Prototype Code

```
POST /tools/generatePrototypeCode/invoke
```

**Purpose**: Generate complete React component code
**Response**: Ready-to-use React component as string

#### 3. Search Components by Use Case

```
POST /tools/searchComponentsByUseCase/invoke
```

**Purpose**: Find relevant components for specific UI patterns
**Response**: Ranked list of component suggestions

### Updated Tools Manifest

Extend existing manifest to include new tools with proper JSON schemas for validation.

---

## Implementation Plan

### Phase 1: Core Data Generation (Week 1)

- [ ] Add placeholder data generation functions
- [ ] Implement `generatePlaceholderData` endpoint
- [ ] Create realistic data templates for all 4 data types
- [ ] Add data generation tests

### Phase 2: Code Generation (Week 2)

- [ ] Build React code templates for common patterns
- [ ] Implement `generatePrototypeCode` endpoint
- [ ] Integrate with existing component scraper
- [ ] Add code generation logic for tables, forms, dashboards

### Phase 3: Smart Search (Week 3)

- [ ] Create use case mapping system
- [ ] Implement `searchComponentsByUseCase` endpoint
- [ ] Add keyword matching and relevance scoring
- [ ] Test with various UI patterns

### Phase 4: Integration & Testing (Week 4)

- [ ] Update tools manifest
- [ ] Add comprehensive error handling
- [ ] Update Docker configuration
- [ ] Test with Cursor integration
- [ ] Update documentation

---

## Success Metrics

### Functionality Metrics

- [ ] All 3 new tools working correctly
- [ ] Generates realistic data for all 4 types
- [ ] Produces working React code for common patterns
- [ ] Suggests relevant components for 15+ use cases

### Integration Metrics

- [ ] Seamless integration with existing MCP architecture
- [ ] Maintains current caching performance
- [ ] Docker build/run succeeds without issues
- [ ] Cursor can successfully call all new tools

### User Experience Metrics

- [ ] Generated code requires minimal manual editing
- [ ] Placeholder data looks realistic and contextually appropriate
- [ ] Component suggestions are relevant and helpful
- [ ] Total time from idea to working prototype < 2 minutes

---

## Testing Strategy

### Unit Tests

- Data generation functions produce valid, realistic data
- Code generation creates syntactically correct React
- Use case search returns relevant components

### Integration Tests

- All endpoints respond correctly to valid inputs
- Error handling works for invalid inputs
- Caching system works with new endpoints

### End-to-End Tests

- Cursor can successfully call new tools
- Generated code runs in React environment
- Prototyping workflow functions smoothly

---

## Deployment

### Docker Updates

- No changes to existing Dockerfile/docker-compose
- New dependencies automatically installed
- Maintains existing port/health check configuration

### Configuration

- Add environment variables for data generation settings
- Maintain existing cache configuration
- Keep current logging and error handling

### Rollback Plan

- New endpoints are additive, won't break existing functionality
- Can disable new tools via feature flags if needed
- Existing tools remain unchanged

---

## Success Definition

The enhanced MeshMCP should enable this workflow:

1. User describes UI concept to Cursor
2. Cursor queries MCP for relevant components
3. Cursor generates placeholder data via MCP
4. Cursor creates React prototype code via MCP
5. User sees working prototype in < 2 minutes

**Key Success Indicator**: Complete "sketch to working prototype" workflow without manual component lookup or data creation.
