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
from typing import Sequence

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str = "input.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    default_config = {
        "llm_model": "claude-opus-4-20250514",
        "temperature": 0.7,
        "max_tokens": 2000,
        "default_tools": ["search"],
        "default_input": "Hello, how can you help me?",
        "agent_config": {
            "verbose": True,
            "max_iterations": 10,
            "early_stopping_method": "generate"
        },
        "output_format": "json",
        "include_metadata": True
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
                logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.warning(f"Error loading config from {config_path}: {e}")
    
    return default_config

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
        search = DuckDuckGoSearchRun()
        # Wrap it with the required name
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search the internet for intermediate answers",
            func=search.run
        )
        tools.append(intermediate_answer_tool)
        logger.info("Initialized Intermediate Answer tool for self-ask-with-search")
    except Exception as e:
        logger.error(f"Error initializing search tool: {e}")
        # Create a dummy tool if search fails
        def dummy_search(query: str) -> str:
            return f"Search unavailable. Unable to find information about: {query}"
        
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Dummy search tool",
            func=dummy_search
        )
        tools.append(intermediate_answer_tool)
    
    return tools

def create_prompt() -> BasePromptTemplate:
    """Create the prompt for the self-ask-with-search agent."""
    try:
        from langchain import hub
        prompt = hub.pull("hwchase17/self-ask-with-search")
        logger.info("Successfully pulled prompt from hub")
        return prompt
    except Exception as e:
        logger.warning(f"Could not pull prompt from hub: {e}. Creating default prompt.")
        template = """Question: {input}

Are follow up questions needed here: Yes.
Follow up: {agent_scratchpad}"""
        return PromptTemplate.from_template(template)

def read_input(input_source: str) -> str:
    """Read input from either direct text or file."""
    if os.path.isfile(input_source):
        with open(input_source, 'r') as f:
            return f.read().strip()
    return input_source

def save_output(result: Any, output_path: str, config: Dict[str, Any], error: str = None) -> None:
    """Save the output to a JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "llm_model": config.get("llm_model"),
            "temperature": config.get("temperature"),
            "max_tokens": config.get("max_tokens")
        }
    }
    
    if error:
        output_data["error"] = error
        output_data["success"] = False
    else:
        output_data["result"] = result
        output_data["success"] = True
    
    if config.get("include_metadata", True):
        output_data["metadata"] = {
            "agent_type": "self-ask-with-search",
            "tools_used": ["Intermediate Answer"]
        }
    
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    logger.info(f"Output saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Run LangChain self-ask-with-search agent")
    parser.add_argument("--input", type=str, help="Input text or path to input file")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Load configuration
    config_path = args.config if args.config else "input.json"
    config = load_config(config_path)
    
    # Set up logging level from config
    log_level = config.get("error_handling", {}).get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    try:
        # Initialize LLM
        llm = initialize_llm(config)
        logger.info("LLM initialized successfully")
        
        # Initialize tools
        tools = initialize_tools(config, llm)
        if not tools:
            raise ValueError("No tools were initialized")
        logger.info(f"Tools initialized: {[tool.name for tool in tools]}")
        
        # Create prompt
        prompt = create_prompt()
        
        # Create agent
        from langchain.agents import create_self_ask_with_search_agent
        agent = create_self_ask_with_search_agent(llm, tools, prompt)
        
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
            user_input = read_input(args.input)
        else:
            user_input = config.get("default_input", "Hello, how can you help me?")
        
        logger.info(f"Processing input: {user_input[:100]}...")
        
        # Execute agent
        result = agent_executor.invoke({"input": user_input})
        
        # Extract the actual output
        if isinstance(result, dict):
            output = result.get("output", str(result))
        else:
            output = str(result)
        
        # Save output
        save_output(output, args.output, config)
        logger.info("Agent execution completed successfully")
        
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        if config.get("error_handling", {}).get("save_errors_to_output", True):
            save_output(None, args.output, config, error=str(e))
        raise

if __name__ == "__main__":
    main()