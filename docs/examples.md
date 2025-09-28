# Usage Examples

This page provides practical examples of using the MCP Car Database System for various tasks.

## Complete Workflow Example

Here's a step-by-step example of using the entire system:

### 1. Generate Test Data
```bash
python dataFaker.py 2000 --output data/cars.csv
```

### 2. Start MCP Server (Terminal 1)
```bash
python MCPserver.py
```

### 3. Run Interactive Client (Terminal 2)
```bash
python OllamaClient.py --interactive
```

### 4. Example Queries

Try these queries in the interactive client:

#### Simple Queries
```
> How many Chevrolet cars are in the database?
> What colors are available for cars?
> Show me the oldest car in the database
> List all available car brands
```

#### Intermediate Queries
```
> Show me all hybrid cars
> Find cars with manual transmission
> What Toyota models are available?
> Show cars from 2020 onwards
```

#### Advanced Queries
```
> Give me statistics about the car database
> Show the distribution of fuel types
> What's the average mileage by brand?
> List cars sorted by year, newest first
```

#### Complex Queries
```
> Find all Toyota cars with mileage under 50,000km, then show me Ford models
> List cars by fuel type distribution and show the most common color
> Show me new condition cars under 30,000km, then count them by brand
```

### 5. Run Performance Comparison
```bash
python test_questions_tools.py --compare --sample 3
```

### 6. Generate Analysis Report
```bash
python json_to_markdown.py --input model_comparison_results.json --output performance_report.md
```

## Sample Questions and Expected Tools

| Question | Expected Tools | Category |
|----------|---------------|----------|
| "How many Toyota cars exist?" | `get_cars_count_by_brand` | Basic |
| "Show hybrid fuel cars" | `filter_cars_by_criteria` | Intermediate |
| "Dataset summary please" | `get_car_statistics` | Advanced |
| "Toyota cars under 50k km, then Ford models" | `filter_cars_by_criteria` (2x) | Complex |

## Batch Processing Example

Create a file with queries and process them:

```python
# queries.txt
How many cars are in the database?
Show me all Toyota cars
What's the most common fuel type?
List cars by condition
```

```bash
python OllamaClient.py --batch queries.txt --output results.md
```

## Custom Model Usage

### Using Different Models

```bash
# Use coding-specialized model
python OllamaClient.py --model qwen3-coder:480b-cloud --interactive

# Use lightweight model
python OllamaClient.py --model gemma:2b --interactive
```

### Programmatic Usage

```python
import asyncio
from OllamaClient import OllamaClient

async def main():
    async with OllamaClient(model="llama3.2:latest") as client:
        await client.connect_to_server("MCPserver.py")
        
        # Simple query
        response = await client.process_query("How many cars are there?")
        print(response)
        
        # Complex query
        response = await client.process_query(
            "Find Toyota cars with low mileage and show their colors"
        )
        print(response)

asyncio.run(main())
```

## Testing Examples

### Single Model Testing
```bash
# Test specific model
python test_questions_tools.py --model llama3.2

# Test with debug output
python test_questions_tools.py --model llama3.2 --debug
```

### Multi-Model Comparison
```bash
# Full comparison (takes longer)
python test_questions_tools.py --compare

# Quick comparison with samples
python test_questions_tools.py --compare --sample 2

# Compare specific categories
python test_questions_tools.py --compare --category basic intermediate
```

## Data Generation Examples

### Basic Generation
```bash
# Standard dataset
python dataFaker.py 1000

# Large dataset
python dataFaker.py 10000 --output large_cars.csv
```

### Custom Configuration
```python
# In dataFaker.py, modify these variables:
SAMPLE_SIZE = 5000
OUTPUT_FILE = "custom_cars.csv"
LANGUAGE = "pt_BR"  # Portuguese Brazilian
```

## Web UI Testing

Test individual MCP tools using the web interface:

```bash
uv run mcp dev MCPserver.py
```

Then open your browser and test tools like:
- `filter_cars_by_criteria` with `brand="toyota"` and `engine=2.0`
- `get_car_statistics` (no parameters needed)
- `search_cars_by_keyword` with `keyword="corolla"`

## Performance Optimization Examples

### Faster Development Testing
```bash
# Use smaller dataset
python dataFaker.py 100 --output test_cars.csv

# Use faster model for development
python OllamaClient.py --model gemma:2b --interactive

# Limited sample testing
python test_questions_tools.py --model gemma:2b --sample 1
```

### Production Setup
```bash
# Larger dataset for realistic testing
python dataFaker.py 10000

# Use best performing model
python OllamaClient.py --model llama3.2:latest --interactive

# Full performance analysis
python test_questions_tools.py --compare
```

## Common Use Cases

### 1. Car Dealership Inventory
```
> Show me all available Volkswagen cars
> Find cars under R$ 50,000 with low mileage
> What's our most popular car model?
> Show automatic transmission cars only
```

### 2. Market Research
```
> What's the distribution of fuel types in our database?
> Show average mileage by car brand
> Which brands have the newest cars?
> Compare manual vs automatic transmission popularity
```

### 3. AI Model Evaluation
```bash
# Compare model performance on car data tasks
python test_questions_tools.py --compare

# Generate detailed performance report
python json_to_markdown.py --input model_comparison_results.json --output model_analysis.md
```

### 4. Educational/Learning
```
> Explain the difference between FLEX and HÍBRIDO fuel types
> How does the MCP protocol work in this system?
> Show me examples of complex database queries
```

## Troubleshooting Examples

### Debug Mode
```python
# Enable debug output
response = await client.process_query(question, enable_debug=True)
```

### Connection Issues
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
ollama serve

# Test individual components
python MCPserver.py --test
```

### Performance Issues
```bash
# Use lighter model
python OllamaClient.py --model gemma:2b

# Reduce dataset size
python dataFaker.py 500

# Test with minimal sample
python test_questions_tools.py --sample 1
```

These examples should give you a solid foundation for using the MCP Car Database System effectively. For more specific use cases or advanced configurations, refer to the individual component documentation.