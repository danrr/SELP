from datetime import datetime, timedelta
from imgurpython import ImgurClient
from app import db
from app.models import User, Post, Submission
from mock import Mock, patch


@patch.object(ImgurClient, 'upload_from_path', Mock(return_value={'link': 'http://i.imgur.com/Sj6yA9J.jpg'}))
def main():
    db.drop_all()
    db.create_all()

    today = datetime.today()

    user1 = User('Erik', 'Erik@ohemgeemail.com', '12345')
    user2 = User('Jane', 'Jane@coldmail.com', 'qwert')
    user3 = User('Mike', 'Mike@oxlarge.com', 'asdfg')
    user4 = User('John', 'John@headtome.com', 'zxcvb')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()

    post1 = Post('Chickpea curry',
                 "Heat a deep saucepan or a medium sized wok and add the oil or butter followed by the onions and"
                 "garlic. Fry the mixture till the onions are caramelised. Then add the salt, cumin, coriander, turmeric"
                 "and red chilli powders. Mix for a minute and tip in the tomato. Cook the sauce until it begins to"
                 "thicken. Add 1/4 cup of water and stir. Then tip in the chickpeas and mix. Mash a few of the chickpeas"
                 "while cooking. Cover and simmer for five minutes. Then add the ginger and the garam masala. Cook for"
                 "another minute. Serve with pitta breads or plain basmati rice.",
                 user3.id, publish_time=today - timedelta(11), difficulty=3)
    post2 = Post('Black pudding',
                 "Wash the pudding skins and soak in salty water overnight. Put the blood into a bowl and add 1"
                 "teaspoon of salt, strain through a fine sieve to a larger bowl. Stir in the milk, suet, onions and"
                 "oatmeal and season with salt and pepper. Now to fill the pudding skins...tie at one end (with string)"
                 "and then turn inside out. Fill it with mixture tie off in equal lengths...like sausages. Place in water"
                 "that is off the boil, after about 5 minutes prick all over with a large needle. Boil for 30 minutes,"
                 "then take out of pan and hang in a cool place to dry.",
                 user3.id, publish_time=today - timedelta(8), difficulty=5)
    post3 = Post('Carrot cake',
                 "Preheat the oven to 180C/Gas 4/fan 160C. Oil and line the base and sides of an 18cm square cake tin"
                 "with baking parchment. The easiest way to do this is to cut two long strips the width of the tin and"
                 "put each strip crossways, covering the base and sides of the tin, with a double layer in the base."
                 "Tip the sugar into a large mixing bowl, pour in the oil and add the eggs. Lightly mix with a wooden"
                 "spoon. Stir in the grated carrots, raisins and orange rind. Mix the flour, bicarbonate of soda and"
                 "spices, then sift into the bowl. Lightly mix all the ingredients - when everything is evenly"
                 "amalgamated stop mixing. The mixture will be fairly soft and almost runny. Pour the mixture into the"
                 "prepared tin and bake for 40-45 minutes, until it feels firm and springy when you press it in the"
                 "centre. Cool in the tin for 5 minutes, then turn it out, peel off the paper and cool on a wire rack."
                 "(You can freeze the cake at this point.) Beat together the frosting ingredients in a small bowl until"
                 "smooth - you want the icing about as runny as single cream. Set the cake on a serving plate and boldly"
                 "drizzle the icing back and forth in diagonal lines over the top, letting it drip down the sides.",
                 user2.id, publish_time=today - timedelta(3), difficulty=2)
    post4 = Post('Soup',
                 "In a large soup pot, heat oil over medium heat. Add onions, carrots and celery; cook and stir until"
                 "onion is tender. Stir in garlic, bay leaf, oregano and basil; cook for 2 minutes. Stir in lentils and"
                 "add water and tomatoes. Bring to the boil. Reduce heat and simmer for at least 1 hour. When ready to"
                 "serve, stir in spinach and cook until it wilts. Stir in vinegar and season to taste with salt and"
                 "pepper and more vinegar if desired.",
                 user1.id, publish_time=today, difficulty=1)
    post5 = Post('Stew',
                 "Preheat the oven to 220 degrees C/425 degrees F/gas 7. Place a large roasting tray in the oven to"
                 "preheat. Carefully remove the hot tray from the oven, then add the oxtail. Season and drizzle over a"
                 "lug of olive oil, then toss to coat and place in the hot oven for around 20 minutes, or until golden"
                 "and caramelized. Meanwhile, trim and halve the leeks and celery lengthways, then chop into rough 2cm"
                 "chunks. Peel and chop the carrots into 2cm pieces, then place into a large ovenproof casserole pan"
                 "over a medium-low heat with 1 tablespoon of olive oil. Pick, roughly chop and add the thyme and"
                 "rosemary leaves, then add the bay and cook for around 20 minutes, or until soft and sweet, stirring"
                 "frequently. Meanwhile, remove the oxtail from the oven and set aside. Reduce the oven temperature to"
                 "170 degrees C/325 degrees F/gas 3. Add the cloves and flour to the veg, stirring well to combine,"
                 "then pour in the tomatoes and porter (or wine, if using). Add the oxtail and any roasting juices,"
                 "cover with the beef stock or 1 litre of cold water and stir well. Turn the heat up to high and bring"
                 "to the boil, then pop the lid on and place in the hot oven for around 5 hours, or until the meat falls"
                 "away from the bone, stirring every hour or so and adding a splash of water to loosen, if needed."
                 "Remove the pan from the oven and leave to cool for about 10 minutes. Using rubber gloves, strip the"
                 "meat from the bones and return to the pan, discarding the bones. Add a good splash of Worcestershire"
                 "sauce, season to taste and enjoy with creamy mash and seasonal steamed greens.",
                 user1.id, publish_time=today + timedelta(3), difficulty=4)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.add(post5)
    db.session.commit()
    post1.add_ingredients(["1 tbsp oil", "1 onion, chopped", "1 garlic clove, crushed", "1/4 tsp salt",
                           "1/2 tsp cumin powder", "1/4 tsp coriander powder", "1/4 tsp turmeric powder",
                           "1/4 tsp red chilli powder", "1 fresh tomato, chopped",
                           "1 x 400g/14oz can chickpeas, drained and rinsed"])
    post2.add_ingredients(["2 Pints Pig or Ox Blood", "1 lb. Chopped Suet", "8 oz. Diced Onions",
                           "1/2 pint Milk", "3 oz. Oatmeal", "Salt and Pepper"])
    post3.add_ingredients(["175g light muscovado sugar", "175ml sunflower oil", "3 large eggs, lightly beaten",
                           "140g grated carrots (about 3 medium)", "100g raisins", "grated zest of 1 large orange",
                           "175g self-raising flour", "1 tsp bicarbonate of soda", "1 tsp ground cinnamon",
                           "1/2 tsp grated nutmeg (freshly grated will give you the best flavour)"])
    post4.add_ingredients(["1 onion, chopped", "4 tablespoons olive oil", "2 carrots, diced",
                           "2 sticks celery, chopped", "2 cloves garlic, finely chopped", "1 teaspoon dried oregano",
                           "1 bay leaf", "1 teaspoon dried basil", "400g passata", "385g dry lentils", "2 litres water",
                           "15g spinach, rinsed and thinly sliced", "2 tablespoons vinegar", "salt to taste",
                           "ground black pepper to taste"])
    post5.add_ingredients(["2.5 kg oxtail, chopped into 4cm chunks (ask your butcher to do this)", "sea salt",
                           "freshly ground black pepper", "olive oil", "2 medium leeks", "2 stalks of celery",
                           "4 medium carrots", "a few sprigs of fresh thyme", "a few sprigs of fresh rosemary",
                           "4 fresh bay leaves", "4 cloves", "2 heaped tablespoons plain flour",
                           "2 x 400 g tins of plum tomatoes", "275 ml porter or red wine"])
    db.session.commit()
    post1.add_tag("curry")
    post1.add_tag("savoury")
    post2.add_tag("blood")
    post3.add_tag("cake")
    post4.add_tag("vegan")
    db.session.commit()

    submission1 = Submission('a/b/c', 'This is my chickpea curry', post_id=post1.id, user_id=user2.id)
    submission2 = Submission('a/b/c', 'This is my chickpea curry', post_id=post1.id, user_id=user1.id)
    submission3 = Submission('a/b/c', 'This is my black pudding', post_id=post2.id, user_id=user1.id)
    submission4 = Submission('a/b/c', 'This is my black pudding', post_id=post2.id, user_id=user2.id)
    submission5 = Submission('a/b/c', 'This is my carrot cake', post_id=post3.id, user_id=user3.id)
    submission6 = Submission('a/b/c', 'This is my carrot cake', post_id=post3.id, user_id=user4.id)
    submission7 = Submission('a/b/c', 'This is my carrot cake', post_id=post3.id, user_id=user1.id)
    db.session.add(submission1)
    db.session.add(submission2)
    db.session.add(submission3)
    db.session.add(submission4)
    db.session.add(submission5)
    db.session.add(submission6)
    db.session.add(submission7)
    db.session.commit()

    submission1.toggle_upvote(user1.id)
    submission1.toggle_upvote(user3.id)
    submission1.toggle_upvote(user4.id)
    submission2.toggle_upvote(user4.id)
    submission2.toggle_upvote(user3.id)
    submission3.toggle_upvote(user3.id)
    submission4.toggle_upvote(user4.id)
    submission5.toggle_upvote(user1.id)
    submission1.make_winner()
    db.session.commit()

if __name__ == "__main__":
    main()