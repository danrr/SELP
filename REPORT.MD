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



###Structure###

<span style="display:block; text-align: center"> 
![Diagram of the main components of the database: User, Post and Submission](http://i.imgur.com/phkObpp.png)
<span>Diagram of the main components of the database: User, Post and Submission</span>
</span>


<span style="float: right; display:block; text-align: center">
![Diagram of Post with the components related to it: Tag and Ingredient](http://i.imgur.com/Q6VEbbn.png)
<span style="display: block; margin: 0 auto">Diagram of Post with the components related to it: Tag and Ingredient</span>
</span>