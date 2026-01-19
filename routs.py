from flask import render_template,redirect,session,request,abort
from forms import RegisterForm,LoginForm, PriceForm
from models import User,Snowboarding,Boots,Bindings,Goggles,Helmets,Skiing,Skiboots,Poles,Masks
from ext import app,db
from flask_login import login_user , logout_user,current_user,login_required
import os
import base64
from io import BytesIO
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")  

client = InferenceClient(
    provider="nscale",
    api_key=HF_TOKEN
)




@app.route("/")
def home():
    return render_template("index.html")


routes = {
    "boards": [Snowboarding, "boards.html"],
    "boots": [Boots, "boots.html"],
    "bindings": [Bindings, "bindings.html"],
    "goggles": [Goggles, "goggles.html"],
    "helmets": [Helmets, "helmets.html"],
    "skies": [Skiing, "skies.html"],
    "skiboots": [Skiboots, "skiboots.html"],
    "poles": [Poles, "poles.html"],
    "masks": [Masks, "masks.html"],
}
@app.route("/<page>",methods=["POST", "GET"] )
def pages(page):
    form = PriceForm()
    data = routes.get(page)
    model = data[0]
    new_model = model.query
    #price filterer
    if form.validate_on_submit():
        if form.min.data is not None:
            new_model = new_model.filter(model.price >= form.min.data)
        if form.max.data is not None:
            new_model = new_model.filter(model.price <= form.max.data)   

    template = data[1]
    products = new_model.all()
    return render_template(template, products=products, form=form, category=page)


@app.route("/<string:model2>/<string:model>/<int:id>")
@app.route("/<string:model>/<int:id>")
def detailed(model, id, model2=None):

    product_model = {
        "snowboarding":{
            "boards": Snowboarding,
            "boots": Boots,
            "bindings": Bindings},

        "helmets": Helmets,
        "goggles": Goggles,
        "masks": Masks,

        "skiing":{
            "skies": Skiing,
            "boots": Skiboots,
            "poles": Poles}
        }

    if model2:
        model2s = product_model.get(model2)
        if model2s:
            models = model2s.get(model)
    else:
        models = product_model.get(model)

    product = models.query.get(id)
    return render_template("detailed.html", product=product, model=model, model2=model2)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    user_id = str(current_user.id)
    img = request.form.get("img")
    price = float(request.form.get("price"))
    description = request.form.get("description")
    model = request.form.get("model")
    model2 = request.form.get("model2")
    product_id = request.form.get("product_id")

    # build correct URL ONCE
    

    if "cart" not in session:
        session["cart"] = {}

    if user_id not in session["cart"]:
        session["cart"][user_id] = {}

    cart = session["cart"][user_id]
    if model2:
        product_url = f"/{model2}/{model}/{product_id}"
    else:
        product_url = f"/{model}/{product_id}"
        
    if img not in cart:
        cart[img] = {
            "price":price,
            "description":description,
            "url": product_url,
            "qty": 1
        }
    else:
        cart[img]["qty"] += 1

    session.modified = True
    return redirect(request.referrer)

@app.route("/cart")
def cart():
    cart = session.get("cart", {}).get(str(current_user.id), {})
    return render_template("cart.html", cart=cart)

@app.route("/cart/update", methods=["POST"])
def update_cart():
    user_id = str(current_user.id)

    img = request.form.get("img")
    action = request.form.get("action")

    if "cart" in session and user_id in session["cart"]:
        user_cart = session["cart"][user_id]

        if img in user_cart:
            if action == "plus":
                user_cart[img]["qty"] += 1

            elif action == "minus":
                user_cart[img]["qty"] -= 1

                if user_cart[img]["qty"] <= 0:
                    user_cart.pop(img)

    session.modified = True
    return redirect(request.referrer)

@app.route("/clear-cart", methods=["POST"])
def clear_cart():
    if current_user.is_authenticated:
        user_id = str(current_user.id)
        if "cart" in session and user_id in session["cart"]:
            session["cart"].pop(user_id)
            session.modified = True
    return redirect(request.referrer)


@app.route("/login",methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data).first()

        if user or user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    form = RegisterForm()
    if form.validate_on_submit():
        new_form = User(email = form.email.data, password = form.password.data, username = form.username.data)
        db.session.add(new_form)
        db.session.commit()
        login_user(new_form)
        return redirect("/")

    return render_template("signin.html",form=form)

@app.route("/admin/delete-product/<string:model2>/<string:model>/<int:product_id>", methods=["POST"])
@app.route("/admin/delete-product/<string:model>/<int:product_id>", methods=["POST"])
@login_required
def delete_product(model, product_id ,model2=None):
    # Only Admin
    if current_user.roles != "Admin":
        abort(403)

    # Get product model dynamically
    product_models = {
        "snowboarding":{
            "boards": Snowboarding,
            "boots": Boots,
            "bindings": Bindings},

        "helmets": Helmets,
        "goggles": Goggles,
        "masks": Masks,

        "skiing":{
            "skies": Skiing,
            "boots": Skiboots,
            "poles": Poles}
        }

    if model2:
        model2s = product_models.get(model2)
        if model2s:
            models = model2s.get(model)
    else:
        models = product_models.get(model)

    product = models.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(request.referrer)

@app.route("/generate_image", methods=["GET", "POST"])
def generate_image():
    image_base64 = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            try:
                image = client.text_to_image(
                    prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0"
                )

                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            except Exception as e:
                print("Error generating image:", str(e))

    return render_template("generate_image.html", image_base64=image_base64)