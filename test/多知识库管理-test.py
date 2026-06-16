import uuid
import os
import logging
import pandas as pd
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document  # 新增：构造Document对象
from sentence_transformers import SentenceTransformer, models
from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType, Collection,
    utility
)

# -------------------------- 基础配置（复用） --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
VECTOR_DIMENSION = 1024
LOCAL_MODEL_PATH = r"D:\workspace_python\models\bge-m3"


# -------------------------- 工具函数（复用） --------------------------
def generate_doc_uuid() -> str:
    return str(uuid.uuid4())


def validate_kb_name(kb_name: str) -> bool:
    import re
    if re.match(r'^[a-zA-Z0-9_]{1,64}$', kb_name):
        return True
    logger.error(f"知识库名称非法：{kb_name}，仅支持字母/数字/下划线，长度1-64")
    return False


def get_kb_collection(kb_name: str) -> Collection:
    if not validate_kb_name(kb_name):
        raise ValueError(f"非法知识库名称：{kb_name}")

    COLLECTION_NAME = "rag_multi_kb"
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="kb_name", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="doc_uuid", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="doc_name", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIMENSION)
    ]
    schema = CollectionSchema(fields, description=f"多知识库管理集合：{kb_name}")

    if not utility.has_collection(COLLECTION_NAME):
        collection = Collection(COLLECTION_NAME, schema)
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "COSINE",
            "params": {"nlist": 256}
        }
        collection.create_index(field_name="vector", index_params=index_params)
        logger.info(f"✅ 新建多知识库集合 {COLLECTION_NAME} 并创建索引")
    else:
        collection = Collection(COLLECTION_NAME)
        logger.info(f"✅ 加载已有多知识库集合 {COLLECTION_NAME}")
    return collection


# -------------------------- 核心修改：新增Excel支持 --------------------------
def load_excel_document(file_path: str):
    """加载Excel文档（.xlsx/.xls），处理多工作表，转为LangChain Document对象"""
    try:
        # 读取Excel所有工作表
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        logger.info(f"✅ 读取Excel文件：{file_path}，包含工作表：{sheet_names}")

        documents = []
        for sheet_name in sheet_names:
            # 读取工作表，跳过空行，填充空值
            df = pd.read_excel(file_path, sheet_name=sheet_name, na_filter=True, na_value="")
            df = df.dropna(how="all")  # 删除全空行
            if df.empty:
                logger.warning(f"⚠️ 工作表 {sheet_name} 无有效内容，跳过")
                continue

            # 将DataFrame转为结构化文本（保留行列信息）
            sheet_text = []
            sheet_text.append(f"【工作表：{sheet_name}】")
            # 获取列名
            columns = df.columns.tolist()
            sheet_text.append(f"列名：{','.join([str(col) for col in columns])}")
            # 逐行拼接内容
            for idx, row in df.iterrows():
                row_text = f"行{idx + 1}：" + " | ".join([f"{col}={row[col]}" for col in columns])
                sheet_text.append(row_text)

            # 合并工作表文本，构造Document对象
            full_sheet_text = "\n".join(sheet_text)
            document = Document(
                page_content=full_sheet_text,
                metadata={"sheet_name": sheet_name, "file_path": file_path}
            )
            documents.append(document)

        logger.info(f"✅ Excel文档处理完成，生成有效Document数：{len(documents)}")
        return documents
    except Exception as e:
        logger.error(f"❌ 加载Excel文档失败：{file_path}，错误：{str(e)}")
        return None


def load_document_by_type(file_path: str):
    """扩展：支持docx/pdf/txt/xlsx/xls"""
    file_suffix = Path(file_path).suffix.lower()
    try:
        if file_suffix == ".docx":
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
        elif file_suffix == ".pdf":
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif file_suffix == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()
        elif file_suffix in [".xlsx", ".xls"]:  # 新增Excel支持
            documents = load_excel_document(file_path)
        else:
            raise ValueError(f"不支持的文件类型：{file_suffix}")

        if documents:
            logger.info(f"✅ 加载文档成功：{file_path}，原始文档数：{len(documents)}")
            return documents
        else:
            logger.warning(f"⚠️ 文档 {file_path} 无有效内容")
            return None
    except Exception as e:
        logger.error(f"❌ 加载文档失败：{file_path}，错误：{str(e)}")
        return None


# -------------------------- 其余函数（复用，无修改） --------------------------
def split_document(documents, chunk_size=512, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"✅ 文档分块完成，生成文本块数：{len(chunks)}")
    return chunks


def upload_document_to_kb(
        kb_name: str,
        file_path: str,
        doc_uuid: str = None,
        chunk_size: int = 512,
        chunk_overlap: int = 50
):
    if not doc_uuid:
        doc_uuid = generate_doc_uuid()
    doc_name = Path(file_path).name

    documents = load_document_by_type(file_path)
    if not documents:
        return doc_uuid, 0
    chunks = split_document(documents, chunk_size, chunk_overlap)
    if not chunks:
        return doc_uuid, 0

    model_path = Path(LOCAL_MODEL_PATH).resolve()
    word_embedding_model = models.Transformer(str(model_path))
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

    texts = [chunk.page_content for chunk in chunks]
    vectors = model.encode(texts, convert_to_tensor=False, show_progress_bar=True, batch_size=8)
    logger.info(f"✅ 生成向量完成，向量数量：{len(vectors)}，维度：{VECTOR_DIMENSION}")

    collection = get_kb_collection(kb_name)
    insert_data = [
        [kb_name] * len(texts),
        [doc_uuid] * len(texts),
        [doc_name] * len(texts),
        texts,
        vectors.tolist()
    ]

    try:
        insert_result = collection.insert(insert_data)
        collection.flush()
        inserted_count = len(insert_result.primary_keys)
        logger.info(f"✅ 文档 {doc_name}（UUID:{doc_uuid}）上传到知识库 {kb_name} 成功，插入分片数：{inserted_count}")
        return doc_uuid, inserted_count
    except Exception as e:
        logger.error(f"❌ 插入数据失败：{str(e)}")
        return doc_uuid, 0


def delete_document_from_kb(kb_name: str, doc_uuid: str):
    if not validate_kb_name(kb_name):
        return False

    collection = get_kb_collection(kb_name)
    delete_expr = f"kb_name == '{kb_name}' and doc_uuid == '{doc_uuid}'"
    try:
        collection.delete(delete_expr)
        collection.flush()
        logger.info(f"✅ 从知识库 {kb_name} 删除文档（UUID:{doc_uuid}）成功")
        return True
    except Exception as e:
        logger.error(f"❌ 删除文档失败：{str(e)}")
        return False


def get_kb_statistics(kb_name: str):
    if not validate_kb_name(kb_name):
        return {}

    collection = get_kb_collection(kb_name)
    collection.load()

    total_chunks_expr = f"kb_name == '{kb_name}'"
    total_chunks = collection.query(expr=total_chunks_expr, output_fields=["id"])
    total_chunks_count = len(total_chunks)

    doc_uuids = collection.query(expr=total_chunks_expr, output_fields=["doc_uuid"])
    unique_docs = len(set([item["doc_uuid"] for item in doc_uuids]))

    doc_stats = {}
    for item in doc_uuids:
        doc_uuid = item["doc_uuid"]
        doc_stats[doc_uuid] = doc_stats.get(doc_uuid, 0) + 1

    stats = {
        "kb_name": kb_name,
        "total_documents": unique_docs,
        "total_chunks": total_chunks_count,
        "document_chunks": doc_stats
    }
    logger.info(f"✅ 知识库 {kb_name} 统计：文档数={unique_docs}，分片数={total_chunks_count}")
    return stats


def search_kb(kb_name: str, query_text: str, top_k: int = 3):
    if not validate_kb_name(kb_name):
        return []

    collection = get_kb_collection(kb_name)
    collection.load()

    model_path = Path(LOCAL_MODEL_PATH).resolve()
    word_embedding_model = models.Transformer(str(model_path))
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    query_vector = model.encode([query_text], convert_to_tensor=False).tolist()

    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": 20}
    }
    filter_expr = f"kb_name == '{kb_name}'"

    results = collection.search(
        data=query_vector,
        anns_field="vector",
        param=search_params,
        limit=top_k,
        expr=filter_expr,
        output_fields=["kb_name", "doc_uuid", "doc_name", "content"]
    )

    search_results = []
    for i, hit in enumerate(results[0]):
        search_results.append({
            "rank": i + 1,
            "similarity": 1 - hit.distance,
            "doc_uuid": hit.entity.get("doc_uuid"),
            "doc_name": hit.entity.get("doc_name"),
            "content": hit.entity.get("content")[:200] + "..." if len(
                hit.entity.get("content")) > 200 else hit.entity.get("content")
        })

    logger.info(f"✅ 知识库 {kb_name} 检索完成，返回Top{top_k}结果")
    return search_results


# -------------------------- 主函数调用示例（新增Excel测试） --------------------------
if __name__ == "__main__":
    # 1. 连接Milvus
    connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)

    # 2. 上传Excel文档到指定知识库（示例）
    KB_NAME = "telecom_bidding"
    # 替换为你的Excel文件路径
    EXCEL_FILE_PATH = r"D:\workspace_python\知识库文档\电信项目参数表.xlsx"
    doc_uuid, inserted_count = upload_document_to_kb(KB_NAME, EXCEL_FILE_PATH)
    print(f"Excel文档UUID：{doc_uuid}，插入分片数：{inserted_count}")

    # 3. 统计知识库信息
    stats = get_kb_statistics(KB_NAME)
    print(f"知识库统计：{stats}")

    # 4. 检索Excel相关内容
    query_text = "电信项目 参数表 工作表1"
    search_results = search_kb(KB_NAME, query_text, top_k=3)
    for res in search_results:
        print(f"\n排名{res['rank']}（相似度{res['similarity']:.4f}）：")
        print(f"文档名称：{res['doc_name']}")
        print(f"内容：{res['content']}")

    # 5. （可选）删除Excel文档
    # delete_document_from_kb(KB_NAME, doc_uuid)

    # 6. 断开连接
    connections.disconnect("default")