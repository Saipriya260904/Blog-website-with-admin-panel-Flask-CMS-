from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from models import db, Post, User, Comment, Category
from forms import PostForm, CategoryForm
from sqlalchemy import desc

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    total_categories = Category.query.count()
    
    recent_posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    recent_comments = Comment.query.order_by(desc(Comment.created_at)).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_posts=total_posts,
        total_comments=total_comments,
        total_categories=total_categories,
        recent_posts=recent_posts,
        recent_comments=recent_comments
    )

@admin_bp.route('/posts')
@login_required
@admin_required
def manage_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.created_at)).paginate(page=page, per_page=10)
    return render_template('admin/manage_posts.html', posts=posts)

@admin_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    form = PostForm()
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        slug = Post.generate_slug(form.title.data)
        
        if Post.query.filter_by(slug=slug).first():
            flash('A post with this title already exists', 'danger')
            return redirect(url_for('admin.create_post'))
        
        post = Post(
            title=form.title.data,
            slug=slug,
            content=form.content.data,
            user_id=current_user.id
        )
        
        if form.categories.data:
            categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
            post.categories = categories
        
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin.manage_posts'))
    
    return render_template('admin/create_post.html', form=form)

@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.slug = Post.generate_slug(form.title.data)
        
        if form.categories.data:
            post.categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        else:
            post.categories = []
        
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin.manage_posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.categories.data = [c.id for c in post.categories]
    
    return render_template('admin/edit_post.html', form=form, post=post)

@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin.manage_posts'))

@admin_bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.name).paginate(page=page, per_page=10)
    return render_template('admin/manage_categories.html', categories=categories)

@admin_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    form = CategoryForm()
    
    if form.validate_on_submit():
        slug = Category.generate_slug(form.name.data)
        
        if Category.query.filter_by(slug=slug).first():
            flash('A category with this name already exists', 'danger')
            return redirect(url_for('admin.create_category'))
        
        category = Category(name=form.name.data, slug=slug, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/create_category.html', form=form)

@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = Category.generate_slug(form.name.data)
        category.description = form.description.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.manage_categories'))
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    
    return render_template('admin/edit_category.html', form=form, category=category)

@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.manage_categories'))

@admin_bp.route('/comments')
@login_required
@admin_required
def manage_comments():
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.order_by(desc(Comment.created_at)).paginate(page=page, per_page=20)
    return render_template('admin/manage_comments.html', comments=comments)

@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_slug = comment.post.slug
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(request.referrer or url_for('admin.manage_comments'))

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/manage_users.html', users=users)
