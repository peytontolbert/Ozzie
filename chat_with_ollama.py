"""
Module Description:

This module provides a class `ChatGPT` that enables chat functionality with OpenAI models.

Classes and Functions:

* `ChatGPT`: A class for processing thoughts and chatting with AI models.
"""

import openai
import os
from dotenv import load_dotenv
import time
import requests
import aiohttp
import json
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    """
    A class for processing thoughts and chatting with AI models.

    Attributes:
        None

    Methods:
        process_thought(thought, message="", goal=""): Processes a thought using an OpenAI model.
        chat_with_gpt3(system_prompt, prompt, retries=5, delay=5): Makes a request to the OpenAI API.
        chat_with_local_llm(system_prompt, prompt, retries=5, delay=5): Uses a local LLM for chatting.
    """

    def __init__(self):
        """
        Initializes the ChatGPT class.

        Args:
            None
        Returns:
            None
        """
        self.base_url = "http://localhost:11434/api/generate"  # Adjust this URL if needed
        self.logger = logging.getLogger(__name__)
        self.models = ["hermes3"]  # Add more models as fallbacks

    async def chat_with_ollama(self, prompt, model="hermes3"):
        for model_name in self.models:
            try:
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "model": "hermes3",
                        "prompt": f"{prompt}",
                        "stream": False,
                    }
                    async with session.post(self.base_url, json=payload) as response:
                        if response.status == 200:
                            result = await response.json()
                            if 'response' in result:
                                return result['response']
                            else:
                                self.logger.warning(f"Unexpected response structure: {result}")
                                return f"Error: Unexpected response structure"
                        else:
                            error_text = await response.text()
                            self.logger.error(f"Ollama API error: Status {response.status}, Response: {error_text}")
                            return f"Error: {response.status} - {error_text}"
            except aiohttp.ClientError as e:
                self.logger.error(f"Ollama API connection error: {str(e)}")
                return f"Error: Connection failed - {str(e)}"
            except Exception as e:
                self.logger.error(f"Unexpected error in chat_with_ollama: {str(e)}")
                return f"Error: Unexpected - {str(e)}"
        
        return "Error: No available models found"

    def chat_with_ollama_nojson(self, system_prompt: str, prompt: str, retries: int=5, delay: int=5):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "hermes3",
            "prompt": f"{system_prompt}\n{prompt}",
            "stream": False,
        }
        headers = {"Content-Type": "application/json"}
        for i in range(retries):
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                response = response.json()
                return response['response']
            except requests.exceptions.RequestException as e:
                if i < retries - 1:  # i is zero indexed
                    time.sleep(delay)  # wait before trying again
                else:
                    raise e  # re-raise the last exception if all retries fail
