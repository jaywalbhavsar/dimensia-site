import os
from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Fix for running on localhost (HTTP)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# --- 1. CONFIGURATION (KEYS) ---
GOOGLE_CLIENT_ID = "701939588182-56qac914ughsp6iolqt5ff2o5tu9inbi.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

GITHUB_CLIENT_ID = "Ov23li4gpittcYAUFFkv"
GITHUB_CLIENT_SECRET = "035226f2ac708cd48afa0767b7a955311e742f97"

# EMAIL CREDENTIALS
SENDER_EMAIL = "jaywal2509@gmail.com"
APP_PASSWORD = "bsky evfn ysun clyr"
RECEIVER_EMAIL = "jaywal2509@gmail.com"

# --- 2. THE EMAIL ROBOT 🤖 ---
def send_login_notification(client_email, client_name):
    """Sends an email TO THE CLIENT confirming their login."""
    
    # Security Check: If GitHub returns no email, stop here so we don't crash
    if not client_email or "@" not in client_email:
        print(f"⚠️ Could not send email to {client_name} (Email hidden or invalid).")
        return

    subject = "Welcome to DIMENSIA | Login Confirmation"
    
    body = f"""
    Hello {client_name},

    This is a confirmation that you have successfully registered/logged into the DIMENSIA Network.

    ACCESS GRANTED.
    
    You can now access your dashboard and project status.
    
    — DIMENSIA SYSTEMS
    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = client_email
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        server.quit()
        print(f"✅ Login Notification sent to: {client_email}")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- 3. OAUTH SETUP ---
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
    redirect_uri='http://127.0.0.1:5000/login/google/callback'
)

github = oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
    redirect_uri='http://127.0.0.1:5000/login/github/callback'
)

# --- 4. PAGE ROUTES ---
@app.route('/')
def home(): return render_template('index.html', user=session.get('user'))

@app.route('/team')
def team(): return render_template('team.html')

@app.route('/services')
def services(): return render_template('services.html')

@app.route('/contact')
def contact(): return render_template('contact.html')

@app.route('/login')
def login(): return render_template('login.html')

@app.route('/register')
def register(): return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user: return redirect('/login')
    
    # Fallback if name is missing
    if 'name' not in user: user['name'] = user.get('email', 'Agent')
    
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# --- 5. CONTACT FORM LOGIC ---
@app.route('/send_email', methods=['POST'])
def contact_form():
    name = request.form.get('name')
    client_email = request.form.get('email')
    message = request.form.get('message')

    subject = f"Inquiry from: {name}"
    body = f"Name: {name}\nEmail: {client_email}\n\nMessage:\n{message}"
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL # Send to YOU
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
        server.quit()
        
        # Also send confirmation to client
        send_login_notification(client_email, name)
        return redirect('/')
    except:
        return "Error sending email."

# --- 6. LOGIN CALLBACKS ---

@app.route('/login/google')
def google_login():
    return google.authorize_redirect('http://127.0.0.1:5000/login/google/callback')

@app.route('/login/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
        user_info = resp.json()
        session['user'] = user_info
        
        # 🔥 SEND EMAIL (Google) 🔥
        send_login_notification(user_info.get('email'), user_info.get('name'))
        
        return redirect('/dashboard')
    except Exception as e:
        return f"Google Error: {e}"

@app.route('/login/github')
def github_login():
    return github.authorize_redirect('http://127.0.0.1:5000/login/github/callback')

@app.route('/login/github/callback')
def github_callback():
    try:
        token = github.authorize_access_token()
        user_info = github.get('user').json()
        
        # Handle missing GitHub email
        if not user_info.get('email'):
             user_info['email'] = "Hidden by GitHub"
             
        session['user'] = user_info
        
        # 🔥 SEND EMAIL (GitHub) 🔥
        # Only sends if email is not hidden
        send_login_notification(user_info.get('email'), user_info.get('login'))
        
        return redirect('/dashboard')
    except Exception as e:
        return f"GitHub Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)