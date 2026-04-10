import os
import google.generativeai as genai
from typing import Dict, Any, List
import json

class IntelligenceService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def process_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Processes audio file using Gemini 1.5 to extract transcript, summary, tasks, and decisions.
        """
        # Upload file to Gemini API
        sample_file = genai.upload_file(path=audio_path)
        
        prompt = """
        Analyze this meeting audio and provide the output in JSON format with the following keys:
        - transcript: The full text transcript of the meeting.
        - summary: A concise summary of what was discussed.
        - action_items: A list of tasks assigned to specific people.
        - decisions: A list of key decisions made during the meeting.
        - topics: A list of main topics discussed.

        The JSON should be valid and well-formatted.
        """

        response = self.model.generate_content([sample_file, prompt])
        
        # Clean up the file from Gemini storage
        genai.delete_file(sample_file.name)

        # Parse JSON from response
        try:
            # Gemini might wrap JSON in markdown code blocks
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return {
                "transcript": response.text,
                "summary": "Extraction failed",
                "action_items": [],
                "decisions": [],
                "topics": []
            }

service = IntelligenceService(api_key=os.getenv("GOOGLE_API_KEY", ""))
