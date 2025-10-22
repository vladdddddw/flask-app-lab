from flask import Blueprint, render_template, request, redirect, url_for


users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.route("/hi/<string:name>") # [cite: 361]
def greetings(name): # [cite: 362]

    age = request.args.get("age")

    return render_template("users/hi.html", name=name.upper(), age=age) # [cite: 364, 366]

@users_bp.route("/admin") # [cite: 368]
def admin():

    return redirect(url_for("users.greetings", name="Administrator"))