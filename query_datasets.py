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

def query_sys_kb_user():
    """查询系统用户数据集"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        # 检查集合是否存在
        if not utility.has_collection("sys_kb_user"):
            logger.warning("⚠️ 系统用户集合不存在")
            return
        
        # 获取集合
        collection = Collection("sys_kb_user")
        collection.load()
        
        # 查询数据
        result = collection.query(
            expr="",
            output_fields=["id", "emp_lob_num", "emp_name", "create_time"],
            limit=10
        )
        
        print("=== 系统用户数据集 ===")
        for item in result:
            print(f"ID: {item['id']}")
            print(f"工号: {item['emp_lob_num']}")
            print(f"姓名: {item['emp_name']}")
            print(f"创建时间: {item['create_time']}")
            print("-" * 50)
        
        # 断开连接
        connections.disconnect("default")
        logger.info("✅ 断开Milvus连接")
        
    except Exception as e:
        logger.error(f"❌ 查询系统用户数据集失败：{str(e)}")

def query_svc_bk_base_info():
    """查询知识库数据集"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        # 检查集合是否存在
        if not utility.has_collection("svc_bk_base_info"):
            logger.warning("⚠️ 知识库集合不存在")
            return
        
        # 获取集合
        collection = Collection("svc_bk_base_info")
        collection.load()
        
        # 查询数据
        result = collection.query(
            expr="",
            output_fields=["bk_id", "bk_en_name", "bk_cn_name", "upload_time", "uploaded_by"],
            limit=10
        )
        
        print("=== 知识库数据集 ===")
        for item in result:
            print(f"知识库ID: {item['bk_id']}")
            print(f"英文名称: {item['bk_en_name']}")
            print(f"中文名称: {item['bk_cn_name']}")
            print(f"上传时间: {item['upload_time']}")
            print(f"上传人: {item['uploaded_by']}")
            print("-" * 50)
        
        # 断开连接
        connections.disconnect("default")
        logger.info("✅ 断开Milvus连接")
        
    except Exception as e:
        logger.error(f"❌ 查询知识库数据集失败：{str(e)}")

if __name__ == "__main__":
    print("=== 查询数据集内容 ===")
    
    # 查询系统用户数据集
    print("\n1. 查询系统用户数据集 sys_kb_user...")
    query_sys_kb_user()
    
    # 查询知识库数据集
    print("\n2. 查询知识库数据集 svc_bk_base_info...")
    query_svc_bk_base_info()
    
    print("\n=== 查询完成 ===")
