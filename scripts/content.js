chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    if (request.message === 'scan') {
      fetch(`${DB_URL_API_BASE}/${request.url}`)
      .then((response) => response.json())
      .then((data) => {
        chrome.runtime.sendMessage(data);
      })
      .catch((err) => console.log(err));
    } 
});

