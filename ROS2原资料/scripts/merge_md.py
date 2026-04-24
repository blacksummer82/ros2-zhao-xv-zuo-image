import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
output = root / 'ROS2.md'

html = index.read_text(encoding='utf-8')
# find data-path attributes in order
paths = re.findall(r'data-path="([^"]+)"', html)
mds = []
for p in paths:
    if p == './':
        candidate = 'README.md'
    else:
        candidate = p.replace('.html', '.md')
    if candidate not in mds:
        mds.append(candidate)

# also try to include any md from the gitbook.page JSON structure if available
page_json_matches = re.findall(r'"path":"([^"]+\.md)"', html)
for p in page_json_matches:
    if p not in mds:
        mds.append(p)

# normalize and read
contents = []
missing = []
for md in mds:
    md_path = root / md
    if md_path.exists():
        contents.append(md_path.read_text(encoding='utf-8'))
    else:
        # try without leading ./
        md_path2 = root / md.lstrip('./')
        if md_path2.exists():
            contents.append(md_path2.read_text(encoding='utf-8'))
        else:
            missing.append(md)

# write output
with open(output, 'w', encoding='utf-8') as f:
    for i, c in enumerate(contents):
        f.write(c)
        if not c.endswith('\n'):
            f.write('\n')
        f.write('\n')

print('WROTE', output)
if missing:
    print('MISSING:', len(missing), 'files')
    for m in missing:
        print('-', m)
else:
    print('All files found.')
