import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

chat_widget = '''
    <!-- Admin Floating Chat Widget -->
    <div x-data="{ 
        chatOpen: false, 
        users: [], 
        activeUser: null,
        messages: [],
        newMessage: '',
        fetchUsers() {
            fetch('/admin/api/chat/users').then(r=>r.json()).then(d => this.users = d);
        },
        fetchMessages() {
            if(!this.activeUser) return;
            fetch('/api/chat?target_user_id=' + this.activeUser.id).then(r=>r.json()).then(d => {
                this.messages = d;
                setTimeout(() => {
                    const cb = document.getElementById('admin-chat-box');
                    if(cb) cb.scrollTop = cb.scrollHeight;
                }, 50);
            });
        },
        sendMessage() {
            if(!this.newMessage || !this.activeUser) return;
            let fd = new FormData();
            fd.append('message', this.newMessage);
            fd.append('target_user_id', this.activeUser.id);
            fetch('/api/chat', {method:'POST', body:fd}).then(() => {
                this.newMessage = '';
                this.fetchMessages();
            });
        }
    }" 
    x-init="setInterval(() => { if(chatOpen) fetchUsers(); if(chatOpen && activeUser) fetchMessages(); }, 3000);"
    class="fixed bottom-6 right-6 z-[200]">
        
        <!-- Chat Button -->
        <button @click="chatOpen = !chatOpen; if(chatOpen) fetchUsers();" class="w-14 h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-full shadow-2xl flex items-center justify-center transition-transform hover:scale-110">
            <i data-lucide="message-circle" class="w-7 h-7" x-show="!chatOpen"></i>
            <i data-lucide="x" class="w-7 h-7" x-show="chatOpen" style="display:none;"></i>
        </button>

        <!-- Chat Window -->
        <div x-show="chatOpen" style="display:none;" x-transition
             class="absolute bottom-20 right-0 w-[600px] h-[500px] bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden flex shadow-blue-900/20">
            
            <!-- Left Pane: Users List -->
            <div class="w-1/3 bg-slate-800 border-r border-slate-700 flex flex-col">
                <div class="p-4 border-b border-slate-700 font-bold text-white bg-slate-900">Active Chats</div>
                <div class="flex-1 overflow-y-auto">
                    <template x-for="u in users" :key="u.id">
                        <button @click="activeUser = u; fetchMessages();" 
                                :class="activeUser && activeUser.id === u.id ? 'bg-blue-600/20 border-l-4 border-blue-500' : 'hover:bg-slate-700 border-l-4 border-transparent'"
                                class="w-full text-left p-3 border-b border-slate-700 transition-colors">
                            <div class="text-sm font-bold text-white truncate" x-text="u.name"></div>
                            <div class="text-[10px] text-slate-400 truncate" x-text="u.email"></div>
                        </button>
                    </template>
                    <div x-show="users.length === 0" class="text-center text-slate-500 text-xs p-4">No active chats</div>
                </div>
            </div>

            <!-- Right Pane: Messages -->
            <div class="w-2/3 flex flex-col bg-slate-900">
                <template x-if="!activeUser">
                    <div class="flex-1 flex flex-col items-center justify-center text-slate-500">
                        <i data-lucide="message-square" class="w-12 h-12 mb-2 opacity-20"></i>
                        <p class="text-sm">Select a user to start chatting</p>
                    </div>
                </template>
                
                <template x-if="activeUser">
                    <div class="flex-1 flex flex-col h-full">
                        <!-- Header -->
                        <div class="p-4 border-b border-slate-700 bg-slate-800 flex items-center justify-between shadow-md z-10 shrink-0">
                            <div class="font-bold text-white" x-text="'Chatting with ' + activeUser.name"></div>
                        </div>
                        
                        <!-- Messages -->
                        <div id="admin-chat-box" class="flex-1 overflow-y-auto p-4 space-y-4">
                            <template x-for="m in messages" :key="m.id">
                                <div class="flex flex-col" :class="m.is_admin ? 'items-end' : 'items-start'">
                                    <div class="max-w-[80%] p-3 rounded-2xl" 
                                         :class="m.is_admin ? 'bg-blue-600 text-white rounded-tr-none shadow-md shadow-blue-500/20' : 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700'">
                                        <div class="text-[10px] font-bold mb-1 opacity-50" x-text="m.is_admin ? 'You' : activeUser.name"></div>
                                        <p class="text-sm whitespace-pre-wrap" x-text="m.message"></p>
                                    </div>
                                    <div class="text-[9px] text-slate-500 mt-1" x-text="new Date(m.created_at).toLocaleTimeString()"></div>
                                </div>
                            </template>
                            <div x-show="messages.length === 0" class="text-center text-slate-500 text-xs mt-10">No messages yet.</div>
                        </div>
                        
                        <!-- Input -->
                        <div class="p-3 border-t border-slate-700 bg-slate-800 shrink-0">
                            <form @submit.prevent="sendMessage()" class="flex gap-2">
                                <input type="text" x-model="newMessage" placeholder="Type a reply..." class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none">
                                <button type="submit" class="bg-blue-600 hover:bg-blue-500 text-white p-2 rounded-xl transition-colors"><i data-lucide="send" class="w-5 h-5"></i></button>
                            </form>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
'''

if 'Admin Floating Chat Widget' not in content:
    content = content.replace('</body>', chat_widget + '\n</body>')
    with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("CHAT WIDGET ADDED")

