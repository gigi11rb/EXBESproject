from ext import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class Skiing(db.Model,UserMixin):

    __tablename__ = "skies"
    __bind_key__ = "skiing"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())
    stats= db.Column(db.String())

class Skiboots(db.Model,UserMixin):

    __tablename__ = "skiboots"
    __bind_key__ = "skiing"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())
    stats= db.Column(db.String())

class Poles(db.Model,UserMixin):

    __tablename__ = "poles"
    __bind_key__ = "skiing"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())
    stats= db.Column(db.String())


class Snowboarding(db.Model,UserMixin):

    __tablename__ = "boards"
    __bind_key__ = "snowboarding"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())
    stats= db.Column(db.String())

class Boots(db.Model,UserMixin):
    __tablename__ = "boots"
    __bind_key__ = "snowboarding"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())
    stats= db.Column(db.String())

class Bindings(db.Model,UserMixin):
    __tablename__ = "bindings"
    __bind_key__ = "snowboarding"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String()) 
    stats= db.Column(db.String())   

class Goggles(db.Model,UserMixin):
    __tablename__ = "goggles"
    __bind_key__ = "snowboarding"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String()) 
    stats= db.Column(db.String())

class Helmets(db.Model,UserMixin):
    __tablename__ = "helmets"
    __bind_key__ = "snowboarding"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())    
    stats= db.Column(db.String()) 

class Masks(db.Model,UserMixin):
    __tablename__ = "masks"
    __bind_key__ = "snowboarding"
    
    id = db.Column(db.Integer(),primary_key = True)
    img = db.Column(db.String())
    price = db.Column(db.Float())
    description= db.Column(db.String())   
    stats= db.Column(db.String()) 




class User(db.Model,UserMixin):

    __tablename__ = "user"
    
    id = db.Column(db.Integer(),primary_key = True)
    email = db.Column(db.String(),nullable = False)
    username = db.Column(db.String(),nullable = False)
    password= db.Column(db.String(), nullable = False)
    roles = db.Column(db.String())

    def __init__(self, email,username, password, roles="Guest"):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.roles = roles
        
    def check_password(self, password):
        return check_password_hash(self.password, password)    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)    





