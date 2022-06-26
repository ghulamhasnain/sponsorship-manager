$(document).ready(function(){
    $(".links").mouseenter(function(){
        $(this).css("background-color", "White");
    });
    
    $(".active_link").css("background-color", "White");

    $(".links").mouseleave(function(){
        $(this).css("background-color", "Gold");
    });

    $(".midlink").mouseenter(function(){
    	$(this).animate({marginTop: "-15px"}, { queue: false })
    	$(this).animate({height: "178px"}, { queue: false })
    });
    $(".midlink").mouseleave(function(){
        $(this).animate({marginTop: "0px"}, { queue: false })
        $(this).animate({height: "147px"}, { queue: false })
    });

    $(".milkplus").click(function(){
        var q = Number($(".milk_q").val())
        $('.milk_q').val(q + 1)
    })
    $(".milkminus").click(function(){
        var q = Number($(".milk_q").val())
        if (q <= 0) {
            $(".milk_q").val(0)
        }
        else {
            $('.milk_q').val(q - 1)
        }
    }) 

    $(".bananaplus").click(function(){
        var q = Number($(".banana_q").val())
        $('.banana_q').val(q + 1)
    })
    $(".bananaminus").click(function(){
        var q = Number($(".banana_q").val())
        if (q <= 0) {
            $(".banana_q").val(0)
        }
        else {
            $('.banana_q').val(q - 1)
        }
    })

    $(".sponplus").click(function(){
        var q = Number($(".spon_q").val())
        $('.spon_q').val(q + 1)
    })
    $(".sponminus").click(function(){
        var q = Number($(".spon_q").val())
        if (q <= 0) {
            $(".spon_q").val(0)
        }
        else {
            $('.spon_q').val(q - 1)
        }
    })

    $(".month").each(function(){
        var entry = $(this).text()
        var num = parseInt(entry)
        var mnt = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        $(this).text(mnt[num])
    })

    $(".stat").each(function(){
        if ($(this).text() == "inactive") {
            $(this).text('(has left school)')
            $(this).css("color", "Red");
        }
        else {
            $(this).text('')
        }
    })

    var pmt_num = 1
    $('.edit_payment').each(function(){
        $(this).find('.pmt_id').find('input').attr('name', 'pmt_id'+pmt_num)
        $(this).find('.pmt_admitnumber').find('input').attr('name', 'profile'+pmt_num)
        $(this).find('.pmt_amount').find('input').attr('name', 'amount'+pmt_num)
        $(this).find('.pmt_date').find('input').attr('name', 'month'+pmt_num)
        pmt_num = pmt_num + 1
    })

});

window.takeScreenShot = function() {
    var admitnumber = $('.admitnumber').text()
    html2canvas(document.getElementById("target"), {
        onrendered: function (canvas) {
            canvas.toBlob(function(blob) {
                saveAs(blob, "view_" + admitnumber + ".jpg")
            })
        },
    });
}
