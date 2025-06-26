# Self-Ask with Search Agent

A reasoning agent that breaks down complex questions into simpler sub-questions and uses search to find intermediate answers before arriving at a final conclusion.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to produce a final answer

## Main Functions

- **Question Decomposition**: Automatically identifies when a question is too complex and needs to be broken down into simpler sub-questions
- **Iterative Search**: Uses a search tool to find answers to each follow-up question
- **Answer Synthesis**: Combines intermediate answers to construct a comprehensive final answer
- **Chain-of-Thought Reasoning**: Follows a structured reasoning pattern similar to human problem-solving

## Example Use Cases

- Answering comparative questions (e.g., "Who lived longer, X or Y?")
- Finding information that requires multiple steps (e.g., "When was the founder of company X born?")
- Resolving questions about relationships (e.g., "Who was the maternal grandfather of person X?")
- Fact-checking claims that require multiple pieces of information

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input`: The question or query to be answered (string)
  - `chat_history`: Optional conversation history (list of dictionaries)

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: Success or error status
  - `output`: The final answer after processing all intermediate steps
  - `message`: Error message (if applicable)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (search capabilities)