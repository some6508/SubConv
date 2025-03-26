// HTML 加载时运行
(function () {
	const now = new Date(); // 获取当前时间（基于用户本地时区）
	window.document.title = '订阅转换' + now.toISOString();

	// 添加图标
	const link = document.createElement('link');
	link.rel = "icon";
	link.type = "svg";
	link.sizes = "any";
	// link.href = "https://www.gstatic.cn/images/branding/product/2x/google_cloud_64dp.png";
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
/* 全局变量 */
:root {
	--color-a: #F596AA;
	--color-b: #66CCFF;
	--color-c: #00FF88;
	--angle: ${angles()};  /* 随机渐变角度 */
	--color-body: ${generateRandomColors(5)};  /* 随机渐变颜色 */
}

/* 淡入效果 */
@keyframes fadeIn {
	from { opacity: 0; }
	to { opacity: 1; }
}
/* 应用动画到所有元素 */
* {
	animation: fadeIn 1s ease-in-out;
}

* {
	margin: 0;
	padding: 0;
}

/* 渐变背景 */
body {
	width: 100%;
	height: 100%;
	color: white;
	text-align: center;
	font-family: 'Arial', sans-serif;
	background: linear-gradient(var(--angle), var(--color-body));
	background-size: 400% 400%;
	animation: gradient 7s ease infinite;
	transition: all 1s ease;
}
@keyframes gradient {
	0% { background-position: 0% 50%; }
	50% { background-position: 100% 50%; }
	100% { background-position: 0% 50%; }
}

#Container {
	margin: 20px;
}

/* 输入输出区域样式 */
textarea {
	width: 100%;
	height: 100px;
	margin: 10px auto;
	border: 2px solid ${getRandomColor()};
	border-radius: 8px;
	resize: vertical;
	font-size: 14px;
	background-color: rgba(255, 255, 255, .1);
	${randomColor()}
}

/* 按钮容器布局 */
.button-group {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
	gap: 10px;
	margin: 15px 0;
}
/* Android端*/
@media (max-width: 768px) {
	.button-group {
		grid-template-columns: repeat(auto-fit, minmax(30%, 1fr));
		justify-content: start;
	}
}

/* 按钮通用样式 */
button {
	padding: 10px 20px;
	border: none;
	border-radius: 6px;
	cursor: pointer;
	color: white;
	transition: all 0.3s ease;
	font-weight: bold;
	${randomColor()}
}

/* 按钮悬停效果 */
button:hover {
	transform: translateY(-2px);
	${randomColor()}
}

/* 结果展示区域 */
#resultContainer {
	margin-top: 20px;
	display: none;  /* 初始隐藏 */
}

/* 页脚部分 */
#footer {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 8px;
	text-align: center;
	font-size: 0.8em;
	color: white;
	box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
	backdrop-filter: blur(5px);
}

/* 深色 */
@media (prefers-color-scheme: dark) {
}

/*设置渐变色文字*/
.footer, .toast, .contact-btn, .hitokoto, .ip-info, .adaptive, .popup {
	background: 
		-webkit-linear-gradient(-45deg, ${generateRandomColors(5,2)});
		-moz-linear-gradient(-45deg, ${generateRandomColors(5,2)});
		-linear-gradient(-45deg, ${generateRandomColors(5,2)});
	background-size: 400% 400%;  /* 将背景图像放大，以便在动画中移动时产生平滑的过渡效果*/
	background-clip: text;  /* 将背景限制在文字范围内 */
	color: transparent;  /* 文字颜色透明（重要：让背景可见） */
	animation: gradientAnimation 3s linear infinite;
	-moz-animation: gradientAnimation 3s linear infinite;
	-webkit-animation: gradientAnimation 3s linear infinite;
	-webkit-background-clip: text;  /* WebKit增强背景裁剪效果 */
	-webkit-text-fill-color: transparent;  /* WebKit浏览器文字透明 */
}
@keyframes gradientAnimation {
	0% { background-position: 100% 100%; }
	100% { background-position: 100vw 100vh; }
}

/* 默认使用竖图 */
.background {
	/*background-image: url('https://api.rls.ovh/vertical');*/
	background-size: cover;
	background-position: center;
	z-index: -1;
}
/* 当前分辨率宽大于高时，使用横图 */
@media (orientation: landscape) {
	.background {
		/*background-image: url('https://api.rls.ovh/horizontal');*/
	}
}

/* 悬浮按钮 */
.contact-btn {
	position: fixed;
	bottom: 40px;
	right: 20px;
	color: white;
	padding: 15px 25px;
	border-radius: 30px;
	text-decoration: none;
	font-weight: bold;
	${randomColor()}
	transition: transform 0.3s, box-shadow 0.3s;
}
.contact-btn:hover {
	transform: translateY(-3px);
	${randomColor()}
}

/* 旋转效果 */
@keyframes rotateIn {
	from { transform: rotate(-180deg) scale(0); }
	to { transform: rotate(0) scale(1); }
}
/* 滑动效果 */
@keyframes slideInFromLeft {
	from { transform: translateX(100%); }
	to { transform: translateX(0); }
}
/* 缩放效果 */
@keyframes scale {
	0% { transform: scale(1); }
	50% { transform: scale(1.5); }
	100% { transform: scale(1); }
}
/* 弹跳效果 */
@keyframes bounce {
	0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
	40% { transform: translateY(-30px); }
	60% { transform: translateY(-15px); }
}
/* 掉落 */
@keyframes dropIn {
	from { transform: translateY(-100vh); }
	to { transform: translateY(0); }
}
`);

// HTML 被加载和解析完成后执行的代码
document.addEventListener("DOMContentLoaded", function() {

	// 创建头部内容
	const header = document.createElement('header');
	setAdd('header', header);  // 设置id和class
	const Container = document.createElement('div');
	setAdd('Container', Container);

	// 创建多行输入框元素
	const textarea = document.createElement('textarea');
	setAdd('inputLinks', textarea);
	textarea.setAttribute('placeholder', '支持链接和v2内容');

	// 创建按钮元素组
	const divButton = document.createElement('div');
	setAdd('button-group', divButton);

	// 创建提交按钮
	const generateBtn = document.createElement('button');
	setAdd('generateBtn', generateBtn);
	generateBtn.setAttribute('onclick', 'generateEncodedUrls()');
	generateBtn.setAttribute('style', `background-image: linear-gradient(to right, ${getRandomColor()} 0%, ${getRandomColor()} 51%, ${getRandomColor()} 100%);`);
	generateBtn.innerText = '生成链接';

	const copyBtn = document.createElement('button');
	setAdd('copyBtn', copyBtn);
	copyBtn.setAttribute('onclick', 'copyResult()');
	copyBtn.setAttribute('style', `background-image: linear-gradient(to right, ${getRandomColor()} 0%, ${getRandomColor()} 51%, ${getRandomColor()} 100%);`);
	copyBtn.innerText = '复制链接';

	const generateAndCopyBtn = document.createElement('button');
	setAdd('generateAndCopyBtn', generateAndCopyBtn);
	generateAndCopyBtn.setAttribute('onclick', 'generateAndCopy()');
	generateAndCopyBtn.setAttribute('style', `background-image: linear-gradient(to right, ${getRandomColor()} 0%, ${getRandomColor()} 51%, ${getRandomColor()} 100%);`);
	generateAndCopyBtn.innerText = '生成并复制';

	const UrlBtn = document.createElement('button');
	setAdd('UrlBtn', UrlBtn);
	UrlBtn.setAttribute('onclick', 'generateEncodedUrls(false)');
	UrlBtn.setAttribute('style', `background-image: linear-gradient(to right, ${getRandomColor()} 0%, ${getRandomColor()} 51%, ${getRandomColor()} 100%);`);
	UrlBtn.innerText = '恢复链接';

	const clashBtn = document.createElement('button');
	setAdd('clashBtn', clashBtn);
	clashBtn.setAttribute('onclick', 'clashBtn()');
	clashBtn.setAttribute('style', `background-image: linear-gradient(to right, ${getRandomColor()} 0%, ${getRandomColor()} 51%, ${getRandomColor()} 100%);`);
	clashBtn.innerText = '导入Clash';

	const openGeneratedLink = document.createElement('button');
	setAdd('openGeneratedLink', openGeneratedLink);
	openGeneratedLink.setAttribute('onclick', 'openGeneratedLink()');
	openGeneratedLink.setAttribute('style', `background-image: linear-gradient(to right, ${getRandomColor()} 0%, ${getRandomColor()} 51%, ${getRandomColor()} 100%);`);
	openGeneratedLink.innerText = '打开链接';

	// 创建结果框
	const resultContainer = document.createElement('div');
	setAdd('resultContainer', resultContainer);

	// 创建多行输入框元素
	const resultArea = document.createElement('textarea');
	setAdd('resultArea', resultArea);
	resultArea.setAttribute('readonly', '');
	resultArea.setAttribute('placeholder', '这里显示生成的编码结果');

	// ip显示
	const myIframe = document.createElement('p');
	setAdd('ip-info', myIframe);
	myIframe.innerText = '正在获取IP地址…'
	myIframe.setAttribute('style', 'height: 100%; display: none;');

	// 一言
	const h1hi = document.createElement('h1');
	setAdd('hitokoto', h1hi);
	h1hi.innerText = '订阅转换';

	// 随机壁纸api，来着http://www.coolapk.com/u/3594531
	const adaptive = document.createElement('img');
	setAdd('adaptive', adaptive);
	adaptive.setAttribute('src', '');
	adaptive.setAttribute('alt', '正在加载壁纸');
	adaptive.setAttribute('style', 'width: 100%; border-radius: 8px; animation: dropIn 1s forwards; display: none;');

	// 悬浮按钮
	const contact = document.createElement('a');
	setAdd('contact-btn', contact);
	contact.setAttribute('href', '//github.com/some6508/SubConv');
	contact.setAttribute('target', '_blank');
	contact.innerText = '项目来源';

	// 添加到提交按钮中
	divButton.appendChild(generateBtn);
	divButton.appendChild(copyBtn);
	divButton.appendChild(generateAndCopyBtn);
	divButton.appendChild(UrlBtn);
	divButton.appendChild(clashBtn);
	divButton.appendChild(openGeneratedLink);
	resultContainer.appendChild(resultArea);

	// 添加到Container中
	Container.appendChild(h1hi);
	Container.appendChild(textarea);
	Container.appendChild(divButton);
	Container.appendChild(resultContainer);
	Container.appendChild(myIframe);
	Container.appendChild(adaptive);
	Container.appendChild(contact);
	// Container.appendChild(hitokotos);

	// 添加到头部内容
	header.appendChild(Container);
	document.body.appendChild(header);

	// 添加尾部内容
	const footer = document.createElement("footer");
	setAdd('footer', footer);

	// 添加到body中
	document.body.appendChild(footer);
});

// 快捷添加id和class
function setAdd(id, ce) {
	ce.setAttribute('class', id);
	ce.setAttribute('id', id);
}

// 生成编码结果
function generateEncodedUrls(UUU = true) {
	const input = document.getElementById('inputLinks').value;
	if (!input) {
		showToast('请输入文本内容！');
		return;
	}
	let result;
	if (UUU){
		// 获取当前网页URL
		const currentURL = window.location.href;
		// URL编码处理函数
		result = currentURL + "sub?url=" + encodeURIComponent(input);
	} else {
		// URL解编码
		result = decodeURIComponent(input);
	}
	document.getElementById('resultArea').value = result;
	document.getElementById('resultContainer').style.display = 'block';
}

// 组合功能：生成并复制
function generateAndCopy() {
	generateEncodedUrls();
	setTimeout(copyResult, 100);
}

// 导入到Clash
function clashBtn() {
	const result = document.getElementById('resultArea').value;
	if (!result) {
		showToast('请输入文本内容！');
		return;
	}
	window.location.href = 'clash://install-config?url=' + result;
}

// 复制结果到剪贴板
async function copyResult() {
	const result = document.getElementById('resultArea');
	const textToCopy = result.value || result.textContent || result.innerText;

	if (!textToCopy) {
		showToast('请输入文本内容！');
		return;
	}

	try {
		await navigator.clipboard.writeText(textToCopy);
		showToast('复制成功！');
	} catch (error) {
		result.select();
		try {
			document.execCommand("copy");
			showToast('复制成功！');
		} catch (error) {
			showToast('复制失败！');
		}
	}
}


// 打开生成的链接
function openGeneratedLink() {
	const outputUrl = document.getElementById("resultArea").value;
	if (!outputUrl) {
		showToast('请输入文本内容！');
		return;
	}
	window.open(outputUrl, "_blank");
}

// 吐司弹窗
function showToast(message) {
	// alert(message);
	const toast = document.createElement('div');
	setAdd('toast', toast);
	toast.innerHTML = message;
	toast.style = `
		position: fixed;
		left: 50%;
		top: 200px;
		color: white;
		font-size: 0.9em;
		padding: 12px 24px;
		border-radius: 25px;
		transform: translateX(-50%);
		${randomColor()}
	`;
	// 无障碍支持
	toast.setAttribute('role', 'alert');
	toast.setAttribute('aria-live', 'polite');
	document.body.appendChild(toast);

	// 点击立即关闭
	toast.addEventListener('click', () => {
		toast.remove();
	});
	// 自动隐藏
	setTimeout(() => toast.remove(), 3000);
}

// 尾部时间显示
function updateTime() {
	const now = new Date();
	const systemTime = document.getElementById("footer");
	// const formattedTime = `${now.getFullYear()}年${String(now.getMonth() + 1).padStart(2)}月${String(now.getDate()).padStart(2)}号 ${String(now.getHours()).padStart(2)}点${String(now.getMinutes()).padStart(2)}分${String(now.getSeconds()).padStart(2)}秒`;
	if (systemTime) {
		// systemTime.innerHTML = formattedTime;
		// systemTime.textContent = now.toLocaleTimeString();
		systemTime.textContent = now.toISOString();
	}
} updateTime(); setInterval(updateTime, 1000);

// 加载ip地址
async function infoIP() {
	const urls = [
		'http://eth0.me',
		'http://90.151.171.106/ip.php',
		'http://checkip.amazonaws.com',
		'http://v4.ident.me',
		'http://freeze.na4u.ru/ip.php',
		'http://ip.bablosoft.com',
		'http://fingerprints.bablosoft.com/ip',
		'http://api.ipify.org',
		'https://web.realsysadm.in',
		'https://ipwho.is',
		'http://ip-api.com/json/?lang=zh-CN',
		'http://api.ipify.org/?format=json',
		'https://ip.skk.moe/simple',
		'https://ping0.cc/geo/jsonp'
	];
	for (const url of urls) {
		try {
			const controller = new AbortController();
			const signal = controller.signal;
			// 设置超时定时器
			const timeoutId = setTimeout(() => {
				controller.abort();
			}, 5000);

			const response = await fetch(url, { signal });
			// 请求成功后清除定时器
			clearTimeout(timeoutId);

			const data = await response.text();
			const i = document.getElementById("ip-info")
			i.innerHTML = data;
			i.style.display = 'block';
			break;
		} catch (error) {
			if (error.name === 'AbortError') {
				console.error('请求超时:', error.message);
			} else {
				console.error('请求失败: ', error);
			}
		}
	}
} infoIP();

// 随机阴影颜色
function randomColor() {
	// box-shadow: 0 8px 20px rgba(0, 255, 136, 0.5);
	return "box-shadow: 0 5px 15px rgba(" + (~~(Math.random() * 255)) + "," + (~~(Math.random() * 255)) + "," + (~~(Math.random() * 255)) + "," + "0.5" + ");";
}

// 随机颜色
function getRandomColor() {
	return '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
}

// 随机角度
function angles() {
	return `${Math.floor(Math.random() * 360)}deg`;
}

// 随机壁纸
async function adaptive() {
	const urls = [
		'https://api.rls.ovh/adaptive',
		'https://t.alcy.cc/ycy',
		'https://image.anosu.top/pixiv',
		'https://moe.jitsu.top/img',
		'https://api.neix.in/random/',
		'https://api.yimian.xyz/img',
		'https://www.loliapi.com/acg/'
	];

	// 加载随机壁纸
	const img = document.getElementById('adaptive');

	// 加载逻辑
	for (const url of urls) {
		try {
			// 使用Promise等待图片加载
			const preload = new Image();
			await new Promise((resolve, reject) => {
				preload.onload = resolve;
				preload.onerror = reject;
				preload.src = url;
			});
			// 成功加载后显示图片
			img.src = url;
			img.style.display = 'block';
			break;
		} catch (error) {
			console.error('请求失败: ', error);
		}
	}
}

/**
 * 生成随机颜色闭环序列
 * @param {number} colorCount - 需要的颜色数量（至少2个）
 * @param {number} [loop=1] - 基础循环次数
 * @returns {string} 颜色序列字符串
 */
function generateRandomColors(colorCount = 3, loop = 1) {
	// 生成随机颜色数组
	const colors = Array.from({ length: colorCount }, () => getRandomColor());

	// 创建闭环序列
	const template = Array.from({ length: loop }, () => [...colors]).flat();
	const closedLoop = [...template, colors[0]];
	return closedLoop.join(', ');
}

function generateColorLoop(vars, loop = 2) {
	// 创建基础循环模板
	const template = Array.from({ length: loop }, () => [...vars]).flat();
	// 添加闭环元素（首元素）实现无缝衔接
	return [...template, vars[0]]
		.map(v => `var(${v})`) // 添加var()包装
		.join(', ');
}

// 切换渐变角度
function updateGradient() {
	document.documentElement.style.setProperty('--angle', angles());
	// document.documentElement.style.setProperty('--color-body', generateRandomColors());
}

// 随机数生成
function getRandomNumber(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 一言API
async function hitokoto() {
	const urls = [
		'https://v1.hitokoto.cn/?encode=text',
		'https://v1.jinrishici.com/all.txt',
		'https://xiaoapi.cn/API/yiyan.php'
	]

	for (const url of urls) {
		try {
			const controller = new AbortController();
			const signal = controller.signal;
			// 设置超时定时器
			const timeoutId = setTimeout(() => {
				controller.abort();
			}, 5000);

			const response = await fetch(url, { signal });
			// 请求成功后清除定时器
			clearTimeout(timeoutId);

			const data = await response.text();
			const i = document.getElementById("hitokoto")
			i.innerHTML = data;
			break;
		} catch (error) {
			if (error.name === 'AbortError') {
				console.error('请求超时:', error.message);
			} else {
				console.error('请求失败: ', error);
			}
		}
	}
} hitokoto();

// HTML加载完成后运行
window.addEventListener("load", async () => {
	// 点击页面切换新渐变
	document.body.addEventListener('click', updateGradient);
	// 获取壁纸
	await adaptive();
});
