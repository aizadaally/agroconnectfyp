# frontend/context_processors.py

from django.utils import translation
from django.conf import settings

def language_context(request):
    """
    Context processor to add language information to templates
    """
    current_language = translation.get_language()
    
    # Correctly create a dictionary with language codes as keys and names as values
    available_languages = {}
    for code, name in settings.LANGUAGES:
        try:
            lang_info = translation.get_language_info(code)
            available_languages[code] = lang_info['name_local']
        except Exception:
            available_languages[code] = name
    
    return {
        'LANGUAGE_CODE': current_language,
        'LANGUAGES': available_languages
    }