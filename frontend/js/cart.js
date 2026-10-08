document.addEventListener('DOMContentLoaded', () => {
    if (!ApiClient.isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }
    loadCart();
});

async function loadCart() {
    try {
        document.getElementById('loadingIndicator').style.display = 'block';
        document.getElementById('cartContent').style.display = 'none';
        document.getElementById('emptyCart').style.display = 'none';
        
        const cart = await ApiClient.get('/cart');
        
        document.getElementById('loadingIndicator').style.display = 'none';
        
        if (!cart || !cart.items || cart.items.length === 0) {
            document.getElementById('emptyCart').style.display = 'block';
        } else {
            renderCart(cart);
            document.getElementById('cartContent').style.display = 'flex';
        }
        
    } catch (error) {
        console.error('Failed to load cart', error);
        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('emptyCart').style.display = 'block';
    }
}

function renderCart(cart) {
    const list = document.getElementById('cartItemsList');
    list.innerHTML = '';
    
    let subtotal = 0;
    
    cart.items.forEach(item => {
        const itemTotal = item.food.price * item.quantity;
        subtotal += itemTotal;
        
        const div = document.createElement('div');
        div.className = 'cart-item';
        div.innerHTML = `
            <img src="${item.food.image_url || '/images/em-veg-starters-img.png'}" class="cart-item-img" alt="${item.food.name}">
            <div class="cart-item-details">
                <div class="cart-item-title">${item.food.name}</div>
                <div class="text-muted small mb-2">₹${item.food.price} each</div>
                <div class="qty-control">
                    <button class="qty-btn" onclick="updateQty(${item.id}, ${item.quantity - 1})">-</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn" onclick="updateQty(${item.id}, ${item.quantity + 1})">+</button>
                </div>
            </div>
            <div class="cart-item-price">₹${itemTotal}</div>
            <button class="btn-remove" onclick="removeItem(${item.id})" title="Remove item">
                <i class="fas fa-trash"></i>
            </button>
        `;
        list.appendChild(div);
    });
    
    const tax = subtotal * 0.05;
    const delivery = 40;
    const total = subtotal + tax + delivery;
    
    document.getElementById('summarySubtotal').textContent = `₹${subtotal.toFixed(2)}`;
    document.getElementById('summaryTax').textContent = `₹${tax.toFixed(2)}`;
    document.getElementById('summaryTotal').textContent = `₹${total.toFixed(2)}`;
    
    updateCartBadge();
}

async function updateQty(itemId, newQty) {
    if (newQty < 1) {
        removeItem(itemId);
        return;
    }
    try {
        await ApiClient.put(`/cart/items/${itemId}`, { quantity: newQty });
        loadCart();
    } catch (error) {
        showToast('Failed to update quantity', 'error');
    }
}

async function removeItem(itemId) {
    try {
        await ApiClient.delete(`/cart/items/${itemId}`);
        loadCart();
        showToast('Item removed');
    } catch (error) {
        showToast('Failed to remove item', 'error');
    }
}
