# 测试记录

## 2026-07-02

### 结构与触发词检查

- 检查方式：搜索旧 Skill 触发名、旧角色文档路径、旧 agent 展示名和旧默认 prompt。
- 结果：除本测试记录的说明文字外无命中。新的可执行入口不再引用旧 Skill 触发名或旧角色文档。

### 素材存在性检查

- 检查命令：`find assets/caomeiyaya-reference caomeiyaya-illustrations/assets/caomeiyaya-reference -type f | sort`
- 结果：根目录与 Skill 内部都包含 3 张草莓芽芽 PNG、`pet.json` 和 `spritesheet.webp`。

### Skill 目录检查

- 检查命令：`find caomeiyaya-illustrations -maxdepth 3 -type f | sort`
- 结果：可安装 Skill 目录已改为 `caomeiyaya-illustrations/`，包含 `SKILL.md`、`agents/openai.yaml`、`references/`、角色 reference 和原始结构样例。

### 第二阶段样片检查

- 检查命令：`file examples/caomeiyaya-showcase/*.png caomeiyaya-illustrations/assets/caomeiyaya-showcase/*.png`
- 结果：6 张正文配图样片已调整为 IP 锁定版，均为 2048 x 1152 PNG；根目录展示区与 Skill 内部展示区各保留一份。

### IP 定稿板检查

- 检查命令：`python3 scripts/build_ip_lock_board.py`
- 结果：已从桌宠 `spritesheet.webp` 生成 IP 标准板与默认帧集合，并同步到根目录资产与 Skill 内部资产。
- 检查命令：`file assets/caomeiyaya-ip-lock/*.png caomeiyaya-illustrations/assets/caomeiyaya-ip-lock/*.png`
- 结果：`caomeiyaya-ip-model-sheet.png` 为 2400 x 1600 PNG，`default-sprite-frames.png` 为 1152 x 588 PNG，根目录与 Skill 内部各保留一份。
- 检查命令：`python3 -m py_compile scripts/build_ip_lock_board.py scripts/generate_ip_locked_showcase.py scripts/generate_qwen_showcase.py`
- 结果：脚本语法检查通过。

### 图像生成说明

- IP 锁定样片命令：`python3 scripts/generate_ip_locked_showcase.py`
- 当前正式样片角色直接来自桌宠 `spritesheet.webp` 默认帧，避免文生图把角色改成泛草莓小人。
- Qwen 参考图输入实验：`qwen-image-2.0-pro` 支持使用 IP 标准板作为参考图，但实测会出现照片背景、大段标题或说明文字漂移，因此未作为当前正式样片来源；`scripts/generate_qwen_showcase.py` 作为后续实验工具保留。

### 安装与推送检查

- 本机安装命令：`mkdir -p /Users/cynthial/.codex/skills/caomeiyaya-illustrations`，随后 `rsync -a caomeiyaya-illustrations/ /Users/cynthial/.codex/skills/caomeiyaya-illustrations/`
- 安装验证：`/Users/cynthial/.codex/skills/caomeiyaya-illustrations/SKILL.md` 的 frontmatter 为 `name: caomeiyaya-illustrations`。
- 安装样片验证：本机安装目录包含 6 张 `assets/caomeiyaya-showcase/0*.png`，均为 2048 x 1152 PNG。
- 推送验证：第二阶段提交 `536e61c Add Caomeiyaya showcase samples` 已通过 SSH 推送到 `cynthialxxxx/caomeiyaya-illustrations` 的 `main` 分支；随后执行 `git fetch git@github.com:cynthialxxxx/caomeiyaya-illustrations.git main:refs/remotes/origin/main`，本地 `origin/main` 已更新到同一提交。
