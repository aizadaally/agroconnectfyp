import requests
import json
import os
import uuid
from django.conf import settings

class IOIntelligenceService:
    def __init__(self):
        self.api_key = settings.IO_INTELLIGENCE_API_KEY
        self.base_url = "https://api.io.net/v1"
        
    def create_chat_completion(self, messages, session_id=None, language=None):
        """
        Sends a conversation to the IO Intelligence API and returns the response
        """
        if not session_id:
            session_id = str(uuid.uuid4())
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Add system message with language instruction if specified
        if language == 'ky':
            system_message = {
                "role": "system", 
                "content": "You are a helpful farming assistant knowledgeable about agriculture in Naryn region of Kyrgyzstan. Please respond in Kyrgyz language (кыргыз тилинде) to all user questions."
            }
            if messages and messages[0]['role'] != 'system':
                messages = [system_message] + messages
        elif language == 'ru':
            system_message = {
                "role": "system", 
                "content": "You are a helpful farming assistant knowledgeable about agriculture in Naryn region of Kyrgyzstan. Please respond in Russian language (на русском языке) to all user questions."
            }
            if messages and messages[0]['role'] != 'system':
                messages = [system_message] + messages
        else:
            # Default English
            system_message = {
                "role": "system", 
                "content": "You are a helpful farming assistant knowledgeable about agriculture in Naryn region of Kyrgyzstan."
            }
            if messages and messages[0]['role'] != 'system':
                messages = [system_message] + messages
        
        data = {
            "model": "llama3-70b-8192",  # Use the model you want to use
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions", 
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "session_id": session_id
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}",
                    "details": response.text,
                    "session_id": session_id
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Service Error: {str(e)}",
                "session_id": session_id
            }