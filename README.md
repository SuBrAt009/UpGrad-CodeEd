# UpGrad CodeEd - Educational Platform

A comprehensive full-stack educational platform built with Flask and React, designed to provide personalized learning experiences for students and working professionals.

## 🚀 Features

### Backend (Flask API)
- **User Authentication**: Secure JWT-based authentication with password hashing
- **User Profiles**: Separate profiles for students and working professionals
- **Course Management**: Dynamic course creation and management system
- **AI-Powered Suggestions**: Intelligent course recommendations based on user profiles
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing for frontend integration

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
│   │   └── suggest.py          # Course suggestion routes
│   └── utils/                   # Utility functions
│       └── auth_middleware.py  # JWT authentication middleware
└── FrontEnd/app/app/            # React Frontend
    ├── src/
    │   ├── App.js              # Main React component
    │   ├── App.css             # Styling
    │   ├── api.js              # API integration
    │   └── index.js            # React entry point
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
- **Learning Assistant**: "Revise with Yoda" feature for AI-powered revision
- **Dashboard Analytics**: Comprehensive learning analytics and progress tracking

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `JWT_TTL_HOURS`: Token expiration time in hours
- `CORS_ORIGINS`: Allowed frontend origins (comma-separated)
- `COOKIE_NAME`: Session cookie name
- `COOKIE_SECURE`: Enable secure cookies (true/false)
- `COOKIE_SAMESITE`: SameSite cookie policy

## 🚀 Deployment

### Backend Deployment
1. Set up a PostgreSQL database
2. Configure environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `python app.py` (creates tables automatically)
5. Deploy using your preferred method (Docker, Heroku, AWS, etc.)

### Frontend Deployment
1. Build the React app: `npm run build`
2. Deploy the `build` folder to your hosting service
3. Update CORS origins in backend configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is part of the UpGrad CodeEd program and is intended for educational purposes.

## 🆘 Support

For support and questions, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for the UpGrad CodeEd program**# UpGrad-CodeEd
