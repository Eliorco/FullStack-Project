from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "$2b$12$O6de.w1FB5HTnee8Ak9WLusDlGoouoVT5CCQMGEwTMfD6nUI/BUiC"


@app.route("/")
def home():
    return '<H1>Herolo World<H1/>'

if __name__ == "__main__":
    app.run(debug=True)
