Idea, for lack of a better one.
=========

Weekly cooking challenge website.

###Baseline###

Website where user can sign up and receive cooking challenges ranked on a scale based on difficulty, number of ingredients, ease of getting ingredients. Users have a week to upload a photo of their cooking. Pictures can be up and down voted. A user receives credits based on the ranking of the challenge if they upload a picture of it, enough users vote on it, and they have a positive score. Users are ranked based on overall score.

- Stage 1: Recipes can be displayed statically - 15 hours
- Stage 1.5: Recipes can be displayed dynamically from DB - 5 hours
- Stage 2: Users can sign up and sign in - 10 hours
- Stage 3: Users can upload pictures - 10 hours
- Stage 4: Users can vote - 10 hours
- Stage 5: User can be ranked - 10 hours

Tweaks, graphical improvements, bug fixes - 10 hours (maybe a bit optimistic)

###Stretch goals###

- Add the ability for users to submit recipes for future competition for bonus points
- Add the ability for users to create their own competitions.


Technologies and Languages
====================

###Flask back-end with:

  * Jinja2 for templating
  * Flask-login for user session management
  * sqlite with Flask-SQLAlchemy as Object Relational Mapper
  
I find myself to be very productive in Python, and I've used it for a variety of projects before. Out of the available Python web framework, I want to use Flask due to being lightweight, yet extensible. As it's widely used there are stable, well-documented libraries available for most common use cases, as shown by the extensions already chosen. For the database behind the application, I want to use sqlite as it's the simplest option, and is easy to store with the application. With the ORM layer it should be easy to migrate to a better long-term solution. 
 

###Front-end:

 * CoffeeScript compiled into JavaScript
 * jQuery for easy event handling and DOM element selection, with many other features being potentially useful
 * styling will be done in SASS compiled into CSS
 * Bootstrap will form the base of the project
 * Backbone.js might be included if required
 
I want to keep the complexity of the front-end code to a minimum. Ideally, I would like to use it only for display, with the logic being performed by the back-end where possible. I'm not sure that having an MCV framework will be necessary, at least not at the start. I'm not sure if this is the best approach but if I find that my front-end code had grown enough to need it, I'll refactor it on top of Backbone.


###Other technical considerations

For image uploading, I plan on using imgur.com through their free to use API (https://api.imgur.com/) with only links to the pictures being stored in my database.

Questions
======

1. Are the stages sensible divisions of work? Do you consider that the effort estimates are suitable?
2. Is the overall volume of work suitable for the course? If not, what should I expand upon?
3. Do you think my assumption regarding the client-side code is valid, or would I be better off using Backbone from the start?
4. On the whole, do you think the choice of technologies meshes well with the planned outcome?
