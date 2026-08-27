with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

migration = """
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN deletion_requested_at TIMESTAMP NULL"))
        db.commit()
    except Exception:
        db.rollback()
"""
if 'deletion_requested_at' not in content:
    content = content.replace('def seed_database():', 'def seed_database():' + migration)
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
