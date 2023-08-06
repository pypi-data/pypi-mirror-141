from hashlib import pbkdf2_hmac
from os import urandom
from requests import post
from secrets import token_hex

from ocs.db import con, cur


tokens = {}  # Create tokens object


def hash(password, salt):
    """Hash password with salt"""

    return salt + pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)


def check_password(username, password):
    """Check if a password is correct"""

    users = cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()
    if len(users) == 0:
        return 404  # Username not found
    if users[0][3] == hash(password, users[0][3][:32]):
        return 200
    return 403  # Incorrect password


def create_user(name, email, username, password):
    """Create a new user in the database"""

    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (name, email, username, hash(password, urandom(32))))
    con.commit()


def modify_user(name, email, username, password):
    """Modify user account information"""    

    if name != '':   
        cur.execute('UPDATE users SET name = ? where username = ?', (name,  username))
    if email != '':
        cur.execute('UPDATE users SET email = ? where username = ?', (email,  username))
    if password != '':
        cur.execute('UPDATE users SET password = ? where username = ?', (hash(password, urandom(32)),  username))
    con.commit()


def delete_user(name, email, username, password):
    """Delete a user from the database"""

    cur.execute('DELETE FROM users where username = ?', (username,))
    con.commit()


def make_token(username, server):
    """Create and return a token"""

    token = [token_hex(8), token_hex(8), 0]
    for s in server.split():
        token[2] = token_hex(8)
        save_token(username, token[0] + token[1] + token[2])
        post(('https://' if s.find('://') == -1 else '') + s, json={
             'type': 'authorize', 'username': username, 'token': token[0] + token[2]})
    return token[0] + token[1]


def save_token(username, token):
    """Save token"""

    if username not in tokens:
        tokens[username] = []

    # If too many tokens, remove first one
    if len(tokens[username]) > 64:
        tokens[username].pop(0)

    tokens[username].append(token)


def combine_token(username, token):
    """Combine a user and contest token"""

    if username not in tokens:
        return 0
    
    l = [i for i in tokens[username] if len(i) == 32 and i[:16] == token[:16]]
    if len(l) == 0:
        return 0
    tokens[username].remove(l[0])
    return token + l[0][16:]


def check_token(username, token):
    """Check if a token is valid"""
    
    if username in tokens and token in tokens[username]:
        tokens[username].remove(token)
        return True
    return False
