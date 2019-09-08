big_slide = true;
big_title = false;

last_dec = 1;
imgs_scaled = false;
original_img_size = null;
original_img_marign = null;
img_size = null;
img_margin = null;

flower = "https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
boat = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQin6epPrshg5ou2oNsvzxQH3Ao8cPnjpYLDalvj8iPTlW7NHnm"

function add_image(img_url) {
    if (big_slide) return;
    if ($(".p-body > .p-images").length == 0)
        $(".p-body").append('<div class="p-images"></div>');
    $(".p-body > .p-images").append("<img src=\"" + img_url + "\" />");
    num_imgs = $(".p-body > .p-images > img").length;
    if (num_imgs >= 1.75 * last_dec) {
        last_dec = num_imgs;
        scale_imgs_down(1.414);
    }
    if (img_size != null)
        correct_imgs();
}

function scale_imgs_down(factor) {
    if (!imgs_scaled) {
        original_img_size = $(".p-body > .p-images > img").css("max-width");
        original_img_marign = $(".p-body > .p-images > img").css("margin");
    }
    imgs_scaled = true;
    width = $(".p-body > .p-images > img").css("max-width");
    margin = $(".p-body > .p-images > img").css("margin");
    img_size = "calc(" + width + " / " + factor + ")";
    img_margin = "calc(" + margin + " / " + factor + ")";
}

function correct_imgs() {
    $(".p-body > .p-images > img").css("max-width", img_size)
        .css("max-height", img_size)
        .css("margin", img_margin);
}

function add_bullet(text) {
    if (big_slide) return;
    if ($(".p-body > .p-text").length == 0) {
        $(".p-body").prepend('<div class="p-text"><ul></ul></div>');
        // if($(".p-body > .p-images").length > 0){
        //     scale_imgs_down(0.7);
        //     correct_imgs();
        // }
    }
    $(".p-body > .p-text > ul").append("<li>" + text + "</li>");
}

function new_slide(title) {
    if (big_slide && !big_title) {
        $(".p-title h1").html(title);
        big_title = true;
    } else if (big_slide && big_title) {
        $(".presentation").empty();
        $(".presentation").append("<div class=\"p-header\"><h1></h1></div>");
        $(".presentation").append("<div class=\"p-body\"></div>");
        big_slide = false;
    }
    $(".p-body").empty();
    $(".p-header h1").html(title);
    img_size = original_img_size;
    img_margin = original_img_marign;
    last_dec = 1;
}

function new_big_slide(title) {
    big_slide = true
    big_title = true
    $(".presentation").empty();
    $(".presentation").append("<div class=\"p-title\"><h1 class=\"title-text\">" + title + "</h1></div>");
    $(".presentation").append("<div class=\"p-accent-bar\"></div>");
}   
