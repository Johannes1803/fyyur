# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import sys

import dateutil.parser
import babel
import sqlalchemy
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    abort,
)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_wtf.csrf import CSRFProtect

from model import Venue, Artist, Show, db

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db.app = app
db.init_app(app)

csrf = CSRFProtect(app)

migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    try:
        date = dateutil.parser.parse(value)
    except TypeError:
        date = value
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    with app.app_context():
        all_venues = Venue.query.order_by(Venue.name).all()

        venues_with_distinct_location = (
            Venue.query.distinct(Venue.city, Venue.state)
            .order_by(Venue.city.desc(), Venue.state.desc())
            .all()
        )

        places_as_dict = [
            {"state": venue.state, "city": venue.city}
            for venue in venues_with_distinct_location
        ]
        for place in places_as_dict:
            place["venues"] = []
            for venue in all_venues:
                if venue.state == place.get("state") and venue.city == place.get(
                    "city"
                ):
                    place["venues"].append(venue)

        return render_template("pages/venues.html", areas=places_as_dict)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [
            {
                "id": 2,
                "name": "The Dueling Pianos Bar",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    with app.app_context():
        venue = Venue.query.get(venue_id)
        app.logger.debug(venue.upcoming_shows)
        return render_template("pages/show_venue.html", venue=venue)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        with app.app_context():
            data = {}
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=form.genres.data,
                image_link=form.image_link.data,
                website_link=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
            )
            error = False
            try:
                db.session.add(venue)
                db.session.commit()
                data["name"] = venue.name
            except Exception as e:
                db.session.rollback()
                print(sys.exc_info())
                error = True
            finally:
                db.session.close()
            if error:
                flash(
                    f'An error occurred. Venue {data.get("name")} could not be listed.'
                )
                abort(400)
            else:
                # on successful db insert, flash success
                flash(f"Venue {data.get('name')} was successfully listed!")
                return render_template("pages/home.html")
    else:
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        return render_template("forms/new_venue.html", form=form)


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button deletes it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    artists = Artist.query.order_by(Artist.name).all()
    return render_template("pages/artists.html", artists=artists)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [
            {
                "id": 4,
                "name": "Guns N Petals",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    with app.app_context():
        artist = Artist.query.get(artist_id)
        return render_template("pages/show_artist.html", artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    with app.app_context():
        artist = Artist.query.get(artist_id)
        form = ArtistForm(
            name=artist.name,
            city=artist.city,
            state=artist.state,
            phone=artist.phone,
            image_link=artist.image_link,
            genres=artist.genres,
            facebook_link=artist.facebook_link,
            website_link=artist.website_link,
            seeking_venue=artist.seeking_venue,
            seeking_description=artist.seeking_description,
        )
        return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    if form.validate_on_submit():
        app.logger.debug(f"form.seeking_venue.data: {form.seeking_venue.data}")
        with app.app_context():
            error = False
            try:
                artist = Artist.query.get(artist_id)

                artist.name = form.name.data
                artist.city = form.city.data
                artist.state = form.state.data
                artist.phone = form.phone.data
                artist.genres = form.genres.data
                artist.image_link = form.image_link.data
                artist.website_link = form.website_link.data
                artist.facebook_link = form.facebook_link.data
                artist.seeking_venue = form.seeking_venue.data
                artist.seeking_description = form.seeking_description.data

                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(sys.exc_info())
                error = True
            finally:
                db.session.close()
            if error:
                flash(f"An error occurred. Artist could not be updated.")
                abort(400)
            else:
                # on successful db insert, flash success
                flash(f"Artist was successfully updated!")
                return render_template("pages/home.html")
    else:
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        return redirect(url_for("edit_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    with app.app_context():
        venue = Venue.query.get(venue_id)
        form = VenueForm(
            name=venue.name,
            city=venue.city,
            state=venue.state,
            address=venue.address,
            phone=venue.phone,
            image_link=venue.image_link,
            genres=venue.genres,
            facebook_link=venue.facebook_link,
            website_link=venue.website_link,
            seeking_talent=venue.seeking_talent,
            seeking_description=venue.seeking_description,
        )
        return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm()
    if form.validate_on_submit():
        with app.app_context():
            data = {}
            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=form.genres.data,
                image_link=form.image_link.data,
                website=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data
            )
            error = False
            try:
                db.session.add(artist)
                db.session.commit()
                data["name"] = artist.name
            except Exception as e:
                db.session.rollback()
                print(sys.exc_info())
                error = True
            finally:
                db.session.close()
            if error:
                flash(
                    f'An error occurred. Artist {data.get("name")} could not be listed.'
                )
                abort(400)
            else:
                # on successful db insert, flash success
                flash(f"Artist {data.get('name')} was successfully listed!")
                return render_template("pages/home.html")
    else:
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        return render_template("forms/new_artist.html", form=form)


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    shows = Show.query.order_by(Show.start_time).all()
    return render_template("pages/shows.html", shows=shows)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm()
    if form.validate_on_submit():
        with app.app_context():
            show = Show(
                start_time=form.start_time.data,
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
            )
            error = False
            try:
                db.session.add(show)
                db.session.commit()
            except IntegrityError as e:
                flash(
                    f"Make sure that venue id and artist id exist. Show could not be listed."
                )
                error = True
                db.session.rollback()
                print(sys.exc_info())
            except sqlalchemy.exc.DataError as e:
                flash(
                    f"Make sure that venue id and artist id are integers. Show could not be listed."
                )
                db.session.rollback()
                print(sys.exc_info())
                error = True
            finally:
                db.session.close()
            if error:
                return render_template("pages/home.html")
            else:
                # on successful db insert, flash success
                flash("Show was successfully listed!")
                return render_template("pages/home.html")
    else:
        message = []
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " + str(message))
        return render_template("forms/new_show.html", form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
