#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档处理器诊断脚本
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
        logger.info("🔍 开始测试文档处理器...")
        
        # 创建处理器实例
        processor = DocumentProcessor()
        
        # 测试集合创建
        logger.info("📊 测试元数据集合创建...")
        if processor.create_metadata_collection():
            logger.info("✅ 元数据集合创建成功")
        else:
            logger.error("❌ 元数据集合创建失败")
            return False
            
        logger.info("📊 测试分片集合创建...")
        if processor.create_chunks_collection():
            logger.info("✅ 分片集合创建成功")
        else:
            logger.error("❌ 分片集合创建失败")
            return False
        
        # 测试文本提取
        logger.info("📄 测试文本提取功能...")
        
        success = False
        test_file_path = None
        
        # 测试实际DOCX文件
        docx_file_path = r"D:\workspace_python\知识库文档\OP20250708B0010-贵阳电信融合通信-标书.docx"
        
        if os.path.exists(docx_file_path):
            logger.info("📄 测试实际DOCX文件...")
            
            try:
                # 测试DOCX文本提取
                extracted_text = processor.extract_text_from_docx(docx_file_path)
                logger.info(f"✅ DOCX文本提取成功，内容长度: {len(extracted_text)}")
                
                if extracted_text:
                    # 测试文本分片
                    chunks = processor.chunk_text(extracted_text)
                    logger.info(f"✅ 文本分片成功，分片数量: {len(chunks)}")
                    
                    # 测试向量化
                    if processor.tokenizer and processor.model:
                        embedding = processor.get_text_embedding("测试文本")
                        logger.info(f"✅ 向量化成功，向量维度: {len(embedding)}")
                    else:
                        logger.warning("⚠️ 模型未加载，跳过向量化测试")
                    
                    # 测试完整文档处理流程
                    logger.info("🔄 测试完整文档处理流程...")
                    success = processor.process_document(
                        docx_file_path,
                        "test_kb",
                        "TEST-001",
                        "OP20250708B0010-贵阳电信融合通信-标书.docx",
                        "test_user"
                    )
                else:
                    logger.error("❌ DOCX文本提取失败，内容为空")
                    
            except Exception as e:
                import traceback
                logger.error(f"❌ DOCX文件处理失败: {str(e)}")
                logger.error(f"详细错误信息: {traceback.format_exc()}")
        else:
            logger.warning("⚠️ 实际DOCX文件不存在，使用测试文件")
            
            # 创建一个测试文件
            test_content = "这是一个测试文档内容，用于验证文档处理器的功能。"
            test_file_path = "test_document.txt"
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            try:
                # 测试文本提取
                extracted_text = processor.extract_text_from_txt(test_file_path)
                logger.info(f"✅ 文本提取成功，内容长度: {len(extracted_text)}")
                
                # 测试文本分片
                chunks = processor.chunk_text(extracted_text)
                logger.info(f"✅ 文本分片成功，分片数量: {len(chunks)}")
                
                # 测试向量化
                if processor.tokenizer and processor.model:
                    embedding = processor.get_text_embedding("测试文本")
                    logger.info(f"✅ 向量化成功，向量维度: {len(embedding)}")
                else:
                    logger.warning("⚠️ 模型未加载，跳过向量化测试")
                
                # 测试完整文档处理流程
                logger.info("🔄 测试完整文档处理流程...")
                success = processor.process_document(
                    test_file_path,
                    "test_kb",
                    "TEST-001",
                    "test_document.txt",
                    "test_user"
                )
                
            except Exception as e:
                import traceback
                logger.error(f"❌ 测试文件处理失败: {str(e)}")
                logger.error(f"详细错误信息: {traceback.format_exc()}")
            finally:
                # 清理测试文件
                if test_file_path and os.path.exists(test_file_path):
                    os.remove(test_file_path)
        
        if success:
            logger.info("✅ 完整文档处理流程成功")
        else:
            logger.error("❌ 完整文档处理流程失败")
        
        logger.info("🎉 文档处理器测试完成")
        return success
        
    except Exception as e:
        import traceback
        logger.error(f"❌ 测试失败: {str(e)}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_document_processor()