#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Milvus连接和集合创建
"""

from pymilvus import connections, utility, Collection, DataType
from pymilvus import FieldSchema, CollectionSchema
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_milvus_connection():
    """测试Milvus连接"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host="localhost", port="19530")
        logger.info("✅ Milvus连接成功")

        # 检查现有集合
        collections = utility.list_collections()
        logger.info(f"📊 现有集合: {collections}")

        # 检查svc_bk_file_metadata是否存在
        if "svc_bk_file_metadata" in collections:
            logger.info("✅ svc_bk_file_metadata集合已存在")

            # 查询集合中的文档数量
            collection = Collection("svc_bk_file_metadata")
            collection.load()
            num_entities = collection.num_entities
            logger.info(f"📄 集合中的文档数量: {num_entities}")

            # 查询前几条记录
            if num_entities > 0:
                results = collection.query(
                    expr="",
                    output_fields=["original_filename", "upload_time", "opportunity_number"],
                    limit=5
                )
                logger.info("📋 前5条记录:")
                for i, record in enumerate(results):
                    logger.info(f"  {i + 1}. {record}")
        else:
            logger.warning("⚠️ svc_bk_file_metadata集合不存在")

            # 尝试创建集合（已修复，虚拟向量维度为2）
            try:
                fields = [
                    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=36),
                    FieldSchema(name="bk_en_name", dtype=DataType.VARCHAR, max_length=100),
                    FieldSchema(name="opportunity_number", dtype=DataType.VARCHAR, max_length=50),
                    FieldSchema(name="original_filename", dtype=DataType.VARCHAR, max_length=255),
                    FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=500),
                    FieldSchema(name="file_type", dtype=DataType.VARCHAR, max_length=10),
                    FieldSchema(name="file_size", dtype=DataType.INT64),
                    FieldSchema(name="upload_time", dtype=DataType.VARCHAR, max_length=20),
                    FieldSchema(name="update_time", dtype=DataType.VARCHAR, max_length=20),
                    FieldSchema(name="uploaded_by", dtype=DataType.VARCHAR, max_length=50),
                    FieldSchema(name="kb_document_id", dtype=DataType.VARCHAR, max_length=36),
                    FieldSchema(name="status", dtype=DataType.VARCHAR, max_length=20),
                    FieldSchema(name="vector_dimension", dtype=DataType.INT64),
                    FieldSchema(name="total_chunks", dtype=DataType.INT64),
                    FieldSchema(name="chunk_strategy", dtype=DataType.VARCHAR, max_length=50),
                    FieldSchema(name="error_msg", dtype=DataType.VARCHAR, max_length=500),
                    FieldSchema(name="md5_hash", dtype=DataType.VARCHAR, max_length=32),
                    # 添加虚拟向量字段（维度为2）
                    FieldSchema(name="dummy_vector", dtype=DataType.FLOAT_VECTOR, dim=2),
                ]

                schema = CollectionSchema(fields, description="知识库文档元数据")
                collection = Collection(name="svc_bk_file_metadata", schema=schema)

                # 为虚拟向量字段创建索引
                index_params = {
                    "index_type": "FLAT",
                    "metric_type": "L2",
                    "params": {}
                }
                collection.create_index("dummy_vector", index_params)

                logger.info("✅ 成功创建svc_bk_file_metadata集合")

            except Exception as e:
                logger.error(f"❌ 创建集合失败: {str(e)}")

        connections.disconnect("default")

    except Exception as e:
        logger.error(f"❌ Milvus连接失败: {str(e)}")


if __name__ == "__main__":
    test_milvus_connection()