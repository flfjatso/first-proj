#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import uuid
from datetime import datetime

from pymilvus import connections, Collection, utility

from services.document_processor import DocumentProcessor


def connect_milvus(host: str, port: str) -> None:
    connections.connect(alias="default", host=host, port=port)


def resolve_kb_id(kb_identifier: str) -> str:
    """
    允许传入 bk_id(UUID) 或 bk_en_name。
    返回可用于 DocumentProcessor 的 kb_id（项目现状里实际存入 svc_bk_file_metadata.bk_en_name 字段）。
    """
    if not utility.has_collection("svc_bk_base_info"):
        raise RuntimeError("Milvus 中不存在集合 svc_bk_base_info，请先运行 init_kb_system.py 或在页面创建知识库")

    col = Collection("svc_bk_base_info")
    col.load()

    # 先按 bk_id 匹配
    res = col.query(expr=f"bk_id == '{kb_identifier}'", output_fields=["bk_id", "bk_en_name"], limit=1)
    if res:
        col.release()
        return res[0]["bk_id"]

    # 再按 bk_en_name 匹配
    res = col.query(expr=f"bk_en_name == '{kb_identifier}'", output_fields=["bk_id", "bk_en_name"], limit=1)
    col.release()
    if res:
        return res[0]["bk_id"]

    raise RuntimeError(f"未找到知识库：{kb_identifier}（请传 bk_id 或 bk_en_name）")


def main() -> int:
    parser = argparse.ArgumentParser(description="将 .sql 文件入库到 Milvus 知识库（生成元数据+向量分片）")
    parser.add_argument("--file", required=True, help="SQL 文件路径（例如 C:\\Users\\...\\emp_info_h.sql）")
    parser.add_argument("--kb", required=True, help="知识库 bk_id 或 bk_en_name")
    parser.add_argument("--opportunity", default="emp_info_h", help="商机编号（用于过滤/检索），默认 emp_info_h")
    parser.add_argument("--uploaded-by", default="cli", help="上传人标识，默认 cli")
    parser.add_argument("--milvus-host", default="localhost", help="Milvus host，默认 localhost")
    parser.add_argument("--milvus-port", default="19530", help="Milvus port，默认 19530")
    args = parser.parse_args()

    src_path = os.path.abspath(args.file)
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"文件不存在：{src_path}")

    file_ext = os.path.splitext(src_path)[1].lower().lstrip(".")
    if file_ext != "sql":
        raise ValueError(f"仅支持 .sql 文件，本次输入为 .{file_ext}")

    # 连接 Milvus，并解析知识库
    connect_milvus(args.milvus_host, args.milvus_port)
    kb_id = resolve_kb_id(args.kb)

    # 按 web 端一致的命名规则落盘到 uploads/uploads_original
    upload_dir = os.path.join(os.path.dirname(__file__), "uploads", "uploads_original")
    os.makedirs(upload_dir, exist_ok=True)

    original_filename = os.path.basename(src_path)
    file_uuid = str(uuid.uuid4())
    opportunity_clean = args.opportunity.replace(" ", "_").replace("/", "-")
    new_filename = f"{file_uuid}_{opportunity_clean}_{original_filename}"
    dst_path = os.path.join(upload_dir, new_filename)

    # 复制（避免移动原文件）
    with open(src_path, "rb") as rf, open(dst_path, "wb") as wf:
        wf.write(rf.read())

    # 入库（document_id 使用 file_uuid，便于与落盘文件名关联）
    processor = DocumentProcessor()
    result = processor.process_document(
        dst_path,
        kb_id,
        args.opportunity,
        original_filename,
        args.uploaded_by,
        document_id=file_uuid,
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] 入库结果: {result}")

    if not result.get("success"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

