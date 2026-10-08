// This JS handles admin-dashboard, admin-users, admin-orders
document.addEventListener('DOMContentLoaded', () => {
    const user = ApiClient.getUser();
    if (!user || user.role !== 'admin') {
        window.location.href = '/login.html';
        return;
    }
    
    if (document.getElementById('adminDashboardStats')) loadAdminDashboard();
    if (document.getElementById('adminUsersTable')) loadAdminUsers();
    if (document.getElementById('adminOrdersTable')) loadAdminOrders();
});

async function loadAdminDashboard() {
    try {
        const stats = await ApiClient.get('/admin/dashboard').catch(()=>({ users:0, orders:0, revenue:0 }));
        document.getElementById('totalUsers').textContent = stats.users || 0;
        document.getElementById('totalOrders').textContent = stats.orders || 0;
        document.getElementById('totalRevenue').textContent = `₹${stats.revenue || 0}`;
    } catch(e) { console.error(e); }
}

async function loadAdminUsers() {
    try {
        const users = await ApiClient.get('/admin/users').catch(()=>[]);
        const tbody = document.getElementById('adminUsersTable');
        tbody.innerHTML = '';
        users.forEach(u => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${u.name}</td>
                <td>${u.email}</td>
                <td><span class="badge badge-info">${u.role}</span></td>
                <td>
                    <select class="form-control form-control-sm" onchange="updateUserRole(${u.id}, this.value)" ${u.id === ApiClient.getUser().id ? 'disabled' : ''}>
                        <option value="customer" ${u.role==='customer'?'selected':''}>Customer</option>
                        <option value="restaurant" ${u.role==='restaurant'?'selected':''}>Restaurant</option>
                        <option value="admin" ${u.role==='admin'?'selected':''}>Admin</option>
                    </select>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) { console.error(e); }
}

async function updateUserRole(id, role) {
    try {
        await ApiClient.put(`/admin/users/${id}/role`, { role });
        showToast('Role updated');
    } catch(e) { showToast('Failed to update role', 'error'); }
}

async function loadAdminOrders() {
    try {
        const orders = await ApiClient.get('/admin/orders').catch(()=>[]);
        const tbody = document.getElementById('adminOrdersTable');
        tbody.innerHTML = '';
        orders.forEach(o => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#ORD-${o.id.toString().padStart(5,'0')}</td>
                <td>${new Date(o.created_at).toLocaleDateString()}</td>
                <td>₹${o.total_amount}</td>
                <td><span class="badge badge-status status-${o.status}">${o.status.replace('_',' ').toUpperCase()}</span></td>
                <td><a href="/order-detail.html?id=${o.id}" class="btn btn-sm btn-outline-primary">View</a></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) { console.error(e); }
}
