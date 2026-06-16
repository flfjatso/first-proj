#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除无用数据集脚本
删除以下无用数据集：
- demo_collection
- rag_kb
"""

import logging
from pymilvus import connections, utility

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def connect_milvus():
    """连接Milvus"""
    try:
        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )
        logger.info("✅ Milvus连接成功")
        return True
    except Exception as e:
        logger.error(f"❌ Milvus连接失败: {str(e)}")
        return False

def delete_collection(collection_name):
    """删除指定集合"""
    try:
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            logger.info(f"✅ 成功删除数据集: {collection_name}")
            return True
        else:
            logger.info(f"ℹ️ 数据集不存在: {collection_name}")
            return False
    except Exception as e:
        logger.error(f"❌ 删除数据集失败 {collection_name}: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("🚀 开始删除无用数据集...")
    
    # 连接Milvus
    if not connect_milvus():
        logger.error("❌ 无法连接Milvus，退出")
        return
    
    # 要删除的数据集列表
    collections_to_delete = ["demo_collection", "rag_kb"]
    
    # 遍历删除每个数据集
    for collection in collections_to_delete:
        delete_collection(collection)
    
    # 显示当前所有集合
    try:
        current_collections = utility.list_collections()
        logger.info(f"📋 当前剩余数据集: {current_collections}")
    except Exception as e:
        logger.error(f"❌ 获取当前数据集失败: {str(e)}")
    
    logger.info("✅ 无用数据集清理完成")

if __name__ == "__main__":
    main()