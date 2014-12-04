load = ->
    $('.upvote').on "click", "a", (e) ->
        $el = $ e.currentTarget
        $el.toggleClass "on"
        score = parseInt $el.siblings().html()
        if $el.hasClass "on"
            $el.siblings().html score + 1
        else
            $el.siblings().html score - 1
        id = $el.parent().parent().attr('id')
        $.ajax
            url: "upvote/#{id}"

$(document).ready load
$(document).on "page:load", load