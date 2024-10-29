from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        new_file = Document(name=file.filename, data=file.read())
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/download')
def download():
    documents = Document.query.all()
    return render_template('download.html', documents=documents)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        new_message = Message(username=username, content=content)
        db.session.add(new_message)
        db.session.commit()
    messages = Message.query.all()
    return render_template('chat.html', messages=messages)

@app.route('/collaborate')
def collaborate():
    return render_template('collaborate.html')

if __name__ == '__main__':
    app.run(debug=True)
