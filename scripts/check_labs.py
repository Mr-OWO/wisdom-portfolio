import re

with open('app/static/js/labs.js', 'r', encoding='utf-8') as f:
    code = f.read()

render_cases = re.findall(r'case\s+["\']([^"\']+)["\']\s*:', code)
print(f'Total case statements in labs.js: {len(render_cases)}')
unique_cases = sorted(list(set(render_cases)))
print(f'Unique slugs handled: {len(unique_cases)}')
for c in unique_cases:
    print(' -', c)
