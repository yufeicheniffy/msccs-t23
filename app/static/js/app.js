function waitGrid() {
    var checkExist = setInterval(function() {
        if ($("#tweet-grid").children().length > 0) {
            $('#refreshing-anim').hide();
            $('#tweet-grid').show();
            $(document).ready(paginationHandler);
            clearInterval(checkExist);
        }
    }, 1000);
}

function filterTweets(active_categories, active_priorities, chronological, media_only) {
    $('#tweet-grid').hide();
    $('#refreshing-anim').show();
    $.ajax({
        url: "/filter_tweets",
        type: "get",
        data: {categories: active_categories.join(','), priorities: active_priorities.join(','), chronological: chronological, media_only: media_only},
        success: function(response) {
            $("#tweet-grid").html(response);
        },
        error: function(xhr) {
        //Do Something to handle error
        },
        complete: function(){
            waitGrid();
        }
    });
}

var paginationHandler = function(){
    // store pagination container so we only select it once
    var $paginationContainer = $(".pagination-container"),
        $pagination = $paginationContainer.find('.pagination ul');
    // click event
    $pagination.find("li a").on('click.pageChange',function(e){
        e.preventDefault();
        // get parent li's data-page attribute and current page
    var parentLiPage = $(this).parent('li').data("page"),
    currentPage = parseInt( $(".pagination-container div[data-page]:visible").data('page') ),
    numPages = $paginationContainer.find("div[data-page]").length;
    // make sure they aren't clicking the current page
    if ( parseInt(parentLiPage) !== parseInt(currentPage) ) {
    // hide the current page
    $paginationContainer.find("div[data-page]:visible").hide();
    if ( parentLiPage === '+' ) {
                // next page
        $paginationContainer.find("div[data-page="+( currentPage+1>numPages ? numPages : currentPage+1 )+"]").show();
    } else if ( parentLiPage === '-' ) {
                // previous page
        $paginationContainer.find("div[data-page="+( currentPage-1<1 ? 1 : currentPage-1 )+"]").show();
    } else {
        // specific page
        $paginationContainer.find("div[data-page="+parseInt(parentLiPage)+"]").show();
            }
        }
    });
};

$(document).ready(paginationHandler);

$(document).ready(function() {
    var active_categories = []
    var active_priorities = []
    var media_only = false
    var chronological = true
    paginationHandler

    setTimeout(function() {
        $('.alert').fadeOut();
    }, 6000);
    

    $('#load_button').click(function(){
        query= $('#query_input').val();
        tweetnum= $('#tweet_num').val();
        if(query == '' || tweetnum == ''){
            if(query == '' ){
                $('#query_input').focus();
                $('#query_input').css("background-color", "red");
            }
            if(tweetnum == '' ){
                $('#tweet_num').focus();
                $('#tweet_num').css("background-color", "red");
            }
            
        }else{
            $('#loading').show();
            $('#query_input').prop('readonly', true);
            $('#tweet_num').prop('readonly', true);
            document.theForm.submit();
        }
    })

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    $('.category-filters').children('label').each(function(i) {
        if ($(this).hasClass('active')) {
            active_categories.push($(this).attr('id'))
        }
    });
    $('.filters').children('.filter').each(function(i) {
        if ($(this).has('i')) {
            active_priorities.push($(this).attr('id'))
        }
    });

    $(document).on('click', '.category', function () {
        var check_val = $.inArray($(this).attr('id'), active_categories)
        if (check_val == -1) {
            active_categories.push($(this).attr('id'))
        } else {
            active_categories.splice(check_val, 1)
        }

        filterTweets(active_categories, active_priorities, chronological, media_only)
    });

    $(document).on('click', '.filter', function () {
        var check_val = $.inArray($(this).attr('id'), active_priorities)
        if (check_val == -1) {
            active_priorities.push($(this).attr('id'))
        } else {
            active_priorities.splice(check_val, 1)
        }

        if ($(this).has('i').length) {
            var temp = $(this).text()
            $(this).empty()
            $(this).html(temp)
        } else {
            var temp = $(this).text()
            $(this).html(temp + '<i class="fas fa-check"></i>')
        }

        filterTweets(active_categories, active_priorities, chronological, media_only)
    });

    $(document).on('click', '.order', function () {
        var id = $(this).attr('id')

        if (id == 'chronological') {
            chronological = true
            var temp = $(this).text()
            $(this).html(temp + '<i class="fas fa-circle fa-xs"></i>')

            if ($('#reverse-chronological').has('i').length) {
                var temp = $('#reverse-chronological').text()
                $('#reverse-chronological').empty()
                $('#reverse-chronological').html(temp)  
            }
        } else {
            chronological = false
            var temp = $(this).text()
            $(this).html(temp + '<i class="fas fa-circle fa-xs"></i>')

            if ($('#chronological').has('i').length) {
                var temp = $('#chronological').text()
                $('#chronological').empty()
                $('#chronological').html(temp)  
            }           
        }
        
        filterTweets(active_categories, active_priorities, chronological, media_only)
    });

    $(document).on('click', '.media-filter', function () {
        var id = $(this).attr('id')

        if (id == 'all-tweets') {
            media_only = false
            var temp = $(this).text()
            $(this).html(temp + '<i class="fas fa-circle fa-xs"></i>')

            if ($('#media-only').has('i').length) {
                var temp = $('#media-only').text()
                $('#media-only').empty()
                $('#media-only').html(temp)  
            }
        } else {
            media_only = true
            var temp = $(this).text()
            $(this).html(temp + '<i class="fas fa-circle fa-xs"></i>')

            if ($('#all-tweets').has('i').length) {
                var temp = $('#all-tweets').text()
                $('#all-tweets').empty()
                $('#all-tweets').html(temp)  
            }           
        }
        
        filterTweets(active_categories, active_priorities, chronological, media_only)
    });

});

$(window).on('load', function() {
    $('#refreshing-anim').hide();
    $('#tweet-grid').show();
});