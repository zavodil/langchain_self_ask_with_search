# Self-Ask with Search Agent

A LangChain-based agent that implements the self-ask-with-search methodology for answering complex questions by breaking them down into simpler sub-questions and using search to find intermediate answers.

## Overview

This agent uses a chain-of-thought reasoning approach where it:
1. Analyzes if a question requires follow-up questions to be answered
2. Generates relevant follow-up questions
3. Searches for intermediate answers to each follow-up question
4. Synthesizes the intermediate answers to provide a final answer

## Key Features

- **Self-Ask Reasoning**: Automatically determines when follow-up questions are needed to answer complex queries
- **Search Integration**: Uses external search tools to find factual information for intermediate answers
- **Chain-of-Thought**: Maintains a clear reasoning chain from initial question to final answer
- **Flexible Search Backend**: Supports multiple search providers (Google Serper, SearchAPI, SerpAPI)

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Finding information that requires multiple steps (e.g., "When was the founder of Craigslist born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of George Washington?")
- Making comparisons that require gathering multiple facts (e.g., "Are both directors of Jaws and Casino Royale from the same country?")

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer after self-ask reasoning and search
  - `message`: Error message (only if status is "error")

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (search capabilities)

## Requirements

The agent requires exactly one tool named "Intermediate Answer" which provides search functionality. This tool is used to find factual information needed to answer the follow-up questions generated during the self-ask process.