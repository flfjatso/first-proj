#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件命名格式
"""

import os
from werkzeug.utils import secure_filename
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_filename_format():
    """测试文件命名格式"""
    
    # 测试用例
    test_cases = [
        {
            "original_filename": "OP20250708B0012-贵阳电信融合通信abc-标书.docx",
            "opportunity_number": "OP20250708B0012",
            "description": "中文文件名测试"
        },
        {
            "original_filename": "test document.pdf",
            "opportunity_number": "TEST-001",
            "description": "英文文件名测试"
        },
        {
            "original_filename": "文件 名称/测试.docx",
            "opportunity_number": "OP/2024/001",
            "description": "特殊字符测试"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n🔍 测试用例 {i}: {test_case['description']}")
        
        original_filename = test_case["original_filename"]
        opportunity_number = test_case["opportunity_number"]
        
        # 模拟实际的文件保存逻辑
        filename = secure_filename(original_filename)
        file_uuid = str(uuid.uuid4())
        opportunity_number_clean = opportunity_number.replace(" ", "_").replace("/", "-")
        new_filename = f"{file_uuid}_{opportunity_number_clean}_{filename}"
        
        logger.info(f"   原始文件名: {original_filename}")
        logger.info(f"   secure_filename后: {filename}")
        logger.info(f"   商机编号: {opportunity_number}")
        logger.info(f"   清理后商机编号: {opportunity_number_clean}")
        logger.info(f"   UUID: {file_uuid}")
        logger.info(f"   最终文件名: {new_filename}")
        logger.info(f"   文件长度: {len(new_filename)} 字符")
        
        # 检查文件名是否过长
        if len(new_filename) > 255:
            logger.warning("   ⚠️ 文件名可能过长")
        
        # 检查是否包含非法字符
        illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for char in illegal_chars:
            if char in new_filename:
                logger.warning(f"   ⚠️ 文件名包含非法字符: {char}")

def diagnose_actual_issue():
    """诊断实际的问题"""
    logger.info("\n🔧 诊断实际的文件名问题")
    
    # 分析您提供的实际文件名
    actual_filename = "OP20250708B0012-abc-.docx"
    expected_format = "uuid_OP20250708B0012_OP20250708B0012-贵阳电信融合通信abc-标书.docx"
    
    logger.info(f"实际文件名: {actual_filename}")
    logger.info(f"期望格式: {expected_format}")
    
    # 分析差异
    if "uuid_" not in actual_filename:
        logger.error("❌ 实际文件名缺少UUID前缀")
    
    if "OP20250708B0012_" not in actual_filename:
        logger.error("❌ 实际文件名缺少商机编号")
    
    if "贵阳电信融合通信abc-标书" not in actual_filename:
        logger.warning("⚠️ 实际文件名缺少中文部分")
        
        # 测试secure_filename对中文的处理
        test_filename = "OP20250708B0012-贵阳电信融合通信abc-标书.docx"
        secured = secure_filename(test_filename)
        logger.info(f"secure_filename测试: '{test_filename}' -> '{secured}'")

if __name__ == "__main__":
    logger.info("🔍 开始测试文件命名格式...")
    test_filename_format()
    diagnose_actual_issue()
    
    logger.info("\n💡 建议:")
    logger.info("1. 检查Flask服务器是否重启加载了最新代码")
    logger.info("2. 检查文件保存路径是否使用了新格式")
    logger.info("3. 如果secure_filename过滤了中文，可能需要自定义文件名处理")