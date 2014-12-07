load = ->
    $('.upvote').on "click", "a", (e) ->
        $el = $ e.currentTarget
        author_id = $el.parents('li').data('author-id')
        post_id = $('div.post').data('post-id')
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

    $('#datepicker').datetimepicker(
        sideBySide: true
        minDate: moment()
        useSeconds: false
        defaultDate: moment()
    )

    $('.remove-tag').on 'click', (e) ->
        $el = $(e.currentTarget)
        post_id = $('div.post').data('post-id')
        tag = $el.parent().data("tag-name")
        $.ajax
            url: "/removetag/"
            type: "POST"
            data:
                post_id: post_id
                tag: tag
            success: ->
                $el.parent().remove()



$(document).ready load
$(document).on "page:load", load