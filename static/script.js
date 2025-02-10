// 生成动态网页
document.addEventListener("DOMContentLoaded", function () {
	// 获取id创建容器
	const Container = document.getElementById('Container');

	// 创建多行输入框元素
	const textarea = document.createElement('textarea');
	textarea.setAttribute('id', 'inputLinks');
	textarea.setAttribute('placeholder', '支持链接和v2内容');

	// 创建按钮元素组
	const divButton = document.createElement('div');
	divButton.setAttribute('class', 'button-group');

	// 创建提交按钮
	const generateBtn = document.createElement('button');
	generateBtn.setAttribute('id', 'generateBtn');
	generateBtn.setAttribute('onclick', 'generateEncodedUrls()');
	generateBtn.innerText = '生成链接';

	const copyBtn = document.createElement('button');
	copyBtn.setAttribute('id', 'copyBtn');
	copyBtn.setAttribute('onclick', 'copyResult()');
	copyBtn.innerText = '复制链接';

	const generateAndCopyBtn = document.createElement('button');
	generateAndCopyBtn.setAttribute('id', 'generateAndCopyBtn');
	generateAndCopyBtn.setAttribute('onclick', 'generateAndCopy()');
	generateAndCopyBtn.innerText = '生成并复制';

	// 创建结果框
	const resultContainer = document.createElement('div');
	resultContainer.setAttribute('id', 'resultContainer');

	// 创建多行输入框元素
	const resultArea = document.createElement('textarea');
	resultArea.setAttribute('id', 'resultArea');
	resultArea.setAttribute('readonly', '');
	resultArea.setAttribute('placeholder', '这里显示生成的编码结果');

	// 添加到提交按钮中
	divButton.appendChild(generateBtn);
	divButton.appendChild(copyBtn);
	divButton.appendChild(generateAndCopyBtn);
	resultContainer.appendChild(resultArea);

	// 添加到容器中
	Container.appendChild(textarea);
	Container.appendChild(divButton);
	Container.appendChild(resultContainer);
});


// 生成编码结果
function generateEncodedUrls() {
	const input = document.getElementById('inputLinks').value;
	if (!input) {
		alert('请输入文本内容！');
		return;
	}
	// 获取当前网页URL
	const currentURL = window.location.href;
	// URL编码处理函数
	const result = encodeURIComponent(input);
	document.getElementById('resultArea').value = currentURL + "sub?url=" + result;
	document.getElementById('resultContainer').style.display = 'block';
}

// 组合功能：生成并复制
function generateAndCopy() {
	generateEncodedUrls();
	setTimeout(copyResult, 100);
}

// 复制结果到剪贴板
async function copyResult() {
	try {
		await navigator.clipboard.writeText(document.getElementById('resultArea').value);
		showToast('✅ 复制成功！');
	} catch (err) {
		showToast('❌ 复制失败！');
	}
}

function showToast(message) {
	const toast = document.createElement('div');
	toast.textContent = message;
	toast.style = `
		position: fixed;
		bottom: 80px;
		left: 50%;
		transform: translateX(-50%);
		background: rgba(0,0,0,0.8);
		color: white;
		padding: 12px 24px;
		border-radius: 25px;
		font-size: 0.9em;
		animation: slideIn 0.3s ease-out;
	`;
	document.body.appendChild(toast);
	setTimeout(() => toast.remove(), 2000);
}

// 尾部时间显示
function updateTime() {
	const myDate = new Date();
	const hours = formatTime(myDate.getHours());
	const minutes = formatTime(myDate.getMinutes());
	const seconds = formatTime(myDate.getSeconds());
	const systemTime = document.getElementById("footer");
	systemTime.innerHTML = hours + "点" + minutes + "分" + seconds + "秒";
}

//格式化时间：分秒。
function formatTime(i) {
	if (i < 10) {
		i = "0" + i;
	}
	return i;
}

setInterval(updateTime, 1000);
updateTime();
