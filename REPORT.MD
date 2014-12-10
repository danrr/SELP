#Report#
##or how I learned to stop worrying and love the Flask##


###Introduction###
	
I set out to build a website on which users could challenge each other to cook various recipes and be awarded points based on the quality of their posts and submissions. In this scenario, quality is indicated by the interest of other users as measured by the number of submissions and the number of upvotes each submission received.

I think that this goal has been achieved and through implementing it and the additional features included in the project I have demonstrated my software engineering skills such as use of source control, writing well-organized code, or identifying and implementing useful refactorings. As such, the project achieved the learning outcomes of the course and deserves a high mark.

The main features that I mentioned in the proposal have been implemented and are working correctly within the simplifying assumptions I made which I will discuss later. The following features have been delivered:

- users can log in and register
- users can create recipes, and edit or delete them
- recipes can have an arbitrary number of ingredients
- users can submit entries to challenges
- the authors of challenges can choose winning entries
- users are assigned scores based on upvotes, number of submissions, and post difficulty
- users are ranked based on aforementioned score system
- users are can add tags to posts and the author can remove them
- users can look up posts based on their title, body, tags or difficulty using the search feature
- users can dynamically load more posts when not all are shown

###Development###
In the development of this application I emphasised the use of libraries and frameworks to minimise the effort spent on developing already existing functionality so I could better focus my time on adding features on top of the external resources. Although Flask does not come built-in with many of the features I used and other frameworks like Django do, Flask has a very rich ecosystem of plug-ins. The ability to choose between multiple libraries that achieve the same result is valuable, as I could choose the one that best suited the needs of the project or my style of programming. As an example I chose to use Flask-SQLalchemy over vanilla SQLalchemy as I preferred the query syntax of the former.

A number of features present in the app were very easy to develop through the use of libraries. Database interactions are done through Flask-SQLalchemy, user login is done through Flask-login, form generation is done through Flask-WTF, and searching the title or body of a post is done through Flask-whooshalchemy. The client-side part of the app has also benefited from using external resources, styling and user interactions have been built on top of Bootstrap which is a great time-saver.

Although choice is great, it requires a careful reading of the documentation. One of the mistakes I made during development was choosing python-scss to compile SCSS files. This library is no longer supported by the author and a quick look at the Github page for it would have pointed me towards pyScss, a more up-to-date library. I only realised my mistake when attempting to use media queries in my SCSS which the old library was not able to parse.

Another poor choice was using node.js to compile the coffeescript. Using node caused me to waste a good deal of time finding a good way to set up an isolated version of it. Although this is the best choice from a feature point of view, and if the project were to grow it might have been needed, there were simpler alternatives that would have covered my limited use, like using python-coffeescript or adding a javascript coffeescript parser from a CDN.

####Refactoring and optimization####
Many of the refactorings I performed have removed code from the view functions. This was done to remove complex database queries or data manipulation and keep the view functions *pure*, which helps with testing and keeps similar code together.

One such refactoring was done on the search endpoints. The functions that parsed the query string and generated a cleaned up string were pulled out into *helpers.py* and had unit test created for them. The database query was pulled into the Post model with the other methods that return lists of posts, and list comprehensions over large lists of posts obtained by first searching for the terms were replaced by query composition leveraging the power of SQL and SQLalchemy.

###Structure###
####Code####
The repository is split into modules that have specific functions, for example the test code and databases can be found in the *tests* module. The structure of the repository has not changed drastically over the development of the application; I settled on this division of code early in the architecture phase and it was sensible enough to not need any major revision. A detailed description of the structure of the repo can be found in the readme file.

The driving idea behind the current structure of the app module was separating code by its purpose. The view functions are intended to do as little data manipulation as possible, being responsible only for passing the data to and from the user. More complex logic has been extracted into the *helpers.py* file, this allows this logic to be unit tested independently of the actual views. All logic regarding the models and database queries is contained within *models.py* by the same principles. Splitting code up in this manner helps with unit testing, and bug investigation, as the nature of the fault very strongly hints at where the issue might lie.

The structure is easily adaptable if the application grows beyond what is sensible to put into the current structure. As an example the views file could be split up and turned into a module containing blueprints if many more views are needed, without needing to change much other than the import statements, or more tests can be added by just adding a file in the test folder.

The only part of the app that I feel could pose issues when expanding would be the coffeescript and SCSS files. Splitting these up would require non-trivial changes to scripts that compile them. In the case of SCSS, there is also the complication of not using Compass but a Python library for compilation. This means that many features available in Compass are missing such as vendor prefix mixins or sprite generation, which might trip up someone who has only used SCSS with Compass. It also means that the app is not dependent on any Ruby gems and the extra complexity they would introduce to the setup process without immediate benefits. Not using Compass is a trade-off which in my opinion is worth it for the initial phase of development at least, especially when considering that the styling of the app is built on Bootstrap so the layout of the page can be substantially modified by only adding or removing classes in the templates.

####Database####

The design of the database has been a very iterative process, with new models, tables, and attributes being added as needed, the requirements of new features driving the modifications to the database. The user model was first added for the account functionality, the post model was added to display stored content on the home page, the tag model was added when the ability to tag posts was put in place. This approach has meant that very little effort was spent on database structures that were not used. 

The following diagrams show the current database schema used by the app.

<span style="display:block; text-align: center"> 
![Diagram of the main components of the database: User, Post and Submission](http://i.imgur.com/phkObpp.png)
<span>Diagram of the main components of the database: User, Post and Submission</span>
</span>

<span style="float: right; display:block; text-align: center">
![Diagram of Post with the components related to it: Tag and Ingredient](http://i.imgur.com/Q6VEbbn.png)
<span style="display: block; margin: 0 auto">Diagram of Post with the components related to it: Tag and Ingredient</span>
</span>

The current structure is described entirely in the models file, all tables and models with their attributes can be found in one place. To change the structure of the databases, one only needs to change the models described in this file, and run the *db\_migrate.py* and *db\_upgrade.py* scripts. The *db\_reset.py* script, responsible for populating an empty database, might also need to be modified though this is not required for the app to work. Major changes will require changes to the tests in *test\_models.py*.

The app and test databases being generated and populated automatically make it easy to make changes to the repo locally against a mock database and then deploy the code without losing data on the production database or checking a database file into git. 

###Test strategy###


###Conclusion###