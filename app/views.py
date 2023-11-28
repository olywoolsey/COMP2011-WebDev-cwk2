from app import app
from flask import Flask, render_template, redirect, url_for, flash, request

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/about')
def about():
    return "About me"
