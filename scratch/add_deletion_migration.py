with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = '''
        try:
            db.execute(text("ALTER TABLE users ADD COLUMN deletion_requested BOOLEAN DEFAULT 0"))
            db.commit()
        except Exception:
            db.rollback()
'''

import re
content = re.sub(r'(db\.execute\(text\("ALTER TABLE users ADD COLUMN plain_password VARCHAR\(255\)"\)\)\n\s*db\.commit\(\))', r'\1' + migration_code, content)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
