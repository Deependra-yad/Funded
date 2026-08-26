with open('app/routers/dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

endpoint = '''
@router.post("/api/payout/request")
async def request_payout(account_id: int = Form(...), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id, TradingAccount.user_id == user.id).first()
    if not account or account.phase != "Funded":
        raise HTTPException(status_code=400, detail="Invalid account for payout")
    
    if account.current_profit <= 0:
        raise HTTPException(status_code=400, detail="No profits available for payout")
        
    # Mock payout deduction
    payout_amt = account.current_profit
    account.current_balance -= payout_amt
    account.current_equity -= payout_amt
    db.commit()
    
    return RedirectResponse(url="/dashboard?payout_success=1", status_code=303)
'''

content += "\n" + endpoint

with open('app/routers/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

