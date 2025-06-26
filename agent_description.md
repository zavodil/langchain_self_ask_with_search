# Self-Ask with Search Agent

A question-answering agent that uses a self-referential prompting technique to break down complex questions into simpler sub-questions, answering each one using a search tool before arriving at a final answer.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes whether a question requires follow-up questions
2. Generates relevant follow-up questions to gather necessary information
3. Uses a search tool to find intermediate answers
4. Combines the intermediate answers to produce a final, comprehensive response

## Key Features

- **Intelligent Question Decomposition**: Automatically identifies when a question is too complex and needs to be broken down
- **Iterative Search**: Performs multiple searches to gather all necessary information
- **Chain-of-Thought Reasoning**: Shows its reasoning process through follow-up questions and intermediate answers
- **Single Tool Focus**: Designed to work with exactly one search tool named "Intermediate Answer"

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, X or Y?")
- Finding information that requires multiple steps (e.g., "When was the founder of company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of person X?")
- Fact-checking and verification tasks

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer to the question (when successful)
  - `message`: Error description (when failed)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (search tool configuration)