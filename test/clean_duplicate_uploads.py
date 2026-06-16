#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 uploads_original 目录下的重复文件。
规则：文件名格式为 uuid_原始文件名，按原始文件名分组，保留修改时间最新的，删除其余的。
"""

import os
import sys
from collections import defaultdict

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "uploads_original")

def get_original_name(filename):
    """去掉开头的 uuid_ 前缀，返回原始文件名"""
    # uuid 格式：8-4-4-4-12 共36字符，后跟下划线
    if len(filename) > 37 and filename[36] == '_':
        return filename[37:]
    return filename

def clean_duplicates(dry_run=False):
    if not os.path.exists(UPLOAD_DIR):
        print(f"目录不存在: {UPLOAD_DIR}")
        return

    # 按原始文件名分组
    groups = defaultdict(list)
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        orig = get_original_name(fname)
        groups[orig].append(fpath)

    deleted = 0
    for orig_name, paths in groups.items():
        if len(paths) <= 1:
            continue
        # 按修改时间排序，保留最新的
        paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        keep = paths[0]
        remove = paths[1:]
        print(f"\n原始文件名: {orig_name}  共 {len(paths)} 个")
        print(f"  保留: {os.path.basename(keep)}  ({os.path.getmtime(keep):.0f})")
        for p in remove:
            print(f"  删除: {os.path.basename(p)}  ({os.path.getmtime(p):.0f})")
            if not dry_run:
                os.remove(p)
                deleted += 1

    if dry_run:
        print("\n[dry_run 模式，未实际删除，去掉 --dry-run 参数执行真正删除]")
    else:
        print(f"\n✅ 清理完成，共删除 {deleted} 个重复文件")

if __name__ == "__main__":
    dry_run = "--run" not in sys.argv
    clean_duplicates(dry_run=dry_run)
