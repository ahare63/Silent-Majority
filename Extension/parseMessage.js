document.getElementById('parseButton').addEventListener('click', function(){
    chrome.runtime.sendMessage({
        action: "parse"
    });
    //alert('Done'); //For debugging
});