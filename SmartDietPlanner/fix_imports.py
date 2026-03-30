
with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('from flask import Flask, render_template, request, redirect, url_for, session, flash',
                    'from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify')

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed jsonify import!')

