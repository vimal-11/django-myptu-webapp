// post-detail.html 

//nav responsive

function showMenu(){
    var resMenu = document.getElementsById("menu")
    resMenu.setAttribute("style", "display: flex;");
}

//reply area

function showReply(){
    var commentArea = document.getElementById("reply-area");
    commentArea.setAttribute("style", "display: block;");
}

function showReplies(){
    var postReplies = document.getElementById("post-replies");
    postReplies.setAttribute("style", "display: block;");
}