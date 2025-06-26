from dotenv import load_dotenv
load_dotenv()
import os
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate, PromptTemplate
from langchain_core.tools import BaseTool, Tool
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from collections.abc import Sequence

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str = "input.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config file {config_path} not found. Using defaults.")
        return {
            "llm_model": "claude-opus-4-20250514",
            "temperature": 0.7,
            "max_tokens": 2000,
            "default_tools": ["search"],
            "default_input": "Hello, how can you help me?",
            "agent_config": {
                "verbose": True,
                "max_iterations": 10,
                "early_stopping_method": "generate"
            }
        }
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

def initialize_llm(config: Dict[str, Any]) -> BaseLanguageModel:
    """Initialize the language model based on configuration."""
    model_name = os.getenv('DEFAULT_MODEL_NAME', config.get('llm_model', 'claude-opus-4-20250514'))
    temperature = config.get('temperature', 0.7)
    max_tokens = config.get('max_tokens', 2000)

    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(temperature=temperature, max_tokens=max_tokens)

def initialize_tools(config: Dict[str, Any], llm: BaseLanguageModel) -> List[BaseTool]:
    """Initialize tools based on configuration."""
    tools = []
    
    # For self-ask-with-search, we need exactly one tool named "Intermediate Answer"
    # We'll use the search tool for this
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search_tool = DuckDuckGoSearchRun()
        # Wrap it with the required name
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search the web for intermediate answers",
            func=search_tool.run
        )
        tools.append(intermediate_answer_tool)
    except Exception as e:
        logger.error(f"Error initializing search tool: {e}")
        # Create a dummy tool if search fails
        def dummy_search(query: str) -> str:
            return f"Unable to search for: {query}"
        
        tools.append(Tool(
            name="Intermediate Answer",
            description="Dummy search tool",
            func=dummy_search
        ))
    
    return tools

def create_prompt() -> BasePromptTemplate:
    """Create the prompt template for the agent."""
    try:
        from langchain import hub
        prompt = hub.pull("hwchase17/self-ask-with-search")
        logger.info("Successfully pulled prompt from hub")
        return prompt
    except Exception as e:
        logger.warning(f"Could not pull from hub: {e}. Creating custom prompt.")
        # Create custom prompt with required variables
        template = """Question: {input}
Are followup questions needed here:{agent_scratchpad}"""
        return PromptTemplate(
            input_variables=["input", "agent_scratchpad"],
            template=template
        )

def read_input(input_source: str) -> str:
    """Read input from file or return as string."""
    if os.path.isfile(input_source):
        with open(input_source, 'r') as f:
            return f.read().strip()
    return input_source

def save_output(result: Any, output_path: str, config: Dict[str, Any], error: str = None):
    """Save the output to a JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "config": config,
        "result": None,
        "error": None,
        "metadata": {
            "agent_type": "Self-Ask with Search Agent",
            "model": config.get("llm_model", "unknown"),
            "temperature": config.get("temperature", 0.7)
        }
    }
    
    if error:
        output_data["error"] = error
    else:
        try:
            if hasattr(result, 'dict'):
                output_data["result"] = result.dict()
            elif isinstance(result, dict):
                output_data["result"] = result
            else:
                output_data["result"] = str(result)
        except Exception as e:
            output_data["result"] = str(result)
            output_data["error"] = f"Error serializing result: {str(e)}"
    
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    logger.info(f"Output saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Run LangChain Self-Ask with Search Agent")
    parser.add_argument("--input", type=str, help="Input text or path to input file")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, default="input.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set up logging level from config
    log_level = config.get("error_handling", {}).get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    try:
        # Initialize LLM
        llm = initialize_llm(config)
        logger.info("LLM initialized successfully")
        
        # Initialize tools
        tools = initialize_tools(config, llm)
        logger.info(f"Initialized {len(tools)} tools")
        
        # Create prompt
        prompt = create_prompt()
        logger.info("Prompt created successfully")
        
        # Create agent
        from langchain.agents import create_self_ask_with_search_agent
        agent = create_self_ask_with_search_agent(llm, tools, prompt)
        logger.info("Agent created successfully")
        
        # Create agent executor
        agent_config = config.get("agent_config", {})
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=agent_config.get("verbose", True),
            max_iterations=agent_config.get("max_iterations", 10),
            early_stopping_method=agent_config.get("early_stopping_method", "generate")
        )
        
        # Get input
        if args.input:
            input_text = read_input(args.input)
        else:
            input_text = config.get("default_input", "Hello, how can you help me?")
        
        logger.info(f"Processing input: {input_text[:100]}...")
        
        # Execute agent
        result = agent_executor.invoke({"input": input_text})
        logger.info("Agent execution completed")
        
        # Save output
        save_output(result, args.output, config)
        
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        if config.get("error_handling", {}).get("save_errors_to_output", True):
            save_output(None, args.output, config, str(e))
        raise

if __name__ == "__main__":
    main()