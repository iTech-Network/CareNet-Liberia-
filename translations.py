
"""
Translation system for CareNet Liberia
Supports major languages and dialects spoken in Liberia
"""

# Major languages and dialects in Liberia
LIBERIAN_LANGUAGES = {
    'english': 'English',
    'kpelle': 'Kpelle',
    'bassa': 'Bassa',
    'gio': 'Gio (Dan)',
    'kru': 'Kru',
    'grebo': 'Grebo',
    'mano': 'Mano',
    'krahn': 'Krahn',
    'gola': 'Gola',
    'gbandi': 'Gbandi',
    'loma': 'Loma',
    'kissi': 'Kissi',
    'vai': 'Vai',
    'belle': 'Belle',
    'dey': 'Dey',
    'mende': 'Mende',
    'mandingo': 'Mandingo',
    'arabic': 'Arabic',
    'liberian_english': 'Liberian English',
    'koloqua': 'Koloqua'
}

# Common health-related translations
TRANSLATIONS = {
    'english': {
        'welcome': 'Welcome to CareNet Liberia',
        'health_for_all': 'Digital Health Platform for All 15 Counties',
        'book_appointment': 'Book Appointment',
        'find_doctor': 'Find Doctor',
        'emergency': 'Emergency',
        'mental_health': 'Mental Health',
        'facilities': 'Health Facilities',
        'education': 'Health Education',
        'login': 'Login',
        'register': 'Register',
        'dashboard': 'Dashboard',
        'prescriptions': 'Prescriptions',
        'telemedicine': 'Telemedicine',
        'ai_assistant': 'AI Health Assistant',
        'name': 'Name',
        'email': 'Email',
        'password': 'Password',
        'county': 'County',
        'phone': 'Phone Number',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'fever': 'Fever',
        'headache': 'Headache',
        'malaria': 'Malaria',
        'doctor': 'Doctor',
        'nurse': 'Nurse',
        'hospital': 'Hospital',
        'clinic': 'Clinic',
        'symptoms': 'Symptoms',
        'treatment': 'Treatment',
        'medication': 'Medication',
        'appointment': 'Appointment',
        'health_tip': 'Health Tip',
        'prevention': 'Prevention'
    },
    'kpelle': {
        'welcome': 'Kɛ CareNet Liberia kɛ',
        'health_for_all': 'Yee koli gbogbo maa county 15 kɛ',
        'book_appointment': 'Yee koli bɛrɛ sii',
        'find_doctor': 'Dokita kɛrɛ',
        'emergency': 'Maa yii',
        'mental_health': 'Sueii yee',
        'facilities': 'Yee koli ma',
        'education': 'Yee kɛlɛng',
        'login': 'Kɔ kɛ',
        'register': 'Yuu tari',
        'dashboard': 'Gbɛlɛng kɛ',
        'prescriptions': 'Kɛɛn sɛbɛ',
        'telemedicine': 'Mɛni yii kɛɛn',
        'ai_assistant': 'Kɛɛn yuu maa',
        'name': 'Yuu',
        'email': 'Sɛbɛ kɛɛ',
        'password': 'Koli gbɛlɛ',
        'county': 'Kɔ',
        'phone': 'Telefon',
        'submit': 'Kɛ',
        'cancel': 'Gbɛlɛ',
        'fever': 'Mɛni yii',
        'headache': 'Wuumɛni',
        'malaria': 'Malaria',
        'doctor': 'Dokita',
        'nurse': 'Nɛsɛ',
        'hospital': 'Yee koli ma baa',
        'clinic': 'Yee koli ma',
        'symptoms': 'Mɛni kɛrɛng',
        'treatment': 'Kɛɛn',
        'medication': 'Kɛɛn',
        'appointment': 'Yee koli bɛrɛ',
        'health_tip': 'Yee kɛlɛng',
        'prevention': 'Kɔɔng'
    },
    'bassa': {
        'welcome': 'Nyɔnmɔ CareNet Liberia ke',
        'health_for_all': 'Wɛn gbɛdii county 15 kɛ',
        'book_appointment': 'Wɛn gbɛdii kɛ',
        'find_doctor': 'Dokita nyɔn',
        'emergency': 'Maa kɛ',
        'mental_health': 'Sueii wɛn',
        'facilities': 'Wɛn gbɛdii ma',
        'education': 'Kɛlɛng',
        'login': 'Kɔ',
        'register': 'Yuu ke',
        'dashboard': 'Gbɛlɛng',
        'prescriptions': 'Kɛɛn sɛbɛ',
        'telemedicine': 'Kɛɛn telefon kɛ',
        'ai_assistant': 'Kɛɛn yuu',
        'name': 'Yuu',
        'email': 'Sɛbɛ',
        'password': 'Koli gbɛlɛ',
        'county': 'Kɔ',
        'phone': 'Telefon',
        'submit': 'Kɛ',
        'cancel': 'Kpɛlɛ',
        'fever': 'Mɛni yii',
        'headache': 'Wuu mɛni',
        'malaria': 'Malaria',
        'doctor': 'Dokita',
        'nurse': 'Nɛsɛ',
        'hospital': 'Wɛn gbɛdii ma baa',
        'clinic': 'Wɛn gbɛdii ma',
        'symptoms': 'Mɛni kɛrɛng',
        'treatment': 'Kɛɛn',
        'medication': 'Kɛɛn',
        'appointment': 'Wɛn gbɛdii',
        'health_tip': 'Wɛn kɛlɛng',
        'prevention': 'Kɔɔng'
    },
    'gio': {
        'welcome': 'Yɛ CareNet Liberia po',
        'health_for_all': 'Yɛɛ geɛng county 15 kɛ',
        'book_appointment': 'Yɛɛ geɛng woo',
        'find_doctor': 'Dokita nyɔn',
        'emergency': 'Maa klɛɛ',
        'mental_health': 'Sueii yɛɛ',
        'facilities': 'Yɛɛ geɛng ma',
        'education': 'Kɛlɛɛng',
        'login': 'Kɔ blɔng',
        'register': 'Yuu taa',
        'dashboard': 'Gbɛlɛɛng',
        'prescriptions': 'Kɛɛn sɛbɛ',
        'telemedicine': 'Kɛɛn telefon',
        'ai_assistant': 'Kɛɛn yuu',
        'name': 'Yuu',
        'email': 'Sɛbɛ',
        'password': 'Koli gbɛlɛ',
        'county': 'Kɔ',
        'phone': 'Telefon',
        'submit': 'Kɛ',
        'cancel': 'Kpɛɛlɛ',
        'fever': 'Mɛni yii',
        'headache': 'Wuu mɛni',
        'malaria': 'Malaria',
        'doctor': 'Dokita',
        'nurse': 'Nɛɛsɛ',
        'hospital': 'Yɛɛ geɛng ma baa',
        'clinic': 'Yɛɛ geɛng ma',
        'symptoms': 'Mɛni kɛrɛɛng',
        'treatment': 'Kɛɛn',
        'medication': 'Kɛɛn',
        'appointment': 'Yɛɛ geɛng',
        'health_tip': 'Yɛɛ kɛlɛɛng',
        'prevention': 'Kɔɔɔng'
    },
    'liberian_english': {
        'welcome': 'Welcome to CareNet Liberia o',
        'health_for_all': 'Health for all de 15 counties dem',
        'book_appointment': 'Book your appointment',
        'find_doctor': 'Find doctor',
        'emergency': 'Emergency o',
        'mental_health': 'Mental health',
        'facilities': 'Health facilities dem',
        'education': 'Health education',
        'login': 'Login',
        'register': 'Register',
        'dashboard': 'Dashboard',
        'prescriptions': 'Your medicine dem',
        'telemedicine': 'Doctor call',
        'ai_assistant': 'AI helper',
        'name': 'Your name',
        'email': 'Email',
        'password': 'Password',
        'county': 'County',
        'phone': 'Phone number',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'fever': 'Fever',
        'headache': 'Headache',
        'malaria': 'Malaria',
        'doctor': 'Doctor',
        'nurse': 'Nurse',
        'hospital': 'Hospital',
        'clinic': 'Clinic',
        'symptoms': 'Symptoms dem',
        'treatment': 'Treatment',
        'medication': 'Medicine',
        'appointment': 'Appointment',
        'health_tip': 'Health tip',
        'prevention': 'Prevention'
    }
}

def get_translation(key, language='english'):
    """Get translation for a specific key and language"""
    if language in TRANSLATIONS and key in TRANSLATIONS[language]:
        return TRANSLATIONS[language][key]
    # Fallback to English if translation not found
    return TRANSLATIONS['english'].get(key, key)

def get_available_languages():
    """Get list of available languages"""
    return LIBERIAN_LANGUAGES

def translate_text(text, target_language='english'):
    """Simple text translation - in production, this would use a translation API"""
    # For now, return basic translations
    basic_translations = {
        'Hello': {
            'kpelle': 'Kɛ',
            'bassa': 'Nyɔnmɔ',
            'gio': 'Yɛ',
            'liberian_english': 'Hello o'
        },
        'How can I help you?': {
            'kpelle': 'Na kɛ yuu kɛrɛ maa?',
            'bassa': 'Na ke yuu nyɔn maa?',
            'gio': 'Na kɛ yuu nyɔɔn maa?',
            'liberian_english': 'How I can help you?'
        },
        'Thank you': {
            'kpelle': 'Gbɛlɛ kɛ',
            'bassa': 'Gbɛlɛ ke',
            'gio': 'Gbɛlɛɛ kɛ',
            'liberian_english': 'Thank you o'
        }
    }
    
    if text in basic_translations and target_language in basic_translations[text]:
        return basic_translations[text][target_language]
    
    return text  # Return original if no translation available
