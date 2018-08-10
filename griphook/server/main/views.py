from flask import render_template


def home():
    return render_template('main/home.html')
