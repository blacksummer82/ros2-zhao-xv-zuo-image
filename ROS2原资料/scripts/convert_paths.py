from pathlib import Path
import re

# 配置：工作目录与目标文件
root = Path(r"d:/ziliao/ROS2_Tuition-main/ROS2_Tuition-main/_book/_book")
file_path = root / 'ROS2.md'

if not file_path.exists():
    print('ERROR: ROS2.md not found at', file_path)
    raise SystemExit(1)

text = file_path.read_text(encoding='utf-8')

# 判断是否为需要转换的相对 URL
def needs_convert(url):
    url = url.strip()
    if not url:
        return False
    if url.startswith('#'):
        return False
    low = url.lower()
    if low.startswith('http://') or low.startswith('https://') or low.startswith('file://'):
        return False
    # already absolute windows drive
    if re.match(r'^[a-zA-Z]:\\', url) or re.match(r'^[a-zA-Z]:/', url):
        return False
    # treat leading slash (site-root relative) as convertible
    if url.startswith('//'):
        return False
    if low.startswith('mailto:'):
        return False
    return True

# Resolve a relative url against the root to Windows absolute path
def to_windows_abs(url):
    # strip surrounding <>
    orig = url
    url = url.strip()
    if url.startswith('<') and url.endswith('>'):
        url = url[1:-1]
    # if URL contains space (title), keep only path part
    if ' ' in url and not url.startswith('http'):
        # common markdown: (path "title") -> split on space before quote
        url = url.split(' ')[0]
    # normalize slashes
    # if url starts with '/', it's site-root relative: strip leading '/'
    if url.startswith('/'):
        url = url.lstrip('/')
    p = (root / url).resolve()
    # produce Windows style path
    abs_path = str(p)
    # ensure backslashes
    abs_path = abs_path.replace('/', '\\')
    return abs_path

# Replace Markdown links/images: [text](url)
def repl_md(m):
    whole = m.group(0)
    before = m.group(1)
    url = m.group(2)
    after = m.group(3) or ''
    if needs_convert(url):
        new = to_windows_abs(url)
        return f"{before}({new}{after})"
    return whole

# pattern captures: (label)(url)(optional title)
md_pattern = re.compile(r'(!?\[[^\]]*\])\(([^)\s]+)([^)]*)\)')
text2 = md_pattern.sub(repl_md, text)

# Replace HTML src/href attributes
def repl_attr(m):
    attr = m.group(1)
    quote = m.group(2)
    url = m.group(3)
    if needs_convert(url):
        new = to_windows_abs(url)
        return f'{attr}={quote}{new}{quote}'
    return m.group(0)

html_pattern = re.compile(r'\b(src|href)=("|\')([^"\']+)("|\')', re.IGNORECASE)
text3 = html_pattern.sub(repl_attr, text2)

# Write back if changed
if text3 != text:
    file_path.write_text(text3, encoding='utf-8')
    print('Updated', file_path)
else:
    print('No changes needed')
