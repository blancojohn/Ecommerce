from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# A continuación Tabla pivote porque un producto puede tener una o varias categorías y 
#una categoría puede tener uno o varios productos.
categories_products= db.Table(
    'categories_products',
    db.Column('products_id', db.Integer, db.ForeignKey('products.id'), nullable= False, primary_key= True),
    db.Column('categories_id', db.Integer, db.ForeignKey('categories.id'), nullable= False, primary_key= True)
)

class Product(db.Model):
    __tablename__= 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category= db.Column(db.String(100), nullable= False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    discount = db.Column(db.Float, nullable=True, default=0.0) # Asegurarse de que el valor introducido sea un float por ejemplo 0.20 = 20% de descuento
    favorites_users= db.relationship('Product_Favortite_User', backref= 'product')# Un producto puede ser favorito de una o más personas.
    categories= db.relationship('Category', secondary= categories_products, back_populates= 'products')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "description": self.description,
            "category": self.category,
            "discount": self.discount,
        }
    
class Category(db.Model):
    __tablename__= 'categories'
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String(80))
    products= db.relationship('Product', secondary= categories_products, back_populates= 'categories')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    username = db.Column(db.String(80))
    rating = db.Column(db.Integer)
    text = db.Column(db.String(500))

    def serialize(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "username": self.username,
            "rating": self.rating,
            "text": self.text
        }
    
class User(db.Model): #Contiene los usuarios agragdos al block
    __tablename__ = 'users'
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(120), nullable=False, unique=True)
    email= db.Column(db.String(120), nullable= False, unique= True)
    password= db.Column(db.String(250), nullable= False)
    profile= db.relationship('Profile', backref= 'user', uselist= False) #Un usuario puede tener un solo perfil.
    favorite_product= db.relationship('Product_Favortite_User', backref= 'user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
 # A continuación clase perfil para poder actualizar datos de usaurio.
class Profile(db.Model):
    __tablename__= 'profiles'
    id= db.Column(db.Integer, primary_key= True)
    country= db.Column(db.String(50), default= "")
    state= db.Column(db.String(50), default= "")
    city= db.Column(db.String(50), default= "")
    street= db.Column(db.String(50), default= "")
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))

    def serialize(self):
        return {
            "id": self.id,
            "direction": self.country,
            "state":self.state,
            "city": self.city,
            "street": self.street
        }
    
class Product_Favortite_User(db.Model):
    __tablename__= 'products_favorites_users'
    id= db.Column(db.Integer, primary_key= True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id= db.Column(db.Integer, db.ForeignKey('products.id'))
    
