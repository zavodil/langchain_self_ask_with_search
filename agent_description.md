# Self-Ask with Search Agent

A LangChain-based agent that implements the self-ask-with-search methodology for answering complex questions by breaking them down into simpler sub-questions.

## Overview

This agent uses a unique approach to answer questions that require multiple steps of reasoning. It determines whether follow-up questions are needed, asks those questions, searches for intermediate answers, and then synthesizes a final answer based on the collected information.

## Key Features

- **Self-Ask Methodology**: Automatically determines when follow-up questions are needed to answer complex queries
- **Search Integration**: Uses search tools to find intermediate answers for each sub-question
- **Chain of Thought**: Maintains a clear reasoning chain from initial question to final answer
- **Single Tool Design**: Works with exactly one search tool named "Intermediate Answer"

## How It Works

The agent follows this pattern:
1. Analyzes the input question
2. Determines if follow-up questions are needed
3. If yes, generates relevant follow-up questions
4. Searches for intermediate answers to each follow-up
5. Synthesizes all intermediate answers into a final response

## Example Use Cases

- Comparative questions (e.g., "Who lived longer, X or Y?")
- Multi-step factual queries (e.g., "When was the founder of company X born?")
- Relationship questions (e.g., "Who was the maternal grandfather of person X?")
- Cross-referencing questions (e.g., "Are the directors of movies X and Y from the same country?")

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer (on success) or error message (on failure)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools