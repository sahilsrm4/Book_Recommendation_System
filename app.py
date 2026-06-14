 
from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Load files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarty_score.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():

    user_input = request.form.get('user_input')

    # Remove extra spaces
    user_input = user_input.strip()

    # Find matching book irrespective of case
    matching_books = [
        book for book in pt.index
        if book.lower() == user_input.lower()
    ]

    # Book not found
    if len(matching_books) == 0:
        return render_template(
            'recommend.html',
            error="❌ Book not found. Please enter a valid book title."
        )

    # Get actual title from dataset
    selected_book = matching_books[0]

    index = np.where(pt.index == selected_book)[0][0]

    # Skip first item because it is the book itself
    similar_items = sorted(
        list(enumerate(similarity_score[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:9]

    data = []

    for i in similar_items:

        item = []

        temp_df = books[
            books['Book-Title'] == pt.index[i[0]]
        ]

        temp_df = temp_df.drop_duplicates('Book-Title')

        item.extend(
            list(temp_df['Book-Title'].values)
        )

        item.extend(
            list(temp_df['Book-Author'].values)
        )

        item.extend(
            list(temp_df['Image-URL-M'].values)
        )

        data.append(item)

    return render_template(
        'recommend.html',
        data=data
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
 
