#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理 svc_bk_file_metadata 数据集索引
删除无用索引，创建指定字段索引
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

def manage_svc_bk_file_metadata_indexes():
    """管理 svc_bk_file_metadata 数据集索引"""
    try:
        if not utility.has_collection("svc_bk_file_metadata"):
            logger.error("❌ 集合 svc_bk_file_metadata 不存在")
            return
        
        collection = Collection("svc_bk_file_metadata")
        
        # 获取当前所有索引
        logger.info("🔍 获取当前索引信息...")
        indexes = collection.indexes
        
        if indexes:
            logger.info(f"📊 当前存在 {len(indexes)} 个索引:")
            for i, index in enumerate(indexes):
                # 使用正确的属性名称
                field_name = getattr(index, 'field_name', 'unknown')
                index_type = getattr(index, 'index_type', getattr(index, 'params', {}).get('index_type', 'unknown'))
                logger.info(f"  索引{i+1}: 字段={field_name}, 类型={index_type}")
        else:
            logger.info("ℹ️ 当前没有索引")
        
        # 删除无用索引（保留指定字段的索引）
        target_fields = ["bk_en_name", "opportunity_number", "original_filename"]
        indexes_to_keep = []
        indexes_to_delete = []
        
        # 检查集合是否有向量字段需要保留索引
        schema = collection.schema
        vector_fields = []
        for field in schema.fields:
            if field.dtype in [101, 100]:  # FLOAT_VECTOR or BINARY_VECTOR
                vector_fields.append(field.name)
        
        for index in indexes:
            field_name = getattr(index, 'field_name', 'unknown')
            
            # 保留向量字段的索引（即使不在target_fields中）
            if field_name in target_fields or field_name in vector_fields:
                indexes_to_keep.append(index)
            else:
                indexes_to_delete.append(index)
        
        # 删除无用索引
        if indexes_to_delete:
            logger.info("🗑️ 开始删除无用索引...")
            for index in indexes_to_delete:
                field_name = getattr(index, 'field_name', 'unknown')
                index_type = getattr(index, 'index_type', getattr(index, 'params', {}).get('index_type', 'unknown'))
                logger.info(f"  删除索引: 字段={field_name}, 类型={index_type}")
                
                # 使用正确的drop_index方法参数
                try:
                    # 方法1：直接使用字段名
                    collection.drop_index(field_name=field_name)
                except Exception as e1:
                    try:
                        # 方法2：使用索引名称
                        index_name = getattr(index, 'index_name', f"{field_name}_index")
                        collection.drop_index(index_name=index_name)
                    except Exception as e2:
                        try:
                            # 方法3：使用默认参数
                            collection.drop_index(field_name)
                        except Exception as e3:
                            logger.error(f"❌ 删除索引失败: {str(e3)}")
                            continue
                
            logger.info("✅ 无用索引删除完成")
        else:
            logger.info("ℹ️ 没有需要删除的无用索引")
        
        # 确保向量字段有索引
        logger.info("🔧 检查向量字段索引...")
        for vector_field in vector_fields:
            field_has_index = False
            for index in indexes_to_keep:
                existing_field_name = getattr(index, 'field_name', 'unknown')
                if existing_field_name == vector_field:
                    field_has_index = True
                    logger.info(f"✅ 向量字段 {vector_field} 已有索引")
                    break
            
            if not field_has_index:
                logger.info(f"🔧 为向量字段 {vector_field} 创建索引...")
                try:
                    index_params = {
                        "index_type": "IVF_FLAT",
                        "metric_type": "L2",
                        "params": {"nlist": 128}
                    }
                    collection.create_index(vector_field, index_params)
                    logger.info(f"✅ 向量字段 {vector_field} 索引创建成功")
                except Exception as e:
                    logger.error(f"❌ 向量字段 {vector_field} 索引创建失败: {str(e)}")
        
        # 创建指定字段索引
        logger.info("🔧 创建指定字段索引...")
        
        # 检查字段是否存在
        schema = collection.schema
        existing_fields = [field.name for field in schema.fields]
        
        for field_name in target_fields:
            if field_name not in existing_fields:
                logger.warning(f"⚠️ 字段不存在: {field_name}")
                continue
            
            # 检查是否已存在该字段的索引
            field_has_index = False
            for index in indexes_to_keep:
                existing_field_name = getattr(index, 'field_name', getattr(index, 'field_name', 'unknown'))
                if existing_field_name == field_name:
                    field_has_index = True
                    logger.info(f"✅ 字段 {field_name} 已有索引，跳过创建")
                    break
            
            if not field_has_index:
                logger.info(f"🔧 为字段 {field_name} 创建索引...")
                try:
                    # 为字符串字段创建索引
                    index_params = {
                        "index_type": "Trie",  # 适合字符串字段的索引类型
                        "metric_type": "HAMMING"  # 字符串字段使用HAMMING距离
                    }
                    collection.create_index(field_name, index_params)
                    logger.info(f"✅ 字段 {field_name} 索引创建成功")
                except Exception as e:
                    logger.error(f"❌ 字段 {field_name} 索引创建失败: {str(e)}")
        
        # 重新加载集合
        logger.info("🔄 重新加载集合...")
        collection.load()
        
        # 验证最终索引状态
        logger.info("🔍 验证最终索引状态...")
        final_indexes = collection.indexes
        
        if final_indexes:
            logger.info(f"📊 最终索引状态 ({len(final_indexes)} 个索引):")
            for i, index in enumerate(final_indexes):
                field_name = getattr(index, 'field_name', getattr(index, 'field_name', 'unknown'))
                index_type = getattr(index, 'index_type', getattr(index, 'params', {}).get('index_type', 'unknown'))
                logger.info(f"  索引{i+1}: 字段={field_name}, 类型={index_type}")
        else:
            logger.info("ℹ️ 最终没有索引")
        
        collection.release()
        logger.info("✅ 索引管理完成")
        
    except Exception as e:
        logger.error(f"❌ 索引管理失败: {str(e)}")

def main():
    """主函数"""
    logger.info("🚀 开始管理 svc_bk_file_metadata 数据集索引...")
    
    # 连接Milvus
    if not connect_milvus():
        logger.error("❌ 无法连接Milvus，退出")
        return
    
    # 管理索引
    manage_svc_bk_file_metadata_indexes()

if __name__ == "__main__":
    main()