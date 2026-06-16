from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, Response
import logging
from pymilvus import connections, Collection, utility
from datetime import datetime
import uuid
import os
import json
import requests
from werkzeug.utils import secure_filename
from services.document_processor import DocumentProcessor
from config.settings import (
    MILVUS_HOST, MILVUS_PORT,
    AGENT_API_URL, AGENT_API_KEY, AGENT_MODEL,
    SECRET_KEY, FLASK_HOST, FLASK_PORT
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = SECRET_KEY

def connect_milvus():
    """连接Milvus数据库"""
    try:
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
        return True
    except Exception as e:
        logger.error(f"连接Milvus失败：{str(e)}")
        return False

def disconnect_milvus():
    """断开Milvus连接"""
    try:
        if "default" in connections.list_connections():
            connections.disconnect("default")
    except Exception as e:
        logger.error(f"断开Milvus连接失败：{str(e)}")

def verify_user_login(emp_lob_num, password):
    """验证用户登录"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        # 获取用户集合
        collection = Collection("sys_kb_user")
        collection.load()
        
        # 查询用户
        result = collection.query(
            expr=f"emp_lob_num == '{emp_lob_num}'",
            output_fields=["id", "emp_lob_num", "emp_name", "password"],
            limit=1
        )
        
        if not result:
            return False, "用户不存在"
        
        user = result[0]
        if user.get("password") == password:
            # 更新登录时间
            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 这里可以添加更新时间的逻辑
            
            return True, {
                "id": user.get("id"),
                "emp_lob_num": user.get("emp_lob_num"),
                "emp_name": user.get("emp_name")
            }
        else:
            return False, "密码错误"
            
    except Exception as e:
        logger.error(f"验证用户登录失败：{str(e)}")
        return False, "系统错误"
    finally:
        disconnect_milvus()

@app.route('/')
def index():
    """首页"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        emp_lob_num = request.form.get('emp_lob_num', '').strip()
        password = request.form.get('password', '').strip()
        
        if not emp_lob_num or not password:
            flash('请输入工号和密码', 'error')
            return render_template('login.html')
        
        success, result = verify_user_login(emp_lob_num, password)
        
        if success:
            # 登录成功，设置session
            session['user_id'] = result['id']
            session['emp_lob_num'] = result['emp_lob_num']
            session['emp_name'] = result['emp_name']
            session['logged_in'] = True
            
            flash(f'欢迎回来，{result["emp_name"]}！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result, 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """仪表板页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                         emp_name=session.get('emp_name'),
                         emp_lob_num=session.get('emp_lob_num'))

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('login'))

# 用户管理功能
def get_all_users():
    """获取所有用户"""
    try:
        if not connect_milvus():
            return []
        
        collection = Collection("sys_kb_user")
        collection.load()
        
        result = collection.query(
            expr="",
            output_fields=["id", "emp_lob_num", "emp_name", "password", "create_time"],
            limit=100
        )
        
        disconnect_milvus()
        return result
    except Exception as e:
        logger.error(f"获取用户列表失败：{str(e)}")
        return []

def add_user(emp_lob_num, emp_name, password):
    """添加用户"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        collection = Collection("sys_kb_user")
        collection.load()
        
        # 检查工号是否已存在
        existing = collection.query(
            expr=f"emp_lob_num == '{emp_lob_num}'",
            output_fields=["id"],
            limit=1
        )
        
        if existing:
            disconnect_milvus()
            return False, "工号已存在"
        
        # 插入新用户
        user_id = str(uuid.uuid4())
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        empty_vector = [0.0] * 128
        
        insert_data = [
            [user_id],
            [emp_lob_num],
            [emp_name],
            [password],
            [now],
            [now],
            [empty_vector]
        ]
        
        collection.insert(insert_data)
        collection.flush()
        disconnect_milvus()
        
        return True, "用户添加成功"
    except Exception as e:
        logger.error(f"添加用户失败：{str(e)}")
        return False, "添加用户失败"

def update_user(user_id, emp_lob_num, emp_name, password):
    """更新用户信息"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        collection = Collection("sys_kb_user")
        collection.load()
        
        # 检查工号是否被其他用户使用
        existing = collection.query(
            expr=f"emp_lob_num == '{emp_lob_num}' and id != '{user_id}'",
            output_fields=["id"],
            limit=1
        )
        
        if existing:
            disconnect_milvus()
            return False, "工号已被其他用户使用"
        
        # 更新用户信息
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 由于Milvus不支持直接更新，需要先删除再插入
        collection.delete(expr=f"id == '{user_id}'")
        collection.flush()
        
        insert_data = [
            [user_id],
            [emp_lob_num],
            [emp_name],
            [password],
            [now],  # 保持原创建时间
            [now],  # 更新修改时间
            [[0.0] * 128]  # 空向量
        ]
        
        collection.insert(insert_data)
        collection.flush()
        disconnect_milvus()
        
        return True, "用户更新成功"
    except Exception as e:
        logger.error(f"更新用户失败：{str(e)}")
        return False, "更新用户失败"

def delete_user(user_id):
    """删除用户"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        collection = Collection("sys_kb_user")
        collection.load()
        
        # 删除用户
        collection.delete(expr=f"id == '{user_id}'")
        collection.flush()
        disconnect_milvus()
        
        return True, "用户删除成功"
    except Exception as e:
        logger.error(f"删除用户失败：{str(e)}")
        return False, "删除用户失败"

@app.route('/user_management')
def user_management():
    """用户管理页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    users = get_all_users()
    return render_template('user_management.html', 
                         users=users,
                         emp_name=session.get('emp_name'),
                         emp_lob_num=session.get('emp_lob_num'))

@app.route('/dataset_query')
def dataset_query():
    """数据集查询页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # 连接Milvus
        if not connect_milvus():
            flash("数据库连接失败", "error")
            return render_template('dataset_query.html', 
                                 emp_name=session.get('emp_name'),
                                 emp_lob_num=session.get('emp_lob_num'),
                                 collections=[])
        
        # 获取所有集合
        collections = utility.list_collections()
        
        # 获取每个集合的基本信息
        collection_info = []
        for collection_name in collections:
            try:
                collection = Collection(collection_name)
                
                # 增强集合加载的健壮性 - 完全避免索引检查
                try:
                    # 直接加载集合，不进行任何索引检查
                    collection.load()
                    logger.info(f"✅ 集合 {collection_name} 加载成功")
                except Exception as load_error:
                    logger.warning(f"集合 {collection_name} 加载失败: {str(load_error)}")
                    
                    # 尝试使用num_entities统计
                    try:
                        actual_count = collection.num_entities
                        schema = collection.schema
                        fields = [field.name for field in schema.fields]
                        collection_info.append({
                            'name': collection_name,
                            'count': actual_count,
                            'fields': fields
                        })
                    except Exception as count_error:
                        logger.error(f"获取集合 {collection_name} 基本信息失败: {str(count_error)}")
                        collection_info.append({
                            'name': collection_name,
                            'count': 0,
                            'fields': []
                        })
                    
                    collection.release()
                    continue  # 跳过当前集合的查询操作
                
                # 执行flush操作清理无效数据
                collection.flush()
                
                # 使用query查询实际有效数据量
                try:
                    # 获取集合的主键字段
                    primary_field = None
                    primary_field_type = None
                    
                    for field in collection.schema.fields:
                        if field.is_primary:
                            primary_field = field.name
                            primary_field_type = field.dtype
                            break
                    
                    # 根据主键字段类型构建查询条件
                    if primary_field:
                        # 尝试使用空表达式查询所有数据，添加合法的limit参数
                        try:
                            # 使用合法的limit值（16384以内）
                            results = collection.query(expr="", output_fields=[primary_field], limit=16384)
                            actual_count = len(results)
                        except Exception as e:
                            # 如果查询失败，回退到num_entities
                            logger.error(f"使用limit查询失败: {str(e)}")
                            actual_count = collection.num_entities
                    else:
                        # 没有主键字段，使用num_entities
                        actual_count = collection.num_entities
                except Exception as e:
                    logger.error(f"查询集合 {collection_name} 数据量失败: {str(e)}")
                    # 回退到使用num_entities
                    actual_count = collection.num_entities
                
                schema = collection.schema
                fields = [field.name for field in schema.fields]
                collection_info.append({
                    'name': collection_name,
                    'count': actual_count,
                    'fields': fields
                })
                collection.release()
            except Exception as e:
                logger.error(f"获取集合 {collection_name} 信息失败: {str(e)}")
                collection_info.append({
                    'name': collection_name,
                    'count': 0,
                    'fields': [],
                    'error': str(e)
                })
        
        return render_template('dataset_query.html', 
                             emp_name=session.get('emp_name'),
                             emp_lob_num=session.get('emp_lob_num'),
                             collections=collection_info)
    except Exception as e:
        logger.error(f"数据集查询失败: {str(e)}")
        flash(f"查询失败: {str(e)}", "error")
        return render_template('dataset_query.html', 
                             emp_name=session.get('emp_name'),
                             emp_lob_num=session.get('emp_lob_num'),
                             collections=[])

@app.route('/smart_search')
def smart_search():
    """智能搜索页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    knowledge_bases = get_all_knowledge_bases()

    # 获取所有文件名（带知识库归属）用于前端联动
    filenames_by_kb = {}
    try:
        if connect_milvus():
            if utility.has_collection("svc_bk_file_metadata"):
                col = Collection("svc_bk_file_metadata")
                col.load()
                results = col.query(
                    expr="",
                    output_fields=["original_filename", "opportunity_number", "bk_en_name"],
                    limit=1000
                )
                for r in results:
                    kb = r.get('bk_en_name', '')
                    fname = r.get('original_filename', '')
                    if kb and fname:
                        filenames_by_kb.setdefault(kb, set()).add(fname)
                col.release()
                filenames_by_kb = {k: sorted(list(v)) for k, v in filenames_by_kb.items()}
    except Exception as e:
        logger.error(f"获取文件名列表失败: {str(e)}")

    return render_template('smart_search.html',
                           emp_name=session.get('emp_name'),
                           emp_lob_num=session.get('emp_lob_num'),
                           knowledge_bases=knowledge_bases,
                           filenames_by_kb=filenames_by_kb)

def format_excel_content(content):
    """格式化Excel文档内容，使其更易读"""
    if not content:
        return ""
    
    # 清理多余的空格和换行
    content = content.strip()
    
    # 处理表格数据
    lines = content.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测是否为表格行（包含制表符或逗号分隔）
        if '\t' in line or (',' in line and len(line.split(',')) > 1):
            # 表格数据，添加表格样式
            cells = line.replace('\t', ',').split(',')
            formatted_cells = []
            
            for cell in cells:
                cell = cell.strip()
                if cell:
                    # 数字格式化
                    if cell.replace('.', '').replace('-', '').isdigit():
                        try:
                            num = float(cell)
                            if num >= 10000:
                                cell = f"{num:,.0f}"  # 千分位格式化
                            else:
                                cell = f"{num:.2f}"  # 保留两位小数
                        except:
                            pass
                    formatted_cells.append(f"<span class='excel-cell'>{cell}</span>")
            
            if formatted_cells:
                formatted_lines.append(f"<div class='excel-row'>{''.join(formatted_cells)}</div>")
        else:
            # 普通文本
            formatted_lines.append(f"<div class='excel-text'>{line}</div>")
    
    if formatted_lines:
        return f"<div class='excel-content'>{''.join(formatted_lines)}</div>"
    else:
        return content

@app.route('/api/smart_search', methods=['POST'])
def api_smart_search():
    """智能搜索API接口"""
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    try:
        data = request.get_json()
        filename_with_opp = data.get('filename', '').strip()
        search_text = data.get('search_text', '').strip()
        top_k = data.get('top_k', 10)
        
        if not filename_with_opp:
            return jsonify({"success": False, "message": "请选择文件名"})
        
        if not search_text:
            return jsonify({"success": False, "message": "请输入搜索内容"})
        
        # 从显示名称中提取商机编号和文件名
        opportunity_number = None
        original_filename = None
        
        if '(' in filename_with_opp and ')' in filename_with_opp:
            # 格式：文件名 (商机编号)
            opp_start = filename_with_opp.rfind('(') + 1
            opp_end = filename_with_opp.rfind(')')
            opportunity_number = filename_with_opp[opp_start:opp_end].strip()
            original_filename = filename_with_opp[:opp_start-1].strip()
        else:
            # 如果没有商机编号，使用整个字符串作为文件名
            original_filename = filename_with_opp
            opportunity_number = filename_with_opp
        
        if not opportunity_number:
            return jsonify({"success": False, "message": "无法从文件名中提取商机编号"})
        
        # 连接Milvus
        if not connect_milvus():
            return jsonify({"success": False, "message": "数据库连接失败"})
        
        # 检查集合是否存在
        if not utility.has_collection("svc_bk_file_metadata"):
            return jsonify({"success": False, "message": "文档元数据不存在，请先上传文档"})
        
        if not utility.has_collection("svc_bk_file_vector_chunks"):
            return jsonify({"success": False, "message": "向量库不存在，请先上传文档"})
        
        # 第一步：从svc_bk_file_metadata找到对应的文档ID
        metadata_collection = Collection("svc_bk_file_metadata")
        
        try:
            metadata_collection.load()
            
            # 构建查询表达式 - 优先使用商机编号，其次使用文件名
            search_expr = f"opportunity_number == '{opportunity_number}'"
            
            # 查询文档元数据
            doc_results = metadata_collection.query(
                expr=search_expr,
                output_fields=["*"],
                limit=10  # 限制查询数量
            )
            
            if not doc_results:
                # 如果按商机编号没找到，尝试按文件名搜索
                search_expr = f"original_filename == '{original_filename}'"
                doc_results = metadata_collection.query(
                    expr=search_expr,
                    output_fields=["*"],
                    limit=10
                )
            
            if not doc_results:
                metadata_collection.release()
                return jsonify({
                    "success": False, 
                    "message": f"未找到对应的文档信息，商机编号: {opportunity_number}, 文件名: {original_filename}"
                })
            
            # 获取文档ID列表
            document_ids = [doc["id"] for doc in doc_results]
            logger.info(f"找到 {len(document_ids)} 个相关文档，文档ID: {document_ids}")
            
            metadata_collection.release()
            
        except Exception as meta_error:
            logger.error(f"文档元数据查询失败: {str(meta_error)}")
            metadata_collection.release()
            return jsonify({"success": False, "message": "文档信息查询失败"})
        
        # 第二步：在svc_bk_file_vector_chunks中搜索相似内容
        # 获取文档处理器
        processor = DocumentProcessor()
        
        # 生成搜索文本的向量
        query_vector = processor.get_text_embedding(search_text)
        if query_vector is None:
            return jsonify({"success": False, "message": "向量生成失败"})
        
        # 构建搜索表达式 - 限制在指定的文档ID范围内
        search_expr = f"document_id in {document_ids}"
        
        # 向量相似度搜索
        collection = Collection("svc_bk_file_vector_chunks")
        
        try:
            collection.load()
        except Exception as load_error:
            logger.error(f"集合加载失败: {str(load_error)}")
            return jsonify({"success": False, "message": "向量库加载失败"})
        
        search_params = {
            "metric_type": "L2",  # 修正为L2距离度量
            "params": {"nprobe": 10}
        }
        
        # 进行向量搜索
        try:
            results = collection.search(
                data=[query_vector],
                anns_field="chunk_embedding",  # 修正字段名称
                param=search_params,
                limit=top_k,
                expr=search_expr,
                output_fields=["*"],
                consistency_level="Strong"
            )
        except Exception as search_error:
            logger.error(f"搜索执行失败: {str(search_error)}")
            collection.release()
            return jsonify({"success": False, "message": "搜索执行失败"})
        
        # 处理搜索结果
        search_results = []
        
        # 检查搜索结果是否为空
        if not results or len(results) == 0 or len(results[0]) == 0:
            collection.release()
            return jsonify({
                "success": True,
                "message": "搜索完成，未找到相关结果",
                "results": [],
                "total": 0
            })
        
        # 处理搜索结果
        for i, hit in enumerate(results[0]):
            similarity = 1 - hit.distance  # 余弦相似度
            document_id = hit.entity.get("document_id")
            
            # 查询文档元数据获取详细信息
            if utility.has_collection("svc_bk_file_metadata"):
                metadata_collection = Collection("svc_bk_file_metadata")
                
                try:
                    metadata_collection.load()
                    
                    doc_results = metadata_collection.query(
                        expr=f"id == '{document_id}'",
                        output_fields=["*"],
                        limit=1
                    )
                    
                    if doc_results:
                        doc_info = doc_results[0]
                        # 优化Excel内容的显示
                        chunk_content = hit.entity.get("chunk_content", "")
                        file_extension = doc_info.get("original_filename", "").lower()
                        
                        # 如果是Excel文件，优化内容显示
                        if file_extension.endswith(('.xlsx', '.xls')):
                            # 清理和格式化Excel内容
                            chunk_content = format_excel_content(chunk_content)
                        
                        search_results.append({
                            "rank": i + 1,
                            "similarity": round(similarity, 4),
                            "chunk_id": hit.entity.get("chunk_id"),
                            "document_id": document_id,
                            "filename": doc_info.get("original_filename", ""),
                            "opportunity_number": doc_info.get("opportunity_number", ""),
                            "chunk_content": chunk_content,
                            "chunk_index": hit.entity.get("chunk_index", 0),
                            "upload_time": doc_info.get("upload_time", ""),
                            "file_type": "excel" if file_extension.endswith(('.xlsx', '.xls')) else "other"
                        })
                    
                    metadata_collection.release()
                except Exception as meta_error:
                    logger.error(f"元数据查询失败: {str(meta_error)}")
        
        collection.release()
        
        return jsonify({
            "success": True,
            "message": "搜索成功",
            "results": search_results,
            "total": len(search_results)
        })
        
    except Exception as e:
        logger.error(f"智能搜索失败: {str(e)}")
        return jsonify({"success": False, "message": f"搜索失败: {str(e)}"})


@app.route('/api/smart_search_llm', methods=['POST'])
def api_smart_search_llm():
    """RAG + LLM 流式智能搜索接口，返回 SSE 流"""
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "未登录"}), 401

    data = request.get_json()
    kb_en_name  = data.get('kb_id', '').strip()   # 前端传 bk_id，存在 bk_en_name 字段里
    filename    = data.get('filename', '').strip()   # 可选
    search_text = data.get('search_text', '').strip()
    top_k       = int(data.get('top_k', 5))

    if not kb_en_name:
        return jsonify({"success": False, "message": "请选择知识库"}), 400
    if not search_text:
        return jsonify({"success": False, "message": "请输入搜索内容"}), 400

    # ── 1. RAG 召回 ────────────────────────────────────────────────
    def rag_retrieve():
        try:
            if not connect_milvus():
                return [], "数据库连接失败"
            if not utility.has_collection("svc_bk_file_metadata") or \
               not utility.has_collection("svc_bk_file_vector_chunks"):
                return [], "向量库不存在，请先上传文档"

            meta_col = Collection("svc_bk_file_metadata")
            meta_col.load()

            if filename:
                expr = f'bk_en_name == "{kb_en_name}" && original_filename == "{filename}"'
            else:
                expr = f'bk_en_name == "{kb_en_name}"'

            doc_results = meta_col.query(expr=expr, output_fields=["id"], limit=200)
            meta_col.release()

            if not doc_results:
                return [], "该知识库下未找到文档，请先上传文档"

            document_ids = [d["id"] for d in doc_results]
            processor = DocumentProcessor()
            query_vector = processor.get_text_embedding(search_text)
            if query_vector is None:
                return [], "向量生成失败"

            vec_col = Collection("svc_bk_file_vector_chunks")
            vec_col.load()
            results = vec_col.search(
                data=[query_vector],
                anns_field="chunk_embedding",
                param={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=top_k,
                expr=f"document_id in {document_ids}",
                output_fields=["chunk_content", "chunk_index", "document_id"],
                consistency_level="Strong"
            )
            vec_col.release()

            chunks = []
            if results and len(results[0]) > 0:
                meta_col2 = Collection("svc_bk_file_metadata")
                meta_col2.load()
                for i, hit in enumerate(results[0]):
                    doc_id = hit.entity.get("document_id")
                    doc_info = meta_col2.query(
                        expr=f'id == "{doc_id}"',
                        output_fields=["original_filename", "opportunity_number", "upload_time"],
                        limit=1
                    )
                    info = doc_info[0] if doc_info else {}
                    chunks.append({
                        "rank": i + 1,
                        "similarity": round(max(0, 1 - hit.distance), 4),
                        "chunk_content": hit.entity.get("chunk_content", ""),
                        "chunk_index": hit.entity.get("chunk_index", 0),
                        "filename": info.get("original_filename", ""),
                        "opportunity_number": info.get("opportunity_number", ""),
                        "upload_time": info.get("upload_time", ""),
                    })
                meta_col2.release()
            return chunks, None
        except Exception as e:
            logger.error(f"RAG召回失败: {e}")
            return [], str(e)

    chunks, err = rag_retrieve()
    if err:
        return jsonify({"success": False, "message": err}), 500

    # ── 2. 拼装上下文 ──────────────────────────────────────────────
    context_parts = [f"[片段{c['rank']} 来源:{c['filename']}]\n{c['chunk_content']}" for c in chunks]
    context_text  = "\n\n".join(context_parts) if context_parts else "（未检索到相关内容）"

    # 加载该知识库的专属提示词
    kb_prompt = get_kb_prompt(kb_en_name)

    prompt = f"""{kb_prompt}

【检索片段】
{context_text}

【用户问题】
{search_text}"""

    # ── 3. SSE 流式生成器 ──────────────────────────────────────────
    def generate():
        yield f"data: {json.dumps({'type': 'rag', 'chunks': chunks}, ensure_ascii=False)}\n\n"

        try:
            from openai import OpenAI
            client = OpenAI(api_key=AGENT_API_KEY, base_url=AGENT_API_URL)
            response = client.chat.completions.create(
                model=AGENT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                timeout=60
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield f"data: {json.dumps({'type': 'answer', 'content': content}, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.error(f"DeepSeek API 调用失败: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return Response(generate(), mimetype='text/event-stream',
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route('/data_analysis')
def data_analysis():
    """数据分析页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    stats = {
        "kb_count": 0,
        "doc_count": 0,
        "chunk_count": 0,
        "total_size_mb": 0,
        "file_type_dist": {},
        "kb_doc_dist": [],
        "upload_trend": {},
    }

    try:
        if connect_milvus():
            # 知识库数量
            if utility.has_collection("svc_bk_base_info"):
                kb_col = Collection("svc_bk_base_info")
                kb_col.load()
                kb_list = kb_col.query(expr="", output_fields=["bk_id", "bk_cn_name", "bk_en_name"], limit=200)
                stats["kb_count"] = len(kb_list)
                kb_col.release()
            else:
                kb_list = []

            # 文档元数据统计
            if utility.has_collection("svc_bk_file_metadata"):
                meta_col = Collection("svc_bk_file_metadata")
                meta_col.load()
                docs = meta_col.query(
                    expr="",
                    output_fields=["id", "bk_en_name", "file_type", "file_size", "upload_time", "total_chunks"],
                    limit=5000
                )
                meta_col.release()

                stats["doc_count"] = len(docs)

                # 文件类型分布
                for d in docs:
                    ft = d.get("file_type", "unknown") or "unknown"
                    stats["file_type_dist"][ft] = stats["file_type_dist"].get(ft, 0) + 1

                # 总文件大小
                total_bytes = sum(d.get("file_size", 0) or 0 for d in docs)
                stats["total_size_mb"] = round(total_bytes / (1024 * 1024), 2)

                # 各知识库文档数（用 bk_en_name 即 bk_id 关联）
                kb_id_map = {kb.get("bk_id"): kb.get("bk_cn_name", kb.get("bk_en_name", "")) for kb in kb_list}
                kb_doc_count = {}
                for d in docs:
                    kb_key = d.get("bk_en_name", "未知")
                    label = kb_id_map.get(kb_key, kb_key)
                    kb_doc_count[label] = kb_doc_count.get(label, 0) + 1
                stats["kb_doc_dist"] = [{"name": k, "count": v} for k, v in kb_doc_count.items()]

                # 上传时间趋势（按日期统计）
                for d in docs:
                    t = (d.get("upload_time") or "")[:10]
                    if t:
                        stats["upload_trend"][t] = stats["upload_trend"].get(t, 0) + 1
                stats["upload_trend"] = dict(sorted(stats["upload_trend"].items()))

            # 向量分片总数
            if utility.has_collection("svc_bk_file_vector_chunks"):
                vec_col = Collection("svc_bk_file_vector_chunks")
                vec_col.load()
                chunks = vec_col.query(expr="", output_fields=["chunk_id"], limit=16384)
                stats["chunk_count"] = len(chunks)
                vec_col.release()

    except Exception as e:
        logger.error(f"数据分析统计失败: {e}")

    return render_template('data_analysis.html',
                           emp_name=session.get('emp_name'),
                           emp_lob_num=session.get('emp_lob_num'),
                           stats=stats)


@app.route('/file_management')
def file_management():
    """上传文件管理页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        upload_dir = "uploads/uploads_original"
        files = []
        
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                file_path = os.path.join(upload_dir, filename)
                if os.path.isfile(file_path):
                    # 获取文件信息
                    file_size = os.path.getsize(file_path)
                    modified_time = os.path.getmtime(file_path)
                    modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 解析文件名
                    parts = filename.split('_', 2)
                    uuid = parts[0] if len(parts) > 0 else ''
                    opportunity_number = parts[1] if len(parts) > 1 else ''
                    original_filename = parts[2] if len(parts) > 2 else filename
                    
                    files.append({
                        'filename': filename,
                        'original_filename': original_filename,
                        'uuid': uuid,
                        'opportunity_number': opportunity_number,
                        'size': file_size,
                        'modified_date': modified_date,
                        'url': url_for('download_file', filename=filename)
                    })
        
        # 按修改时间倒序排序
        files.sort(key=lambda x: x['modified_date'], reverse=True)
        
        return render_template('file_management.html', 
                             emp_name=session.get('emp_name'),
                             emp_lob_num=session.get('emp_lob_num'),
                             files=files)
    except Exception as e:
        logger.error(f"文件管理失败: {str(e)}")
        flash(f"文件管理失败: {str(e)}", "error")
        return render_template('file_management.html', 
                             emp_name=session.get('emp_name'),
                             emp_lob_num=session.get('emp_lob_num'),
                             files=[])

@app.route('/download/<filename>')
def download_file(filename):
    """文件下载"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        upload_dir = "uploads/uploads_original"
        file_path = os.path.join(upload_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash("文件不存在", "error")
            return redirect(url_for('file_management'))
    except Exception as e:
        logger.error(f"文件下载失败: {str(e)}")
        flash(f"文件下载失败: {str(e)}", "error")
        return redirect(url_for('file_management'))

@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_users():
    """用户管理API接口"""
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    if request.method == 'GET':
        users = get_all_users()
        return jsonify({"success": True, "data": users})
    
    elif request.method == 'POST':
        data = request.get_json()
        emp_lob_num = data.get('emp_lob_num', '').strip()
        emp_name = data.get('emp_name', '').strip()
        password = data.get('password', '').strip()
        
        if not all([emp_lob_num, emp_name, password]):
            return jsonify({"success": False, "message": "请填写完整信息"})
        
        success, message = add_user(emp_lob_num, emp_name, password)
        return jsonify({"success": success, "message": message})
    
    elif request.method == 'PUT':
        data = request.get_json()
        user_id = data.get('id')
        emp_lob_num = data.get('emp_lob_num', '').strip()
        emp_name = data.get('emp_name', '').strip()
        password = data.get('password', '').strip()
        
        if not all([user_id, emp_lob_num, emp_name, password]):
            return jsonify({"success": False, "message": "请填写完整信息"})
        
        success, message = update_user(user_id, emp_lob_num, emp_name, password)
        return jsonify({"success": success, "message": message})
    
    elif request.method == 'DELETE':
        user_id = request.args.get('id')
        if not user_id:
            return jsonify({"success": False, "message": "用户ID不能为空"})
        
        success, message = delete_user(user_id)
        return jsonify({"success": success, "message": message})

# 知识库管理功能

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "config", "prompts")

def get_kb_prompt(bk_id):
    """按 bk_id 加载知识库专属提示词，找不到则用 default.md"""
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    prompt_file = os.path.join(PROMPTS_DIR, f"{bk_id}.md")
    default_file = os.path.join(PROMPTS_DIR, "default.md")
    target = prompt_file if os.path.exists(prompt_file) else default_file
    try:
        with open(target, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        logger.warning(f"提示词文件读取失败: {e}")
        return "你是一个知识库智能助手，请根据检索到的文档片段回答用户问题。"

def save_kb_prompt(bk_id, content):
    """保存知识库专属提示词"""
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    prompt_file = os.path.join(PROMPTS_DIR, f"{bk_id}.md")
    try:
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"提示词文件保存失败: {e}")
        return False

def delete_kb_prompt(bk_id):
    """删除知识库专属提示词文件"""
    prompt_file = os.path.join(PROMPTS_DIR, f"{bk_id}.md")
    if os.path.exists(prompt_file):
        try:
            os.remove(prompt_file)
        except Exception as e:
            logger.warning(f"提示词文件删除失败: {e}")

def get_all_knowledge_bases():
    """获取所有知识库"""
    try:
        if not connect_milvus():
            return []
        
        collection = Collection("svc_bk_base_info")
        collection.load()
        
        result = collection.query(
            expr="",
            output_fields=["bk_id", "bk_en_name", "bk_cn_name", "upload_time", "update_time", "uploaded_by"],
            limit=100
        )
        
        disconnect_milvus()
        return result
    except Exception as e:
        logger.error(f"获取知识库列表失败：{str(e)}")
        return []

def add_knowledge_base(bk_en_name, bk_cn_name, uploaded_by):
    """添加知识库"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        collection = Collection("svc_bk_base_info")
        collection.load()
        
        # 检查英文名称是否已存在
        existing = collection.query(
            expr=f"bk_en_name == '{bk_en_name}'",
            output_fields=["bk_id"],
            limit=1
        )
        
        if existing:
            disconnect_milvus()
            return False, "知识库英文名称已存在"
        
        # 插入新知识库
        bk_id = str(uuid.uuid4())
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        empty_vector = [0.0] * 128
        
        insert_data = [
            [bk_id],
            [bk_en_name],
            [bk_cn_name],
            [now],
            [now],
            [uploaded_by],
            [empty_vector]
        ]
        
        collection.insert(insert_data)
        collection.flush()
        disconnect_milvus()
        
        return True, "知识库添加成功"
    except Exception as e:
        logger.error(f"添加知识库失败：{str(e)}")
        return False, "添加知识库失败"

def update_knowledge_base(bk_id, bk_en_name, bk_cn_name):
    """更新知识库信息"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        collection = Collection("svc_bk_base_info")
        collection.load()
        
        # 检查英文名称是否被其他知识库使用
        existing = collection.query(
            expr=f"bk_en_name == '{bk_en_name}' and bk_id != '{bk_id}'",
            output_fields=["bk_id"],
            limit=1
        )
        
        if existing:
            disconnect_milvus()
            return False, "知识库英文名称已被其他知识库使用"
        
        # 更新知识库信息
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 由于Milvus不支持直接更新，需要先删除再插入
        collection.delete(expr=f"bk_id == '{bk_id}'")
        collection.flush()
        
        # 获取原知识库信息
        original = collection.query(
            expr=f"bk_id == '{bk_id}'",
            output_fields=["upload_time", "uploaded_by"],
            limit=1
        )
        
        if original:
            upload_time = original[0].get("upload_time")
            uploaded_by = original[0].get("uploaded_by")
        else:
            upload_time = now
            uploaded_by = "unknown"
        
        insert_data = [
            [bk_id],
            [bk_en_name],
            [bk_cn_name],
            [upload_time],  # 保持原上传时间
            [now],          # 更新修改时间
            [uploaded_by],  # 保持原上传人
            [[0.0] * 128]   # 空向量
        ]
        
        collection.insert(insert_data)
        collection.flush()
        disconnect_milvus()
        
        return True, "知识库更新成功"
    except Exception as e:
        logger.error(f"更新知识库失败：{str(e)}")
        return False, "更新知识库失败"

def delete_knowledge_base(bk_id):
    """删除知识库"""
    try:
        if not connect_milvus():
            return False, "数据库连接失败"
        
        collection = Collection("svc_bk_base_info")
        collection.load()
        
        # 删除知识库
        collection.delete(expr=f"bk_id == '{bk_id}'")
        collection.flush()
        disconnect_milvus()
        
        return True, "知识库删除成功"
    except Exception as e:
        logger.error(f"删除知识库失败：{str(e)}")
        return False, "删除知识库失败"

@app.route('/knowledge_base_management')
def knowledge_base_management():
    """知识库管理页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    knowledge_bases = get_all_knowledge_bases()
    return render_template('knowledge_base_management.html', 
                         knowledge_bases=knowledge_bases,
                         emp_name=session.get('emp_name'),
                         emp_lob_num=session.get('emp_lob_num'))

@app.route('/api/knowledge_bases', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_knowledge_bases():
    """知识库管理API接口"""
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    if request.method == 'GET':
        knowledge_bases = get_all_knowledge_bases()
        return jsonify({"success": True, "data": knowledge_bases})
    
    elif request.method == 'POST':
        data = request.get_json()
        bk_en_name = data.get('bk_en_name', '').strip()
        bk_cn_name = data.get('bk_cn_name', '').strip()
        uploaded_by = session.get('emp_lob_num', 'unknown')
        
        if not all([bk_en_name, bk_cn_name]):
            return jsonify({"success": False, "message": "请填写完整信息"})
        
        success, message = add_knowledge_base(bk_en_name, bk_cn_name, uploaded_by)
        return jsonify({"success": success, "message": message})
    
    elif request.method == 'PUT':
        data = request.get_json()
        bk_id = data.get('bk_id')
        bk_en_name = data.get('bk_en_name', '').strip()
        bk_cn_name = data.get('bk_cn_name', '').strip()
        
        if not all([bk_id, bk_en_name, bk_cn_name]):
            return jsonify({"success": False, "message": "请填写完整信息"})
        
        success, message = update_knowledge_base(bk_id, bk_en_name, bk_cn_name)
        return jsonify({"success": success, "message": message})
    
    elif request.method == 'DELETE':
        bk_id = request.args.get('bk_id')
        if not bk_id:
            return jsonify({"success": False, "message": "知识库ID不能为空"})
        
        success, message = delete_knowledge_base(bk_id)
        return jsonify({"success": success, "message": message})

# 文档上传功能

@app.route('/api/kb_prompt', methods=['GET', 'POST'])
def api_kb_prompt():
    """知识库提示词读取/保存接口"""
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "未登录"}), 401

    if request.method == 'GET':
        bk_id = request.args.get('bk_id', '').strip()
        if not bk_id:
            return jsonify({"success": False, "message": "bk_id 不能为空"})
        # 读取专属提示词，没有则读 default
        prompt_file = os.path.join(PROMPTS_DIR, f"{bk_id}.md")
        default_file = os.path.join(PROMPTS_DIR, "default.md")
        has_custom = os.path.exists(prompt_file)
        target = prompt_file if has_custom else default_file
        try:
            with open(target, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            content = ""
        return jsonify({"success": True, "content": content, "has_custom": has_custom})

    elif request.method == 'POST':
        data = request.get_json()
        bk_id   = data.get('bk_id', '').strip()
        content = data.get('content', '')
        reset   = data.get('reset', False)
        if not bk_id:
            return jsonify({"success": False, "message": "bk_id 不能为空"})
        if reset:
            delete_kb_prompt(bk_id)
            return jsonify({"success": True, "message": "已恢复默认"})
        ok = save_kb_prompt(bk_id, content)
        return jsonify({"success": ok, "message": "保存成功" if ok else "保存失败"})

@app.route('/prompt_management')
def prompt_management():
    """提示词管理页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    knowledge_bases = get_all_knowledge_bases()
    # 标记每个知识库是否有自定义提示词
    for kb in knowledge_bases:
        prompt_file = os.path.join(PROMPTS_DIR, f"{kb['bk_id']}.md")
        kb['has_prompt'] = os.path.exists(prompt_file)
    return render_template('prompt_management.html',
                           emp_name=session.get('emp_name'),
                           emp_lob_num=session.get('emp_lob_num'),
                           knowledge_bases=knowledge_bases)

@app.route('/document_upload')
def document_upload():
    """文档上传页面"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    knowledge_bases = get_all_knowledge_bases()
    return render_template('document_upload.html', 
                         knowledge_bases=knowledge_bases,
                         emp_name=session.get('emp_name'),
                         emp_lob_num=session.get('emp_lob_num'))

@app.route('/api/upload_document', methods=['POST'])
def api_upload_document():
    """文档上传API接口"""
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "未登录"}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "没有选择文件"})
        
        file = request.files['file']
        kb_id = request.form.get('kb_id')
        opportunity_number = request.form.get('opportunity_number')
        
        if not kb_id:
            return jsonify({"success": False, "message": "请选择知识库"})
        
        if not opportunity_number:
            return jsonify({"success": False, "message": "请输入商机编号"})
        
        if file.filename == '':
            return jsonify({"success": False, "message": "没有选择文件"})
        
        # 检查文件类型
        allowed_extensions = {'pdf', 'doc', 'docx', 'txt', 'sql', 'xlsx', 'xls'}
        file_ext = file.filename.lower().split('.')[-1]
        if file_ext not in allowed_extensions:
            return jsonify({"success": False, "message": "不支持的文件格式"})
        
        # 保存文件
        upload_dir = "uploads/uploads_original"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保留原始文件名中的中文，只清理路径分隔符等危险字符
        original_filename = file.filename
        
        # 自定义文件名清理函数，保留中文
        def safe_filename(name):
            # 保留中文字符、字母、数字、下划线、连字符、点
            import re
            # 匹配中文字符、字母、数字、下划线、连字符、点
            safe_chars = re.compile(r'[^\u4e00-\u9fff\w\-_.]', re.UNICODE)
            cleaned = safe_chars.sub('', name)
            # 如果清理后为空，使用安全的后备名称
            if not cleaned:
                cleaned = "uploaded_file"
            return cleaned
        
        filename = safe_filename(original_filename)
        
        # 使用新格式：uuid_商机编号_原始文件名称
        file_uuid = str(uuid.uuid4())
        opportunity_number_clean = opportunity_number.replace(" ", "_").replace("/", "-")
        
        # 检查文件名是否已经包含商机编号，避免重复
        if opportunity_number_clean in filename:
            # 文件名已包含商机编号，直接使用uuid_文件名格式
            new_filename = f"{file_uuid}_{filename}"
        else:
            # 文件名不包含商机编号，使用uuid_商机编号_文件名格式
            new_filename = f"{file_uuid}_{opportunity_number_clean}_{filename}"
        
        file_path = os.path.join(upload_dir, new_filename)
        
        file.save(file_path)
        
        # 处理文档
        processor = DocumentProcessor()
        uploaded_by = session.get('emp_lob_num', 'unknown')
        
        # 记录API调用信息
        logger.info(f"🔍 API开始处理文档: {filename}")
        logger.info(f"   文件路径: {file_path}")
        logger.info(f"   知识库ID: {kb_id}")
        logger.info(f"   商机编号: {opportunity_number}")
        logger.info(f"   文件UUID: {file_uuid}")
        
        result = processor.process_document(
            file_path, 
            kb_id, 
            opportunity_number, 
            filename, 
            uploaded_by,
            document_id=file_uuid  # 传递生成的UUID
        )
        
        # 保留原始文件，不移除
        logger.info("✅ 原始文件已保存: {file_path}")
        
        # 记录API处理结果
        logger.info(f"📊 API处理结果: {result}")
        
        if result.get("success", False):
            logger.info("✅ API处理成功")
            return jsonify({
                "success": True, 
                "message": "文档上传和处理成功",
                "step": result.get("step", "完成"),
                "total_chunks": result.get("total_chunks", 0),
                "overwrite": result.get("overwrite", False)
            })
        else:
            error_msg = result.get("message", "文档处理失败")
            error_step = result.get("step", "未知")
            logger.error(f"❌ API处理失败: {error_msg} (步骤: {error_step})")
            
            # 记录详细错误信息
            error_detail = result.get("error_detail", "")
            if error_detail:
                logger.error(f"详细错误信息: {error_detail}")
            
            return jsonify({
                "success": False, 
                "message": error_msg,
                "step": error_step,
                "error_detail": error_detail
            })
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"文档上传失败: {str(e)}")
        logger.error(f"详细错误堆栈:\n{error_detail}")
        return jsonify({"success": False, "message": f"上传失败: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host=FLASK_HOST, port=FLASK_PORT, use_reloader=False)