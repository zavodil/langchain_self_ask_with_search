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
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import AgentExecutor, create_self_ask_with_search_agent
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain import hub
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
            logger.warning(f"Error loading config from {config_path}: {e}. Using defaults.")
    
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
    
    # For self-ask-with-search agent, we need exactly one tool named "Intermediate Answer"
    # We'll use the search tool for this purpose
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search_tool = DuckDuckGoSearchRun()
        # Rename it to "Intermediate Answer" as required by self-ask-with-search agent
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search engine for finding intermediate answers to questions",
            func=search_tool.run
        )
        tools.append(intermediate_answer_tool)
        logger.info("Initialized Intermediate Answer tool (search)")
    except Exception as e:
        logger.error(f"Error initializing search tool: {e}")
        # Create a fallback tool
        def fallback_search(query: str) -> str:
            return f"Unable to search for: {query}"
        
        tools.append(Tool(
            name="Intermediate Answer",
            description="Fallback search tool",
            func=fallback_search
        ))
    
    return tools

def get_input_text(input_arg: str) -> str:
    """Get input text from argument (either direct text or file path)."""
    if os.path.isfile(input_arg):
        try:
            with open(input_arg, 'r') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error reading input file {input_arg}: {e}")
            return input_arg
    return input_arg

def save_output(result: Any, output_path: str, config: Dict[str, Any], input_text: str) -> None:
    """Save the output to a JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "result": str(result) if not isinstance(result, (dict, list)) else result,
        "status": "success"
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
        logger.error(f"Error saving output: {e}")

def main():
    """Main function to run the LangChain agent."""
    parser = argparse.ArgumentParser(description="Run a LangChain self-ask-with-search agent")
    parser.add_argument("--input", type=str, help="Input text or path to input file")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, default="input.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Get input text
    if args.input:
        input_text = get_input_text(args.input)
    else:
        input_text = config.get("default_input", "Hello, how can you help me?")
    
    logger.info(f"Processing input: {input_text[:100]}...")
    
    try:
        # Initialize LLM
        llm = initialize_llm(config)
        logger.info("LLM initialized successfully")
        
        # Initialize tools
        tools = initialize_tools(config, llm)
        logger.info(f"Initialized {len(tools)} tools")
        
        # Get prompt
        try:
            prompt = hub.pull("hwchase17/self-ask-with-search")
            logger.info("Loaded prompt from hub")
        except Exception as e:
            logger.warning(f"Could not load prompt from hub: {e}. Creating default prompt.")
            prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad"],
                template="""Question: {input}
Are followup questions needed here:{agent_scratchpad}"""
            )
        
        # Create agent
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
        
        # Execute agent
        result = agent_executor.invoke({"input": input_text})
        logger.info("Agent execution completed")
        
        # Save output
        save_output(result, args.output, config, input_text)
        
    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
        error_output = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "error": str(e),
            "status": "error"
        }
        
        if config.get("error_handling", {}).get("save_errors_to_output", True):
            with open(args.output, 'w') as f:
                json.dump(error_output, f, indent=2)
            logger.info(f"Error details saved to {args.output}")

if __name__ == "__main__":
    main()