#!/usr/bin/env python3

"""
Script to convert model_comparison_results.json into formatted Markdown report
"""

import json
import sys
from typing import Dict, List, Any
from datetime import datetime

def load_results(json_file: str = "model_comparison_results.json") -> Dict[str, Any]:
    """Load the JSON results file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{json_file}': {e}")
        sys.exit(1)

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for better readability."""
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp

def generate_executive_summary(data: Dict[str, Any]) -> str:
    """Generate executive summary section."""
    total_models = data.get("total_models_tested", 0)
    failed_models = data.get("failed_models", 0)
    sample_size = data.get("sample_size", "all")
    
    # Calculate overall statistics
    all_results = data.get("results", [])
    valid_results = [r for r in all_results if r.get("total_tests", 0) > 0]
    
    if not valid_results:
        return "## 📊 Executive Summary\n\nNo valid test results found.\n"
    
    total_tests = sum(r.get("total_tests", 0) for r in valid_results)
    total_passed = sum(r.get("passed", 0) for r in valid_results)
    overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    best_model = max(valid_results, key=lambda x: (x.get("passed", 0) / x.get("total_tests", 1), -x.get("avg_response_time", float('inf'))))
    
    summary = f"""## 📊 Executive Summary

**Test Overview:**
- **Date**: {format_timestamp(data.get('timestamp', 'Unknown'))}
- **Models Tested**: {total_models} successful, {failed_models} failed
- **Sample Size**: {sample_size} test(s) per category
- **Total Test Executions**: {total_tests}
- **Overall Success Rate**: {overall_success_rate:.1f}%

**Key Results:**
- **🏆 Best Performing Model**: `{best_model.get('model', 'Unknown')}` ({best_model.get('passed', 0)}/{best_model.get('total_tests', 0)} passed, {best_model.get('avg_response_time', 0):.2f}s avg)
- **⚡ Fastest Model**: `{min(valid_results, key=lambda x: x.get('avg_response_time', float('inf'))).get('model', 'Unknown')}` ({min(r.get('avg_response_time', float('inf')) for r in valid_results):.2f}s avg)
- **🎯 Most Reliable**: Models with highest success rates perform consistently across categories

"""
    return summary

def generate_model_performance_table(data: Dict[str, Any]) -> str:
    """Generate model performance comparison table."""
    results = data.get("results", [])
    valid_results = [r for r in results if r.get("total_tests", 0) > 0]
    
    if not valid_results:
        return "## 🤖 Model Performance\n\nNo valid results to display.\n"
    
    # Sort by success rate, then by speed
    valid_results.sort(key=lambda x: (x.get("passed", 0) / x.get("total_tests", 1), -x.get("avg_response_time", float('inf'))), reverse=True)
    
    table = """## 🤖 Model Performance Comparison

| Rank | Model | Tests | ✅ Passed | ❌ Failed | ⚠️ Errors | Success Rate | Avg Time | Tools/Test |
|------|-------|-------|-----------|-----------|-----------|--------------|----------|------------|
"""
    
    for i, result in enumerate(valid_results, 1):
        model = result.get("model", "Unknown")
        total_tests = result.get("total_tests", 0)
        passed = result.get("passed", 0)
        failed = result.get("failed", 0)
        errors = result.get("errors", 0)
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        avg_time = result.get("avg_response_time", 0)
        
        # Calculate average tools per test
        details = result.get("details", [])
        avg_tools = sum(d.get("tool_count", 0) for d in details) / len(details) if details else 0
        
        # Add medal emoji for top 3
        rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, str(i))
        
        table += f"| {rank_emoji} | `{model}` | {total_tests} | {passed} | {failed} | {errors} | {success_rate:.1f}% | {avg_time:.2f}s | {avg_tools:.1f} |\n"
    
    return table + "\n"

def generate_failure_analysis(data: Dict[str, Any]) -> str:
    """Generate question failure analysis section."""
    failure_analysis = data.get("question_failure_analysis", [])
    
    if not failure_analysis:
        return "## ❌ Question Failure Analysis\n\nNo failure analysis data available.\n"
    
    section = """## ❌ Question Failure Analysis

This section identifies which questions are most challenging across all models.

| Failures | Total Tests | Failure Rate | Question |
|----------|-------------|--------------|----------|
"""
    
    for item in failure_analysis:
        question = item.get("question", "Unknown")
        failures = item.get("failures", 0)
        total = item.get("total", 0)
        failure_rate = item.get("failure_rate", 0)
        
        # Truncate long questions
        question_display = question[:60] + "..." if len(question) > 63 else question
        
        # Add status emoji based on failure rate
        status_emoji = "🚨" if failure_rate >= 50 else "⚠️" if failure_rate > 0 else "✅"
        
        section += f"| {failures} | {total} | {failure_rate:.1f}% | {status_emoji} {question_display} |\n"
    
    # Add insights
    most_problematic = [q for q in failure_analysis if q.get("failure_rate", 0) >= 50]
    most_reliable = [q for q in failure_analysis if q.get("failure_rate", 0) == 0]
    
    if most_problematic:
        section += f"\n### 🚨 Most Problematic Questions ({len(most_problematic)} questions with ≥50% failure rate)\n\n"
        for i, item in enumerate(most_problematic, 1):
            question = item.get("question", "Unknown")
            failures = item.get("failures", 0)
            total = item.get("total", 0)
            failure_rate = item.get("failure_rate", 0)
            section += f"{i}. **{question}**\n   - Failures: {failures}/{total} ({failure_rate:.1f}%)\n\n"
    
    if most_reliable:
        section += f"\n### ✅ Most Reliable Questions ({len(most_reliable)} questions with 0% failure rate)\n\n"
        for i, item in enumerate(most_reliable[:5], 1):  # Show top 5 reliable
            question = item.get("question", "Unknown")
            total = item.get("total", 0)
            section += f"{i}. **{question}** (Perfect success across {total} models)\n"
    
    return section + "\n"

def generate_category_breakdown(data: Dict[str, Any]) -> str:
    """Generate performance breakdown by question category."""
    results = data.get("results", [])
    valid_results = [r for r in results if r.get("total_tests", 0) > 0]
    
    if not valid_results:
        return "## 📋 Category Performance\n\nNo category data available.\n"
    
    # Collect category statistics
    categories = {}
    
    for result in valid_results:
        model = result.get("model", "Unknown")
        details = result.get("details", [])
        
        for detail in details:
            category = detail.get("category", "unknown")
            status = detail.get("status", "UNKNOWN")
            response_time = detail.get("response_time", 0)
            
            if category not in categories:
                categories[category] = {}
            
            if model not in categories[category]:
                categories[category][model] = {
                    "passed": 0,
                    "total": 0,
                    "times": []
                }
            
            categories[category][model]["total"] += 1
            categories[category][model]["times"].append(response_time)
            
            if status == "PASSED":
                categories[category][model]["passed"] += 1
    
    section = "## 📋 Performance by Category\n\n"
    
    category_order = ["basics", "intermediates", "advanced", "complex"]
    category_names = {
        "basics": "🟢 Basic Queries",
        "intermediates": "🟡 Intermediate Queries", 
        "advanced": "🟠 Advanced Queries",
        "complex": "🔴 Complex Queries"
    }
    
    for category in category_order:
        if category not in categories:
            continue
            
        section += f"### {category_names.get(category, category.title())}\n\n"
        section += "| Model | Success Rate | Avg Response Time | Performance |\n"
        section += "|-------|--------------|-------------------|-------------|\n"
        
        # Sort models by success rate for this category
        category_data = categories[category]
        model_stats = []
        
        for model, stats in category_data.items():
            success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            avg_time = sum(stats["times"]) / len(stats["times"]) if stats["times"] else 0
            model_stats.append((model, success_rate, avg_time, stats["passed"], stats["total"]))
        
        model_stats.sort(key=lambda x: (x[1], -x[2]), reverse=True)  # Sort by success rate, then by speed
        
        for model, success_rate, avg_time, passed, total in model_stats:
            # Performance indicator
            if success_rate >= 90:
                perf_indicator = "🟢 Excellent"
            elif success_rate >= 70:
                perf_indicator = "🟡 Good"
            elif success_rate >= 50:
                perf_indicator = "🟠 Fair"
            else:
                perf_indicator = "🔴 Poor"
            
            section += f"| `{model}` | {passed}/{total} ({success_rate:.1f}%) | {avg_time:.2f}s | {perf_indicator} |\n"
        
        section += "\n"
    
    return section

def generate_detailed_insights(data: Dict[str, Any]) -> str:
    """Generate detailed insights and recommendations."""
    results = data.get("results", [])
    valid_results = [r for r in results if r.get("total_tests", 0) > 0]
    failure_analysis = data.get("question_failure_analysis", [])
    
    if not valid_results:
        return "## 💡 Insights & Recommendations\n\nInsufficient data for analysis.\n"
    
    # Best performing model
    best_model = max(valid_results, key=lambda x: (x.get("passed", 0) / x.get("total_tests", 1), -x.get("avg_response_time", float('inf'))))
    
    # Fastest model
    fastest_model = min(valid_results, key=lambda x: x.get("avg_response_time", float('inf')))
    
    # Most problematic questions
    problematic_questions = [q for q in failure_analysis if q.get("failure_rate", 0) >= 50]
    
    # Most reliable questions
    reliable_questions = [q for q in failure_analysis if q.get("failure_rate", 0) == 0]
    
    section = """## 💡 Insights & Recommendations

### 🎯 Model Selection Guide

"""
    
    # Production recommendations
    section += f"**For Production Systems:**\n"
    section += f"- **Recommended**: `{best_model.get('model', 'Unknown')}` - Best balance of accuracy ({best_model.get('passed', 0)}/{best_model.get('total_tests', 0)} passed) and reliability\n"
    section += f"- **Speed-Critical**: `{fastest_model.get('model', 'Unknown')}` - Fastest responses ({fastest_model.get('avg_response_time', 0):.2f}s average)\n\n"
    
    # Query optimization
    if problematic_questions:
        section += "**Query Optimization:**\n"
        section += f"- Avoid or rephrase {len(problematic_questions)} problematic question pattern(s)\n"
        for q in problematic_questions[:2]:  # Show top 2 problematic
            question_short = q.get("question", "")[:50] + "..." if len(q.get("question", "")) > 50 else q.get("question", "")
            section += f"  - \"{question_short}\" ({q.get('failure_rate', 0):.0f}% failure rate)\n"
        section += "\n"
    
    if reliable_questions:
        section += "**Reliable Query Patterns:**\n"
        section += f"- {len(reliable_questions)} question types show 100% success across all models\n"
        for q in reliable_questions[:3]:  # Show top 3 reliable
            question_short = q.get("question", "")[:50] + "..." if len(q.get("question", "")) > 50 else q.get("question", "")
            section += f"  - \"{question_short}\"\n"
        section += "\n"
    
    # Performance patterns
    section += "### 📈 Performance Patterns\n\n"
    
    # Calculate average success rates by model
    model_performances = []
    for result in valid_results:
        model = result.get("model", "Unknown")
        success_rate = (result.get("passed", 0) / result.get("total_tests", 1)) * 100
        avg_time = result.get("avg_response_time", 0)
        model_performances.append((model, success_rate, avg_time))
    
    # Group by performance tiers
    excellent = [m for m in model_performances if m[1] >= 90]
    good = [m for m in model_performances if 70 <= m[1] < 90]
    fair = [m for m in model_performances if 50 <= m[1] < 70]
    poor = [m for m in model_performances if m[1] < 50]
    
    if excellent:
        section += f"**🟢 Excellent Performers (≥90% success):** {', '.join([f'`{m[0]}`' for m in excellent])}\n"
    if good:
        section += f"**🟡 Good Performers (70-89% success):** {', '.join([f'`{m[0]}`' for m in good])}\n"
    if fair:
        section += f"**🟠 Fair Performers (50-69% success):** {', '.join([f'`{m[0]}`' for m in fair])}\n"
    if poor:
        section += f"**🔴 Needs Improvement (<50% success):** {', '.join([f'`{m[0]}`' for m in poor])}\n"
    
    section += "\n### 🚀 Next Steps\n\n"
    section += "1. **Deploy** the recommended model for your use case\n"
    section += "2. **Monitor** question success rates in production\n"
    section += "3. **Optimize** or avoid problematic question patterns\n"
    section += "4. **Test** new questions with sample runs before deployment\n"
    section += "5. **Re-evaluate** model performance periodically\n\n"
    
    return section

def generate_technical_appendix(data: Dict[str, Any]) -> str:
    """Generate technical appendix with raw data summary."""
    results = data.get("results", [])
    
    section = """## 📊 Technical Appendix

### Test Configuration
"""
    
    section += f"- **Timestamp**: {data.get('timestamp', 'Unknown')}\n"
    section += f"- **Sample Size**: {data.get('sample_size', 'all')} test(s) per category\n"
    section += f"- **Total Models**: {data.get('total_models_tested', 0)} tested, {data.get('failed_models', 0)} failed\n"
    section += f"- **Data Export**: `model_comparison_results.json`\n\n"
    
    # Tool usage statistics
    all_tools_used = set()
    tool_usage_count = {}
    
    for result in results:
        for detail in result.get("details", []):
            for tool in detail.get("actual_tools", []):
                all_tools_used.add(tool)
                tool_usage_count[tool] = tool_usage_count.get(tool, 0) + 1
    
    if tool_usage_count:
        section += "### 🔧 Tool Usage Statistics\n\n"
        sorted_tools = sorted(tool_usage_count.items(), key=lambda x: x[1], reverse=True)
        
        for tool, count in sorted_tools:
            section += f"- `{tool}`: {count} executions\n"
        
        section += f"\n**Total Unique Tools Used**: {len(all_tools_used)}\n\n"
    
    # Response time statistics
    all_times = []
    for result in results:
        for detail in result.get("details", []):
            response_time = detail.get("response_time", 0)
            if response_time > 0:
                all_times.append(response_time)
    
    if all_times:
        section += "### ⏱️ Response Time Analysis\n\n"
        section += f"- **Fastest Response**: {min(all_times):.2f}s\n"
        section += f"- **Slowest Response**: {max(all_times):.2f}s\n"
        section += f"- **Average Response**: {sum(all_times)/len(all_times):.2f}s\n"
        section += f"- **Total Test Executions**: {len(all_times)}\n\n"
    
    return section

def main():
    """Main function to generate the Markdown report."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert model comparison JSON to Markdown report")
    parser.add_argument('--input', '-i', default='model_comparison_results.json',
                       help='Input JSON file (default: model_comparison_results.json)')
    parser.add_argument('--output', '-o', default='model_comparison_report.md',
                       help='Output Markdown file (default: model_comparison_report.md)')
    
    args = parser.parse_args()
    
    # Load data
    print(f"📖 Loading data from {args.input}...")
    data = load_results(args.input)
    
    # Generate report sections
    print("📝 Generating Markdown report...")
    
    report = f"""# 🚀 MCP Model Comparison Report

*Generated from test results on {format_timestamp(data.get('timestamp', 'Unknown'))}*

---

"""
    
    report += generate_executive_summary(data)
    report += generate_model_performance_table(data)
    report += generate_failure_analysis(data)
    report += generate_category_breakdown(data)
    report += generate_detailed_insights(data)
    report += generate_technical_appendix(data)
    
    report += """---

*This report was automatically generated from MCP tool testing results. For questions or issues, please review the source data in the JSON file.*
"""
    
    # Write to file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ Report saved to {args.output}")
        print(f"📄 Report contains {len(report.split())} words and {len(report.splitlines())} lines")
    except Exception as e:
        print(f"❌ Error writing to {args.output}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()