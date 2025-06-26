# Self-Ask with Search Agent

A reasoning agent that breaks down complex questions into simpler sub-questions and uses search to find intermediate answers before arriving at a final conclusion.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to produce a final answer

The agent excels at multi-hop reasoning tasks that require gathering information from multiple sources to answer complex queries.

## Key Features

- **Multi-hop Reasoning**: Automatically decomposes complex questions into simpler sub-questions
- **Search Integration**: Uses a search tool to find factual information for each sub-question
- **Chain-of-Thought**: Shows its reasoning process through intermediate steps
- **Flexible Search Backend**: Supports Google Serper, SearchAPI, or SerpAPI as search providers

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, Person A or Person B?")
- Finding information that requires multiple lookups (e.g., "When was the founder of Company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of Historical Figure?")
- Making comparisons that require gathering facts (e.g., "Are both directors from the same country?")

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to answer
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer after reasoning through sub-questions
  - `message`: Error details (only if status is "error")

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (search capabilities)