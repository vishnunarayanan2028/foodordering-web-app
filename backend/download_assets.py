import os
import urllib.request

# Ensure target directory exists
IMAGE_DIR = r"e:\Foodbooking\frontend\images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Map of filename -> Unsplash URL
ASSETS = {
    # UI Banner & Sections
    "foodmunch-banner-bg.jpg": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1600&auto=format&fit=crop&q=80",
    "food-serve.png": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&auto=format&fit=crop&q=80",
    "fruits-img.png": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=300&auto=format&fit=crop&q=80",
    "offers-img.png": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=300&auto=format&fit=crop&q=80",
    "delivery-payment-section-img.png": "https://images.unsplash.com/photo-1526367790999-0150786686a2?w=600&auto=format&fit=crop&q=80",
    "healthy-food-plate-img.png": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&auto=format&fit=crop&q=80",
    "thanking-customers-section-img.png": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80",
    
    # Categories
    "em-non-veg-starters-img.png": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&auto=format&fit=crop&q=80",
    "em-veg-starters-img.png": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=600&auto=format&fit=crop&q=80",
    "em-soup-img.png": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&auto=format&fit=crop&q=80",
    "em-grilled-seafood-img.png": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600&auto=format&fit=crop&q=80",
    "em-hyderabadi-biryani-img.png": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80",
    "em-mushroom-noodles-img.png": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600&auto=format&fit=crop&q=80",
    "em-gluten-img.png": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&auto=format&fit=crop&q=80",
    "em-coffee-bourbon-img.png": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&auto=format&fit=crop&q=80",
    
    # Foods
    "chicken-tikka.jpg": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&auto=format&fit=crop&q=80",
    "tandoori-chicken.jpg": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=600&auto=format&fit=crop&q=80",
    "fish-amritsari.jpg": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600&auto=format&fit=crop&q=80",
    "mutton-seekh-kebab.jpg": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&auto=format&fit=crop&q=80",
    "paneer-tikka.jpg": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=600&auto=format&fit=crop&q=80",
    "hara-bhara-kebab.jpg": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop&q=80",
    "crispy-corn.jpg": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=600&auto=format&fit=crop&q=80",
    "mushroom-pepper-fry.jpg": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop&q=80",
    "tomato-shorba.jpg": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&auto=format&fit=crop&q=80",
    "hot-sour-soup.jpg": "https://images.unsplash.com/photo-1541832676-9b763b0239ab?w=600&auto=format&fit=crop&q=80",
    "manchow-soup.jpg": "https://images.unsplash.com/photo-1603105037880-880cd4edfb5d?w=600&auto=format&fit=crop&q=80",
    "cream-mushroom-soup.jpg": "https://images.unsplash.com/photo-1547592180-85f173990554?w=600&auto=format&fit=crop&q=80",
    "grilled-fish.jpg": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600&auto=format&fit=crop&q=80",
    "prawn-masala.jpg": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=600&auto=format&fit=crop&q=80",
    "fish-curry.jpg": "https://images.unsplash.com/photo-1535400255456-984241443b29?w=600&auto=format&fit=crop&q=80",
    "tandoori-prawns.jpg": "https://images.unsplash.com/photo-1559737679-d6536b0429f9?w=600&auto=format&fit=crop&q=80",
    "hyderabadi-biryani.jpg": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80",
    "butter-chicken.jpg": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=600&auto=format&fit=crop&q=80",
    "palak-paneer.jpg": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=600&auto=format&fit=crop&q=80",
    "dal-makhani.jpg": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600&auto=format&fit=crop&q=80",
    "hakka-noodles.jpg": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600&auto=format&fit=crop&q=80",
    "schezwan-noodles.jpg": "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=600&auto=format&fit=crop&q=80",
    "mushroom-noodles.jpg": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&auto=format&fit=crop&q=80",
    "singapore-noodles.jpg": "https://images.unsplash.com/photo-1552611052-33e04de081de?w=600&auto=format&fit=crop&q=80",
    "caesar-salad.jpg": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=600&auto=format&fit=crop&q=80",
    "greek-salad.jpg": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&auto=format&fit=crop&q=80",
    "garden-fresh-salad.jpg": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&auto=format&fit=crop&q=80",
    "quinoa-bowl.jpg": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=600&auto=format&fit=crop&q=80",
    "gulab-jamun.jpg": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&auto=format&fit=crop&q=80",
    "rasmalai.jpg": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80",
    "chocolate-brownie.jpg": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&auto=format&fit=crop&q=80",
    "kulfi.jpg": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600&auto=format&fit=crop&q=80",
}

print(f"Downloading {len(ASSETS)} assets to {IMAGE_DIR}...")
for fname, url in ASSETS.items():
    dest = os.path.join(IMAGE_DIR, fname)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(dest, 'wb') as f:
            f.write(resp.read())
        print(f"  [OK] {fname}")
    except Exception as e:
        print(f"  [ERR] {fname}: {e}")

# Generate a high quality SVG/PNG logo for Food Munch Logo
svg_logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 60" width="240" height="60">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#d0b200;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#a88f00;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="30" cy="30" r="22" fill="url(#grad)" />
  <path d="M22 22 C22 16, 38 16, 38 22 L38 34 C38 40, 22 40, 22 34 Z" fill="#0d1b2a" />
  <circle cx="30" cy="26" r="4" fill="#d0b200" />
  <text x="60" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-weight="bold" font-size="24" fill="#0d1b2a">
    Food <tspan fill="#d0b200">Munch</tspan>
  </text>
</svg>"""

with open(os.path.join(IMAGE_DIR, "food-munch-logo.svg"), "w", encoding="utf-8") as f:
    f.write(svg_logo)
print("  [OK] food-munch-logo.svg generated")

print("All assets processed successfully!")
