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
from langchain.agents import AgentExecutor, create_self_ask_with_search_agent
from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from collections.abc import Sequence

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_configuration(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from input.json or specified config file."""
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
    
    # Try to load input.json
    if os.path.exists("input.json"):
        try:
            with open("input.json", "r") as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
                logger.info("Loaded configuration from input.json")
        except Exception as e:
            logger.warning(f"Failed to load input.json: {e}")
    
    # Override with specified config file if provided
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                override_config = json.load(f)
                default_config.update(override_config)
                logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logger.warning(f"Failed to load {config_path}: {e}")
    
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
    # We'll use the search tool for this purpose
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search_tool = DuckDuckGoSearchRun()
        # Rename it to "Intermediate Answer" as required by self-ask-with-search
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search engine for finding information",
            func=search_tool.run
        )
        tools.append(intermediate_answer_tool)
        logger.info("Initialized Intermediate Answer tool (search)")
    except Exception as e:
        logger.error(f"Failed to initialize search tool: {e}")
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
    """Create or load the prompt template."""
    try:
        from langchain import hub
        prompt = hub.pull("hwchase17/self-ask-with-search")
        logger.info("Loaded prompt from hub")
        return prompt
    except Exception as e:
        logger.warning(f"Failed to load prompt from hub: {e}")
        # Create a default self-ask prompt
        template = """Question: {input}

Are follow up questions needed here? Yes.
Follow up: {agent_scratchpad}"""
        
        return PromptTemplate(
            input_variables=["input", "agent_scratchpad"],
            template=template
        )

def process_input(input_arg: str) -> str:
    """Process input - either direct text or file path."""
    if os.path.isfile(input_arg):
        try:
            with open(input_arg, 'r') as f:
                content = f.read().strip()
                logger.info(f"Loaded input from file: {input_arg}")
                return content
        except Exception as e:
            logger.error(f"Failed to read file {input_arg}: {e}")
            return input_arg
    return input_arg

def save_output(result: Any, output_path: str, config: Dict[str, Any], error: str = None):
    """Save the output to a JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "success": error is None,
        "result": str(result) if result else None,
        "error": error
    }
    
    if config.get("include_metadata", True):
        output_data["metadata"] = {
            "llm_model": config.get("llm_model"),
            "temperature": config.get("temperature"),
            "max_tokens": config.get("max_tokens"),
            "agent_type": "self_ask_with_search"
        }
    
    try:
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        logger.info(f"Output saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save output: {e}")

def main():
    """Main function to run the LangChain agent."""
    parser = argparse.ArgumentParser(description="Run LangChain self-ask-with-search agent")
    parser.add_argument("--input", type=str, help="Input text or file path")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_configuration(args.config)
    
    # Set up logging level from config
    log_level = config.get("error_handling", {}).get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    try:
        # Initialize LLM
        llm = initialize_llm(config)
        logger.info("Initialized LLM")
        
        # Initialize tools
        tools = initialize_tools(config, llm)
        if not tools:
            raise ValueError("No tools initialized")
        logger.info(f"Initialized {len(tools)} tools")
        
        # Create prompt
        prompt = create_prompt()
        logger.info("Created prompt template")
        
        # Create agent
        agent = create_self_ask_with_search_agent(llm, tools, prompt)
        logger.info("Created self-ask-with-search agent")
        
        # Create agent executor
        agent_config = config.get("agent_config", {})
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=agent_config.get("verbose", True),
            max_iterations=agent_config.get("max_iterations", 10),
            early_stopping_method=agent_config.get("early_stopping_method", "generate")
        )
        logger.info("Created agent executor")
        
        # Get input
        if args.input:
            input_text = process_input(args.input)
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
        save_output(None, args.output, config, str(e))

if __name__ == "__main__":
    main()