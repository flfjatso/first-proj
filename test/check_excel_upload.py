#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Excel文件上传问题诊断脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from services.document_processor import DocumentProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_excel_dependencies():
    """检查Excel处理依赖包"""
    logger.info("🔍 检查Excel处理依赖包...")
    
    try:
        import openpyxl
        logger.info("✅ openpyxl已安装 (版本: %s)", openpyxl.__version__)
    except ImportError:
        logger.error("❌ openpyxl未安装，无法处理.xlsx文件")
        logger.info("💡 请执行: pip install openpyxl")
    
    try:
        import xlrd
        logger.info("✅ xlrd已安装 (版本: %s)", xlrd.__version__)
    except ImportError:
        logger.error("❌ xlrd未安装，无法处理.xls文件")
        logger.info("💡 请执行: pip install xlrd==1.2.0")

def test_excel_extraction():
    """测试Excel文件文本提取功能"""
    logger.info("\n🔍 测试Excel文件文本提取功能...")
    
    processor = DocumentProcessor()
    
    # 创建一个测试Excel文件
    test_file_path = "test_excel.xlsx"
    
    try:
        import openpyxl
        
        # 创建测试Excel文件
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "测试工作表"
        
        # 添加测试数据
        sheet['A1'] = "项目名称"
        sheet['B1'] = "项目编号"
        sheet['A2'] = "OP20251208I0003-项目资金计划"
        sheet['B2'] = "OP20251208I0003"
        sheet['A3'] = "这是一个测试Excel文件"
        sheet['B3'] = "用于验证Excel处理功能"
        
        workbook.save(test_file_path)
        logger.info("✅ 创建测试Excel文件: %s", test_file_path)
        
        # 测试文本提取
        logger.info("📄 测试Excel文本提取...")
        text = processor.extract_text_from_xlsx(test_file_path)
        
        if text:
            logger.info("✅ Excel文本提取成功")
            logger.info("📊 提取内容长度: %d 字符", len(text))
            logger.info("📋 提取内容预览: %s", text[:200] + "..." if len(text) > 200 else text)
        else:
            logger.error("❌ Excel文本提取失败，内容为空")
            
    except Exception as e:
        logger.error("❌ Excel处理测试失败: %s", str(e))
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            logger.info("🧹 清理测试文件")

def check_upload_environment():
    """检查上传环境配置"""
    logger.info("\n🔍 检查上传环境配置...")
    
    # 检查上传目录
    upload_dir = "uploads/uploads_original"
    if os.path.exists(upload_dir):
        logger.info("✅ 上传目录存在: %s", upload_dir)
    else:
        logger.warning("⚠️ 上传目录不存在: %s", upload_dir)
        logger.info("💡 系统会自动创建该目录")
    
    # 检查Milvus连接
    try:
        from pymilvus import connections, utility
        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )
        logger.info("✅ Milvus连接成功")
        
        # 检查必要集合是否存在
        required_collections = ["svc_bk_file_metadata", "svc_bk_file_vector_chunks"]
        for collection_name in required_collections:
            if utility.has_collection(collection_name):
                logger.info("✅ 集合存在: %s", collection_name)
            else:
                logger.warning("⚠️ 集合不存在: %s", collection_name)
                
    except Exception as e:
        logger.error("❌ Milvus检查失败: %s", str(e))

def main():
    """主函数"""
    logger.info("🚀 开始检查Excel文件上传问题...")
    
    # 检查依赖包
    check_excel_dependencies()
    
    # 测试Excel提取功能
    test_excel_extraction()
    
    # 检查上传环境
    check_upload_environment()
    
    logger.info("\n📋 诊断完成，请根据以上信息解决问题")

if __name__ == "__main__":
    main()