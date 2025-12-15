# Blog Platform with Admin Panel

A production-ready blogging platform built with Python, Flask, and SQLAlchemy. Features user authentication, role-based access control, CRUD operations for posts, categories, and comments, plus a comprehensive admin dashboard.

## Features

### User Authentication
- User registration and login
- Password hashing with Werkzeug
- Session-based authentication with Flask-Login
- Role-based access (USER and ADMIN)

### Blog Management
- Create, read, update, delete blog posts
- SEO-friendly URL slugs (auto-generated from titles)
- Post categorization with many-to-many relationships
- Pagination for blog listing
- Rich content support (HTML)

### Comments System
- Users can comment on published posts
- Admin can view and delete comments
- Paginated comment display
- Comment timestamps and author information

### Category System
- Create and manage categories
- Many-to-many relationship with posts
- Category-based post filtering
- Auto-generated slugs from category names

### Admin Dashboard
- Overview with statistics (users, posts, comments, categories)
- Recent activity display
- Quick action buttons
- User management
- Complete CRUD interfaces for all resources

## Tech Stack

- **Backend**: Python 3, Flask
- **ORM**: SQLAlchemy
- **Database**: SQLite (default, easily switchable to MySQL/PostgreSQL)
- **Authentication**: Flask-Login, Werkzeug
- **Forms**: Flask-WTF, WTForms
- **Frontend**: HTML5, Bootstrap 5, Jinja2
- **Security**: CSRF protection, password hashing, role-based access control

## Project Structure

```
blog_app/
├── app.py                    # Main Flask application
├── config.py               # Configuration settings
├── models.py               # SQLAlchemy ORM models
├── forms.py                # WTForms definitions
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── blog.py            # Blog routes
│   └── admin.py           # Admin panel routes
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── index.html         # Blog homepage
│   ├── post.html          # Single post view
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── category.html      # Category listing
│   └── admin/
│       ├── dashboard.html
│       ├── manage_posts.html
│       ├── manage_categories.html
│       ├── manage_comments.html
│       ├── manage_users.html
│       ├── create_post.html
│       ├── edit_post.html
│       ├── create_category.html
│       └── edit_category.html
├── static/
│   └── css/
│       └── style.css      # Custom CSS
├── requirements.txt       # Python dependencies
├── blog.db               # SQLite database (auto-created)
└── README.md            # This file
```

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd "/Users/saipandu/blog website with admin panel(Flask CMS)"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## Default Admin Account

The application automatically creates a default admin user on first run:
- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change this password in production!

## Usage

### User Registration & Login
1. Click "Register" in the navbar
2. Fill in username, email, and password
3. Log in with your credentials
4. Log out anytime from the dropdown menu

### Reading Blog Posts
- View all published posts on the homepage
- Click "Read More" to view full post with comments
- Browse posts by category
- Post comments (requires login)

### Admin Features

#### Access Admin Panel
- Log in with admin account
- Click "Admin Panel" in navbar
- View dashboard with statistics and recent activity

#### Manage Posts
1. Click "Manage Posts"
2. Create new post: Click "Create New Post"
3. Edit post: Click "Edit" button
4. Delete post: Click "Delete" button
5. Assign categories when creating/editing posts

#### Manage Categories
1. Click "Manage Categories"
2. Create new category: Click "Create New Category"
3. Edit category: Click "Edit" button
4. Delete category: Click "Delete" button

#### Manage Comments
1. Click "Manage Comments"
2. View all user comments
3. Delete inappropriate comments: Click "Delete" button

#### Manage Users
1. Click "Manage Users"
2. View all registered users
3. See user roles, post counts, and join dates

## Database Models

### User
- id, username (unique), email (unique)
- password_hash, role (USER/ADMIN)
- created_at, relationships to posts and comments

### Post
- id, title, slug (unique, auto-generated), content
- user_id (author), created_at, updated_at, published
- relationships to author, categories, and comments

### Category
- id, name (unique), slug (unique, auto-generated)
- description, created_at
- many-to-many relationship with posts

### Comment
- id, content, user_id (author), post_id
- created_at, updated_at
- relationships to author and post

### PostCategory (Junction Table)
- post_id, category_id (many-to-many relationship)

## Security Features

- **Password Hashing**: Using Werkzeug's secure hashing
- **CSRF Protection**: Flask-WTF form protection
- **Input Validation**: WTForms validators on all inputs
- **Authentication**: Flask-Login session management
- **Role-Based Access**: Admin-only routes protected with decorators
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries

## Configuration

Edit `config.py` to customize:
- Database URI (change to MySQL/PostgreSQL if needed)
- Session duration
- Posts per page
- Comments per page
- Environment (development/production)

## Production Deployment

Before deploying to production:

1. **Change secret key**: Update `SECRET_KEY` in `config.py`
2. **Change admin password**: Log in and update it
3. **Set production config**: Use `ProductionConfig` class
4. **Use a production database**: Switch from SQLite
5. **Use HTTPS**: Set `SESSION_COOKIE_SECURE = True`
6. **Set environment variables**: Use `.env` file
7. **Use a production WSGI server**: Gunicorn, uWSGI, etc.

Example for Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## Troubleshooting

### Database Issues
If you encounter database errors, delete `blog.db` and restart:
```bash
rm blog.db
python app.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## License

This project is free to use and modify for personal and commercial purposes.

## Support

For issues or questions, refer to the source code comments or review the Flask/SQLAlchemy documentation.

## Future Enhancements

- Search functionality
- User profiles and author pages
- Email notifications
- Post tags
- Social sharing buttons
- SEO optimization
- Performance caching
- API endpoints
- Dark mode theme
