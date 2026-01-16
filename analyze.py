import json
from typing import Any, Dict
from google import genai

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL = "gemini-3-flash-preview"

client = genai.Client()

def validate_schema(data: Dict[str, Any]) -> None:
    required_fields = ["destination", "price_range", "ideal_visit_times", "top_attractions"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")


def get_itinerary(destination: str) -> Dict[str, Any]:
    prompt = f"""Generate a travel itinerary in JSON format with the following exact schema:

{{
  "destination": "",
  "price_range": "",
  "ideal_visit_times": ["<time period 1>", "<time period 2>", ......],
  "top_attractions": ["<attraction 1>", "<attraction 2>", ......]
}}

Destination: {destination}

Return ONLY valid JSON. Do not include any explanations, markdown formatting, or code blocks."""
    
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1].strip()
            if text.startswith("json"):
                text = text[4:].strip()
        
        data = json.loads(text)
        validate_schema(data)
        return data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")
