let relaxationGif = "https://media.giphy.com/media/j6aoUHK5YiJEc/giphy.gif";
let potentialEarImg = "https://media.giphy.com/media/a5viI92PAF89q/giphy.gif";
let noEarimg = "https://media.giphy.com/media/Od0QRnzwRBYmDU3eEO/giphy.gif";
let foundEarimg = "https://media.giphy.com/media/lRv3gbfX68oMDDPuwv/giphy.gif";

let safe = "No redirect found. Not vulnerable.";
let okay = "302 status code found, but no Location header.";
let potentialEAR = "Found 302 with Location header but content length is less than expected.";

let result;
let img;
let desc;

window.addEventListener('DOMContentLoaded', () => {
  result = document.getElementById('result')
  img = document.getElementById('img')
  desc = document.getElementById('desc');
});

chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, {message:"scan", url:tabs[0].url});
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.vulnerable) {
    result.innerText = "Vulnerable!";
    desc.innerText = "The site \'" + request.url + "\' was last checked on \'" + request.dateChecked + "\' and found to be vulnerable! Report this issue to the site owners!";
    img.src = foundEarimg;
  } else {
    result.innerText = "All Clear!";
    img.src = noEarimg;
    desc.innerText = "The site \'" + request.url + "\' was last checked on \'" + request.dateChecked + "\' and " + fullMsg(request);
  }  
});


function fullMsg(resp) {
  if (resp.message == safe) {
    return "there was no redirect found!";
  } else if (resp.message == okay) {
    return " there was a " + resp.message;
  } else if (resp.message == potentialEAR) {
    result.innerText = "Potential Vulnerability...";
    img.src = potentialEarImg;
    return "although there is a redirect request, the content header is too short to say for sure.";
  } else {
    return resp.message;
  }
}