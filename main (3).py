from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
import requests
from bs4 import BeautifulSoup
from translations import get_translation, get_available_languages, translate_text, LIBERIAN_LANGUAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecare-liberia-health-app-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'patient' or 'professional'
    age = db.Column(db.Integer)
    county = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    medical_history = db.Column(db.Text)
    specialty = db.Column(db.String(100))  # for professionals
    license_info = db.Column(db.String(100))  # for professionals
    availability = db.Column(db.String(500))  # for professionals
    rating = db.Column(db.Float, default=5.0)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_type = db.Column(db.String(20))  # 'in-person' or 'virtual'
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MentalHealthAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood_score = db.Column(db.Integer)  # 1-10 scale
    anxiety_level = db.Column(db.Integer)  # 1-10 scale
    depression_indicators = db.Column(db.Text)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)

class HealthFacility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    facility_type = db.Column(db.String(50))  # hospital, clinic, health center
    address = db.Column(db.String(200))
    contact = db.Column(db.String(20))
    services = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class HealthEducation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # malaria, maternal, mental, etc.
    language = db.Column(db.String(20), default='English')
    content_type = db.Column(db.String(20))  # article, video, podcast
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100))
    instructions = db.Column(db.Text)
    prescribed_date = db.Column(db.DateTime, default=datetime.utcnow)

# Liberian Counties
LIBERIAN_COUNTIES = [
    'Bomi', 'Bong', 'Gbarpolu', 'Grand Bassa', 'Grand Cape Mount',
    'Grand Gedeh', 'Grand Kru', 'Lofa', 'Margibi', 'Maryland',
    'Montserrado', 'Nimba', 'River Cess', 'River Gee', 'Sinoe'
]

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form

        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            user_type=data.get('user_type'),
            age=data.get('age'),
            county=data.get('county'),
            contact=data.get('contact'),
            gender=data.get('gender'),
            medical_history=data.get('medical_history', ''),
            specialty=data.get('specialty', ''),
            license_info=data.get('license_info', ''),
            availability=data.get('availability', ''),
            is_approved=True if data.get('user_type') == 'patient' else False
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Registration successful!'})

    return render_template('register.html', counties=LIBERIAN_COUNTIES)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            return jsonify({'success': True, 'redirect': '/dashboard'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.user_type == 'patient':
        return render_template('patient_dashboard.html', user=user)
    else:
        return render_template('professional_dashboard.html', user=user)

@app.route('/professionals')
def professionals():
    county = request.args.get('county', '')
    specialty = request.args.get('specialty', '')
    name = request.args.get('name', '')
    profession = request.args.get('profession', '')

    query = User.query.filter_by(user_type='professional', is_approved=True)

    if county:
        query = query.filter_by(county=county)
    if specialty:
        query = query.filter(User.specialty.ilike(f'%{specialty}%'))
    if name:
        query = query.filter(User.name.ilike(f'%{name}%'))
    if profession:
        query = query.filter(User.specialty.ilike(f'%{profession}%'))

    professionals = query.all()

    # Get unique specializations for filter dropdown
    specializations = db.session.query(User.specialty).filter(
        User.user_type == 'professional',
        User.is_approved == True,
        User.specialty.isnot(None)
    ).distinct().all()
    specializations = [s[0] for s in specializations if s[0]]

    return render_template('professionals.html', 
                         professionals=professionals, 
                         counties=LIBERIAN_COUNTIES,
                         specializations=specializations)

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    data = request.get_json()
    appointment = Appointment(
        patient_id=session['user_id'],
        professional_id=data.get('professional_id'),
        appointment_date=datetime.fromisoformat(data.get('appointment_date')),
        appointment_type=data.get('appointment_type'),
        notes=data.get('notes', '')
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Appointment booked successfully!'})

@app.route('/search')
def search():
    return render_template('search.html', counties=LIBERIAN_COUNTIES)

@app.route('/ai_chatbot')
def ai_chatbot():
    return render_template('ai_chatbot.html')

@app.route('/translator')
def translator():
    return render_template('translator.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    user_language = session.get('language', 'english')

    # Simple AI responses for demonstration - with language support
    responses = {
        'hello': {
            'english': 'Hello! I\'m Wilmot, your AI health assistant. How can I help you today?',
            'kpelle': 'Kɛ! Ma Wilmot ma, yee kɛɛn yuu. Na kɛ yuu kɛrɛ maa?',
            'bassa': 'Nyɔnmɔ! Ma Wilmot ma, wɛn kɛɛn yuu. Na ke yuu nyɔn maa?',
            'gio': 'Yɛ! Ma Wilmot ma, yɛɛ kɛɛn yuu. Na kɛ yuu nyɔɔn maa?',
            'liberian_english': 'Hello o! I Wilmot, your health helper. How I can help you today?'
        },
        'fever': {
            'english': 'For fever, rest and drink plenty of fluids. If fever persists above 101°F for more than 2 days, please consult a healthcare professional.',
            'kpelle': 'Mɛni yii kɛ, gbɛɛ bɛrɛ kɛɛ nyu maa. Mɛni yii kɛ sɔɔng wulu fɛɛli kɛ, dokita nyɔn.',
            'bassa': 'Mɛni yii ke, gbɛɛ bɛrɛ kɛɛ nyu maa. Mɛni yii ke sɔɔng wulu fɛɛli kɛ, dokita nyɔn.',
            'gio': 'Mɛni yii kɛ, gbɛɛ bɛrɛ kɛɛ nyu maa. Mɛni yii kɛ sɔɔng wulu fɛɛli kɛ, dokita nyɔɔn.',
            'liberian_english': 'For fever, rest and drink plenty water. If fever stay pass 2 days, go see doctor.'
        },
        'malaria': {
            'english': 'Malaria symptoms include fever, chills, and flu-like illness. If you suspect malaria, seek immediate medical attention.',
            'kpelle': 'Malaria kɛrɛng: mɛni yii, kɔlɔng, kɛɛ nɛɛng. Malaria bɛɛ kɛ, dokita nyɔn maa bɔ.',
            'bassa': 'Malaria kɛrɛng: mɛni yii, kɔlɔng, kɛɛ nɛɛng. Malaria bɛɛ ke, dokita nyɔn maa bɔ.',
            'gio': 'Malaria kɛrɛɛng: mɛni yii, kɔlɔɔng, kɛɛ nɛɛng. Malaria bɛɛ kɛ, dokita nyɔɔn maa bɔ.',
            'liberian_english': 'Malaria signs: fever, cold, body pain. If you think malaria, go hospital quick quick.'
        }
    }

    default_response = {
        'english': 'I\'m here to help! Could you please provide more details about your health concern?',
        'kpelle': 'Ma kɛ yuu bɔɔlɔ! Yuu yee kɛɛ kɛrɛng mɔɔ sɛbɛ?',
        'bassa': 'Ma ke yuu bɔɔlɔ! Yuu wɛn kɛɛ kɛrɛng mɔɔ sɛbɛ?',
        'gio': 'Ma kɛ yuu bɔɔlɔ! Yuu yɛɛ kɛɛ kɛrɛɛng mɔɔ sɛbɛ?',
        'liberian_english': 'I here to help you! Tell me more about your health problem.'
    }

    response = default_response.get(user_language, default_response['english'])
    
    for keyword, reply_dict in responses.items():
        if keyword in user_message:
            response = reply_dict.get(user_language, reply_dict['english'])
            break

    return jsonify({'response': response})

@app.route('/mental_health')
def mental_health():
    return render_template('mental_health.html')

@app.route('/assessment', methods=['POST'])
def mental_health_assessment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    data = request.get_json()
    assessment = MentalHealthAssessment(
        user_id=session['user_id'],
        mood_score=data.get('mood_score'),
        anxiety_level=data.get('anxiety_level'),
        depression_indicators=json.dumps(data.get('depression_indicators', []))
    )

    db.session.add(assessment)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Assessment completed. Thank you for sharing.'})

@app.route('/facilities')
def facilities():
    county = request.args.get('county', '')
    facility_type = request.args.get('facility_type', '')
    service = request.args.get('service', '')
    name = request.args.get('name', '')

    query = HealthFacility.query

    if county:
        query = query.filter_by(county=county)
    if facility_type:
        query = query.filter_by(facility_type=facility_type)
    if service:
        query = query.filter(HealthFacility.services.ilike(f'%{service}%'))
    if name:
        query = query.filter(HealthFacility.name.ilike(f'%{name}%'))

    facilities = query.all()

    # Get unique facility types and services for filter dropdowns
    facility_types = db.session.query(HealthFacility.facility_type).distinct().all()
    facility_types = [ft[0] for ft in facility_types if ft[0]]

    return render_template('facilities.html', 
                         facilities=facilities, 
                         counties=LIBERIAN_COUNTIES,
                         facility_types=facility_types)

@app.route('/telemedicine')
def telemedicine():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('telemedicine.html')

@app.route('/education')
def health_education():
    category = request.args.get('category', '')
    language = request.args.get('language', 'English')

    query = HealthEducation.query
    if category:
        query = query.filter_by(category=category)
    if language:
        query = query.filter_by(language=language)

    articles = query.all()
    return render_template('education.html', articles=articles)

@app.route('/prescriptions')
def prescriptions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_prescriptions = Prescription.query.filter_by(patient_id=session['user_id']).all()
    return render_template('prescriptions.html', prescriptions=user_prescriptions)

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Simple admin check (in real app, you'd have proper role management)
    pending_professionals = User.query.filter_by(user_type='professional', is_approved=False).all()
    total_users = User.query.count()
    total_appointments = Appointment.query.count()

    return render_template('admin.html', 
                         pending_professionals=pending_professionals,
                         total_users=total_users,
                         total_appointments=total_appointments)

@app.route('/approve_professional/<int:professional_id>')
def approve_professional(professional_id):
    professional = User.query.get(professional_id)
    if professional:
        professional.is_approved = True
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/disease_scanner')
def disease_scanner():
    return render_template('disease_scanner.html')

@app.route('/disease_outbreak')
def disease_outbreak():
    return render_template('disease_outbreak.html')

@app.route('/scan_disease', methods=['POST'])
def scan_disease():
    # Placeholder for AI image analysis
    # In production, this would integrate with computer vision AI
    return jsonify({
        'success': True, 
        'analysis': 'Common skin condition detected. Consult healthcare provider.',
        'confidence': 85
    })

@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_appointments = Appointment.query.filter_by(patient_id=session['user_id']).all()
    return render_template('appointments.html', appointments=user_appointments)

@app.route('/nphil_health_info')
def nphil_health_info():
    """Display health information from NPHIL website"""
    health_data = scrape_nphil_health_info()
    return render_template('nphil_health.html', health_data=health_data)

@app.route('/api/fetch_nphil_data')
def fetch_nphil_data():
    """API endpoint to fetch fresh NPHIL data"""
    health_data = scrape_nphil_health_info()
    return jsonify({'success': True, 'data': health_data, 'count': len(health_data)})

@app.route('/offline_sync', methods=['POST'])
def offline_sync():
    # Handle offline data synchronization
    data = request.get_json()
    # Store offline data and sync when connection is available
    return jsonify({'success': True, 'message': 'Data synced successfully'})

@app.route('/set_language/<language>')
def set_language(language):
    """Set the user's preferred language"""
    if language in LIBERIAN_LANGUAGES:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/translate', methods=['POST'])
def translate():
    """Translate text to specified language"""
    data = request.get_json()
    text = data.get('text', '')
    target_language = data.get('language', 'english')
    
    translated_text = translate_text(text, target_language)
    return jsonify({
        'success': True,
        'original': text,
        'translated': translated_text,
        'language': target_language
    })

@app.context_processor
def inject_translation():
    """Make translation functions available in templates"""
    current_language = session.get('language', 'english')
    return {
        'get_translation': get_translation,
        'current_language': current_language,
        'available_languages': get_available_languages(),
        'LIBERIAN_LANGUAGES': LIBERIAN_LANGUAGES
    }

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def scrape_nphil_health_info():
    """Scrape health information from NPHIL website"""
    try:
        url = "https://nphil.gov.lr/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        health_articles = []

        # Extract news/articles from the website
        articles = soup.find_all(['article', 'div'], class_=['post', 'news-item', 'article', 'content-item'])

        # If no specific article containers found, try general content extraction
        if not articles:
            articles = soup.find_all(['div', 'section'], class_=['content', 'main-content', 'news', 'updates'])

        # Extract text content from paragraphs and headers
        content_sections = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p'])

        # Combine extracted content
        for i, section in enumerate(content_sections[:20]):  # Limit to first 20 sections
            text = section.get_text(strip=True)
            if len(text) > 50:  # Only include substantial content
                title = f"NPHIL Health Update {i+1}"
                if section.name in ['h1', 'h2', 'h3', 'h4']:
                    title = text[:100]
                    continue

                health_articles.append({
                    'title': title,
                    'content': text,
                    'category': 'public-health',
                    'source': 'NPHIL'
                })

        # Extract any health alerts or announcements
        alerts = soup.find_all(string=lambda text: text and any(keyword in text.lower() for keyword in 
                              ['alert', 'outbreak', 'vaccination', 'epidemic', 'health', 'disease', 'prevention']))

        for alert in alerts[:10]:  # Limit alerts
            text = alert.strip()
            if len(text) > 30:
                health_articles.append({
                    'title': 'NPHIL Health Alert',
                    'content': text,
                    'category': 'health-alert',
                    'source': 'NPHIL'
                })

        return health_articles

    except Exception as e:
        print(f"Error scraping NPHIL website: {e}")
        return []

def init_sample_data():
    # Import and initialize comprehensive health data
    try:
        from init_health_data import initialize_health_professionals, initialize_health_facilities
        initialize_health_professionals()
        initialize_health_facilities()
    except ImportError:
        pass

    # Add sample health facilities (fallback if comprehensive data fails)
    if HealthFacility.query.count() == 0:
        facilities = [
            HealthFacility(name='JFK Medical Center', county='Montserrado', facility_type='hospital', 
                         address='Sinkor, Monrovia', contact='231-77-123-456', 
                         services='Emergency, Surgery, Maternity, Pediatrics'),
            HealthFacility(name='Phebe Hospital', county='Bong', facility_type='hospital',
                         address='Suakoko, Bong County', contact='231-88-234-567',
                         services='General Medicine, Surgery, Mental Health'),
            HealthFacility(name='Ganta United Methodist Hospital', county='Nimba', facility_type='hospital',
                         address='Ganta, Nimba County', contact='231-77-345-678',
                         services='General Medicine, Maternity, Pediatrics')
        ]

        for facility in facilities:
            db.session.add(facility)

    # Add sample health education content
    if HealthEducation.query.count() == 0:
        articles = [
            HealthEducation(title='Malaria Prevention in Liberia', 
                          content='Malaria is a serious disease in Liberia. Use mosquito nets, eliminate standing water, and seek treatment immediately if you have symptoms.',
                          category='malaria', language='English'),
            HealthEducation(title='Maternal Health Care', 
                          content='Proper prenatal care is essential for healthy pregnancies. Regular checkups and skilled birth attendance save lives.',
                          category='maternal', language='English'),
            HealthEducation(title='Mental Health Awareness', 
                          content='Mental health is just as important as physical health. Don\'t hesitate to seek help if you\'re struggling.',
                          category='mental', language='English')
        ]

        # Add NPHIL health information
        try:
            nphil_data = scrape_nphil_health_info()
            for item in nphil_data[:5]:  # Add first 5 items to avoid overwhelming the database
                article = HealthEducation(
                    title=item['title'][:200],  # Limit title length
                    content=item['content'],
                    category=item['category'],
                    language='English',
                    content_type='article'
                )
                articles.append(article)
        except Exception as e:
            print(f"Error adding NPHIL data: {e}")

        for article in articles:
            db.session.add(article)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(host='0.0.0.0', port=5000, debug=True)