from dotenv import load_dotenv
load_dotenv()
import os
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.tools import BaseTool, Tool
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain_core.prompts import PromptTemplate

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
    # We'll use the search tool for this purpose
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        # Wrap it with the required name
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search for intermediate answers",
            func=search.run
        )
        tools.append(intermediate_answer_tool)
        logger.info("Initialized Intermediate Answer tool for self-ask-with-search")
    except Exception as e:
        logger.error(f"Error initializing search tool: {e}")
        # Create a dummy tool if search fails
        def dummy_search(query: str) -> str:
            return f"Search results for: {query}"
        
        intermediate_answer_tool = Tool(
            name="Intermediate Answer",
            description="Search for intermediate answers",
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
        logger.warning(f"Could not pull prompt from hub: {e}")
        # Create a fallback prompt
        template = """Question: Who lived longer, Muhammad Ali or Alan Turing?
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali

Question: When was the founder of craigslist born?
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952

Question: Who was the maternal grandfather of George Washington?
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball

Question: Are both the directors of Jaws and Casino Royale from the same country?
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate answer: New Zealand.
So the final answer is: No

Question: {input}
Are follow up questions needed here:{agent_scratchpad}"""
        
        return PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"]
        )

def read_input(input_source: str) -> str:
    """Read input from either a file or direct text."""
    if os.path.isfile(input_source):
        with open(input_source, 'r') as f:
            return f.read().strip()
    return input_source

def save_output(result: Any, output_path: str, config: Dict[str, Any], error: str = None) -> None:
    """Save the output to a JSON file."""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "success": error is None,
        "result": str(result) if result else None,
        "error": error,
        "config": {
            "llm_model": config.get("llm_model"),
            "temperature": config.get("temperature"),
            "max_tokens": config.get("max_tokens")
        }
    }
    
    if config.get("include_metadata", True):
        output_data["metadata"] = {
            "agent_type": "self-ask-with-search",
            "tools_used": ["Intermediate Answer"],
            "execution_time": datetime.now().isoformat()
        }
    
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    logger.info(f"Output saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Run a LangChain self-ask-with-search agent")
    parser.add_argument("--input", type=str, help="Input text or path to input file")
    parser.add_argument("--output", type=str, default="output.json", help="Output file path")
    parser.add_argument("--config", type=str, default="input.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set up logging level from config
    log_level = config.get("error_handling", {}).get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    # Determine input
    if args.input:
        user_input = read_input(args.input)
    else:
        user_input = config.get("default_input", "Hello, how can you help me?")
    
    logger.info(f"Processing input: {user_input[:100]}...")
    
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
        
        # Execute agent
        result = agent_executor.invoke({"input": user_input})
        logger.info("Agent execution completed successfully")
        
        # Save output
        save_output(result, args.output, config)
        
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        save_output(None, args.output, config, error=str(e))

if __name__ == "__main__":
    main()