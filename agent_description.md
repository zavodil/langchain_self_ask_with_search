# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach with search capabilities to break down complex questions into simpler sub-questions and find answers step by step.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant sub-questions to gather intermediate information
3. Uses a search tool to find answers to each sub-question
4. Combines the intermediate answers to produce a final response

## Main Functions

- **Complex Question Decomposition**: Automatically identifies when a question needs to be broken down into simpler parts
- **Iterative Search**: Performs searches for each sub-question to gather necessary information
- **Answer Synthesis**: Combines intermediate answers to formulate a comprehensive final answer
- **Multi-step Reasoning**: Handles questions that require multiple steps of information gathering

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, X or Y?")
- Finding information about relationships (e.g., "Who was the grandfather of X?")
- Verifying facts across multiple sources (e.g., "Are directors X and Y from the same country?")
- Discovering dates and biographical information

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer to the question (on success)
  - `message`: Error description (on error)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools for the agent