# Getting Started

This guide will help you set up and use the MCP Car Database System.

## Prerequisites

### Required Software
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Git for cloning the repository

### Install Ollama

=== "macOS"
    ```bash
    brew install ollama
    ```

=== "Linux"
    ```bash
    curl -fsSL https://ollama.ai/install.sh | sh
    ```

=== "Windows"
    Download from [https://ollama.ai/](https://ollama.ai/)

### Install Required Models

```bash
ollama pull llama3.2:latest
ollama pull qwen3-coder:480b-cloud
ollama pull gpt-oss:20b-cloud
ollama pull gemma:2b
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/pcumino/desafio_mcp
cd desafio_mcp
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start Ollama service:**
```bash
ollama serve
```

4. **Generate sample data:**
```bash
python dataFaker.py 1000
```

5. **Verify installation:**
```bash
python MCPserver.py --help
python OllamaClient.py --help
```

## First Steps

### 1. Start the MCP Server

In one terminal:
```bash
python MCPserver.py
```

### 2. Run Interactive Client

In another terminal:
```bash
python OllamaClient.py --interactive
```

### 3. Try Your First Query

```
> How many cars are in the database?
> What Toyota models are available?
> Show me hybrid cars with low mileage
```

## Validation

If everything is working correctly, you should see:

- ✅ MCP server starts without errors
- ✅ Client connects successfully
- ✅ Sample queries return results
- ✅ Data file exists at `data/cars.csv`

## What's Next?

- Explore [Components](components.md) to understand the system
- Try [Usage Examples](examples.md) for common tasks
- Check [Troubleshooting](troubleshooting.md) if you encounter issues