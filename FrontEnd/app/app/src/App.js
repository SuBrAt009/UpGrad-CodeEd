import React, { useEffect, useState } from 'react';
import './App.css';
import { api } from './api';

function App() {
  const [currentScreen, setCurrentScreen] = useState('login'); // 'login', 'working-professional', 'college-student', 'home', 'desktop-1', 'skillfit-dashboard', 'skillfit-assessment', 'revise-yoda'
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  
  // Working Professional Form States
  const [currentRole, setCurrentRole] = useState('');
  const [organization, setOrganization] = useState('');
  const [interestedProfession, setInterestedProfession] = useState('');
  
  // College Student Form States
  const [degree, setDegree] = useState('');
  const [specialisation, setSpecialisation] = useState('');
  const [collegeOrganization, setCollegeOrganization] = useState('');
  const [interestedProfessionStudent, setInterestedProfessionStudent] = useState('');

 const handleLoginSubmit = async (e) => {
  e.preventDefault();
  try {
    const data = await api.login(userId.trim(), password);
    console.log("login response:", data); // keep for dev
    setCurrentScreen("working-professional");
  } catch (err) {
    alert(err.message || "Login failed");
  }
};

const handleWorkingProfessionalSubmit = async (e) => {
  e.preventDefault();
  try {
    const token = localStorage.getItem("token");
    await api.saveWorkingProfessional({ currentRole, organization, interestedProfession }, token);
    setCurrentScreen('home');
  } catch (err) {
    alert(err.message || "Could not save profile");
  }
};

const handleCollegeStudentSubmit = async (e) => {
  e.preventDefault();
  try {
    const token = localStorage.getItem("token");
    await api.saveCollegeStudent(
      { degree, specialisation, collegeOrganization, interestedProfessionStudent },
      token
    );
    setCurrentScreen("home");
  } catch (err) {
    alert(err.message || "Could not save profile");
  }
};



  const toggleUserType = () => {
    if (currentScreen === 'working-professional') {
      setCurrentScreen('college-student');
    } else {
      setCurrentScreen('working-professional');
    }
  };

  const closeModal = () => {
    setCurrentScreen('login');
  };

  // Navigation functions for course pages
  const navigateToDesktop1 = () => {
    setCurrentScreen('desktop-1');
  };

  const navigateToSkillfitDashboard = () => {
    setCurrentScreen('skillfit-dashboard');
  };

  const navigateToSkillfitAssessment = () => {
    setCurrentScreen('skillfit-assessment');
  };

  const navigateToReviseYoda = () => {
    setCurrentScreen('revise-yoda');
  };

  const navigateToHome = () => {
    setCurrentScreen('home');
  };

  return (
    <div className="app">
      {/* Logo - Always visible */}
      <div className="logo">
        <h1>upGrad</h1>
      </div>

      {/* Login Screen */}
      {currentScreen === 'login' && (
        <div className="login-container">
          {/* Main Content */}
          <div className="main-content">
            <h2 className="welcome-text">Welcome! Sign Up or Login</h2>
            
            <form onSubmit={handleLoginSubmit} className="login-form">
              <div className="input-group">
                <input
                  type="text"
                  placeholder="User Id"
                  value={userId}
                  onChange={(e) => setUserId(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div className="input-group">
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <button type="submit" className="next-button">
                Next
              </button>
            </form>
          </div>

          {/* Rocket Illustration */}
          <div className="rocket-illustration">
  <img src="/data/upgrad graphic enhanced.png" alt="Rocket Illustration" class="rocket-image" />
</div>

        </div>
      )}

      {/* Working Professional Modal */}
      {currentScreen === 'working-professional' && (
        <div className="modal-overlay">
          <div className="modal">
            <button className="close-button" onClick={closeModal}>
              ×
            </button>
            <h2 className="modal-title">Tell us more about you!</h2>
            <p className="modal-subtitle">Helps us craft courses just for you</p>
            
            <form onSubmit={handleWorkingProfessionalSubmit} className="modal-form">
              <div className="input-group">
                <input
                  type="text"
                  placeholder="What is your current role?"
                  value={currentRole}
                  onChange={(e) => setCurrentRole(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div className="input-group">
                <input
                  type="text"
                  placeholder="Organization?"
                  value={organization}
                  onChange={(e) => setOrganization(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div className="input-group">
                <input
                  type="text"
                  placeholder="Interested Profession"
                  value={interestedProfession}
                  onChange={(e) => setInterestedProfession(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <button type="submit" className="next-button">
                Next
              </button>
              
              <button type="button" className="toggle-link" onClick={toggleUserType}>
                I am a college student
              </button>
            </form>
          </div>
        </div>
      )}

      {/* College Student Modal */}
      {currentScreen === 'college-student' && (
        <div className="modal-overlay">
          <div className="modal">
            <button className="close-button" onClick={closeModal}>
              ×
            </button>
            <h2 className="modal-title">Tell us more about you!</h2>
            <p className="modal-subtitle">Helps us craft courses just for you</p>
            
            <form onSubmit={handleCollegeStudentSubmit} className="modal-form">
              <div className="input-group">
                <select
                  value={degree}
                  onChange={(e) => setDegree(e.target.value)}
                  className="input-field dropdown-field"
                >
                  <option value="">What is your degree?</option>
                  <option value="B.E.">B.E.</option>
                  <option value="M.E.">M.E.</option>
                </select>
              </div>
              
              <div className="input-group">
                <select
                  value={specialisation}
                  onChange={(e) => setSpecialisation(e.target.value)}
                  className="input-field dropdown-field"
                >
                  <option value="">Specialisation?</option>
                  <option value="Computer Science">Computer Science</option>
                  <option value="Electrical">Electrical</option>
                  <option value="Mechanical">Mechanical</option>
                  <option value="Civil">Civil</option>
                </select>
              </div>
              
              <div className="input-group">
                <input
                  type="text"
                  placeholder="College/ Organization?"
                  value={collegeOrganization}
                  onChange={(e) => setCollegeOrganization(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div className="input-group">
                <input
                  type="text"
                  placeholder="Interested profession?"
                  value={interestedProfessionStudent}
                  onChange={(e) => setInterestedProfessionStudent(e.target.value)}
                  className="input-field"
                />
              </div>
              
              <button type="submit" className="next-button">
                Next
              </button>
              
              <button type="button" className="toggle-link" onClick={toggleUserType}>
                I am a working professional
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Home Page Dashboard */}
      {currentScreen === 'home' && (
        <div className="home-page">
          {/* Header */}
          <header className="header">
            <div className="header-content">
              <div className="logo-section">
                <h1 className="logo-text"> </h1>
              </div>
              
              <div className="search-section">
                <div className="search-bar">
                  <input type="text" placeholder="Explore Courses" className="search-input" />
                  <div className="search-icon">🔍</div>
                </div>
              </div>
              
              <nav className="main-nav">
                <div className="nav-item dropdown">
                  <span>For working professionals</span>
                  <span className="dropdown-arrow">▼</span>
                </div>
                <div className="nav-item dropdown">
                  <span>For fresh graduates</span>
                  <span className="dropdown-arrow">▼</span>
                </div>
                <div className="nav-item">Study abroad</div>
                <div className="nav-item dropdown">
                  <span>More</span>
                  <span className="dropdown-arrow">▼</span>
                </div>
              </nav>
              
              <div className="header-actions">
                <button className="free-courses-btn">Free Courses</button>
                <div className="user-profile">
                  <div className="profile-avatar">D</div>
                  <span className="dropdown-arrow">▼</span>
                </div>
                <div className="scroll-arrow">→</div>
              </div>
            </div>
          </header>

          {/* Sub Navigation */}
          <nav className="sub-nav">
            <div className="category-item">
              <div className="category-icon">🎓</div>
              <span>Doctorate</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">🤖</div>
              <span>AI & ML</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">🎓</div>
              <span>MBA</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">📊</div>
              <span>Data Science</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">📢</div>
              <span>Marketing</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">🔗</div>
              <span>Management</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">📚</div>
              <span>Education</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="category-item">
              <div className="category-icon">💻</div>
              <span>Software & Tech</span>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className="scroll-arrow">→</div>
          </nav>

          {/* Main Content */}
          <main className="main-content-dashboard">
            <div className="content-grid">
              {/* Left Column - Courses for you */}
              <div className="left-column">
                <div className="section-header">
                  <h2 className="section-title">Courses for you</h2>
                  <p className="section-subtitle">Recommended by AI</p>
                </div>
                
                <div className="course-cards">
                  <div className="course-card featured">
                    <h3 className="course-title">Intro to Object Oriented Programming</h3>
                    <button className="enroll-btn" onClick={navigateToDesktop1}>Enroll now!</button>
                  </div>
                  
                  <div className="course-card faded">
                    <p className="faded-text">Learn for new role</p>
                  </div>
                  
                  <div className="course-card faded">
                    <p className="faded-text">General skill/English Proficiency</p>
                  </div>
                </div>
              </div>

              {/* Right Column - Assessments and Study Abroad */}
              <div className="right-column">
                {/* SkillFit Assessment */}
                <div className="assessment-card">
                  <div className="card-header">
                    <h3 className="card-title">SkillFit Assessment</h3>
                    <div className="card-icon">✏️</div>
                  </div>
                  <p className="faded-text">Give a test and see where you stand among others in your profession</p>
                </div>

                {/* Study Abroad */}
                <div className="study-abroad-card">
                  <div className="card-header">
                    <h3 className="card-title">Study Abroad</h3>
                    <p className="card-subtitle">Recommended by AI</p>
                  </div>
                  <p className="faded-text">Explore courses based on your current background</p>
                </div>
              </div>
            </div>
          </main>
        </div>
      )}

      {/* Desktop-1 (Course Progress) Page */}
      {currentScreen === 'desktop-1' && (
        <div className="course-page">
          {/* Header */}
          <header className="course-header">
            <div className="course-header-content">
              <div className="logo-section">
                <h1 className="logo-text">upGrad</h1>
              </div>
              <h2 className="course-title-header">Intro to Object Oriented Programming</h2>
              <div className="header-actions">
                <div className="user-profile">
                  <div className="profile-avatar">D</div>
                </div>
                <div className="notification-icon">🔔<span className="notification-count">2</span></div>
                <div className="points-icon">⭐<span className="points-count">24</span></div>
                <a href="#" className="track-progress-link">Track your progress</a>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="course-main-content">
            <div className="course-grid">
              {/* Left Column */}
              <div className="course-left-column">
                <div className="modules-list">
                  <div className="module-item completed">
                    <span className="module-name">Module 1</span>
                    <span className="module-progress">100% Completed</span>
                  </div>
                  <div className="module-item in-progress">
                    <span className="module-name">Module 2</span>
                    <span className="module-progress">53% Completed</span>
                  </div>
                  <div className="module-item pending">
                    <span className="module-name">Module 3</span>
                    <span className="module-progress">0% Completed</span>
                  </div>
                  <div className="module-item pending">
                    <span className="module-name">Module 4</span>
                    <span className="module-progress">0% Completed</span>
                  </div>
                </div>

                <div className="dashboard-link-section">
                  <button className="see-dashboard-btn" onClick={navigateToSkillfitDashboard}>
                    See Dashboard
                  </button>
                  <div className="arrow">→</div>
                </div>

                <div className="progress-info">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{width: '34.44%'}}></div>
                  </div>
                  <div className="progress-text">34.44% Complete</div>
                  <div className="time-left">9h 10m left</div>
                </div>

                <div className="dashboard-summary">
                  <h3>Dashboard Summary</h3>
                </div>
              </div>

              {/* Right Column */}
              <div className="course-right-column">
                <div className="module-details">
                  <h3>Module 1: Inheritance</h3>
                  <div className="module-status completed">Completed</div>
                  <button className="revise-btn" onClick={navigateToReviseYoda}>
                    Revise with Yoda
                  </button>
                </div>

                <div className="module-details">
                  <h3>Module 2: Encapsulation</h3>
                  <div className="lecture-list">
                    <div className="lecture-item completed">Lecture 1 - Completed</div>
                    <div className="lecture-item completed">Lecture 2 - Completed</div>
                    <div className="lecture-item completed">Lecture 3 - Completed</div>
                    <button className="skillfit-btn" onClick={navigateToSkillfitAssessment}>
                      Skillfit Assessment
                    </button>
                    <div className="lecture-item completed">Lecture 4 - Completed</div>
                    <div className="lecture-item completed">Lecture 5 - Completed</div>
                    <div className="lecture-item completed">Lecture 6 - Completed</div>
                  </div>
                </div>

                <button className="continue-learning-btn">
                  <span className="play-icon">▶</span>
                  Continue Learning
                </button>
              </div>
            </div>
          </main>
        </div>
      )}

      {/* SkillFit Assessment Dashboard */}
      {currentScreen === 'skillfit-dashboard' && (
        <div className="course-page">
          {/* Header */}
          <header className="course-header">
            <div className="course-header-content">
              <div className="logo-section">
                <h1 className="logo-text">upGrad</h1>
              </div>
              <h2 className="course-title-header">Intro to Object Oriented Programming</h2>
              <div className="header-actions">
                <div className="user-profile">
                  <div className="profile-avatar">D</div>
                </div>
                <div className="notification-icon">🔔<span className="notification-count">2</span></div>
                <div className="points-icon">⭐<span className="points-count">24</span></div>
                <a href="#" className="track-progress-link">Track your progress</a>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="dashboard-main-content">
            <div className="dashboard-header">
              <h2 className="dashboard-title">Dashboard</h2>
              <div className="bar-chart-icon">📊</div>
            </div>

            <div className="dashboard-grid">
              <div className="leaderboards-section">
                <h3>Leaderboards</h3>
                <div className="leaderboards-placeholder"></div>
              </div>

              <div className="core-learning-info">
                <h3>Core Learning Info</h3>
                <ul>
                  <li>Progress Tracker (% syllabus completed, chapters/topics covered.)</li>
                  <li>Daily/Weekly Goals (bite-sized targets (e.g., "Finish 10 flashcards today"))</li>
                  <li>Upcoming Tasks/Deadlines (quizzes, assignments, test dates.)</li>
                  <li>Performance Summary (scores, accuracy, speed trends.)</li>
                </ul>
              </div>

              <div className="yoda-remarks">
                <div className="yoda-header">
                  <div className="trophy-icon">🏆</div>
                  <span>Yoda's remarks!</span>
                </div>
                <p>"You'll be exam-ready in 45 days if you follow this plan."</p>
              </div>

              <div className="weaknesses-section">
                <h3>Weaknesses</h3>
                <p>subject/topic-wise breakdown</p>
                <p>AI powered course suggestions</p>
              </div>
            </div>
          </main>
        </div>
      )}

      {/* SkillFit Assessment Page */}
      {currentScreen === 'skillfit-assessment' && (
        
        <div className="course-page">
          {/* Header */}
          <header className="course-header">
            <div className="course-header-content">
              <div className="logo-section">
                <h1 className="logo-text">upGrad</h1>
              </div>
              <h2 className="course-title-header">Intro to Object Oriented Programming</h2>
              <div className="header-actions">
                <div className="user-profile">
                  <div className="profile-avatar">D</div>
                </div>
                <div className="notification-icon">🔔<span className="notification-count">2</span></div>
                <div className="points-icon">⭐<span className="points-count">24</span></div>
                <a href="#" className="track-progress-link">Track your progress</a>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="assessment-main-content">
            <div className="assessment-header">
              <h2 className="assessment-title">SkillFit Assessment</h2>
              <div className="pencil-icon">✏️</div>
            </div>

            <div className="assessment-container">
              <div className="timer-section">
                <div className="timer-box">9:56</div>
              </div>

              <div className="question-section">
                <div className="question-header">
                  <span className="question-number">Q)</span>
                  <span className="difficulty-tag">Easy</span>
                </div>
                <p className="question-text">Which feature of OOP indicates code reusability?</p>

                <div className="options-list">
                  <label className="option-item">
                    <input type="radio" name="question" value="abstraction" />
                    <span>Abstraction</span>
                  </label>
                  <label className="option-item">
                    <input type="radio" name="question" value="polymorphism" />
                    <span>Polymorphism</span>
                  </label>
                  <label className="option-item">
                    <input type="radio" name="question" value="encapsulation" />
                    <span>Encapsulation</span>
                  </label>
                  <label className="option-item">
                    <input type="radio" name="question" value="inheritance" />
                    <span>Inheritance</span>
                  </label>
                </div>

                <button className="hint-btn">Get a Hint!</button>
              </div>
            </div>

            <div className="question-navigation">
              <div className="question-numbers">
                {Array.from({length: 11}, (_, i) => (
                  <div key={i} className={`question-box ${i === 10 ? 'current' : ''}`}>
                    {i}
                  </div>
                ))}
              </div>
            </div>
          </main>
        </div>
      )}

      {/* Revise with Yoda Page */}
      {currentScreen === 'revise-yoda' && (
        <div className="course-page">
          {/* Header */}
          <header className="course-header">
            <div className="course-header-content">
              <div className="logo-section">
                <h1 className="logo-text">upGrad</h1>
              </div>
              <h2 className="course-title-header">Intro to Object Oriented Programming</h2>
              <div className="header-actions">
                <div className="user-profile">
                  <div className="profile-avatar">D</div>
                </div>
                <div className="notification-icon">🔔<span className="notification-count">2</span></div>
                <div className="points-icon">⭐<span className="points-count">24</span></div>
                <a href="#" className="track-progress-link">Track your progress</a>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="revise-main-content">
            <div className="revise-header">
              <h2 className="revise-title">Revise with Yoda</h2>
              <div className="yoda-character">🧙‍♂️</div>
            </div>

            <div className="revise-tabs">
              <button className="tab-btn active">Notes</button>
              <button className="tab-btn">Short Lecture Clips</button>
            </div>

            <div className="ai-summary">
              <h3>AI Summary</h3>
              <div className="summary-content">
                <h4>Inheritance</h4>
                <p>Inheritance in object-oriented programming is a mechanism that allows one class (called the child or derived class) to acquire the properties and behaviors of another class (called the parent or base class).</p>
              </div>
            </div>

            <div className="assessment-section">
              <h3>Assessment</h3>
              <div className="question-section">
                <p className="question-text">Q) Which feature of OOP indicates code reusability?</p>
                <div className="options-list">
                  <label className="option-item">
                    <input type="radio" name="revise-question" value="abstraction" />
                    <span>Abstraction</span>
                  </label>
                  <label className="option-item">
                    <input type="radio" name="revise-question" value="polymorphism" />
                    <span>Polymorphism</span>
                  </label>
                  <label className="option-item">
                    <input type="radio" name="revise-question" value="encapsulation" />
                    <span>Encapsulation</span>
                  </label>
                  <label className="option-item">
                    <input type="radio" name="revise-question" value="inheritance" />
                    <span>Inheritance</span>
                  </label>
                </div>
              </div>
            </div>

            <div className="reminder-section">
              <a href="#" className="reminder-link">Set reminder to revise everyday</a>
            </div>
          </main>
        </div>
      )}
    </div>
  );
}

export default App;
