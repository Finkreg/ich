from app.models import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    questions = db.relationship('Question', back_populates='category', lazy=True)

    def __repr__(self):
        return f'Category {self.name}'

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    category = db.relationship('Category', back_populates='questions', lazy=True)
    responses = db.relationship('Response', back_populates='question', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'Question {self.text}'

