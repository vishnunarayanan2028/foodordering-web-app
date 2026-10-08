from dotenv import load_dotenv
load_dotenv()

from app.extensions import db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.category import Category
from app.models.food import Food

LOCAL_IMG = '/images/'

def seed_data(drop_tables=False):
    if drop_tables:
        db.drop_all()
    db.create_all()
    print("Tables ready.")

    # --- Users ---
    admin = User(name='Admin User', email='admin@demo.com', role='admin')
    admin.set_password('Demo@123')

    restaurant_user = User(name='Restaurant Owner', email='restaurant@demo.com', role='restaurant')
    restaurant_user.set_password('Demo@123')

    customer = User(name='John Customer', email='customer@demo.com', role='customer')
    customer.set_password('Demo@123')

    db.session.add_all([admin, restaurant_user, customer])
    db.session.commit()
    print("Users created.")

    # --- Madurai Restaurants ---
    restaurants_data = [
        {
            'name': 'Murugan Idli Shop',
            'description': 'Famous iconic Madurai veg tiffin center known for soft ghee podi idlis, crisp vadas, uthappam & filter coffee.',
            'address': '46, Town Hall Road, Madurai - 625001',
            'phone': '+91-452-234-1234',
            'email': 'contact@muruganidlishop.com',
            'image_url': LOCAL_IMG + 'murugan-idli-shop.jpg',
            'rating': 4.8,
            'cuisine': 'Authentic South Indian Veg Tiffin',
            'city': 'Madurai'
        },
        {
            'name': 'Simmakkal Konar Mess',
            'description': 'World-famous origin of Madurai Mutton Kari Dosa, Bun Parotta, Kola Urundai and authentic Madurai non-veg delicacies.',
            'address': '147, North Veli Street, Simmakkal, Madurai - 625001',
            'phone': '+91-452-233-5678',
            'email': 'orders@konarmessmadurai.com',
            'image_url': LOCAL_IMG + 'konar-mess.jpg',
            'rating': 4.7,
            'cuisine': 'Traditional Madurai Non-Veg & Kari Dosa',
            'city': 'Madurai'
        },
        {
            'name': 'Famous Special Jigarthanda',
            'description': "Madurai's original & legendary Jigarthanda shop serving chilled Badam Pisin ice cream drinks since 1977.",
            'address': '144, East Marret Street, Madurai - 625001',
            'phone': '+91-452-232-9999',
            'email': 'info@famousjigarthanda.com',
            'image_url': LOCAL_IMG + 'jigarthanda-shop.jpg',
            'rating': 4.9,
            'cuisine': 'Madurai Famous Coolers & Desserts',
            'city': 'Madurai'
        },
        {
            'name': 'Amma Mess',
            'description': 'Iconic Madurai non-veg landmark famous for Bone Marrow Omelette (Nalli Fry), Ayra Fish Fry & Crab Masala.',
            'address': '136, Alagar Kovil Main Road, KK Nagar, Madurai - 625020',
            'phone': '+91-452-253-4321',
            'email': 'ammamess@maduraifood.com',
            'image_url': LOCAL_IMG + 'amma-mess.jpg',
            'rating': 4.6,
            'cuisine': 'Madurai Special Non-Veg & Seafood',
            'city': 'Madurai'
        },
        {
            'name': 'Sree Sabarees Veg Restaurant',
            'description': 'Premier vegetarian restaurant near Meenakshi Temple serving banana leaf meals & crispy ghee roast dosas.',
            'address': '15, West Tower Street, Near Meenakshi Temple, Madurai - 625001',
            'phone': '+91-452-234-8888',
            'email': 'sabarees@maduraiveg.com',
            'image_url': LOCAL_IMG + 'sree-sabarees.jpg',
            'rating': 4.6,
            'cuisine': 'South Indian Pure Veg & Filter Coffee',
            'city': 'Madurai'
        },
        {
            'name': 'Kumar Mess',
            'description': 'Traditional Madurai mess famous for Seeraga Samba Mutton Biryani, Naattu Kozhi Roast & Viral Fish Curry.',
            'address': '80 Feet Road, KK Nagar, Madurai - 625020',
            'phone': '+91-452-258-7777',
            'email': 'kumarmess@maduraifood.com',
            'image_url': LOCAL_IMG + 'kumar-mess.jpg',
            'rating': 4.7,
            'cuisine': 'Seeraga Samba Biryani & Naattu Kozhi',
            'city': 'Madurai'
        }
    ]

    restaurants = []
    for r_data in restaurants_data:
        r = Restaurant(owner_id=restaurant_user.id, **r_data)
        restaurants.append(r)
        db.session.add(r)
    db.session.commit()
    print(f"{len(restaurants)} Madurai restaurants created.")

    r_map = {r.name: r for r in restaurants}

    # --- Categories ---
    categories_data = [
        {'name': 'Madurai Tiffin & Parotta', 'description': 'Iconic South Indian breakfast & fluffy bun parottas', 'image_url': LOCAL_IMG + 'em-veg-starters-img.png', 'display_order': 1},
        {'name': 'Biryani & Rice Meals', 'description': 'Aromatic Seeraga Samba biryanis & rich mess meals', 'image_url': LOCAL_IMG + 'em-hyderabadi-biryani-img.png', 'display_order': 2},
        {'name': 'Madurai Non-Veg Gravies', 'description': 'Spicy mutton chukkas, bone marrow omelettes & chicken roasts', 'image_url': LOCAL_IMG + 'em-non-veg-starters-img.png', 'display_order': 3},
        {'name': 'Seafood Delights', 'description': 'Fresh river fish fries & coastal crab masalas', 'image_url': LOCAL_IMG + 'em-grilled-seafood-img.png', 'display_order': 4},
        {'name': 'Jigarthanda & Beverages', 'description': 'Famous Madurai Jigarthanda, Nannari sarbath & filter coffee', 'image_url': LOCAL_IMG + 'em-coffee-bourbon-img.png', 'display_order': 5},
    ]

    categories = []
    for c_data in categories_data:
        cat = Category(restaurant_id=restaurants[0].id, **c_data)
        categories.append(cat)
        db.session.add(cat)
    db.session.commit()
    print("Categories created.")

    cat_map = {c.name: c for c in categories}

    # --- Foods mapped to specific Madurai Restaurants ---
    foods_data = [
        # Murugan Idli Shop
        {
            'restaurant': 'Murugan Idli Shop',
            'category': 'Madurai Tiffin & Parotta',
            'name': 'Soft Ghee Podi Idli (4 Pcs)',
            'description': 'Pillowy soft steamed rice cakes coated with aromatic spicy podi and pure ghee.',
            'price': 90,
            'image': 'ghee-podi-idli.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Murugan Idli Shop',
            'category': 'Madurai Tiffin & Parotta',
            'name': 'Onion Uthappam',
            'description': 'Thick rice pancake topped with finely chopped onions, green chillies, and cilantro.',
            'price': 110,
            'image': 'onion-uthappam.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Murugan Idli Shop',
            'category': 'Madurai Tiffin & Parotta',
            'name': 'Medu Vada (2 Pcs)',
            'description': 'Crispy golden lentil donuts served with fresh coconut chutney and hot sambar.',
            'price': 70,
            'image': 'medu-vada.jpg',
            'is_veg': True
        },

        # Simmakkal Konar Mess
        {
            'restaurant': 'Simmakkal Konar Mess',
            'category': 'Madurai Tiffin & Parotta',
            'name': 'Madurai Mutton Kari Dosa',
            'description': 'Three-layered signature dosa topped with fluffy egg omelette and spicy minced mutton gravy.',
            'price': 240,
            'image': 'kari-dosa.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Simmakkal Konar Mess',
            'category': 'Madurai Tiffin & Parotta',
            'name': 'Madurai Fluffy Bun Parotta (2 Pcs)',
            'description': 'Famous fluffy, golden-brown bun-shaped parottas served with rich spicy salna.',
            'price': 65,
            'image': 'bun-parotta.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Simmakkal Konar Mess',
            'category': 'Madurai Non-Veg Gravies',
            'name': 'Mutton Kola Urundai (4 Pcs)',
            'description': 'Crispy deep-fried spicy minced mutton meatballs seasoned with hand-ground spices.',
            'price': 180,
            'image': 'mutton-kola-urunadi.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Simmakkal Konar Mess',
            'category': 'Madurai Non-Veg Gravies',
            'name': 'Elumbu Roast (Mutton Bone Roast)',
            'description': 'Tender mutton marrow bones pan-roasted with spicy shallot and pepper masala.',
            'price': 270,
            'image': 'elumbu-roast.jpg',
            'is_veg': False
        },

        # Famous Special Jigarthanda
        {
            'restaurant': 'Famous Special Jigarthanda',
            'category': 'Jigarthanda & Beverages',
            'name': 'Famous Special Royal Jigarthanda',
            'description': 'Madurai legendary drink made with almond gum (badam pisin), nannari syrup, basundi milk & ice cream.',
            'price': 110,
            'image': 'special-jigarthanda.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Famous Special Jigarthanda',
            'category': 'Jigarthanda & Beverages',
            'name': 'Chilled Nannari Sarbath',
            'description': 'Refreshing natural herbal root extract cooler served with freshly squeezed lemon and soaked basil seeds.',
            'price': 50,
            'image': 'nannari-sarbath.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Famous Special Jigarthanda',
            'category': 'Jigarthanda & Beverages',
            'name': 'Madurai Basundi Delight',
            'description': 'Rich slow-reduced sweetened milk dessert infused with saffron, cardamom, and roasted nuts.',
            'price': 130,
            'image': 'basundi.jpg',
            'is_veg': True
        },

        # Amma Mess
        {
            'restaurant': 'Amma Mess',
            'category': 'Madurai Non-Veg Gravies',
            'name': 'Nalli Omelette (Bone Marrow Omelette)',
            'description': 'Fluffy double egg omelette infused with rich mutton bone marrow juice and crushed pepper.',
            'price': 210,
            'image': 'nalli-omelette.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Amma Mess',
            'category': 'Madurai Non-Veg Gravies',
            'name': 'Chicken Chintamani Fry',
            'description': 'Rustic Kongu & Madurai style chicken dish stir-fried with dry red chillies and gingelly oil.',
            'price': 260,
            'image': 'chicken-chintamani.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Amma Mess',
            'category': 'Seafood Delights',
            'name': 'Ayra Meen Fry (River Fish Fry)',
            'description': 'Fresh small river fish (Ayra Meen) pan-fried in traditional spicy red pepper marinade.',
            'price': 340,
            'image': 'ayra-fish-fry.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Amma Mess',
            'category': 'Biryani & Rice Meals',
            'name': 'Madurai Non-Veg Special Mess Meals',
            'description': 'Steaming hot white rice served with Mutton Gravy, Chicken Gravy, Fish Curry, Rasam & Appalam.',
            'price': 280,
            'image': 'non-veg-meals.jpg',
            'is_veg': False
        },

        # Sree Sabarees Veg Restaurant
        {
            'restaurant': 'Sree Sabarees Veg Restaurant',
            'category': 'Madurai Tiffin & Parotta',
            'name': 'Crispy Ghee Roast Paper Dosa',
            'description': 'Extra long wafer-thin crispy dosa roasted in pure cow ghee, served with 4 chutneys & sambar.',
            'price': 140,
            'image': 'ghee-roast-dosa.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Sree Sabarees Veg Restaurant',
            'category': 'Biryani & Rice Meals',
            'name': 'South Indian Special Banana Leaf Veg Meals',
            'description': 'Traditional banana leaf feast with Sambar, Vatha Kuzhambu, Poriyal, Kootu, Appalam & Sweet Payasam.',
            'price': 180,
            'image': 'veg-meals.jpg',
            'is_veg': True
        },
        {
            'restaurant': 'Sree Sabarees Veg Restaurant',
            'category': 'Jigarthanda & Beverages',
            'name': 'Kumbakonam Degree Filter Coffee',
            'description': 'Strong aromatic South Indian filter coffee brewed with chicory-blended coffee beans and hot cow milk.',
            'price': 45,
            'image': 'filter-coffee.jpg',
            'is_veg': True
        },

        # Kumar Mess
        {
            'restaurant': 'Kumar Mess',
            'category': 'Biryani & Rice Meals',
            'name': 'Seeraga Samba Mutton Biryani',
            'description': 'Authentic Madurai dum biryani made with fragrant Seeraga Samba rice and tender mutton pieces.',
            'price': 330,
            'image': 'seeraga-samba-biryani.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Kumar Mess',
            'category': 'Madurai Non-Veg Gravies',
            'name': 'Madurai Naattu Kozhi Pepper Roast',
            'description': 'Country chicken pan-roasted with freshly crushed black pepper, garlic, and shallots.',
            'price': 290,
            'image': 'nattu-kozhi-roast.jpg',
            'is_veg': False
        },
        {
            'restaurant': 'Kumar Mess',
            'category': 'Seafood Delights',
            'name': 'Viral Meen Tangy Fish Curry',
            'description': 'Fresh river snakehead fish cooked in a tangy tamarind, garlic, and coconut gravy.',
            'price': 310,
            'image': 'viral-meen-curry.jpg',
            'is_veg': False
        }
    ]

    food_count = 0
    for item in foods_data:
        rest = r_map[item['restaurant']]
        cat = cat_map[item['category']]
        food = Food(
            restaurant_id=rest.id,
            category_id=cat.id,
            name=item['name'],
            description=item['description'],
            price=item['price'],
            image_url=LOCAL_IMG + item['image'],
            is_veg=item['is_veg'],
            is_available=True
        )
        db.session.add(food)
        food_count += 1

    db.session.commit()
    print(f"{food_count} authentic Madurai food items created across {len(restaurants)} hotels!")
    print("MADURAI RESTAURANTS & FOOD DATABASE SEEDED SUCCESSFULLY!")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_data(drop_tables=True)
