# Technical Interview - LLM Engineer

## Problem Statement
Your goal is to create an LLM Agent to:
- Process the file provided in the `data` directory
- Answer the following questions on this PDF:
  - What is the biochar ?
  - What is the targeted molecule
  - What is the adsortion capacity of the biochar ?
  - Where is located the information (page number or section) ?

- Output format:
  - The output should be a table (dataframe, markdown or html)
  - Each new row should correspond to a new biochar
  - Each column should be a question

### Example (not exhaustive):

![output](./docs/output.png)

## Prerequisites
- The data is provided in the `data` directory. The file is named `research_paper.pdf`
- You will be given an OpenAI API key with 10$ to conduct your experiments


## Deliverables
We expect you to provide us with:
- Some python scripts that implements the LLM Agent in `src` directory
- Your coding good practises

## Hints
- Use well known agentic framewords to speed up you experiments
- Use cache features in developement to avoid unnecessary API calls (you are limited to $10 of API calls)


