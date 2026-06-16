#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查svc_bk_file_vector_chunks分片数据集内容
"""

from pymilvus import connections, utility, Collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_chunks_collection():
    """检查分片数据集内容"""
    try:
        # 连接Milvus
        connections.connect(alias="default", host="localhost", port="19530")
        logger.info("✅ Milvus连接成功")
        
        # 检查集合是否存在
        collections = utility.list_collections()
        logger.info(f"📊 现有集合: {collections}")
        
        if "svc_bk_file_vector_chunks" not in collections:
            logger.error("❌ svc_bk_file_vector_chunks集合不存在")
            return False
        
        # 获取集合信息
        collection = Collection("svc_bk_file_vector_chunks")
        collection.load()
        
        # 检查集合中的文档数量
        num_entities = collection.num_entities
        logger.info(f"📄 集合中的分片数量: {num_entities}")
        
        # 检查集合schema
        schema = collection.schema
        logger.info("🔍 集合字段结构 (共{}个字段):".format(len(schema.fields)))
        for i, field in enumerate(schema.fields):
            logger.info(f"  {i+1}. {field.name}: {field.dtype} (max_length: {field.max_length})")
        
        if num_entities == 0:
            logger.warning("⚠️ 集合为空，没有分片记录")
            return False
        
        # 查询所有记录
        logger.info("📋 查询集合中的所有分片记录 (最多显示10条):")
        results = collection.query(
            expr="", 
            output_fields=["chunk_id", "document_id", "chunk_index", "chunk_content", "create_time"],
            limit=min(10, num_entities)
        )
        
        logger.info(f"📊 实际查询到 {len(results)} 条分片记录:")
        for i, record in enumerate(results):
            logger.info(f"\n  {i+1}. 分片详情:")
            logger.info(f"     分片ID: {record.get('chunk_id', 'N/A')}")
            logger.info(f"     文档ID: {record.get('document_id', 'N/A')}")
            logger.info(f"     分片索引: {record.get('chunk_index', 'N/A')}")
            logger.info(f"     创建时间: {record.get('create_time', 'N/A')}")
            
            # 显示分片内容（截断显示）
            chunk_content = record.get('chunk_content', '')
            if chunk_content:
                preview = chunk_content[:100] + "..." if len(chunk_content) > 100 else chunk_content
                logger.info(f"     分片内容: {preview}")
            else:
                logger.info(f"     分片内容: 空")
            
            logger.info(f"     {'-'*50}")
        
        # 按文档ID分组统计
        logger.info("\n📊 按文档ID统计分片数量:")
        
        # 获取所有文档ID
        all_results = collection.query(
            expr="", 
            output_fields=["document_id"],
            limit=num_entities
        )
        
        from collections import Counter
        doc_counter = Counter([record['document_id'] for record in all_results])
        
        for doc_id, count in doc_counter.most_common():
            logger.info(f"  文档ID: {doc_id} -> 分片数量: {count}")
        
        # 检查特定文档的分片
        if doc_counter:
            sample_doc_id = list(doc_counter.keys())[0]
            logger.info(f"\n🔍 检查文档 {sample_doc_id} 的分片详情:")
            
            doc_chunks = collection.query(
                expr=f'document_id == "{sample_doc_id}"', 
                output_fields=["chunk_id", "chunk_index", "chunk_content"],
                limit=5
            )
            
            for i, chunk in enumerate(doc_chunks):
                logger.info(f"  {i+1}. 分片索引: {chunk['chunk_index']}")
                content_preview = chunk['chunk_content'][:50] + "..." if len(chunk['chunk_content']) > 50 else chunk['chunk_content']
                logger.info(f"     内容预览: {content_preview}")
        
        connections.disconnect("default")
        return True
        
    except Exception as e:
        logger.error(f"❌ 检查分片集合失败: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return False

def diagnose_chunks_issue():
    """诊断分片数据问题"""
    logger.info("🔍 开始诊断分片数据集...")
    
    # 检查集合内容
    if not check_chunks_collection():
        logger.info("\n💡 诊断结果:")
        logger.info("1. 分片集合为空或分片未保存成功")
        logger.info("2. 可能的原因:")
        logger.info("   - 文档处理流程在分片保存阶段中断")
        logger.info("   - 分片数据字段不匹配")
        logger.info("   - 向量化过程失败")
        logger.info("   - 元数据保存成功但分片保存失败")
        logger.info("\n🔧 建议解决方案:")
        logger.info("1. 检查services/document_processor.py中的save_document_chunks方法")
        logger.info("2. 验证分片数据集的字段结构")
        logger.info("3. 检查BGE-M3模型是否正常加载")
        logger.info("4. 重新运行test_document_processor.py验证分片功能")
    else:
        logger.info("\n✅ 诊断结果: 分片数据保存正常")

if __name__ == "__main__":
    diagnose_chunks_issue()