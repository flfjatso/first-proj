#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一修复所有集合的索引问题
"""

from pymilvus import connections, utility, Collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_collection_index(collection_name, vector_fields):
    """修复指定集合的索引"""
    try:
        logger.info(f"🔧 开始修复集合: {collection_name}")
        
        # 获取集合
        collection = Collection(collection_name)
        
        # 检查现有索引
        indexes = collection.indexes
        logger.info(f"  现有索引数量: {len(indexes)}")
        
        for i, index in enumerate(indexes):
            logger.info(f"    索引 {i+1}: {index.field_name} -> {index.params}")
        
        # 为向量字段创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2", 
            "params": {"nlist": 128}
        }
        
        fixed_count = 0
        for field_name in vector_fields:
            # 检查是否需要创建索引
            has_index = any(index.field_name == field_name for index in indexes)
            
            if not has_index:
                logger.info(f"  🔄 为 {field_name} 字段创建索引...")
                collection.create_index(field_name, index_params)
                logger.info(f"  ✅ {field_name} 索引创建成功")
                fixed_count += 1
            else:
                logger.info(f"  ✅ {field_name} 字段已有索引")
        
        # 验证索引创建成功
        if fixed_count > 0:
            collection.load()
            logger.info(f"  ✅ 集合加载成功，索引修复完成")
        
        # 检查集合中的文档数量
        num_entities = collection.num_entities
        logger.info(f"  📄 集合中的文档数量: {num_entities}")
        
        return True
        
    except Exception as e:
        logger.error(f"  ❌ 修复集合 {collection_name} 索引失败: {str(e)}")
        return False

def fix_all_collections():
    """修复所有相关集合的索引"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host="localhost", port="19530")
        logger.info("✅ Milvus连接成功")
        
        # 检查集合是否存在
        collections = utility.list_collections()
        logger.info(f"📊 现有集合: {collections}")
        
        # 定义需要修复的集合和对应的向量字段
        collections_to_fix = {
            "svc_bk_file_metadata": ["dummy_vector"],
            "svc_bk_file_vector_chunks": ["chunk_embedding", "dummy_vector"]
        }
        
        success_count = 0
        total_count = len(collections_to_fix)
        
        for collection_name, vector_fields in collections_to_fix.items():
            if collection_name in collections:
                if fix_collection_index(collection_name, vector_fields):
                    success_count += 1
                logger.info("")
            else:
                logger.warning(f"⚠️ 集合 {collection_name} 不存在，跳过修复")
        
        connections.disconnect("default")
        
        if success_count == total_count:
            logger.info("🎉 所有集合索引修复完成")
            return True
        else:
            logger.warning(f"⚠️ 部分集合修复失败 ({success_count}/{total_count})")
            return False
        
    except Exception as e:
        logger.error(f"❌ 修复过程失败: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("🔧 开始统一修复所有集合索引...")
    
    if fix_all_collections():
        logger.info("\n🚀 索引修复完成，现在可以运行检查脚本了")
        
        # 提示用户运行检查脚本
        print("\n📋 建议按顺序运行以下检查脚本:")
        print("1. python test\\test_svc_bk_file_metadata.py")
        print("2. python test\\test_svc_bk_file_vector_chunks.py")
        print("3. python test\\test_document_processor.py")
        print("\n💡 如果检查脚本仍然失败，可能需要重新创建集合")
    else:
        logger.error("❌ 索引修复失败")