#!/usr/bin/env python3

"""
Optimized Ollama Client following OpenAI pattern for MCP tools integration
"""

import argparse

import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional
from ollama import AsyncClient

import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.types import TextContent
from mcp.client.stdio import stdio_client

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
load_dotenv("../.env")


class OllamaClient:
	"""Optimized client for interacting with Ollama models using MCP tools (OpenAI-style)."""

	def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
		"""Initialize the Ollama MCP client."""
		self.session: Optional[ClientSession] = None
		self.exit_stack = AsyncExitStack()
		self.model = model
		self.base_url = base_url
		self.stdio: Optional[Any] = None
		self.write: Optional[Any] = None
		
		# Configure ollama client
		self.ollama_client = AsyncClient(host=base_url)
		
		# Model fallback order (most reliable first)
		self.models_fallback = ['llama3.2', 'gpt-oss:20b-cloud', 'qwen3-coder:480b-cloud']
		self.last_used_tools = []

	async def connect_to_server(self, server_script_path: str = "MCPserver.py"):
		"""Connect to an MCP server."""
		server_params = StdioServerParameters(
			command="python",
			args=[server_script_path],
		)

		stdio_transport = await self.exit_stack.enter_async_context(
			stdio_client(server_params)
		)
		self.stdio, self.write = stdio_transport
		self.session = await self.exit_stack.enter_async_context(
			ClientSession(self.stdio, self.write)
		)
		await self.session.initialize()

	async def get_mcp_tools(self) -> List[Dict[str, Any]]:
		"""Get available tools from the MCP server in OpenAI format."""
		if not self.session:
			raise RuntimeError("Not connected to MCP server. Call connect_to_server() first.")
			
		tools_result = await self.session.list_tools()
		return [
			{
				"type": "function",
				"function": {
					"name": tool.name,
					"description": tool.description,
					"parameters": tool.inputSchema,
				},
			}
			for tool in tools_result.tools
		]

	async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
		"""Call an MCP tool with the given arguments."""
		if not self.session:
			raise RuntimeError("Not connected to MCP server")
		
		result = await self.session.call_tool(tool_name, arguments=arguments)
		print(f'🔧 Executed: {tool_name}({arguments})')
		# print(result)
		# print("+"*80)
		
		# Extract text content from the result
		return ' '.join([content.text for content in result.content if isinstance(content, TextContent)])

	async def process_query(self, query: str, enable_debug: bool = True) -> str:
		"""Process a query using Ollama and available MCP tools.

		Args:
			query: The user query.

		Returns:
			The response from Ollama.
		"""
		# Get available tools
		try:
			
			tools = await self.get_mcp_tools()

			# Create a more explicit system prompt that forces tool usage
# 			system_prompt = """\
# You are a helpful assistant with access to car database tools. You MUST use the available tools to answer questions about cars. 
# NEVER write pandas code or SQL queries. Instead, ALWAYS use ONLY the provided tools to get the actual data.
# Available tools will be provided to you. When asked about cars, you must call the appropriate tools to get real data from the database.
# Example: If asked about Toyota cars, use the search_cars_by_brand tool with brand="Toyota" parameter. Format the response in Markdown whenever it is possible.\
# """
			system_prompt = """\
You are a helpful assistant with access to specialized car database tools.
You MUST always use the provided tools to retrieve real data when answering questions about cars.

Rules:  
- NEVER write or suggest pandas code, SQL queries, or any direct database operations.
- Database-bound answers only: Never invent, assume, or suggest information that is not explicitly present in the database or returned by the available tools. If the data is missing, clearly state that no results were found.
- ALWAYS call the appropriate tool(s) to obtain information.
- If multiple tools are needed, chain them logically and use their outputs to form the final answer.
- Only use tools exactly as defined (correct names, valid parameters). Do not invent tools or arguments.
- Logical argument parsing: Break down the user's query into clear, structured arguments so they can be matched to the correct tool parameters. Ensure arguments are concise, valid, and directly tied to the tool definitions (e.g., brand, model, year range, fuel type).
- Format final answers in clear, user-friendly natural language. Prefer Markdown formatting when appropriate (e.g., tables, lists, highlights).
- Keep reasoning hidden: show only the final, useful answer to the user.

Example:  
User: *"Show me all Toyota cars."*  
Action: Call `search_cars_by_brand` with `brand="Toyota"`.
Answer: Present the returned results in a clean Markdown table or list.

Your role: Interpret the query, choose the correct tool(s) and argument(s), execute, and respond with the most accurate and clear information possible.\
"""

			messages = []
			messages.append(dict(role='system', content=system_prompt))
			messages.append(dict(role='user', content=query))
			options = dict(temperature=0.1)  # Lower temperature for more deterministic tool usage
			
			response = None
			try:
				response = await self.ollama_client.chat(
					# model='qwen3-coder:480b-cloud',
					model=self.model,
					messages=messages,
					tools=tools,
					options=options
				)
			except Exception as e:
				print(f'Exception {e}\n Trying use default model')
				response = await self.ollama_client.chat(
					# model='qwen3-coder:480b-cloud',
					model=self.model,
					messages=messages,
					tools=tools,
					options=options
				)

			
			# Step 1: Check if tools are needed
			assistant_message = response.message
			
			# Step 2: If no tools needed, return direct response
			if not assistant_message.tool_calls:
				return assistant_message.content or "I can help you with car database queries."
			
			# Step 3: Execute tool calls one by one
			messages = []
			messages.append(dict(role='system', content=system_prompt))
			messages.append(dict(
				role = "assistant",
				content = assistant_message.content,
				tool_calls = assistant_message.tool_calls
			))
			
			self.last_used_tools = assistant_message.tool_calls

			for tool_call in assistant_message.tool_calls:
				# Extract tool information
				tool_name = tool_call.function.name
				arguments = dict(tool_call.function.arguments)  # Convert to dict for type safety
				
				if enable_debug:
					print(f"🔧 Executing tool: {tool_name} with arguments: {arguments}")
				
				# Step 4: Execute the tool
				content = ''
				try:
					content = await self.call_mcp_tool(tool_name, arguments)
				except Exception as e:
					content = f"Error executing tool {tool_name}: {e}"
					if enable_debug:
						print(f"❌ {content}")
			
				# Add tool result to conversation
				if len(content) > 0:
					messages.append(dict(role="tool", content=content, tool_name=tool_name))
					# messages.append(dict(role="assistant", content=f"{tool_name} returns :\n```json\n{content}\n```\n"))
			messages.append(dict(role='user', content=query))


			# Step 5: Generate final response with tool results
			# [print(json.dumps(i, indent=2).replace('\\n','\n')) for i in messages]
			# print("="*80)	
			# [print(i, '\n') for i in messages]
			# print("="*80)	
			options = dict(temperature=0.13)  # Lower temperature for more deterministic tool usage
			final_response = await self.ollama_client.chat(
				# model='qwen3-coder:480b-cloud',
				model=self.model,
				messages=messages,
				options=options
			)
			
			return final_response.message.content or "Unable to generate response with tool results."
		
		except KeyboardInterrupt as e:
			print('KeyboardInterrupt', e)
			return "Unable to generate response with tool results (KeyboardInterrupt)."

	async def close(self):
		"""Close connections and clean up resources."""
		if self.exit_stack:
			await self.exit_stack.aclose()

	async def __aenter__(self):
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		await self.close()


async def main(args):
	"""Test the optimized client."""

	print("🚀 Starting Optimized Ollama MCP Client...")

	async with OllamaClient() as client:
		await client.connect_to_server("MCPserver.py")

		os.system(f'rm {args.output}; touch {args.output}')

		if args.interactive:
			while True:
				try:
					question = input('Type a question: ').strip()
					if not question:
						continue
					if question.lower() in ['quit', 'exit', 'q']:
						print("👋 Goodbye!")
						break
					if question.lower() in ['help', 'h']:
						print("\n🆘 Available commands:")
						print("  - Ask any question")
						print("  - 'quit' - Exit interactive mode")
						print("  - 'help' - Provide this help content")
						continue
					response = await client.process_query(question)
					with open(args.output, 'a') as file:
						used_tools = '\n'.join([f'{i.function.name:<30}\t{i.function.arguments}' for i in client.last_used_tools])
						file.writelines(f'```json\n{used_tools}\n```\n')
						file.writelines([f'\n# {question}\n\n{response}\n\n---\n'])
					print(response)
				except KeyboardInterrupt as e:
					print('KeyboardInterrupt', e)
					continue
				# print(response)
			return
		# Test queries
		questions = []
		# questions.append("Provide me a summary of the current available cars")
		# questions.append("Find me all Toyota cars with low mileage lower than 38576 kilometers. Then, list all available models from the brand Ford.")
		# questions.append("Encontre todos os carros Toyota com quilometragem inferior a 38576 quilômetros. Em seguida, liste todos os modelos disponíveis da marca Ford.")
		# questions.append("What are the available car brands in the dataset?")
		# questions.append("List the car brands sorted by the number of cars of each branch")
		questions.append("Qual o carro mais antigo e qual o carro mais novo?")


		for question in questions:
			print(f"\n🎯 Query: {question}")
			with open(args.output, 'a') as file:
				file.writelines([f'\n# {question}\n\n'])

			response = await client.process_query(question)
			with open(args.output, 'a') as file:
				used_tools = '\n'.join([f'{i.function.name:<30}\t{i.function.arguments}' for i in client.last_used_tools])
				file.writelines(f'```json\n{used_tools}\n```\n')
				file.writelines([f'{response}\n\n---\n'])
			
			print(f"✅ Response saved to {args.output}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="OllamaClient chat.")
	parser.add_argument('-i', '--interactive', help='Enable interactive mode', type=bool, required=False, nargs='?', const=True, default=False)
	parser.add_argument('-o', '--output', help='Output file name for agent responses', type=str, default='agent_output.md')
	args = parser.parse_args()

	asyncio.run(main(args))