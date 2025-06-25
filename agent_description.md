# Self-Ask with Search Agent

A LangChain-based agent that implements the self-ask-with-search methodology for answering complex questions by breaking them down into simpler sub-questions.

## Overview

This agent uses a chain-of-thought reasoning approach where it:
1. Analyzes if a question requires follow-up questions to answer properly
2. Generates relevant follow-up questions
3. Searches for intermediate answers using a search tool
4. Combines the intermediate answers to produce a final response

## Key Features

- **Intelligent Question Decomposition**: Automatically determines when a question needs to be broken down into simpler sub-questions
- **Iterative Search**: Uses a search tool to find intermediate answers for each sub-question
- **Chain-of-Thought Reasoning**: Maintains context throughout the questioning process to arrive at accurate final answers
- **Single Tool Design**: Specifically designed to work with one search tool named "Intermediate Answer"

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
  - `output`: The final answer to the question (on success)
  - `message`: Error description (on error)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (search tool configuration)