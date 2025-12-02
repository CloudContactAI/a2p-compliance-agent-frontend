#!/bin/bash
# Generate env-config.js for local development
export API_URL=${API_URL:-http://localhost:8000/api}
export ADMIN_URL=${ADMIN_URL:-http://localhost:8000}
echo "window.ENV = { API_URL: '$API_URL' };" > env-config.js
echo "Environment configured with API_URL=$API_URL"
echo "Open index.html in your browser"
