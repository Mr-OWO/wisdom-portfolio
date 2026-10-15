import urllib.request
import json

print('=== 1. VERIFYING LIVE CSS ===')
req = urllib.request.Request('http://wisdomowabor.online/static/css/style.css', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    css_content = resp.read().decode('utf-8')
    has_light_theme = '--bg-main: #141722;' in css_content
    print('Live CSS updated with lighter theme:', has_light_theme)

print('\n=== 2. VERIFYING LIVE PROJECTS API ===')
req = urllib.request.Request('http://wisdomowabor.online/api/public/projects', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    projects = json.loads(resp.read().decode('utf-8'))
    print(f'Total projects returned from live API: {len(projects)}')
    for p in projects:
        print(f"[{p['id']}/20] {p['slug']} -> {p['github_url']}")
