#!/usr/bin/env python3
# coding=utf-8
import re
import os
import time
import httpx
import random
import uvicorn
import logging
import tempfile
import argparse
import aiofiles
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, StreamingResponse, RedirectResponse, HTMLResponse, JSONResponse


# 自定义
from mod import SubV2Ray, SubPack, DeepSeek
run_name = 'SubConv'

# 动态获取系统临时目录
log_temp_dir = os.path.join(tempfile.gettempdir(), run_name)
log_filename = os.path.join(log_temp_dir, 'ccaeo.log')
# 确保目录存在
os.makedirs(log_temp_dir, exist_ok=True)

# 配置根日志记录器
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	handlers=[
		RotatingFileHandler(
			filename=log_filename,
			maxBytes=1 * 1024 * 1024,
			backupCount=3
		),
		logging.StreamHandler()
	]
)


# 开始运行
if __name__ == "__main__":
	# 设置默认参数
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", "-P", type=int, default=8080, help="端口设置, 默认: 8080")
	parser.add_argument("--host", "-H", type=str, default="0.0.0.0", help="IP设置, 默认: 0.0.0.0")
	parser.add_argument("--version", "-V", action="version", version="版本: v1.0.0（20250120）")
	args = parser.parse_args()

	# 脚本名
	module_name = __name__.split(".")[0]

	logging.info(f"{module_name} - 开始运行: {run_name}")
	logging.info(f"{module_name} - IP:端口: {args.host}:{args.port}")
	logging.info(f"{module_name} - 日志文件: {log_filename}")
	# 运行
	uvicorn.run(module_name + ":app", host=args.host, port=args.port, workers=4, log_config=None)

# 服务器端
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


# 全局异常捕获中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
	start_time = time.time()

	try:
		response = await call_next(request)
	except Exception as e:
		logging.error(f"请求错误: {str(e)}")
		raise

	# 计算处理时间
	process_time = (time.time() - start_time) * 1000
	process_time = round(process_time, 2)

	# 记录请求完成
	logging.info(
		f"请求: {request.method} {request.url.path} "
		f"响应码: {response.status_code} "
		f"响应时间: {process_time}ms"
	)
	return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	logging.error(f"未处理异常: {exc}")
	raise


@app.get("/")
async def 主页():
	# 生成随机数
	random_number = random.random()
	current_time = datetime.now().isoformat()
	async with aiofiles.open("static/index.html", "r", encoding="utf-8") as f:
		lines = await f.readlines()
		html_content = "\n".join(lines)

		# 在head标签内插入
		# script_tag = f'<script src="script-6038eb19.js?v={random_number}"></script>'
		script_tag = f'<script src="script-6038eb19.js?t={current_time}"></script>'
		html_content = html_content.replace('</head>', script_tag + '</head>')
		return HTMLResponse(content=html_content)


@app.get("/robots.txt")
async def robots():
	return Response(content="User-agent: *\nDisallow: /", media_type="text/plain")


@app.get("/provider")
async def provider(request: Request):
	headers = {'Content-Type': 'text/yaml;charset=utf-8'}
	url = request.query_params.get("url")
	url_ua = request.headers.get('User-Agent', 'clash-verge/v1.6.6')
	if "clash" not in url_ua:
		url_ua = "clash-verge/v1.6.6"
	timeout = httpx.Timeout(10.0, connect=30.0)  # 总超时10秒，连接超时30秒
	async with httpx.AsyncClient(timeout=timeout) as client:
		try:
			resp = await client.get(url, headers={'User-Agent': url_ua}, follow_redirects=True)
			if resp.status_code != 200:
				raise HTTPException(status_code=resp.status_code, detail=f"请求失败{url}")
			if resp.text:
				Headers = await DeepSeek.parse_info(resp.headers)
				result = await SubV2Ray.Sub(resp.text, headers=Headers)
			# 获取当前时间并格式化
			current_time = datetime.now().isoformat()
			result = f"# 由{run_name}一键生成\n# {current_time}\n{result}\n# {current_time}\n# 由{run_name}一键生成"
			if 'Subscription-Userinfo' in resp.headers:  # 流量及日期信息
				headers['Subscription-Userinfo'] = resp.headers['Subscription-Userinfo']
			if 'Content-Disposition' in resp.headers:  # 订阅名
				headers['Content-Disposition'] = resp.headers['Content-Disposition'].replace("attachment", "inline")
				# 使用正则表达式去除 filename= 部分
				pattern = r';\s*filename=[^;]*'
				headers['Content-Disposition'] = re.sub(pattern, '', headers['Content-Disposition'])
		except Exception as e:
			logging.error(f"错误来源: {e.__class__.__name__} 请求链接: {url}")
			raise HTTPException(status_code=404, detail="出现请求错误")
	return Response(content=result, headers=headers)


@app.get("/sub")
async def sub(request: Request):
	args = request.query_params

	# 获取域名或ip
	domain = re.search(r"([^:]+)(:\d{1,5})?", request.url.hostname).group(1)
	base_url = str(request.base_url)
	if "127.0.0.1" in base_url:  # 如果是本地ip
		forwarded_host = request.headers.get("X-Forwarded-Host") or request.headers.get("X-Host", "").split(":")[0]
		if forwarded_host:
			base_url = f"https://{forwarded_host}/"
			domain = forwarded_host

	# 是否全部输出代理列表
	all_list = args.get("all", False)

	# 获取请求UA
	url_ua = request.headers.get('User-Agent', 'clash-verge/v1.6.6')
	if "clash" not in url_ua:  # 如果不是clash
		url_ua = "clash-verge/v1.6.6"
	headers = {'Content-Type': 'text/yaml; charset=utf-8', 'Content-Disposition': f"inline; filename*=utf-8''{run_name}", 'Subscription-Userinfo': f'upload=0; download={int(time.time())}; total=1099511627776; expire={int(time.time())}'}

	# 从args获取链接
	url = args.get("url", "")
	url = re.split(r"[|\n]", url)
	tmp = list(filter(lambda x: x != "", url))
	if not tmp:
		raise HTTPException(status_code=404, detail="！没有参数")
	url = []  # 链接
	urls = []  # v2
	for i in tmp:  # 判断文件
		if (i.startswith("http://") or i.startswith("https://")) and not i.startswith("https://t.me/"):
			url.append(i)
		else:
			urls.append(i)

	urls = "\n".join(urls)
	# 如果有v2先解析
	urls = await SubV2Ray.解析(urls)

	timeout = httpx.Timeout(10.0, connect=30.0)  # 总超时10秒，连接超时30秒
	async with httpx.AsyncClient(timeout=timeout) as client:
		data = []
		for i in range(len(url)):
			try:
				response = await client.get(url[i], headers={'User-Agent': url_ua}, follow_redirects=True)
				if response.status_code == 200:
					if response.text == "":
						logging.warning("链接内容为空:", url[i])
						continue
					url_headers = await DeepSeek.parse_info(response.headers)
					temp = {"链接": "{}provider?{}".format(base_url, urlencode({"url": url[i]}))}
					if url_headers['filename']:  # 订阅名
						temp["订阅"] = "{:02}@".format(i) + url_headers['filename']
					else:
						temp["订阅"] = "{:02}@订阅来源".format(i)

					temp["数据"] = await SubV2Ray.Sub(response.text, headers=url_headers)
					data.append(temp)
				else:
					logging.warning(f"请求失败 {response.status_code}: {url[i]}")
			except Exception as e:
				logging.error(f"错误来源: {e.__class__.__name__} 请求链接: {url[i]}")
		if data or urls:
			result = await SubPack.pack(数据=data, 节点=urls, 域名=base_url, 列表=all_list)
			# 获取当前时间并格式化
			current_time = datetime.now().isoformat()
			headers['Content-Disposition'] = headers['Content-Disposition'] + f"-{current_time}"
			result = f"# 由{run_name}一键生成\n# {current_time}\n{result}\n# {current_time}\n# 由{run_name}一键生成"
		else:
			raise HTTPException(status_code=404, detail="请求出现错误")
	return Response(content=result, headers=headers)


@app.get("/proxy")
async def proxy(request: Request, url: str):
	url_ua = request.headers.get('User-Agent', 'clash-verge/v1.6.6')
	timeout = httpx.Timeout(10.0, connect=30.0)  # 总超时10秒，连接超时30秒

	# file was big so use stream
	async def stream():
		async with httpx.AsyncClient(timeout=timeout) as client:
			async with client.stream("GET", url, headers={'User-Agent': url_ua}, follow_redirects=True) as resp:
				yield resp.status_code
				yield resp.headers
				if resp.status_code < 200 or resp.status_code >= 400:
					yield await resp.aread()
					return
				async for chunk in resp.aiter_bytes():
					yield chunk

	streamResp = stream()
	status_code = await streamResp.__anext__()
	headers = await streamResp.__anext__()
	if status_code < 200 or status_code >= 400:
		raise HTTPException(status_code=status_code, detail=await streamResp.__anext__())
	return StreamingResponse(streamResp, media_type=headers['Content-Type'])


@app.get("/日志")
@app.post("/日志")
async def 日志(request: Request):
	if request.method == "POST":
		headers = request.headers
		log_file_path = Path(log_filename)

		try:
			async with aiofiles.open(log_file_path, "r", encoding="utf-8") as f:
				lines = await f.readlines()
				# last_line = lines[-1000:]  # 显示后面1000行内容
				reversed_lines = lines[::-1]  # 反转行顺序
				return {"响应头": headers, "日志": reversed_lines}
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="没有日志文件")
		except Exception as e:
			raise HTTPException(status_code=500, detail=str(e))
	else:
		current_time = datetime.now().isoformat()
		async with aiofiles.open("static/index.html", "r", encoding="utf-8") as f:
			lines = await f.readlines()
			html_content = "\n".join(lines)
		# 在head标签内插入
		script_tag = f'<script src="log-6038eb19.js?t={current_time}"></script>'
		html_content = html_content.replace('</head>', script_tag + '</head>')
		return HTMLResponse(content=html_content)


# 如果没有相应请求
@app.get("/{path:path}")
async def index(path):
	if Path("static/" + path).exists():
		# if '.js' in path:
		# result = DeepSeek.dynamic_obfuscate("static/" + path)
		# return Response(content=result, headers={'Content-Type': 'application/javascript'})
		return FileResponse("static/" + path)
	else:
		result = 'https://t.me/CcaeoBot'
		return RedirectResponse(url=result, status_code=302, headers={"Location": result})
