console.log("content script exists")

chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    console.log("scan");
    if (request.message === 'scan') {
      // get response
      let result = {
        vulnerable: true,
        message: 'This site is not vulnerable!'
      }

      // return result to background script to process result
      chrome.runtime.sendMessage(result);
      
    } 
});



// document.getElementById('scanButton').addEventListener('click', function() {
//   chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//       const currentTab = tabs[0];
//       fetch('http://localhost:5000/scan', {
//           method: 'POST',
//           headers: {
//               'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ url: currentTab.url }),
//       })
//       .then(response => response.json())
//       .then(data => {
//           document.getElementById('result').textContent = JSON.stringify(data);
//       })
//       .catch(error => {
//           console.error('Error:', error);
//       });
//   });
// });
