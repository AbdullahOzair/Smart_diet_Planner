import sys
for line in open('check_pages2.txt'):
    if any(x in line for x in ['ERROR', 'Exception', 'status:', 'Traceback']):
        print(line.strip())
