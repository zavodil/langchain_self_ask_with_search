# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach with search capabilities to break down complex questions into simpler sub-questions and find answers incrementally.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

The agent is particularly effective for multi-hop questions that require gathering information from multiple sources or reasoning through several steps.

## Key Features

- **Intelligent Question Decomposition**: Automatically determines when follow-up questions are needed
- **Incremental Answer Building**: Gathers intermediate answers to build towards the final response
- **Search Integration**: Uses external search tools to find factual information
- **Chain-of-Thought Reasoning**: Shows its reasoning process through explicit follow-up questions

## Inputs

- **HTTP POST `/run`**:
  - `input` (string): The question or query to be answered
  - `chat_history` (optional): Previous conversation context

## Outputs

- **HTTP Response**:
  - `status`: Success or error status
  - `output`: The final answer after processing all necessary follow-up questions
  - Shows intermediate reasoning steps including:
    - Follow-up questions generated
    - Intermediate answers found
    - Final synthesized answer

## Example Use Cases

- Comparative questions (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Multi-step factual queries (e.g., "When was the founder of Craigslist born?")
- Genealogical or relationship questions (e.g., "Who was the maternal grandfather of George Washington?")
- Cross-referencing questions (e.g., "Are both directors of Jaws and Casino Royale from the same country?")

## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available search tools