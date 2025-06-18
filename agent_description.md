# Self-Ask with Search Agent

A question-answering agent that uses a self-asking approach with search capabilities to break down complex questions into simpler sub-questions and find answers step by step.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

## Main Functions

- **Question Decomposition**: Automatically identifies when a question needs to be broken down into simpler sub-questions
- **Iterative Search**: Performs searches for each sub-question to gather intermediate answers
- **Answer Synthesis**: Combines intermediate answers to formulate a comprehensive final response

## Examples of Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, Person A or Person B?")
- Finding information that requires multiple steps (e.g., "When was the founder of Company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of Historical Figure?")
- Making comparisons that require gathering multiple facts

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input`: The question to be answered (string)
  - `chat_history`: Optional conversation history (list of dictionaries)

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: Success or error status
  - `output`: The final answer to the question (on success)
  - `message`: Error description (on failure)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools used by the agent