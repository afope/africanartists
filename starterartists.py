
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Artists, Base, Projects

engine = create_engine('sqlite:///artistdatabase.db')
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



artist1 = Artists(name="Lorem Ipsum",
                bio="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo",
               imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
               category="Lorem Ipsum",
               country="Lorem Ipsum")

session.add(artist1)
session.commit()

project1 = Projects(title="hey", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist1)

session.add(project1)
session.commit()

project2 = Projects(title="there", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist1)

session.add(project2)
session.commit()

artist2 = Artists(name="Lorem Ipsum",
               bio="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo",
               imageUrl="""https://cdn.theculturetrip.com/images/56-3632528-4532000718-b568541910-o.jpg""",
               category="Lorem Ipsum",
               country="Lorem Ipsum")

session.add(artist2)
session.commit()

project1 = Projects(title="what", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist2)

session.add(project1)
session.commit()

project2 = Projects(title="is", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist2)

session.add(project2)
session.commit()

artist3 = Artists(name="Lorem Ipsum",
               bio="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo",
               imageUrl="""https://cdn.theculturetrip.com/images/56-3632551-800px-ato-malinda-video-3267-moy.jpg""",
               category="Lorem Ipsum",
               country="Lorem Ipsum")

session.add(artist3)
session.commit()

project1 = Projects(title="up", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist3)

session.add(project1)
session.commit()

project2 = Projects(title="i", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist3)

session.add(project2)
session.commit()

artist4 = Artists(name="Lorem Ipsum",
               bio="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo",
               imageUrl="""https://cdn.theculturetrip.com/images/56-3632553-5719247401-a11550f68d-o.jpg""",
              category="Lorem Ipsum",
              country="Lorem Ipsum")

session.add(artist4)
session.commit()

project1 = Projects(title="miss", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist4)

session.add(project1)
session.commit()

project2 = Projects(title="you", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist4)

session.add(project2)
session.commit()

artist5 = Artists(name="Lorem Ipsum",
               bio="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo",
               imageUrl="""https://image.theculturetrip.com/fit-in/1024x/images/56-3632572-girl-in-car-with-father2.jpg""",
               category="Lorem Ipsum",
               country="Lorem Ipsum")

session.add(artist5)
session.commit()


project1 = Projects(title="so", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist5)

session.add(project1)
session.commit()

project2 = Projects(title="much", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", imageUrl="""https://cdn.theculturetrip.com/images/56-3632575-6755478359-737f995e95-o.jpg""",
artist=artist5)

session.add(project2)
session.commit()



print "added Artists and projects!"
