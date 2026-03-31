# WordEmbeddingDemo 新手说明书

## 这个项目是干什么的？

这是一个**词向量（Word Embedding）可视化教学项目**。  
你可以把它理解成一个网页小实验室，用图形直观地看：

- 词和词之间谁更像（相似度）
- 词向量怎么做“类比推理”（例如 `king - man + woman ≈ queen`）
- 不同语义维度（如 gender、age）如何影响词的位置

---

## 一句话理解“词向量”

把每个单词变成一串数字（向量），这串数字包含了词的语义信息。  
语义相近的词，向量也会更接近；某些语义关系可以用向量加减表示。

---

## 项目结构（先看这个）

- `index.html`  
  主页面，定义了所有 UI：3D 点图、向量热力图、输入框、类比面板、自定义维度面板。

- `wordembeddingdemo.js`  
  核心逻辑文件（最重要）：加载数据、处理用户操作、计算相似度、画图。

- `vector.js`  
  向量数学工具：加法、减法、点积、归一化等。

- `wordvecs50k.vec.gz`  
  压缩后的词向量模型（约 5 万词）。

- `nearest_words.txt`  
  预计算好的“每个词最相近的 10 个词”。

- `words50k.txt`  
  词表清单（一行一个词，表示模型里有哪些词）。

- `preprocess_model.sh` / `nearest_words.py`  
  离线预处理脚本，用来制作上面的数据文件。

- `tutorial.html` / `experiments.html`  
  教学文档和实验指导页面。

---

## 这个网页启动后会发生什么？

在 `wordembeddingdemo.js` 的 `main()` 里，大致流程是：

1. 显示 loading 提示
2. `fetch("wordvecs50k.vec.gz")` 下载模型
3. 用 `pako.inflate` 解压
4. 把文本向量读入内存（`processRawVecs`）
5. 读取 `nearest_words.txt`（`processNearestWords`）
6. 初次绘图：3D 散点图 + 右侧热力图
7. 绑定各种交互事件（点击、悬停、输入、窗口缩放等）

---

## 页面三大核心功能（小白视角）

## 1) 3D 散点图（左侧）
每个词是一个点。  
点的位置来自“把高维向量投影到 3 个方向”。

- 默认两个方向是语义维度（如 `[gender]`, `[age]`）
- 第三个是 residual（剩余信息方向）
- 点击词可以选中（变红）

---

## 2) 向量热力图（右侧）
显示多个词（最多 6 个）的向量分量颜色。

- 行 = 词
- 列 = 向量维度索引（0~299）
- 颜色 = 该维度数值大小
- 鼠标悬停会显示具体数值

---

## 3) 类比推理（底部面板）
输入 A、B、C，计算：

`y = vec(B) - vec(A) + vec(C)`

然后在词表里找与 `y` 最相似的词作为结果。  
这就是常见的“词向量做 analogy”。

---

## 关键代码函数（建议优先看）

在 `wordembeddingdemo.js` 中：

- `main()`  
  启动入口，加载数据并初始化图表。

- `processRawVecs(text)`  
  把模型文本解析成 `word -> vector` 的映射。

- `plotScatter()`  
  计算投影坐标，绘制 3D 散点图。

- `plotVector()` / `plotMagnify()`  
  绘制向量热力图和放大视图。

- `modifyWord()`  
  处理“添加/删除词”。

- `processAnalogy()`  
  处理类比计算逻辑（最经典的一段）。

---

## 数学上到底用了什么？

主要是两个概念：

1. **向量归一化**（unit vector）  
   向量长度变成 1，方便比较方向。

2. **点积（dot product）**  
   在归一化后，点积近似表示余弦相似度。  
   点积越大，两个词越相似。

`vector.js` 里就实现了这些基础操作。

---

## 数据文件之间的关系

- `wordvecs50k.vec.gz`：核心模型（单词 + 300维向量）
- `nearest_words.txt`：从模型预先算好的 top-10 邻居（加速前端悬停显示）
- `words50k.txt`：只是词表（方便查模型里是否有某词）

### `words50k.txt` 和 `wordvecs50k.vec.gz` 的区别（重点）

- `words50k.txt` 只有“单词列表”，一行一个词，适合快速查看模型包含哪些词。
- `wordvecs50k.vec.gz` 包含“单词 + 向量数值”，每行除了单词还有约 300 个数，是实际计算相似度和类比时用到的核心数据。
- 可以把它们理解成：`words50k.txt` 是“目录”，`wordvecs50k.vec.gz` 是“正文内容”。
- 前端真正用于数学计算的是 `wordvecs50k.vec.gz`，`words50k.txt` 更偏向检查和辅助分析。

---

## 如何运行（避免踩坑）

不要直接双击打开 HTML。  
建议用本地静态服务器（例如 Python 的 `http.server`）后再访问 `index.html`，否则 `fetch` 本地文件可能被浏览器限制。

---

## 给新手的阅读顺序（最快上手）

1. 先在网页里操作一遍（点词、加词、做类比）
2. 看 `experiments.html`（知道每个功能怎么玩）
3. 读 `wordembeddingdemo.js` 的这几段：`main` → `processRawVecs` → `plotScatter` → `processAnalogy`
4. 最后读 `tutorial.html` 补概念（为什么点积可以测相似）

---

## 你现在可以做的三个小实验

1. 输入 `man king woman` 做类比，观察结果和点图变化  
2. 添加 `doctor nurse teacher engineer` 看它们在图上的分布  
3. 在自定义维度里自己造一组词对（如 `good/bad`, `hot/cold`）看坐标轴如何变化

---

## 最后一句话

这个项目不是“训练模型”的代码库，而是“用已有模型做可视化教学”的代码库。  
你学会它，就已经掌握了词向量应用层最核心的一套思路。