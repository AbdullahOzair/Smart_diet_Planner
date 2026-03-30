import codecs

def final_patch():
    try:
        with open('flask_app/templates/user_dashboard.html', 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')

        # Line 774 is currently user_add_daily_log and says Add Water.
        for i, line in enumerate(lines):
            if "Add Water" in "".join(lines[max(0, i-5):min(len(lines), i+5)]) and "url_for('user_add_daily_log')" in line:
                lines[i] = line.replace("url_for('user_add_daily_log')", "url_for('user_add_water')")

        with open('flask_app/templates/user_dashboard.html', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print("Patched.")
    except Exception as e:
        print("Error", e)

if __name__ == '__main__':
    final_patch()