from pathlib import Path
import re

root = Path(r"d:/ziliao/ROS2_Tuition-main/ROS2_Tuition-main/_book/_book")
file_path = root / 'ROS2.md'

if not file_path.exists():
    print('ERROR: ROS2.md not found at', file_path)
    raise SystemExit(1)

text = file_path.read_text(encoding='utf-8')
# normalize backslashes to forward for easier regex
text_fs = text.replace('\\', '/')
root_unix = str(root).replace('\\', '/')

# replace absolute windows-like paths that contain the repo root
pattern = re.compile(r"[A-Za-z]:/[^)\s\"']+")

def repl(m):
    p = m.group(0)
    p_unix = p.replace('\\', '/')
    # case-insensitive match for Windows drive letter
    if root_unix.lower() in p_unix.lower():
        # find index using lower-case to preserve original casing beyond matched prefix
        idx = p_unix.lower().find(root_unix.lower())
        rel = p_unix[idx + len(root_unix):]
        rel = '/' + rel.lstrip('/')
        return rel
    return p

text2 = pattern.sub(repl, text_fs)

# write back (use forward slashes for site-root relative paths)
if text2 != text:
    file_path.write_text(text2, encoding='utf-8')
    print('Reverted paths in', file_path)
else:
    print('No changes needed')
