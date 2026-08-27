import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

chat_widget = """
    <!-- Admin Live Support Chat -->
    <div class="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl mb-8 mt-12 max-w-7xl mx-auto flex flex-col h-[500px]" x-data="{ messages: [], newMessage: '', fetchChat() { fetch('/api/chat').then(r=>r.json()).then(d=> { this.messages = d; setTimeout(()=>$refs.adminchatbox.scrollTop = $refs.adminchatbox.scrollHeight, 100); }); } }" x-init="fetchChat(); setInterval(()=>fetchChat(), 3000);">
        <div class="p-6 border-b border-slate-800 bg-slate-800/50 flex justify-between items-center">
            <h3 class="text-xl font-bold text-white flex items-center gap-2">
                <i data-lucide="message-square" class="w-6 h-6 text-blue-500"></i> Global Live Support Chat
            </h3>
            <span class="text-xs text-slate-400">Showing all user messages</span>
        </div>
        
        <div x-ref="adminchatbox" class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-800/20">
            <template x-for="m in messages" :key="m.id">
                <div class="flex flex-col" :class="m.is_admin ? 'items-end' : 'items-start'">
                    <div class="max-w-[80%] p-3 rounded-2xl" :class="m.is_admin ? 'bg-blue-600 text-white rounded-tr-none shadow-md shadow-blue-500/20' : 'bg-slate-800 text-white rounded-tl-none border border-slate-700'">
                        <div class="text-xs font-bold mb-1 opacity-50" x-text="m.is_admin ? 'You (Admin)' : ('User ID: ' + m.user_id)"></div>
                        <p class="text-sm" x-text="m.message"></p>
                    </div>
                    <div class="text-[10px] text-slate-500 mt-1" x-text="new Date(m.created_at).toLocaleTimeString()"></div>
                </div>
            </template>
            <div x-show="messages.length === 0" class="text-center text-slate-500 text-sm mt-10">No chat messages yet.</div>
        </div>
        
        <div class="p-4 border-t border-slate-800 bg-slate-900">
            <form @submit.prevent="if(newMessage){ let fd = new FormData(); fd.append('message', newMessage); fetch('/api/chat', {method:'POST', body:fd}).then(()=>{ newMessage=''; fetchChat(); }); }">
                <div class="flex gap-2">
                    <input type="text" x-model="newMessage" placeholder="Reply as Admin..." class="flex-1 bg-slate-800 border-none rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none text-white">
                    <button type="submit" class="bg-blue-600 text-white p-2 rounded-xl hover:bg-blue-500 transition-colors"><i data-lucide="send" class="w-5 h-5"></i></button>
                </div>
            </form>
        </div>
    </div>
"""

if 'Global Live Support Chat' not in content:
    content = content.replace('<!-- Modals -->', chat_widget + '\n<!-- Modals -->')
    with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
