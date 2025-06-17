# Self-Ask with Search Agent

A LangChain-based agent that implements the self-ask-with-search methodology for answering complex questions by breaking them down into simpler sub-questions and using search tools to find intermediate answers.

## Overview

This agent uses a chain-of-thought approach where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers using a search tool
4. Combines the intermediate answers to produce a final answer

The agent is particularly effective for questions that require multiple steps of reasoning or fact-finding, such as comparing attributes of different entities or tracing relationships.

## Key Features

- **Self-directed questioning**: Automatically determines when follow-up questions are needed
- **Search integration**: Uses search APIs to find factual information
- **Chain-of-thought reasoning**: Shows its reasoning process through intermediate steps
- **Flexible search backend**: Supports Google Serper, SearchAPI, or SerpAPI

## Inputs

- **HTTP POST /run**
  - `input` (string, required): The question or query to answer
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **HTTP Response**
  - `status`: "success" or "error"
  - `output`: The final answer to the question (or error message if failed)

## Example Usage

**Input Question**: "Are both the directors of Jaws and Casino Royale from the same country?"

**Agent Process**:
1. Follow up: Who is the director of Jaws?
2. Intermediate answer: The director of Jaws is Steven Spielberg.
3. Follow up: Where is Steven Spielberg from?
4. Intermediate answer: The United States.
5. Follow up: Who is the director of Casino Royale?
6. Intermediate answer: The director of Casino Royale is Martin Campbell.
7. Follow up: Where is Martin Campbell from?
8. Intermediate answer: New Zealand.
9. Final answer: No

## Additional Endpoints

- **GET /**: Health check endpoint
- **GET /tools**: Returns the list of available tools

## Requirements

The agent requires exactly one tool named "Intermediate Answer" which should be a search tool configured with one of the supported search APIs.