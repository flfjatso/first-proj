import uuid
import logging
from datetime import datetime
from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType, Collection,
    utility
)

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

# 1. 创建用户登录数据集 sys_kb_user
def create_sys_kb_user():
    """创建系统用户数据集"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        COLLECTION_NAME = "sys_kb_user"
        
        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=64, is_primary=True),
            FieldSchema(name="emp_lob_num", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="emp_name", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name="password", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="create_time", dtype=DataType.VARCHAR, max_length=30),
            FieldSchema(name="update_time", dtype=DataType.VARCHAR, max_length=30),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128)  # 添加向量字段
        ]
        
        # 创建 schema
        schema = CollectionSchema(fields, description="系统用户登录信息")
        
        # 检查集合是否存在
        if utility.has_collection(COLLECTION_NAME):
            utility.drop_collection(COLLECTION_NAME)
            logger.info(f"⚠️ 删除已存在的集合 {COLLECTION_NAME}")
        
        # 创建集合
        collection = Collection(COLLECTION_NAME, schema)
        logger.info(f"✅ 创建集合 {COLLECTION_NAME} 成功")
        
        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="vector", index_params=index_params)
        logger.info(f"✅ 为集合 {COLLECTION_NAME} 创建索引成功")
        
        # 插入初始化数据
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = str(uuid.uuid4())
        # 生成全0向量
        empty_vector = [0.0] * 128
        insert_data = [
            [user_id],
            ["0000276236"],
            ["雷晓杰"],
            ["0000276236"],
            [now],
            [now],
            [empty_vector]
        ]
        
        collection.insert(insert_data)
        collection.flush()
        logger.info("✅ 插入初始化用户数据成功")
        
        # 断开连接
        connections.disconnect("default")
        logger.info("✅ 断开Milvus连接")
        
        return True
    except Exception as e:
        logger.error(f"❌ 创建系统用户数据集失败：{str(e)}")
        return False

# 2. 创建知识库数据集 svc_bk_base_info
def create_svc_bk_base_info():
    """创建知识库基础信息数据集"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        COLLECTION_NAME = "svc_bk_base_info"
        
        # 定义字段
        fields = [
            FieldSchema(name="bk_id", dtype=DataType.VARCHAR, max_length=64, is_primary=True),
            FieldSchema(name="bk_en_name", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="bk_cn_name", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="upload_time", dtype=DataType.VARCHAR, max_length=30),
            FieldSchema(name="update_time", dtype=DataType.VARCHAR, max_length=30),
            FieldSchema(name="uploaded_by", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128)  # 添加向量字段
        ]
        
        # 创建 schema
        schema = CollectionSchema(fields, description="知识库基础信息")
        
        # 检查集合是否存在
        if utility.has_collection(COLLECTION_NAME):
            utility.drop_collection(COLLECTION_NAME)
            logger.info(f"⚠️ 删除已存在的集合 {COLLECTION_NAME}")
        
        # 创建集合
        collection = Collection(COLLECTION_NAME, schema)
        logger.info(f"✅ 创建集合 {COLLECTION_NAME} 成功")
        
        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="vector", index_params=index_params)
        logger.info(f"✅ 为集合 {COLLECTION_NAME} 创建索引成功")
        
        # 插入初始化数据
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 生成全0向量
        empty_vector = [0.0] * 128
        
        # 插入资金计划知识库
        insert_data_1 = [
            ["a0c0cb30-5e8b-497b-a238-04ae62abde7b"],
            ["fp_butler_financial"],
            ["资金计划"],
            [now],
            [now],
            ["0000276236"],
            [empty_vector]
        ]
        
        # 插入标书知识库
        bid_id = str(uuid.uuid4())
        insert_data_2 = [
            [bid_id],
            ["fp_butler_bid"],
            ["标书"],
            [now],
            [now],
            ["0000276236"],
            [empty_vector]
        ]
        
        # 插入数据
        collection.insert(insert_data_1)
        collection.insert(insert_data_2)
        collection.flush()
        logger.info("✅ 插入初始化知识库数据成功")
        
        # 断开连接
        connections.disconnect("default")
        logger.info("✅ 断开Milvus连接")
        
        return True
    except Exception as e:
        logger.error(f"❌ 创建知识库数据集失败：{str(e)}")
        return False

# 3. 验证创建结果
def verify_collections():
    """验证数据集创建结果"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ 连接Milvus成功")
        
        # 检查系统用户集合
        if utility.has_collection("sys_kb_user"):
            collection = Collection("sys_kb_user")
            collection.load()  # 加载集合
            result = collection.query(expr="", output_fields=["id", "emp_lob_num", "emp_name"], limit=10)
            logger.info(f"✅ 系统用户集合存在，数据：{result}")
        else:
            logger.warning("❌ 系统用户集合不存在")
        
        # 检查知识库集合
        if utility.has_collection("svc_bk_base_info"):
            collection = Collection("svc_bk_base_info")
            collection.load()  # 加载集合
            result = collection.query(expr="", output_fields=["bk_id", "bk_en_name", "bk_cn_name"], limit=10)
            logger.info(f"✅ 知识库集合存在，数据：{result}")
        else:
            logger.warning("❌ 知识库集合不存在")
        
        # 断开连接
        connections.disconnect("default")
        logger.info("✅ 断开Milvus连接")
        
    except Exception as e:
        logger.error(f"❌ 验证数据集失败：{str(e)}")

if __name__ == "__main__":
    print("=== 初始化知识库系统 ===")
    
    # 创建系统用户数据集
    print("\n1. 创建系统用户数据集 sys_kb_user...")
    create_sys_kb_user()
    
    # 创建知识库数据集
    print("\n2. 创建知识库数据集 svc_bk_base_info...")
    create_svc_bk_base_info()
    
    # 验证结果
    print("\n3. 验证创建结果...")
    verify_collections()
    
    print("\n=== 初始化完成 ===")
