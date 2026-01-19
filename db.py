from ext import app, db
from models import User,Snowboarding,Boots,Bindings,Goggles,Helmets,Skiing,Skiboots,Poles,Masks
import os

with app.app_context():
    # db.drop_all()
    db.create_all()
    
    # admin = User(email="admin@gmail.com",username="admin", password="A12345", roles="Admin")
    # db.session.add(admin)
    # db.session.commit()     



    image_folder = os.path.join(app.root_path, 'static/snowboarding/boots')
    price_file = os.path.join(app.root_path, 'static/snowboarding/boots/prices.txt')
    description_file = os.path.join(app.root_path, 'static/snowboarding/boots/description.txt')
    stats_file = os.path.join(app.root_path, 'static/snowboarding/boots/stats.txt')

    image_files=[]
    
    for file_name in os.listdir(image_folder):
        if file_name.lower().endswith(('.png', '.jpg')):
            image_files.append(file_name)

    image_files.sort()

    file = open(price_file, 'r')
    file2 = open(description_file, 'r')
    file3 = open(stats_file, 'r')

    for filename in image_files:
        line = file.readline()
        line2 = file2.readline()
        line3 = file3.readline()

        price = float(line)
        description = str(line2)
        stats = str(line3)

        image=Boots(
            img=filename,
            price=price,
            description = description,
            stats = stats
        )
        db.session.add(image)

    file.close()
    file2.close()
    file3.close()

    db.session.commit()
