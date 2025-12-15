from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Post, Comment, Category
from forms import CommentForm
from sqlalchemy import desc

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True).order_by(desc(Post.created_at)).paginate(
        page=page, per_page=10
    )
    return render_template('index.html', posts=posts)

@blog_bp.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    form = CommentForm() if current_user.is_authenticated else None
    
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(post_id=post.id).order_by(desc(Comment.created_at)).paginate(
        page=page, per_page=20
    )
    
    return render_template('post.html', post=post, form=form, comments=comments)

@blog_bp.route('/post/<slug>/comment', methods=['POST'])
@login_required
def add_comment(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
    else:
        flash('Error posting comment', 'danger')
    
    return redirect(url_for('blog.post', slug=slug))

@blog_bp.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = category.posts.filter_by(published=True).order_by(desc(Post.created_at)).paginate(
        page=page, per_page=10
    )
    return render_template('category.html', category=category, posts=posts)
