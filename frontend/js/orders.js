document.addEventListener('DOMContentLoaded', () => {
    if (!ApiClient.isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }

    if (document.getElementById('ordersList')) {
        loadOrders();
    }

    if (document.getElementById('orderDetailContent')) {
        loadOrderDetail();
    }
});

async function loadOrders() {
    try {
        const orders = await ApiClient.get('/orders');
        const loading = document.getElementById('loadingIndicator');
        if (loading) loading.style.display = 'none';

        if (!orders || orders.length === 0) {
            const empty = document.getElementById('emptyOrders');
            if (empty) empty.style.display = 'block';
        } else {
            const list = document.getElementById('ordersList');
            if (!list) return;
            list.style.display = 'flex';
            list.innerHTML = '';

            orders.forEach(order => {
                const col = document.createElement('div');
                col.className = 'col-lg-6 mb-4';
                const date = new Date(order.created_at).toLocaleDateString('en-IN', {
                    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
                });

                const currentStatus = order.order_status || order.status || 'placed';
                const statusFmt = currentStatus.replace(/_/g, ' ').toUpperCase();
                const restName = order.restaurant_name || 'Madurai Hotel';
                const pStatus = (order.payment_status || 'pending').toUpperCase();
                const pBadgeClass = order.payment_status === 'paid' ? 'badge-success' : 'badge-warning';

                col.innerHTML = `
                    <div class="custom-card order-card p-3 shadow-sm h-100" style="cursor:pointer; border-radius:12px;" onclick="window.location.href='/order-detail.html?id=${order.id}'">
                        <div class="order-header d-flex justify-content-between align-items-start border-bottom pb-2 mb-2">
                            <div>
                                <h5 class="mb-1 font-weight-bold">Order #ORD-${order.id.toString().padStart(5, '0')}</h5>
                                <span class="text-warning small font-weight-bold"><i class="fas fa-store mr-1"></i>${restName}</span>
                                <br><small class="text-muted">${date}</small>
                            </div>
                            <div class="text-right">
                                <span class="badge badge-status status-${currentStatus} px-2 py-1">${statusFmt}</span>
                                <br><span class="badge ${pBadgeClass} px-2 py-1 mt-1 font-weight-bold" style="font-size:0.75rem;">${pStatus}</span>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-end mt-3 pt-2">
                            <div class="text-muted small">${order.items ? order.items.length : 'Multiple'} item(s)</div>
                            <h5 class="mb-0 text-primary-custom font-weight-bold">₹${parseFloat(order.total_amount).toFixed(2)}</h5>
                        </div>
                    </div>
                `;
                list.appendChild(col);
            });
        }
    } catch (error) {
        console.error('Failed to load orders', error);
        const loading = document.getElementById('loadingIndicator');
        if (loading) loading.style.display = 'none';
        const empty = document.getElementById('emptyOrders');
        if (empty) empty.style.display = 'block';
    }
}

async function loadOrderDetail() {
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('id');
    if (!orderId) { window.location.href = '/orders.html'; return; }

    try {
        const order = await ApiClient.get(`/orders/${orderId}`);
        const loading = document.getElementById('loadingIndicator');
        if (loading) loading.style.display = 'none';

        const content = document.getElementById('orderDetailContent');
        if (content) content.style.display = 'block';

        const date = new Date(order.created_at).toLocaleDateString('en-IN', {
            day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
        });

        const currentStatus = order.order_status || order.status || 'placed';

        document.getElementById('orderNum').textContent = `#ORD-${order.id.toString().padStart(5, '0')}`;
        document.getElementById('orderDate').textContent = date;

        const statusBadge = document.getElementById('orderStatusBadge');
        if (statusBadge) {
            statusBadge.className = `badge badge-status status-${currentStatus}`;
            statusBadge.textContent = currentStatus.replace(/_/g, ' ').toUpperCase();
        }

        // Setup cancel button
        const cancelBtn = document.getElementById('cancelOrderBtn');
        if (cancelBtn) {
            if (currentStatus === 'placed') {
                cancelBtn.style.display = 'block';
                cancelBtn.onclick = async () => {
                    if (confirm('Are you sure you want to cancel this order?')) {
                        try {
                            cancelBtn.disabled = true;
                            await ApiClient.put(`/orders/${orderId}/cancel`, {});
                            showToast('Order cancelled');
                            location.reload();
                        } catch (e) {
                            showToast(e.message || 'Failed to cancel', 'error');
                            cancelBtn.disabled = false;
                        }
                    }
                };
            } else {
                cancelBtn.style.display = 'none';
            }
        }

        // Render timeline
        const statuses = ['placed', 'confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered'];
        const icons = ['fa-clipboard-list', 'fa-check', 'fa-fire-burner', 'fa-box', 'fa-motorcycle', 'fa-home'];
        const titles = ['Order Placed', 'Confirmed', 'Preparing', 'Ready', 'Out for Delivery', 'Delivered'];

        let timelineHtml = '';
        if (currentStatus === 'cancelled') {
            timelineHtml = `
                <div class="timeline-step active">
                    <div class="timeline-icon" style="background:#ef4444;border-color:#ef4444;"><i class="fas fa-times text-white"></i></div>
                    <div class="timeline-content">
                        <div class="timeline-title text-danger">Order Cancelled</div>
                    </div>
                </div>
            `;
        } else {
            let passedCurrent = false;
            for (let i = 0; i < statuses.length; i++) {
                const s = statuses[i];
                const isActive = !passedCurrent;
                if (s === currentStatus) passedCurrent = true;

                timelineHtml += `
                    <div class="timeline-step ${isActive ? 'active' : ''}">
                        <div class="timeline-icon"><i class="fas ${icons[i]}"></i></div>
                        <div class="timeline-content">
                            <div class="timeline-title">${titles[i]}</div>
                        </div>
                    </div>
                `;
            }
        }
        const timeline = document.getElementById('orderTimeline');
        if (timeline) timeline.innerHTML = timelineHtml;

        // Render items
        const tbody = document.getElementById('orderItemsTable');
        if (tbody && order.items) {
            tbody.innerHTML = '';
            order.items.forEach(item => {
                const tr = document.createElement('tr');
                const itemName = item.food ? item.food.name : (item.food_name_snapshot || 'Food Item');
                const itemPrice = item.price_snapshot || item.price || (item.food ? item.food.price : 0);
                const itemImg = (item.food && item.food.image_url) ? item.food.image_url : '/images/em-veg-starters-img.png';
                const itemSubtotal = item.subtotal || (itemPrice * item.quantity);

                tr.innerHTML = `
                    <td>
                        <div class="d-flex align-items-center">
                            <img src="${itemImg}" style="width:40px;height:40px;object-fit:cover;border-radius:4px;margin-right:10px;">
                            ${itemName}
                        </div>
                    </td>
                    <td class="text-center">${item.quantity}</td>
                    <td class="text-right">₹${parseFloat(itemPrice).toFixed(2)}</td>
                    <td class="text-right font-weight-bold">₹${parseFloat(itemSubtotal).toFixed(2)}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Totals
        const subtotal = order.subtotal || (order.items ? order.items.reduce((acc, i) => acc + ((i.price_snapshot || i.price || 0) * i.quantity), 0) : 0);
        const tax = order.tax || (subtotal * 0.05);
        const delivery = order.delivery_fee || 40;

        if (document.getElementById('detailSubtotal')) document.getElementById('detailSubtotal').textContent = `₹${parseFloat(subtotal).toFixed(2)}`;
        if (document.getElementById('detailTax')) document.getElementById('detailTax').textContent = `₹${parseFloat(tax).toFixed(2)}`;
        if (document.getElementById('detailDelivery')) document.getElementById('detailDelivery').textContent = `₹${parseFloat(delivery).toFixed(2)}`;
        if (document.getElementById('detailTotal')) document.getElementById('detailTotal').textContent = `₹${parseFloat(order.total_amount).toFixed(2)}`;
        if (document.getElementById('detailAddress')) document.getElementById('detailAddress').textContent = `${order.delivery_address} (Phone: ${order.phone})`;

    } catch (error) {
        console.error('Failed to load order detail', error);
        showToast('Failed to load order details', 'error');
    }
}
