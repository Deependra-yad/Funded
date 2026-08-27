import re

with open('app/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

chat_model = """
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_admin = Column(Boolean, default=False)
    message = Column(String(1000))
    created_at = Column(DateTime, default=utc_now)
    
    user = relationship("User")
"""

if 'class ChatMessage' not in content:
    content = content + "\n" + chat_model
    with open('app/models.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
with open('app/main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

chat_migration = """
    try:
        db.execute(text("CREATE TABLE IF NOT EXISTS chat_messages (id SERIAL PRIMARY KEY, user_id INTEGER, is_admin BOOLEAN DEFAULT FALSE, message TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
        db.commit()
    except Exception:
        db.rollback()
        try:
            db.execute(text("CREATE TABLE IF NOT EXISTS chat_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, is_admin BOOLEAN DEFAULT 0, message TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"))
            db.commit()
        except Exception:
            db.rollback()
"""

if 'CREATE TABLE IF NOT EXISTS chat_messages' not in main_content:
    main_content = main_content.replace('    try:\n        db.execute(text("ALTER TABLE users ADD COLUMN deletion_requested_at', chat_migration + '\n    try:\n        db.execute(text("ALTER TABLE users ADD COLUMN deletion_requested_at')
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)

