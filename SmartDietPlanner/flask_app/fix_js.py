import re

with open('templates/user_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the broken addWaterGlass function that ends with "// Update water glass display dynamically without reload\n      }"
# and remove it entirely.
pattern = r"function addWaterGlass\(\) \{\s*console\.log\('.*?addWaterGlass\(\) called'\);.*?// Update water glass display dynamically without reload\s*\}"

res, count = re.subn(pattern, '', text, flags=re.DOTALL)
print('Removed broken function occurrences:', count)

# We also need to see if there is any other syntax error using 'node -c'
with open('templates/user_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(res)
