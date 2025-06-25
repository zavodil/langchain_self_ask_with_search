# Self-Ask with Search Agent

A reasoning agent that breaks down complex questions into simpler sub-questions and uses search to find intermediate answers before arriving at a final conclusion.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to produce a final answer

The agent excels at multi-step reasoning tasks that require gathering information from multiple sources.

## Key Features

- **Multi-step Reasoning**: Automatically decomposes complex questions into simpler sub-questions
- **Search Integration**: Uses search tools to find factual information for each sub-question
- **Chain-of-Thought**: Shows its reasoning process through intermediate steps
- **Fact-Based Answers**: Grounds responses in searchable, verifiable information

## Example Use Cases

- Comparative questions (e.g., "Who lived longer, X or Y?")
- Multi-hop questions requiring multiple facts (e.g., "When was the founder of company X born?")
- Questions requiring geographical or historical context
- Fact-checking and verification tasks

## Inputs

- **Medium**: HTTP POST request to `/run`
- **Format**: JSON
  json
  {
    "input": "Your question here",
    "chat_history": [] // Optional
  }
  

## Outputs

- **Medium**: HTTP response
- **Format**: JSON
  json
  {
    "status": "success",
    "output": "Final answer with reasoning steps"
  }
  

## API Endpoints

- `POST /run` - Execute the agent with a question
- `GET /` - Health check endpoint
- `GET /tools` - List available search tools

## Requirements

The agent requires exactly one search tool named "Intermediate Answer" to function properly. This tool is used to look up information for each follow-up question generated during the reasoning process.