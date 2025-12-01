"""
Flask app for A2P Compliance Chat UI
Serves the frontend and proxies API calls
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# Backend API URL - can be set via environment variable
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5001')

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files like CSS"""
    return send_from_directory('.', filename)

@app.route('/api/<path:endpoint>', methods=['POST', 'GET'])
def proxy_api(endpoint):
    """Proxy API calls to backend"""
    try:
        if request.method == 'POST':
            response = requests.post(
                f"{BACKEND_URL}/{endpoint}",
                json=request.get_json(),
                headers={'Content-Type': 'application/json'},
                cookies=request.cookies,
                timeout=5
            )
        else:
            response = requests.get(
                f"{BACKEND_URL}/{endpoint}",
                cookies=request.cookies,
                timeout=5
            )
        
        # Forward response with cookies
        flask_response = jsonify(response.json())
        flask_response.status_code = response.status_code
        for key, value in response.cookies.items():
            flask_response.set_cookie(key, value)
        return flask_response
    except Exception as e:
        return jsonify({"error": "Backend compliance service is not running. Please start the backend API."}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "a2p-compliance-frontend"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
