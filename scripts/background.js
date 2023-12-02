chrome.tabs.onActivated.addListener(async function(activeInfo) {
  let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  if (tab) {
    chrome.tabs.sendMessage(tab.id, {
      message: "scan",
      url: tab.url
    })
  }
})

chrome.tabs.onUpdated.addListener(
  async function(tabId, changeInfo, tab) {
    if (changeInfo.status == "complete") {
      let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
      if (tab) {
        chrome.tabs.sendMessage(tab.id, {
          message: "scan",
          url: tab.url
        })
      }
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