console.log("content script exists")

chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    if (request.message === 'scan') {
      console.log("received response!")
      // get response
      let result = {
        _id: null,
        dateChecked: "date", 
        message: "EAR detected",
        status_code: 200, 
        url: "url",
        vulnerable: true
      }

      // return result to requester
      chrome.runtime.sendMessage(result);
    } 
});

