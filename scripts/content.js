chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    if (request.message === 'scan') {
      fetch(`https://ear-extension-backend.onrender.com/scan/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: request.url }),
      })
      .then((response) => response.json())
      .then((data) => {
        chrome.runtime.sendMessage(data);
      })
      .catch((err) => console.log(err));
    } 
});

