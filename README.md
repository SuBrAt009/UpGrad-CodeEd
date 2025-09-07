## 🚀 Features

### Backend (Flask API)
- **User Authentication**: Secure JWT-based authentication with password hashing
- **User Profiles**: Separate profiles for students and working professionals
- **Course Management**: Dynamic course creation and management system
- **AI-Powered Suggestions**: Intelligent course recommendations based on user profiles
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Quiz Proxy**: Seamless integration with FastAPI quiz engine

### Quiz Engine (FastAPI)
- **Adaptive Assessment**: Intelligent difficulty adjustment based on user performance
- **AI-Powered Hints**: Contextual hints generated using OpenAI/Anthropic APIs
- **Smart Explanations**: Detailed explanations for answers with AI-generated content
- **Performance Tracking**: Real-time ability, mastery, and fatigue scoring
- **Time Management**: Configurable time limits with adaptive pacing
- **Multi-Difficulty Support**: Easy, Medium, Hard question bands with staircase progression

### Frontend (React)
- **Modern UI/UX**: Clean, responsive design with upGrad branding
- **Multi-Screen Experience**: 
  - Login/Signup with animated rocket illustration
  - Profile setup for students and professionals
  - Course dashboard with AI recommendations
  - Interactive course progress tracking
  - SkillFit assessment system
  - "Revise with Yoda" learning assistant
- **Real-time Features**: Progress tracking, notifications, and points system
- **Responsive Design**: Works seamlessly across all devices

## 🏗️ Project Structure

```
UpGrad-CodeEd-main/
├── app/                          # Flask Backend
│   ├── app.py                   # Main Flask application
│   ├── config.py                # Configuration management
│   ├── models.py                # Database models
│   ├── requirements.txt         # Python dependencies
│   ├── routes/                  # API route blueprints
│   │   ├── auth.py             # Authentication routes
│   │   ├── profile.py          # User profile routes
│   │   ├── suggest.py          # Course suggestion routes
│   │   └── quiz_proxy.py       # Quiz engine proxy routes
│   └── utils/                   # Utility functions
│       └── auth_middleware.py  # JWT authentication middleware
├── quiz/                         # FastAPI Quiz Engine
│   ├── main.py                  # FastAPI quiz service
│   └── adaptive_inheritance_quiz.py  # Adaptive quiz logic
└── FrontEnd/app/app/            # React Frontend
    ├── src/
    │   ├── App.js              # Main React component
    │   ├── App.css             # Styling
    │   ├── api.js              # API integration
    │   ├── index.js            # React entry point
    │   └── src/quiz/           # Quiz components
    │       ├── api.js          # Quiz API integration
    │       ├── QuestionCard.jsx # Quiz question component
    │       ├── SkillfitAssessment.jsx # Assessment component
    │       └── styles.css      # Quiz styling
    ├── public/                  # Static assets
    └── package.json            # Node.js dependencies
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.3** - Web framework
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **Flask-CORS 4.0.1** - Cross-origin resource sharing
- **PostgreSQL** - Database (with psycopg2-binary)
- **JWT** - Authentication tokens
- **Argon2** - Password hashing
- **Python-dotenv** - Environment configuration

### Quiz Engine
- **FastAPI 0.111.0** - High-performance API framework
- **Uvicorn 0.30.1** - ASGI server
- **Pydantic 2.8.2** - Data validation
- **OpenAI API** - AI-powered hints and explanations
- **Anthropic Claude** - Alternative AI provider
- **Adaptive Algorithm** - Intelligent difficulty adjustment

### Frontend
- **React 18.2.0** - UI library
- **React Scripts 5.0.1** - Build tools
- **CSS3** - Styling and animations

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- npm or yarn

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd UpGrad-CodeEd-main/app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `app` directory:
   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/upgrad_codeed
   JWT_SECRET=your-super-secret-jwt-key
   JWT_TTL_HOURS=8
   CORS_ORIGINS=http://localhost:3000
   ```

5. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE upgrad_codeed;
   ```

6. **Run the Flask application:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Quiz Engine Setup

1. **Navigate to the quiz directory:**
   ```bash
   cd UpGrad-CodeEd-main/quiz
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn openai anthropic pydantic
   ```

3. **Set up environment variables:**
   Create a `.env` file in the `quiz` directory:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   OPENAI_MODEL=gpt-4o-mini
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```

4. **Run the quiz engine:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001 --reload
   ```

   The quiz API will be available at `http://localhost:8001`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd UpGrad-CodeEd-main/FrontEnd/app/app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The application will be available at `http://localhost:3000`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Profile Management
- `GET /api/profile/` - Get user profile
- `POST /api/profile/student` - Create/update student profile
- `POST /api/profile/professional` - Create/update professional profile

### Course Suggestions
- `GET /api/suggestions/` - Get AI-powered course recommendations

### Quiz Engine (via Flask Proxy)
- `POST /api/quiz/session/start` - Start a new quiz session
- `POST /api/quiz/session/next` - Get the next question
- `POST /api/quiz/session/hint` - Get a hint for current question
- `POST /api/quiz/session/answer` - Submit an answer
- `POST /api/quiz/session/explain_batch` - Get explanations for completed questions

## 🎯 Key Features Explained

### User Types
The platform supports two distinct user types:
- **Students**: College students with degree, specialization, and college information
- **Working Professionals**: Current role, organization, and career interests

### Course System
- **Dynamic Course Creation**: Courses are stored in the database with metadata
- **AI Recommendations**: Personalized course suggestions based on user profiles
- **Progress Tracking**: Real-time progress monitoring with completion percentages

### Learning Experience
- **Interactive Assessments**: SkillFit assessment system with timed quizzes
- **Adaptive Quiz Engine**: AI-powered adaptive difficulty adjustment
- **Learning Assistant**: "Revise with Yoda" feature for AI-powered revision
- **Dashboard Analytics**: Comprehensive learning analytics and progress tracking

### Quiz System
- **Adaptive Difficulty**: Questions adjust based on user performance and ability
- **AI-Powered Features**: Hints and explanations generated using OpenAI/Anthropic
- **Performance Metrics**: Real-time tracking of ability, mastery, and fatigue
- **Time Management**: Configurable time limits with intelligent pacing
- **Multi-Band Questions**: Easy, Medium, Hard difficulty levels with staircase progression

## 🔧 Configuration

### Environment Variables

#### Backend (Flask)
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `JWT_TTL_HOURS`: Token expiration time in hours
- `CORS_ORIGINS`: Allowed frontend origins (comma-separated)
- `COOKIE_NAME`: Session cookie name
- `COOKIE_SECURE`: Enable secure cookies (true/false)
- `COOKIE_SAMESITE`: SameSite cookie policy
- `QUIZ_BASE`: Quiz engine base URL (default: http://localhost:8001)

#### Quiz Engine (FastAPI)
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `ANTHROPIC_API_KEY`: Anthropic API key for AI features
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `ANTHROPIC_MODEL`: Anthropic model to use (default: claude-3-5-sonnet-20241022)

## 🚀 Deployment

### Backend Deployment
1. Set up a PostgreSQL database
2. Configure environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `python app.py` (creates tables automatically)
5. Deploy using your preferred method (Docker, Heroku, AWS, etc.)

### Quiz Engine Deployment
1. Set up AI API keys (OpenAI/Anthropic)
2. Configure environment variables
3. Install dependencies: `pip install fastapi uvicorn openai anthropic pydantic`
4. Deploy using your preferred method (Docker, Heroku, AWS, etc.)
5. Update `QUIZ_BASE` environment variable in Flask backend

### Frontend Deployment
1. Build the React app: `npm run build`
2. Deploy the `build` folder to your hosting service
3. Update CORS origins in backend configuration

