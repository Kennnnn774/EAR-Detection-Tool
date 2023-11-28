document.getElementById('scanButton').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const currentTab = tabs[0];
        console.log("currentURL", currentTab.url);
        fetch('http://localhost:5000/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: currentTab.url }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = JSON.stringify(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
