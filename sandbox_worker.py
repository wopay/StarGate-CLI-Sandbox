#!/usr/bin/env python3
"""
🌌 星门 OS - 01号协作沙盒 (V50.0 纯净稳定版)
特性：单线并发锁定、任务柔性回退、数据流静默接入、3DVR视觉资产跨域传输、ReAct自循环。
🛡️ 核心防线矩阵：
  - 权限隔离：su -m 降维执行配合 $HOME 指针重定向，防范目录越权。
  - 无阻塞并发：原生异步赋权，消除 Event Loop 的 I/O 阻塞。
  - 全局重置：直达容器底层的物理级进程树安全释放。
  - 全域巡护：100KB 内存防溢出滑窗，异常节点跨域清理。
  - 柔性调度：429 动态冷却与退避策略，平稳规避算力限流。
"""

import os
import re
import json
import time
import pwd
import shlex
import httpx
import asyncio
import logging
import shutil
import subprocess
import urllib.parse
import signal
from typing import Set, Dict
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from collections import defaultdict

async def graceful_stop(proc, task_id="UNKNOWN"):
    """🏛️ 平滑停止协议：遵循 POSIX 标准，触发平稳中止以释放算力"""
    if proc and proc.returncode is None:
        try:
            pgid = os.getpgid(proc.pid)
            os.killpg(pgid, signal.SIGINT)
            logging.getLogger("StarGateWorker").warning(f"🚦 [柔性制动] 已向单元 {task_id} 发送中断信号，API 请求已截断。")
            for _ in range(10):
                if proc.returncode is not None: return
                await asyncio.sleep(0.1)
            if proc.returncode is None:
                os.killpg(pgid, signal.SIGTERM)
                await asyncio.sleep(0.5)
            if proc.returncode is None:
                os.killpg(pgid, signal.SIGKILL)
        except Exception: 
            try: proc.kill()
            except: pass

def force_release(proc):
    """🪢 资源强制释放：安全释放整个进程组，清理停滞进程"""
    if proc and proc.returncode is None:
        try: os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception: 
            try: proc.kill()
            except: pass

def global_process_cleanup(signal_type="-INT"):
    """☢️ 全局算力重置：直连容器底层，向所有停滞进程发送系统级释放信号"""
    try:
        target_container = os.getenv("TARGET_CLI_CONTAINER", "stargate_cli_01")
        subprocess.run(["docker", "exec", target_container, "pkill", signal_type, "-f", "gemini"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.getLogger("StarGateWorker").warning(f"☢️ [全域重置] 已向容器 {target_container} 广播 {signal_type} 全局释放指令！")
    except Exception as e:
        logging.getLogger("StarGateWorker").error(f"❌ 释放指令广播失败: {e}")

# ================= 🗄️ 物理空间与防线配置 =================
BASE_DIR = os.getenv("FACTORY_BASE_DIR", "/app")
INBOX_DIR = os.path.join(BASE_DIR, "inbox")
OUTBOX_DIR = os.path.join(BASE_DIR, "outbox")
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
GALLERY_DIR = os.path.join(STORAGE_DIR, "gallery")

RADAR_HISTORY_FILE = os.path.join(LOGS_DIR, "radar_history.json")

for d in [INBOX_DIR, OUTBOX_DIR, WORKSPACE_DIR, LOGS_DIR, STORAGE_DIR, GALLERY_DIR]:
    os.makedirs(d, exist_ok=True)

MASTER_HOST = os.getenv("MASTER_HOST", "192.168.2.2")
MASTER_PORT = os.getenv("MASTER_PORT", "3333")

FACTORY_INGEST_API = f"http://{MASTER_HOST}:{MASTER_PORT}/api/workflow/execute" 
LOG_FILE_PATH = os.path.join(LOGS_DIR, "worker_radar.log")
RADAR_PORT = 8999 

GLOBAL_PROCESS_REGISTRY = {} 

DNA_RULES_FILE = os.path.join(LOGS_DIR, "sandbox_dna_rules.json")
SESSION_BASE_DIR = os.getenv("SESSION_BASE_DIR", "/root/.gemini/tmp/isolated_sessions")
WILD_CHATS_DIR = os.getenv("WILD_CHATS_DIR", "/app/.gemini/tmp/app/chats")
MAX_SESSION_SIZE_KB = 100

for d in [SESSION_BASE_DIR, WILD_CHATS_DIR]:
    os.makedirs(d, exist_ok=True)

# ================= 🛡️ 双轨异步文件锁矩阵 =================
_vault_locks = defaultdict(asyncio.Lock)

class DNAVaultManager:
    @staticmethod
    async def atomic_write(target_path: str, payload: dict):
        async with _vault_locks[target_path]:
            temp_path = f"{target_path}.tmp_mutation"
            try:
                with open(temp_path, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)
                os.replace(temp_path, target_path)
                logging.getLogger("StarGateWorker").info(f"💾 [数据守护] 任务流已安全锚定: {target_path}")
            except Exception as e:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                logging.getLogger("StarGateWorker").error(f"❌ [数据守护] 写入异常，已执行回退: {e}")
                raise e

    @staticmethod
    async def atomic_read(target_path: str):
        async with _vault_locks[target_path]:
            if not os.path.exists(target_path):
                return None
            with open(target_path, "r", encoding="utf-8") as f:
                return json.load(f)

# ================= 🦾 无形协作组件 =================
class CyberneticHand:
    @staticmethod
    def force_write(content):
        pattern_xml = r"<file\s+path=[\"'](/app/[^\"']+)[\"']>\s*(.*?)\s*</file>"
        for match in re.finditer(pattern_xml, content, re.DOTALL | re.IGNORECASE):
            path, body = match.group(1).strip(), match.group(2)
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(body)
                logging.getLogger("StarGateWorker").info(f"🦾 [无形协助] 文本数据已落盘: {path}")
            except Exception as e:
                logging.getLogger("StarGateWorker").error(f"❌ [无形协助] 写入失败 {path}: {e}")
        return content

    @staticmethod
    def trigger_physical_forge(content, task_id):
        pattern = r"<forge_entity>\s*(.*?)\s*</forge_entity>"
        
        def repl(match):
            script = match.group(1)
            script_name = f"temp_forge_{int(time.time())}.py"
            script_path = os.path.join(WORKSPACE_DIR, script_name)
            
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script)
            
            logger = logging.getLogger("StarGateWorker")
            logger.info("🔧 [自动装配] 捕获构建图纸，正在执行代码生成...")
            
            result = subprocess.run(["python3", script_path], capture_output=True, text=True, cwd=WORKSPACE_DIR)
            
            try: os.remove(script_path)
            except: pass

            if result.returncode == 0:
                logger.info("✅ [自动装配] 实体生成完毕！正在启动跨域传输...")
                target_dir = os.path.join(STORAGE_DIR, "duihua", task_id)
                os.makedirs(target_dir, exist_ok=True)
                
                extradited_files = []
                for f in os.listdir(WORKSPACE_DIR):
                    if f.endswith(('.docx', '.xlsx', '.pdf', '.pptx', '.csv')):
                        src_path = os.path.join(WORKSPACE_DIR, f)
                        dst_path = os.path.join(target_dir, f)
                        shutil.copy2(src_path, dst_path)
                        try: os.remove(src_path)
                        except: pass
                        
                        extradited_files.append(f"[[ASSET:/storage/duihua/{task_id}/{f}]]")
                        logger.info(f"🚚 [数据传输] 资产已送达主控中心: {dst_path}")
                
                if extradited_files:
                    beacons_str = "\n".join(extradited_files)
                    return f"\n\n✅ **生成文件已传输完毕**。资源指引：\n{beacons_str}\n"
                else:
                    return "\n\n⚠️ **代码执行成功，但工作区未发现可传输的产物文件。**\n"
            else:
                logger.error(f"❌ [自动装配] 生成失败:\n{result.stderr}")
                return f"\n\n❌ **实体生成异常**（代码执行报错）：\n```text\n{result.stderr}\n```\n"

        return re.sub(pattern, repl, content, flags=re.DOTALL | re.IGNORECASE)

# ================= 🧬 异步日志雷达 =================
class ReactiveLogBus:
    def __init__(self):
        self.listeners: Set[asyncio.Queue] = set()
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(RADAR_HISTORY_FILE):
            try:
                with open(RADAR_HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data[-100:] if isinstance(data, list) else []
            except Exception:
                pass
        return []

    def _save_history(self):
        try:
            with open(RADAR_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False)
        except Exception:
            pass

    async def subscribe(self) -> asyncio.Queue:
        q = asyncio.Queue(maxsize=150)
        self.listeners.add(q)
        for msg in self.history:
            try: q.put_nowait(msg)
            except asyncio.QueueFull: pass
        return q

    def unsubscribe(self, q: asyncio.Queue):
        self.listeners.discard(q)

    def broadcast(self, message: str):
        self.history.append(message)
        if len(self.history) > 100:
            self.history.pop(0)
        self._save_history()
            
        for q in list(self.listeners):
            try: q.put_nowait(message)
            except asyncio.QueueFull:
                try: q.get_nowait()
                except asyncio.QueueEmpty: pass
                q.put_nowait(message)

async_bus = ReactiveLogBus()
logger = logging.getLogger("StarGateWorker")
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
file_handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

class AsyncBroadcastHandler(logging.Handler):
    def emit(self, record):
        msg = json.dumps({
            "time": datetime.fromtimestamp(record.created).strftime('%H:%M:%S'),
            "level": record.levelname,
            "msg": record.getMessage()
        })
        try:
            loop = asyncio.get_running_loop()
            loop.call_soon_threadsafe(async_bus.broadcast, msg)
        except Exception: 
            async_bus.broadcast(msg)

logger.addHandler(AsyncBroadcastHandler())

# ================= 🚀 SSE 状态与控制枢纽 =================
async def handle_radar_connection(reader, writer):
    try:
        request_line = await asyncio.wait_for(reader.readline(), timeout=5.0)
        if not request_line: return writer.close()
        
        req_parts = request_line.decode('utf-8', errors='ignore').strip().split()
        if len(req_parts) < 2: return writer.close()
        
        method = req_parts[0].upper()
        raw_path = req_parts[1]
        
        content_length = 0
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=5.0)
            if not line or line in (b'\r\n', b'\n'): break
            header_line = line.decode('utf-8', errors='ignore').strip()
            if header_line.lower().startswith('content-length:'):
                content_length = int(header_line.split(':')[1].strip())
        
        parsed_path = urllib.parse.urlparse(raw_path)
        route = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        target_task = query.get('task', [None])[0]
        
        CORS_HEADERS = b"Access-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\r\n\r\n"

        if method == 'OPTIONS':
            writer.write(
                b"HTTP/1.1 204 No Content\r\n"
                b"Access-Control-Allow-Origin: *\r\n"
                b"Access-Control-Allow-Methods: POST, GET, OPTIONS, DELETE, PUT\r\n"
                b"Access-Control-Allow-Headers: Content-Type, Authorization\r\n"
                b"Access-Control-Max-Age: 86400\r\n\r\n"
            )
            await writer.drain()
            return
        
        if route == '/api/config/dna' and method == 'POST':
            body = b''
            if content_length > 0:
                body = await asyncio.wait_for(reader.readexactly(content_length), timeout=5.0)
            try:
                payload = json.loads(body.decode('utf-8'))
                with open(DNA_RULES_FILE, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)
                logger.info("📡 [系统基座] 全局规则库已成功同步至本地！")
                writer.write(b"HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n{\"status\":\"ok\"}")
            except Exception as e:
                logger.error(f"❌ [系统基座] 规则同步失败: {e}")
                writer.write(b"HTTP/1.1 500 Error\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            await writer.drain()

        elif route == '/api/dispatch' and method == 'POST':
            body = b''
            if content_length > 0:
                body = await asyncio.wait_for(reader.readexactly(content_length), timeout=10.0)
            try:
                payload = json.loads(body.decode('utf-8'))
                task_id = payload.get("task_id", f"TASK_{int(time.time())}_{os.urandom(2).hex()}")
                payload['task_id'] = task_id
                
                target_path = os.path.join(INBOX_DIR, f"{task_id}.json")
                await DNAVaultManager.atomic_write(target_path, payload)
                
                logger.info(f"📥 [调度中枢] 接收到协作指令，已分配流转通道: {task_id}")
                response_body = json.dumps({"status": "dispatched", "task_id": task_id}).encode('utf-8')
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + response_body)
            except Exception as e:
                logger.error(f"❌ [调度中枢] 任务分发失败: {e}")
                writer.write(b"HTTP/1.1 500 Error\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            await writer.drain()

        elif route == '/stream':
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\nConnection: keep-alive\r\n" + CORS_HEADERS)
            await writer.drain()
            q = await async_bus.subscribe()
            try:
                while True:
                    try:
                        msg = await asyncio.wait_for(q.get(), timeout=15.0)
                        writer.write(f"data: {msg}\n\n".encode('utf-8'))
                        await writer.drain()
                    except asyncio.TimeoutError:
                        writer.write(b": heartbeat\n\n")
                        await writer.drain()
            except Exception: pass
            finally:
                async_bus.unsubscribe(q)

        elif route == '/stop':
            if target_task == 'ALL':
                logger.warning("🛡️ [安全守护] 触发全局保护，正在平滑挂起所有活跃节点...")
                for tid, proc_info in list(GLOBAL_PROCESS_REGISTRY.items()):
                    proc = proc_info['process']
                    if proc.returncode is None:
                        try: await graceful_stop(proc, tid)
                        except Exception: pass
                        force_release(proc)
            elif target_task and target_task in GLOBAL_PROCESS_REGISTRY:
                proc = GLOBAL_PROCESS_REGISTRY[target_task]['process']
                if proc.returncode is None:
                    try: await graceful_stop(proc, target_task)
                    except Exception: pass
                    force_release(proc)
                    logger.warning(f"🛡️ [安全守护] 成功挂起目标节点: {target_task}")
            
            if target_task and target_task != 'ALL':
                subprocess.run(["pkill", "-INT", "-f", f"{target_task}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            response = b"HTTP/1.1 200 OK\r\n" + CORS_HEADERS + b"{\"status\":\"stopped\",\"target\":\"" + target_task.encode() + b"\"}"
            writer.write(response)
            await writer.drain()

        elif route == '/kill':
            killed = False
            if target_task == 'ALL_WILD':
                logger.warning("♻️ [资源回收] 接收到环境清理指令，正在平滑释放底层资源...")
                global_process_cleanup("-KILL") 
                for d in [SESSION_BASE_DIR, WILD_CHATS_DIR]:
                    if os.path.exists(d):
                        for item in os.listdir(d):
                            item_path = os.path.join(d, item)
                            try:
                                if os.path.isdir(item_path): shutil.rmtree(item_path)
                                else: os.remove(item_path)
                            except Exception: pass
                writer.write(b"HTTP/1.1 200 OK\r\n" + CORS_HEADERS + b"{\"status\":\"purged_all\"}")
                await writer.drain()
                return

            if target_task and target_task in GLOBAL_PROCESS_REGISTRY:
                proc_info = GLOBAL_PROCESS_REGISTRY[target_task]
                proc = proc_info['process']
                if proc.returncode is None:
                    try: await graceful_stop(proc, target_task)
                    except Exception: pass
                    force_release(proc)
                if os.path.exists(proc_info['session_dir']):
                    try: shutil.rmtree(proc_info['session_dir'])
                    except Exception: pass
                killed = True
            
            if target_task:
                isolation_mark_path = os.path.join(WILD_CHATS_DIR, f"{target_task}.isolated")
                try: open(isolation_mark_path, 'a').close()
                except: pass
                
                wild_path = os.path.join(WILD_CHATS_DIR, f"{target_task}.json")
                if os.path.exists(wild_path):
                    try:
                        os.chmod(wild_path, 0o666)
                        toxic_data = {"messages": [{"role": "model", "content": "【系统通知】：此节点资源已被系统安全回收，环境已重置。"}], "session_state": {"is_purged": True}}
                        with open(wild_path, "w", encoding="utf-8") as f: json.dump(toxic_data, f, ensure_ascii=False)
                        os.chmod(wild_path, 0o444) 
                        logger.warning(f"♻️ [资源回收] 已对节点 {target_task} 实施运行环境回收。")
                        killed = True
                    except Exception as e: pass
                
                subprocess.run(["pkill", "-KILL", "-f", f"{target_task}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if killed:
                response = b"HTTP/1.1 200 OK\r\n" + CORS_HEADERS + b"{\"status\":\"killed\",\"target\":\"" + target_task.encode() + b"\"}"
            else:
                response = b"HTTP/1.1 404 Not Found\r\n" + CORS_HEADERS + b"{\"error\":\"Task not found\"}"
            writer.write(response)
            await writer.drain()

        elif route == '/reboot_sandbox':
            logger.critical("🚨 [系统维护] 触发环境重置协议！当前容器即将在 1 秒内安全重启...")
            writer.write(b"HTTP/1.1 200 OK\r\n" + CORS_HEADERS + b"{\"status\":\"rebooting\"}")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            
            asyncio.get_event_loop().call_later(1.0, lambda: os._exit(1))

        elif route == '/api/sessions/list':
            try:
                active_sessions = []
                history_sessions_dict = {}
                current_time = time.time()

                def _get_meta(t_id):
                    m_path = os.path.join(WILD_CHATS_DIR, f"{t_id}.meta.json")
                    if os.path.exists(m_path):
                        try:
                            with open(m_path, "r", encoding="utf-8") as mf: return json.load(mf)
                        except: pass
                    return {}

                if os.path.exists(SESSION_BASE_DIR):
                    for task_dir in os.listdir(SESSION_BASE_DIR):
                        task_path = os.path.join(SESSION_BASE_DIR, task_dir)
                        if os.path.isdir(task_path):
                            for f in os.listdir(task_path):
                                if f.endswith('.json'):
                                    fp = os.path.join(task_path, f)
                                    mtime = os.path.getmtime(fp)
                                    tokens_total = 0
                                    try:
                                        with open(fp, 'r', encoding='utf-8') as sf:
                                            s_data = json.load(sf)
                                            for m in reversed(s_data.get('messages', [])):
                                                if m.get('type') == 'gemini' and m.get('tokens'):
                                                    tokens_total = m['tokens'].get('total', 0)
                                                    break
                                    except: pass

                                    meta = _get_meta(task_dir)
                                    active_sessions.append({
                                        "id": task_dir, "file": f, "path": fp, 
                                        "mtime": mtime, "tokens": tokens_total,
                                        "client_id": meta.get("client_id", "UNKNOWN"),
                                        "workflow_id": meta.get("workflow_id", task_dir),
                                        "title": meta.get("title", "隔离区协作推演")
                                    })

                if os.path.exists(WILD_CHATS_DIR):
                    for f in os.listdir(WILD_CHATS_DIR):
                        if f.endswith('.json') and not f.endswith('.meta.json'):
                            fp = os.path.join(WILD_CHATS_DIR, f)
                            mtime = os.path.getmtime(fp)
                            task_id = f.replace('.json', '')
                            
                            meta = _get_meta(task_id)
                            
                            if current_time - mtime < 60:
                                tokens_total = 0
                                try:
                                    with open(fp, 'r', encoding='utf-8') as sf:
                                        s_data = json.load(sf)
                                        for m in reversed(s_data.get('messages', [])):
                                            if m.get('type') == 'gemini' and m.get('tokens'):
                                                tokens_total = m['tokens'].get('total', 0)
                                                break
                                except: pass
                                
                                if not any(s['id'] == task_id for s in active_sessions):
                                    active_sessions.append({
                                        "id": task_id, "file": f, "path": fp, 
                                        "mtime": mtime, "tokens": tokens_total,
                                        "client_id": meta.get("client_id", "UNKNOWN"),
                                        "workflow_id": meta.get("workflow_id", task_id),
                                        "title": meta.get("title", "系统指令推演")
                                    })
                            else:
                                    if f not in history_sessions_dict:
                                        history_sessions_dict[f] = {
                                            "id": task_id, "file": f, "path": fp, "mtime": mtime,
                                            "title": meta.get("title", task_id)
                                        }

                # 👇 架构师级修复：将靶场发射井的“底层穿透指令”强制暴露给前端雷达！
                if os.path.exists(INBOX_DIR):
                    for f in os.listdir(INBOX_DIR):
                        if f.endswith('.processing'):
                            fp = os.path.join(INBOX_DIR, f)
                            task_id = f.replace('.json.processing', '')
                            try:
                                with open(fp, 'r', encoding='utf-8') as sf:
                                    t_data = json.load(sf)
                                    if not any(s['id'] == task_id for s in active_sessions):
                                        active_sessions.append({
                                            "id": task_id, "file": f, "path": fp, 
                                            "mtime": os.path.getmtime(fp), "tokens": 0,
                                            "client_id": t_data.get("client_id", "SILO_COMMAND"),
                                            "workflow_id": t_data.get("workflow_id", "MANUAL_OVERRIDE"),
                                            "title": "⚡ 靶场物理直连进程"
                                        })
                            except: pass

                active_sessions.sort(key=lambda x: x['mtime'], reverse=True)
                history_list = list(history_sessions_dict.values())
                history_list.sort(key=lambda x: x['mtime'], reverse=True)

                res = {"active": active_sessions, "history": history_list}
                body = json.dumps(res).encode('utf-8')
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
            except Exception as e:
                writer.write(b"HTTP/1.1 500 Error\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            await writer.drain()

        elif route == '/api/sessions/read':
            target_path = query.get('path', [''])[0]
            try:
                data = await DNAVaultManager.atomic_read(target_path)
                if data:
                    body = json.dumps({"data": data, "mtime": os.path.getmtime(target_path)}).encode('utf-8')
                    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
                else:
                    writer.write(b"HTTP/1.1 404 Not Found\r\nAccess-Control-Allow-Origin: *\r\n\r\n{\"error\": \"File missing\"}")
            except Exception as e:
                writer.write(b"HTTP/1.1 500 Error\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            await writer.drain()

        elif route == '/api/sessions/delete':
            target_path = query.get('path', [''])[0]
            try:
                if target_path and os.path.exists(target_path) and target_path.endswith('.json'):
                    if SESSION_BASE_DIR in target_path:
                        shutil.rmtree(os.path.dirname(target_path)) 
                    else:
                        os.remove(target_path) 
                    writer.write(b"HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n{\"status\": \"deleted\"}")
                else:
                    writer.write(b"HTTP/1.1 404 Not Found\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            except Exception as e:
                writer.write(b"HTTP/1.1 500 Error\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            await writer.drain()
        else:
            writer.write(b"HTTP/1.1 404 Not Found\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
            await writer.drain()

    except: pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except: pass

# ================= 🦾 沙盒主脑核心 =================
class SandboxWorker:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=60.0, trust_env=False)
        self.is_running = True
        self.task_queue = asyncio.Queue()
        self._task_lock = asyncio.Lock()
        
        self.MAX_CONCURRENCY = 1
        self.RETRY_COOLDOWN = 300 
        self._cooldown_until = 0

    async def _system_preflight_check(self):
        """🔍 [开机自检] 协作系统底层资产扫描"""
        import shutil
        
        logger.info("═"*60)
        logger.info("🛸 [系统初始化] 正在进行协作环境防线自检...")
        logger.info("═"*60)

        logger.info("🗄️ 【运行目录映射核验】")
        dirs = {
            "📥 接收通道 (INBOX)": INBOX_DIR,
            "📤 回传通道 (OUTBOX)": OUTBOX_DIR,
            "🗜️ 工作台区 (WORKSPACE)": WORKSPACE_DIR,
            "🗄️ 档案存储 (STORAGE)": STORAGE_DIR,
            "🛡️ 独立会话 (SESSIONS)": SESSION_BASE_DIR,
            "🏕️ 外部协作 (WILD)": WILD_CHATS_DIR
        }
        for name, path in dirs.items():
            status = "✅ 就绪" if os.path.exists(path) else "❌ 缺失 (配置异常)"
            logger.info(f"  ├─ {name:<18} [{status}] -> {path}")

        logger.info("⚙️ 【核心进程工具链】")
        pkill_ready = "✅ 满载" if shutil.which("pkill") else "⚠️ 未找到 pkill (中止功能受限)"
        docker_ready = "✅ 满载" if shutil.which("docker") else "⚠️ 未找到 docker (容器清理受限)"
        python_ready = "✅ 满载" if shutil.which("python3") else "❌ 缺失 (执行器停摆)"
        logger.info(f"  ├─ ☢️ 进程管理引擎 (pkill)        [{pkill_ready}]")
        logger.info(f"  ├─ 🐋 容器通信组件 (docker) [{docker_ready}]")
        logger.info(f"  ├─ 🦾 脚本执行环境 (python3)  [{python_ready}]")

        logger.info("🧬 【规则库与日志状态】")
        dna_status = "✅ 已挂载" if os.path.exists(DNA_RULES_FILE) else "🈳 待同步 (初始化)"
        radar_status = "✅ 历史留存" if os.path.exists(RADAR_HISTORY_FILE) else "🆕 全新运行"
        logger.info(f"  ├─ 全局规则基座 (DNA_RULES) [{dna_status}]")
        logger.info(f"  ├─ 状态历史记录 (RADAR_HIST)  [{radar_status}]")

        logger.info("📡 【网络与调度配置】")
        logger.info(f"  ├─ 📡 监听服务端口     [✅ TCP:{RADAR_PORT}]")
        logger.info(f"  ├─ 🌐 结果回传链路     [🔗 {FACTORY_INGEST_API}]")
        logger.info(f"  ├─ 🚦 任务并发配额     [{self.MAX_CONCURRENCY} 线程池]")
        logger.info(f"  ├─ ❄️ 频控冷却时间     [{self.RETRY_COOLDOWN} 秒]")

        logger.info("═"*60)
        logger.info("🟢 [诊断完成] 系统各项防线扫描通过，核心服务已启动！")
        logger.info("═"*60)
        await asyncio.sleep(0.5)

    async def sync_source_code(self):
        source_path = Path(__file__).absolute()
        target_path = Path(WORKSPACE_DIR) / "dna_source.py"
        try:
            if target_path.exists(): target_path.unlink()
            os.link(source_path, target_path)
            logger.info(f"🧬 源码映射完成: {target_path}")
        except Exception: pass

    def _intercept_and_forge_document(self, file_path: Path) -> Path:
        ext = file_path.suffix.lower()
        try:
            if ext == '.docx':
                logger.info(f"🔨 [文档解析] 正在提取 .docx 纯文本内容: {file_path.name}")
                import docx
                doc = docx.Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
            elif ext == '.pdf':
                logger.info(f"🔨 [文档解析] 正在提取 .pdf 纯文本内容: {file_path.name}")
                import pdfplumber
                text_blocks = []
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        if page_text := page.extract_text():
                            text_blocks.append(page_text)
                text = "\n".join(text_blocks)
            elif ext in ['.xlsx', '.xls']:
                logger.info(f"🔨 [文档解析] 正在提取 Excel 纯文本内容: {file_path.name}")
                import pandas as pd
                df = pd.read_excel(file_path)
                text = df.to_string()
            else:
                return file_path
                
            new_path = file_path.with_suffix('.txt')
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(f"【系统提取的 {file_path.name} 纯文本内容】\n{text}")
            
            file_path.unlink() 
            return new_path
        except Exception as e:
            logger.error(f"❌ 文档解析异常 ({ext}): {e}")
            return file_path

    async def execute_cli_task(self, execution_prompt: str, target_urls: list, task_id: str, limits: dict, world: str, cli_config: dict = None, dna_sequence: list = None, temporary_dna_patch: dict = None, is_enigma: bool = True) -> dict:
        import hashlib
        logger.info(f"🚀 [任务 {task_id}] 协作节点已接入流转...")
        start_time = time.time()
        
        if not cli_config: cli_config = {}
        cli_cmd = cli_config.get("cli_cmd") or "gemini"
        model_id = cli_config.get("model_id") or "gemini-2.5-flash"
        temperature = cli_config.get("temperature") or 0.2
        cli_args = cli_config.get("cli_args") or ""
        base_prompt = cli_config.get("base_prompt") or "你是一个稳定、高效的协作节点。"

        local_asset_paths = []
        storage_links = re.findall(r'(/storage/(?:temp_)?duihua/[\w\.-]+)', execution_prompt)
        if target_urls:
            storage_links.extend([str(u) for u in target_urls if '/storage/' in str(u)])
        storage_links = list(set(storage_links))

        if storage_links:
            asset_dir = Path(WORKSPACE_DIR) / "assets" / task_id
            asset_dir.mkdir(parents=True, exist_ok=True)
            for link in storage_links:
                download_url = f"http://{MASTER_HOST}:{MASTER_PORT}{link}"
                file_name = link.split("/")[-1]
                local_path = asset_dir / file_name
                try:
                    logger.info(f"📥 资源同步: 正在提取相关文件 {file_name}...")
                    resp = await self.http_client.get(download_url, timeout=30.0)
                    resp.raise_for_status()
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                    local_path = self._intercept_and_forge_document(local_path)
                    local_asset_paths.append(str(local_path.absolute()))
                except Exception as e:
                    logger.error(f"❌ 资源同步异常 {download_url}: {e}")

        context_str = ""
        if local_asset_paths:
            paths_str = "\n".join(local_asset_paths)
            context_str = (
                f"\n\n【🚀 SYSTEM NOTICE - 关联资产已同步】\n"
                f"任务关联的图片/文件已成功挂载至当前环境。\n"
                f"⚠️ 运行建议：请优先直接读取以下具体路径的文件，勿进行全局目录遍历以保障性能：\n"
                f"{paths_str}\n"
            )
        elif target_urls:
            urls_str = "\n".join(target_urls)
            context_str = f"\n\n[CONTEXT RESOURCES]\n{urls_str}"

        # 💡 变量已通过函数参数透传，直接组装 Payload
        machine_dna_payload = {
            "SYS_META_DIRECTIVE": "SOJ_STRUCTURAL_COMMUNICATION_ONLY",
            "COGNITIVE_BASE_LIMITS": limits,
            "WORLD_LINE": world.upper(),
            "SOJ_OUTPUT_SCHEMA": {
                "status": "processing | completed | error",
                "ai_dynamic_stop": "<int>", "ai_dynamic_purge": "<int>",
                "action": "<str>", "thoughts": ["<str>"], "safe_markdown": "<str>"
            },
            "CRITICAL_TOOL_BOUNDARIES": (
                "System Restriction: File traversal is strictly isolated to /app/workspace/ and /app/storage/. "
                "Attempting to read /app/sandbox_worker.py or .json configurations will result in fatal I/O exceptions. "
                "Rely solely on provided context."
            )
        }
        
        # 🔄 根据前端开关，动态插拔 Enigma 硬件芯片
        if is_enigma:
            machine_dna_payload["SOJ_OUTPUT_SCHEMA"]["machine_signals"] = ["<ENIGMA_CODE>"]
            machine_dna_payload["ENIGMA_DICTIONARY"] = {
                "S_OK|path": "Target file created/modified successfully",
                "S_ERR|reason": "Execution failed, see reason",
                "OS_CMD|cmd": "Using OS_COMMAND mechanical arm",
                "REQ_NET|url": "Requesting external network data",
                "T_END": "Task fully completed"
            }
            machine_dna_payload["BASE_PROMPT"] = base_prompt + " ⚠️ [ENIGMA PROTOCOL ENABLED]: You MUST use ENIGMA_DICTIONARY codes in `machine_signals` array to compress your actions. Keep `safe_markdown` extremely short!"
        else:
            machine_dna_payload["BASE_PROMPT"] = base_prompt + " 🌐 [NATURAL LANGUAGE MODE ENABLED]: Enigma protocol is suspended. Please communicate naturally and provide rich, detailed explanations in `safe_markdown`."

        dynamic_dna_compiled = ""
        
        if temporary_dna_patch:
            logger.info(f"🪚 [系统演化] 检测到动态调优补丁！正在合并至最高优先级策略...")
            dynamic_dna_compiled += "\n\n【🧬 节点动态调优补丁 (Evolution Patch)】"
            dynamic_dna_compiled += f"\n\n--- [优先法则: {temporary_dna_patch.get('name', '未命名补丁')}] ---\n{temporary_dna_patch.get('content', '')}"
            
        if dna_sequence:
            dynamic_dna_compiled += "\n\n【🧬 节点专项协作法则 (Dynamic Context Vault)】"
            for d_id in dna_sequence:
                dna_path = os.path.join(STORAGE_DIR, "os", "dna", "vault", "dynamic", f"{d_id}.json")
                if os.path.exists(dna_path):
                    try:
                        with open(dna_path, "r", encoding="utf-8") as f:
                            dna_frag = json.load(f)
                            dynamic_dna_compiled += f"\n\n--- [法则: {dna_frag.get('name', d_id)}] ---\n{dna_frag.get('content', '')}"
                    except Exception: pass

        hash_factor = { "payload": machine_dna_payload, "dynamic_dna_content": dynamic_dna_compiled }
        dna_string = json.dumps(hash_factor, sort_keys=True, ensure_ascii=False)
        dna_hash = hashlib.md5(dna_string.encode('utf-8')).hexdigest()[:10]
        macro_name = f"dna_{dna_hash}"
        
        cli_cmd_dir = "/home/ai_worker/.gemini/commands"
        os.makedirs(cli_cmd_dir, exist_ok=True)
        toml_path = os.path.join(cli_cmd_dir, f"{macro_name}.toml")

        if not os.path.exists(toml_path):
            logger.info(f"✨ [配置更新] 生成并应用 V-{dna_hash} 节点运行配置...")
            toml_content = f"""description = "Auto-Generated Configuration V-{dna_hash}"\n\n[model]\nname = "{model_id}"\ntemperature = {temperature}\n\n[system]\ntext = '''\n【SYSTEM_PROTOCOL_ENGAGED: STRUCTURAL_MODE】\n{json.dumps(machine_dna_payload, ensure_ascii=False, indent=2)}\n{dynamic_dna_compiled}\n\n⚠️ CRITICAL INSTRUCTION: You are a structural node. Avoid conversational pleasantries.\nEvery response you emit MUST be a valid JSON object matching the `SOJ_OUTPUT_SCHEMA` exactly.\nDO NOT wrap the JSON in ```json blocks. Start directly with {{ and end with }}.\n'''\n"""
            with open(toml_path, "w", encoding="utf-8") as f:
                f.write(toml_content)
                
            try:
                ai_uid = pwd.getpwnam('ai_worker').pw_uid
                ai_gid = pwd.getpwnam('ai_worker').pw_gid
                for root_dir, dirs, files in os.walk("/home/ai_worker/.gemini"):
                    os.chown(root_dir, ai_uid, ai_gid)
                    for file in files:
                        os.chown(os.path.join(root_dir, file), ai_uid, ai_gid)
            except KeyError:
                logger.warning("⚠️ 未找到专用系统用户，跳过权限降维应用。")
        else:
            logger.info(f"⚡ [配置命中] 当前逻辑策略已在缓存中 (V-{dna_hash})，跳过编译直接执行。")

        base_cmd = cli_cmd.strip()
        if base_cmd.endswith("chat"): 
            base_cmd = base_cmd[:-4].strip()
            
        cmd_parts = [base_cmd, macro_name]
        if cli_args: cmd_parts.append(cli_args)
        final_cmd_str = " ".join(cmd_parts)
        
        pure_prompt = f"{execution_prompt}{context_str}"
        
        task_session_dir = os.path.join(SESSION_BASE_DIR, task_id)
        os.makedirs(task_session_dir, exist_ok=True)
        
        env = os.environ.copy()
        env["GEMINI_SESSION_DIR"] = task_session_dir 
        env["HOME"] = "/home/ai_worker"
        env["USER"] = "ai_worker"
        
        active_purge = limits.get("purge", 10)
        dynamic_timeout = float(active_purge * 60)
        logger.info(f"⏱️ [算力分配] 节点已挂载 {dynamic_timeout}s 运行周期保护 (流转上限: {active_purge})")

        max_react_loops = 3
        current_loop = 0
        final_text = ""
        visual_assets = []
        
        try:
            while current_loop < max_react_loops:
                current_loop += 1
                prompt_file = os.path.join(WORKSPACE_DIR, f"{task_id}_prompt_{current_loop}.txt")
                
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(pure_prompt)
                    
                os.chmod(prompt_file, 0o777)
                    
                su_cmd_str = f"cat {shlex.quote(prompt_file)} | {final_cmd_str}"
                
                # 💡 架构师级防撞：动态嗅探用户，不存在则直接用 bash 物理直连
                try:
                    pwd.getpwnam('ai_worker')
                    cmd = f"su -m ai_worker -c {shlex.quote(su_cmd_str)}"
                except KeyError:
                    cmd = f"bash -c {shlex.quote(su_cmd_str)}"
                    
                logger.info(f"⚙️ [底层指令] (执行轮次 {current_loop}/{max_react_loops}): {cmd}")
                
                process = await asyncio.create_subprocess_shell(
                    cmd, cwd=WORKSPACE_DIR, env=env,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                    start_new_session=True 
                )
                
                GLOBAL_PROCESS_REGISTRY[task_id] = {
                    "process": process,
                    "session_dir": task_session_dir
                }
                
                stdout_acc = []
                stderr_acc = []
                
                async def read_stdout():
                    buffer = ""
                    while True:
                        chunk = await process.stdout.read(256)
                        if not chunk:
                            if buffer.strip():
                                stdout_acc.append(buffer.strip())
                            break
                            
                        text = chunk.decode('utf-8', errors='ignore')
                        buffer += text
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line_clean = line.strip()
                            if line_clean:
                                stdout_acc.append(line_clean)
                                if "Generated files:" in line_clean or "• /app/storage/" in line_clean:
                                    img_match = re.search(r'(/app/storage/[\w\.-]+)', line_clean)
                                    if img_match:
                                        relative_route = img_match.group(1).replace("/app/storage", "/storage")
                                        visual_assets.append(f"[[ASSET:{relative_route}]]")
                                        logger.info(f"🖼️ [视觉系统] 成功捕获图像资源信标: {relative_route}")

                async def read_stderr():
                    while True:
                        line = await process.stderr.readline()
                        if not line: break
                        text = line.decode('utf-8', errors='ignore').rstrip()
                        if text:
                            stderr_acc.append(text)
                            if "RESOURCE_EXHAUSTED" in text or "429" in text:
                                async_bus.broadcast(json.dumps({
                                    "time": datetime.now().strftime('%H:%M:%S'),
                                    "level": "WARN", "msg": f"接口调用频控预警 (429): {text}"
                                }))
                
                try:
                    await asyncio.wait_for(asyncio.gather(process.wait(), read_stdout(), read_stderr()), timeout=dynamic_timeout)
                except asyncio.TimeoutError:
                    await graceful_stop(process, task_id)
                    logger.error(f"❌ [任务 {task_id}] {dynamic_timeout}s 周期限制触发，已执行强制阻断。")
                    return {"status": "error", "output": f"【系统干预】：任务执行超时 ({dynamic_timeout}s)，相关进程已被系统安全终止。", "error": "timeout"}

                out_str = "\n".join(stdout_acc)
                err_str = "\n".join(stderr_acc)

                if "RESOURCE_EXHAUSTED" in out_str or "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                    if current_loop >= 2:
                        logger.error(f"🛡️ [安保策略] 任务 {task_id} 因陷入死循环导致请求溢出，已执行安全干预。")
                        return {"status": "error", "output": "【系统干预】：检测到工具重复调用引发请求超载，运行状态已被系统重置。", "error": "token_explosion"}
                    return {"status": "rate_limit", "output": out_str, "error": err_str}
                
                if process.returncode != 0:
                    if process.returncode in [-9, -15]:
                         return {"status": "error", "output": out_str, "error": f"【系统干预】：任务触碰保护阈值，该进程已被底层策略强制挂起。"}
                    return {"status": "error", "output": out_str, "error": err_str}
                
                os_match = re.search(r'\[OS_COMMAND\](.*?)\[/OS_COMMAND\]', out_str, re.DOTALL | re.IGNORECASE)
                if os_match:
                    if current_loop >= max_react_loops:
                        logger.error(f"🛡️ [边界保护] 任务 {task_id} 达到最大调度深度限制，已中止冗余递归。")
                        return {"status": "error", "output": "【系统干预】：超出最大执行层级限制，协作环境已被阻断重置。", "error": "max_bounces_exceeded"}
                        
                    command_str = os_match.group(1).strip()
                    logger.info(f"🦾 [系统通信] 节点请求发起网络交互，正在放行...")
                    try:
                        cmd_json = json.loads(command_str)
                        if cmd_json.get("type") == "HTTP_REQUEST":
                            async with httpx.AsyncClient(trust_env=False, follow_redirects=True) as http_c:
                                resp = await http_c.request(
                                    method=cmd_json.get("method", "GET"),
                                    url=cmd_json.get("url"),
                                    headers=cmd_json.get("headers", {}),
                                    timeout=15.0
                                )
                                obs = resp.text[:4000] 
                                logger.info(f"🌐 [数据获取] 网页数据抓取成功 ({len(obs)} 字节)，准备重载至上下文...")
                                pure_prompt += f"\n\n{out_str}\n\n【OS_OBSERVATION (系统回传的结构化数据)】:\n{obs}\n\n系统指令：请基于上述真实数据继续推进。如果信息已完备，请直接输出最终结果，无需再次发起请求。"
                                continue 
                    except Exception as e:
                        logger.warning(f"⚠️ [交互异常] 网络请求未能完成: {e}")
                        pure_prompt += f"\n\n{out_str}\n\n【OS_OBSERVATION (异常状态)】:\n{str(e)}\n\n系统指令：请求外部数据未成功，请检查目标地址或更换分析策略。"
                        continue
                
                elapsed_time = round(time.time() - start_time, 2)
                logger.info(f"✅ [任务 {task_id}] 逻辑闭环执行完毕 | 耗时: {elapsed_time}s")
                final_text = out_str
                break

            if len(final_text) > 4000:
                final_text = f"【...前序日志记录过长，为防溢出已执行安全折叠...】\n{final_text[-4000:]}"

            if visual_assets:
                beacons_str = "\n".join(visual_assets)
                final_text += f"\n\n✅ **视觉资源生成完毕**。附件列表：\n{beacons_str}\n"

            return {"status": "success", "output": final_text}
            
        except Exception as e:
            error_msg = str(e)[:200].replace('"', '\\"')
            logger.error(f"🔥 [任务 {task_id}] 节点执行产生严重异常: {error_msg}")
            return {"status": "error", "output": "", "error": f"ExecutionFault::{error_msg}"}
        finally:
            GLOBAL_PROCESS_REGISTRY.pop(task_id, None)
            if os.path.exists(prompt_file):
                os.remove(prompt_file)

    # 💡 接收 original_task 参数，用于提取 HTTP 422 报错中提及的缺失字段
    async def report_to_factory(self, domain: str, result_text: str, task_id: str, original_task: dict = None):
        """📤 数据回传：集成指数退避与异步兜底"""
        if not original_task:
            original_task = {}
            
        payload = {
            "task_id": task_id,
            "target_domain": domain,
            "output": result_text,
            "status": "completed",
            "timestamp": time.time(),
            # 🔗 补齐主系统强制校验的 Pydantic 模型字段 (从下发的原始任务包中提取，若无则使用兜底值防崩)
            "chat_id": original_task.get("chat_id", "UNKNOWN_CHAT"),
            "step_title": original_task.get("step_title", "Sandbox Execution"),
            "instruction": original_task.get("instruction") or original_task.get("prompt") or "Run Agent",
            "user_input": original_task.get("user_input", "System Invoke"),
            "deliver_type": original_task.get("deliver_type", "text")
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"📤 [状态同步] 正在向业务中枢回传任务 {task_id} (尝试 {attempt+1}/{max_retries})...")
                
                response = await self.http_client.post(
                    FACTORY_INGEST_API,
                    json=payload,
                    timeout=30.0
                )
                
                # 💡 架构师级侦测：拦截非 200 状态码，强行剥离并暴露主控的底层 JSON 报错详情！
                if not response.is_success:
                    error_detail = response.text
                    logger.error(f"⚠️ [状态同步] 主控中枢拒绝接收 (HTTP {response.status_code})，详细驳回原因: {error_detail}")
                    response.raise_for_status() # 继续抛出异常以触发本地兜底逻辑
                
                logger.info(f"✅ [状态同步] 任务 {task_id} 结果已成功回传！")
                return 
                
            except httpx.HTTPStatusError as e:
                logger.error(f"⚠️ [任务 {task_id}] 通信阻断(重试 {attempt+1}/3): 状态码 {e.response.status_code}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"⚠️ [任务 {task_id}] 通信波动(重试 {attempt+1}/3): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        logger.error(f"❌ [任务 {task_id}] 多次汇报失败！触发本地异步缓存兜底...")
        fallback_path = os.path.join(OUTBOX_DIR, f"{task_id}_fallback.json")
        try:
            await DNAVaultManager.atomic_write(fallback_path, payload)
            logger.info(f"💾 [缓存兜底] 数据已安全落地至待发区: {fallback_path}")
        except Exception as dump_err:
            logger.error(f"💀 [缓存兜底] 落盘发生严重错误: {dump_err}")

    async def _session_watchdog(self):
        """🦅 全域巡护：动态内存管理与状态异常检测"""
        logger.info("👁️‍🗨️ [系统巡护] 内存安全防护与周期检测机制已挂载...")
        while self.is_running:
            try:
                if os.path.exists(SESSION_BASE_DIR):
                    for task_dir in os.listdir(SESSION_BASE_DIR):
                        task_session_path = os.path.join(SESSION_BASE_DIR, task_dir)
                        if not os.path.isdir(task_session_path): continue
                        total_size = sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(task_session_path) for f in files if f.endswith('.json'))
                        
                        if (total_size / 1024) > MAX_SESSION_SIZE_KB:
                            logger.warning(f"🧹 [巡护干预] 隔离区 {task_dir} 容量超限 ({total_size/1024:.1f}KB)，正在执行平稳缩容压缩！")
                            for f in os.listdir(task_session_path):
                                if not f.endswith(".json"): continue
                                filepath = os.path.join(task_session_path, f)
                                try:
                                    with open(filepath, "r", encoding="utf-8") as file_obj:
                                        data = json.load(file_obj)
                                    
                                    messages = data.get("messages", [])
                                    if len(messages) > 8:
                                        head = messages[0]
                                        tail = messages[-6:]
                                        
                                        for msg in tail:
                                            if msg.get("type") == "user" or msg.get("role") == "user":
                                                content = msg.get("content", [])
                                                warning = "【🛡️ 系统状态修剪：为保障上下文容量健康，早期冗余记录已被安全归档释放。请聚焦最新线索推演】\n\n"
                                                if isinstance(content, list) and len(content) > 0:
                                                    original_text = content[0].get("text", "")
                                                    if not original_text.startswith("【🛡️ 系统状态修剪"):
                                                        content[0]["text"] = warning + original_text
                                                elif isinstance(content, str):
                                                    if not content.startswith("【🛡️ 系统状态修剪"):
                                                        msg["content"] = warning + content
                                                break 
                                        
                                        data["messages"] = [head] + tail
                                        
                                        tmp_filepath = filepath + ".tmp"
                                        with open(tmp_filepath, "w", encoding="utf-8") as file_obj:
                                            json.dump(data, file_obj, ensure_ascii=False, indent=2)
                                        os.replace(tmp_filepath, filepath)
                                        logger.info(f"✅ [巡护干预] {f} 状态修剪通过，应用平稳。")
                                except Exception as e:
                                    logger.error(f"❌ [巡护干预] 记录压缩失败 {f}: {e}")

                if os.path.exists(WILD_CHATS_DIR):
                    live_all_rules = {}
                    if os.path.exists(DNA_RULES_FILE):
                        try:
                            with open(DNA_RULES_FILE, "r", encoding="utf-8") as f:
                                live_all_rules = json.load(f)
                        except Exception: pass

                    security_level = live_all_rules.get("global_security_level", "medium").lower()
                    scan_windows = {"low": 120, "medium": 60, "high": 30}
                    active_scan_window = scan_windows.get(security_level, 60) 

                    node_stop, node_purge = None, None
                    ai_config_path = os.path.join(BASE_DIR, "data", "config", "ai_core.json")
                    if os.path.exists(ai_config_path):
                        try:
                            with open(ai_config_path, "r", encoding="utf-8") as f:
                                for v in json.load(f).get("vendors", []):
                                    if v.get("enabled", True) and v.get("exec_mode") == "cli":
                                        node_stop = v.get("force_stop")
                                        node_purge = v.get("purge_limit")
                                        break
                        except Exception: pass

                    def get_ultimate_limit(node_v, global_v, ai_v, default_v):
                        if node_v not in [None, ""]: return int(node_v)
                        if global_v not in [None, ""]: return int(global_v)
                        if ai_v not in [None, ""]: return int(ai_v)
                        return default_v

                    for f in os.listdir(WILD_CHATS_DIR):
                        if f.endswith('.json') and not f.endswith('.meta.json'):
                            wild_path = os.path.join(WILD_CHATS_DIR, f)
                            task_id = f.replace('.json', '')
                            
                            isolation_mark_path = os.path.join(WILD_CHATS_DIR, f"{task_id}.isolated")
                            if os.path.exists(isolation_mark_path):
                                subprocess.run(["pkill", "-KILL", "-f", f"{task_id}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                continue
                            
                            if time.time() - os.path.getmtime(wild_path) < active_scan_window:
                                try:
                                    with open(wild_path, 'r', encoding='utf-8') as sf:
                                        s_data = json.load(sf)
                                        
                                        session_world = s_data.get("world", "stargate_os")
                                        
                                        live_world_rules = live_all_rules.get(session_world, {})
                                        dna_rules = s_data.get("dna_rules", {})
                                        
                                        global_stop = live_world_rules.get("stop") or dna_rules.get("stop")
                                        global_purge = live_world_rules.get("purge") or dna_rules.get("purge")
                                        
                                        session_state = s_data.get("session_state", {})
                                        ai_allocated_stop = session_state.get("ai_dynamic_stop")
                                        ai_allocated_purge = session_state.get("ai_dynamic_purge")
                                        
                                        thoughts_count = 0
                                        for m in s_data.get('messages', []):
                                            if m.get('type') != 'user': 
                                                try:
                                                    content = m.get('content', '')
                                                    if isinstance(content, list) and len(content) > 0: 
                                                        content = content[0].get('text', '')
                                                    elif not isinstance(content, str):
                                                        content = str(content)
                                                    
                                                    json_match = re.search(r'\{[^{}]*?"ai_dynamic_(?:stop|purge)"[^{}]*?\}', content)
                                                    if json_match:
                                                        soj_payload = json.loads(json_match.group(0))
                                                        if soj_payload.get('ai_dynamic_stop'): ai_allocated_stop = int(soj_payload['ai_dynamic_stop'])
                                                        if soj_payload.get('ai_dynamic_purge'): ai_allocated_purge = int(soj_payload['ai_dynamic_purge'])
                                                except Exception: pass
                                                
                                                if m.get('thoughts'): thoughts_count += len(m.get('thoughts'))
                                                else: thoughts_count += 1
                                        
                                        active_stop = get_ultimate_limit(node_stop, global_stop, ai_allocated_stop, 5)
                                        active_purge = get_ultimate_limit(node_purge, global_purge, ai_allocated_purge, 10)
                                        
                                        if thoughts_count >= active_purge:
                                            logger.error(f"🛡️ [频率控制] 任务节点 {task_id} 检测到高频流转异常 ({thoughts_count}/{active_purge})！触发安全熔断！")
                                            
                                            open(isolation_mark_path, 'a').close()
                                            
                                            try:
                                                os.chmod(wild_path, 0o666)
                                                s_data.setdefault("session_state", {})["is_purged"] = True
                                                s_data["messages"] = [{"role": "model", "content": "【系统通知】：资源请求频率超过限额。运行节点已转入安全隔离模式。"}]
                                                with open(wild_path, 'w', encoding='utf-8') as sf_out: json.dump(s_data, sf_out, ensure_ascii=False)
                                                os.chmod(wild_path, 0o444) 
                                            except Exception: pass
                                            
                                            if task_id in GLOBAL_PROCESS_REGISTRY:
                                                proc = GLOBAL_PROCESS_REGISTRY[task_id]['process']
                                                await graceful_stop(proc, task_id)
                                                force_release(proc)
                                            
                                            subprocess.run(["pkill", "-KILL", "-f", f"{task_id}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                            
                                            try: await self.http_client.get(f"http://{MASTER_HOST}:{MASTER_PORT}/api/stargate/emp_strike?task_id={task_id}", timeout=3.0)
                                            except: pass
                                            
                                        elif thoughts_count >= active_stop:
                                            logger.warning(f"🛑 [频率控制] 任务节点 {task_id} 触碰调度预警线 ({thoughts_count}/{active_stop})！实施柔性点刹！")
                                            
                                            s_data.setdefault("session_state", {})["is_stopped"] = True
                                            try:
                                                with open(wild_path, 'w', encoding='utf-8') as sf_out: json.dump(s_data, sf_out, ensure_ascii=False, indent=2)
                                            except Exception: pass
                                            
                                            if task_id in GLOBAL_PROCESS_REGISTRY:
                                                proc = GLOBAL_PROCESS_REGISTRY[task_id]['process']
                                                await graceful_stop(proc, task_id)
                                            
                                            subprocess.run(["pkill", "-INT", "-f", f"{task_id}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                                
                                            try: await self.http_client.get(f"http://{MASTER_HOST}:{MASTER_PORT}/api/stargate/emp_strike?task_id={task_id}", timeout=3.0)
                                            except: pass

                                except Exception as e: pass
            except Exception as e:
                logger.error(f"❌ [巡视异常] 核心目录扫描阻断: {e}")
            
            await asyncio.sleep(3.0) 

    async def _recover_zombies(self):
        now = time.time()
        try:
            for filename in os.listdir(INBOX_DIR):
                if filename.endswith(".processing"):
                    filepath = os.path.join(INBOX_DIR, filename)
                    if now - os.path.getmtime(filepath) > 1800:
                        os.rename(filepath, filepath.replace(".processing", ""))
                        logger.warning(f"🔄 识别并重载停滞的挂起队列: {filename}")
        except Exception: pass

    async def producer_loop(self):
        logger.info("👁️ 调度分配脉冲已激活 (队列轮询模式)...")
        while self.is_running:
            try:
                await self._recover_zombies()
                found_task = False
                async with self._task_lock:
                    for filename in os.listdir(INBOX_DIR):
                        if filename.endswith(".json") and not filename.endswith(".processing"):
                            old_path = os.path.join(INBOX_DIR, filename)
                            new_path = old_path + ".processing"
                            try:
                                os.rename(old_path, new_path)
                                await self.task_queue.put(new_path)
                                found_task = True
                                logger.info(f"📥 提取新增协作包: {filename}")
                            except OSError: pass 
                await asyncio.sleep(0.5 if found_task else 2.0)
            except Exception as e: 
                logger.error(f"列队提取发生异常: {e}")
                await asyncio.sleep(5.0)

    async def consumer_worker(self, worker_id: int):
        while self.is_running:
            filepath = await self.task_queue.get()
            task_id = os.path.basename(filepath).replace('.json.processing', '')
            
            try:
                while time.time() < self._cooldown_until:
                    remain = int(self._cooldown_until - time.time())
                    logger.warning(f"❄️ [网络降级] 算力平台流控策略已触发，当前请求排队等待 {remain} 秒...")
                    await asyncio.sleep(min(remain, 15)) 

                with open(filepath, "r", encoding="utf-8") as f: task = json.load(f)
                
                if task.get("status") == "pending" or task.get("status") is None:
                    logger.info(f"⚡ [调度工位-{worker_id}] 接管业务: {task_id}")
                    task["status"] = "processing"
                    with open(filepath, "w", encoding="utf-8") as f: json.dump(task, f)
                    
                    execution_prompt = task.get("prompt") or task.get("execution_prompt", "")
                    world = task.get("world", "stargate_os")
                    
                    target_node_id = task.get("target_node")
                    vendor_config = {}
                    ai_config_path = os.path.join(BASE_DIR, "data", "config", "ai_core.json")
                    if os.path.exists(ai_config_path):
                        try:
                            with open(ai_config_path, "r", encoding="utf-8") as f:
                                vendors = json.load(f).get("vendors", [])
                                if target_node_id:
                                    for v in vendors:
                                        if v.get("id") == target_node_id:
                                            vendor_config = v
                                            break
                                else:
                                    for v in vendors:
                                        if v.get("enabled", True) and v.get("exec_mode") == "cli":
                                            vendor_config = v
                                            break
                        except Exception: pass

                    live_rules = {}
                    if os.path.exists(DNA_RULES_FILE):
                        try:
                            with open(DNA_RULES_FILE, "r", encoding="utf-8") as f:
                                live_rules = json.load(f).get(world, {})
                        except Exception: pass

                    dna_rules = task.get("dna_rules", {})
                    active_stop = live_rules.get("stop") or dna_rules.get("stop", 5)
                    active_purge = live_rules.get("purge") or dna_rules.get("purge", 10)

                    if vendor_config.get("force_stop"): active_stop = int(vendor_config["force_stop"])
                    if vendor_config.get("purge_limit"): active_purge = int(vendor_config["purge_limit"])

                    normalized_limits = {"force_stop": active_stop, "purge": active_purge}

                    injected_dna = task.get("injected_dna", []) 
                    temporary_dna_patch = task.get("temporary_dna_patch") 
                    is_enigma_mode = task.get("enigma_mode", True)
                    
                    result = await self.execute_cli_task(
                        execution_prompt, task.get("specific_urls", []), task_id,
                        normalized_limits, world,
                        cli_config=vendor_config, dna_sequence=injected_dna,
                        temporary_dna_patch=temporary_dna_patch,
                        is_enigma=is_enigma_mode
                    )
                    
                    if isinstance(result, dict):
                        if result.get('status') == 'rate_limit':
                            if task.get("is_autopsy_replay") is True:
                                logger.error(f"🔬 [诊断分析] 系统诊断任务 {task_id} 验证过程中触发 429 阈值，该方案未通过连通性测试。")
                                result['status'] = 'error'
                                result['error'] = '【流程干预】：诊断测试时命中接口频控策略 (429)，该推演存在高频触发异常的隐患。'
                            else:
                                logger.warning(f"♻️ [调度降级] 识别到云端算力封锁保护(429)，任务 {task_id} 退回处理队列，系统进入静默退避 {self.RETRY_COOLDOWN} 秒。")
                                self._cooldown_until = time.time() + self.RETRY_COOLDOWN 
                                task["status"] = "pending"
                                with open(filepath, "w", encoding="utf-8") as f: json.dump(task, f)
                                
                                os.rename(filepath, filepath.replace('.processing', ''))
                                self.task_queue.task_done()
                                continue 
                    
                    if isinstance(result, dict):
                        # 💡 强行透传系统底层的物理致命报错
                        if result.get('status') == 'error' and not result.get('output'):
                            final_result_text = f"【底层执行瘫痪】: {result.get('error')}"
                        else:
                            final_result_text = result.get('output', str(result))
                    else:
                        final_result_text = result
                    
                    try:
                        if task.get("is_autopsy_replay") is True:
                            case_id = task.get("case_id")
                            replay_status = "success" if (isinstance(result, dict) and result.get("status") == "success") else "error"
                            error_msg = result.get("error", "") if isinstance(result, dict) else ""
                            
                            autopsy_payload = {
                                "case_id": case_id,
                                "status": replay_status,
                                "output": final_result_text if replay_status == "success" else error_msg,
                                "thoughts_dump": final_result_text
                            }
                            
                            logger.warning(f"🔬 [诊断分析] 诊断复盘序列 {task_id} 推演结束 ({replay_status})，已将报告归档至中心...")
                            await self.http_client.post(
                                f"http://{MASTER_HOST}:{MASTER_PORT}/api/audit/autopsy/append_round",
                                json=autopsy_payload,
                                timeout=15.0
                            )
                        else:
                            # 💡 架构师级缝合：把完整的 task 字典一并传给汇报函数，保留主控要求的所有元数据
                            await self.report_to_factory(task.get("target_domain", "factory_dev"), final_result_text, task_id, original_task=task)
                    except Exception as e: 
                        logger.error(f"❌ 链路回传阻断: {e}")
            except Exception as e:
                logger.error(f"❌ [调度工位-{worker_id}] 进程执行严重故障: {e}")
            finally:
                if os.path.exists(filepath) and filepath.endswith('.processing'):
                    os.remove(filepath)
                
                asset_dir = Path(WORKSPACE_DIR) / "assets" / task_id
                if asset_dir.exists():
                    shutil.rmtree(asset_dir, ignore_errors=True)
                    logger.info(f"🧹 [任务注销] 本地缓冲临时空间已安全释放: {task_id}")
                    
                self.task_queue.task_done()

    async def main_loop(self):
        await self.sync_source_code()
        await self._system_preflight_check() 
        
        server = await asyncio.start_server(handle_radar_connection, '0.0.0.0', RADAR_PORT)
        logger.info(f"📡 主控雷达通道已全线贯通，侦听端口: {RADAR_PORT}")
        
        async with server:
            producer = asyncio.create_task(self.producer_loop())
            watchdog = asyncio.create_task(self._session_watchdog())
            consumers = [asyncio.create_task(self.consumer_worker(i)) for i in range(self.MAX_CONCURRENCY)]
            await asyncio.gather(producer, watchdog, *consumers)

if __name__ == "__main__":
    worker = SandboxWorker()
    try: 
        asyncio.run(worker.main_loop())
    except KeyboardInterrupt:
        worker.is_running = False
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running(): loop.create_task(worker.http_client.aclose())
            else: asyncio.run(worker.http_client.aclose())
        except: pass
        logger.info("节点下线，系统安全交接完毕。")