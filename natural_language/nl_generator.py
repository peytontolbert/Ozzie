from chat_with_ollama import ChatGPT
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class NLGenerator:
    def __init__(self):
        self.chat_gpt = ChatGPT()
        self.logger = Logger("NLGenerator")
        self.error_handler = ErrorHandler()

    async def generate_text(self, prompt, max_tokens=100):
        try:
            system_prompt = "You are an AI assistant that generates text based on given prompts. Respond within the specified token limit."
            full_prompt = f"{prompt}\nToken limit: {max_tokens}"
            response = await self.chat_gpt.chat_with_ollama(system_prompt, full_prompt)
            return response[:max_tokens]  # Ensure we don't exceed the token limit
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating text")
            return None

    async def summarize_text(self, text, max_tokens=50):
        try:
            system_prompt = "You are an AI assistant that summarizes text. Provide a concise summary within the specified token limit."
            prompt = f"Summarize the following text in {max_tokens} tokens or less:\n\n{text}"
            summary = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            return summary[:max_tokens]  # Ensure we don't exceed the token limit
        except Exception as e:
            self.error_handler.handle_error(e, "Error summarizing text")
            return None

    async def generate_response(self, user_input, context, max_tokens=100):
        try:
            system_prompt = f"You are an AI assistant. Use the following context to respond to the user within {max_tokens} tokens: {context}"
            response = await self.chat_gpt.chat_with_ollama(system_prompt, user_input)
            return response[:max_tokens]  # Ensure we don't exceed the token limit
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating response")
            return None