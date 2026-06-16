#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文档上传功能
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.document_processor import DocumentProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_document_processor():
    """测试文档处理器"""
    try:
        processor = DocumentProcessor()

        # 测试集合创建
        if processor.create_metadata_collection():
            logger.info("✅ 元数据集合创建成功")
        else:
            logger.error("❌ 元数据集合创建失败")

        if processor.create_chunks_collection():
            logger.info("✅ 分片集合创建成功")
        else:
            logger.error("❌ 分片集合创建失败")

    except Exception as e:
        logger.error(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_document_processor()