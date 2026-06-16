#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复svc_bk_file_vector_chunks集合的索引问题
"""

from pymilvus import connections, utility, Collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_chunks_collection_index():
    """修复分片集合的索引"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host="localhost", port="19530")
        logger.info("✅ Milvus连接成功")
        
        # 检查集合是否存在
        collections = utility.list_collections()
        logger.info(f"📊 现有集合: {collections}")
        
        if "svc_bk_file_vector_chunks" not in collections:
            logger.error("❌ svc_bk_file_vector_chunks集合不存在")
            return False
        
        # 获取集合
        collection = Collection("svc_bk_file_vector_chunks")
        
        # 检查现有索引
        logger.info("🔍 检查现有索引...")
        indexes = collection.indexes
        logger.info(f"现有索引数量: {len(indexes)}")
        
        for i, index in enumerate(indexes):
            logger.info(f"  索引 {i+1}: {index.params}")
        
        # 为向量字段创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2", 
            "params": {"nlist": 128}
        }
        
        # 检查是否需要为chunk_embedding创建索引
        has_chunk_embedding_index = any(
            index.field_name == "chunk_embedding" for index in indexes
        )
        
        if not has_chunk_embedding_index:
            logger.info("🔄 为chunk_embedding字段创建索引...")
            collection.create_index("chunk_embedding", index_params)
            logger.info("✅ chunk_embedding索引创建成功")
        else:
            logger.info("✅ chunk_embedding字段已有索引")
        
        # 检查是否需要为dummy_vector创建索引
        has_dummy_vector_index = any(
            index.field_name == "dummy_vector" for index in indexes
        )
        
        if not has_dummy_vector_index:
            logger.info("🔄 为dummy_vector字段创建索引...")
            collection.create_index("dummy_vector", index_params)
            logger.info("✅ dummy_vector索引创建成功")
        else:
            logger.info("✅ dummy_vector字段已有索引")
        
        # 验证索引创建成功
        collection.load()
        logger.info("✅ 集合加载成功，索引修复完成")
        
        # 检查集合中的文档数量
        num_entities = collection.num_entities
        logger.info(f"📄 集合中的分片数量: {num_entities}")
        
        connections.disconnect("default")
        return True
        
    except Exception as e:
        logger.error(f"❌ 修复索引失败: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("🔧 开始修复分片集合索引...")
    
    if fix_chunks_collection_index():
        logger.info("🎉 索引修复完成，现在可以运行分片数据集检查脚本了")
        
        # 提示用户运行检查脚本
        print("\n🚀 现在可以运行分片数据集检查脚本:")
        print("python test\\test_svc_bk_file_vector_chunks.py")
    else:
        logger.error("❌ 索引修复失败")