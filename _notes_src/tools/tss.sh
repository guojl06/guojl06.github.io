#!/usr/bin/env bash
# typst-section.sh — 增强版：支持全选、章节范围选择及 Preamble 保持
set -euo pipefail

usage() {
  cat <<EOF
用法: $(basename "$0") [选项] <file.typ>

选项:
  -l             列出文档中所有指定层级的章节
  -s <范围>      渲染指定章节 (例如: 1, 3-5)。不指定则默认渲染全部。
  -d <深度>      标题层级深度 (默认: 2，即匹配 == 标题)
  -o <输出路径>  输出 PDF 路径 (默认: 原文件名_sections.pdf)
  -k             保留临时 .typ 文件用于调试
  -h             显示此帮助

示例:
  $(basename "$0") notes.typ             # 渲染全部章节
  $(basename "$0") -s 1,3 notes.typ      # 仅渲染第1和第3章
  $(basename "$0") -l notes.typ          # 查看章节索引
EOF
}

# ──────────────────────────────────────────────
# 默认配置
# ──────────────────────────────────────────────
LIST_ONLY=false
SECTIONS="all"  # 默认渲染全部
DEPTH=2
OUTPUT=""
KEEP_TEMP=false

while getopts "ls:d:o:kh" opt; do
  case $opt in
    l) LIST_ONLY=true ;;
    s) SECTIONS="$OPTARG" ;;
    d) DEPTH="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    k) KEEP_TEMP=true ;;
    h) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

if [[ $# -lt 1 ]]; then
  echo "❌ 错误: 未指定输入文件" >&2; usage; exit 1
fi

INPUT="$1"
[[ ! -f "$INPUT" ]] && { echo "❌ 错误: 找不到文件 $INPUT"; exit 1; }

# ──────────────────────────────────────────────
# Python 逻辑：精准解析与提取
# ──────────────────────────────────────────────
PYTHON_SCRIPT=$(cat <<'PYEOF'
import sys, re

def parse_docs(text, depth):
    # 匹配恰好 depth 个 '=' 的标题，且必须在行首
    pattern = re.compile(r'^' + ('=' * depth) + r'(?!=)\s+(.*)$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    
    # 提取 Preamble (第一个标题之前的所有内容)
    preamble = text[:matches[0].start()] if matches else text
    
    sections = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        sections.append({
            "id": i + 1,
            "title": m.group(1).strip(),
            "content": text[start:end]
        })
    return preamble, sections

def get_wanted_indices(spec, total):
    if spec == "all": return set(range(1, total + 1))
    indices = set()
    try:
        for part in spec.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                indices.update(range(start, end + 1))
            else:
                indices.add(int(part))
    except ValueError:
        print(f"❌ 错误: 无效的范围格式 '{spec}'", file=sys.stderr); sys.exit(1)
    return {i for i in indices if 1 <= i <= total}

mode, path, depth_s = sys.argv[1:4]
with open(path, 'r', encoding='utf-8') as f:
    raw = f.read()

preamble, sections = parse_docs(raw, int(depth_s))

if mode == "list":
    if not sections:
        print(f"  (未发现深度为 {depth_s} 的标题)")
    for s in sections:
        print(f"  [{s['id']:>2}] {s['title']}")
elif mode == "extract":
    spec, out_tmp = sys.argv[4:6]
    wanted = get_wanted_indices(spec, len(sections))
    
    if not wanted and sections:
        print("❌ 错误: 指定的编号不在范围内", file=sys.stderr); sys.exit(1)
        
    chosen_content = [s['content'] for s in sections if s['id'] in wanted]
    # 组合渲染内容
    final_output = preamble + "\n" + "\n".join(chosen_content)
    
    with open(out_tmp, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    # 打印反馈
    print(f"✅ 已成功提取 {len(chosen_content)}/{len(sections)} 个章节")
PYEOF
)

# ──────────────────────────────────────────────
# 执行流程
# ──────────────────────────────────────────────

# 1. 列表模式
if $LIST_ONLY; then
  echo "📄 正在读取 $INPUT 中的章节 (深度: $DEPTH):"
  python3 -c "$PYTHON_SCRIPT" list "$INPUT" "$DEPTH"
  exit 0
fi

# 2. 准备输出路径
[[ -z "$OUTPUT" ]] && OUTPUT="${INPUT%.typ}_sections.pdf"

# 3. 创建临时文件
INPUT_DIR="$(dirname "$INPUT")"
TEMP_TYP="${INPUT_DIR}/.tmp_$(date +%s)_render.typ"
trap '[[ "$KEEP_TEMP" == false ]] && rm -f "$TEMP_TYP"' EXIT

# 4. 提取内容
python3 -c "$PYTHON_SCRIPT" extract "$INPUT" "$DEPTH" "$SECTIONS" "$TEMP_TYP"

# 5. 编译
echo "🚀 开始渲染 PDF..."
# 增加 --root 确保绝对路径下的资源引用的正确性
typst compile --root "$(pwd)" "$TEMP_TYP" "$OUTPUT"

echo "✨ 完成！输出文件: $OUTPUT"
[[ "$KEEP_TEMP" == true ]] && echo "📝 调试文件已保留: $TEMP_TYP"