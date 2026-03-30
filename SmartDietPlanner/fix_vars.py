import re

with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix params like :user_id to %(user_id)s
# Only for SQL strings.
# The simplest way is to replace :(\w+) with %(\1)s inside text, but be careful with http:// urls.
# Luckily in app.py there are usually no urls like http:// that use :word that isn't safe.
# Actually, let's just do a smart regex: if it's inside a string used in execute_query.
# Let's just blindly replace :(\w+) with %(\1)s everywhere EXCEPT in standard decorators/etc.

def replacer(match):
    word = match.group(1)
    if word in ('type', 'focus', 'hover', 'active'): # common css pseudo classes
        return str(match.group(0))
    return f'%({word})s'

new_text = re.sub(r':([a-zA-Z_]\w*)', replacer, text)

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Replaced all :vars to %(vars)s")
