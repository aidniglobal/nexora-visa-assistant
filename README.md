# Nexora - Global Residency & Visa Platform

A comprehensive web application for discovering, comparing, and applying for residency programs and visas worldwide.

## Features

### 🏠 Core Features
- **Residency Program Directory** - Browse 50+ residency programs across 10+ countries
- **Smart Eligibility Checker** - Find programs matching your budget and requirements
- **ROI Calculator** - Calculate investment returns and costs
- **Program Comparison Tool** - Compare multiple programs side-by-side
- **Consultant Network** - Connect with verified immigration experts

### 👤 User Features
- User authentication and profiles
- Save favorite programs
- Track residency applications
- Document management with OCR verification
- Consultation booking system
- Application progress tracking

### 📚 Content & Education
- Blog with guides and case studies
- Timeline estimators
- Investment guides
- Success stories
- Immigration resources

### 🔧 Admin Features
- Consultant verification
- Blog post management
- Application tracking
- User management

## Technology Stack

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-Mail (Email notifications)
- WeasyPrint (PDF generation)
- Tesseract (OCR)

**Frontend:**
- HTML5
- CSS3 (Glassmorphism, Gradients)
- Vanilla JavaScript
- Responsive Design

**Database:**
- SQLite (Development)
- Can be configured for PostgreSQL

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Tesseract OCR (for document scanning)

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd nova
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

5. **Run the application**
```bash
python run.py
```

Access the application at `http://localhost:5000`

## Project Structure

```
nova/
├── app.py                 # Main Flask application with routes
├── models.py             # Database models
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── run.py               # Entry point
├── residency_data.py    # Residency programs database
├── visa_data.py         # Visa information database
├── app/                 # Application module
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── ocr.py
│   ├── europass.py
│   ├── payments.py
│   └── utils.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── residencies.html
│   ├── residency_country.html
│   ├── residency_detail.html
│   ├── residency_calculator.html
│   ├── residency_eligibility.html
│   ├── residency_comparison.html
│   ├── residency_blog.html
│   ├── residency_blog_post.html
│   ├── consultants.html
│   ├── consultant_profile.html
│   ├── book_consultation.html
│   ├── my_residency_applications.html
│   └── ... (other templates)
├── static/              # Static files
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── profile_pics/
└── migrations/          # Database migrations

```

## Key Routes

### Residency Routes
- `/residencies` - Browse all residency programs
- `/residencies/<country>` - View programs in a specific country
- `/residencies/<country>/<program>` - View program details
- `/residency-comparison` - Compare programs
- `/residency-calculator` - ROI calculator
- `/residency-eligibility` - Eligibility checker
- `/residency-blog` - Blog posts
- `/residency-blog/<slug>` - Individual blog post
- `/consultants` - Find consultants
- `/consultant/<id>` - Consultant profile
- `/book-consultation` - Book a consultation
- `/my-residency-applications` - View your applications

### Visa Routes
- `/` - Home page
- `/submit_application` - Visa application form
- `/upload_document` - Document upload
- `/verify-document` - Document verification

### User Routes
- `/register` - User registration
- `/login` - User login
- `/dashboard` - User dashboard
- `/profile` - User profile management

## Database Models

### User Management
- `User` - User accounts
- `UserAgreement` - Terms acceptance
- `ResidencyConsultant` - Consultant profiles

### Residency Management
- `ResidencyProgram` - Program information
- `ResidencyApplication` - User applications
- `ApplicationStep` - Application progress tracking
- `ResidencyApplicationDocument` - Documents for applications
- `UserSavedProgram` - Saved favorites

### Content
- `ResidencyBlogPost` - Blog articles
- `ConsultantAppointment` - Scheduled consultations

### Visa Management
- `VisaApplication` - Visa applications
- `Document` - User documents
- `VerifiedDocument` - Verified documents

## API Endpoints

### Calculate ROI
```
POST /api/calculate-roi
{
    "investment": 500000,
    "annual_return": 5,
    "years": 5
}
```

### Check Eligibility
```
POST /api/check-eligibility
{
    "investment_budget": 500000,
    "income": 100000,
    "citizenship_wanted": true,
    "preferred_countries": ["Portugal", "Malta"]
}
```

## Configuration

### Email Setup
Update in `app.py`:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
```

### Database
In `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///nova.db'  # or PostgreSQL connection string
```

## Customization

### Adding New Residency Programs
Edit `residency_data.py` and add entries:
```python
"Country": {
    "Program Name": {
        "description": "...",
        "residency_type": "Investment",
        "minimum_investment": "€250,000",
        # ... other fields
    }
}
```

### Adding Blog Posts
Use the admin interface or create directly in database:
```python
from models import db, ResidencyBlogPost
post = ResidencyBlogPost(
    title="...",
    slug="...",
    content="...",
    published=True
)
db.session.add(post)
db.session.commit()
```

## Security Notes

- Change the secret key in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting for APIs
- Regular security updates

## Performance Optimization

- Implement caching for program data
- Use pagination for blog/consultants
- Lazy load images
- Minify CSS/JS in production
- Enable gzip compression

## Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Using Docker
Create `Dockerfile` and deploy to cloud platforms.

## Deploy on Render (Docker)

This repository includes a `Dockerfile` configured to run Nexora on Render using Docker. The image installs system dependencies needed by WeasyPrint and Tesseract — if you don't use those features you can remove those packages to slim the image.

Quick local build and run:

```bash
docker build -t nexora:local .
docker run -p 5000:5000 -e PORT=5000 nexora:local
```

To deploy on Render using the included `render.yaml`:

1. Push this repository to GitHub.
2. In the Render dashboard, connect your GitHub repo and enable Deploy from `render.yaml` or import the service.
3. Render will build the Docker image using the repository `Dockerfile` and run the web service.

Notes:
- The `run.py` entrypoint safely loads the main `app.py` and is used by Gunicorn in the Dockerfile (`gunicorn run:app`).
- The Dockerfile exposes a port and honors `$PORT` provided by Render. Adjust the `render.yaml` `envVars` or Render service settings as needed.

## Continuous Integration (Docker image build)

This repository includes a GitHub Actions workflow that builds and publishes a Docker image to GitHub Container Registry (GHCR) on push to `main`.

- Workflow file: `.github/workflows/docker-build.yml`
- The workflow builds and pushes two tags: `ghcr.io/<owner>/nexora:latest` and `ghcr.io/<owner>/nexora:<commit-sha>`.
- By default the workflow uses `${{ secrets.GITHUB_TOKEN }}` for authentication to GHCR. You may instead provide a personal access token with `packages:write` privileges as `CR_PAT` if required.

To enable the workflow:

1. Ensure the repository is hosted on GitHub and Actions are enabled.
2. Optionally create a long-lived token in `Settings → Developer settings` if you want to use a PAT.

## Render deployment notes

- `render.yaml` is included and references the `Dockerfile`. Edit `render.yaml` to set production `DATABASE_URL` and safe `SECRET_KEY` values (use Render's dashboard or secrets to store them securely).
- Recommended Render env vars: `DATABASE_URL`, `SECRET_KEY`, `MAIL_USERNAME`, `MAIL_PASSWORD`.


## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Add your license here]

## Support

For issues, questions, or suggestions, please contact: support@aidiniglobal.com

## Roadmap

- [ ] Multi-language support
- [ ] Video consultations
- [ ] Payment gateway integration
- [ ] Mobile app
- [ ] AI-powered recommendations
- [ ] Document automation
- [ ] Government integration APIs
- [ ] Real-time application status tracking

---

**Version:** 2.0 (Enhanced Residency Platform)
**Last Updated:** December 2025
**Developed by:** Aidni Global LLP
