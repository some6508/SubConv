document.addEventListener("DOMContentLoaded", function() {
    // 创建容器
    var shortLinkContainer = document.getElementById('shortLinkContainer');

    // 创建表单元素
    var form = document.createElement('form');

    // 创建多行输入框元素
    var textarea = document.createElement('textarea');
    textarea.setAttribute('id', 'text');
    textarea.setAttribute('name', 'text');
    textarea.setAttribute('placeholder', '支持链接和v2内容');

    // 创建提交按钮
    var submitButton = document.createElement('button');
    submitButton.setAttribute('type', 'submit');
    submitButton.innerText = '生成链接并复制';

    // 将按钮添加到表单中
    form.appendChild(textarea);
    form.appendChild(submitButton);

    // 将表单添加到容器中
    shortLinkContainer.appendChild(form);

    // 表单提交处理
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单默认提交行为
        var longText = document.getElementById('text').value.trim();

        if (!longText) {
            alert('请输入文本内容！');
            return;
        }

        // 获取当前网页URL
        var currentURL = window.location.href;

        // 将文本转换为URL编码
        var encoded = encodeURIComponent(longText);

        // 检查容器中是否已存在段落元素
        var shortLinkElement = shortLinkContainer.querySelector('p');
        // 如果不存在，则创建一个新的段落元素
        if (!shortLinkElement) {
            shortLinkElement = document.createElement('p');
            shortLinkElement.id = "text-copy";
            shortLinkContainer.appendChild(shortLinkElement);
        }
        // 更新段落元素的文本内容
        shortLinkElement.textContent = currentURL + "sub?url=" + encoded;

        // 获取要复制的文本元素
        var textElement = document.getElementById("text-copy");

        // 创建一个临时的textarea元素来复制文本
        var tempTextArea = document.createElement("textarea");
        tempTextArea.value = textElement.innerText;

        // 将textarea元素添加到DOM中（这一步是为了让textarea成为可聚焦的元素）
        document.body.appendChild(tempTextArea);

        // 选中textarea中的文本
        tempTextArea.select();
        tempTextArea.setSelectionRange(0, 99999); // 对于移动设备

        // 执行复制命令
        var successful = document.execCommand("copy");
        var msg = successful ? "成功" : "失败";

        // 可选：显示一个提示消息给用户
        alert("复制链接 " + msg);

        // 移除临时的textarea元素
        document.body.removeChild(tempTextArea);

    })
});
