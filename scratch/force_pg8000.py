with open('app/config.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('postgresql+psycopg://', 'postgresql+pg8000://')

with open('app/config.py', 'w', encoding='utf-8') as f:
    f.write(content)
