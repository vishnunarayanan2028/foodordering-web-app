import os
import re

frontend_dir = r"e:\Foodbooking\frontend"

replacements = [
    ("https://d1tgh8fmlzexmh.cloudfront.net/ccbp-responsive-website/foodmunch-banner-bg.png", "/images/foodmunch-banner-bg.jpg"),
    ("https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/foodmunch-banner-bg.png", "/images/foodmunch-banner-bg.jpg"),
    ("https://d1tgh8fmlzexmh.cloudfront.net/ccbp-responsive-website/food-munch-img.png", "/images/food-munch-img.svg"),
    ("https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/food-munch-img.png", "/images/food-munch-img.svg"),
    ("https://d1tgh8fmlzexmh.cloudfront.net/ccbp-responsive-website/", "/images/"),
    ("https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/", "/images/"),
]

updated_files = 0
for root, dirs, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith(('.html', '.css', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = content
            for old, new in replacements:
                new_content = new_content.replace(old, new)
            
            if new_content != content:
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated image references in: {f}")
                updated_files += 1

print(f"Finished updating {updated_files} frontend files.")
