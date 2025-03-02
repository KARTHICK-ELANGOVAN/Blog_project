# BLOG Website

# TITLE - BLOG NEST

## Overview
This is a **full-stack e-commerce website** built using **Django, MySQL, HTML, CSS, and JavaScript**. The project includes features for product browsing, user authentication, shopping cart management, and order processing. It is designed to provide a seamless online shopping experience with an intuitive UI/UX.

##Project Structure

myapp/                  # Main Django application
│── blog/              # Blog app for adding and managing blog content
│── members/           # Authentication app (login, registration, user management)
│── static/            # Static files (CSS, JS, images)
│── templates/         # HTML templates for rendering UI
│── manage.py          # Django's project management file
│── db.sqlite3         # SQLite database (can be switched to MySQL)


## Features
### **1. User Authentication**
- User registration and login (via the **Members** app)
- Password reset and authentication
- Secure session management

### **2. Product & Blog Management**
- Display products dynamically
- Blog section (via the **Blog** app) where users can view and interact with blog content
- Admin panel for adding, editing, and deleting products/blogs


### **5. Responsive UI/UX**
- Modern design with **HTML, CSS, and JavaScript**
- Mobile-friendly and fully responsive



## Installation & Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/KARTHICK-ELANGOVAN/Blog_project.git
cd Blog_project
```
### **2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```
### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4. Apply Migrations**
```bash
python manage.py migrate
python manage.py makemigrations
```
### **5. Run the Server**
```bash
python manage.py runserver
```
Visit **karthickelangovan.pythonanywhere.com** to view the application.

## Future Enhancements
- Implement **AI-powered product recommendations**
- Add **payment gateway integration**
- Improve UI with **React.js frontend**
- Dockerize the project for better deployment

## Contribution
Feel free to fork this repository and make improvements. Pull requests are welcome!

##Creation
   By KARTHICK E - Full stack python developer..
## Contact
For any questions or collaboration, reach out to me on ** email me at **karthielangovan2003@gmail.com**.

