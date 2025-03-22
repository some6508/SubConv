import yaml
import random
from . import config
from urllib.parse import urlparse, urlencode


async def pack(数据: list, 节点: list, 域名: str, 列表: bool):
	result = {}
	result.update(config.configInstance.HEAD)

	# 添加V2节点
	proxies = {"proxies": []}
	if 节点:
		for i in 节点:
			proxies["proxies"].append(i)
		result.update(proxies)

	if not 列表:
		# 添加网络订阅
		providers = {"proxy-providers": {}}
		if 数据:
			for i in range(len(数据)):
				providers["proxy-providers"].update({
					"{}".format(数据[i]["订阅"]): {
						"type": "http",
						"url": 数据[i]["链接"],
						"interval": 1800,
						"path": f'./sub/{数据[i]["订阅"].split("@")[0]}.yaml',
						"health-check": {
							"enable": True,
							"interval": 300,
							"url": config.configInstance.TEST_URL
						},
						"override": {
							"additional-prefix": f'{数据[i]["订阅"].split("@")[0]}@'
							# "additional-suffix": f"@{u}"
						}
					}
				})
			result.update(providers)
	else:
		if 数据:
			for i in range(len(数据)):
				内容 = yaml.load(数据[i]["数据"], Loader=yaml.FullLoader).get("proxies")
				for n in 内容:
					if n not in proxies["proxies"]:
						proxies["proxies"].append(n)
			result.update(proxies)

	# 添加分组
	proxyGroups = {
		"proxy-groups": []
	}
	proxySelect = {
		"name": "🚀 节点选择",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Proxy.png",
		"type": "select",
		"proxies": []
	}
	for i in ["♻️ 自动选择", "☁️ 故障转移", "🔮 负载均衡", "🖲️ 手动选择"]:
		proxySelect["proxies"].append(i)
	if 节点:
		proxySelect["proxies"].append('⛱️ 附加来源')
	if not 列表:
		for i in range(len(数据)):
			proxySelect["proxies"].append("🏖 " + 数据[i]["订阅"])
	proxySelect["proxies"].append("DIRECT")
	proxyGroups["proxy-groups"].append(proxySelect)

	proxyGroup = []
	proxyGroup.append({
		"name": "♻️ 自动选择",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Auto.png",
		"type": "url-test",
		"include-all": True,
		"interval": 300,
		"url": config.configInstance.TEST_URL
	})
	proxyGroup.append({
		"name": "☁️ 故障转移",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Available.png",
		"type": "fallback",
		"include-all": True,
		"interval": 300,
		"url": config.configInstance.TEST_URL
	})
	proxyGroup.append({
		"name": "🔮 负载均衡",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Round_Robin.png",
		"type": "load-balance",
		"include-all": True,
		"interval": 300,
		"url": config.configInstance.TEST_URL
	})
	proxyGroup.append({
		"name": "🖲️ 手动选择",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Direct.png",
		"type": "select",
		"include-all": True,
		"proxies": [
			"DIRECT"
		]
	})

	proxyGroup.append({
		"name": "🎯 直连访问",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Loop.png",
		"type": "select",
		"proxies": [
			"DIRECT",
			"REJECT",
			"🚀 节点选择"
		]
	})
	proxyGroup.append({
		"name": "🛑 拦截访问",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Reject.png",
		"type": "select",
		"proxies": [
			"REJECT",
			"DIRECT",
			"🚀 节点选择"
		]
	})
	proxyGroup.append({
		"name": "🐟 漏网之鱼",
		"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Lab.png",
		"type": "select",
		"proxies": [
			"🚀 节点选择",
			"DIRECT",
			"REJECT"
		]
	})

	if 节点:
		proxyGroup.append({
			"name": "⛱️ 附加来源",
			"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Static_1.png",
			"type": "select",
			"include-all-proxies": True,
			"proxies": [
				"DIRECT"
			]
		})
	if not 列表:
		for i in range(len(数据)):
			proxyGroup.append({
				"name": "🏖 {}".format(数据[i]["订阅"]),
				"icon": "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Static_1.png",
				"type": "select", # load-balance fallback
				"use": [
					数据[i]["订阅"]
				]
			})

	# 添加分组合集
	proxyGroups["proxy-groups"].extend(proxyGroup)
	result.update(proxyGroups)

	# 添加规则集
	rule_providers = {
		"rule-providers": {}
	}
	rule_map = {}
	classical = {
		"type": "http",
		"interval": 86400 * 7,
	}
	for item in config.configInstance.RULESET:
		url = item[1]
		name = urlparse(url).path.split("/")[-1].split(".")[0]
		if ".mrs" in url:
			types = "mrs"
			classical["behavior"] = "domain"
			classical["format"] = "mrs"
		elif ".yaml" in url:
			types = "yaml"
			classical["behavior"] = "domain"
			classical["format"] = "yaml"
		else:
			types = "txt"
			classical["behavior"] = "classical"
			classical["format"] = "text"

		while name in rule_map:
			name += str(random.randint(0, 9))
		rule_map[name] = item[0]
		if url.startswith("[]"):
			continue
		if ",http" in url:
			url = url.replace(",http", "")
		else:
			url = "{}proxy?{}".format(域名, urlencode({"url": url}))

		rule_providers["rule-providers"].update({
			name: {
				**classical,
				"path": "./rule/{}.{}".format(name, types),
				"url": url
			}
		})
	result.update(rule_providers)

	# 添加规则
	rules = {
		"rules": []
	}
	# 域名直连
	# rules["rules"].append(
	# f"DOMAIN,{domain},DIRECT"
	# )
	for k, v in rule_map.items():
		if not k.startswith("[]"):
			rules["rules"].append(
				f"RULE-SET,{k},{v}"
			)
		elif k[2:] != "FINAL" and k[2:] != "MATCH":
			if ",no-resolve," in k:
				n = k[2:].replace(",no-resolve,", "")
				rules["rules"].append(
					f"{n},{v},no-resolve"
				)
			else:
				rules["rules"].append(
					f"{k[2:]},{v}"
				)
		else:
			rules["rules"].append(
				f"MATCH,{v}"
			)

	result.update(rules)

	yaml.SafeDumper.ignore_aliases = lambda *args : True
	return yaml.safe_dump(result, allow_unicode=True, sort_keys=False)
