$(function(){

    //　Mypage以下のAタグリンク先のドメインを取得し、リンク先のFaviconを表示する。
    $(".mypage a[href^='http']").each(function() {
        $(this).css({
            background: "url(https://www.google.com/s2/favicons?domain=" + this.hostname + ") left center no-repeat",
            "padding-left": "20px"
        });
    });

});


