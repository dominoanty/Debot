import $ from 'jquery';
window.$ = window.jQuery = $;
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
        
        
        if(request.function == 'get_data')
            $.get('http://localhost:5000/' + request.user_id, function(data) { 
                console.log(request)
                sendResponse({user_id : request.user_id, result : request.result, confidence : request.confidence});
            })
        else if(request.function = 'report')
            $.post('http://localhost:5000/' + request.id + '/' + request.type, function(data) {
                sendResponse({});
            })
        return true;
});