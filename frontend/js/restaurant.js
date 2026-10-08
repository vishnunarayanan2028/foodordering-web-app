document.addEventListener('DOMContentLoaded', () => {
    const user = ApiClient.getUser();
    if (!user || user.role !== 'restaurant') {
        window.location.href = '/login.html';
        return;
    }
    
    if (document.getElementById('restDashboardStats')) loadRestDashboard();
    if (document.getElementById('restOrdersTable')) loadRestOrders();
    if (document.getElementById('restFoodsTable')) loadRestFoods();
    if (document.getElementById('restCategoriesList')) loadRestCategories();
});

async function loadRestDashboard() {
    try {
        const stats = await ApiClient.get('/restaurant/dashboard').catch(()=>({ orders:0, revenue:0, pending:0 }));
        document.getElementById('totalOrders').textContent = stats.orders || 0;
        document.getElementById('totalRevenue').textContent = `₹${stats.revenue || 0}`;
        document.getElementById('pendingOrders').textContent = stats.pending || 0;
    } catch(e) { console.error(e); }
}

async function loadRestOrders() {
    try {
        const orders = await ApiClient.get('/restaurant/orders').catch(()=>[]);
        const tbody = document.getElementById('restOrdersTable');
        tbody.innerHTML = '';
        orders.forEach(o => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#ORD-${o.id.toString().padStart(5,'0')}</td>
                <td>${new Date(o.created_at).toLocaleDateString()}</td>
                <td>₹${o.total_amount}</td>
                <td>
                    <select class="form-control form-control-sm" onchange="updateOrderStatus(${o.id}, this.value)">
                        <option value="placed" ${o.status==='placed'?'selected':''}>Placed</option>
                        <option value="confirmed" ${o.status==='confirmed'?'selected':''}>Confirmed</option>
                        <option value="preparing" ${o.status==='preparing'?'selected':''}>Preparing</option>
                        <option value="ready" ${o.status==='ready'?'selected':''}>Ready</option>
                        <option value="out_for_delivery" ${o.status==='out_for_delivery'?'selected':''}>Out for Delivery</option>
                        <option value="delivered" ${o.status==='delivered'?'selected':''}>Delivered</option>
                        <option value="cancelled" ${o.status==='cancelled'?'selected':''}>Cancelled</option>
                    </select>
                </td>
                <td><a href="/order-detail.html?id=${o.id}" class="btn btn-sm btn-outline-primary">View</a></td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) { console.error(e); }
}

async function updateOrderStatus(id, status) {
    try {
        await ApiClient.put(`/restaurant/orders/${id}/status`, { status });
        showToast('Status updated');
    } catch(e) { showToast('Failed to update status', 'error'); }
}

// Stubs for Menu Management
async function loadRestFoods() {
    try {
        const foods = await ApiClient.get('/foods').catch(()=>[]);
        const tbody = document.getElementById('restFoodsTable');
        tbody.innerHTML = '';
        foods.forEach(f => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><img src="${f.image_url||'#'}" style="width:40px;height:40px;object-fit:cover;border-radius:4px;"></td>
                <td>${f.name}</td>
                <td>₹${f.price}</td>
                <td>${f.is_veg ? '<span class="badge badge-success">Veg</span>' : '<span class="badge badge-danger">Non-Veg</span>'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteFood(${f.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) { console.error(e); }
}

async function loadRestCategories() {
    try {
        const cats = await ApiClient.get('/categories').catch(()=>[]);
        const ul = document.getElementById('restCategoriesList');
        ul.innerHTML = '';
        cats.forEach(c => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${c.name}
                <button class="btn btn-sm btn-danger" onclick="deleteCategory(${c.id})"><i class="fas fa-trash"></i></button>
            `;
            ul.appendChild(li);
        });
    } catch(e) { console.error(e); }
}

async function deleteFood(id) {
    if(confirm('Delete this item?')) {
        await ApiClient.delete(`/restaurant/foods/${id}`).catch(()=>showToast('Failed to delete','error'));
        loadRestFoods();
    }
}
async function deleteCategory(id) {
    if(confirm('Delete this category?')) {
        await ApiClient.delete(`/restaurant/categories/${id}`).catch(()=>showToast('Failed to delete','error'));
        loadRestCategories();
    }
}
