# Mini Portfolio Website Generator

A Flask-based web application that allows users to create and manage their personal portfolio websites with a beautiful, responsive design.

## 🌟 Features

- **User Authentication**
  - Secure user registration and login
  - Password hashing and security
  - Session management
  - Protected routes

- **Portfolio Management**
  - Create and edit portfolios
  - Store portfolio data in SQLite database
  - Preview portfolio before publishing
  - Share portfolio via unique URL

- **Responsive Design**
  - Mobile-friendly layout
  - Dark/Light theme support
  - Modern UI components
  - Loading animations

- **Data Storage**
  - SQLite database integration
  - Secure data handling
  - JSON storage for complex data
  - Automatic data validation

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mini-portfolio-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 📝 Usage

1. **Registration**
   - Click "Register" to create a new account
   - Fill in your details (username, email, password)
   - Verify your email (if configured)

2. **Login**
   - Use your email and password to log in
   - Access your dashboard

3. **Create Portfolio**
   - Click "Create Portfolio" in the dashboard
   - Fill in your portfolio details
   - Preview and save your portfolio

4. **Edit Portfolio**
   - Access your portfolio from the dashboard
   - Click "Edit" to modify your portfolio
   - Save changes to update your portfolio

5. **Share Portfolio**
   - Get your unique portfolio URL
   - Share with others to showcase your work

## 🔧 Configuration

The application uses the following configuration:

- `SECRET_KEY`: Randomly generated for security
- `SESSION_TYPE`: File-based session storage
- `SQLALCHEMY_DATABASE_URI`: SQLite database location
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled for performance

## 📦 Project Structure

```
mini-portfolio-generator/
├── app.py              # Main application file
├── models.py           # Database models
├── forms.py            # Form definitions
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS)
│   └── css/
│       └── style.css
├── templates/         # HTML templates
│   ├── base.html
│   ├── form.html
│   ├── portfolio.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── flask_session/     # Session storage
```

## 🔒 Security Features

- Password hashing using Werkzeug
- CSRF protection
- Session management
- Protected routes
- Input validation
- SQL injection prevention

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created by Yogendra Bhange

- GitHub: [yogendra-27-bhange](https://github.com/yogendra-27-bhange)
- Instagram: [yogi.__27](https://www.instagram.com/yogi.__27)

