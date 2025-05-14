# app/views.py
from flask import Blueprint, render_template, request
from app.models import Word
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

main = Blueprint('main', __name__, template_folder='../templates')

engine = create_engine('sqlite:///wordbook.db')
Session = sessionmaker(bind=engine)
session = Session()

@main.route('/')
def home():
    return render_template('search.html')

@main.route('/search')
def search():
    from sqlalchemy import func
    query = request.args.get('q', '').strip()
    # sort = request.args.get('sort', 'english')
    order = request.args.get('order', 'asc')
    results = []

    if query:
        q = session.query(Word).filter(Word.english.ilike(f'%{query}%'))

        # if sort == 'meaning':
        #     col = Word.meaning
        # elif sort == 'example_len':
        #     col = func.char_length(Word.example_sentence)
        # else:
        #     col = Word.english

        sort_column = Word.english

        if order == 'desc':
            q = q.order_by(sort_column.desc())
        else:
            q = q.order_by(sort_column.asc())

        results = q.all()

        # results = (session.query(Word)
        #     .filter(Word.english.ilike(f'%{query}%'))
        #     .all())

    return render_template('search.html', query=query, results=results)
