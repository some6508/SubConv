// 加载时添加
(function () {
	const now = new Date(); // 获取当前时间（基于用户本地时区）
	window.document.title = '订阅转换' + now.toISOString();

	// 添加图标
	const slink = document.createElement('link');
	slink.rel = "shortcut icon";
	slink.href="https://www.gstatic.cn/images/branding/product/2x/google_cloud_64dp.png?";
	const tlink = document.createElement('link');
	tlink.rel = "apple-touch-icon";
	tlink.href="https://www.gstatic.cn/images/branding/product/2x/google_cloud_64dp.png?";
	document.head.appendChild(slink);
	document.head.appendChild(tlink);
}());

// 添加style
function addGlobalStyle(css) {
	const style = document.createElement('style');
	style.textContent = css; // 更现代的写法，兼容非IE
	document.head.appendChild(style);
}

addGlobalStyle(`
/* 全局变量 */
:root {
	--primary-color: ${getRandomColor()};  /* #F596AA */
	--secondary-color: ${getRandomColor()};  /* #66CCFF */
	--secon-color : ${getRandomColor()};  /* #00FF88 */
	--angle: ${angles()};
}

/* 渐变背景 */
body {
	margin: 0;
	width: 100%;
	height: 100vh;
	color: #fff;
	background: linear-gradient(var(--angle), #ee7752, ${getRandomColor()}, #23a6d5, #23d5ab);
	background-size: 400% 400%;
	animation: gradient 5s ease infinite;
	transition: all 1s ease;
}
@keyframes gradient {
	0% { background-position: 0% 50%; }
	50% { background-position: 100% 50%; }
	100% { background-position: 0% 50%; }
}

header {
	width: 100%;
	height: 100%;
	text-align: center;
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
/* animation: hi 1s, runs 2s infinite linear; */
.footer, .toast, .contact-btn, .hitokoto, .ip-info, .adaptive {
	font-weight: bold;
	background: -webkit-linear-gradient(left, var(--primary-color), var(--secondary-color), var(--secon-color), var(--primary-color), var(--secondary-color), var(--secon-color), var(--primary-color));
	background-size: 200% 100%;
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	animation: gradientAnimation 3s linear infinite;
}
@keyframes gradientAnimation {
	0% { background-position: 100% 50%; }
	100% { background-position: 0% 50%; }
}

/* 默认使用竖图 */
.background {
	/*background-image: url('https://api.rls.ovh/vertical');*/
	background-size: cover;
	background-position: center;
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
	bottom: 30px;
	right: 30px;
	color: white;
	padding: 15px 25px;
	border-radius: 30px;
	text-decoration: none;
	font-weight: bold;
	${randomColor()}
	transition: transform 0.3s, box-shadow 0.3s;
	z-index: 1000;
}
.contact-btn:hover {
	transform: translateY(-3px);
	${randomColor()}
}

`);


// HTML 文档被加载和解析完成后执行的代码
document.addEventListener("DOMContentLoaded", function() {

	// 创建头部内容
	const header = document.createElement('header');
	setAdd('header', header);
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
	generateBtn.setAttribute('style', `background: ${getRandomColor()}`);
	generateBtn.innerText = '生成链接';

	const copyBtn = document.createElement('button');
	setAdd('copyBtn', copyBtn);
	copyBtn.setAttribute('onclick', 'copyResult()');
	copyBtn.setAttribute('style', `background: ${getRandomColor()}`);
	copyBtn.innerText = '复制链接';

	const generateAndCopyBtn = document.createElement('button');
	setAdd('generateAndCopyBtn', generateAndCopyBtn);
	generateAndCopyBtn.setAttribute('onclick', 'generateAndCopy()');
	generateAndCopyBtn.setAttribute('style', `background: ${getRandomColor()}`);
	generateAndCopyBtn.innerText = '生成并复制';

	const UrlBtn = document.createElement('button');
	setAdd('UrlBtn', UrlBtn);
	UrlBtn.setAttribute('onclick', 'generateEncodedUrls(false)');
	UrlBtn.setAttribute('style', `background: ${getRandomColor()}`);
	UrlBtn.innerText = '恢复链接';

	const clashBtn = document.createElement('button');
	setAdd('clashBtn', clashBtn);
	clashBtn.setAttribute('onclick', 'clashBtn()');
	clashBtn.setAttribute('style', `background: ${getRandomColor()}`);
	clashBtn.innerText = '导入Clash';

	const openGeneratedLink = document.createElement('button');
	setAdd('openGeneratedLink', openGeneratedLink);
	openGeneratedLink.setAttribute('onclick', 'openGeneratedLink()');
	openGeneratedLink.setAttribute('style', `background: ${getRandomColor()}`);
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
	myIframe.setAttribute('style', 'height: 100%;');

	// 文心一言API
	const h1hi = document.createElement('h1');
	setAdd('hitokoto', h1hi);
	h1hi.innerText = '订阅转换';
	// h1hi.style = randomColor() + 'border-radius: 8px;';
	const hitokotos = document.createElement('script');
	hitokotos.setAttribute('src', 'https://v1.hitokoto.cn/?encode=js&amp;select=%23hitokoto');
	hitokotos.setAttribute('defer', '');

	// 随机壁纸api，来着http://www.coolapk.com/u/3594531
	const adaptive = document.createElement('img');
	setAdd('adaptive', adaptive);
	adaptive.setAttribute('src', '');
	adaptive.setAttribute('alt', '随机壁纸');
	adaptive.setAttribute('style', 'width: 100%; border-radius: 8px;');

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
	Container.appendChild(hitokotos);

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
	const result = document.getElementById('resultArea').value;
	if (!result) {
		showToast('请输入文本内容！');
		return;
	}
	try {
		// result.select();
		// document.execCommand("copy");
		await navigator.clipboard.writeText(result);
		showToast('复制成功！');
	} catch (err) {
		showToast('复制失败！');
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
	const toast = document.createElement('div');
	setAdd('toast', toast);
	toast.textContent = message;
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
		'https://web.realsysadm.in?Z79362604080Q1',
		'http://ip.bablosoft.com?Z79362604080Q1',
		'http://api.ipify.org/?format=json',
		'http://api.ipify.org?Z79362604080Q1',
		'http://ip-api.com/json/?lang=zh-CN',
		'http://fingerprints.bablosoft.com/ip?Z79362604080Q1',
		'https://ipwho.is?Z79362604080Q1',
		'http://eth0.me?Z79362604080Q1',
		'http://90.151.171.106/ip.php?Z79362604080Q1',
		'http://checkip.amazonaws.com?Z79362604080Q1',
		'http://v4.ident.me?Z79362604080Q1',
		'http://freeze.na4u.ru/ip.php?Z79362604080Q1',
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
			document.getElementById("ip-info").innerHTML = data;
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

async function adaptive() {
	const urls = [
		'https://api.rls.ovh/adaptive',
		'https://t.alcy.cc/ycy',
		'https://image.anosu.top/pixiv',
		'https://moe.jitsu.top/img'
	];

	// 加载随机壁纸
	const img = document.getElementById('adaptive');

	img.src = 'https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/Flamingo.png';
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
			break;
		} catch (error) {
			console.error('请求失败: ', error);
		}
	}
}

function updateGradient() {
	document.documentElement.style.setProperty('--angle', angles());
}

// 页面加载完成
window.addEventListener("load", async () => {
	adaptive();
	// 点击页面切换新渐变
	document.body.addEventListener('click', updateGradient);
});

