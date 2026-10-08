let currentCategory = 'all';
let currentRestaurant = 'all';
let searchQuery = '';
let isVegOnly = false;
let allFoods = [];
let allRestaurants = [];

document.addEventListener('DOMContentLoaded', async () => {
    // Parse URL params
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('restaurant_id')) {
        currentRestaurant = urlParams.get('restaurant_id');
    }
    if (urlParams.has('category_id')) {
        currentCategory = urlParams.get('category_id');
    }

    await loadRestaurants();
    await loadCategories();
    await loadFoods();

    // Setup event listeners
    document.getElementById('searchInput').addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        renderFoods();
    });

    document.getElementById('vegFilter').addEventListener('change', (e) => {
        isVegOnly = e.target.checked;
        renderFoods();
    });

    const restSelect = document.getElementById('restaurantSelect');
    if (restSelect) {
        restSelect.addEventListener('change', (e) => {
            currentRestaurant = e.target.value;
            renderFoods();
        });
    }
});

async function loadRestaurants() {
    try {
        allRestaurants = await ApiClient.get('/restaurant/all').catch(() => []);
        const select = document.getElementById('restaurantSelect');
        if (!select) return;

        allRestaurants.forEach(r => {
            const opt = document.createElement('option');
            opt.value = r.id;
            opt.textContent = `📍 ${r.name} (${r.cuisine})`;
            if (String(r.id) === String(currentRestaurant)) {
                opt.selected = true;
            }
            select.appendChild(opt);
        });
    } catch (error) {
        console.error('Failed to load restaurants', error);
    }
}

async function loadCategories() {
    try {
        const categories = await ApiClient.get('/categories').catch(() => []);
        const container = document.getElementById('categoryPills');
        if (!container) return;

        categories.forEach(cat => {
            const pill = document.createElement('div');
            pill.className = 'category-pill';
            if (String(cat.id) === String(currentCategory)) {
                pill.classList.add('active');
            }
            pill.textContent = cat.name;
            pill.dataset.id = cat.id;
            pill.addEventListener('click', () => {
                document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                currentCategory = cat.id;
                renderFoods();
            });
            container.appendChild(pill);
        });

        // Setup 'all' click
        container.firstElementChild.addEventListener('click', (e) => {
            document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
            e.target.classList.add('active');
            currentCategory = 'all';
            renderFoods();
        });
    } catch (error) {
        console.error('Failed to load categories', error);
    }
}

async function loadFoods() {
    try {
        const loading = document.getElementById('loadingIndicator');
        if (loading) loading.style.display = 'block';

        allFoods = await ApiClient.get('/foods').catch(() => []);

        if (loading) loading.style.display = 'none';
        renderFoods();
    } catch (error) {
        console.error('Failed to load foods', error);
    }
}

function renderFoods() {
    const grid = document.getElementById('foodGrid');
    const emptyState = document.getElementById('emptyState');
    if (!grid) return;
    grid.innerHTML = '';

    const filtered = allFoods.filter(food => {
        const matchesRestaurant = currentRestaurant === 'all' || String(food.restaurant_id) === String(currentRestaurant);
        const matchesCategory = currentCategory === 'all' || String(food.category_id) === String(currentCategory);
        const matchesSearch = food.name.toLowerCase().includes(searchQuery) || (food.description && food.description.toLowerCase().includes(searchQuery));
        const matchesVeg = !isVegOnly || food.is_veg;
        return matchesRestaurant && matchesCategory && matchesSearch && matchesVeg;
    });

    if (filtered.length === 0) {
        if (emptyState) emptyState.style.display = 'block';
    } else {
        if (emptyState) emptyState.style.display = 'none';
        filtered.forEach(food => {
            const col = document.createElement('div');
            col.className = 'col-12 col-md-6 col-lg-4 col-xl-3 mb-4';

            const isVeg = food.is_veg;
            const badgeClass = isVeg ? 'veg' : 'non-veg';
            const badgeText = isVeg ? 'Veg' : 'Non-Veg';
            const imgUrl = food.image_url || '/images/em-veg-starters-img.png';
            const restName = food.restaurant_name || 'Madurai Hotel';

            col.innerHTML = `
                <div class="custom-card food-card h-100 d-flex flex-column">
                    <div class="food-img-wrapper" style="position:relative; overflow:hidden; border-radius:12px 12px 0 0;">
                        <img src="${imgUrl}" class="food-img" alt="${food.name}" style="width:100%; height:180px; object-fit:cover;">
                        <div class="food-badge ${badgeClass}" style="position:absolute; top:10px; right:10px;">${badgeText}</div>
                        <div class="hotel-tag" style="position:absolute; bottom:10px; left:10px; background:rgba(0,0,0,0.75); color:#ffd700; padding:3px 8px; border-radius:4px; font-size:0.75rem; font-weight:bold;">
                            <i class="fas fa-hotel mr-1"></i>${restName}
                        </div>
                    </div>
                    <div class="food-info p-3 d-flex flex-column flex-grow-1">
                        <h5 class="font-weight-bold mb-1">${food.name}</h5>
                        <p class="text-muted small flex-grow-1 mb-2">${food.description || ''}</p>
                        <div class="d-flex justify-content-between align-items-center mt-auto pt-2 border-top">
                            <span class="font-weight-bold text-dark h5 mb-0">₹${food.price}</span>
                            <button class="custom-outline-button btn-sm font-weight-bold" onclick="addToCart(${food.id})">
                                <i class="fas fa-cart-plus mr-1"></i> Add
                            </button>
                        </div>
                    </div>
                </div>
            `;
            grid.appendChild(col);
        });
    }
}

async function addToCart(foodId) {
    if (!ApiClient.isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }

    try {
        await ApiClient.post('/cart/items', { food_id: foodId, quantity: 1 });
        showToast('Item added to cart!');
        updateCartBadge();
    } catch (error) {
        showToast(error.message || 'Failed to add item', 'error');
    }
}
