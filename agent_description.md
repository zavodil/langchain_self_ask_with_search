# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach to break down complex questions into simpler sub-questions and searches for intermediate answers to arrive at a final conclusion.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Synthesizes the information to provide a final answer

## Main Functions

- **Question Decomposition**: Automatically determines if a question needs to be broken down into simpler sub-questions
- **Iterative Search**: Performs searches for each follow-up question to gather intermediate answers
- **Answer Synthesis**: Combines intermediate answers to formulate a comprehensive final response

## Examples

The agent excels at answering questions that require multiple steps of reasoning, such as:
- Comparative questions (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Questions requiring background information (e.g., "When was the founder of craigslist born?")
- Multi-hop reasoning questions (e.g., "Who was the maternal grandfather of George Washington?")

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object containing:
  - `status`: "success" or "error"
  - `output`: The final answer to the question (on success)
  - `message`: Error description (on failure)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (search capabilities)