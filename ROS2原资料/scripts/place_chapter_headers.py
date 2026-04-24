from pathlib import Path
import re

root = Path(r"d:/ziliao/ROS2_Tuition-main/ROS2_Tuition-main/_book/_book")
file_path = root / 'ROS2.md'
if not file_path.exists():
    print('ROS2.md not found')
    raise SystemExit(1)

text = file_path.read_text(encoding='utf-8')

# If file starts with the 6 chapter headers we previously inserted, remove that leading block
if text.lstrip().startswith('# 第1章'):
    m = re.search(r"\n##\s*1\.1\b", text)
    if m:
        # keep from the '## 1.1' line onward
        text = text[m.start()+1:]

# Chapter headers to insert
headers = {
    1: ('# 第1章  ROS2 概述与环境搭建', '本章概述 ROS2 的背景、主要概念与版本信息，并指导在目标平台上快速搭建开发与运行环境。'),
    2: ('# 第2章  ROS2 通信机制核心', '本章讲解 ROS2 的核心通信模型：话题（Topics）、服务（Services）、动作（Actions）和参数（Parameters），并给出接口定义与示例实现。'),
    3: ('# 第3章  ROS2 通信机制补充', '本章补充分布式部署、命名规则、时间/定时 API 及常用通信工具的使用与实战案例。'),
    4: ('# 第4章  ROS2 工具：launch 与 rosbag2', '本章介绍 launch 文件（包括 Python/XML 实现）和 rosbag2 的录制、回放与编程使用方法。'),
    5: ('# 第5章  ROS2 工具：坐标变换（TF）', '本章覆盖 TF 坐标系的原理、广播与监听方法，以及常见的坐标变换实操示例。'),
    6: ('# 第6章  ROS2 工具：可视化与 URDF', '本章讲解 rviz2 可视化工具、URDF/xacro 语法与机器人模型集成与优化实践。'),
}

changed = False
for n in range(1, 7):
    # find the first subheading like '## 1.1' etc
    pat = re.compile(rf'(^##\s*{n}\.1\b.*)', re.MULTILINE)
    m = pat.search(text)
    if m:
        insert_pos = m.start()
        # Check if header already exists immediately before (avoid duplicates)
        before_segment = text[max(0, insert_pos-200):insert_pos]
        if f'# 第{n}章' in before_segment:
            continue
        title, summary = headers[n]
        insertion = f"{title}\n\n{summary}\n\n"
        text = text[:insert_pos] + insertion + text[insert_pos:]
        changed = True

if changed:
    file_path.write_text(text, encoding='utf-8')
    print('Inserted chapter headers into', file_path)
else:
    print('No insertions needed')
