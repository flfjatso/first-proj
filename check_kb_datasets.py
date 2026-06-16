import logging
from pymilvus import connections, Collection, utility

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Milvus连接配置
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "rag_multi_kb"

def get_all_kb_names():
    """获取所有知识库名称"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        # 检查集合是否存在
        if not utility.has_collection(COLLECTION_NAME):
            logger.warning("⚠️ 集合不存在")
            return []
        
        # 获取集合
        collection = Collection(COLLECTION_NAME)
        collection.load()
        
        # 查询所有知识库名称
        result = collection.query(
            expr="",
            output_fields=["kb_name"],
            limit=1000  # 添加limit参数
        )
        
        # 去重获取知识库名称
        kb_names = list(set([item["kb_name"] for item in result]))
        logger.info(f"✅ 找到 {len(kb_names)} 个知识库")
        
        return kb_names
    except Exception as e:
        logger.error(f"❌ 获取知识库名称失败：{str(e)}")
        return []
    finally:
        # 断开连接
        if "default" in connections.list_connections():
            connections.disconnect("default")
            logger.info("✅ 断开Milvus连接")

def get_kb_documents(kb_name):
    """获取指定知识库中的文档"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        
        # 获取集合
        collection = Collection(COLLECTION_NAME)
        collection.load()
        
        # 查询指定知识库的所有文档
        result = collection.query(
            expr=f"kb_name == '{kb_name}'",
            output_fields=["doc_uuid", "doc_name"]
        )
        
        # 去重获取文档信息
        doc_info = {}
        for item in result:
            doc_uuid = item["doc_uuid"]
            doc_name = item["doc_name"]
            if doc_uuid not in doc_info:
                doc_info[doc_uuid] = doc_name
        
        logger.info(f"✅ 知识库 {kb_name} 中有 {len(doc_info)} 个文档")
        
        return doc_info
    except Exception as e:
        logger.error(f"❌ 获取知识库文档失败：{str(e)}")
        return {}
    finally:
        # 断开连接
        if "default" in connections.list_connections():
            connections.disconnect("default")

def check_collection_data():
    """检查集合中的数据"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        
        # 获取集合
        collection = Collection(COLLECTION_NAME)
        collection.load()
        
        # 获取集合统计信息
        stats = collection.get_stats()
        print(f"集合统计信息：{stats}")
        
        # 尝试查询一些数据
        try:
            result = collection.query(
                expr="",
                output_fields=["id", "kb_name", "doc_name"],
                limit=10
            )
            print(f"查询到 {len(result)} 条数据")
            for i, item in enumerate(result):
                print(f"  {i+1}. ID: {item.get('id')}, KB: {item.get('kb_name')}, Doc: {item.get('doc_name')}")
        except Exception as e:
            print(f"查询数据失败：{e}")
        
        connections.disconnect("default")
    except Exception as e:
        print(f"检查集合数据失败：{e}")

if __name__ == "__main__":
    print("=== 知识库数据集查询 ===")
    print(f"正在连接Milvus服务：{MILVUS_HOST}:{MILVUS_PORT}")
    print(f"集合名称：{COLLECTION_NAME}")
    print("-" * 50)
    
    try:
        # 先检查Milvus连接
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        print("✅ Milvus连接成功")
        
        # 检查集合是否存在
        if utility.has_collection(COLLECTION_NAME):
            print(f"✅ 集合 {COLLECTION_NAME} 存在")
            # 获取集合信息
            collection = Collection(COLLECTION_NAME)
            print(f"集合分区数量：{collection.num_partitions}")
            print(f"集合索引：{collection.indexes}")
        else:
            print(f"❌ 集合 {COLLECTION_NAME} 不存在")
        
        connections.disconnect("default")
    except Exception as e:
        print(f"❌ Milvus连接失败：{str(e)}")
    
    print("-" * 50)
    
    # 检查集合中的数据
    print("检查集合中的数据：")
    check_collection_data()
    
    print("-" * 50)
    
    # 获取所有知识库
    kb_names = get_all_kb_names()
    
    if not kb_names:
        print("❌ 未找到任何知识库")
    else:
        for kb_name in kb_names:
            print(f"\n📚 知识库：{kb_name}")
            print("-" * 50)
            
            # 获取知识库中的文档
            documents = get_kb_documents(kb_name)
            
            if not documents:
                print("  ❌ 该知识库中没有文档")
            else:
                print(f"  📄 文档数量：{len(documents)}")
                print("  📋 文档列表：")
                for doc_uuid, doc_name in documents.items():
                    print(f"    - {doc_name} (UUID: {doc_uuid})")
    
    print("\n=== 查询完成 ===")
