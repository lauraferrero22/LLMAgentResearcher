from agent import LLMAgentWorkflow

if __name__ == "__main__":
    # Path to the research paper PDF and cache directory
    pdf_path = "data/research_paper.pdf"
    cache_dir = "cache"  # Specify the cache directory

    
    # Create the agent workflow instance
    agent = LLMAgentWorkflow(cache_dir=cache_dir)  # Initialize the workflow with cache path
        
    # Running the agent and obtaining results as a DataFrame
    result_df = agent.run(pdf_path)
    
    # Display the results
    print("Results in DataFrame format:")
    print(result_df)