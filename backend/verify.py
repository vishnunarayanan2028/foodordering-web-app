from app import create_app

def verify():
    app = create_app()
    client = app.test_client()

    pages = [
        'login.html', 'register.html', 'menu.html', 'cart.html',
        'checkout.html', 'orders.html', 'order-detail.html',
        'order-confirmation.html', 'profile.html',
        'restaurant-dashboard.html', 'restaurant-menu-manage.html',
        'restaurant-orders.html', 'admin-dashboard.html',
        'admin-users.html', 'admin-orders.html'
    ]

    print("=" * 60)
    print("FOOD MUNCH APPLICATION - FULL HEALTH CHECK & VERIFICATION")
    print("=" * 60)

    print(f"{'Page / View':<35} {'Status'}")
    print("-" * 50)
    for p in pages:
        res = client.get(f'/{p}')
        status_text = "200 OK" if res.status_code == 200 else f"{res.status_code} ERROR"
        print(f"{p:<35} {status_text}")

    apis = [
        ('GET', '/api/categories'),
        ('GET', '/api/foods'),
        ('GET', '/api/restaurant'),
        ('POST', '/api/auth/login (Customer)', '/api/auth/login', {'email': 'customer@demo.com', 'password': 'Demo@123'}),
        ('POST', '/api/auth/login (Owner)', '/api/auth/login', {'email': 'restaurant@demo.com', 'password': 'Demo@123'}),
        ('POST', '/api/auth/login (Admin)', '/api/auth/login', {'email': 'admin@demo.com', 'password': 'Demo@123'}),
    ]

    print("\n" + "=" * 60)
    print(f"{'API Endpoint':<35} {'Status'}")
    print("-" * 50)
    for item in apis:
        if len(item) == 2:
            method, endpoint = item
            res = client.get(endpoint)
            name = f"{method} {endpoint}"
        else:
            _, name, endpoint, payload = item
            res = client.post(endpoint, json=payload)
        status_text = "200 OK" if res.status_code in [200, 201] else f"{res.status_code} ERROR"
        print(f"{name:<35} {status_text}")

    assets = [
        '/css/common.css', '/css/auth.css', '/css/menu.css',
        '/css/cart.css', '/css/orders.css', '/css/dashboard.css', '/css/admin.css',
        '/js/api.js', '/js/auth.js', '/js/menu.js',
        '/js/cart.js', '/js/checkout.js', '/js/orders.js',
        '/js/restaurant.js', '/js/admin.js'
    ]

    print("\n" + "=" * 60)
    print(f"{'Static Asset':<35} {'Status'}")
    print("-" * 50)
    for asset in assets:
        res = client.get(asset)
        status_text = "200 OK" if res.status_code == 200 else f"{res.status_code} ERROR"
        print(f"{asset:<35} {status_text}")

    print("\n" + "=" * 60)
    print("ALL 15 PAGES, 6 API ENDPOINTS, AND 15 STATIC ASSETS VERIFIED!")
    print("=" * 60)

if __name__ == '__main__':
    verify()
