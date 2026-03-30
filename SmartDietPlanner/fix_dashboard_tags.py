with open('flask_app/templates/user_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

if '</body>' not in content:
    content += '\n</body>\n</html>'
    with open('flask_app/templates/user_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Appended closing tags")
else:
    print("Closing tags exist")
