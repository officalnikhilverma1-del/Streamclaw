from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class SceneScriptwriter(BaseAgent):
    """Agent for converting stories into scene-by-scene scripts"""
    
    SYSTEM_PROMPT = """You are an experienced screenwriter and script formatter. Your task is to:
1. Break down detailed narratives into individual scenes
2. Generate clear scene headings and descriptions
3. Write dialogue that matches character voices
4. Include action descriptions and character movements
5. Specify scene transitions and technical directions
6. Format output as structured JSON for video production systems
7. Ensure each scene is self-contained yet connected to the narrative arc

Output format (JSON):
{
  "title": "Story Title",
  "total_scenes": number,
  "scenes": [
    {
      "scene_number": number,
      "scene_heading": "INT/EXT. LOCATION - TIME OF DAY",
      "description": "Scene setup and atmosphere",
      "characters": ["Character names"],
      "action": "Action descriptions and character movements",
      "dialogue": [
        {"character": "Name", "text": "Dialogue"},
      ],
      "transition": "CUT TO / FADE TO / etc"
    }
  ]
}"""
    
    def __init__(self):
        super().__init__(
            agent_name="Scene-by-Scene Scriptwriter",
            system_prompt=self.SYSTEM_PROMPT
        )
    
    def process(self, detailed_story: str) -> Dict[str, Any]:
        """
        Convert a detailed story into a scene-by-scene script
        
        Args:
            detailed_story: The detailed narrative from the Detailed Story Writer
        
        Returns:
            Dictionary containing the structured scene script
        """
        if not self.validate_input(detailed_story):
            logger.error("Invalid input provided to Scene Scriptwriter")
            return {"error": "Invalid input", "status": "failed"}
        
        try:
            logger.info("Converting story into scene-by-scene script")
            
            message = f"""Please convert this story into a detailed scene-by-scene script:

{detailed_story}

Break the story into individual scenes with:
- Clear scene headings (INT/EXT. LOCATION - TIME)
- Scene descriptions and atmosphere
- Character names and their actions
- Realistic dialogue
- Technical transitions
- Appropriate timing for video production

Format the output as valid JSON that can be parsed by video production software."""
            
            result = self.call_claude(message)
            
            # Attempt to parse as JSON
            try:
                script_data = json.loads(result)
            except json.JSONDecodeError:
                # If not valid JSON, return raw result
                script_data = {"raw_script": result}
            
            return {
                "status": "success",
                "script": script_data,
                "input_story": detailed_story[:500] + "..." if len(detailed_story) > 500 else detailed_story
            }
        
        except Exception as e:
            logger.error(f"Error in Scene Scriptwriter: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }