"""
AI-powered research engine using OpenAI GPT-4
Flushes out initial ideas with deep research, sources, and data
"""
from openai import OpenAI
from typing import Dict, List, Optional
import json
from ..config import Config


class ResearchEngine:
    """Conducts AI-powered research on topics"""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"

    def research_topic(self, initial_idea: str, depth: str = "deep") -> Dict:
        """
        Research a topic deeply using AI

        Args:
            initial_idea: The initial topic or idea to research
            depth: Research depth - 'quick', 'medium', or 'deep'

        Returns:
            Dict containing research results, sources, key points, and statistics
        """
        depth_prompts = {
            "quick": "Provide a brief overview with 3-5 key points",
            "medium": "Provide comprehensive research with 5-8 key points and some statistics",
            "deep": "Provide in-depth research with 8-12 key points, statistics, expert insights, and multiple angles"
        }

        prompt = f"""You are a research assistant helping create viral Twitter content.

Research Topic: {initial_idea}

Instructions: {depth_prompts.get(depth, depth_prompts['deep'])}

Please provide your research in the following JSON format:
{{
    "main_topic": "Clear topic title",
    "hook": "Attention-grabbing opening statement (max 280 chars)",
    "key_points": [
        {{"point": "Key insight 1", "evidence": "Supporting data/fact"}},
        {{"point": "Key insight 2", "evidence": "Supporting data/fact"}}
    ],
    "statistics": [
        {{"stat": "Impressive number/percentage", "context": "What it means"}},
    ],
    "expert_insights": [
        {{"insight": "Expert opinion or quote", "attribution": "Source/expert name"}}
    ],
    "controversial_angles": [
        "Contrarian viewpoint 1",
        "Debate-worthy angle 2"
    ],
    "trending_connections": [
        "How this relates to current trend 1",
        "Connection to popular topic 2"
    ],
    "actionable_takeaways": [
        "Practical tip 1",
        "Actionable advice 2"
    ],
    "viral_potential_score": 8.5,
    "recommended_hashtags": ["#hashtag1", "#hashtag2"],
    "sources": [
        "Source 1 (general reference)",
        "Source 2 (general reference)"
    ]
}}

Make the content factual, engaging, and optimized for Twitter virality."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert researcher who creates comprehensive, accurate, and engaging research for social media content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            research_data = json.loads(response.choices[0].message.content)
            return research_data

        except Exception as e:
            raise Exception(f"Research failed: {str(e)}")

    def enhance_with_web_context(self, research_data: Dict, query: str) -> Dict:
        """
        Enhance research with current web context and trends
        (Placeholder for future web scraping integration)
        """
        # TODO: Add web scraping for real-time data
        # For now, return research as-is
        return research_data

    def find_viral_angles(self, topic: str) -> List[str]:
        """
        Find multiple viral angles for a topic

        Returns:
            List of different angles/perspectives on the topic
        """
        prompt = f"""Given this topic: "{topic}"

Suggest 5 different viral angles or perspectives that would make great Twitter threads.
Each angle should be unique, attention-grabbing, and shareable.

Respond with a JSON array of angles:
["Angle 1", "Angle 2", "Angle 3", "Angle 4", "Angle 5"]"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral content strategist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result.get("angles", [])

        except Exception as e:
            return [topic]
