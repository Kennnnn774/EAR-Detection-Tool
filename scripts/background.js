chrome.tabs.onUpdated.addListener(
  async function(tabId, changeInfo, tab) {
    if (changeInfo.url) {
      chrome.action.setBadgeText({
        text: "...",
      });
      chrome.tabs.sendMessage(tab.id, {
        message: "scan",
        url: tab.url
      });
    }
  }
);

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.vulnerable === true) {
    chrome.action.setBadgeText({
      text: "👂",
    });
  } else {
    chrome.action.setBadgeText({
      text: "✅",
    });
  }
});