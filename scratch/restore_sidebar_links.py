import re

with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I will insert them right after the Payouts link in the Main section
billing_cert_links = """
                    <a href="/feature/payouts" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-white transition-colors font-medium text-sm">
                        <i data-lucide="credit-card" class="w-4 h-4"></i> Payouts
                    </a>
                    <a href="/billing" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-white transition-colors font-medium text-sm">
                        <i data-lucide="receipt" class="w-4 h-4"></i> Billing
                    </a>
                    <a href="/passed-challenges" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-white transition-colors font-medium text-sm">
                        <i data-lucide="award" class="w-4 h-4"></i> Certificate Area
                    </a>
"""

payouts_link_regex = r'<a href="/feature/payouts"[^>]*>[\s\S]*?<i data-lucide="credit-card"[^>]*></i>\s*Payouts\s*</a>'
content = re.sub(payouts_link_regex, billing_cert_links, content)

with open('app/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

