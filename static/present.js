last_dec = 1;
imgs_scaled = false;
original_img_size = null;
original_img_marign = null;
img_size = null;
img_margin = null;

function add_image(img_url) {
    if($(".p-body > .p-images").length == 0)
        $(".p-body").append('<div class="p-images"></div>');
    $(".p-body > .p-images").append("<img src=\"" + img_url + "\" />");
    num_imgs = $(".p-body > .p-images > img").length;
    if (num_imgs >= 1.75*last_dec) {
        last_dec = num_imgs;
        scale_imgs_down(1.414);
    }
    if (img_size != null)
        correct_imgs();
}

function scale_imgs_down(factor){
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
    if($(".p-body > .p-text").length == 0){
        $(".p-body").prepend('<div class="p-text"><ul></ul></div>');
        if($(".p-body > .p-images").length > 0){
            scale_imgs_down(0.7);
            correct_imgs();
        }
    }
    $(".p-body > .p-text > ul").append("<li>" + text + "</li>");
}

function new_slide(title){
    $(".p-body").empty();
    $("#my-p-header h1").html(title);
    img_size = original_img_size;
    img_margin = original_img_marign;
    last_dec = 1;
}