import json
import hashlib
import random
import string
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

class User:
    """
        Represents the user model in the database
    """
    def __init__(self, email, password, is_active=True, activation_code=None):
        self.email = email
        self.password_hash = self._hash_password(password)
        self.is_active = is_active
        self.activation_code = activation_code

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password, hashed_password):
        """
        Function that return true or false in passwords compare
        """
        return self._hash_password(password) == hashed_password

class  AuthenticationSystem:
    """
        Class containing both authentication and registration for an user, 
        also contains DDL for the database.
    """
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password_hash TEXT,
                is_active INTEGER,
                activation_code TEXT
            )
        ''')
        self.conn.commit()

    def register(self, email, password):
        """
            Register a new user in the database with an email and the password
        """
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            return False, "Email already registered"
        activation_code = self._generate_activation_code()
        user = User(email, password, is_active=False, activation_code=activation_code)
        self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user.email, user.password_hash, user.is_active, user.activation_code))
        self.conn.commit()
        return True, "Registration successful"

    def authenticate(self, email, password):
        """
            Perform an authentication against the user table if the user credentials are valid and the user is active
        """
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user_exists = self.cursor.fetchone()
        if user_exists:
            user = User(user_exists[0], user_exists[1], user_exists[2], user_exists[3])
            if user.is_active:
                if user.check_password(password, user.password_hash):
                    return True, "Authentication successful"
            return False, "User is not active"    
        return False, "Invalid email or password"

    def _generate_activation_code(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

class MyHTTPHandler(BaseHTTPRequestHandler):
    """
    Class generated using ChatGPT. Extends from python3 http.server class BaseHTTPRequestHandler
    At the moment only support POST method, it's extendable to any other method.
    No middlewares and no authentication headers are being used at this test.
    """
    def do_POST(self):
        """
        Support POST request method
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/register':
            email = data.get('email')
            password = data.get('password')
            if email and password:
                success, message = sys.register(email, password)
                response = {'success': success, 'message': message}
            else:
                response = {'success': False, 'message': 'Email and password are required'}
        elif self.path == '/login':
            email = data.get('email')
            password = data.get('password')
            if email and password:
                success, message = sys.authenticate(email, password)
                response = {'success': success, 'message': message}
            else:
                response = {'success': False, 'message': 'Email and password are required'}
        else:
            response = {'success': False, 'message': 'Invalid endpoint'}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    DB_PATH = "ableton.db"  # It might require the absolute or relative path depending on the OS
    sys = AuthenticationSystem(DB_PATH)
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHTTPHandler)
    print('HTTP server is running...')
    httpd.serve_forever()

# Tests for Registration and Authentication
@pytest.fixture
def auth_system():
    """
    System re-definition for pytest tests
    """
    system = AuthenticationSystem(DB_PATH)
    yield system
    system.conn.close()

def test_registration(system):
    """
    Registration related tests
    """
    assert system.register("test@example.com", "password123") == (True, "Registration successful")
    assert system.register("test@example.com", "password123") == (False, "Email already registered")

def test_authentication(system):
    """
    Authentication related tests
    """
    system.register("test@example.com", "password123")
    assert system.authenticate("test@example.com", "password123") == (True, "Authentication successful")
    assert system.authenticate("test@example.com", "wrongpassword") == (False, "Invalid email or password")
