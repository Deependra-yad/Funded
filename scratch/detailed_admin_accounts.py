with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

thead_old = '''<th class="px-4 py-4 text-right">Balance</th>
                                    <th class="px-4 py-4 text-right">Equity</th>
                                    <th class="px-4 py-4 text-center">God Controls</th>'''
thead_new = '''<th class="px-4 py-4 text-right">Balance</th>
                                    <th class="px-4 py-4 text-right">Equity</th>
                                    <th class="px-4 py-4 text-center">Days</th>
                                    <th class="px-4 py-4 text-center">Loss Limits</th>
                                    <th class="px-4 py-4 text-center">God Controls</th>'''

html = html.replace(thead_old, thead_new)

tbody_old_start = '''<td class="px-4 py-3 text-right font-mono text-emerald-400">{{ acc.current_balance|inr(2) }}</td>
                                    <td class="px-4 py-3 text-right font-mono text-blue-400">{{ acc.current_equity|inr(2) }}</td>
                                    <td class="px-4 py-3 text-center space-x-1">'''

tbody_new_start = '''<td class="px-4 py-3 text-right font-mono text-emerald-400">{{ acc.current_balance|inr(2) }}</td>
                                    <td class="px-4 py-3 text-right font-mono text-blue-400">{{ acc.current_equity|inr(2) }}</td>
                                    <td class="px-4 py-3 text-center font-bold text-slate-300">{{ acc.days_traded }} / {{ acc.min_trading_days }}</td>
                                    <td class="px-4 py-3 text-center font-mono text-xs text-rose-400">D: {{ acc.daily_loss_pct|round(1) }}% / {{ acc.max_daily_loss_pct }}%<br>M: {{ acc.total_loss_pct|round(1) }}% / {{ acc.max_total_loss_pct }}%</td>
                                    <td class="px-4 py-3 text-center space-x-1">'''

html = html.replace(tbody_old_start, tbody_new_start)

# I should also make sure to use |inr filter where $ was used in the rows
html = html.replace('{{ acc.current_balance }}', '{{ acc.current_balance|inr(2) }}')
html = html.replace('{{ acc.current_equity }}', '{{ acc.current_equity|inr(2) }}')

with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

