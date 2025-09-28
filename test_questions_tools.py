#!/usr/bin/env python3

#===========================================================#
#File Name:			test_questions_tools.py
#Author:			Pedro Cumino
#Email:				pedro.cumino@gmail.com
#Creation Date:		Sat Sep 27 11:32:37 2025
#Last Modified:		Sat Sep 27 11:36:35 2025
#Description:
#Args:
#Usage:
#===========================================================#

import asyncio
from OllamaClient import OllamaClient
import json
import time
from typing import List, Dict, Any, Optional

def create_test_cases():
	"""Create test cases mapping questions to expected MCP tool calls."""
	
	test_cases = {
		"basics": [
			{
				"question": "Quantos carros da marca Chevrolet existem no banco de dados?",
				"expected_tools": [
					{"name": "get_cars_count_by_brand", "args": {}},
					# Alternative: {"name": "filter_cars_by_criteria", "args": {"brand": "Chevrolet"}}
				],
				"description": "Count Chevrolet cars using brand count tool"
			},
			{
				"question": "Existe algum carro com motor 1.0 no banco de dados?",
				"expected_tools": [
					{"name": "search_cars_by_keyword", "args": {"keyword": "1.0"}},
					# Alternative: {"name": "get_available_values", "args": {"column": "engine_size"}}
				],
				"description": "Search for 1.0 engine cars using keyword search"
			},
			{
				"question": "Qual é a quilometragem do Hyundai Elantra 2017?",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"brand": "Hyundai", "model": "Elantra", "year_min": 2017, "year_max": 2017}}
				],
				"description": "Find specific Hyundai Elantra 2017 and get mileage"
			},
			{
				"question": "Qual foi a data de adição mais recente no banco?",
				"expected_tools": [
					{"name": "get_cars_sorted_by", "args": {"sort_by": "date_added", "ascending": False, "limit": 1}}
				],
				"description": "Get most recent car by date_added"
			},
			{
				"question": "Qual é o carro mais antigo registrado e de que ano ele é?",
				"expected_tools": [
					{"name": "get_cars_sorted_by", "args": {"sort_by": "year", "ascending": True, "limit": 1}}
				],
				"description": "Get oldest car by year"
			},
			{
				"question": "Quais são as cores disponíveis entre os carros cadastrados?",
				"expected_tools": [
					{"name": "get_available_values", "args": {"column": "color"}}
				],
				"description": "Get all unique colors from dataset"
			}
		],
		
		"intermediates": [
			{
				"question": "Liste todos os modelos de carros que usam combustível híbrido.",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"fuel_type": "hybrid"}}
				],
				"description": "Filter cars by hybrid fuel type"
			},
			{
				"question": "Quais veículos possuem apenas 2 portas?",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"min_doors": 2, "max_doors": 2}}
				],
				"description": "Filter cars with exactly 2 doors"
			},
			{
				"question": "Quais carros têm transmissão manual e ainda estão na condição seminovo?",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"transmission": "Manual", "condition": "seminovo"}}
				],
				"description": "Filter manual transmission cars in seminovo condition"
			},
			{
				"question": "Liste todos os carros cadastrados com condição \"usado regular\".",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"condition": "usado regular"}}
				],
				"description": "Filter cars with 'usado regular' condition"
			},
			{
				"question": "What are the available car brands in the dataset?",
				"expected_tools": [
					{"name": "get_available_values", "args": {"column": "brand"}}
				],
				"description": "Get all unique car brands"
			}
		],
		
		"advanced": [
			{
				"question": "List the car brands sorted by the number of cars of each branch",
				"expected_tools": [
					{"name": "get_cars_count_by_brand", "args": {}}
				],
				"description": "Get brand counts (already sorted by count)"
			},
			{
				"question": "Provide me a summary of the current available cars",
				"expected_tools": [
					{"name": "get_car_statistics", "args": {}}
				],
				"description": "Get comprehensive dataset statistics"
			}
		],
		
		"complex": [
			{
				"question": "Find me all Toyota cars with low mileage lower than 38576 kilometers. Then, list all available models from the brand Ford.",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"brand": "Toyota", "max_mileage": 38576}},
					{"name": "filter_cars_by_criteria", "args": {"brand": "Ford"}}
				],
				"description": "Multi-step: Toyota low mileage + Ford models"
			},
			{
				"question": "Encontre todos os carros Toyota com quilometragem inferior a 38576 quilômetros. Em seguida, liste todos os modelos disponíveis da marca Ford.",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"brand": "Toyota", "max_mileage": 38576}},
					{"name": "filter_cars_by_criteria", "args": {"brand": "Ford"}}
				],
				"description": "Multi-step (Portuguese): Toyota low mileage + Ford models"
			},
			{
				"question": "Show me all cars manufactured after 2020 that use hybrid fuel. Then, count how many are in \"seminovo\" condition.",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"year_min": 2021, "fuel_type": "hybrid"}},
					{"name": "filter_cars_by_criteria", "args": {"year_min": 2021, "fuel_type": "hybrid", "condition": "seminovo"}}
				],
				"description": "Multi-step: Recent hybrid cars + count seminovo"
			},
			{
				"question": "List all models with manual transmission, grouped by brand. After that, tell me which group has the highest mileage average.",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"transmission": "Manual"}},
					{"name": "get_grouped_statistics", "args": {"group_by": "brand", "aggregate_field": "mileage", "operation": "mean"}}
				],
				"description": "Multi-step: Manual cars + grouped mileage statistics"
			},
			{
				"question": "Find all vehicles with more than 4 doors. Then, among them, give me the one with the lowest mileage.",
				"expected_tools": [
					{"name": "filter_cars_by_criteria", "args": {"min_doors": 5}},
					{"name": "get_cars_sorted_by", "args": {"sort_by": "mileage", "ascending": True, "limit": 1}}
				],
				"description": "Multi-step: 5+ doors + lowest mileage"
			},
			{
				"question": "Provide the total number of cars by fuel type. Afterward, show me which color is most frequent in the dataset.",
				"expected_tools": [
					{"name": "get_column_value_distribution", "args": {"column": "fuel"}},
					{"name": "get_column_value_distribution", "args": {"column": "color"}}
				],
				"description": "Multi-step: Fuel type distribution + color frequency"
			},
			{
				"question": "List all cars added in 2022. Then, sort them by engine size in descending order.",
				"expected_tools": [
					{"name": "filter_cars_by_date_range", "args": {"year": 2022}},
					{"name": "get_cars_sorted_by", "args": {"sort_by": "engine_size", "ascending": False}}
				],
				"description": "Multi-step: 2022 cars + sort by engine size"
			}
		]
	}
	
	return test_cases

async def run_single_model_test(model_name: str, test_cases: Dict, sample_size: Optional[int] = None):
	"""Run test suite for a single model."""
	print(f"\n🤖 Testing Model: {model_name}")
	print("=" * 60)
	
	results = {
		"model": model_name,
		"total_tests": 0,
		"passed": 0,
		"failed": 0,
		"errors": 0,
		"total_time": 0,
		"avg_response_time": 0,
		"details": []
	}
	
	start_time = time.time()
	
	async with OllamaClient(model=model_name) as client:
		await client.connect_to_server("MCPserver.py")
		
		for category, cases in test_cases.items():
			# If sample_size is specified, take a subset of test cases for faster comparison
			selected_cases = cases[:sample_size] if sample_size else cases
			
			for i, test_case in enumerate(selected_cases, 1):
				results["total_tests"] += 1
				question = test_case["question"]
				expected_tools = test_case["expected_tools"]
				description = test_case["description"]
				
				with open('test_questions_responses.md', 'a') as file:
					file.writelines([f'\n## Model: {model_name}\n'])
					file.writelines(f"\nCategory|Test case\n--|--\n{category}|{i}\n")
					file.writelines([f'\n### Query: {question}\n'])
				test_start_time = time.time()
				
				try:
					# Run the query
					response = await client.process_query(question, enable_debug=False)
					with open('test_questions_responses.md', 'a') as file:
						used_tools = '\n'.join([f'{i.function.name:<30}\t{i.function.arguments}' for i in client.last_used_tools])
						file.writelines(f'\n```json\n{used_tools}\n```\n')
						file.writelines([f'\n{response}\n\n---\n'])

					test_time = time.time() - test_start_time
					
					# Get the actual tools used
					actual_tools = []
					if hasattr(client, 'last_used_tools') and client.last_used_tools:
						actual_tools = [
							{
								"name": tool.function.name,
								"args": dict(tool.function.arguments)
							}
							for tool in client.last_used_tools
						]
					
					# Check if expected tools were used
					expected_names = [tool["name"].lower() for tool in expected_tools]
					actual_names = [tool["name"].lower() for tool in actual_tools]
					
					# Simple validation: check if at least one expected tool was used
					# tools_match = any(name in actual_names for name in expected_names)
					tools_match = all(name in actual_names for name in expected_names)
					
					if tools_match:
						results["passed"] += 1
						status = "PASSED"
					else:
						results["failed"] += 1
						status = "FAILED"
					
					results["details"].append({
						"category": category,
						"question": question,
						"expected_tools": expected_names,
						"actual_tools": actual_names,
						"status": status,
						"response_length": len(response) if response else 0,
						"response_time": test_time,
						"tool_count": len(actual_tools)
					})
					
				except Exception as e:
					test_time = time.time() - test_start_time
					results["errors"] += 1
					results["details"].append({
						"category": category,
						"question": question,
						"expected_tools": [tool["name"] for tool in expected_tools],
						"actual_tools": [],
						"status": "ERROR",
						"error": str(e),
						"response_time": test_time,
						"tool_count": 0
					})
	
	results["total_time"] = time.time() - start_time
	results["avg_response_time"] = sum(d.get("response_time", 0) for d in results["details"]) / len(results["details"]) if results["details"] else 0
	
	return results

async def run_model_comparison(sample_size: Optional[int] = None):
	"""Run performance comparison across multiple Ollama models."""
	print("🚀 Starting Multi-Model MCP Tool Performance Comparison...")
	print("=" * 80)
	
	# Available models to test
	models_to_test = [
		"qwen3-coder:480b-cloud",
		"gpt-oss:20b-cloud",
		"llama3.2:latest",
		"gemma:2b"
	]
	
	test_cases = create_test_cases()
	all_results = []
	
	# Test each model
	for model in models_to_test:
		try:
			model_results = await run_single_model_test(model, test_cases, sample_size)
			all_results.append(model_results)
			
			# Print quick summary for this model
			success_rate = (model_results["passed"] / model_results["total_tests"] * 100) if model_results["total_tests"] > 0 else 0
			print(f"📊 {model}: {model_results['passed']}/{model_results['total_tests']} passed ({success_rate:.1f}%) - Avg: {model_results['avg_response_time']:.2f}s")
			
		except Exception as e:
			print(f"❌ Failed to test model {model}: {e}")
			all_results.append({
				"model": model,
				"total_tests": 0,
				"passed": 0,
				"failed": 0,
				"errors": 1,
				"total_time": 0,
				"avg_response_time": 0,
				"details": [],
				"error": str(e)
			})
	
	# Generate comparison report
	print("\n" + "=" * 80)
	print("📊 MULTI-MODEL PERFORMANCE COMPARISON")
	print("=" * 80)
	
	# Sort by success rate
	valid_results = [r for r in all_results if r["total_tests"] > 0]
	valid_results.sort(key=lambda x: (x["passed"] / x["total_tests"], -x["avg_response_time"]), reverse=True)
	
	print(f"{'Model':<25} {'Tests':<8} {'Passed':<8} {'Failed':<8} {'Success%':<10} {'Avg Time':<10} {'Tools/Test':<12}")
	print("-" * 90)
	
	for result in valid_results:
		success_rate = (result["passed"] / result["total_tests"] * 100) if result["total_tests"] > 0 else 0
		avg_tools = sum(d.get("tool_count", 0) for d in result["details"]) / len(result["details"]) if result["details"] else 0
		
		print(f"{result['model']:<25} {result['total_tests']:<8} {result['passed']:<8} {result['failed']:<8} {success_rate:<10.1f} {result['avg_response_time']:<10.2f} {avg_tools:<12.1f}")
	
	# Show failed models
	failed_results = [r for r in all_results if r["total_tests"] == 0]
	if failed_results:
		print(f"\n❌ Failed to test {len(failed_results)} models:")
		for result in failed_results:
			print(f"   - {result['model']}: {result.get('error', 'Unknown error')}")
	
	# Detailed analysis by category
	if valid_results:
		print(f"\n📋 PERFORMANCE BY CATEGORY (Best Model: {valid_results[0]['model']})")
		print("-" * 80)
		
		categories = ["basics", "intermediates", "advanced", "complex"]
		for category in categories:
			print(f"\n{category.upper()}:")
			for result in valid_results[:3]:  # Top 3 models
				category_tests = [d for d in result["details"] if d["category"] == category]
				if category_tests:
					passed = sum(1 for d in category_tests if d["status"] == "PASSED")
					total = len(category_tests)
					success_rate = (passed / total * 100) if total > 0 else 0
					avg_time = sum(d.get("response_time", 0) for d in category_tests) / total
					print(f"  {result['model']:<25} {passed}/{total} ({success_rate:.1f}%) - {avg_time:.2f}s")
	
	# Question failure analysis
	question_stats_sorted = []  # Initialize to avoid unbound variable
	
	if valid_results:
		print(f"\n📊 QUESTION FAILURE ANALYSIS")
		print("-" * 80)
		
		# Collect all question failures across models
		question_failures = {}
		question_totals = {}
		
		for result in valid_results:
			for detail in result["details"]:
				question = detail.get("question", "Unknown")
				status = detail.get("status", "UNKNOWN")
				
				# Initialize counters
				if question not in question_failures:
					question_failures[question] = 0
					question_totals[question] = 0
				
				question_totals[question] += 1
				if status in ["FAILED", "ERROR"]:
					question_failures[question] += 1
		
		# Calculate failure rates and sort by highest failure rate
		question_stats = []
		for question, failures in question_failures.items():
			total = question_totals[question]
			failure_rate = (failures / total * 100) if total > 0 else 0
			question_stats.append({
				"question": question,
				"failures": failures,
				"total": total,
				"failure_rate": failure_rate
			})
		
		# Sort by failure rate (highest first)
		question_stats_sorted = sorted(question_stats, key=lambda x: (-x["failure_rate"], -x["failures"]))
		
		print(f"{'Failures':<10} {'Total':<8} {'Rate%':<8} {'Question':<60}")
		print("-" * 90)
		
		for stat in question_stats_sorted:
			question_short = stat["question"][:55] + "..." if len(stat["question"]) > 58 else stat["question"]
			print(f"{stat['failures']:<10} {stat['total']:<8} {stat['failure_rate']:<8.1f} {question_short}")
		
		# Show most problematic questions
		most_failed = [q for q in question_stats_sorted if q["failure_rate"] > 50]
		if most_failed:
			print(f"\n🚨 MOST PROBLEMATIC QUESTIONS (>50% failure rate):")
			for i, stat in enumerate(most_failed, 1):
				print(f"  {i}. {stat['question']}")
				print(f"     Failures: {stat['failures']}/{stat['total']} ({stat['failure_rate']:.1f}%)")
		
		# Show most reliable questions  
		most_reliable = [q for q in question_stats_sorted if q["failure_rate"] == 0 and q["total"] > 1]
		if most_reliable:
			print(f"\n✅ MOST RELIABLE QUESTIONS (0% failure rate):")
			for i, stat in enumerate(most_reliable[:5], 1):
				question_short = stat["question"][:70] + "..." if len(stat["question"]) > 73 else stat["question"]
				print(f"  {i}. {question_short}")

	# Save comprehensive results
	comparison_results = {
		"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
		"sample_size": sample_size,
		"total_models_tested": len(valid_results),
		"failed_models": len(failed_results),
		"question_failure_analysis": question_stats_sorted,
		"results": all_results
	}
	
	with open('model_comparison_results.json', 'w') as f:
		json.dump(comparison_results, f, indent=2)
	
	print(f"\n💾 Comprehensive results saved to model_comparison_results.json")
	
	return comparison_results

async def run_test_suite():
	"""Run the complete test suite with default model (backward compatibility)."""
	print("🚀 Starting MCP Tool Testing Suite (Single Model)...")
	
	test_cases = create_test_cases()
	results = await run_single_model_test("llama3.2", test_cases)
	
	# Print summary
	print("\n" + "=" * 60)
	print("📊 TEST SUITE SUMMARY")
	print("=" * 60)
	print(f"Model: {results['model']}")
	print(f"Total Tests: {results['total_tests']}")
	print(f"✅ Passed: {results['passed']}")
	print(f"❌ Failed: {results['failed']}")
	print(f"⚠️  Errors: {results['errors']}")
	print(f"Success Rate: {(results['passed']/results['total_tests']*100):.1f}%")
	print(f"Average Response Time: {results['avg_response_time']:.2f}s")
	
	# Save detailed results
	with open('test_results.json', 'w') as f:
		json.dump(results, f, indent=2)
	
	print(f"\n💾 Detailed results saved to test_results.json")
	
	return results

def main(argv):
	"""Main function to run the test suite."""
	import argparse
	
	parser = argparse.ArgumentParser(description="MCP Tool Testing Suite")
	parser.add_argument('--compare', '-c', action='store_true', 
						help='Run model comparison across all available models')
	parser.add_argument('--sample', '-s', type=int, default=None,
						help='Sample size per category for faster testing (default: all tests)')
	parser.add_argument('--model', '-m', type=str, default='llama3.2',
						help='Single model to test (default: llama3.2)')
	
	args = parser.parse_args(argv)
	
	if args.compare:
		print(f"🔄 Running model comparison with sample size: {args.sample or 'all tests'}")
		results = asyncio.run(run_model_comparison(args.sample))
	else:
		print(f"🔄 Running single model test: {args.model}")
		test_cases = create_test_cases()
		results = asyncio.run(run_single_model_test(args.model, test_cases, args.sample))
		
		# Print summary for single model
		print("\n" + "=" * 60)
		print("📊 TEST SUITE SUMMARY")
		print("=" * 60)
		print(f"Model: {results['model']}")
		print(f"Total Tests: {results['total_tests']}")
		print(f"✅ Passed: {results['passed']}")
		print(f"❌ Failed: {results['failed']}")
		print(f"⚠️  Errors: {results['errors']}")
		print(f"Success Rate: {(results['passed']/results['total_tests']*100):.1f}%")
		print(f"Average Response Time: {results['avg_response_time']:.2f}s")
		
		# Show failed questions for single model
		if results['failed'] > 0 or results['errors'] > 0:
			print(f"\n❌ FAILED QUESTIONS:")
			print("-" * 60)
			failed_questions = [d for d in results["details"] if d["status"] in ["FAILED", "ERROR"]]
			for i, detail in enumerate(failed_questions, 1):
				question_short = detail["question"][:50] + "..." if len(detail["question"]) > 53 else detail["question"]
				status = detail["status"]
				category = detail.get("category", "unknown")
				print(f"  {i}. [{category.upper()}] {question_short} ({status})")
				if "error" in detail:
					print(f"     Error: {detail['error']}")
		
		# Save detailed results
		with open('test_results.json', 'w') as f:
			json.dump(results, f, indent=2)
		
		print(f"\n💾 Detailed results saved to test_results.json")
	
	return results
	

if __name__ == '__main__':
	import sys
	main(sys.argv[1:])


