import re

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

cleanup_logic = """
    # Auto-delete users pending deletion for 15+ days
    try:
        from datetime import datetime, timedelta
        db = SessionLocal()
        cutoff_date = datetime.utcnow() - timedelta(days=15)
        users_to_delete = db.query(User).filter(User.deletion_requested == True, User.deletion_requested_at <= cutoff_date).all()
        for u in users_to_delete:
            db.delete(u)
        db.commit()
    except Exception as e:
        print("Auto-delete failed:", e)
    finally:
        db.close()
"""

if 'users_to_delete' not in content:
    content = content.replace('app = FastAPI(', cleanup_logic + '\napp = FastAPI(')
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(content)

