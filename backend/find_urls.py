import os, re, urllib.request

urls = set()
frontend_dir = r"e:\Foodbooking"

for root, dirs, files in os.walk(frontend_dir):
    if 'node_modules' in root or '.git' in root or 'venv' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.css', '.js', '.py', '.sql')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                found = re.findall(r'https?://[^\s\'"`>\)]+', content)
                for u in found:
                    if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', '.svg', 'cloudfront', 'unsplash', 'images']):
                        urls.add((u, f))

print(f"Found {len(urls)} image URLs:")
for u, fname in sorted(urls):
    print(f"File: {fname:25s} URL: {u}")
