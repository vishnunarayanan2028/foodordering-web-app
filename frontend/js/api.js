const API_BASE = '/api';

class ApiClient {
    static getToken() { return localStorage.getItem('token'); }
    static setToken(token) { localStorage.setItem('token', token); }
    static removeToken() { localStorage.removeItem('token'); }
    static getUser() { return JSON.parse(localStorage.getItem('user') || 'null'); }
    static setUser(user) { localStorage.setItem('user', JSON.stringify(user)); }
    static removeUser() { localStorage.removeItem('user'); }
    static isLoggedIn() { return !!this.getToken(); }
    
    static async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const headers = { 'Content-Type': 'application/json', ...options.headers };
        const token = this.getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;
        
        try {
            const response = await fetch(url, { ...options, headers });
            
            let data = null;
            try {
                data = await response.json();
            } catch (jsonErr) {
                data = null;
            }

            if (response.status === 401) {
                if (!endpoint.includes('/auth/login') && !endpoint.includes('/auth/register')) {
                    this.removeToken();
                    this.removeUser();
                    if (!window.location.pathname.endsWith('login.html')) {
                        window.location.href = '/login.html';
                    }
                }
                throw new Error((data && data.message) ? data.message : 'Invalid email or password');
            }
            
            if (!response.ok) {
                throw new Error((data && data.message) ? data.message : `API Error (${response.status})`);
            }
            return (data && data.data !== undefined) ? data.data : data;

        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }
    
    static get(endpoint) { return this.request(endpoint); }
    static post(endpoint, data) { return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) }); }
    static put(endpoint, data) { return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data) }); }
    static delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }
    
    static logout() {
        this.removeToken();
        this.removeUser();
        window.location.href = '/login.html';
    }
}

function updateNavbar() {
    const user = ApiClient.getUser();
    const authNav = document.getElementById('authNav');
    const cartNav = document.getElementById('cartNav');
    
    if (!authNav) return;
    
    if (user) {
        let dashboardLink = '';
        if (user.role === 'admin') dashboardLink = '<li class="nav-item"><a class="nav-link" href="/admin-dashboard.html">Dashboard</a></li>';
        else if (user.role === 'restaurant') dashboardLink = '<li class="nav-item"><a class="nav-link" href="/restaurant-dashboard.html">Dashboard</a></li>';
        
        authNav.innerHTML = `
            ${dashboardLink}
            <li class="nav-item"><a class="nav-link" href="/orders.html">My Orders</a></li>
            <li class="nav-item"><a class="nav-link" href="/profile.html">${user.name}</a></li>
            <li class="nav-item"><a class="nav-link" href="#" onclick="ApiClient.logout(); return false;">Logout</a></li>
        `;
        if (cartNav && user.role === 'customer') {
            cartNav.style.display = 'block';
            updateCartBadge();
        } else if (cartNav) {
            cartNav.style.display = 'none';
        }
    } else {
        authNav.innerHTML = `
            <li class="nav-item"><a class="nav-link" href="/login.html">Login</a></li>
            <li class="nav-item"><a class="nav-link" href="/register.html">Register</a></li>
        `;
        if (cartNav) cartNav.style.display = 'none';
    }
}

async function updateCartBadge() {
    try {
        const cart = await ApiClient.get('/cart');
        const count = cart.items ? cart.items.reduce((acc, item) => acc + item.quantity, 0) : 0;
        const badge = document.getElementById('cartBadgeCount');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    } catch (e) {
        console.error('Failed to update cart badge', e);
    }
}

function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => { 
        toast.classList.remove('show'); 
        setTimeout(() => toast.remove(), 300); 
    }, 3000);
}

document.addEventListener('DOMContentLoaded', updateNavbar);
