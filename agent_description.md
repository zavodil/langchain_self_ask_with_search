# Self-Ask with Search Agent

A sophisticated question-answering agent that uses a self-ask approach to break down complex questions into simpler sub-questions, search for intermediate answers, and synthesize a final response.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes whether a question requires follow-up questions
2. Generates relevant follow-up questions to gather necessary information
3. Searches for intermediate answers using a search tool
4. Combines the intermediate answers to produce a final, comprehensive response

## Key Features

- **Intelligent Question Decomposition**: Automatically identifies when a question needs to be broken down into simpler sub-questions
- **Iterative Search**: Performs multiple searches to gather all necessary information
- **Context-Aware Reasoning**: Maintains context across multiple follow-up questions to arrive at accurate answers
- **Structured Response Format**: Follows a consistent pattern of question → follow-up → intermediate answer → final answer

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, X or Y?")
- Finding information that requires multiple steps (e.g., "When was the founder of company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of person X?")
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
  - `output`: The final answer to the question (when successful)
  - `message`: Error description (when failed)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools used by the agent

## Requirements

The agent requires exactly one tool named "Intermediate Answer" for performing searches and gathering information needed to answer questions.