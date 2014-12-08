timer = ->
    $timer = $('.timer')
    if $timer
        closing_time = moment($timer.data("date"))
        setInterval ->
            time_left = closing_time - moment()
            seconds_left = time_left / 1000
            days = parseInt(seconds_left / 86400)
            seconds_left = seconds_left % 86400
            hours = parseInt(seconds_left / 3600)
            seconds_left = seconds_left % 3600
            minutes = parseInt(seconds_left / 60)
            seconds = parseInt(seconds_left % 60)
            $timer.html("""Time until submissions are closed:
                        <span class="days"> #{days} Days</span>
                        <span class="hours"> #{hours} Hours</span>
                        <span class="minutes"> #{minutes} Minutes</span>
                        <span class="seconds"> #{seconds} Seconds</span>""")
        , 1000

load = ->

    timer()

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

    $('.tags').on 'click','.remove-tag', (e) ->
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

    $('.more-tags').on 'click', (e) ->
        post_id = $('div.post').data('post-id')
        tag = prompt("tag")
        tag_regex = /^[a-zA-Z0-9]+$/g
        if not tag_regex.test(tag)
            alert("Please supply a valid tag name (letters and numbers only)")
        else
            $.ajax
                url: "/addtag/"
                type: "POST"
                data:
                    post_id: post_id
                    tag: tag
                success: (data) ->
                    if data.success
                        $('ul.tags').append(data.html)


$(document).ready load
$(document).on "page:load", load