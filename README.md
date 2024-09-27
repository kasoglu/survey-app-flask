
# Flask Survey Application

This is a simple Flask-based web application that allows users to fill out a survey with multiple-choice questions. The survey collects personal information before starting and calculates a total score based on the user's responses. All data is stored in a SQLite database.

## Features

- User-friendly survey with 16 multiple-choice questions.
- Personal information collection form (e.g., firm name, role, job description).
- Dynamic question navigation (one question per page).
- Survey results display after the last question is answered.
- Total score calculation based on responses.
- Data is stored in an SQLite database for future retrieval.
  
## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [File Structure](#file-structure)
- [License](#license)

## Installation

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.x
- `pip` (Python package installer)
- Flask

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Create a Virtual Environment

It is recommended to create a virtual environment for your project to avoid conflicts between dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate  # For Windows
```

### Install Dependencies

Install all necessary Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### Database Setup

The project uses an SQLite database. To initialize the database, follow these steps:

1. Open a Python shell:

   ```bash
   flask shell
   ```

2. Inside the Python shell, run the following commands:

   ```python
   from app import db
   db.create_all()
   ```

This will create the required tables in your SQLite database.

### Running the Application

Start the Flask development server:

```bash
flask run
```

By default, the application will be available at `http://127.0.0.1:5000/`.

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000/`.
2. Click "Start Survey" to begin.
3. Fill out the personal information form.
4. Answer the survey questions (one per page).
5. After completing the survey, the results will be displayed, including the total score and personal information summary.

## Endpoints

- `/`: The homepage, where users can start the survey.
- `/anket/basla`: Collects personal information before the survey.
- `/anket/soru/<int:soru_id>`: Displays the survey questions one by one.
- `/anket/sonuc`: Shows the survey results after completion.
- `/results`: Displays the survey result and the associated personal data of the user.

## File Structure

```bash
.
├── app/
│   ├── __init__.py        # Flask app and database setup
│   ├── models.py          # Database models (User, Answer, etc.)
│   ├── routes.py          # Application routes
│   ├── templates/
│   │   ├── index.html     # Home page
│   │   ├── start_survey.html # Form to capture personal information
│   │   ├── survey.html    # Page for survey questions
│   │   └── results.html   # Survey results page
│   └── static/
├── venv/                  # Virtual environment (generated after creating virtualenv)
├── requirements.txt        # Project dependencies
├── config.py               # Application configuration
├── run.py                  # Script to run the Flask app
└── README.md               # Project documentation (this file)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
