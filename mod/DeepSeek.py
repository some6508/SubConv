import random
import base64
import string
import urllib.parse
from datetime import datetime


async def parse_info(headers):
	"""增强版流量信息解析器，支持无限流量和RFC编码"""

	def parse_sub_params(header_value):
		"""处理包含Infinity的特殊数值解析"""
		params = {}
		for item in header_value.split(';'):
			item = item.strip()
			if not item:
				continue

			# 处理键值分割
			if '=' not in item:
				continue

			key, value = item.split('=', 1)
			key = key.strip().lower()
			value = value.strip()

			# 特殊值处理
			if value.lower() == 'infinity':
				params[key] = float('inf')
			elif not value:  # 空值处理
				params[key] = None
			else:
				# 数值转换尝试
				try:
					params[key] = int(value)
				except ValueError:
					params[key] = value  # 保留原始值

		return params

	def parse_filename(header_value):
		"""增强版文件名解析，处理多编码声明"""
		filename = None

		# 优先处理RFC 5987编码格式
		for part in header_value.split(';'):
			part = part.strip()
			if part.lower().startswith('filename*='):
				try:
					# 分割编码声明和值
					_, encoded_part = part.split('*=', 1)

					# 处理带字符集的格式：utf-8''filename
					if "'" in encoded_part:
						charset, _, filename_enc = encoded_part.split("'", 2)
						filename_bytes = urllib.parse.unquote_to_bytes(filename_enc)
						filename = filename_bytes.decode(charset)
					else:
						# 无字符集声明时默认UTF-8
						filename_bytes = urllib.parse.unquote_to_bytes(encoded_part)
						filename = filename_bytes.decode('utf-8')
					break
				except (ValueError, LookupError, UnicodeDecodeError):
					continue

		# 回退到普通filename参数
		if not filename:
			for part in header_value.split(';'):
				part = part.strip()
				if part.lower().startswith('filename='):
					filename = part.split('=', 1)[1].strip('" ')
					filename = urllib.parse.unquote(filename)
					break

		return filename or ""

	def format_flow(value):
		"""智能流量格式化，支持无限大"""
		if isinstance(value, float) and value == float('inf'):
			return "∞"

		if not isinstance(value, (int, float)) or value < 0:
			return "0.00 B"

		units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
		unit_idx = 0
		value = float(value)

		while value >= 1024 and unit_idx < len(units)-1:
			value /= 1024
			unit_idx += 1

		return f"{value:.2f} {units[unit_idx]}" if unit_idx > 0 else f"{int(value)} B"

	def format_expire(timestamp):
		"""时间戳转换增强版"""
		if not isinstance(timestamp, (int, float)) or timestamp <= 0:
			return "无到期时间"

		try:
			# 处理32位系统限制
			max_timestamp = 32503680000  # 3000-01-01
			if timestamp > max_timestamp:
				return "永久有效"

			return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
		except (ValueError, OSError):
			return "时间格式无效"

	# 主解析流程
	info = parse_sub_params(headers.get('subscription-userinfo', ''))

	# 核心参数提取
	upload = info.get('upload', 0) or 0
	download = info.get('download', 0) or 0
	total = info.get('total', 0) or 0
	expire = info.get('expire')

	# 流量计算逻辑
	is_infinite = isinstance(total, float) and total == float('inf')
	used = download
	try:
		remaining = float('inf') if is_infinite else (total - download if total >= download else 0)
	except:
		remaining = float('inf')

	return {
		'filename': parse_filename(headers.get('content-disposition', '')),
		'upload': format_flow(upload),
		'download': format_flow(download),
		'total': format_flow(total),
		'used': format_flow(used),
		'remaining': format_flow(remaining),
		'expire': format_expire(expire),
		'raw_data': info
	}


def random_string(length=8):
	"""生成随机变量名"""
	chars = string.ascii_letters + string.digits
	return ''.join(random.choices(chars, k=length))


def dynamic_obfuscate(js_code):
	with open(js_code, 'r') as f:
		js_code = f.read()
	# Base64编码原始代码
	encoded_js = base64.b64encode(js_code.encode()).decode()

	# 生成随机变量名
	var_name = random_string()

	# 构建混淆后的JS代码
	obfuscated = [
		"(function(){",
		f"  var {var_name}=['" + encoded_js + "'];",
		f"  var decodedCode = new TextDecoder('utf8').decode(Uint8Array.from(atob({var_name}), c => c.charCodeAt(0)));",
		"  if (typeof console !== 'undefined') {",
		"	setInterval(function(){ debugger; }, 1000);",
		"  }",
		"  new Function(decodedCode)();",
		"})();"
	]
	return '\n'.join(obfuscated)
