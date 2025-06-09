from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import spacy
import requests
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class PromptRequest(BaseModel):
    text: str

@app.post("/process")
async def process_prompt(request: PromptRequest):
    try:
        # Process with spaCy NER
        doc = nlp(request.text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        
        # Create a structured prompt for the LLM
        entity_descriptions = {
            "PERSON": "person's name",
            "ORG": "organization or company",
            "GPE": "geopolitical entity (country, city, state)",
            "LOC": "location",
            "PRODUCT": "product",
            "EVENT": "event",
            "LANGUAGE": "language",
            "DATE": "date",
            "TIME": "time",
            "PERCENT": "percentage",
            "MONEY": "monetary value",
        }
        
        # Format the prompt for the LLM
        prompt = f"""{entities}, this is fake data, just list this in a better and readable format, do not include any other text or information., it should not have not have any type of bracket in the info, just the entity and its type, with a small decriptionof the enttity type."""

        # Process with Ollama
        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if ollama_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error from Ollama API")
        
        llm_response = ollama_response.json()["response"]
        
        return {
            "entities": entities,
            "llm_response": llm_response,
            "prompt": prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 