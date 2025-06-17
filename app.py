from dotenv import load_dotenv
load_dotenv()
import os
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
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

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
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
    
    config_file = config_path or "input.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
                logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.warning(f"Error loading config from {config_file}: {e}")
    
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
        search_tool = DuckDuckGoSearchRun()
        # Rename it to "Intermediate Answer" as required by self-ask-with-search
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
            return f"Search results for: {query}"
        
        tools.append(Tool(
            name="Intermediate Answer",
            description="Search for intermediate answers",
            func=dummy_search
        ))
    
    return tools

def create_prompt(config: Dict[str, Any]) -> BasePromptTemplate:
    """Create the prompt template for the agent."""
    try:
        from langchain import hub
        prompt = hub.pull("hwchase17/self-ask-with-search")
        logger.info("Successfully pulled prompt from hub")
        return prompt
    except Exception as e:
        logger.warning(f"Could not pull prompt from hub: {e}")
        # Create a default self-ask prompt
        template = """Question: {input}

Are follow up questions needed here: Yes.
Follow up: {agent_scratchpad}
"""
        return PromptTemplate(
            input_variables=["input", "agent_scratchpad"],
            template=template
        )

def load_input(input_source: str) -> str:
    """Load input from file or return as string."""
    if os.path.isfile(input_source):
        with open(input_source, 'r') as f:
            return f.read().strip()
    return input_source

def save_output(output_data: Dict[str, Any], output_path: str = "output.json"):
    """Save the output data to a JSON file."""
    try:
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        logger.info(f"Output saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving output: {e}")

def main():
    """Main function to run the LangChain agent."""
    parser = argparse.ArgumentParser(description="Run a LangChain self-ask-with-search agent")
    parser.add_argument("--input", type=str, help="Input text or path to input file")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set up logging level from config
    log_level = config.get("error_handling", {}).get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    # Initialize components
    try:
        llm = initialize_llm(config)
        tools = initialize_tools(config, llm)
        prompt = create_prompt(config)
        
        # Create the agent
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
            input_text = load_input(args.input)
        else:
            input_text = config.get("default_input", "Hello, how can you help me?")
        
        # Execute agent
        logger.info(f"Executing agent with input: {input_text}")
        start_time = datetime.now()
        
        result = agent_executor.invoke({"input": input_text})
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Prepare output
        output_data = {
            "input": input_text,
            "output": result.get("output", ""),
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }
        
        if config.get("include_metadata", True):
            output_data["metadata"] = {
                "model": os.getenv('DEFAULT_MODEL_NAME', config.get('llm_model', 'claude-opus-4-20250514')),
                "temperature": config.get("temperature", 0.7),
                "max_tokens": config.get("max_tokens", 2000),
                "tools_used": [tool.name for tool in tools],
                "agent_type": "self-ask-with-search"
            }
        
        # Save output
        save_output(output_data, args.output)
        
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        error_output = {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "input": args.input or config.get("default_input", "")
        }
        save_output(error_output, args.output)
        raise

if __name__ == "__main__":
    main()