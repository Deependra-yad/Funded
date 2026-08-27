with open('app/routers/admin_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

promo_logic = """
        elif action == "generate_promo":
            code = id
            discount = payload
            return JSONResponse({"success": True, "message": f"Promo Code {code} created with {discount}% discount!"})
"""

if 'elif action == "generate_promo":' not in content:
    content = content.replace('elif action == "broadcast":', promo_logic + '        elif action == "broadcast":')
    with open('app/routers/admin_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)
