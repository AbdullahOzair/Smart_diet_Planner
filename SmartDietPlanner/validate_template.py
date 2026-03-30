#!/usr/bin/env python3
"""Validate Jinja2 template conditionals"""
import re

with open(r'd:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\templates\user_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
issues = []

for i, line in enumerate(lines, 1):
    # Find all if and endif in order
    parts = []
    
    # Find all {% if ... %} and {% endif %}
    for match in re.finditer(r'{%\s*(if|endif)\s*([^%]}*)?%}', line):
        keyword = match.group(1)
        condition = match.group(2) if match.group(2) else ''
        start_pos = match.start()
        parts.append((keyword, condition.strip(), start_pos))
    
    # Process in order they appear on the line
    for keyword, condition, _ in parts:
        if keyword == 'if':
            stack.append((i, condition))
            print(f"PUSH Line {i}: if {condition} - stack depth:{len(stack)}")
        elif keyword == 'endif':
            if stack:
                start_line, start_condition = stack.pop()
                print(f"POP  Line {i}: endif closes Line {start_line}: if {start_condition} - stack depth:{len(stack)}")
            else:
                issues.append(f"Line {i}: Unexpected endif with no matching if")
                print(f"ERROR Line {i}: Unexpected endif")

if stack:
    print(f"\n⚠️ UNCLOSED CONDITIONALS:")
    for line, condition in stack:
        print(f"  Line {line}: if {condition}")

if issues:
    print(f"\n❌ ISSUES:")
    for issue in issues:
        print(f"  {issue}")

if not stack and not issues:
    print("\n✅ Template structure is balanced!")

