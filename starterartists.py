#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Artists, Base, Projects, User

engine = create_engine('sqlite:///artistswithusers.db')



# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# projects for adeola olagunju
artist1 = Artists(name="Adeola Olagunju",
                bio="Adeola Olagunju is a Nigerian Artist who lives and works in Lagos, Nigeria.After obtaining a degree in Fine and Applied Arts (Graphic Design) in 2009, Adeola worked as a Graphic Artist for Advertising Agencies in Lagos. Working Primarily with Photography, her artistic practice encompasses a range of medium; including Video, Painting, and Collage. She explores themes around her Environment, Self and Memory with documentary and conceptual approach. Adeola has been on residencies at Kuona Trust Centre for Visual Art in Nairobi, Kenya and the Lagos Photo Summer School exchange programme in Berlin, Germany. She has participated in Photography Master classes and exhibitions locally and internationally",
               imageUrl="""http://adeolaolagunju.com/wp-content/uploads/2016/01/Adeola-Olagunju1-1920x2880.jpg""",
               category="Photography",
               country="Nigeria")

session.add(artist1)
session.commit()


project1 = Projects(title="Home is", description="Through portraiture, staged tableaux and costuming I use photography to explore and invoke rituals of home and home-making. Most recently, this has taken the form of largescale color photographs created outside of, but in relationship to my home in Nigeria.", imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/c_scale,w_897/v1519112813/Home-is_Adeola-Olagunju_2017-4_j8bcpc.jpg""",
artist=artist1)

session.add(project1)
session.commit()

project2 = Projects(title="Resurgence", description="RESURGENCE: A MANIFESTO is a series of photographic performance which portrays the unacceptability and high level of socio-religion and political decadence in Africa", imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/c_scale,w_897/v1519113026/BLOODLINE-BLOODLUST_l1wipv.jpg""",
artist=artist1)

session.add(project2)
session.commit()

#projects for eloghosa osunde
artist2 = Artists(name="Eloghosa Osunde",
               bio="Eloghosa Osunde is a Nigerian writer and visual artist whose work revolves around mental health, sexuality and the psychology of identity and interpersonal intimacies.Eloghosa graduated from the University of Nottingham, UK in 2015. She is an alumna of the Farafina Creative Writing Workshop and has studied screenwriting at New York Film Academy. Her selection of vignettes ‘Shapes’ has been edited and published online by Chimamanda Ngozi Adichie and her short memoir ‘Don’t Let It Bury You’ was published in Catapult.",
               imageUrl="""https://art635.gallery/wp-content/uploads/2018/01/eloghosa-portrait-.jpg""",
               category="Photographer + Writer",
               country="Nigeria")

session.add(artist2)
session.commit()

project1 = Projects(title="And now we have entered broken earth", description="‘And Now We Have Entered Broken Earth’ is an ongoing series exploring intergenerational cycles and their effects on our individual identities. What gets passed down the bloodline? How much of the patterns - persisting through generations - can we ward off completely? What patterns have we resented in our parents, only to find them in ourselves? Is it possible to run far enough away or do we keep redrafting until we can claim ourselves? ", imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/v1519111889/deliverance_vubmja.jpg""",
artist=artist2)

session.add(project1)
session.commit()

project2 = Projects(title="Color this brain", description="Color This Brain' is a six part vision-board on mental health and what (my) neurodivergence looks like in living colour. My brain in six parts, sixteen images and honest hues.", imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/v1519111889/vjdekrfblfrlf_wrgk9x.jpg""",
artist=artist2)

session.add(project2)
session.commit()

artist1 = Artists(name="Yagazie Emezi",
               bio="Yagazie Emezi is a self-taught documentary photographer from Aba, Nigeria. She began her journey in early 2015 and has since been commissioned by Al-Jazeera, New York Times, Vogue, Refinery29, Everyday Projects, and UNFPA. She has also been featured by Huffington Post, Nieman Reports, New York Times, Mashable, Newsweek, and Buzzfeed. In 2017, she was a participant of the World Press Photo Masterclass West Africa and is a contributor to Everyday Africa. Yagazie spent ten months in Liberia on a project around education for girls in at-risk communities while working on her ongoing project Relearning Bodies.",
               imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/v1519111510/emezi_dubmga.webp""",
               category="Photographer",
               country="Nigeria")

session.add(artist1)
session.commit()

project1 = Projects(title="The beauties of West Point", description="In engaging with the women of West Point, Yagazie explained that she wanted to make work that would expand on the idea of women and what makes a beautiful woman, challenging what the globally enforced standard narrowly defines beauty as.", imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/v1519111258/4233ef97f68df8214401ec1293e43205_vswz6n.jpg""",
artist=artist1)

session.add(project1)
session.commit()

project2 = Projects(title="The ease of Monrovia's 'Hipco' Clubs", description="At a nightclub in Liberia, the photographer Yagazie Emezi found a stylish music scene unencumbered by the country’s past", imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/v1519111109/Recognizing_Bodies_Yagazie_Emezi_2016_IB-1862_mzyuls.jpg""",
artist=artist1)

session.add(project2)
session.commit()

artist1 = Artists(name="Yadichinma Ukoha-Kalu",
               bio="Yadichinma is a young and restless artist. She is also eccentric and brilliant, with a body of work that has a certain intricacy to it. Her unique talent is what makes her work compelling, it is also part of the reason she’s gone from her debut group exhibition: woman in bloom, to being selected as one of Rele’s 2016 young contemporaries to working with Maki Oh and Lakin Ogunbanwo during Art X, and then prepping for a solo show scheduled for March in South Africa, all in the space of a year.",
               imageUrl="""http://res.cloudinary.com/didhg8jke/image/upload/v1519111452/yadichinma-ukoha-kalu_1_apzfra.jpg""",
              category="Artist",
              country="Nigeria")

session.add(artist1)
session.commit()

project1 = Projects(title="Of things to come", description="I am becoming through them just as they are through me . “World without end”. Though an end draws near, they continue as they have done all their lives, travelling through mind and imagination of all who seek them in some way. Becoming, forming and then moving again through another unconsciousness.", imageUrl="""https://pbs.twimg.com/media/CvTHVySWgAAc-1L.jpg""",
artist=artist1)

session.add(project1)
session.commit()

project2 = Projects(title="Opening Shadows", description="Universe I, from the Opening Shadows exhibition, #opemingshadows #ottc", imageUrl="""https://payload.persona.co/1/1/43296/152787/YBBO0880_1300.jpg""",
artist=artist1)

session.add(project2)
session.commit()




print "added Artists and projects!"
