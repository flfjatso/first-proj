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

def check_kb_data():
    """检查知识库数据"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        # 检查集合是否存在
        if not utility.has_collection(COLLECTION_NAME):
            logger.warning("⚠️ 集合不存在")
            return
        
        # 获取集合
        collection = Collection(COLLECTION_NAME)
        collection.load()
        
        # 尝试查询数据
        try:
            # 查询所有数据（限制100条）
            result = collection.query(
                expr="",
                output_fields=["id", "kb_name", "doc_name", "doc_uuid"],
                limit=100
            )
            
            if not result:
                print("❌ 集合中没有数据")
                return
            
            print(f"✅ 查询到 {len(result)} 条数据")
            
            # 统计知识库
            kb_dict = {}
            for item in result:
                kb_name = item.get("kb_name")
                doc_name = item.get("doc_name")
                doc_uuid = item.get("doc_uuid")
                
                if kb_name not in kb_dict:
                    kb_dict[kb_name] = {}
                
                if doc_uuid not in kb_dict[kb_name]:
                    kb_dict[kb_name][doc_uuid] = doc_name
            
            # 输出知识库信息
            print("\n=== 知识库数据集 ===")
            for kb_name, docs in kb_dict.items():
                print(f"\n📚 知识库：{kb_name}")
                print(f"  📄 文档数量：{len(docs)}")
                print("  📋 文档列表：")
                for doc_uuid, doc_name in docs.items():
                    print(f"    - {doc_name} (UUID: {doc_uuid})")
                    
        except Exception as e:
            print(f"查询数据失败：{e}")
        
    except Exception as e:
        logger.error(f"❌ 检查知识库数据失败：{str(e)}")
    finally:
        # 断开连接
        if "default" in connections.list_connections():
            connections.disconnect("default")
            logger.info("✅ 断开Milvus连接")

if __name__ == "__main__":
    print("=== 知识库数据集查询 ===")
    check_kb_data()
    print("\n=== 查询完成 ===")
