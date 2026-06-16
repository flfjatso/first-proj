#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：查询和打印svc_bk_base_info数据集
用于验证知识库管理功能的数据存储情况
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymilvus import connections, Collection
import logging
from datetime import datetime

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


def connect_milvus():
    """连接Milvus数据库"""
    try:
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info("✅ Milvus连接成功")
        return True
    except Exception as e:
        logger.error(f"❌ 连接Milvus失败：{str(e)}")
        return False


def disconnect_milvus():
    """断开Milvus连接"""
    try:
        if "default" in connections.list_connections():
            connections.disconnect("default")
            logger.info("✅ Milvus连接已断开")
    except Exception as e:
        logger.error(f"❌ 断开Milvus连接失败：{str(e)}")


def check_collection_exists(collection_name):
    """检查集合是否存在"""
    try:
        collections = Collection.list_collections()
        exists = collection_name in collections
        logger.info(f"集合 '{collection_name}' 存在: {exists}")
        return exists
    except Exception as e:
        logger.error(f"检查集合存在性失败：{str(e)}")
        return False


def get_collection_info(collection_name):
    """获取集合信息"""
    try:
        collection = Collection(collection_name)
        schema = collection.schema
        logger.info(f"📊 集合 '{collection_name}' 信息：")
        logger.info(f"   - 实体数量: {collection.num_entities}")
        logger.info(f"   - 字段数量: {len(schema.fields)}")

        for field in schema.fields:
            logger.info(f"   - 字段: {field.name}, 类型: {field.dtype}, 主键: {field.is_primary}")

        return collection.schema
    except Exception as e:
        logger.error(f"获取集合信息失败：{str(e)}")
        return None


def query_all_knowledge_bases():
    """查询所有知识库数据"""
    try:
        if not connect_milvus():
            return []

        collection_name = "svc_bk_base_info"

        # 检查集合是否存在
        if not check_collection_exists(collection_name):
            logger.error(f"集合 '{collection_name}' 不存在")
            return []

        # 获取集合信息
        get_collection_info(collection_name)

        # 加载集合
        collection = Collection(collection_name)
        collection.load()

        # 查询所有数据
        result = collection.query(
            expr="",  # 空表达式表示查询所有
            output_fields=["bk_id", "bk_en_name", "bk_cn_name", "upload_time", "update_time", "uploaded_by"],
            limit=1000  # 限制查询数量
        )

        logger.info(f"📈 查询到 {len(result)} 条知识库记录")

        # 打印数据
        if result:
            print("\n" + "=" * 80)
            print("📚 知识库数据列表")
            print("=" * 80)

            for i, kb in enumerate(result, 1):
                print(f"\n🔹 记录 #{i}")
                print(f"   ID: {kb.get('bk_id', 'N/A')}")
                print(f"   英文名称: {kb.get('bk_en_name', 'N/A')}")
                print(f"   中文名称: {kb.get('bk_cn_name', 'N/A')}")
                print(f"   上传时间: {kb.get('upload_time', 'N/A')}")
                print(f"   更新时间: {kb.get('update_time', 'N/A')}")
                print(f"   上传人: {kb.get('uploaded_by', 'N/A')}")

        else:
            print("❌ 没有找到任何知识库记录")

        disconnect_milvus()
        return result

    except Exception as e:
        logger.error(f"查询知识库数据失败：{str(e)}")
        disconnect_milvus()
        return []


def test_specific_query():
    """测试特定查询"""
    try:
        if not connect_milvus():
            return

        collection = Collection("svc_bk_base_info")
        collection.load()

        # 查询前5条记录
        result = collection.query(
            expr="",
            output_fields=["bk_id", "bk_en_name", "bk_cn_name"],
            limit=5
        )

        if result:
            print("\n" + "=" * 50)
            print("🔍 前5条知识库记录（简要信息）")
            print("=" * 50)
            for i, kb in enumerate(result, 1):
                print(f"{i}. {kb.get('bk_id', 'N/A')} - {kb.get('bk_en_name', 'N/A')} - {kb.get('bk_cn_name', 'N/A')}")

        disconnect_milvus()

    except Exception as e:
        logger.error(f"特定查询测试失败：{str(e)}")
        disconnect_milvus()


def main():
    """主函数"""
    print("🚀 开始测试 svc_bk_base_info 数据集")
    print("=" * 60)

    # 测试1: 查询所有知识库数据
    print("\n1️⃣ 测试1: 查询所有知识库数据")
    knowledge_bases = query_all_knowledge_bases()

    # 测试2: 特定查询测试
    print("\n2️⃣ 测试2: 特定查询测试")
    test_specific_query()

    # 汇总信息
    print("\n" + "=" * 60)
    print("📋 测试汇总")
    print("=" * 60)
    print(f"✅ 总记录数: {len(knowledge_bases)}")
    print(f"✅ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if knowledge_bases:
        print("✅ 数据查询成功")
    else:
        print("⚠️  未找到数据或查询失败")


if __name__ == "__main__":
    main()