import logging
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from inspect import signature
from json import loads, dumps

from requests import post

import ocs.request
from ocs.data import about_data, contest_data
from ocs.user import combine_token


class Server(BaseHTTPRequestHandler):
    """Main HTTP server"""

    def CORS(self):
        """Handle CORS"""

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')

    def send(self, result):
        """Send HTTP response"""
        
        if isinstance(result, int):
            code, body = result, None
        else:
            code, body = result
        logging.debug(code)
        logging.debug(body)

        self.send_response(code)  # Send status code
        self.CORS()
        if body is None:
            self.end_headers()
        else:
            body = dumps(body).encode('utf-8')
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)  # Send body

    def process(self, body):
        """Process a request"""

        if 'type' not in body:
            return 400  # Bad request
        if body['type'] not in dir(ocs.request):
            return 501  # Not implemented

        # Check if all required parameters are in the request
        parameters = str(signature(eval('ocs.request.' + body['type'])))[1:-1]
        for parameter in parameters.split():
            if 'None' in parameter:  # Optional parameter
                if parameter.replace('=None', '') not in body:
                    parameters = parameters.replace(', ' + parameter, '')  # Remove it
                else:
                    parameters = parameters.replace('=None', '')
            else:
                if parameter.replace(',', '') not in body:
                    return 400  # Bad request

        # Check token
        if 'token' in body and not body['type'] == 'authorize':
            token = combine_token(body['username'], body['token'])
            if token == 0:
                return 401  # Token not found
            authorization = post(('https://' if body['homeserver'].find('://') == -1 else '') + body['homeserver'],
                json={'type': 'authorize', 'username': body['username'], 'token': token}).status_code
            if authorization != 200:
                return authorization

        # Check if contest exists
        if 'contest' in body and body['contest'] not in about_data['contests']:
            return 404  # Contest not found

        # Check if problem exists
        if 'problem' in body and (body['problem'] not in contest_data[body['contest']]['problems'] or
            datetime.now().timestamp() < datetime.fromisoformat(contest_data[body['contest']]['start-time']).timestamp()):
            return 404  # Problem not found

        # Run the corresponding function and send the results
        if parameters == '':
            return eval('ocs.request.' + body['type'] + '()')
        else:
            return eval('ocs.request.' + body['type'] + '(body["' + parameters.replace(', ', '"], body["') + '"])')

    def do_POST(self):
        """Handle POST requests"""

        # Decode request body
        content_length = int(self.headers['Content-Length'])
        try:
            body = loads(self.rfile.read(content_length).decode('utf-8'))
        except JSONDecodeError:
            self.send(400)  # Bad request
        logging.debug(body)

        self.send(self.process(body))  # Process request and send back results
    
    def do_GET(self):
        """Handle GET requests"""
        
        self.send_response(200)
        self.CORS()
        self.end_headers()
        self.wfile.write('<html><body>Your <a href="https://github.com/LadueCS/OpenContest">\
                         OpenContest</a> server is working!</body></html>'.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests"""
        
        self.send_response(200)
        self.CORS()
        self.end_headers()
