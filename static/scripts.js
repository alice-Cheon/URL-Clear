function copyToClipboard() {
    const resultElement = document.getElementById('result');
    resultElement.select();
    resultElement.setSelectionRange(0, 99999); // For mobile devices
    document.execCommand('copy');
    alert('Copied to clipboard');
}
