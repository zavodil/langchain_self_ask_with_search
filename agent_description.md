# Self-Ask with Search Agent

A sophisticated question-answering agent that uses a self-ask approach to break down complex questions into simpler sub-questions, then searches for intermediate answers to arrive at a final conclusion.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Synthesizes the information to provide a final answer

## Key Features

- **Intelligent Question Decomposition**: Automatically identifies when a question needs to be broken down into simpler parts
- **Iterative Search**: Performs multiple searches to gather all necessary information
- **Chain-of-Thought Reasoning**: Shows its reasoning process through intermediate steps
- **Single Tool Focus**: Designed to work with one search tool for retrieving intermediate answers

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, X or Y?")
- Finding information that requires multiple steps (e.g., "When was the founder of company X born?")
- Answering questions about relationships (e.g., "Who was the maternal grandfather of person X?")
- Fact-checking and verification tasks

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer (when successful)
  - `message`: Error description (when failed)

## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available tools for the agent

## Requirements

The agent requires:
- An LLM (Language Model) for reasoning
- Exactly one search tool named "Intermediate Answer" for retrieving information
- OpenAI API credentials (configured via environment variables in the deployment)