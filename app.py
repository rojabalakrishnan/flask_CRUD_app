from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_posts.db'
db = SQLAlchemy(app)


class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pay_per_hour = db.Column(db.Integer, nullable=False, default=20)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Blog post ' + str(self.id)



@app.route('/')
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        pay_per_hour = request.form['pay_per_hour']
        expiry_date = request.form['expiry_date']

        expiry_date_old = expiry_date.replace('T', ' ')
        expiry_date_new = datetime.strptime(expiry_date_old, '%Y-%m-%d %H:%M')

        new_job_post = JobPost(title=job_title, description=job_description, pay_per_hour=pay_per_hour,
                               expiry_date=expiry_date_new)
        db.session.add(new_job_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_job_posts = JobPost.query.order_by(JobPost.date_posted).all()
        return render_template('posts.html', job_posts=all_job_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    job_post = JobPost.query.get_or_404(id)
    db.session.delete(job_post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    job_post = JobPost.query.get_or_404(id)
    if request.method == 'POST':
        job_post.title = request.form['title']
        job_post.description = request.form['description']
        job_post.pay_per_hour = request.form['pay_per_hour']
        expiry_date = request.form['expiry_date1']

        expiry_date_old = expiry_date.replace('T', ' ')
        expiry_date_new = datetime.strptime(expiry_date_old, '%Y-%m-%d %H:%M')

        job_post.expiry_date = expiry_date_new
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', job_post=job_post)

@app.route('/posts/new', methods=['GET', 'POST'])

def new_post():
    if request.method == 'POST':
        job_title = request.form['title']
        job_description = request.form['description']
        pay_per_hour = request.form['pay_per_hour']
        expiry_date = request.form['expiry_date']

        expiry_date_old = expiry_date.replace('T', ' ')
        expiry_date_new = datetime.strptime(expiry_date_old, '%Y-%m-%d %H:%M')

        new_job_post = JobPost(title=job_title, description=job_description, pay_per_hour=pay_per_hour,
                               expiry_date=expiry_date_new)
        db.session.add(new_job_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')
if __name__ == "__main__":
    app.run(debug=True)
