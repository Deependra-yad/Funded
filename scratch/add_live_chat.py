import re

with open('app/routers/features.py', 'r', encoding='utf-8') as f:
    content = f.read()

chat_endpoints = """
from fastapi import Form
from fastapi.responses import JSONResponse
from app.models import ChatMessage

@router.post("/api/chat")
async def send_chat(request: Request, message: str = Form(...), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    if not message.strip():
        return JSONResponse({"success": False})
    msg = ChatMessage(user_id=user.id, is_admin=user.is_super_admin, message=message.strip())
    db.add(msg)
    db.commit()
    return JSONResponse({"success": True})

@router.get("/api/chat")
async def get_chat(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    # If admin, fetch all chats. If user, fetch only their own chats.
    if user.is_super_admin:
        messages = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(100).all()
    else:
        messages = db.query(ChatMessage).filter(ChatMessage.user_id == user.id).order_by(ChatMessage.created_at.desc()).limit(50).all()
    
    return JSONResponse([
        {"id": m.id, "user_id": m.user_id, "is_admin": m.is_admin, "message": m.message, "created_at": m.created_at.isoformat()}
        for m in reversed(messages)
    ])
"""

support_widget = """
        <div class="h-[500px] flex flex-col" x-data="{ messages: [], newMessage: '', fetchChat() { fetch('/api/chat').then(r=>r.json()).then(d=> { this.messages = d; setTimeout(()=>$refs.chatbox.scrollTop = $refs.chatbox.scrollHeight, 100); }); } }" x-init="fetchChat(); setInterval(()=>fetchChat(), 3000);">
            <div class="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 flex justify-between items-center">
                <div class="font-bold flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div> Live Support</div>
                <div class="text-xs text-slate-500">Average response: 3 mins</div>
            </div>
            <div x-ref="chatbox" class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50 dark:bg-slate-900/50">
                <template x-for="m in messages" :key="m.id">
                    <div class="flex flex-col" :class="m.is_admin ? 'items-start' : 'items-end'">
                        <div class="max-w-[80%] p-3 rounded-2xl" :class="m.is_admin ? 'bg-white dark:bg-slate-800 text-slate-800 dark:text-white rounded-tl-none border border-slate-200 dark:border-slate-700' : 'bg-blue-600 text-white rounded-tr-none shadow-md shadow-blue-500/20'">
                            <div class="text-xs font-bold mb-1 opacity-50" x-text="m.is_admin ? 'Support Agent' : 'You'"></div>
                            <p class="text-sm" x-text="m.message"></p>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-1" x-text="new Date(m.created_at).toLocaleTimeString()"></div>
                    </div>
                </template>
                <div x-show="messages.length === 0" class="text-center text-slate-500 text-sm mt-10">Send a message to start chatting with support.</div>
            </div>
            <div class="p-4 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
                <form @submit.prevent="if(newMessage){ let fd = new FormData(); fd.append('message', newMessage); fetch('/api/chat', {method:'POST', body:fd}).then(()=>{ newMessage=''; fetchChat(); }); }">
                    <div class="flex gap-2">
                        <input type="text" x-model="newMessage" placeholder="Type your message..." class="flex-1 bg-slate-100 dark:bg-slate-800 border-none rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none text-slate-800 dark:text-white">
                        <button type="submit" class="bg-blue-600 text-white p-2 rounded-xl hover:bg-blue-500 transition-colors"><i data-lucide="send" class="w-5 h-5"></i></button>
                    </div>
                </form>
            </div>
        </div>
"""

# Inject the endpoints
if '@router.post("/api/chat")' not in content:
    content = content.replace('router = APIRouter()', 'router = APIRouter()\n' + chat_endpoints)

# Inject the support widget
support_regex = r'"support": \{.*?\}\s*\}\s*\},'
# We have to be careful with regex replacement of multiline dictionary.
# Let's just use string replace.
content = re.sub(r'("support": \{.*?)"widget":.*?</div>\'\'\'', r'\1"widget": \'\'\'' + support_widget + r'\'\'\'', content, flags=re.DOTALL)

with open('app/routers/features.py', 'w', encoding='utf-8') as f:
    f.write(content)

