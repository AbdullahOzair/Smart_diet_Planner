with open('user_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
start = 0
for i, l in enumerate(lines):
    if l.strip() == "{% elif view == 'add_activity_log' %}" or l.strip() == "{% if view == 'add_activity_log' %}":
        start = i
        break

if start > 0:
    for i in range(start, start + 250):
        if 'col-' in lines[i] and '<!--' not in lines[i]:
            print(f'{i}: {lines[i].strip()}')
    print('--------- MEAL LOG ----------')
    for i, l in enumerate(lines):
        if l.strip() == "{% elif view == 'add_meal_log' %}" or l.strip() == "{% if view == 'add_meal_log' %}":
            start_m = i
            break
    for i in range(start_m, start_m + 250):
        if 'col-' in lines[i] and '<!--' not in lines[i]:
            print(f'{i}: {lines[i].strip()}')
