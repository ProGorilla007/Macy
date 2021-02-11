// trigger when document loaded
$(function(){
    // get link field in account edit page
    let link_fields = $(".edit tbody").get();
    // set how many its hidden
    let counter = 5;

    // add scale animation to all link fields
    for (let i = 0; i < link_fields.length; ++i) {
        $(link_fields[i]).addClass("scale-transition");
    // hide last i of link fields
        if (i>4){
            $(link_fields[i]).addClass("scale-out");
            $(link_fields[i]).hide();
        }
    }

    // show hidden link fields dynamically in account edit page
    $('.add-link').click(function() {
        if (counter <= 9) {
            $(link_fields[counter]).show();
            $(link_fields[counter]).addClass('scale-in');
            ++counter;
        }
    });

    //　Mypage以下のAタグリンク先のドメインを取得し、リンク先のFaviconを表示する。
    $(".mypage a[href^='http']").each(function() {
        $(this).css({
            background: "url(https://www.google.com/s2/favicons?domain=" + this.hostname + ") left center no-repeat",
            "padding-left": "20px"
        });
    });
});




