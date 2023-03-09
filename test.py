from flask import Flask, session

app = Flask(__name__)
app.config.update(ENV='development')
app.secret_key  = "secret key"

@app.route('/session/<string:user_name>')
def set_session(user_name):
    session["user_name"] = user_name
    return f"User name {user_name} set to session"


@app.route('/session/user')
def get_session():
    return session["user_name"]
if __name__ == '__main__':
    app.run(debug=True)