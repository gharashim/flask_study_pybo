from pybo import db

# 질문 - 답변 모델
# 질문 class
# - id, subject, content, create_date

# 답변 class
# - id, question_id, subject, content, create_date

question_voter = db.Table(
    'question_voter',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id', ondelete = 'CASCADE'),
        primary_key = True
    ),
    db.Column(
        'question_id',
        db.Integer,
        db.ForeignKey('question.id', ondelete = 'CASCADE'),
        primary_key = True
    )
)

answer_voter = db.Table(
    'answer_voter',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id', ondelete = 'CASCADE'),
        primary_key = True
    ),
    db.Column(
        'answer_id',
        db.Integer,
        db.ForeignKey('answer.id', ondelete='CASCADE'),
        primary_key=True
    )
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True, server_default='1')
    user = db.relationship("User", backref = db.backref("question_set"))
    modify_date = db.Column(db.DateTime(), nullable = True)
    voter = db.relationship('User', secondary = question_voter, backref = db.backref('question_voter_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # question_id : 답변을 질문과 연결 하기 위해 추가한 속성
    # db.ForeignKey : 질문 - 답변 모델을 서로 연겨할 때 사용
    # question.id : question 클래스의 id 속성
    # ondelete는 삭제 연동 설정 이다. 즉, ondelete='CASCADE'는 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다는 의미
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete = "CASCADE"))
    # backref : 역참조 설정
    question = db.relationship("Question", backref = db.backref("answer_set"))
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = True, server_default = '1')
    user = db.relationship("User", backref = db.backref("answer_set"))
    modify_date = db.Column(db.DateTime(), nullable = True)
    voter = db.relationship('User', secondary = answer_voter, backref = db.backref('answer_voter_set'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)