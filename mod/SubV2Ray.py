import yaml
import json
import base64
import distutils.util
import urllib.parse as urlparse
from fake_useragent import UserAgent


async def 解析(buf):
	try:
		data = base64.b64decode(buf).decode('utf-8')
	except:
		try:
			data = buf.decode('utf-8')
		except:
			data = buf

	arr = data.splitlines()

	proxies = []
	names = {}

	for i in arr:
		if i == "":
			continue
		if -1 == i.find("://"):
			continue
		scheme, body = i.split("://", 1)
		scheme = scheme.lower()

		if scheme == "hysteria":
			try:
				try:
					urlHysteria = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(urlHysteria.query))
				name = 重复名(names, urlparse.unquote(urlHysteria.fragment))
				hysteria = {}

				hysteria["name"] = name
				hysteria["type"] = scheme
				hysteria["server"] = urlHysteria.hostname
				hysteria["port"] = urlHysteria.port
				hysteria["sni"] = query.get("peer")
				hysteria["obfs"] = query.get("obfs")
				alpn = 获取(query.get("alpn"))
				if alpn != "":
					hysteria["alpn"] = alpn.split(",")
				hysteria["auth_str"] = query.get("auth")
				hysteria["protocol"] = query.get("protocol")
				up = 获取(query.get("up"))
				down = 获取(query.get("down"))
				if up == "":
					up = query.get("upmbps")
				if down == "":
					down = query.get("downmbps")
				hysteria["up"] = up
				hysteria["down"] = down
				hysteria["skip-cert-verify"] = bool(
					distutils.util.strtobool(query.get("insecure")))

				proxies.append(hysteria)
			except:
				continue

		elif scheme == "hysteria2" or scheme == "hy2":
			try:
				try:
					urlHysteria2 = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(urlHysteria2.query))
				name = 重复名(names, urlparse.unquote(urlHysteria2.fragment))
				hysteria2 = {}

				hysteria2["name"] = name
				hysteria2["type"] = scheme
				hysteria2["server"] = urlHysteria2.hostname
				port = 获取(urlHysteria2.port)
				if port != "":
					hysteria2["port"] = int(port)
				else:
					hysteria2["port"] = 443
				obfs = 获取(query.get("obfs"))
				if obfs != "" and obfs not in ["none", "None"]:
					hysteria2["obfs"] = query.get("obfs")
					hysteria2["obfs-password"] = 获取(query.get("obfs-password"))
				sni = 获取(query.get("sni"))
				if sni == "":
					sni = 获取(query.get("peer"))
				if sni != "":
					hysteria2["sni"] = sni
				hysteria2["skip-cert-verify"] = bool(
					distutils.util.strtobool(query.get("insecure")))
				alpn = 获取(query.get("alpn"))
				if alpn != "":
					hysteria2["alpn"] = alpn.split(",")
				auth = 获取(urlHysteria2.username)
				if auth != "":
					hysteria2["password"] = auth
				hysteria2["fingerprint"] = 获取(query.get("pinSHA256"))
				hysteria2["down"] = 获取(query.get("down"))
				hysteria2["up"] = 获取(query.get("up"))

				proxies.append(hysteria2)
			except:
				continue

		elif scheme == "tuic":
			try:
				try:
					urlTUIC = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(urlTUIC.query))

				tuic = {}
				tuic["name"] = 重复名(
					names, urlparse.unquote(urlTUIC.fragment))
				tuic["type"] = scheme
				tuic["server"] = urlTUIC.hostname
				tuic["port"] = urlTUIC.port
				tuic["udp"] = True
				password = urlTUIC.password
				if password is not None:
					tuic["uuid"] = urlTUIC.username
					tuic["password"] = password
				else:
					tuic["token"] = urlTUIC.username
				cc = 获取(query.get("congestion_control"))
				if cc != "":
					tuic["congestion-control"] = cc
				alpn = 获取(query.get("alpn"))
				if alpn != "":
					tuic["alpn"] = alpn.split(",")
				sni = 获取(query.get("sni"))
				if sni != "":
					tuic["sni"] = sni
				if query.get("disable_sni") == "1":
					tuic["disable-sni"] = True
				udpRelayMode = 获取(query.get("udp_relay_mode"))
				if udpRelayMode != "":
					tuic["udp-relay-mode"] = udpRelayMode

				proxies.append(tuic)
			except:
				continue

		elif scheme == "trojan":
			try:
				try:
					url_trojan = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(url_trojan.query))
				name = 重复名(names, urlparse.unquote(url_trojan.fragment))
				trojan = {}

				trojan["name"] = name
				trojan["type"] = scheme
				trojan["server"] = url_trojan.hostname
				trojan["port"] = url_trojan.port
				# trojan["password"] = urlTrojan.password if urlTrojan.password is not None else ''
				trojan["password"] = (url_trojan.password if getattr(url_trojan, 'password', None) is not None else
				                      url_trojan.netloc.split('@')[0] if getattr(url_trojan, 'netloc', None) is not None else '')
				trojan["udp"] = True
				trojan["skip-cert-verify"] = bool(
					distutils.util.strtobool(query.get("allowInsecure", "false")))
				sni = 获取(query.get("sni"))
				if sni != "":
					trojan["sni"] = sni

				alpn = 获取(query.get("alpn"))
				if alpn != "":
					trojan["alpn"] = alpn.split(",")

				network = 获取(query.get("type"))
				if network != "":
					network = network.lower()
					trojan["network"] = network

				if network == "ws":
					headers = {}
					wsOpts = {}

					headers["User-Agent"] = RandUserAgent()

					wsOpts["path"] = query.get("path", "/")
					wsOpts["headers"] = headers

					trojan["ws-opts"] = wsOpts

				elif network == "grpc":
					grpcOpts = {}
					grpcOpts["serviceName"] = query.get("serviceName")
					trojan["grpc-opts"] = grpcOpts

				fingerprint = 获取(query.get("fp"))
				if fingerprint == "":
					trojan["client-fingerprint"] = "chrome"
				else:
					trojan["client-fingerprint"] = fingerprint

				proxies.append(trojan)
			except:
				continue

		elif scheme == "vless":
			try:
				try:
					urlVless = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(urlVless.query))
				vless = {}
				try:
					handleVShareLink(names, urlVless, scheme, vless)
				except:
					continue
				flow = 获取(query.get("flow"))
				if flow != "":
					vless["flow"] = str(flow).lower()

				# 清空h2-opts内容
				if 'h2-opts' in vless:
					vless['h2-opts'] = {}
				# 清空reality-opts内容
				if 'reality-opts' in vless:
					vless['reality-opts'] = {}
				if vless.get('port') is None:
					continue
				if vless.get('uuid') is None:
					continue

				proxies.append(vless)
			except:
				continue

		elif scheme == "vmess":
			try:
				try:
					dcBuf = base64.b64decode(body)
				except:
					# Xray VMessAEAD share link
					try:
						urlVMess = urlparse.urlparse(i)
					except:
						continue
					query = dict(urlparse.parse_qsl(urlVMess.query))
					vmess = {}
					try:
						handleVShareLink(names, urlVMess, scheme, vmess)
					except:
						continue
					vmess["alterId"] = 0
					vmess["cipher"] = "auto"
					encryption = 获取(query.get("encryption"))
					if encryption != "":
						vmess["cipher"] = encryption

					proxies.append(vmess)
					continue

				values = {}
				try:
					values = json.loads(dcBuf)
				except:
					continue

				try:
					tempName = values["ps"]
				except:
					continue
				name = 重复名(names, tempName)
				vmess = {}

				vmess["name"] = name
				vmess["type"] = scheme
				vmess["server"] = values["add"]
				vmess["port"] = values["port"]
				vmess["uuid"] = values["id"]
				alterId = values.get("aid")
				if alterId is not None:
					vmess["alterId"] = alterId
				else:
					vmess["alterId"] = 0
				vmess["udp"] = True
				vmess["xudp"] = True
				vmess["tls"] = False
				vmess["skip-cert-verify"] = False

				vmess["cipher"] = "auto"
				cipher = 获取(values.get("scy"))
				if cipher != "":
					vmess["cipher"] = cipher

				sni = 获取(values.get("sni"))
				if sni != "":
					vmess["servername"] = sni

				network = 获取(values.get("net")).lower()
				if values.get("type") == "http":
					network = "http"
				elif network == "http":
					network = "h2"
				vmess["network"] = network

				tls = values.get("tls")
				if tls is not None:
					tls = str(tls).lower()
					if tls.endswith("tls"):
						vmess["tls"] = True
					alpn = values.get("alpn")
					if alpn is not None and alpn != "":
						vmess["alpn"] = alpn.split(",")

				if network == "http":
					headers = {}
					httpOpts = {}
					host = 获取(values.get("host"))
					if host != "":
						headers["Host"] = host
					httpOpts["path"] = "/"
					path = 获取(values.get("path"))
					if path != "":
						httpOpts["path"] = path
					httpOpts["headers"] = headers

					# 清空http-opts内容
					httpOpts.clear()

					vmess["http-opts"] = httpOpts

				elif network == "h2":
					headers = {}
					h2Opts = {}
					host = 获取(values.get("host"))
					if host != "":
						headers["Host"] = host
					h2Opts["path"] = values.get("path", "/")
					h2Opts["headers"] = headers

					# 清空h2-opts内容
					h2Opts.clear()

					vmess["h2-opts"] = h2Opts

				elif network == "ws":
					headers = {}
					wsOpts = {}
					wsOpts["path"] = "/"
					host = 获取(values.get("host"))
					if host != "":
						headers["Host"] = host
					path = 获取(values.get("path"))
					if path != "":
						wsOpts["path"] = path
					wsOpts["headers"] = headers
					vmess["ws-opts"] = wsOpts

				elif network == "grpc":
					grpcOpts = {}
					grpcOpts["grpc-service-name"] = 获取(values.get("path"))
					vmess["grpc-opts"] = grpcOpts

				proxies.append(vmess)
			except:
				continue

		elif scheme == "ss":
			try:
				try:
					urlSS = urlparse.urlparse(i)
				except:
					continue

				name = 重复名(names, urlparse.unquote(urlSS.fragment))
				port = urlSS.port

				if port == "":
					try:
						dcBuf = base64RawStdDecode(urlSS.hostname)
					except:
						continue

					try:
						urlSS = urlparse.urlparse("ss://"+dcBuf)
					except:
						continue

				# there may be bugs
				cipherRaw = urlSS.username
				cipher = cipherRaw
				password = urlSS.password
				if password is None:
					try:
						dcBuf = base64RawStdDecode(cipherRaw)
					except:
						try:
							dcBuf = base64RawURLDecode(cipherRaw)
						except:
							continue
					try:
						cipher, password = dcBuf.split(":", 1)
						if cipher == "ss":
							continue
					except:
						continue
				# ther may be bugs

				ss = {}

				ss["name"] = name
				ss["type"] = scheme
				ss["server"] = urlSS.hostname
				ss["port"] = urlSS.port
				ss["cipher"] = cipher
				ss["password"] = password
				query = dict(urlparse.parse_qsl(urlSS.query))
				ss["udp"] = True
				if 获取(query.get("udp-over-tcp")) == "true" or 获取(query.get("uot")) == "1":
					ss["udp"] = True
				if "obfs" in 获取(query.get("plugin")):
					obfsParam = 获取(query.get("plugin-opts")).split(";")
					ss["plugin"] = "obfs"
					ss["plugin-opts"] = {
						"host": obfsParam[2][10:],
						"mode": obfsParam[1][5:],
					}

				# 跳过密码为空的
				if not ss.get("password"):
					continue

				proxies.append(ss)
			except:
				continue

		elif scheme == "ssr":
			try:
				try:
					dcBuf = base64RawStdDecode(body)
				except:
					continue

				try:
					before, after = dcBuf.split("/?", 1)
				except:
					continue

				beforeArr = before.split(":")

				if len(beforeArr) < 6:
					continue

				host = beforeArr[0]
				port = beforeArr[1]
				protocol = beforeArr[2]
				method = beforeArr[3]
				obfs = beforeArr[4]
				password = base64RawURLDecode(urlSafe(beforeArr[5]))

				try:
					query = dict(urlparse.parse_qsl(urlSafe(after)))
				except:
					continue

				remarks = base64RawURLDecode(query.get("remarks"))
				name = 重复名(names, remarks)

				obfsParam = 获取(query.get("obfsparam"))
				protocolParam = 获取(query.get("protoparam"))

				ssr = {}

				ssr["name"] = name
				ssr["type"] = scheme
				ssr["server"] = host
				ssr["port"] = port
				ssr["cipher"] = method
				ssr["password"] = password
				ssr["protocol"] = protocol
				ssr["udp"] = True

				if obfsParam != "":
					ssr["obfs-param"] = obfsParam

				if protocolParam != "":
					ssr["protocol-param"] = protocolParam

				proxies.append(ssr)
			except:
				continue

		elif scheme == "tg":
			try:
				try:
					urlTG = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(urlTG.query))

				tg = {}
				remark = 获取(query.get("remark"))
				if remark == "":
					remark = 获取(query.get("remarks"))
				if remark == "":
					remark = urlTG.hostname
				tg["name"] = 重复名(names, remark)
				tg["type"] = urlTG.hostname
				tg["server"] = 获取(query.get("server"))
				tg["port"] = str(获取(query.get("port")))
				user = 获取(query.get("user"))
				if user != "":
					tg["username"] = user
				password = 获取(query.get("pass"))
				if password != "":
					tg["password"] = password

				proxies.append(tg)
			except:
				continue

		elif scheme == "https":
			try:
				try:
					urlHTTPS = urlparse.urlparse(i)
				except:
					continue

				query = dict(urlparse.parse_qsl(urlHTTPS.query))

				if not urlHTTPS.hostname.startswith("t.me"):
					return

				tg = {}

				remark = 获取(query.get("remark"))
				if remark == "":
					remark = 获取(query.get("remarks"))
				if remark == "":
					urlHTTPS.path.strip("/")
				tg["name"] = 重复名(names, remark)
				tg["type"] = urlHTTPS.path.strip("/")
				tg["server"] = 获取(query.get("server"))
				tg["port"] = str(获取(query.get("port")))
				user = 获取(query.get("user"))
				if user != "":
					tg["username"] = user
				password = 获取(query.get("pass"))
				if password != "":
					tg["passwork"] = password

				proxies.append(tg)
			except:
				continue

	if proxies:
		return proxies
	else:
		return None


def 重复名(names: dict, name):
	index = names.get(name)
	if index is None:
		index = 0
		names[name] = index
	else:
		index += 1
		names[name] = index
		name = "%s-%02d" % (name, index)
	return name


def 获取(content):
	if content is None:
		return ""
	else:
		return content


def base64RawStdDecode(encoded):
	return base64.b64decode(
		encoded + "="*(-len(encoded)%4)
	).decode("utf-8")


def base64RawURLDecode(encoded):
	return base64.urlsafe_b64decode(
		encoded + "="*(-len(encoded)%4)
	).decode("utf-8")


def urlSafe(string):
	return string.replace("+", "-").replace("/", "_")


def handleVShareLink(names: dict, url: urlparse.ParseResult, scheme: str, proxy: dict):
	query = dict(urlparse.parse_qsl(url.query))
	proxy["name"] = 重复名(names, urlparse.unquote(url.fragment))
	if url.hostname == "":
		raise
	if url.port == "":
		raise
	proxy["type"] = scheme
	proxy["server"] = url.hostname
	proxy["port"] = url.port
	proxy["uuid"] = url.username
	proxy["udp"] = True
	tls = 获取(query.get("security")).lower()
	if tls.endswith("tls") or tls == "reality":
		proxy["tls"] = True
		fingerprint = 获取(query.get("fp"))
		if fingerprint == "":
			proxy["client-fingerprint"] = "chrome"
		else:
			proxy["client-fingerprint"] = fingerprint
		alpn = 获取(query.get("alpn"))
		if alpn != "":
			proxy["alpn"] = alpn.split(",")
	sni = 获取(query.get("sni"))
	if sni != "":
		proxy["servername"] = sni
	realityPublicKey = 获取(query.get("pbk"))
	if realityPublicKey != "":
		proxy["reality-opts"] = {
			"public-key": realityPublicKey,
			"short-id": 获取(query.get("sid"))
		}

	switch = 获取(query.get("packetEncoding"))
	if switch == "none" or switch == "":
		pass
	elif switch == "packet":
		proxy["packet-addr"] = True
	else:
		proxy["xudp"] = True

	network = 获取(query.get("type")).lower()
	if network == "":
		network = "tcp"
	fakeType = 获取(query.get("headerType")).lower()
	if fakeType == "http":
		network = "http"
	elif network == "http":
		network = "h2"
	proxy["network"] = network
	if network == "tcp":
		if fakeType != "none" and fakeType != "":
			headers = {}
			httpOpts = {}
			httpOpts["path"] = "/"

			host = 获取(query.get("host"))
			if host != "":
				headers["Host"] = str(host)

			method = 获取(query.get("method"))
			if method != "":
				httpOpts["method"] = method

			path = 获取(query.get("path"))
			if path != "":
				httpOpts["path"] = str(path)

			httpOpts["headers"] = headers
			proxy["http-opts"] = httpOpts

	elif network == "http":
		headers = {}
		h2Opts = {}
		h2Opts["path"] = "/"
		path = 获取(query.get("path"))
		if path != "":
			h2Opts["path"] = str(path)
		host = 获取(query.get("host"))
		if host != "":
			h2Opts["host"] = str(host)
		h2Opts["headers"] = headers
		proxy["h2-opts"] = h2Opts

	elif network == "ws":
		headers = {}
		wsOpts = {}
		headers["User-Agent"] = RandUserAgent()
		headers["Host"] = 获取(query.get("host"))
		wsOpts["path"] = 获取(query.get("path"))
		wsOpts["headers"] = headers

		earlyData = 获取(query.get("ed"))
		if earlyData != "":
			try:
				med = int(earlyData)
			except:
				raise
			wsOpts["max-early-data"] = med
		earlyDataHeader = 获取(query.get("edh"))
		if earlyDataHeader != "":
			wsOpts["early-data-header-name"] = earlyDataHeader

		proxy["ws-opts"] = wsOpts

	elif network == "grpc":
		grpcOpts = {}
		grpcOpts["grpc-service-name"] = 获取(query.get("serviceName"))
		proxy["grpc-opts"] = grpcOpts


def RandUserAgent() -> str:
	# 创建UserAgent对象
	ua = UserAgent()
	# 生成随机User-Agent
	return ua.random


def proxies_info(info, args):
	data = yaml.safe_load(info)
	num = len(data.get('proxies'))
	proxies = []
	n = 0
	proxies_num = {"name": f"节点共有{num}条", "type": "http", "server": "127.0.0.1", "port": 443}
	proxies.append(proxies_num)
	# data.get('proxies').insert(0, proxies_num)
	if args.get('raw_data'):
		data_info = {"name": f"流量{args['remaining']}/{args['total']}|{args['expire']}", "type": "http", "server": "127.0.0.1", "port": 443}
		proxies.append(data_info)
	# data.get('proxies').insert(0, data_info)
	for proxy in data.get('proxies', []):
		n += 1
		proxy['name'] = f"[{n}]{proxy.get('name')}"
		proxies.append(proxy)
	data['proxies'] = proxies
	return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


async def Sub(data, **kwargs):
	try:
		proxies = yaml.safe_dump(
			{"proxies": yaml.load(data, Loader=yaml.FullLoader).get("proxies")},
			allow_unicode=True,
			sort_keys=False
		)
		proxies = proxies_info(proxies, kwargs.get('headers'))
	except:
		proxies = yaml.safe_dump(
			{"proxies": await 解析(data)},
			allow_unicode=True,
			sort_keys=False
		)
		proxies = proxies_info(proxies, kwargs.get('headers'))
	return proxies
