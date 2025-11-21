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

@app.route('/api/<path:endpoint>', methods=['POST'])
def proxy_api(endpoint):
    """Proxy API calls to backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/{endpoint}",
            json=request.get_json(),
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": "Backend compliance service is not running. Please start the backend API."}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "a2p-compliance-frontend"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
