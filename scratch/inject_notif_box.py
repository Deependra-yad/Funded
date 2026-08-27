with open('app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

notification_box = """
    <!-- Notifications Box -->
    <div class="bg-white dark:bg-darkpanel rounded-2xl border border-slate-200 dark:border-darkborder p-6 shadow-sm mb-6 mt-6" x-data="{ notifications: [] }" x-init="
        fetch('/api/notifications').then(r => r.json()).then(d => notifications = d);
    ">
        <h3 class="text-lg font-black text-slate-800 dark:text-white mb-4 flex items-center gap-2">
            <i data-lucide="bell" class="w-5 h-5 text-indigo-500"></i> Platform Notifications
        </h3>
        <div class="space-y-3">
            <template x-for="n in notifications" :key="n.id">
                <div class="flex items-start gap-3 bg-slate-50 dark:bg-darkbg p-3 rounded-xl border border-slate-100 dark:border-darkborder shadow-sm relative group" :id="'notif-'+n.id">
                    <div class="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0">
                        <i data-lucide="info" class="w-4 h-4"></i>
                    </div>
                    <div class="flex-1 pr-6">
                        <p class="text-sm text-slate-700 dark:text-slate-300" x-text="n.message"></p>
                        <span class="text-[10px] text-slate-400 font-medium" x-text="new Date(n.created_at).toLocaleString()"></span>
                    </div>
                    <button @click="fetch('/api/notifications/'+n.id+'/dismiss', {method: 'POST'}).then(() => { notifications = notifications.filter(x => x.id !== n.id) })" class="absolute top-3 right-3 text-slate-400 hover:text-slate-600 dark:hover:text-white bg-white dark:bg-darkpanel rounded-md p-1 shadow-sm opacity-0 group-hover:opacity-100 transition-opacity">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
            </template>
            <div x-show="notifications.length === 0" class="text-center text-slate-500 text-sm py-4">
                No new notifications.
            </div>
        </div>
    </div>
"""

if 'Platform Notifications' not in content:
    content = content.replace('    <!-- Trading Statistics Grid -->', notification_box + '\n    <!-- Trading Statistics Grid -->')
    with open('app/templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

