load = ->
    $('.upvote').on "click", "a", (e) ->
        $el = $ e.currentTarget
        author_id = $el.parents('li').data('author-id')
        post_id = $el.parents('ul').data('post-id')
        $.ajax
            url: "/upvote/"
            type: "POST"
            data:
                type: "submission"
                author_id: author_id
                post_id: post_id
            success: (data)->
                if data.success
                    $el.toggleClass "on"
                    score = parseInt $el.siblings().html()
                    if $el.hasClass "on"
                        $el.siblings().html score + 1
                    else
                        $el.siblings().html score - 1
                else
                    alert(data.reason)

$(document).ready load
$(document).on "page:load", load