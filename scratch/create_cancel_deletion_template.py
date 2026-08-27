html = """{% extends "base.html" %}

{% block title %}Account Deletion Pending - {{ app_name }}{% endblock %}

{% block content %}
<div class="min-h-[80vh] flex items-center justify-center">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl border border-rose-100 p-8 text-center">
        <div class="w-16 h-16 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <i data-lucide="alert-triangle" class="w-8 h-8"></i>
        </div>
        <h2 class="text-2xl font-black text-slate-900 mb-2">Account Deletion Pending</h2>
        <p class="text-slate-500 mb-6">
            You requested to permanently delete this account on <strong>{{ deletion_date }}</strong>. 
            Your account is scheduled for automatic deletion 15 days after that date.
        </p>
        
        <div class="bg-amber-50 border border-amber-200 p-4 rounded-xl text-left mb-6">
            <h4 class="font-bold text-amber-800 text-sm mb-1">Want to recover your account?</h4>
            <p class="text-amber-700 text-xs">If you made a mistake, you can cancel the deletion process right now and instantly regain access to your dashboard.</p>
        </div>
        
        <form action="/profile/cancel-deletion" method="POST" class="space-y-4">
            <input type="hidden" name="email" value="{{ email }}">
            <div>
                <textarea name="reason" required placeholder="Reason for keeping account (e.g., Accidentally clicked, changed my mind)..." class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none text-sm transition-all" rows="3"></textarea>
            </div>
            <div class="flex flex-col gap-3">
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-4 rounded-xl transition-colors shadow-lg shadow-emerald-600/20">
                    Cancel Deletion & Login
                </button>
                <a href="/login" class="text-slate-500 hover:text-slate-700 text-sm font-medium">No, return to login</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""

with open('app/templates/cancel_deletion.html', 'w', encoding='utf-8') as f:
    f.write(html)

