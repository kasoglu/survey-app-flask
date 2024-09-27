from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    definition = db.Column(db.String(1000))  # Additional information if needed
    options = db.relationship('Option', backref='question', lazy=True)

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # The score tied to this option
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)


# User model to store personal information
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firma_adi = db.Column(db.String(100), nullable=False)
    bolum = db.Column(db.String(100), nullable=False)
    gorev = db.Column(db.String(100), nullable=False)
    nitelik = db.Column(db.String(100), nullable=False)
    gorev_tanimi = db.Column(db.String(500), nullable=False)
    genel_is_tanimi = db.Column(db.String(500), nullable=False)
    calisabilecek_personel_sayisi = db.Column(db.String(100), nullable=False)

    answers = db.relationship('Answer', backref='user', lazy=True)


# Answer model to store survey responses linked to the user
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    q_1 = db.Column(db.String(10000))
    q_2 = db.Column(db.String(10000))
    q_3 = db.Column(db.String(10000))
    q_4 = db.Column(db.String(10000))
    q_5 = db.Column(db.String(10000))
    q_6 = db.Column(db.String(10000))
    q_7 = db.Column(db.String(10000))
    q_8 = db.Column(db.String(10000))
    q_9 = db.Column(db.String(10000))
    q_10 = db.Column(db.String(10000))
    q_11 = db.Column(db.String(10000))
    q_12 = db.Column(db.String(10000))
    q_13 = db.Column(db.String(10000))
    q_14 = db.Column(db.String(10000))
    q_15 = db.Column(db.String(10000))
    q_16 = db.Column(db.String(10000))

    total_score = db.Column(db.Integer, nullable=False)


# Form to collect user personal information
class StartSurveyForm(FlaskForm):
    firma_adi = StringField('Firma Adı', validators=[DataRequired()])
    bolum = StringField('Bölüm', validators=[DataRequired()])
    gorev = StringField('Görev', validators=[DataRequired()])
    nitelik = StringField('Nitelik', validators=[DataRequired()])
    gorev_tanimi = StringField('Görev Tanımı', validators=[DataRequired()])
    genel_is_tanimi = StringField('Genel İş Tanımı', validators=[DataRequired()])
    calisabilecek_personel_sayisi = StringField('Çalışabilecek Personel Sayısı', validators=[DataRequired()])
    submit = SubmitField('Ankete Başla')


# Dynamic form to display each question
class SurveyForm(FlaskForm):
    options = RadioField('Seçenekler', choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')

def get_secenekler_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        details = {}
        for question in data['questions']:
            soru_id = question['question_id']
            details[soru_id] = {
                "details": question.get('details', [])  # Tanımlar ve notları alır.
            }

        return details

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/anket/basla', methods=['GET', 'POST'])
def start_survey():
    form = StartSurveyForm()

    if form.validate_on_submit():
        # Kullanıcı bilgilerini session'da sakla
        session['firma_adi'] = form.firma_adi.data
        session['bolum'] = form.bolum.data
        session['gorev'] = form.gorev.data
        session['nitelik'] = form.nitelik.data
        session['gorev_tanimi'] = form.gorev_tanimi.data
        session['genel_is_tanimi'] = form.genel_is_tanimi.data
        session['calisabilecek_personel_sayisi'] = form.calisabilecek_personel_sayisi.data

        user_info = User(
            firma_adi=session.get('firma_adi'),
            bolum=session.get('bolum'),
            gorev=session.get('gorev'),
            nitelik=session.get('nitelik'),
            gorev_tanimi=session.get('gorev_tanimi'),
            genel_is_tanimi=session.get('genel_is_tanimi'),
            calisabilecek_personel_sayisi=session.get('calisabilecek_personel_sayisi')
        )

        try:
            db.session.add(user_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Veritabanı hatası: {e}")

        session['user_id']  = user_info.id


        return redirect(url_for('survey', soru_id=1))  # İlk soruya yönlendir

    return render_template('start_survey.html', form=form)


@app.route('/anket/soru/<int:soru_id>', methods=['GET', 'POST'])
def survey(soru_id):
    # Soru id'ye göre arıyoruz
    question = Question.query.filter_by(id=soru_id).first()

    file_path = 'details.json'
    details = get_secenekler_from_json(file_path)

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('start_survey'))

    if not question:
        return redirect(url_for('results'))  # Eğer soru yoksa sonuçlara git

    form = SurveyForm()
    form.options.choices = [(str(opt.id), opt.text) for opt in question.options]  # Seçenekleri ayarla

    if form.validate_on_submit():
        selected_answer_id = form.options.data

        # Session.get() kullanarak seçilen seçeneği al
        selected_option = db.session.get(Option, selected_answer_id)

        # Puanları session içinde tutuyoruz
        total_score = session.get('total_score', 0)
        total_score += selected_option.score
        session['total_score'] = total_score

        # Kullanıcı cevaplarını session'da sakla
        answers = session.get('answers', {})
        answers[f'q_{soru_id}'] = selected_option.text
        session['answers'] = answers


        # Son soru kontrolü
        next_question_id = soru_id + 1
        if not Question.query.filter_by(id=next_question_id).first():
            # Eğer son sorudaysak, cevapları veritabanına kaydet
            user_id = session.get('user_id')



            try:
                answer = Answer(
                    user_id=user_id,
                    q_1=answers.get('q_1'),
                    q_2=answers.get('q_2'),
                    q_3=answers.get('q_3'),
                    q_4=answers.get('q_4'),
                    q_5=answers.get('q_5'),
                    q_6=answers.get('q_6'),
                    q_7=answers.get('q_7'),
                    q_8=answers.get('q_8'),
                    q_9=answers.get('q_9'),
                    q_10=answers.get('q_10'),
                    q_11=answers.get('q_11'),
                    q_12=answers.get('q_12'),
                    q_13=answers.get('q_13'),
                    q_14=answers.get('q_14'),
                    q_15=answers.get('q_15'),
                    q_16=answers.get('q_16'),
                    total_score=total_score
                )
                db.session.add(answer)
                db.session.commit()
                session.pop('answers')  # Cevapları session'dan temizle
                session.pop('total_score')  # Skoru da session'dan temizle
            except Exception as e:
                db.session.rollback()
                print(f"Veritabanı hatası: {e}")
                flash("Veritabanı hatası meydana geldi, lütfen tekrar deneyin.", "error")
            return redirect(url_for('results'))  # Sonuçlar sayfasına yönlendir

        # Sonraki soruya yönlendir
        return redirect(url_for('survey', soru_id=next_question_id))

    return render_template('survey.html', form=form, question=question, details=details[soru_id]['details'])






@app.route('/anket/sonuc')
def results():
    last_user_info = User.query.order_by(User.id.desc()).first()
    selected_answers = Answer.query.order_by(Answer.id.desc()).first()

    # Sonuçları eğer varsa göster, yoksa hata mesajı gösterin.
    if last_user_info and selected_answers:
        return render_template('results.html', last_user=last_user_info, selected_answers=selected_answers)
    else:
        return "Kullanıcı kaydı bulunamadı."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)