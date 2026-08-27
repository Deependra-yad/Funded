
    
    let currentModel = '1-Step' || '1-Step';
    let discountPercent = 0;
    const razorpayKeyId = "key";

    function selectModel(model) {
        currentModel = model;
        document.querySelectorAll('.model-btn').forEach(b => {
            b.classList.remove('border-blue-600', 'bg-blue-50/50');
            b.classList.add('border-slate-200');
        });
        const activeBtn = document.getElementById('btn-model-' + model);
        if (activeBtn) {
            activeBtn.classList.remove('border-slate-200');
            activeBtn.classList.add('border-blue-600', 'bg-blue-50/50');
        }

        let firstPkgFound = false;
        document.querySelectorAll('.package-card').forEach(card => {
            if (card.getAttribute('data-model') === model) {
                card.style.display = 'block';
                if (!firstPkgFound) {
                    const input = card.querySelector('input');
                    input.checked = true;
                    firstPkgFound = true;
                }
            } else {
                card.style.display = 'none';
            }
        });

        updateSummary();
    }

    function selectPlatform(input) {
        document.querySelectorAll('.platform-option').forEach(p => {
            p.classList.remove('border-blue-600', 'bg-blue-50/50');
            p.classList.add('border-slate-200');
        });
        input.closest('.platform-option').classList.add('border-blue-600', 'bg-blue-50/50');
    }

    function applyCoupon() {
        const val = document.getElementById('coupon-input').value.trim().toUpperCase();
        const msg = document.getElementById('coupon-msg');
        if (val === 'SAVE20' || val === 'FundedDesk20' || val === 'TRADER20') {
            discountPercent = 0.20;
            msg.innerText = '✓ Promo Code applied (20% OFF)!';
            msg.className = 'text-xs mt-1.5 font-semibold text-emerald-400 block';
        } else if (val === 'LAUNCH50' || val === 'HALFPRICE') {
            discountPercent = 0.50;
            msg.innerText = '✓ Promo Code applied (50% OFF)!';
            msg.className = 'text-xs mt-1.5 font-semibold text-emerald-400 block';
        } else if (val === 'LAUNCH10') {
            discountPercent = 0.10;
            msg.innerText = '✓ Promo Code applied (10% OFF)!';
            msg.className = 'text-xs mt-1.5 font-semibold text-emerald-400 block';
        } else {
            discountPercent = 0;
            msg.innerText = '✗ Invalid coupon code. Try SAVE20';
            msg.className = 'text-xs mt-1.5 font-semibold text-rose-400 block';
        }
        updateSummary();
    }

    function getSelectedPackage() {
        const selected = document.querySelector('input[name="package_id"]:checked');
        if (!selected) return null;
        return selected.closest('.package-card');
    }

    function updateSummary() {
        const card = getSelectedPackage();
        if (!card) return;

        document.querySelectorAll('.package-card').forEach(c => {
            c.classList.remove('border-blue-600', 'bg-blue-50/40');
            c.classList.add('border-slate-200');
        });
        card.classList.add('border-blue-600', 'bg-blue-50/40');

        const basePrice = parseFloat(card.getAttribute('data-price'));
        const size = parseFloat(card.getAttribute('data-size'));
        const model = card.getAttribute('data-model');

        document.getElementById('summary-title').innerText = `₹${(size).toLocaleString('en-IN')} ${model} Evaluation`;

        let finalPrice = basePrice;
        if (discountPercent > 0) {
            const discAmt = basePrice * discountPercent;
            finalPrice = basePrice - discAmt;
            document.getElementById('original-price-display').innerText = `₹${basePrice.toLocaleString('en-IN')}`;
        } else {
            document.getElementById('original-price-display').innerText = '';
        }

        document.getElementById('final-price-display').innerText = `₹${finalPrice.toLocaleString('en-IN')}`;
        document.getElementById('inr-price-display').innerText = `Native INR Checkout`;
    }

    // Official Razorpay Gateway Integration
    async function startRazorpayPayment() {
        const card = getSelectedPackage();
        if (!card) return alert('Please select a challenge package');

        const packageId = card.getAttribute('data-id');
        const couponCode = document.getElementById('coupon-input').value.trim();
        const platformInput = document.querySelector('input[name="platform"]:checked');
        const platform = platformInput ? platformInput.value : 'WebTrader';

        const btn = document.getElementById('pay-btn');
        const btnText = document.getElementById('pay-btn-text');
        btnText.innerText = 'Creating Razorpay Order...';
        btn.disabled = true;

        try {
            // 1. Create Razorpay order on server
            const formData = new FormData();
            formData.append('package_id', packageId);
            formData.append('coupon_code', couponCode);

            const res = await fetch('/api/payment/create-order', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (!data.success) {
                alert('Order Error: ' + (data.error || 'Failed to create payment order'));
                btnText.innerText = 'Pay with Razorpay';
                btn.disabled = false;
                return;
            }

            // 2. Launch Razorpay Checkout Modal or bypass if mock
            if (data.order_id.startsWith('order_mock_')) {
                btnText.innerText = 'Verifying Mock Payment...';
                const verifyForm = new FormData();
                verifyForm.append('package_id', packageId);
                verifyForm.append('platform', platform);
                verifyForm.append('coupon_code', couponCode);
                verifyForm.append('razorpay_order_id', data.order_id);
                verifyForm.append('razorpay_payment_id', 'pay_mock_' + Math.random().toString(36).substr(2, 9));
                verifyForm.append('razorpay_signature', 'mock_signature_123');

                const verifyRes = await fetch('/api/payment/verify', {
                    method: 'POST',
                    body: verifyForm
                });
                const verifyData = await verifyRes.json();
                if (verifyData.success) {
                    window.location.href = verifyData.redirect_url;
                } else {
                    alert('Verification Error: ' + (verifyData.error || 'Payment verification failed'));
                    btnText.innerText = 'Pay with Razorpay';
                    btn.disabled = false;
                }
                return;
            }

            const options = {
                "key": data.key_id,
                "amount": data.amount_paise,
                "currency": data.currency,
                "name": "FundedDesk",
                "description": data.package_name + " Evaluation",
                "order_id": data.order_id,
                "prefill": {
                    "name": data.user_name,
                    "email": data.user_email
                },
                "theme": {
                    "color": "#10B981"
                },
                "handler": async function (response) {
                    btnText.innerText = 'Verifying Payment...';
                    // 3. Verify Razorpay Payment Signature
                    const verifyForm = new FormData();
                    verifyForm.append('package_id', packageId);
                    verifyForm.append('platform', platform);
                    verifyForm.append('coupon_code', couponCode);
                    verifyForm.append('razorpay_order_id', response.razorpay_order_id);
                    verifyForm.append('razorpay_payment_id', response.razorpay_payment_id);
                    verifyForm.append('razorpay_signature', response.razorpay_signature);

                    const verifyRes = await fetch('/api/payment/verify', {
                        method: 'POST',
                        body: verifyForm
                    });
                    const verifyData = await verifyRes.json();

                    if (verifyData.success) {
                        window.location.href = verifyData.redirect_url;
                    } else {
                        alert('Verification Error: ' + (verifyData.error || 'Payment verification failed'));
                        btnText.innerText = 'Pay with Razorpay';
                        btn.disabled = false;
                    }
                },
                "modal": {
                    "ondismiss": function () {
                        btnText.innerText = 'Pay with Razorpay';
                        btn.disabled = false;
                    }
                }
            };

            
            if (typeof window.Razorpay === 'undefined') {
                alert('Razorpay SDK failed to load. Please disable your adblocker or check your internet connection.');
                btnText.innerText = 'Pay with Razorpay';
                btn.disabled = false;
                return;
            }
            const rzp = new window.Razorpay(options);
            rzp.on('payment.failed', function (response) {
                alert('Payment Failed: ' + response.error.description);
                btnText.innerText = 'Pay with Razorpay';
                btn.disabled = false;
            });
            rzp.open();

        } catch (err) {
            console.error('Payment checkout error:', err);
            alert('Failed to initiate Razorpay checkout.');
            btnText.innerText = 'Pay with Razorpay';
            btn.disabled = false;
        }
    }

    // Initialize
    selectModel(currentModel);
