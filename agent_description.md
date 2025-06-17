# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach with search capabilities to answer complex questions by breaking them down into simpler sub-questions.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions to be answered
2. Generates relevant follow-up questions
3. Searches for intermediate answers using a search tool
4. Combines the intermediate answers to provide a final answer

The agent is particularly effective for questions that require multiple steps of reasoning or gathering information from different sources.

## Main Functions

- **Question Decomposition**: Automatically determines if a question needs to be broken down into simpler sub-questions
- **Follow-up Generation**: Creates relevant follow-up questions to gather necessary information
- **Search Integration**: Uses search tools to find intermediate answers for each sub-question
- **Answer Synthesis**: Combines all intermediate answers to formulate a comprehensive final answer

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
- `GET /tools`: Returns the list of available search tools

## Example Use Cases

- Answering comparative questions (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Finding specific information about people or events (e.g., "When was the founder of craigslist born?")
- Answering questions requiring multiple steps of reasoning (e.g., "Who was the maternal grandfather of George Washington?")