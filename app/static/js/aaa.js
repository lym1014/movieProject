$(window).on('scroll',function(){
    /*console.log("scrollTop--->" + scrollTop());
    console.log("windowHeight--->" + windowHeight());
    console.log("documentHeight--->" + documentHeight());*/
    if(scrollTop() + windowHeight() >= documentHeight()){
        loadMore();
    }
});
function loadMore() {
    console.log("enter load More , isloading = " + isloading);


}
function scrollTop(){
    return Math.max(
            //chrome
            document.body.scrollTop,
            //firefox/IE
            document.documentElement.scrollTop);
}
function documentHeight(){
    //现代浏览器（IE9+和其他浏览器）和IE8的document.body.scrollHeight和document.documentElement.scrollHeight都可以
    return Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);
}
function windowHeight(){
    return (document.compatMode == "CSS1Compat")?
            document.documentElement.clientHeight:
            document.body.clientHeight;
}