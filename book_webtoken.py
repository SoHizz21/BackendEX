from flask import Flask,jsonify,request
from flask_jwt_extended import JWTManager,jwt_required,create_access_token

app = Flask(__name__)

app.config['JWT_SECRET_KEY']="your_jwt_secret_key"
jwt=JWTManager(app)

books=[
    {"id":1,"title":"Book 1","author":"Author 1"},
    {"id":2,"title":"Book 2","author":"Author 2"},
    {"id":3,"title":"Book 3","author":"Author 3"}
]

@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    username =data.get('username',None)
    password =data.get('password',None)
    if username == 'user' and password=='pass':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token),200
    else:
        return jsonify({"error":"Invalid Credential"}),401
    


@app.route("/")
def Greet():
    return "<p>Welcome to Book Management Systems</p>"

@app.route("/books",methods=["GET"])
@jwt_required()
def get_all_books():
    return jsonify({"books":books})

@app.route("/books/<int:book_id>",methods=["GET"])
@jwt_required()
def get_book(book_id):
    book=next( (b for b in books if b["id"]==book_id),None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error":"Book not found"}),404

@app.route("/books",methods=["POST"]) #Post
@jwt_required()
def create_book():
    data = request.get_json()
    new_book={
        "id" : len(books)+1,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    return jsonify(new_book),201

#delete VER1
# @app.route("/books/<int:book_id>",methods=["DELETE"])
# def delete_book(book_id):
#     global books
#     books = [b for b in books if b ["id"]!= book_id]
#     return jsonify({"message":"Book delete Successfully"})


@app.route("/books/<int:book_id>",methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    book = next((b for b in books if b["id"]==book_id),None)
    if book:
        books.remove(book)
        return jsonify({"message":"Book delete Successfully"})
    else:
        return jsonify({"message":"Book not found"})
    

@app.route("/books/<int:book_id>",methods=["PUT"])
@jwt_required()
def update_book(book_id):
    book = next((b for b in books if b["id"]==book_id),None)
    if book:
        data = request.get_json()
        book.update(data)
        return jsonify({"message":"Book update Successfully"})
    else:
        return jsonify({"message":"Book not found"}),404

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)