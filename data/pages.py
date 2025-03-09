from flask import Flask, render_template


def main():
    app = Flask(__name__)

    @app.route('/')
    def main_page():
        user = 'None'
        return render_template('templates/main_page.html', title='Домашняя страница', username=user)

    @app.route('/account')
    def account():
        return 'И здесь могла быть ваша реклама!'

    @app.route('/registration')
    def registration():
        return 'И даже здесь могла быть ваша реклама!'

    @app.route('/logIn')
    def logIn():
        return 'И тут могла быть ваша реклама!'

    @app.route('/reading')
    def reading():
        return 'И на Марсе могла быть ваша реклама!'

    app.run(port=8080, host='127.0.0.1')
