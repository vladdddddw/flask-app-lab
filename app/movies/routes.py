from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Movie, Genre
from .forms import MovieForm

movies_bp = Blueprint("movies", __name__, template_folder="../templates/movies")


def populate_genre_choices(form: MovieForm):
    genres = Genre.query.order_by(Genre.name).all()
    form.genre_id.choices = [(g.id, g.name) for g in genres]


@movies_bp.route("/")
@login_required
def list_movies():
    search_query = request.args.get("q", "", type=str).strip()
    sort_by = request.args.get("sort", "created_at")

    query = Movie.query.filter_by(owner_id=current_user.id)

    if search_query:
        like = f"%{search_query}%"
        query = query.filter(Movie.title.ilike(like))

    if sort_by == "title":
        query = query.order_by(Movie.title.asc())
    elif sort_by == "year":
        query = query.order_by(Movie.year.desc().nullslast())
    elif sort_by == "rating":
        query = query.order_by(Movie.rating.desc().nullslast())
    else:
        query = query.order_by(Movie.created_at.desc())

    movies = query.all()
    return render_template("movies/list.html", movies=movies, search_query=search_query, sort_by=sort_by)


@movies_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_movie():
    form = MovieForm()
    populate_genre_choices(form)

    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            year=form.year.data,
            rating=form.rating.data,
            genre_id=form.genre_id.data,
            owner_id=current_user.id,
        )
        db.session.add(movie)
        db.session.commit()
        flash("Movie has been created.", "success")
        return redirect(url_for("movies.list_movies"))

    return render_template("movies/create_edit.html", form=form, title="Add movie")


@movies_bp.route("/<int:movie_id>")
@login_required
def movie_detail(movie_id: int):
    movie = Movie.query.get_or_404(movie_id)
    if movie.owner_id != current_user.id:
        abort(403)
    return render_template("movies/detail.html", movie=movie)


@movies_bp.route("/<int:movie_id>/edit", methods=["GET", "POST"])
@login_required
def edit_movie(movie_id: int):
    movie = Movie.query.get_or_404(movie_id)
    if movie.owner_id != current_user.id:
        abort(403)

    form = MovieForm(obj=movie)
    populate_genre_choices(form)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.year = form.year.data
        movie.rating = form.rating.data
        movie.genre_id = form.genre_id.data
        db.session.commit()
        flash("Movie has been updated.", "success")
        return redirect(url_for("movies.movie_detail", movie_id=movie.id))

    return render_template("movies/create_edit.html", form=form, title="Edit movie")


@movies_bp.route("/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_movie(movie_id: int):
    movie = Movie.query.get_or_404(movie_id)
    if movie.owner_id != current_user.id:
        abort(403)

    db.session.delete(movie)
    db.session.commit()
    flash("Movie has been deleted.", "info")
    return redirect(url_for("movies.list_movies"))
