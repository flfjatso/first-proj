#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查svc_bk_file_metadata数据一致性
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

def check_svc_bk_file_metadata():
    """检查svc_bk_file_metadata数据一致性"""
    try:
        if not utility.has_collection("svc_bk_file_metadata"):
            logger.error("❌ 集合 svc_bk_file_metadata 不存在")
            return
        
        collection = Collection("svc_bk_file_metadata")
        collection.load()
        
        # 方法1：使用num_entities
        num_entities = collection.num_entities
        logger.info(f"📊 num_entities统计: {num_entities} 条")
        
        # 方法2：使用query查询所有数据
        results = collection.query(expr="id like '%'", output_fields=["*"])
        query_count = len(results)
        logger.info(f"📊 query查询统计: {query_count} 条")
        
        # 分析数据
        logger.info("🔍 分析数据内容...")
        
        # 按文件名分组，检查重复
        filename_groups = {}
        for result in results:
            filename = result.get('original_filename')
            if filename not in filename_groups:
                filename_groups[filename] = []
            filename_groups[filename].append(result)
        
        logger.info(f"📋 按文件名分组: {len(filename_groups)} 个唯一文件")
        
        for filename, records in filename_groups.items():
            logger.info(f"  文件: {filename} -> 记录数: {len(records)}")
            for i, record in enumerate(records):
                logger.info(f"    记录{i+1}: id={record.get('id')}, status={record.get('status')}")
        
        # 按状态分组
        status_groups = {}
        for result in results:
            status = result.get('status', 'unknown')
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(result)
        
        logger.info("📋 按状态分组:")
        for status, records in status_groups.items():
            logger.info(f"  状态: {status} -> 记录数: {len(records)}")
        
        # 检查重复ID
        ids = [result.get('id') for result in results]
        unique_ids = set(ids)
        if len(ids) != len(unique_ids):
            logger.warning(f"⚠️ 存在重复ID: 总ID数={len(ids)}, 唯一ID数={len(unique_ids)}")
        else:
            logger.info("✅ 所有ID都是唯一的")
        
        # 差异分析
        if num_entities != query_count:
            logger.warning(f"⚠️ 数据统计不一致: num_entities={num_entities}, query_count={query_count}")
            logger.info("💡 可能原因: 存在已删除但未清理的数据")
        else:
            logger.info("✅ 数据统计一致")
        
        # 检查实际文件数与预期的差异
        expected_count = 2  # 用户预期上传了2个文件
        actual_unique_files = len(filename_groups)
        
        if actual_unique_files != expected_count:
            logger.warning(f"⚠️ 文件数量不一致: 预期={expected_count}, 实际唯一文件数={actual_unique_files}")
        else:
            logger.info(f"✅ 文件数量一致: 预期={expected_count}, 实际唯一文件数={actual_unique_files}")
        
        return num_entities, query_count, filename_groups
        
    except Exception as e:
        logger.error(f"❌ 检查 svc_bk_file_metadata 失败: {str(e)}")
        return None, None, None

def main():
    """主函数"""
    logger.info("🚀 开始检查 svc_bk_file_metadata 数据一致性...")
    
    # 连接Milvus
    if not connect_milvus():
        logger.error("❌ 无法连接Milvus，退出")
        return
    
    # 检查数据
    check_svc_bk_file_metadata()

if __name__ == "__main__":
    main()