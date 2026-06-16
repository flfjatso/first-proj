#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理Milvus中的无效数据
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


def clean_collection(collection_name):
    """清理指定集合的无效数据"""
    try:
        if not utility.has_collection(collection_name):
            logger.info(f"ℹ️ 集合不存在: {collection_name}")
            return

        collection = Collection(collection_name)
        collection.load()

        # 先统计清理前的状态
        num_entities_before = collection.num_entities
        results_before = collection.query(expr="id like '%'", output_fields=["id"])
        query_count_before = len(results_before)

        logger.info(f"📊 清理前 - num_entities: {num_entities_before}, query_count: {query_count_before}")

        # 执行flush操作清理无效数据
        logger.info("🔄 执行flush操作清理无效数据...")
        collection.flush()

        # 再次统计清理后的状态
        num_entities_after = collection.num_entities
        results_after = collection.query(expr="id like '%'", output_fields=["id"])
        query_count_after = len(results_after)

        logger.info(f"📊 清理后 - num_entities: {num_entities_after}, query_count: {query_count_after}")

        if num_entities_after == query_count_after:
            logger.info("✅ 数据清理成功，统计一致")
        else:
            logger.warning("⚠️ 数据清理后仍然不一致")

    except Exception as e:
        logger.error(f"❌ 清理集合 {collection_name} 失败: {str(e)}")


def main():
    """主函数"""
    logger.info("🚀 开始清理Milvus无效数据...")

    # 连接Milvus
    if not connect_milvus():
        logger.error("❌ 无法连接Milvus，退出")
        return

    # 清理指定集合
    clean_collection("svc_bk_file_metadata")
    clean_collection("svc_bk_file_vector_chunks")


if __name__ == "__main__":
    main()