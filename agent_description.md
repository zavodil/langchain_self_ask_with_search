# Self-Ask with Search Agent

This agent implements the self-ask-with-search methodology, a powerful approach for answering complex questions by breaking them down into simpler sub-questions and using search to find intermediate answers.

## Overview

The Self-Ask with Search Agent is designed to handle questions that require multiple steps of reasoning. It automatically determines when follow-up questions are needed, formulates these questions, searches for answers, and combines the information to provide a final answer.

## Key Features

- **Automatic Question Decomposition**: Identifies when a question requires additional information and generates relevant follow-up questions
- **Search Integration**: Uses search tools to find intermediate answers for each sub-question
- **Chain-of-Thought Reasoning**: Maintains a clear reasoning path from initial question to final answer
- **Single Tool Design**: Works with exactly one search tool named "Intermediate Answer"

## How It Works

1. Analyzes the input question to determine if follow-up questions are needed
2. If yes, generates specific follow-up questions
3. Uses the search tool to find intermediate answers
4. Continues this process until sufficient information is gathered
5. Synthesizes all intermediate answers into a final response

## Example Use Cases

- **Comparative Questions**: "Who lived longer, Muhammad Ali or Alan Turing?"
- **Multi-step Factual Queries**: "Who was the maternal grandfather of George Washington?"
- **Date/Time Questions**: "When was the founder of craigslist born?"
- **Cross-reference Questions**: "Are both the directors of Jaws and Casino Royale from the same country?"

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