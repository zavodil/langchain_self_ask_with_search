# Self-Ask with Search Agent

This agent implements the self-ask-with-search methodology, where complex questions are broken down into simpler sub-questions that can be answered through iterative search queries.

## Overview

The agent uses a chain-of-thought approach to answer questions by:
1. Determining if follow-up questions are needed
2. Generating relevant sub-questions
3. Searching for intermediate answers
4. Combining the results to produce a final answer

## Main Functions

- **Question Decomposition**: Automatically identifies when a question requires multiple steps to answer
- **Iterative Search**: Performs searches for each sub-question to gather intermediate answers
- **Answer Synthesis**: Combines intermediate results to formulate the final answer

## How It Works

The agent follows a structured pattern:
1. Analyzes the input question
2. Decides if follow-up questions are necessary
3. If yes, generates specific sub-questions
4. Searches for answers to each sub-question
5. Uses the intermediate answers to derive the final answer

## Inputs

- **Medium**: HTTP API endpoint `/run`
- **Format**: JSON request body
  - `input` (string, required): The question to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON response
  - `status`: "success" or "error"
  - `output`: The final answer to the question (on success)
  - `message`: Error description (on error)

## Example Use Cases

- Answering comparative questions (e.g., "Who lived longer, X or Y?")
- Finding information that requires multiple lookups (e.g., "When was the founder of company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of person X?")
- Verifying facts that require multiple pieces of information

## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available tools used by the agent