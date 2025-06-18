# Self-Ask with Search Agent

A LangChain-based agent that implements the self-ask-with-search methodology for answering complex questions by breaking them down into simpler sub-questions.

## Overview

This agent uses a unique approach to answer questions that require multiple steps of reasoning. It determines whether follow-up questions are needed, asks those questions, searches for intermediate answers, and then synthesizes a final answer based on the collected information.

## Main Functions

- **Question Decomposition**: Automatically identifies when a question requires follow-up questions to be answered properly
- **Iterative Search**: Performs searches for intermediate answers to sub-questions
- **Answer Synthesis**: Combines intermediate answers to produce a comprehensive final answer
- **Chain-of-Thought Reasoning**: Follows a structured reasoning pattern similar to human problem-solving

## Key Features

- Handles complex multi-step questions that require gathering information from multiple sources
- Supports various search backends (Google Serper API, Search API, SerpAPI)
- Provides transparent reasoning by showing the thought process and intermediate steps
- Particularly effective for questions about comparisons, relationships, and facts that require multiple lookups

## Inputs

- **HTTP POST /run**
  - `input`: The question or query to be answered (string)
  - `chat_history`: Optional conversation history (list of dictionaries)

## Outputs

- **HTTP Response**
  - `status`: Success or error status
  - `output`: The final answer after processing all necessary sub-questions
  - Shows intermediate reasoning steps when verbose mode is enabled

## Additional Endpoints

- **GET /**: Health check endpoint
- **GET /tools**: Returns the list of available tools (search capabilities)

## Example Use Cases

- Comparing lifespans of historical figures
- Finding relationships between people or events
- Answering questions that require multiple fact lookups
- Resolving queries about dates, locations, or biographical information