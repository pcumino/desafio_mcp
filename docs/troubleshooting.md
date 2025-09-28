# Troubleshooting

Common issues and solutions for the MCP Car Database System.

## Installation Issues

### Python Dependencies
**Problem**: Dependencies fail to install
```bash
pip install -r requirements.txt
# ERROR: Could not install packages...
```

**Solutions**:
```bash
# Update pip first
pip install --upgrade pip

# Use virtual environment
python -m venv mcp-env
source mcp-env/bin/activate  # Windows: mcp-env\Scripts\activate
pip install -r requirements.txt

# Install with verbose output for debugging
pip install -v -r requirements.txt
```

### Ollama Installation
**Problem**: Ollama not found or won't start

**Solutions**:
```bash
# Check if Ollama is installed
ollama --version

# Install Ollama (macOS)
brew install ollama

# Install Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

## Runtime Issues

### MCP Server Won't Start
**Problem**: `python MCPserver.py` fails

**Common Causes & Solutions**:

1. **Missing data file**:
```bash
# Generate data first
python dataFaker.py 1000
# Check if file exists
ls -la data/cars.csv
```

2. **Python path issues**:
```bash
# Run from project root directory
cd desafio_mcp
python MCPserver.py
```

3. **Port conflicts**:
```bash
# Check for running processes
ps aux | grep MCPserver
# Kill if needed
pkill -f MCPserver.py
```

### Client Connection Issues
**Problem**: Client can't connect to MCP server

**Solutions**:
```bash
# Ensure server is running first
python MCPserver.py

# In another terminal, test client
python OllamaClient.py --interactive

# Check Ollama is running
ollama list
ollama serve  # If not running
```

### Ollama Model Issues
**Problem**: Model not found or won't load

**Solutions**:
```bash
# List available models
ollama list

# Pull missing models
ollama pull llama3.2:latest
ollama pull qwen3-coder:480b-cloud

# Test model directly
ollama run llama3.2:latest "Hello"

# Check available memory
free -h  # Linux
vm_stat  # macOS
```

## Performance Issues

### Slow Response Times
**Problem**: Queries take too long to execute

**Solutions**:

1. **Use lighter models**:
```bash
# Try smaller model
python OllamaClient.py --model gemma:2b --interactive
```

2. **Reduce dataset size**:
```bash
# Generate smaller dataset
python dataFaker.py 500 --output small_cars.csv
```

3. **Check system resources**:
```bash
# Monitor CPU/Memory usage
top  # Linux/macOS
htop  # If available
```

### Memory Issues
**Problem**: System runs out of memory

**Solutions**:
```bash
# Use smaller models
ollama pull gemma:2b

# Reduce dataset size
python dataFaker.py 100

# Close other applications
# Add swap space (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Data Issues

### Missing or Corrupted Data
**Problem**: Data file missing or corrupted

**Solutions**:
```bash
# Regenerate data
python dataFaker.py 1000

# Verify data integrity
python -c "import pandas as pd; print(pd.read_csv('data/cars.csv').shape)"

# Check data structure
head data/cars.csv
```

### Encoding Issues
**Problem**: Character encoding errors

**Solutions**:
```python
# In dataFaker.py, ensure UTF-8 encoding
df.to_csv('data/cars.csv', index=False, encoding='utf-8')

# When reading data
import pandas as pd
df = pd.read_csv('data/cars.csv', encoding='utf-8')
```

## Testing Issues

### Test Failures
**Problem**: Tests fail or give unexpected results

**Solutions**:
```bash
# Run single test for debugging
python test_questions_tools.py --model llama3.2 --sample 1 --debug

# Check individual components
python -c "from MCPserver import get_car_statistics; print(get_car_statistics())"

# Verify data quality
python -c "import pandas as pd; df=pd.read_csv('data/cars.csv'); print(df.info())"
```

### Model Comparison Issues
**Problem**: Model comparison fails or incomplete

**Solutions**:
```bash
# Test with smaller sample
python test_questions_tools.py --compare --sample 1

# Test individual models first
python test_questions_tools.py --model llama3.2
python test_questions_tools.py --model gemma:2b

# Check available models
ollama list
```

## Debug Mode

Enable debug mode for detailed troubleshooting:

### Client Debug Mode
```python
# In OllamaClient.py or when calling
response = await client.process_query(question, enable_debug=True)
```

### Server Debug Mode
```python
# Add debug prints in MCPserver.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### System Debug Info
```bash
# Check system info
python --version
ollama --version
pip list | grep -E "(pandas|fastmcp|faker)"

# Check file permissions
ls -la *.py
ls -la data/

# Check running processes
ps aux | grep -E "(ollama|python)"
```

## Common Error Messages

### "Connection refused"
```
ConnectionRefusedError: [Errno 61] Connection refused
```
**Solution**: Start Ollama service: `ollama serve`

### "Model not found"
```
Error: model 'llama3.2:latest' not found
```
**Solution**: Pull the model: `ollama pull llama3.2:latest`

### "No such file or directory: data/cars.csv"
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/cars.csv'
```
**Solution**: Generate data: `python dataFaker.py 1000`

### "Module not found"
```
ModuleNotFoundError: No module named 'fastmcp'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

### "Permission denied"
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Check file permissions or use virtual environment

## Performance Optimization

### For Development
```bash
# Use minimal setup
python dataFaker.py 100 --output test_cars.csv
python OllamaClient.py --model gemma:2b --interactive
python test_questions_tools.py --sample 1
```

### For Production
```bash
# Optimize system resources
# Close unnecessary applications
# Use SSD storage
# Ensure adequate RAM (16GB+ recommended)
# Use latest model versions
```

## Getting Help

### Check Logs
```bash
# Check system logs
tail -f /var/log/system.log  # macOS
journalctl -f  # Linux

# Check Ollama logs
ollama logs
```

### Diagnostic Commands
```bash
# System health check
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import pandas as pd
    print(f'Pandas: {pd.__version__}')
except ImportError:
    print('Pandas: Not installed')
"

# Network connectivity
ping ollama.ai
curl -I http://localhost:11434/  # Ollama API endpoint
```

### Report Issues
When reporting issues, include:
- Operating system and version
- Python version
- Error messages (full traceback)
- Steps to reproduce
- System specifications (RAM, CPU)
- Ollama version and available models

## Useful Commands Summary

```bash
# Quick health check
ollama list && python --version && ls data/cars.csv

# Restart everything
pkill -f "ollama\|MCPserver"
ollama serve &
python MCPserver.py &
python OllamaClient.py --interactive

# Clean restart
rm -rf data/cars.csv model_comparison_results.json test_results.json
python dataFaker.py 1000
python test_questions_tools.py --model llama3.2 --sample 1
```

If you're still experiencing issues after trying these solutions, consider creating a minimal reproduction case and checking the project's issue tracker or documentation for additional help.