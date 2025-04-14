# Django Awesome

Django Awesome is a social platform where users can upload and share photos, comment on them, and chat with others. Built with Django and HTMX, it provides a responsive interface with features like user authentication, real-time messaging, and photo sharing.

## Screenshots

<img src="images/home.png" alt="Home Screen" width="250"/>          <img src="images/comment%20and%20reply.png" alt="Comment and Reply" width="250"/>        
  <img src="images/inbox%20message.png" alt="Inbox Message" width="250"/>




## Django Social Photo App

A social photo-sharing app built with Django where users can upload photos, share them with others, leave comments, and chat with each other.

## Features

- **User registration and login:** Secure authentication features.
- **Uploading and viewing photos:** A smooth interface for managing photos.
- **Commenting on photos:** Engage with content and provide feedback.
- **Real-time chat between users:** Enjoy seamless, live communication.
- **Responsive UI with Tailwind CSS:** A clean and responsive user interface.
- **User avatars for profiles:** Enhance user identity representation.

## Technologies Used

- **Django** (Backend)
- **HTMX + TailwindCSS** (Frontend)
- **Pillow** for image processing
- **SQLite** (with the option to switch to PostgreSQL)
- **JavaScript**

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository**

   Open your terminal and clone the repository using:
   ```bash
   git clone https://github.com/alirezasalimzadeh/django-awesome.git
   cd django-awesome
   
2. **Create and Activate a Virtual Environment**
   
   It is highly recommended to use a virtual environment to manage project dependencies:
   On Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
   ```
   On macOS and Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
   ```
3. **Install Dependencies**

   Install the required packages listed in the requirements.txt file:
   ```bash
      pip install -r requirements.txt
   ```

4. **Apply Migrations**

   Set up your database by applying Django migrations:
   ```bash
      python manage.py migrate
   ```
5. **Create a Superuser (Optional)**
   
   To access the Django admin panel, create a superuser:
   ```bash
      python manage.py createsuperuser
   ```
   
Follow the prompts to complete the user creation.

6. **Run the Development Server**
   Start the Django development server:
   ```bash
      python manage.py runserver
   ```
   
Then, open your browser and navigate to http://127.0.0.1:8000/ to see your project in action.

7. **Additional Configuration**
   
   If your project requires environment-specific variables (like SECRET_KEY or DEBUG), create a .env file in the project root based on the provided template (if available).
   For production environments, make sure to configure your static files settings and run:
   ```bash
   python manage.py collectstatic
   ```
