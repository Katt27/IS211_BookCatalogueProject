from flask import render_template, url_for, redirect, flash, request
from . import app, db
from .models import User, Book
from .auth import login_required, login_user, logout_user
from .google_books_api import search_books_by_isbn, search_books_by_title

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', books=Book.query.filter_by(user_id=current_user.id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login logic here
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
def search():
    isbn = request.form.get('isbn')
    books = search_books_by_isbn(isbn)
    return render_template('search_results.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    book_data = request.form
    new_book = Book(title=book_data['title'], author=book_data['author'], page_count=book_data['page_count'],
                    average_rating=book_data['average_rating'], thumbnail_url=book_data['thumbnail_url'],
                    user_id=current_user.id)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))
