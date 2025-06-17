# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach with search capabilities to break down complex questions into simpler sub-questions and find answers iteratively.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

The agent is particularly effective for multi-hop questions that require gathering information from multiple sources or reasoning through several steps.

## Key Features

- **Iterative Question Decomposition**: Automatically breaks down complex questions into simpler, answerable sub-questions
- **Search Integration**: Uses a search tool to find intermediate answers for each sub-question
- **Chain-of-Thought Reasoning**: Shows the reasoning process through follow-up questions and intermediate answers
- **Single Tool Design**: Requires exactly one search tool named "Intermediate Answer"

## Inputs

- **HTTP POST** to `/run` endpoint
  - `input` (string, required): The question or query to answer
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **HTTP Response** (JSON)
  - `status`: "success" or "error"
  - `output`: The final answer after processing all follow-up questions
  - `message`: Error message (only on failure)

## Example Use Cases

- **Comparative Questions**: "Who lived longer, Muhammad Ali or Alan Turing?"
- **Multi-hop Queries**: "Who was the maternal grandfather of George Washington?"
- **Fact-checking**: "Are both the directors of Jaws and Casino Royale from the same country?"
- **Date/Time Questions**: "When was the founder of craigslist born?"

## API Endpoints

- `POST /run` - Execute the agent with a question
- `GET /` - Health check endpoint
- `GET /tools` - List available tools