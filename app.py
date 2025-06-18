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
from typing import Sequence

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
    tool_config = config.get("tool_config", {})
    
    # For self-ask-with-search agent, we need exactly one tool named "Intermediate Answer"
    # We'll use the search tool for this purpose
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search_tool = DuckDuckGoSearchRun()
        # Rename the tool to "Intermediate Answer" as required by self-ask-with-search
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search the internet for intermediate answers",
            func=search_tool.run
        )
        tools.append(intermediate_answer_tool)
    except ImportError as e:
        logger.error(f"Error importing search tool: {e}")
        if tool_config.get("handle_import_errors", True):
            # Create a dummy tool if import fails
            def dummy_search(query: str) -> str:
                return f"Search functionality not available. Query: {query}"
            
            tools.append(Tool(
                name="Intermediate Answer",
                description="Dummy search tool",
                func=dummy_search
            ))
    
    return tools

def load_input(input_source: str) -> str:
    """Load input from file or return as string."""
    if os.path.isfile(input_source):
        try:
            with open(input_source, 'r') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            return input_source
    return input_source

def save_output(result: Any, output_path: str, config: Dict[str, Any], input_text: str):
    """Save the output to a JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "result": str(result) if result else None,
        "config": config
    }
    
    if config.get("include_metadata", True):
        output_data["metadata"] = {
            "agent_type": "self_ask_with_search",
            "model": config.get("llm_model", "unknown"),
            "temperature": config.get("temperature", 0.7),
            "max_tokens": config.get("max_tokens", 2000)
        }
    
    try:
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        logger.info(f"Output saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving output: {e}")

def main():
    parser = argparse.ArgumentParser(description="Run LangChain self-ask-with-search agent")
    parser.add_argument("--input", type=str, help="Input text or path to input file")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, default="input.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set up logging level from config
    log_level = config.get("error_handling", {}).get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    # Get input
    if args.input:
        input_text = load_input(args.input)
    else:
        input_text = config.get("default_input", "Hello, how can you help me?")
    
    logger.info(f"Processing input: {input_text[:100]}...")
    
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
            logger.warning(f"Could not pull prompt from hub: {e}. Using default prompt.")
            prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad"],
                template="""Question: {input}
Are followup questions needed here:{agent_scratchpad}"""
            )
        
        # Create agent
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
        
        # Execute agent
        result = agent_executor.invoke({"input": input_text})
        
        logger.info("Agent execution completed successfully")
        
    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
        result = {"error": str(e)} if config.get("error_handling", {}).get("save_errors_to_output", True) else None
    
    # Save output
    save_output(result, args.output, config, input_text)

if __name__ == "__main__":
    main()