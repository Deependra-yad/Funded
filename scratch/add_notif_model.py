with open('app/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

model_code = '''
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(500))
    type = Column(String(50), default="info")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
'''

if 'class Notification' not in content:
    content += '\n' + model_code
    with open('app/models.py', 'w', encoding='utf-8') as f:
        f.write(content)

