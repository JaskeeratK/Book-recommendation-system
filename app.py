from flask import *
import numpy as np
import joblib as joblib
from app import *
from flask import request,render_template


popular_data=joblib.load(open('populer.pkl','rb'))
pt=joblib.load(open('pt.pkl','rb'))
books_df = joblib.load(open('books_df.pkl','rb'))
similarity=joblib.load(open('similarity1.pkl','rb'))


app=Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_data['Book-Title'].values),
        author=list(popular_data['Book-Author'].values),
        image=list(popular_data['Image-URL-M'].values),
        rating=list(popular_data['Num-Rating'].values),
        avg=list(popular_data['avg_rating'].values)
    )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books' ,methods=['post'])


def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data = []
    for i in similar_books:
        item = []
        temp_df = books_df[books_df['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)