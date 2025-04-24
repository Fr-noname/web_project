from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.books import Book
from data.users import User
from forms.news import BookForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'qwertyuiopasdfghjkl_ghhasdfjksdfghsdaf_ebanoeafaffd_g0vn0:hgdfsahfsaf132213'


def main():
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    book = db_sess.query(Book)
    return render_template("index.html", news=book, title='Главная страница')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect("/")


@app.route('/book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        book = Book()
        print(form.title.data)
        book.title = form.title.data
        book.content = form.content.data
        book.is_private = form.is_private.data
        current_user.book.append(book)
        #  Изменили текущего пользователя с помощью метода merge:
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление книги',
                           form=form)


# Пробуем запустить

# 3-2 Редактирование новости:
@app.route('/book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = BookForm()
    # Если мы запросили страницу записи,
    if request.method == "GET":
        # ищем ее в базе по id, причем автор новости должен совпадать с текущим пользователем.
        db_sess = db_session.create_session()
        news = db_sess.query(Book).filter(Book.id == id,
                                          Book.user == current_user).first()
        if news:
            # Если что-то нашли, предзаполняем форму:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            # иначе показываем пользователю страницу 404:
            abort(404)
    # Такую же проверку на всякий случай делаем перед изменением новости.
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Book).filter(Book.id == id,
                                          Book.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование книги',
                           form=form
                           )


# 3-3 Добавляем в шаблон index.html кнопки: "Изменить" и "Удалить"

# Пробуем запустить

# 3-4 Обработчик удаления записей:
@app.route('/book_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    try:
        db_sess = db_session.create_session()
        news = db_sess.query(Book).filter(Book.id == id,
                                          Book.user == current_user
                                          ).first()
    except Exception:
        print('БД умерла.')
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('Глобальная ошибка')
