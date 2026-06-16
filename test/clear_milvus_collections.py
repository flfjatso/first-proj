#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清空Milvus数据集脚本
"""

import logging
from pymilvus import connections, utility, Collection

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


def clear_collection(collection_name):
    """清空指定集合"""
    try:
        if not utility.has_collection(collection_name):
            logger.info(f"ℹ️ 集合不存在: {collection_name}")
            return True

        collection = Collection(collection_name)
        collection.load()

        # 根据集合名选择正确的主键字段
        if collection_name == "svc_bk_file_vector_chunks":
            # 这个集合的主键是 chunk_id
            collection.delete(expr="chunk_id like '%'")
        else:
            # 其他集合的主键是 id
            collection.delete(expr="id like '%'")

        collection.flush()
        num_entities = collection.num_entities

        if num_entities == 0:
            logger.info(f"✅ 成功清空集合: {collection_name}")
            return True
        else:
            logger.error(f"❌ 清空集合 {collection_name} 失败，剩余 {num_entities} 条数据")
            return False

    except Exception as e:
        logger.error(f"❌ 清空集合 {collection_name} 时发生错误: {str(e)}")
        return False


def main():
    """主函数"""
    logger.info("🚀 开始清空Milvus数据集...")

    # 连接Milvus
    if not connect_milvus():
        logger.error("❌ 无法连接Milvus，退出")
        return

    # 要清空的集合列表
    collections_to_clear = ["svc_bk_file_metadata", "svc_bk_file_vector_chunks"]

    # 遍历清空每个集合
    success_count = 0
    for collection in collections_to_clear:
        if clear_collection(collection):
            success_count += 1

    # 显示清空结果
    logger.info(f"\n📊 清空结果:")
    logger.info(f"    成功清空: {success_count}/{len(collections_to_clear)} 个集合")

    if success_count < len(collections_to_clear):
        logger.warning("⚠️ 部分集合清空失败，请检查错误信息")
    else:
        logger.info("✅ 所有集合清空成功")


if __name__ == "__main__":
    main()