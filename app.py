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
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain.agents.self_ask_with_search.prompt import PROMPT
from langchain.agents import create_self_ask_with_search_agent
from typing import Sequence

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str = "input.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
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
    tool_config = config.get('tool_config', {})
    
    # For self-ask-with-search, we need exactly one tool named "Intermediate Answer"
    # We'll use the search tool for this purpose
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search_tool = DuckDuckGoSearchRun()
        # Rename to "Intermediate Answer" as required by self-ask-with-search
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search the internet for intermediate answers",
            func=search_tool.run
        )
        tools.append(intermediate_answer_tool)
    except ImportError as e:
        if tool_config.get('handle_import_errors', True):
            logger.warning(f"Could not import search tool: {e}")
            # Create a dummy tool if needed
            def dummy_search(query: str) -> str:
                return f"Search functionality not available. Query: {query}"
            
            intermediate_answer_tool = Tool(
                name="Intermediate Answer",
                description="Dummy search tool",
                func=dummy_search
            )
            tools.append(intermediate_answer_tool)
        else:
            raise
    
    return tools

def get_input(args: argparse.Namespace, config: Dict[str, Any]) -> str:
    """Get input from command line or file."""
    if args.input:
        if os.path.isfile(args.input):
            with open(args.input, 'r') as f:
                return f.read().strip()
        else:
            return args.input
    else:
        return config.get('default_input', 'Hello, how can you help me?')

def save_output(result: Any, output_path: str, config: Dict[str, Any], error: Exception = None):
    """Save output to JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "success": error is None
    }
    
    if config.get('include_metadata', True):
        output_data["metadata"] = {
            "llm_model": config.get('llm_model', 'claude-opus-4-20250514'),
            "temperature": config.get('temperature', 0.7),
            "max_tokens": config.get('max_tokens', 2000)
        }
    
    if error:
        output_data["error"] = str(error)
        if config.get('error_handling', {}).get('save_errors_to_output', True):
            output_data["error_details"] = {
                "type": type(error).__name__,
                "message": str(error)
            }
    else:
        output_data["result"] = result
    
    try:
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        logger.info(f"Output saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving output: {e}")

def main():
    """Main function to run the LangChain agent."""
    parser = argparse.ArgumentParser(description='Run LangChain agent')
    parser.add_argument('--input', type=str, help='Input text or file path')
    parser.add_argument('--output', type=str, default='output.json', help='Output file path')
    parser.add_argument('--config', type=str, default='input.json', help='Configuration file path')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set logging level
    log_level = config.get('error_handling', {}).get('log_level', 'INFO')
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    try:
        # Initialize LLM
        llm = initialize_llm(config)
        
        # Initialize tools
        tools = initialize_tools(config, llm)
        
        # Create prompt
        try:
            from langchain import hub
            prompt = hub.pull("hwchase17/self-ask-with-search")
        except Exception as e:
            logger.warning(f"Could not pull prompt from hub: {e}, using default")
            prompt = PROMPT
        
        # Create agent
        agent = create_self_ask_with_search_agent(llm, tools, prompt)
        
        # Create agent executor
        agent_config = config.get('agent_config', {})
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=agent_config.get('verbose', True),
            max_iterations=agent_config.get('max_iterations', 10),
            early_stopping_method=agent_config.get('early_stopping_method', 'generate')
        )
        
        # Get input
        user_input = get_input(args, config)
        
        # Execute agent
        result = agent_executor.invoke({"input": user_input})
        
        # Save output
        save_output(result, args.output, config)
        
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        save_output(None, args.output, config, error=e)
        raise

if __name__ == "__main__":
    main()