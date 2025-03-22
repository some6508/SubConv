// HTML 加载时运行
(function () {
	const now = new Date(); // 获取当前时间（基于用户本地时区）
	window.document.title = '运行日志' + now.toISOString();

	// 添加图标
	const link = document.createElement('link');
	link.rel = "icon";
	link.type = "svg";
	link.sizes = "any";
	link.href = `https://icons.qweather.com/assets/icons/${getRandomNumber(1001, 1089)}.svg`;
	document.head.appendChild(link);
	const idTime = localStorage.getItem('idTime');
	if (!idTime) {
		localStorage.setItem('idTime', now.toISOString());
	}
}());

// 添加style
function addGlobalStyle(css) {
	const style = document.createElement('style');
	style.textContent = css; // 更现代的写法，兼容非IE
	// 添加到head
	document.head.appendChild(style);
}

addGlobalStyle(`
table {
	border-collapse: collapse;
	width: 100%;
	margin: 10px;
}
th, td {
	border: 1px solid #ddd;
	padding: 5px;
	text-align: left;
	font-size: 14px;
}
th {
	background-color: #f2f2f2;
}
`);

// HTML 被加载和解析完成后执行的代码
document.addEventListener("DOMContentLoaded", function() {
	const table = document.createElement('table');
	table.id = 'logTable';
	table.innerHTML = `
		<thead>
			<tr>
				<th>时间</th>
				<th>记录</th>
				<th>等级</th>
				<th>IP</th>
				<th>信息</th>
				<th>𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭𑲭</th>
			</tr>
		</thead>
		<tbody id="tableBody"></tbody>
	`;
	document.body.appendChild(table);
});

// 随机数生成
function getRandomNumber(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function Table() {
	// 获取表格id
	const tbody = document.getElementById('tableBody');
	// 中文转为url编码
	const chinesePath = encodeURIComponent("日志");
	// 发送post请求
	const res = await fetch(`./${chinesePath}`, {method: 'POST'});
	if (res.ok) {  // 请求成功
		// 解析json数据
		const data = await res.json();
		// 循环列表
		data.日志.forEach(item => {
			const columns = item.split(' - ');  // 分割内容
			const tr = document.createElement('tr');
			columns.forEach((col, index) => {
				const row = col.replace(/\s+/g, ' ').trim();
				if (col.length > 23) {
					for (let i = index + 1; i < 5; i++) {
						tr.appendChild(document.createElement('td'));
					}
				}
				const td = document.createElement('td');
				if(index === 2) {
					const level = col.trim();
					td.style.color = level === 'INFO' ? 'green' : level === 'WARNING' ? 'orange' : 'red';
				}
				if (index === 4) {
					const textarea = document.createElement('textarea');
					textarea.style.width = '100%';
					textarea.value = row;
					td.appendChild(textarea);
				} else {
					td.textContent = row;
				}
				tr.appendChild(td);
			});
			tbody.appendChild(tr);
		})
	}
}

// IP验证
function IPWithPort(str) {
	// 匹配IPv4地址+端口格式
	const ipPortPattern = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(:[0-9]{1,5})?$/;
	return ipPortPattern.test(str);
}

// HTML加载完成后运行
window.addEventListener("load", async () => {
	await Table();
});
