document.addEventListener('DOMContentLoaded', () => {
    if (!ApiClient.isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }
    
    // Pre-fill phone if available
    const user = ApiClient.getUser();
    if (user && user.phone) {
        document.getElementById('contactPhone').value = user.phone;
    }
    
    loadCheckoutSummary();
    
    document.getElementById('checkoutForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = document.getElementById('placeOrderBtn');
        const deliveryAddress = document.getElementById('deliveryAddress').value;
        const phone = document.getElementById('contactPhone').value;
        const notes = document.getElementById('orderNotes').value;
        const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
        
        try {
            btn.innerHTML = '<span class="loading-spinner" style="width:1rem;height:1rem;"></span> Processing...';
            btn.disabled = true;
            
            const res = await ApiClient.post('/orders', {
                delivery_address: deliveryAddress,
                phone: phone,
                notes: notes,
                payment_method: paymentMethod
            });
            
            window.location.href = `/order-confirmation.html?id=${res.id}`;
        } catch (error) {
            showToast(error.message || 'Failed to place order', 'error');
            btn.innerHTML = 'Place Order';
            btn.disabled = false;
        }
    });
});

async function loadCheckoutSummary() {
    try {
        const cart = await ApiClient.get('/cart');
        
        if (!cart || !cart.items || cart.items.length === 0) {
            window.location.href = '/cart.html';
            return;
        }
        
        const itemsContainer = document.getElementById('checkoutItems');
        let subtotal = 0;
        
        cart.items.forEach(item => {
            const itemTotal = item.food.price * item.quantity;
            subtotal += itemTotal;
            
            const div = document.createElement('div');
            div.className = 'd-flex justify-content-between mb-2 text-muted';
            div.innerHTML = `
                <span>${item.quantity} x ${item.food.name}</span>
                <span>₹${itemTotal}</span>
            `;
            itemsContainer.appendChild(div);
        });
        
        const tax = subtotal * 0.05;
        const delivery = 40;
        const total = subtotal + tax + delivery;
        
        document.getElementById('checkoutSubtotal').textContent = `₹${subtotal.toFixed(2)}`;
        document.getElementById('checkoutTax').textContent = `₹${tax.toFixed(2)}`;
        document.getElementById('checkoutTotal').textContent = `₹${total.toFixed(2)}`;
        
    } catch (error) {
        console.error('Failed to load checkout summary', error);
        showToast('Failed to load summary', 'error');
    }
}
