function add_image(img_url) {
    if($(".p-body > .p-images").length == 0){
        $(".p-body").append('<div class="p-images"></div>');
    }
    $(".p-body > .p-text").append("<img src=\"" + img_url + "\" />");
}

function add_bullet(text) {
    if($(".p-body > .p-text").length == 0){
        $(".p-body").append('<div class="p-text"><ul></ul></div>');
    }
    $(".p-body > .p-text > ul").append("<li>" + text + "</li>");
}

function new_slide(title){
    $(".p-body").empty();
    $("#my-p-header h1").html(title);
}