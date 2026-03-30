import re

with open('app.py', encoding='utf-8') as f:
    text = f.read()

text = text.replace('FETCH FIRST 10 ROWS ONLY', 'LIMIT 10')
text = text.replace('FETCH FIRST 5 ROWS ONLY', 'LIMIT 5')
text = text.replace('FETCH FIRST 7 ROWS ONLY', 'LIMIT 7')

text = text.replace('TRUNC(SYSDATE)', 'CURRENT_DATE')
text = text.replace('TRUNC(log_date)', 'DATE(log_date)')
text = text.replace('TRUNC(log_date)=TO_DATE(%(d)s, \'YYYY-MM-DD\')', 'DATE(log_date)=%(d)s::DATE')

text = re.sub(r"TO_DATE\((.*?),\s*'YYYY-MM-DD'\)", r"\1::DATE", text)

def replace_bindings(match):
    s = match.group(0)
    # avoid replacing things in dicts or URLs
    # only replace if it's inside a SQL string and preceded by space, =(, etc.
    s_new = re.sub(r'(?<=[=\s(,])(:)([a-zA-Z_]\w*)', r'%(\2)s', s)
    return s_new

text = re.sub(r'\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\'|\"[^\"]*?\"|\'[^\']*?\'', replace_bindings, text)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated app.py")
