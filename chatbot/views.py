# chatbot/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import uuid
import os
import requests
import traceback
from django.conf import settings

from .models import ChatSession, ChatMessage

@login_required
def chat_page(request):
    """Render the chatbot interface page"""
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def chat_api(request):
    """API endpoint to handle chat messages"""
    print(f"Request method: {request.method}")
    
    if request.method != 'POST':
        return JsonResponse({'error': f'Only POST method is allowed. You sent {request.method}'}, status=405)
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        language = data.get('language', 'en')
        
        print(f"Received message: {message}")
        print(f"Session ID: {session_id}")
        print(f"Language: {language}")
        
        if not message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
        # Ensure session_id is never None
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # Get or create a chat session using try/except to avoid NULL session_id
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(
                session_id=session_id,
                user=request.user if request.user.is_authenticated else None
            )
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=message
        )
        
        # Get API key from settings
        api_key = settings.IO_INTELLIGENCE_API_KEY
        
        # Prepare language-specific system instructions
        if language == 'ky':
            system_message = (
                "Сиз айыл чарба боюнча жардам берүүчү ассистентсиз. "
                "Сиз Нарын областындагы айыл чарбасы жөнүндө билимдүүсүз. "
                "Бардык суроолорго кыргызча жооп бериңиз. "
                "Нарын областы - Кыргызстандын тоолуу аймагы, бийик тоолуу климаты бар, "
                "негизинен мал чарбачылыгы, жайыт чарбачылыгы жана айрым айыл чарба өсүмдүктөрү өстүрүлөт."
            )
        elif language == 'ru':
            system_message = (
                "Вы ассистент по сельскому хозяйству, обладающий знаниями о сельском хозяйстве "
                "в Нарынской области Кыргызстана. Пожалуйста, отвечайте на все вопросы на русском языке. "
                "Нарынская область - горный регион Кыргызстана с высокогорным климатом, "
                "в основном специализирующийся на животноводстве, пастбищном хозяйстве и некоторых сельскохозяйственных культурах."
            )
        else:
            system_message = (
                "You are a helpful farming assistant knowledgeable about agriculture "
                "in Naryn region of Kyrgyzstan. Please respond in English. "
                "The Naryn region is a mountainous area of Kyrgyzstan with a high-altitude climate, "
                "primarily focused on livestock, pasture management, and some agricultural crops."
            )
        
        # Get previous messages for context (limited to recent messages)
        previous_messages = list(ChatMessage.objects.filter(session=session).order_by('-timestamp')[1:6])
        previous_messages.reverse()  # Reverse to get chronological order
        
        # Format messages for the API
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add previous conversation context if available
        for msg in previous_messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add the current user message
        messages.append({"role": "user", "content": message})
        
        # Set up headers for API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Define possible endpoints and models to try
        endpoints = [
            "https://api.io.net/v1/chat/completions",
            "https://api.io.net/ai/v1/chat/completions",
            "https://api.io.net/ai/chat/completions"
        ]
        
        models = [
            "llama-3-70b-chat",
            "llama-3",
            "llama-3-8b-chat",
            "claude-3-opus",
            "gpt-4"
        ]
        
        response_received = False
        
        # Try different endpoints and models until one works
        for endpoint in endpoints:
            if response_received:
                break
                
            for model in models:
                if response_received:
                    break
                    
                print(f"Trying endpoint: {endpoint} with model: {model}")
                
                try:
                    api_data = {
                        "model": model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 800
                    }
                    
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json=api_data,
                        timeout=15
                    )
                    
                    print(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        response_received = True
                        response_data = response.json()
                        print(f"Response data: {response_data}")
                        
                        # Extract the assistant's message from the response
                        try:
                            assistant_message = response_data['choices'][0]['message']['content']
                        except (KeyError, IndexError):
                            try:
                                # Alternative format
                                assistant_message = response_data.get('response') or response_data.get('output', '')
                            except (KeyError, TypeError):
                                # Just use the whole response as a last resort
                                assistant_message = str(response_data)
                        
                        # Log the successful endpoint and model
                        print(f"✅ Success with endpoint: {endpoint} and model: {model}")
                        
                        # Save assistant message
                        ChatMessage.objects.create(
                            session=session,
                            role='assistant',
                            content=assistant_message
                        )
                        
                        return JsonResponse({
                            'response': assistant_message,
                            'session_id': session_id
                        })
                    else:
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('error', {}).get('message', str(error_data))
                        except:
                            error_msg = response.text
                            
                        print(f"Error with endpoint {endpoint} and model {model}: {error_msg}")
                except Exception as e:
                    print(f"Exception with endpoint {endpoint} and model {model}: {str(e)}")
        
        # If no successful API response was received, fall back to mock response
        print("All API combinations failed, using mock response.")
        assistant_message = mock_ai_response(message, language)
        
        # Save mock assistant message
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=assistant_message
        )
        
        return JsonResponse({
            'response': assistant_message,
            'session_id': session_id,
            'mock': True
        })
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Exception in chat_api: {str(e)}")
        print(error_traceback)
        
        # Try to use mock response even in case of general error
        try:
            if 'message' in locals() and 'language' in locals():
                assistant_message = mock_ai_response(message, language)
            else:
                assistant_message = "I'm sorry, I encountered an error processing your request."
                
            # Create a new session ID if needed
            if 'session_id' not in locals() or session_id is None:
                session_id = str(uuid.uuid4())
                
            return JsonResponse({
                'response': assistant_message,
                'error': str(e),
                'session_id': session_id,
                'mock': True
            })
        except:
            return JsonResponse({
                'error': str(e),
                'traceback': error_traceback,
                'session_id': session_id if 'session_id' in locals() else None
            }, status=500)

@login_required
def chat_history(request, session_id=None):
    """Endpoint to retrieve chat history"""
    if session_id:
        try:
            session = ChatSession.objects.get(session_id=session_id)
            # Ensure user can only access their own sessions
            if session.user != request.user and not request.user.is_staff:
                return JsonResponse({'error': 'Not authorized to access this session'}, status=403)
                
            messages = ChatMessage.objects.filter(session=session)
            
            history = [{
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages]
            
            return JsonResponse({'history': history, 'session_id': session_id})
            
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
    else:
        # List all sessions for the user
        sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
        
        session_list = [{
            'id': session.session_id,
            'created_at': session.created_at.isoformat()
        } for session in sessions]
        
        return JsonResponse({'sessions': session_list})

def debug_endpoint(request):
    """Debug endpoint to help troubleshooting"""
    return JsonResponse({
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers),
        'cookies': request.COOKIES,
        'GET': dict(request.GET),
        'POST': dict(request.POST),
        'body': request.body.decode() if request.body else None,
        'user': str(request.user),
        'is_ajax': request.headers.get('x-requested-with') == 'XMLHttpRequest',
        'content_type': request.content_type,
        'language': request.LANGUAGE_CODE,
    })

def test_form(request):
    """View for testing POST requests with a simple form"""
    return render(request, 'chatbot/test_form.html')

def test_fetch(request):
    """Simple test endpoint for fetch API requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({
                'status': 'success',
                'message': f"Received: {data.get('message', '')}",
                'data': data
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'error': 'Only POST method is allowed'
        }, status=405)

def mock_ai_response(message, language):
    """Creates a context-aware mock AI response for development purposes"""
    
    # Simple response based on the language
    if language == 'ky':
        responses = [
            "Салам! Мен сизге Нарын аймагындагы айыл чарбасы боюнча маалымат бере алам.",
            "Нарын аймагында жакшы өсүүчү өсүмдүктөр: картошка, буудай жана арпа.",
            "Топурактын сапатын жакшыртуу үчүн органикалык жер семирткичтерди колдонуңуз.",
            "Кыргызстандын тоолуу аймактарында жайыт малчылыгы абдан маанилүү."
        ]
    elif language == 'ru':
        responses = [
            "Привет! Я могу предоставить информацию о сельском хозяйстве в Нарынской области.",
            "В Нарынской области хорошо растут: картофель, пшеница и ячмень.",
            "Для улучшения качества почвы используйте органические удобрения.",
            "В горных районах Кыргызстана очень важно пастбищное животноводство."
        ]
    else:  # Default to English
        responses = [
            "Hello! I can provide information about agriculture in the Naryn region.",
            "Crops that grow well in Naryn region include potatoes, wheat, and barley.",
            "To improve soil quality, use organic fertilizers and proper crop rotation.",
            "Pasture-based livestock farming is very important in the mountainous areas of Kyrgyzstan."
        ]
    
    import random
    
    # Keywords for each language to make responses more relevant
    keywords_en = {
        "hello": "Hello! I'm your farming assistant for the Naryn region. How can I help you today?",
        "hi": "Hi there! I can provide information about agriculture in the Naryn region. What would you like to know?",
        "crop": "The main crops grown in Naryn region are potatoes, wheat, barley, and some hardy vegetables due to the high-altitude climate.",
        "soil": "Soil quality in Naryn can be improved with organic fertilizers, proper crop rotation, and careful water management.",
        "livestock": "Livestock farming is the backbone of Naryn's agriculture. Sheep, horses, and cattle are commonly raised in the region's vast mountain pastures.",
        "weather": "The Naryn region has a continental climate with cold winters and mild summers. The growing season is relatively short, typically from late April to early September."
    }
    
    keywords_ru = {
        "привет": "Привет! Я ваш сельскохозяйственный помощник по Нарынской области. Чем могу помочь?",
        "здравствуй": "Здравствуйте! Я могу предоставить информацию о сельском хозяйстве в Нарынской области. Что бы вы хотели узнать?",
        "культур": "Основные культуры, выращиваемые в Нарынской области: картофель, пшеница, ячмень и некоторые выносливые овощи из-за высокогорного климата.",
        "почв": "Качество почвы в Нарыне можно улучшить с помощью органических удобрений, правильного севооборота и тщательного управления водными ресурсами.",
        "скот": "Животноводство - основа сельского хозяйства Нарына. На обширных горных пастбищах региона обычно разводят овец, лошадей и крупный рогатый скот.",
        "погод": "В Нарынской области континентальный климат с холодной зимой и мягким летом. Вегетационный период относительно короткий, обычно с конца апреля до начала сентября."
    }
    
    keywords_ky = {
        "салам": "Салам! Мен Нарын аймагы боюнча айыл чарба жардамчысымын. Сизге кандай жардам бере алам?",
        "өсүмдүк": "Нарын аймагында, бийик тоолуу климатка байланыштуу, негизинен картошка, буудай, арпа жана айрым чыдамкай жашылчалар өстүрүлөт.",
        "топурак": "Нарындагы топурактын сапатын органикалык жер семирткичтерди колдонуп, туура которуштуруп айдоо жана сууну туура пайдалануу менен жакшыртса болот.",
        "мал": "Мал чарбачылыгы Нарын айыл чарбасынын негизи болуп саналат. Аймактын кенен тоо жайыттарында көбүнчө кой, жылкы жана бодо мал өстүрүлөт.",
        "аба": "Нарын аймагында континенталдык климат бар, кыш суук, жай мелүүн. Өсүү мезгили салыштырмалуу кыска, адатта апрель айынын аягынан сентябрь айынын башына чейин."
    }
    
    # Choose the appropriate keywords based on language
    keywords = keywords_en if language == 'en' else keywords_ru if language == 'ru' else keywords_ky
    
    # Check if any keywords match the message
    lower_message = message.lower()
    for keyword, response in keywords.items():
        if keyword in lower_message:
            return response
    
    # If no keywords match, return a random response
    return random.choice(responses)