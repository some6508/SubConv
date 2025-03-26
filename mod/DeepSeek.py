import re
import random
import base64
import string
from urllib.parse import unquote
from datetime import datetime, timezone


async def parse_info(headers):
	# 提取订阅信息
	sub_info = headers.get('Subscription-Userinfo', '')
	sub_dict = {}
	for item in sub_info.split(';'):
		item = item.strip()
		if '=' in item:
			key, value = item.split('=', 1)
			sub_dict[key.strip().lower()] = value.strip()

	# 流量转换函数
	def convert_traffic(value):
		if value.lower() == 'infinity' or not re.match(r'^[\d.]+(e[+-]?\d+)?$', value):
			return '∞'
		try:
			num = float(value)
			if num == float('inf'):
				return '∞'
		except:
			return '∞'

		units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
		unit_index = 0
		while num >= 1024 and unit_index < len(units)-1:
			num /= 1024
			unit_index += 1
		return f"{num:.2f} {units[unit_index]}" if unit_index > 0 else f"{int(num)} B"

	# 处理时间戳
	expire_date = '长期有效'
	if sub_dict.get('expire'):
		try:
			timestamp = int(sub_dict['expire'])
			dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
			expire_date = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
		except:
			expire_date = '无效时间戳'

	# 处理文件名
	content_disposition = headers.get('Content-Disposition', '')
	parts = [p.strip() for p in content_disposition.split(';')]
	filename = None
	for part in parts:
		if part.lower().startswith('filename*='):
			value = part.split('=', 1)[1].strip()
			if "''" in value:
				charset, fname = value.split("''", 1)
				filename = unquote(fname, encoding=charset.strip())
			else:
				filename = unquote(value)
			break
		elif part.lower().startswith('filename=') and not filename:
			value = part.split('=', 1)[1].strip()
			filename = value.strip('"')

	return {
		'upload': convert_traffic(sub_dict.get('upload', '0')),
		'download': convert_traffic(sub_dict.get('download', '0')),
		'total': convert_traffic(sub_dict.get('total', '0')),
		'expire': expire_date,
		'filename': filename or '',
		'raw_data': sub_dict
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
