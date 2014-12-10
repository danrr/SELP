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

onClickUpvote = (e) ->
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

onClickRemoveTag = (e) ->
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

onClickMoreTags = (e) ->
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

onClickMoreIngredients = (e) ->
    incrementAttribute = (attr, $el)->
        oldValue = $el.attr(attr)
        number = parseInt(oldValue.charAt(oldValue.length - 1))
        number++
        newValue = "ingredients-#{number}"  # hard coding it for now,
                                            # can be refactored to be more general if need be
        $el.attr(attr, newValue)

    $formList = $(e.currentTarget).parent()
    $lastInput =  $formList.find('input:last-of-type')
    $newInput = $lastInput.clone()
    $newInput.val("")
    incrementAttribute("id", $newInput)
    incrementAttribute("name", $newInput)
    $lastInput.after($newInput)

onClickLessIngredients = (e) ->
    $formList = $(e.currentTarget).parent()
    $lastInput =  $formList.find('input:last-of-type')
    $lastInput.remove() unless $lastInput.attr("id") == "ingredients-0"  # don't remove the input field if there is
                                                                         # only one, hard coded for now

onClickShowMore = (e) ->
    $el = $(e.currentTarget)
    page = $el.data("page")
    status = $el.data("status")
    query = $el.data("query")
    $.ajax
        url : "/getmore/"
        type: "POST"
        data:
            page: page
            status: status
            query: query
            start: window.offsets[status]
        success: (data) ->
            if data.success
                window.offsets[status] += data.posts.length
                for post in data.posts
                    $el.before(post)
            else
                $el.before('<div class="alert alert-danger">No more posts to show</div>')
                $el.remove()

load = ->
    # events
    $('.upvote').on "click", "a", onClickUpvote
    $('.tags').on 'click','.remove-tag', onClickRemoveTag
    $('.more-tags').on 'click', onClickMoreTags
    $('.more-ingredients').on 'click', onClickMoreIngredients
    $('.less-ingredients').on 'click', onClickLessIngredients
    $('.show-more-posts').on 'click', onClickShowMore

    timer()

    $('#datepicker').datetimepicker(
        sideBySide: true
        minDate: moment()
        useSeconds: false
        defaultDate: moment()
    )

$(document).ready load
$(document).on "page:load", load