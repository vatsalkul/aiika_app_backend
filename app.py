from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedr = os.path.abspath(os.path.dirname(__file__))
# setup db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:ncrtncrt@aiika.c75muf0sprwy.ap-south-1.rds.amazonaws.com/innodb'
#'sqlite:///' + os.path.join(basedr, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'content', 'status')

class galerySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'parent', 'status')

class DirectorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'father', 'email', 'occupation', 'city', 'state', 'country', 'mobile')        
                


           

# Init schema
Product_schema = ProductSchema()
Products_schema = ProductSchema(many=True)

galery_schema = galerySchema()
galerys_schema = galerySchema(many=True)

Directory_schema = DirectorySchema()
Directorys_schema = DirectorySchema(many=True)



# get all info
class Directory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    father = db.Column(db.String(200))
    email = db.Column(db.String(200))
    occupation = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    country = db.Column(db.String(200))
    mobile = db.Column(db.String(200))
   
    def __init__(self, name, father, email, occupation, city, state, country, mobile):
        self.name = name
        self.father = father
        self.email = email
        self.occupation = occupation 
        self.city = city
        self.state = state
        self.country = country
        self.mobile = mobile

class tbl_pages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    content = db.Column(db.String(200))
    status = db.Column(db.Integer)
  
    def __init__(self, name, content, status):
        self.name = name
        self.content = content
        self.status = status 

class photo_gallery(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    status = db.Column(db.Integer)
    parent = db.Column(db.Integer)
    

  
    def __init__(self, name, status, parent):
        self.name = name
        self.status = status
        self.parent = parent



@app.route('/product', methods=['POST'])
def add_person():
    
    
        name = request.json['name']
        father = request.json['father']
        email = request.json['email']
        occupation = request.json['occupation']
        city = request.json['city']
        state = request.json['state']
        country = request.json['country']
        mobile = request.json['mobile']
        
        new_person = Directory(name, father, email, occupation, city, state, country, mobile)
        email_exist = bool(Directory.query.filter_by(email=email).first())
        
        if email_exist:
            return jsonify({'error': 'Details are already present'})
        else: 
            db.session.add(new_person)
            db.session.commit()

        return jsonify({'success': 'You are successfully added to AIIKA Directory'})


@app.route('/product', methods=['GET'])
def get_state():

    all_State = photo_gallery.query.all()
    result = galerys_schema.dump(all_State)
   
    return jsonify({"News" : result})
    

@app.route('/directory', methods=['GET'])
def get_directory():

    dir = Directory.query.all()
    result = Directorys_schema.dump(dir)
   
    return jsonify(result)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)