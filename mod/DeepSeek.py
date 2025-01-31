import urllib.parse
from datetime import datetime


async def parse_info(headers):
	"""解析包含流量信息的HTTP头信息"""
	def parse_sub_params(header_value):
		"""解析subscription-userinfo参数"""
		params = {}
		for item in header_value.split(';'):
			item = item.strip()
			if not item:
				continue
			try:
				key, value = item.split('=', 1)
				key = key.strip().lower()
				value = value.strip()

				# 处理空值和数值转换
				if not value:
					params[key] = None
				else:
					try:
						params[key] = int(value)
					except ValueError:
						params[key] = value  # 保留原始字符串值
			except ValueError:
				continue
		return params

	def parse_filename(header_value):
		"""解析RFC 5987编码的文件名"""
		filename = None
		for part in header_value.split(';'):
			part = part.strip()
			if part.lower().startswith('filename*='):
				# 处理编码文件名
				value_part = part.split('*=', 1)[-1]
				if "'" in value_part:
					try:
						charset, _, filename_enc = value_part.split("'", 2)
						filename_bytes = urllib.parse.unquote_to_bytes(filename_enc)
						filename = filename_bytes.decode(charset)
					except (ValueError, LookupError, UnicodeDecodeError):
						pass
				else:
					filename_bytes = urllib.parse.unquote_to_bytes(value_part)
					filename = filename_bytes.decode('utf-8', errors='replace')
				break

		# 回退到普通filename参数
		if filename is None:
			for part in header_value.split(';'):
				part = part.strip()
				if part.lower().startswith('filename='):
					filename = part.split('=', 1)[-1].strip('" ')
					filename = urllib.parse.unquote(filename)
					break

		return filename or ""

	def format_flow(bytes_num):
		"""智能转换流量单位"""
		if bytes_num is None or bytes_num < 0:
			return "0.00 B"

		units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
		unit_idx = 0
		while bytes_num >= 1024 and unit_idx < 5:
			bytes_num /= 1024
			unit_idx += 1
		return f"{bytes_num:.2f} {units[unit_idx]}"

	# 主解析逻辑
	info = parse_sub_params(headers.get('subscription-userinfo', ''))

	# 获取核心参数（带默认值）
	upload = info.get('upload', 0) or 0
	download = info.get('download', 0) or 0
	total = info.get('total', 0) or 0
	expire = info.get('expire')

	# 计算衍生指标
	used = download  # 根据业务逻辑定义已用流量
	remaining = total - download if isinstance(total, int) and isinstance(download, int) else 0

	# 时间戳转换
	expire_str = "长期"
	if isinstance(expire, int) and expire > 0:
		try:
			expire_str = datetime.utcfromtimestamp(expire).strftime('%Y-%m-%d %H:%M:%S UTC')
		except (ValueError, OSError):
			expire_str = "无效时间戳"

	return {
		'filename': parse_filename(headers.get('content-disposition', '')),
		'upload': format_flow(upload),
		'download': format_flow(download),
		'total': format_flow(total),
		'used': format_flow(used),
		'remaining': format_flow(remaining),
		'expire': expire_str,
		'raw_data': info  # 原始参数信息
	}
