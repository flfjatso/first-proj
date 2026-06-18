# KB Milvus - RAG 知识库系统

基于 Flask + Milvus + BGE-M3 构建的检索增强生成（RAG）知识库管理平台，支持多知识库管理、文档向量化存储、智能检索与大模型问答。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Web 框架 | Flask |
| 向量数据库 | Milvus |
| 嵌入模型 | BGE-M3 (1024 维) |
| 大模型 API | 智谱 AI (GLM-4-flash) |
| 文档解析 | PyPDF2 / python-docx / openpyxl / xlrd |
| 前端 | HTML + JavaScript (marked.js) |

---

## 功能特性

### 核心功能
- **多知识库管理**：支持创建多个知识库，每个知识库独立配置专属提示词
- **文档上传与处理**：支持 PDF / Word / TXT / SQL / Excel(.xlsx/.xls) 等格式
- **文档自动清洗**：自动移除图片、视频、Base64、HTML 多媒体标签等冗余内容
- **智能分片与向量化**：基于 BGE-M3 模型生成 1024 维向量，支持超大文件分片（5000+ 分片）
- **向量相似度检索**：基于 Milvus ANN 搜索实现语义检索
- **RAG + LLM 问答**：检索片段拼接上下文，通过 SSE 流式调用大模型生成回答
- **用户与权限管理**：基于 Milvus 的简易用户登录与 Session 管理
- **数据分析看板**：统计知识库、文档、分片数量及文件类型分布
- **CLI 工具**：`upload_sql_to_kb.py` 支持命令行批量入库

### 系统模块
- **用户管理** (`/user_management`)：增删改查系统用户
- **知识库管理** (`/knowledge_base_management`)：创建、编辑、删除知识库
- **提示词管理** (`/prompt_management`)：按知识库配置专属 LLM 提示词
- **文档上传** (`/document_upload`)：上传文件并自动入库
- **文件管理** (`/file_management`)：查看与下载已上传的原始文件
- **智能搜索** (`/smart_search`)：向量检索 + LLM 流式问答
- **数据集查询** (`/dataset_query`)：浏览 Milvus 各集合结构
- **数据分析** (`/data_analysis`)：可视化统计与趋势分析

---

## 项目结构

```
kb_milvus/
├── app.py                          # Flask 主应用（路由 + 业务逻辑）
├── config/
│   ├── settings.py                 # 全局配置（Milvus / API / Flask）
│   └── prompts/                    # 知识库专属提示词存储目录
├── services/
│   └── document_processor.py       # 文档处理服务（解析、分片、向量化、入库）
├── routes/                         # 蓝图路由（当前未启用）
├── utils/                          # 工具函数
├── templates/                      # Jinja2 页面模板
│   ├── login.html
│   ├── dashboard.html
│   ├── document_upload.html
│   ├── smart_search.html
│   ├── data_analysis.html
│   ├── user_management.html
│   ├── knowledge_base_management.html
│   ├── prompt_management.html
│   ├── file_management.html
│   └── dataset_query.html
├── static/
│   └── marked.min.js               # Markdown 渲染前端库
├── uploads/
│   └── uploads_original/           # 原始文件存储目录
├── test/                           # 测试与运维脚本
├── init_kb_system.py               # 初始化 Milvus 集合（用户 + 知识库）
├── upload_sql_to_kb.py             # CLI 工具：将 .sql 文件入库到知识库
├── query_datasets.py               # 查询数据集内容脚本
├── check_kb_datasets.py            # 检查知识库数据集脚本
└── README.md                       # 项目说明
```

---

## 环境依赖

```bash
# 基础依赖
pip install flask pymilvus PyPDF2 python-docx torch transformers numpy requests openai

# Excel 处理（可选，若需解析 Excel 文档）
pip install openpyxl xlrd==1.2.0
```

> **注意**：BGE-M3 模型默认从本地路径 `D:\workspace_python\models\bge-m3` 加载，若不存在会自动回退到 HuggingFace `BAAI/bge-m3`。

---

## 快速开始

### 1. 启动 Milvus
确保 Milvus 服务已启动，默认连接地址为 `10.100.16.201:19530`（可在 `config/settings.py` 中修改）。

### 2. 初始化系统数据
```bash
python init_kb_system.py
```
该脚本会创建以下集合并插入初始数据：
- `sys_kb_user`：系统用户表（含默认用户）
- `svc_bk_base_info`：知识库基础信息表（含默认知识库）

### 3. 启动 Flask 服务
```bash
python app.py
```
服务默认监听 `10.100.16.201:8000`。

### 4. 访问系统
打开浏览器访问 `http://10.100.16.201:8000`，使用默认账号登录：
- **工号**：`admin`
- **密码**：`admin`

---

## Milvus 集合设计

| 集合名称 | 用途 | 关键字段 |
|----------|------|----------|
| `sys_kb_user` | 用户登录信息 | `id`, `emp_lob_num`, `emp_name`, `password` |
| `svc_bk_base_info` | 知识库基础信息 | `bk_id`, `bk_en_name`, `bk_cn_name` |
| `svc_bk_file_metadata` | 文档元数据 | `id`, `bk_en_name`, `opportunity_number`, `original_filename`, `file_size`, `total_chunks`, `md5_hash` |
| `svc_bk_file_vector_chunks` | 文档向量分片 | `chunk_id`, `document_id`, `chunk_index`, `chunk_content`, `chunk_embedding` (dim=1024) |

---

## 配置说明

修改 `config/settings.py` 中的参数以适配环境：

```python
# Milvus 连接
MILVUS_HOST = "10.100.16.201"
MILVUS_PORT = "19530"

# 智谱 AI API
AGENT_API_URL  = "https://open.bigmodel.cn/api/paas/v4/"
AGENT_API_KEY  = "your-api-key"
AGENT_MODEL    = "glm-4-flash"

# Flask 服务
SECRET_KEY   = "your-secret-key"
FLASK_HOST   = "10.100.16.201"
FLASK_PORT   = 8000
```

---

## CLI 工具

### 将 SQL 文件入库到知识库
```bash
python upload_sql_to_kb.py \
  --file "C:\path\to\file.sql" \
  --kb "fp_butler_financial" \
  --opportunity "emp_info_h" \
  --uploaded-by "cli" \
  --milvus-host "localhost" \
  --milvus-port "19530"
```

参数说明：
- `--file`：待上传的 SQL 文件路径
- `--kb`：目标知识库 `bk_id` 或 `bk_en_name`
- `--opportunity`：商机编号（用于检索过滤）
- `--uploaded-by`：上传人标识

---

## 主要 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/login` | GET / POST | 用户登录 |
| `/logout` | GET | 退出登录 |
| `/api/users` | GET / POST / PUT / DELETE | 用户管理 CRUD |
| `/api/knowledge_bases` | GET / POST / PUT / DELETE | 知识库管理 CRUD |
| `/api/upload_document` | POST | 文档上传与入库 |
| `/api/smart_search` | POST | 向量检索（返回片段） |
| `/api/smart_search_llm` | POST | RAG + LLM 流式问答（SSE） |
| `/api/kb_prompt` | GET / POST | 读取 / 保存知识库提示词 |
| `/download/<filename>` | GET | 下载原始文件 |

---

## 注意事项

1. **Milvus 更新限制**：Milvus 不支持直接更新字段，因此用户/知识库修改采用“先删除再插入”策略。
2. **分片长度控制**：`chunk_content` 字段最大长度 2000 字符，超长内容会自动截断到安全长度（1950 字符）。
3. **同名文档覆盖**：上传同名文档时会自动删除旧元数据、旧向量分片及旧磁盘文件。
4. **超大文件处理**：单文件分片上限 5000，采用批量插入（每批 1000）避免内存溢出。
5. **提示词配置**：每个知识库可在 `config/prompts/<bk_id>.md` 中配置专属提示词，未配置则回退到 `default.md`。

---

## 作者

- 雷晓杰

---

## 许可证

本项目仅供内部使用。
