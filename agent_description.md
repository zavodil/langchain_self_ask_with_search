# Self-Ask with Search Agent

This agent implements the self-ask-with-search methodology, a powerful question-answering approach that breaks down complex queries into simpler sub-questions and uses search capabilities to find intermediate answers.

## Overview

The Self-Ask with Search Agent is designed to answer complex questions by:
1. Determining if follow-up questions are needed
2. Generating relevant sub-questions
3. Searching for intermediate answers
4. Synthesizing the final answer from the gathered information

This approach is particularly effective for multi-hop questions that require gathering information from multiple sources or understanding relationships between different entities.

## Key Features

- **Intelligent Question Decomposition**: Automatically identifies when a question requires multiple steps to answer
- **Iterative Search**: Performs targeted searches for each sub-question
- **Answer Synthesis**: Combines intermediate answers to provide comprehensive final responses
- **Support for Multiple Search Backends**: Compatible with Google Serper API, Search API, and Serp API

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Finding information about relationships (e.g., "Who was the maternal grandfather of George Washington?")
- Answering questions requiring multiple facts (e.g., "Are both directors of Jaws and Casino Royale from the same country?")

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object containing:
  - `status`: "success" or "error"
  - `output`: The final answer to the question (on success)
  - `message`: Error description (on error)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools for the agent