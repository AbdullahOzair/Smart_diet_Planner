with open('user_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(3400, 3420):
    print(f'{i}: {lines[i].rstrip()}')
