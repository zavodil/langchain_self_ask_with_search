# Self-Ask with Search Agent

A reasoning agent that breaks down complex questions into simpler sub-questions and uses search to find intermediate answers before arriving at a final conclusion.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question needs follow-up questions to be answered
2. Generates relevant follow-up questions
3. Searches for intermediate answers to each follow-up question
4. Synthesizes the information to provide a final answer

The agent excels at multi-hop reasoning tasks that require gathering information from multiple sources or following chains of logic.

## Key Features

- **Multi-hop Reasoning**: Automatically decomposes complex questions into manageable sub-questions
- **Search Integration**: Uses search tools to find factual information for each intermediate step
- **Structured Thinking**: Follows a clear pattern of question → follow-up → intermediate answer → final answer
- **Fact-Based Responses**: Grounds answers in searchable, verifiable information

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, Person A or Person B?")
- Finding information that requires multiple steps (e.g., "When was the founder of Company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of Historical Figure?")
- Making comparisons that require gathering multiple facts (e.g., "Are both directors from the same country?")

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer after following the self-ask reasoning chain
  - `message`: Error message (only present if status is "error")

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available search tools