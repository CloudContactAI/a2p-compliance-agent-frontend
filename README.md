# A2P Compliance Agent - Chat UI

Interactive chat interface for A2P compliance checking.

## Features

- **Interactive Chat**: Conversational interface for data collection
- **Quick Check**: Fast compliance analysis with minimal input
- **Real-time Results**: Instant compliance feedback with violations and recommendations
- **AWS Ready**: Multiple deployment options for AWS

## Local Development

```bash
pip3 install -r requirements.txt
python3 app.py
```

Visit `http://localhost:3000`

## AWS Deployment Options

### 1. AWS App Runner (Recommended)
```bash
# Create apprunner.yaml with your backend URL
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

### 3. AWS Lambda (Serverless)
```bash
# Package for Lambda
zip -r lambda-package.zip . -x "*.git*" "__pycache__/*"

# Deploy with SAM or Serverless Framework
sam deploy --template-file template.yaml
```

## Environment Variables

- `BACKEND_URL`: URL of the compliance pipeline API
- `PORT`: Port to run the application (default: 3000)

## Usage

1. **Start Collection**: Type "start" to begin full data collection
2. **Quick Check**: Type "quick check" for fast analysis
3. **Help**: Type "help" for available commands

### Quick Check Format
```
Brand: Your Brand Name
Website: https://yourwebsite.com
Message: Your sample message here
```

## API Endpoints

- `GET /`: Chat interface
- `POST /api/quick-check`: Quick compliance check
- `POST /api/analyze-submission`: Full submission analysis
- `GET /health`: Health check
