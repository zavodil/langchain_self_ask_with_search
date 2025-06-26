# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach with search capabilities to break down complex questions into simpler sub-questions and find answers step by step.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

The agent is particularly effective for multi-hop questions that require gathering information from multiple sources or reasoning through several steps.

## Key Features

- **Intelligent Question Decomposition**: Automatically determines when follow-up questions are needed
- **Step-by-Step Reasoning**: Breaks down complex queries into manageable sub-questions
- **Search Integration**: Uses search tools to find intermediate answers
- **Structured Output**: Provides clear reasoning paths from question to final answer

## Inputs

- **HTTP POST /run**
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **HTTP Response**
  - `status`: Success or error status
  - `output`: The final answer after processing all necessary follow-up questions
  - `message`: Error message if applicable

## Example Use Cases

- Historical comparisons (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Genealogical queries (e.g., "Who was the maternal grandfather of George Washington?")
- Fact-finding about people or organizations (e.g., "When was the founder of Craigslist born?")
- Cross-referencing information (e.g., "Are both directors of Jaws and Casino Royale from the same country?")

## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available search tools