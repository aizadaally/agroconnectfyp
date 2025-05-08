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
    print(f"Request headers: {request.headers}")
    
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
            
        # Get or create a chat session
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={'user': request.user if request.user.is_authenticated else None}
        )
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=message
        )
        
        # Call the IO Intelligence API directly
        api_key = os.environ.get('IO_INTELLIGENCE_API_KEY', settings.IO_INTELLIGENCE_API_KEY)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Add system message with language instruction if specified
        system_message = "You are a helpful farming assistant knowledgeable about agriculture in Naryn region of Kyrgyzstan."
        if language == 'ky':
            system_message = "Сиз айыл чарба боюнча жардам берүүчү ассистентсиз. Сиз Нарын областындагы айыл чарбасы жөнүндө билимдүүсүз. Бардык суроолорго кыргызча жооп бериңиз."
        elif language == 'ru':
            system_message = "Вы ассистент по сельскому хозяйству, обладающий знаниями о сельском хозяйстве в Нарынской области Кыргызстана. Пожалуйста, отвечайте на все вопросы на русском языке."
        
        # Format messages for the API
        api_messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]
        
        api_data = {
            "model": "llama3-70b-8192",
            "messages": api_messages,
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        print(f"Sending to API: {json.dumps(api_data)}")
        
        response = requests.post(
            "https://api.io.net/v1/chat/completions",
            headers=headers,
            json=api_data
        )
        
        print(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"API response: {response_data}")
            
            assistant_message = response_data['choices'][0]['message']['content']
            
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
            print(f"API error: {response.text}")
            return JsonResponse({
                'error': f"API Error: {response.status_code}",
                'details': response.text,
                'session_id': session_id
            }, status=500)
            
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Exception in chat_api: {str(e)}")
        print(error_traceback)
        
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
            messages = ChatMessage.objects.filter(session=session)
            
            history = [{
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp
            } for msg in messages]
            
            return JsonResponse({'history': history, 'session_id': session_id})
            
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
    else:
        # List all sessions for the user
        sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
        
        session_list = [{
            'id': session.session_id,
            'created_at': session.created_at
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