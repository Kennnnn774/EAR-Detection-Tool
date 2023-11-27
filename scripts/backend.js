chrome.tabs.onUpdated.addListener(
  async function(tabId, changeInfo, tab) {
    // read changeInfo data and do something with it
    // like send the new url to contentscripts.js
    if (changeInfo.url) {
      chrome.tabs.sendMessage( tabId, {
        message: 'scan',
        url: changeInfo.url
      })
    }
  }
);

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === true) {
    chrome.action.setBadgeText({
      text: "👂!!",
    });
  } else {
    chrome.action.setBadgeText({
      text: "✅",
    });
  }
});