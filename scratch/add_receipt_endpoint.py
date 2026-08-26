with open('app/routers/store.py', 'r', encoding='utf-8') as f:
    content = f.read()

endpoint = '''
@router.get("/api/orders/{order_id}/receipt", response_class=HTMLResponse)
async def view_receipt(request: Request, order_id: int, db: Session = Depends(get_db), user: User = Depends(require_auth)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return templates.TemplateResponse(
        request=request,
        name="receipt.html",
        context={"order": order, "user": user}
    )
'''

content += "\n" + endpoint

with open('app/routers/store.py', 'w', encoding='utf-8') as f:
    f.write(content)

