with open('app/templates/profile.html', 'r', encoding='utf-8') as f:
    html = f.read()

delete_section = '''
        <!-- Danger Zone -->
        <div class="bg-white rounded-2xl border border-rose-200 overflow-hidden shadow-sm mt-8">
            <div class="px-6 py-4 border-b border-rose-100 bg-rose-50 flex items-center gap-2">
                <i data-lucide="alert-triangle" class="w-5 h-5 text-rose-600"></i>
                <h2 class="font-extrabold text-lg text-rose-900 tracking-tight">Danger Zone</h2>
            </div>
            <div class="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h3 class="font-bold text-slate-900 text-sm">Permanent Account Deletion</h3>
                    <p class="text-xs text-slate-500 mt-1">Once you request deletion, an admin will permanently wipe your account, trading data, and active challenges. This action cannot be undone.</p>
                </div>
                {% if user.deletion_requested %}
                <div class="bg-amber-100 text-amber-800 px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 shrink-0">
                    <i data-lucide="clock" class="w-4 h-4"></i> Deletion Pending Admin Approval
                </div>
                {% else %}
                <form action="/profile/delete-request" method="POST" onsubmit="return confirm('Are you absolutely sure you want to permanently delete your account?');">
                    <button type="submit" class="bg-rose-100 hover:bg-rose-600 hover:text-white text-rose-700 font-bold py-2.5 px-6 rounded-xl text-xs transition-colors shrink-0">
                        Request Account Deletion
                    </button>
                </form>
                {% endif %}
            </div>
        </div>
'''

html = html.replace('</div>\n{% endblock %}', delete_section + '\n</div>\n{% endblock %}')

with open('app/templates/profile.html', 'w', encoding='utf-8') as f:
    f.write(html)

