#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查svc_bk_file_metadata元数据数据集内容
"""

from pymilvus import connections, utility, Collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_metadata_collection():
    """检查元数据数据集内容"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host="localhost", port="19530")
        logger.info("✅ Milvus连接成功")
        
        # 检查集合是否存在
        collections = utility.list_collections()
        logger.info(f"📊 现有集合: {collections}")
        
        if "svc_bk_file_metadata" not in collections:
            logger.error("❌ svc_bk_file_metadata集合不存在")
            return False
        
        # 获取集合信息
        collection = Collection("svc_bk_file_metadata")
        
        # 尝试加载集合（检查索引状态）
        try:
            collection.load()
            logger.info("✅ 集合加载成功")
        except Exception as e:
            logger.error(f"❌ 集合加载失败: {str(e)}")
            logger.info("💡 可能需要为向量字段创建索引")
            return False
        
        # 检查集合中的文档数量
        num_entities = collection.num_entities
        logger.info(f"📄 集合中的文档数量: {num_entities}")
        
        # 检查集合schema
        schema = collection.schema
        logger.info("🔍 集合字段结构 (共{}个字段):".format(len(schema.fields)))
        for i, field in enumerate(schema.fields):
            logger.info(f"  {i+1}. {field.name}: {field.dtype} (max_length: {field.max_length})")
        
        if num_entities == 0:
            logger.warning("⚠️ 集合为空，没有文档记录")
            return False
        
        # 查询所有记录
        logger.info("📋 查询集合中的所有文档记录 (最多显示10条):")
        results = collection.query(
            expr="", 
            output_fields=["id","kb_document_id","vector_dimension","total_chunks","chunk_strategy","error_msg","md5_hash","original_filename", "opportunity_number", "bk_en_name","file_path", "file_type", "file_size", "upload_time","update_time","uploaded_by", "status","dummy_vector"],

            limit=min(10, num_entities)
        )
        
        logger.info(f"📊 实际查询到 {len(results)} 条文档记录:")
        for i, record in enumerate(results):
            logger.info(f"\n  {i+1}. 文档详情:")
            logger.info(f"     文档ID: {record.get('id', 'N/A')}")
            logger.info(f"     文件名: {record.get('original_filename', 'N/A')}")
            logger.info(f"     商机编号: {record.get('opportunity_number', 'N/A')}")
            logger.info(f"     知识库: {record.get('bk_en_name', 'N/A')}")
            logger.info(f"     文件类型: {record.get('file_type', 'N/A')}")
            logger.info(f"     文件大小: {record.get('file_size', 'N/A')} bytes")
            logger.info(f"     上传时间: {record.get('upload_time', 'N/A')}")
            logger.info(f"     上传用户: {record.get('uploaded_by', 'N/A')}")
            logger.info(f"     状态: {record.get('status', 'N/A')}")
            logger.info(f"     文件路径: {record.get('file_path', 'N/A')}")
            logger.info(f"     {'-'*50}")
        
        # 按知识库分组统计
        logger.info("\n📊 按知识库统计文档数量:")
        
        # 获取所有记录用于统计
        all_results = collection.query(
            expr="", 
            output_fields=["bk_en_name", "opportunity_number"],
            limit=num_entities
        )
        
        from collections import Counter
        
        # 按知识库分组统计
        kb_counter = Counter([record['bk_en_name'] for record in all_results])
        
        for kb_name, count in kb_counter.most_common():
            logger.info(f"  知识库: {kb_name} -> 文档数量: {count}")
        
        # 按商机编号统计
        logger.info("\n📊 按商机编号统计:")
        opp_counter = Counter([record['opportunity_number'] for record in all_results])
        
        for opp_num, count in opp_counter.most_common():
            logger.info(f"  商机编号: {opp_num} -> 文档数量: {count}")
        
        # 检查特定文件是否存在
        target_filenames = [
            "OP20250708B0010-贵阳电信融合通信-标书.docx"
        ]
        
        for target_filename in target_filenames:
            logger.info(f"\n🔍 检查特定文件是否在集合中: {target_filename}")
            
            specific_results = collection.query(
                expr=f'original_filename == "{target_filename}"', 
                output_fields=["id", "original_filename", "opportunity_number", "upload_time", "status","file_path"]
            )
            
            if specific_results:
                logger.info("✅ 文件已成功保存到集合中")
                for record in specific_results:
                    logger.info(f"   文档ID: {record['id']}")
                    logger.info(f"   文件名: {record['original_filename']}")
                    logger.info(f"   商机编号: {record['opportunity_number']}")
                    logger.info(f"   上传时间: {record['upload_time']}")
                    logger.info(f"   状态: {record['status']}")
                    logger.info(f"   文件路径: {record['file_path']}")

            else:
                logger.warning("⚠️ 文件未在集合中找到")
        
        connections.disconnect("default")
        return True
        
    except Exception as e:
        logger.error(f"❌ 检查元数据集合失败: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return False

def diagnose_metadata_issue():
    """诊断元数据问题"""
    logger.info("🔍 开始诊断元数据数据集...")
    
    # 检查集合内容
    if not check_metadata_collection():
        logger.info("\n💡 诊断结果:")
        logger.info("1. 元数据集合为空或文档未保存成功")
        logger.info("2. 可能的原因:")
        logger.info("   - 数据字段数量不匹配（expect 20, got 18）")
        logger.info("   - 虚拟向量字段数据未正确添加")
        logger.info("   - 数据插入过程出现异常")
        logger.info("   - 集合缺少索引无法加载")
        logger.info("\n🔧 建议解决方案:")
        logger.info("1. 检查services/document_processor.py中的save_document_metadata方法")
        logger.info("2. 验证数据字段数量是否匹配（20个字段）")
        logger.info("3. 检查RowID和Timestamp字段是否正确添加")
        logger.info("4. 运行索引修复脚本")
    else:
        logger.info("\n✅ 诊断结果: 元数据保存正常")

if __name__ == "__main__":
    diagnose_metadata_issue()