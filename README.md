# A2P Compliance Agent - Chat UI

Interactive chat interface for A2P 10DLC compliance checking with admin dashboard and clean site generation.

## Features

### User Features
- **Interactive Chat**: Conversational interface for data collection
- **Quick Check**: Fast compliance analysis with minimal input
- **Real-time Results**: Instant compliance feedback with violations and recommendations
- **Content Analysis**: Detailed breakdown of debt-related and marketing terms found
- **Multi-page Scanning**: Analyzes homepage, privacy policy, and terms & conditions

### Admin Features
- **Admin Dashboard**: View all submissions with filtering and sorting
- **Compliance Tracking**: Monitor scores, status, and violations
- **Clean Site Generation**: Generate debt-free versions of websites for compliance review
- **Asset Management**: Automatically downloads and hosts all CSS, images, and JavaScript
- **Submission Management**: View details and delete submissions

## Local Development

```bash
# Install dependencies
pip3 install -r requirements.txt

# Start frontend (port 5002)
python3 app.py

# Start backend (port 5001) - in separate terminal
cd ../a2p-compliance-agent-backend
python3 pipeline_api.py
```

Visit `http://localhost:5002` for the chat interface
Visit `http://localhost:5002/admin.html` for the admin dashboard

## Admin Access

Default credentials (change in production):
- Username: `Admin`
- Password: `Maws@1234`

Set via environment variables:
```bash
export ADMIN_USER=your_username
export ADMIN_PASSWORD=your_password
```

## Environment Variables

### Frontend
- `BACKEND_URL`: URL of the compliance pipeline API (default: http://localhost:5001)
- `PORT`: Port to run the application (default: 5002)

### Backend
- `ADMIN_USER`: Admin username for dashboard access
- `ADMIN_PASSWORD`: Admin password for dashboard access
- `AWS_PROFILE`: AWS profile for DynamoDB and S3 access (default: ccai)

## Database

Uses DynamoDB for submission tracking:
- **Production table**: `a2p-submissions`
- **Development table**: `a2p-submissions-dev` (automatically used on localhost)

Create tables:
```bash
cd ../a2p-compliance-agent-backend
python3 create_dynamodb_table.py
```

## Clean Site Generation

The admin dashboard includes a "Generate" button that creates cleaned versions of websites:

1. Downloads homepage, privacy policy, and terms & conditions
2. Downloads all CSS, JavaScript, and image assets
3. Removes debt-related terms (debt, collection, payment, etc.)
4. Uploads to S3 bucket: `a2p-compliance-websites`
5. Provides public URL for compliance review

Generated sites are stored at:
```
http://a2p-compliance-websites.s3-website-us-east-1.amazonaws.com/{domain}/index.html
```

## AWS Deployment Options

### 1. AWS App Runner (Recommended)
```bash
aws apprunner create-service --cli-input-json file://apprunner-config.json
```

### 2. AWS ECS with Fargate
```bash
# Build and push Docker image
docker build -t a2p-frontend .
docker tag a2p-frontend:latest your-ecr-repo/a2p-frontend:latest
docker push your-ecr-repo/a2p-frontend:latest

# Deploy with ECS
aws ecs create-service --cli-input-json file://ecs-service.json
```

### 3. Kubernetes
```bash
kubectl apply -f deploy.yaml
```

## API Endpoints

### Public Endpoints
- `GET /`: Chat interface
- `GET /admin.html`: Admin dashboard
- `POST /api/quick-check`: Quick compliance check
- `POST /api/analyze-submission`: Full submission analysis
- `GET /health`: Health check

### Admin Endpoints (Requires Authentication)
- `POST /admin/login`: Admin login
- `GET /admin/submissions`: Get all submissions
- `POST /admin/generate-clean-site/{id}`: Generate cleaned website
- `DELETE /admin/submissions/{id}`: Delete submission
- `POST /admin/logout`: Admin logout

## Usage

### Chat Interface

1. **Start Collection**: Type "start" to begin full data collection
2. **Quick Check**: Type "quick check" for fast analysis
3. **Help**: Type "help" for available commands

### Quick Check Format
```
Brand: Your Brand Name
Website: https://yourwebsite.com
Message: Your sample message here
```

### Admin Dashboard

1. Login with admin credentials
2. View all submissions sorted by timestamp
3. Click "View" to see full submission details
4. Click "Generate" to create a cleaned website
5. Click "View Site" to open the generated site
6. Click "Delete" to remove a submission

## Compliance Checks

The system checks for:

### Auto-Fail Triggers
- Third-party debt collection references
- Skip-tracing services
- Payday loan content
- Lead generation services
- Data brokerage services

### Content Analysis
- Debt-related terms: debt, collection, owe, payment
- Marketing terms near debt content (within 200 characters)
- Email domain validation (must have working website)
- Phone number format validation (US and international)
- Area code validation for US numbers

### Scoring
- Base score: 100 points
- Deductions for violations:
  - Invalid phone: -5 points
  - Invalid email domain: -10 points
  - Auto-fail triggers: -25 to -30 points
  - Missing opt-in language: -15 points

## Architecture

```
Frontend (Port 5002)
  ├── index.html - Chat interface
  ├── admin.html - Admin dashboard
  └── app.py - Flask proxy server

Backend (Port 5001)
  ├── pipeline_api.py - Main API server
  ├── data_collection_agent.py - Website scraping and analysis
  ├── site_generator.py - Clean site generation
  ├── submission_tracker.py - DynamoDB operations
  └── agent_core.py - Compliance scoring logic

AWS Resources
  ├── DynamoDB: a2p-submissions-dev / a2p-submissions
  └── S3: a2p-compliance-websites
```

## Security

- Token-based authentication for admin endpoints
- CORS configured for specific origins
- Session cookies with HttpOnly and SameSite flags
- PII redaction in code examples
- Separate dev/prod DynamoDB tables

## License

Copyright (c) 2024 CloudContactAI, LLC. All rights reserved.
