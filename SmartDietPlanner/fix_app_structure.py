import re

with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure if __name__ is at the end.
if "if __name__ == '__main__':" in text:
    parts = text.split("if __name__ == '__main__':")
    main_block = "if __name__ == '__main__':" + parts[1]
    
    # Lines before if __name__
    before = parts[0]
    
    lines = main_block.split('\n')
    run_lines = []
    other_lines = []
    
    in_run_block = True
    for line in lines:
        if in_run_block and (line.strip() == '' or 'app.run(' in line or "if __name__ == '__main__':" in line):
            run_lines.append(line)
        else:
            in_run_block = False
            if line.strip() != "":  # Optional to strip empty lines
                other_lines.append(line)
            
    # Now rebuild the file
    new_text = before + '\n' + '\n'.join(other_lines) + '\n\n' + '\n'.join(run_lines) + '\n'
    
    with open('flask_app/app.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Reordered app.py successfully.")
else:
    print("No main block found.")
