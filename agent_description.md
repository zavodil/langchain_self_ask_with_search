# Self-Ask with Search Agent

A conversational AI agent that uses a self-ask with search methodology to answer complex questions by breaking them down into simpler sub-questions and searching for intermediate answers.

## Overview

This agent implements the self-ask with search approach, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

The agent excels at answering multi-step questions that require gathering information from multiple sources, such as comparing facts about different people, finding relationships between entities, or answering questions that depend on intermediate facts.

## Key Features

- **Intelligent Question Decomposition**: Automatically identifies when a question needs to be broken down into simpler sub-questions
- **Iterative Search**: Searches for intermediate answers to build up to the final response
- **Chain-of-Thought Reasoning**: Shows its reasoning process through follow-up questions and intermediate answers
- **Single Tool Integration**: Works with one search tool named "Intermediate Answer"

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

## Example Use Cases

- Comparing attributes of different people (e.g., "Who lived longer, Person A or Person B?")
- Finding information about founders or creators (e.g., "When was the founder of X born?")
- Tracing relationships (e.g., "Who was the maternal grandfather of George Washington?")
- Cross-referencing facts (e.g., "Are both directors from the same country?")

## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available tools for the agent