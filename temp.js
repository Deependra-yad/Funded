
    lucide.createIcons();

    function showToast(msg, type='success') {
        const container = document.getElementById('toast-container');
        const t = document.createElement('div');
        t.className = `px-4 py-3 rounded-lg text-sm font-bold text-white shadow-lg transform transition-all duration-300 translate-x-full ${type==='success' ? 'bg-emerald-600' : 'bg-rose-600'}`;
        t.innerText = msg;
        container.appendChild(t);
        
        setTimeout(() => { t.style.transform = 'translateX(0)'; }, 10);
        setTimeout(() => { 
            t.style.transform = 'translateX(100%)'; 
            t.style.opacity = '0';
            setTimeout(() => t.remove(), 300);
        }, 3000);
    }

    function switchTab(tab) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('nav button').forEach(el => {
            el.classList.remove('bg-slate-800/50', 'text-white');
            el.classList.add('text-slate-400');
        });
        
        document.getElementById('tab-' + tab).classList.add('active');
        const navBtn = document.getElementById('nav-' + tab);
        navBtn.classList.remove('text-slate-400');
        navBtn.classList.add('bg-slate-800/50', 'text-white');
        
        const titles = {
            'overview': 'Platform Overview',
            'users': 'User Management',
            'accounts': 'Trading Accounts',
            'trades': 'Live Market Positions',
            'rules': 'Prop Firm Rules Engine',
            'payouts': 'Payout Requests',
            'ops': 'Market Operations & Risk',
            'settings': 'Platform Settings'
        };
        document.getElementById('page-title').innerText = titles[tab];
    }
    
    function openEditUserModal(id, name, email, password) {
        document.getElementById('eu-id').value = id;
        document.getElementById('eu-name').value = name;
        document.getElementById('eu-email').value = email;
        document.getElementById('eu-pass').value = password || '';
        document.getElementById('edit-user-modal').classList.remove('hidden');
    }

    function openNotifyModal(id, name) {
        document.getElementById('nu-id').value = id;
        document.getElementById('nu-name').innerText = name;
        document.getElementById('nu-msg').value = '';
        document.getElementById('notify-user-modal').classList.remove('hidden');
    }

    function closeModal(id) {
        document.getElementById(id).classList.add('hidden');
    }

    async function submitEditUser(e) {
        e.preventDefault();
        const form = e.target;
        const data = new FormData(form);
        try {
            const res = await fetch('/admin/api/user/update', { method: 'POST', body: data });
            const json = await res.json();
            if (json.success) {
                showToast(json.message, 'success');
                closeModal('edit-user-modal');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast(json.error, 'error');
            }
        } catch (err) {
            showToast('Error updating user', 'error');
        }
    }

    async function submitNotifyUser(e) {
        e.preventDefault();
        const form = e.target;
        const data = new FormData(form);
        try {
            const res = await fetch('/admin/api/user/notify', { method: 'POST', body: data });
            const json = await res.json();
            if (json.success) {
                showToast(json.message, 'success');
                closeModal('notify-user-modal');
            } else {
                showToast(json.error, 'error');
            }
        } catch (err) {
            showToast('Error sending notification', 'error');
        }
    }

    async function adminAction(entity, id, action) {
        if(!confirm(`EXECUTE: '${{action}}' on ${{entity}} #${{id}}?`)) return;
        
        const formData = new FormData();
        formData.append('entity', entity);
        formData.append('id', id);
        formData.append('action', action);

        try {
            const res = await fetch('/admin/api/action', {
                method: 'POST',
                body: formData
            });
            const json = await res.json();
            if(json.success) {
                showToast(json.message, 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showToast(json.error, 'error');
            }
        } catch(e) {
            showToast('Execution failed.', 'error');
        }
    }

    async function submitAdminSettings(e) {
        e.preventDefault();
        const form = e.target;
        const data = new FormData(form);
        try {
            const res = await fetch('/admin/api/settings', { method: 'POST', body: data });
            const json = await res.json();
            if (json.success) {
                showToast(json.message, 'success');
            } else {
                showToast(json.error, 'error');
            }
        } catch (err) {
            showToast('Error updating settings', 'error');
        }
    }
