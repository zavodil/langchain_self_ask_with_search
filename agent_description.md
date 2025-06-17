# Self-Ask with Search Agent

A conversational AI agent that uses a self-ask with search approach to answer complex questions by breaking them down into simpler sub-questions and searching for intermediate answers.

## Overview

This agent implements the self-ask with search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

The agent is particularly effective for questions that require multiple steps of reasoning or gathering information from different sources.

## Key Features

- **Multi-step Reasoning**: Automatically breaks down complex questions into manageable sub-questions
- **Search Integration**: Uses search tools to find intermediate answers
- **Chain-of-Thought**: Shows its reasoning process through follow-up questions and intermediate answers
- **Flexible Architecture**: Can work with various search providers (Google Serper, SearchAPI, SerpAPI)

## Inputs

- **HTTP POST /run**
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **HTTP Response**
  - `status`: Success or error status
  - `output`: The final answer after processing all follow-up questions and intermediate answers

## Example Usage

When asked "Are both the directors of Jaws and Casino Royale from the same country?", the agent will:
1. Ask "Who is the director of Jaws?" → Find "Steven Spielberg"
2. Ask "Where is Steven Spielberg from?" → Find "The United States"
3. Ask "Who is the director of Casino Royale?" → Find "Martin Campbell"
4. Ask "Where is Martin Campbell from?" → Find "New Zealand"
5. Provide final answer: "No"

## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available tools for the agent