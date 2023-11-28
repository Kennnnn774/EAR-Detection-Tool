// chrome.runtime.onMessage.addListener(
//   async function(request, sender, sendResponse) {
//     // listen for messages sent from background.js
//     if (request.message === 'scan') {
//       // get response
//       let result = {
//         vulnerable: false,
//         message: 'This site is not vulnerable!'
//       }
//       // if found
//       // else conduct scan

//       // return result to the background script
//       chrome.runtime.sendMessage(result);

//       // store the result in local storage. so that the popup can display the result.
//       chrome.storage.local.set(result);
//     } 
// });

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
