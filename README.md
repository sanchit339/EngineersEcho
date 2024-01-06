# The EngineersEcho Blog Website

## Introduction
The EngineersEcho is a dynamic full-stack blog website developed using Django, HTML, CSS, Bootstrap, AWS, and SQLite. This README provides information about the tech stack, features, and deployment details.

## Tech Stack
- Django
- HTML
- CSS
- Bootstrap
- AWS (S3 for file uploads, SMTP for email services)
- SQLite

## Features

### User Authentication
- Implemented user authentication functionalities, including Register, Login, Logout, and Profile Management.

### AWS Integration
- Utilized AWS S3 Buckets for efficient file uploads.
- Implemented SMTP mail services for password reset functionality.

### Performance Optimization
- Implemented Pagination for better navigation and user experience.
- Utilized image compression techniques to optimize website performance.

### Database
- Used SQLite for data storage.
- Enabled user profile searches by usernames.

### Deployment
- Deployed the website using Nginx as a reverse proxy and Gunicorn combination for efficient handling of web requests.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. Setup is same as default Django setup.
3. Install Dependencies in requirements.txt file
   ```bash
   pip install -r requirements.txt
4. Start the Development Server
   ```bash
   python manage.py runserver

## Deployment
    Follow the deployment guide in the DEPLOYMENT.md file for deploying the website on a production server.

## Issues and Contributions
   If you encounter any issues or have suggestions for improvement, please open an issue on GitHub. Contributions are welcome!