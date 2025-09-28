# 🚀 MCP Model Comparison Report

*Generated from test results on September 27, 2025 at 10:46 PM*

---

## 📊 Executive Summary

**Test Overview:**
- **Date**: September 27, 2025 at 10:46 PM
- **Models Tested**: 4 successful, 0 failed
- **Sample Size**: None test(s) per category
- **Total Test Executions**: 80
- **Overall Success Rate**: 51.2%

**Key Results:**
- **🏆 Best Performing Model**: `llama3.2:latest` (15/20 passed, 12.59s avg)
- **⚡ Fastest Model**: `gemma:2b` (0.06s avg)
- **🎯 Most Reliable**: Models with highest success rates perform consistently across categories

## 🤖 Model Performance Comparison

| Rank | Model | Tests | ✅ Passed | ❌ Failed | ⚠️ Errors | Success Rate | Avg Time | Tools/Test |
|------|-------|-------|-----------|-----------|-----------|--------------|----------|------------|
| 🥇 | `llama3.2:latest` | 20 | 15 | 5 | 0 | 75.0% | 12.59s | 1.6 |
| 🥈 | `qwen3-coder:480b-cloud` | 20 | 14 | 4 | 2 | 70.0% | 6.88s | 1.1 |
| 🥉 | `gpt-oss:20b-cloud` | 20 | 12 | 6 | 2 | 60.0% | 14.16s | 0.9 |
| 4 | `gemma:2b` | 20 | 0 | 0 | 20 | 0.0% | 0.06s | 0.0 |

## ❌ Question Failure Analysis

This section identifies which questions are most challenging across all models.

| Failures | Total Tests | Failure Rate | Question |
|----------|-------------|--------------|----------|
| 4 | 4 | 100.0% | 🚨 Existe algum carro com motor 1.0 no banco de dados? |
| 4 | 4 | 100.0% | 🚨 Liste todos os modelos de carros que usam combustível híbrido. |
| 3 | 4 | 75.0% | 🚨 Show me all cars manufactured after 2020 that use hybrid fue... |
| 3 | 4 | 75.0% | 🚨 List all models with manual transmission, grouped by brand. ... |
| 3 | 4 | 75.0% | 🚨 List all cars added in 2022. Then, sort them by engine size ... |
| 2 | 4 | 50.0% | 🚨 Quantos carros da marca Chevrolet existem no banco de dados? |
| 2 | 4 | 50.0% | 🚨 Qual é a quilometragem do Hyundai Elantra 2017? |
| 2 | 4 | 50.0% | 🚨 Qual foi a data de adição mais recente no banco? |
| 2 | 4 | 50.0% | 🚨 Quais veículos possuem apenas 2 portas? |
| 2 | 4 | 50.0% | 🚨 Find me all Toyota cars with low mileage lower than 38576 ki... |
| 2 | 4 | 50.0% | 🚨 Find all vehicles with more than 4 doors. Then, among them, ... |
| 2 | 4 | 50.0% | 🚨 Provide the total number of cars by fuel type. Afterward, sh... |
| 1 | 4 | 25.0% | ⚠️ Qual é o carro mais antigo registrado e de que ano ele é? |
| 1 | 4 | 25.0% | ⚠️ Quais são as cores disponíveis entre os carros cadastrados? |
| 1 | 4 | 25.0% | ⚠️ Quais carros têm transmissão manual e ainda estão na condiçã... |
| 1 | 4 | 25.0% | ⚠️ Liste todos os carros cadastrados com condição "usado regular". |
| 1 | 4 | 25.0% | ⚠️ What are the available car brands in the dataset? |
| 1 | 4 | 25.0% | ⚠️ List the car brands sorted by the number of cars of each branch |
| 1 | 4 | 25.0% | ⚠️ Provide me a summary of the current available cars |
| 1 | 4 | 25.0% | ⚠️ Encontre todos os carros Toyota com quilometragem inferior a... |

### 🚨 Most Problematic Questions (12 questions with ≥50% failure rate)

1. **Existe algum carro com motor 1.0 no banco de dados?**
   - Failures: 4/4 (100.0%)

2. **Liste todos os modelos de carros que usam combustível híbrido.**
   - Failures: 4/4 (100.0%)

3. **Show me all cars manufactured after 2020 that use hybrid fuel. Then, count how many are in "seminovo" condition.**
   - Failures: 3/4 (75.0%)

4. **List all models with manual transmission, grouped by brand. After that, tell me which group has the highest mileage average.**
   - Failures: 3/4 (75.0%)

5. **List all cars added in 2022. Then, sort them by engine size in descending order.**
   - Failures: 3/4 (75.0%)

6. **Quantos carros da marca Chevrolet existem no banco de dados?**
   - Failures: 2/4 (50.0%)

7. **Qual é a quilometragem do Hyundai Elantra 2017?**
   - Failures: 2/4 (50.0%)

8. **Qual foi a data de adição mais recente no banco?**
   - Failures: 2/4 (50.0%)

9. **Quais veículos possuem apenas 2 portas?**
   - Failures: 2/4 (50.0%)

10. **Find me all Toyota cars with low mileage lower than 38576 kilometers. Then, list all available models from the brand Ford.**
   - Failures: 2/4 (50.0%)

11. **Find all vehicles with more than 4 doors. Then, among them, give me the one with the lowest mileage.**
   - Failures: 2/4 (50.0%)

12. **Provide the total number of cars by fuel type. Afterward, show me which color is most frequent in the dataset.**
   - Failures: 2/4 (50.0%)


## 📋 Performance by Category

### 🟢 Basic Queries

| Model | Success Rate | Avg Response Time | Performance |
|-------|--------------|-------------------|-------------|
| `gpt-oss:20b-cloud` | 5/6 (83.3%) | 2.77s | 🟡 Good |
| `llama3.2:latest` | 4/6 (66.7%) | 11.14s | 🟠 Fair |
| `qwen3-coder:480b-cloud` | 3/6 (50.0%) | 6.57s | 🟠 Fair |
| `gemma:2b` | 0/6 (0.0%) | 0.07s | 🔴 Poor |

### 🟡 Intermediate Queries

| Model | Success Rate | Avg Response Time | Performance |
|-------|--------------|-------------------|-------------|
| `qwen3-coder:480b-cloud` | 4/5 (80.0%) | 7.66s | 🟡 Good |
| `gpt-oss:20b-cloud` | 4/5 (80.0%) | 10.90s | 🟡 Good |
| `llama3.2:latest` | 3/5 (60.0%) | 14.00s | 🟠 Fair |
| `gemma:2b` | 0/5 (0.0%) | 0.06s | 🔴 Poor |

### 🟠 Advanced Queries

| Model | Success Rate | Avg Response Time | Performance |
|-------|--------------|-------------------|-------------|
| `gpt-oss:20b-cloud` | 2/2 (100.0%) | 3.23s | 🟢 Excellent |
| `qwen3-coder:480b-cloud` | 2/2 (100.0%) | 5.60s | 🟢 Excellent |
| `llama3.2:latest` | 2/2 (100.0%) | 8.63s | 🟢 Excellent |
| `gemma:2b` | 0/2 (0.0%) | 0.06s | 🔴 Poor |

### 🔴 Complex Queries

| Model | Success Rate | Avg Response Time | Performance |
|-------|--------------|-------------------|-------------|
| `llama3.2:latest` | 6/7 (85.7%) | 13.97s | 🟡 Good |
| `qwen3-coder:480b-cloud` | 5/7 (71.4%) | 6.94s | 🟡 Good |
| `gpt-oss:20b-cloud` | 1/7 (14.3%) | 29.38s | 🔴 Poor |
| `gemma:2b` | 0/7 (0.0%) | 0.06s | 🔴 Poor |

## 💡 Insights & Recommendations

### 🎯 Model Selection Guide

**For Production Systems:**
- **Recommended**: `llama3.2:latest` - Best balance of accuracy (15/20 passed) and reliability
- **Speed-Critical**: `gemma:2b` - Fastest responses (0.06s average)

**Query Optimization:**
- Avoid or rephrase 12 problematic question pattern(s)
  - "Existe algum carro com motor 1.0 no banco de dados..." (100% failure rate)
  - "Liste todos os modelos de carros que usam combustí..." (100% failure rate)

### 📈 Performance Patterns

**🟡 Good Performers (70-89% success):** `qwen3-coder:480b-cloud`, `llama3.2:latest`
**🟠 Fair Performers (50-69% success):** `gpt-oss:20b-cloud`
**🔴 Needs Improvement (<50% success):** `gemma:2b`

### 🚀 Next Steps

1. **Deploy** the recommended model for your use case
2. **Monitor** question success rates in production
3. **Optimize** or avoid problematic question patterns
4. **Test** new questions with sample runs before deployment
5. **Re-evaluate** model performance periodically

## 📊 Technical Appendix

### Test Configuration
- **Timestamp**: 2025-09-27 22:46:19
- **Sample Size**: None test(s) per category
- **Total Models**: 4 tested, 0 failed
- **Data Export**: `model_comparison_results.json`

### 🔧 Tool Usage Statistics

- `filter_cars_by_criteria`: 23 executions
- `get_cars_sorted_by`: 13 executions
- `get_available_values`: 11 executions
- `get_cars_count_by_brand`: 7 executions
- `get_car_statistics`: 5 executions
- `get_grouped_statistics`: 5 executions
- `check_value_exists`: 3 executions
- `get_column_value_distribution`: 3 executions
- `filter_cars_by_date_range`: 1 executions
- `search_cars_by_keyword`: 1 executions

**Total Unique Tools Used**: 10

### ⏱️ Response Time Analysis

- **Fastest Response**: 0.05s
- **Slowest Response**: 55.69s
- **Average Response**: 8.42s
- **Total Test Executions**: 80

---

*This report was automatically generated from MCP tool testing results. For questions or issues, please review the source data in the JSON file.*
