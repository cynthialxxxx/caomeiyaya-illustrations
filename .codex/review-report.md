# 复盘报告

## 设计原则

本次改造保留原始小黑正文配图 Skill 的核心方法论：先提炼文章认知锚点，再用一个低科技、手绘、留白充分的视觉隐喻表达一个核心结构。二创重点放在默认 IP、提示词、QA 与展示文档上，避免把整个 Skill 改成单纯头像、贴纸或表情包生成器。

## 方案取舍

- 选择把可安装目录重命名为 `caomeiyaya-illustrations/`，让安装后触发名自然变为 `$caomeiyaya-illustrations`。
- 选择新增 `references/caomeiyaya-ip.md` 替代 `xiaohei-ip.md`，明确草莓帽、叶片刘海、绿色背带装、草莓配件等识别点。
- 选择保留原始小黑 example 图片作为结构校准资产，并在 README/NOTICE 中注明来源；新增草莓芽芽 reference 资产用于角色稳定。
- 选择改写 prompt 和 QA，强调“可以软萌，但必须服务结构表达”，防止生成结果退化成可爱贴纸。

## 风险与后续建议

- 当前还没有生成新的 16:9 草莓芽芽正文配图样片，下一步建议按视频方法生成 5-8 张 reference/样片再补入 README。
- 原始小黑 examples 仍保留在仓库中，适合做结构校准；如果后续草莓芽芽样片足够稳定，可以逐步替换根目录 `examples/images/`。
- 如果要让本机 Codex 直接可用，还需要把 `caomeiyaya-illustrations/` 复制到 `$CODEX_HOME/skills/`，这会写入仓库外目录，执行前应单独确认。
