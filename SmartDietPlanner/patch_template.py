import codecs
def fix_template():
    try:
        with open('flask_app/templates/user_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()

        import re
        
        # We need to find where the `url_for('user_add_daily_log')` was placed instead of `url_for('user_add_water')`
        # and where `url_for('user_profile')` was placed instead of `url_for('user_progress')`.
        # However, we don't want to break the ACTUALLY correct links. 
        # So we can just find them based on the surrounding UI text.
        
        # Look for the water card:
        # It had <a href="{{ url_for('user_add_water') }}" style="display: block; ...">
        # Right now it has <a href="{{ url_for('user_add_daily_log') }}" style="display: block; text-decoration: none; transition: all 0.3s ease;">
        # ... inside a card with "Water Intake" or similar.
        
        lines = content.split('\n')
        
        # We'll re-read and replace line by line based on context.
        for i in range(len(lines)):
            # Fix Add Water
            if "url_for('user_add_daily_log')" in lines[i] and 'water' in lines[max(0, i-20): min(len(lines), i+20)] and "Water Intake" in ''.join(lines[max(0, i-10): min(len(lines), i+10)]):
                if '<a href="{{ url_for(\'user_add_daily_log\') }}" style="display: block;' in lines[i]:
                    lines[i] = lines[i].replace("url_for('user_add_daily_log')", "url_for('user_add_water')")

            # Fix Progress
            if "url_for('user_profile')" in lines[i] and "View Progress" in ''.join(lines[max(0, i-5): min(len(lines), i+5)]):
                lines[i] = lines[i].replace("url_for('user_profile')", "url_for('user_progress')")

        with open('flask_app/templates/user_dashboard.html', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        print("Patched template.")
            
    except Exception as e:
        print("Error", e)

if __name__ == '__main__':
    fix_template()