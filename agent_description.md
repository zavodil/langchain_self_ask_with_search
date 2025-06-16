# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach to break down complex questions into simpler sub-questions, then searches for intermediate answers to arrive at a final conclusion.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

## Main Functions

- **Question Decomposition**: Automatically identifies when a question is too complex and needs to be broken down into simpler sub-questions
- **Iterative Search**: Performs searches for each follow-up question to gather intermediate answers
- **Answer Synthesis**: Combines intermediate answers to formulate a comprehensive final response

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, X or Y?")
- Finding information that requires multiple steps (e.g., "When was the founder of company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of person X?")
- Fact-checking and verification queries

## Inputs

- **Medium**: HTTP (POST request to `/run` endpoint)
- **Format**: JSON object with:
  - `input`: The question or query to be answered (string)
  - `chat_history`: Optional conversation history (list of dictionaries)

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: Success or error status
  - `output`: The final answer to the question (string)
  - `message`: Error message if applicable

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available search tools

## Requirements

The agent requires:
- A configured Language Model (LLM) for reasoning
- Access to a search tool (Google Serper, SearchAPI, or SerpAPI)
- Appropriate API keys for the LLM and search services