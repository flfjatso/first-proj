#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版测试脚本：查询和打印sys_kb_user数据集
用于验证用户管理功能的数据存储情况
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymilvus import connections, Collection, utility
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
        collections = utility.list_collections()
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


def query_all_users():
    """查询所有用户数据"""
    try:
        if not connect_milvus():
            return []

        collection_name = "sys_kb_user"

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
        #result = collection.query(expr="id != ''", output_fields=["*"])
        #result = collection.query(expr="id like '%'", output_fields=["*"])

        result = collection.query(
            expr="",  # 空表达式表示查询所有
            output_fields=["id", "emp_lob_num", "emp_name", "password", "create_time", "update_time"],
            limit=1000  # 限制查询数量
        )


        logger.info(f"👥 查询到 {len(result)} 条用户记录")

        # 打印数据
        if result:
            print("\n" + "=" * 90)
            print("👤 用户数据列表")
            print("=" * 90)

            for i, user in enumerate(result, 1):
                print(f"\n🔹 用户 #{i}")
                print(f"   📍 ID: {user.get('id', 'N/A')}")
                print(f"   🔢 工号: {user.get('emp_lob_num', 'N/A')}")
                print(f"   👤 姓名: {user.get('emp_name', 'N/A')}")
                print(f"   🔐 密码: {user.get('password', 'N/A')}")
                print(f"   📅 创建时间: {user.get('create_time', 'N/A')}")
                print(f"   🔄 更新时间: {user.get('update_time', 'N/A')}")
                print("-" * 70)

        else:
            print("❌ 没有找到任何用户记录")

        disconnect_milvus()
        return result

    except Exception as e:
        logger.error(f"查询用户数据失败：{str(e)}")
        disconnect_milvus()
        return []


def test_user_count():
    """测试用户数量统计"""
    try:
        if not connect_milvus():
            return

        collection = Collection("sys_kb_user")
        collection.load()

        # 获取实体总数
        count = collection.num_entities
        print(f"\n📊 实体总数: {count}")

        disconnect_milvus()

    except Exception as e:
        logger.error(f"用户数量统计失败：{str(e)}")
        disconnect_milvus()


def main():
    """主函数"""
    print("🚀 开始查询 sys_kb_user 数据集所有信息")
    print("=" * 70)

    # 查询所有用户数据
    users = query_all_users()

    # 测试用户数量统计
    test_user_count()

    # 汇总信息
    print("\n" + "=" * 70)
    print("📋 查询结果汇总")
    print("=" * 70)
    print(f"✅ 总用户数: {len(users)}")
    print(f"✅ 查询完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if users:
        print("✅ 数据查询成功，所有用户记录已完整显示")
    else:
        print("⚠️  未找到任何用户记录")


if __name__ == "__main__":
    main()