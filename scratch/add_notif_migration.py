with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = '''
    try:
        db.execute(text("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, message VARCHAR(500), type VARCHAR(50) DEFAULT 'info', is_read BOOLEAN DEFAULT 0, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"))
        db.commit()
    except Exception as e:
        db.rollback()
        print("Notification migration failed:", e)
'''

import re
content = re.sub(r'(db\.execute\(text\("ALTER TABLE users ADD COLUMN plain_password VARCHAR\(255\)"\)\)\n\s*db\.commit\(\))', r'\1' + '\n' + migration_code, content)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

