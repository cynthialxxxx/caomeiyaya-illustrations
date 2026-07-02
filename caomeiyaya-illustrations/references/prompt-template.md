# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean product-sketch feeling with a soft playful character. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no sticker poster, no children's illustration, no realistic UI.

Recurring IP character required:
草莓芽芽, a tiny strawberry desktop-pet character. She has a red strawberry hat with seed dots, green leaf bangs, small sprout leaves, soft round face with blush, light green overalls, red shoes, and small strawberry accessories or vines. 草莓芽芽 must perform the core conceptual action, not decorate the scene. Keep her recognizable, expressive, and slightly dramatic, but the cuteness must serve the article's structure.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：草莓芽芽在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Black for main line art, structure, and handwritten labels. Strawberry red for 草莓芽芽's hat and key warnings/problems/results. Leaf green for 草莓芽芽's leaf bangs, overalls, vines, and small identity details. Orange for main flow/path/arrows. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, dense explainer, cute sticker sheet, or mascot poster. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, cute but not childish, playful but clean.
```

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强角色参与感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 草莓芽芽 more central to the conceptual action. 草莓芽芽 should be doing the work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, recognizable, and not a sticker poster.
```
