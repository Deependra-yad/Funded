import os
import glob

# Convert Python files
for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py') or file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace('USD', 'INR').replace('$', '₹').replace('amount_usd', 'amount_inr').replace('final_price_usd', 'final_price_inr')
            if 'buy_challenge.html' in filepath:
                # Also revert the weird symbol that might be corrupting
                new_content = new_content.replace('%^ ', '')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")

