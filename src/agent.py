import pandas as pd
import hashlib
from langgraph.graph import StateGraph,  END
from pdf_extractor import PdfTextExtractor
from llm_model import LLMQuery
from cache_node import Cache  # Import the Cache class
from typing import TypedDict
from typing_extensions import Annotated
import re
# Define the state for our workflow
class State(TypedDict):
    pdf_path: str
    pdf_text: str
    answers: list
    df: pd.DataFrame


class LLMAgentWorkflow:
    def __init__(self, cache_dir="cache"):
        # Initialize cache and workflow
        self.cache = Cache(cache_dir=cache_dir)  # Specify the cache directory
        self.workflow = StateGraph(State)

        # Add nodes to our graph
        self.workflow.add_node("extract_pdf_text", self.extract_pdf_text)
        self.workflow.add_node("query_llm", self.query_llm)
        self.workflow.add_node("format_answers", self.format_answers)

        # Set entry point and connect the nodes
        self.workflow.set_entry_point("extract_pdf_text")
        self.workflow.add_edge("extract_pdf_text", "query_llm")
        self.workflow.add_edge("query_llm", "format_answers")
        self.workflow.add_edge("format_answers", END)
        
        # Compile the workflow
        self.app = self.workflow.compile()

    def run(self, pdf_path: str) -> pd.DataFrame:
        """Run the agent workflow with a given PDF path."""

        inputs = {"pdf_path": pdf_path}
        output = self.app.invoke(inputs) 
      
        return output.get("df", pd.DataFrame())


    def extract_pdf_text(self, state: State) -> dict:
        """Extract text from the provided PDF."""
        extractor = PdfTextExtractor(state['pdf_path'])
        pdf_text = extractor.run()
        return {"pdf_text": pdf_text}

    def query_llm(self, state: State) -> dict:
        """Query the model with predefined questions and process multiple biochars."""
        cache_key = self.generate_cache_key(state["pdf_path"])
        cached_answers = self.get_cached_answers(cache_key)
        if cached_answers:
            return {"answers": cached_answers}
        answers = self.query_llm_model(state["pdf_text"])
        self.cache.set(cache_key, answers)
        return {"answers": answers}


    def generate_cache_key(self, pdf_path: str) -> str:
        """Generate a unique cache key based on the PDF path."""
        return hashlib.sha256(pdf_path.encode()).hexdigest()

    def get_cached_answers(self, cache_key: str) -> list:
        """Fetch cached answers from the cache if available."""
        return self.cache.get(cache_key)

    def query_llm_model(self, pdf_text: str) -> dict:
        """Query the LLM for biochars and extract their details in one go."""
        
        # Initialize LLMQuery with the extraction question
        
        llm = LLMQuery(
            "Extract the following details for each biochar found in the document:\n"
            "1. Name of the biochar\n"
            "2. Targeted species\n"
            "3. Adsorption capacity\n"
            "4. Location (if the biochar is mentioned in a table, use the table number. If it is mentioned in plain text, use the title of the section where the information is found)\n\n"
            "Please format the response as follows, using '-' as a separator:\n"
            "Biochar Name - Targeted Molecule - Adsorption Capacity - Location"
        )

        # Run the LLM query
        answers = llm.run(pdf_text)
        
       
        # Return the structured answers (one line per biochar)
        return answers.split("\n")


    def format_answers(self, state: dict) -> dict:
        """Format the extracted biochar details into a pandas DataFrame."""
        answers = state["answers"]
        
        biochars = []
        targeted_molecules = []
        adsorption_capacities = []
        locations = []

        for entry in answers:
            # Skip the first line if it contains "Targeted Molecule"
            if "Targeted" in entry:
                continue

            parts = entry.split("-")  # Splitting by ' - ' as per format
            if len(parts) == 4:  # Ensure all fields exist

                # Remove leading numbers (e.g., 1., 2.) and any surrounding asterisks from the biochar field
                biochar = re.sub(r'^\d+\.\s*\*?([^*]+)\*?$', r'\1', parts[0].strip())
                
                # Remove all asterisks from the other fields (targeted molecules, adsorption capacities, and locations)
                targeted_molecule = re.sub(r'\*', '', parts[1].strip())  # Remove all asterisks
                adsorption_capacity = re.sub(r'\*', '', parts[2].strip())  # Remove all asterisks
                location = re.sub(r'\*', '', parts[3].strip())  # Remove all asterisks

                biochars.append(biochar)
                targeted_molecules.append(targeted_molecule)
                adsorption_capacities.append(adsorption_capacity)
                locations.append(location)

        data = {
            "Biochar": biochars,
            "Targeted Molecule": targeted_molecules,
            "Adsorption Capacity": adsorption_capacities,
            "Location": locations
        }

        df = pd.DataFrame(data)

        return {"df": df}
