import $ from 'jquery';
window.$ = window.jQuery = $;
import 'arrive';

var tweetVerifier = '<div class="tweet_verifier">This is a test.</div>'

function report_user(user_id, user_type) {
                console.log("Called with user_id=" + user_id + "user_type" + "bot")
                chrome.runtime.sendMessage({id: user_id, type: user_type, function: 'report'}, function(data) {
                    var findItem = $(value).find(".bs_confidence")
                    findItem.text('Thank you! ')

                  });
}
function injectData(bsItem, data) // Data = { userid : id, result : '', confidence : %}
{
    bsItem.find(".bs_loading").hide();
    bsItem.find(".bs_guess").css('display', 'inline-block');
    bsItem.find(".bs_ack").css('display', 'inline-block');
    if(data.result == 'bot'){
        bsItem.find(".bs_dhuman").hide()
        bsItem.css('background-color', '#eb4040')
    }
    else{
        bsItem.find(".bs_dbot").hide()
        bsItem.css('background-color', '#a0a0eb')
    }
    // console.log(data.confidence)
    // bsItem.find(".bs_confidence").text("Confidence : " + parseFloat(data.confidence)*100 + '%')
    console.log(bsItem.find(".bs_bot"))
    bsItem.find(".bs_bot").click(() => report_user(data.user_id, 'bot'))
    bsItem.find(".bs_human").click(() => report_user(data.user_id, 'human'))
    
}


$(function()
{ 
    //To check how many elements are initially spawned and how many get added later
    var counter = 0;
    var new_counter=0;

    //Load bsItem from local resource 
    var bsItem = null;

    $.get(chrome.extension.getURL('/static/item.html'), function(data) {
        bsItem = data;

        $(".js-stream-tweet").each(function(tweet, value) {
            if($(value) != null)
            {
                $(value).append(bsItem) 

                if($(value).data("user-id") == null) console.log($(value))

                var user_chain = $(value).data("reply-to-users-json").reverse()

                //Post current user
                console.log($(value).data("user-id"))
                console.log("Posting user : " + user_chain[0].screen_name + " " + user_chain[0].id_str )

                //Get data from extension
                chrome.runtime.sendMessage({user_id: user_chain[0].id_str, function: 'get_data'}, function(data) {
                    var findItem = $(value).find(".bs_item")
                    injectData(findItem, data)
                  });

                //Retweet chain
                console.log(user_chain.length)
                for(var i=1; i<user_chain.length; i++)
                    console.log("Retweeted from : " + user_chain[i].screen_name + " " + user_chain[i].id_str )
            }
            counter++;
        }) });

    document.arrive(".js-stream-tweet",function(item){
        $(item).append(bsItem)
        console.log("Our counter : " + counter + " main counter : " + new_counter)
        counter++;
    })
})