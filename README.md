# MyOwnGuru - Agentic AI Professional Development Platform

MyOwnGuru is an intelligent platform that provides personalized, proactive learning roadmaps for professional development. It analyzes individual skills and projects to create tailored learning paths that adapt in real-time.

## Features

- **Resume Analysis**: Intelligent parsing and skill extraction from resumes
- **AI-Powered Roadmaps**: Personalized multi-step learning plans
- **Content Aggregation**: Curated courses, tutorials, and projects from across the web
- **Adaptive Learning**: Real-time path adjustments based on progress and feedback
- **Career Alignment**: Learning paths aligned with career aspirations and business needs
- **Progress Tracking**: Comprehensive analytics and progress monitoring

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **AI/ML**: OpenAI API, scikit-learn, spaCy
- **Authentication**: JWT tokens
- **File Processing**: PyPDF2, python-docx

## Project Structure

```
MyOwnGuru/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── public/
├── database/               # Database scripts
└── docs/                   # Documentation
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the backend:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at http://localhost:5173

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
