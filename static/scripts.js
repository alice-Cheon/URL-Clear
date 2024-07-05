function submitContent() {
    const contentElement = document.getElementById('content');
    const hiddenContentElement = document.getElementById('hidden-content');
    hiddenContentElement.value = contentElement.innerHTML;
}

function copyToClipboard() {
    const resultElement = document.getElementById('result');
    const range = document.createRange();
    range.selectNode(resultElement);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
    alert('Copied to clipboard');
}
