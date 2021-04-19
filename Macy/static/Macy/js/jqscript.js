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
    let thumbnail_uri = '/static/Macy/img/';
    let img_ext = '.png';
    let options = $('.link-choice option').get();
    for (let i = 0; i < options.length; ++i) {
        $(options[i]).attr('data-icon', thumbnail_uri + $(options[i]).val() + img_ext);
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

    const mediaChoice = {
        TWT: 'https://twitter.com/',
        FBK: 'https://www.facebook.com/',
        INS: 'https://www.instagram.com/',
        YTB: 'https://www.youtube.com/c/',
    }

    $('.link-choice').change(function() {
        let url_field = $(this).closest('tr').find('.link-url');
        let account_field = $(this).closest('tr').find('.link-account');
        url_field.val('');
        account_field.val('');
        if (this.value in mediaChoice) {
            url_field.attr('readonly', true);
        } else {
            url_field.attr('readonly', false);
        }
    });

    $('.link-account').on('input propertychange paste', function() {
        let media = $(this).closest('tr').find('.link-choice');
        let url = $(this).closest('tr').find('.link-url');
        if(media.val() in mediaChoice){
            url.val( mediaChoice[media.val()] + $(this).val());
        }
    });

    $('#hamburger').on('click', function(){
        $(this).toggleClass('active');
        $('.menu').toggleClass('menu-active')
        $('#hamburger_list').toggleClass('active')
        // console.log('open menu')
        return false;
    });


    let target = $('.signup')
    if(target.length>0) {
        $('.menu').addClass('menu-signup');
    }
    

});




