with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = '''
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN plain_password VARCHAR(255)"))
        db.commit()
    except Exception as e:
        db.rollback()
        print("Migration skipped or failed:", e)
    finally:
        db.close()
    
    asyncio.create_task(daily_equity_reset_worker())
'''

import re
content = re.sub(r'@app\.on_event\("startup"\)\nasync def startup_event\(\):\n\s*asyncio\.create_task\(daily_equity_reset_worker\(\)\)', migration_code, content)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

