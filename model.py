from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120), nullable=False)
    shows = db.relationship("Show", backref="venue", lazy="joined", cascade='all, delete')
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))


    @property
    def upcoming_shows(self):
        return [show for show in self.shows if show.is_upcoming]

    @property
    def past_shows(self):
        return [show for show in self.shows if show.is_in_past]

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    @property
    def past_shows_count(self):
        return len(self.past_shows)


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship("Show", backref="artist", lazy="joined", cascade='all, delete')
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    @property
    def upcoming_shows(self):
        return [show for show in self.shows if show.is_upcoming]

    @property
    def past_shows(self):
        return [show for show in self.shows if show.is_in_past]

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    @property
    def past_shows_count(self):
        return len(self.past_shows)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)


    @property
    def is_upcoming(self) -> bool:
        """
        Return true if show is in the future.
        """
        if self.start_time >= datetime.now():
            self._is_upcoming = True
        else:
            self._is_upcoming = False
        return self._is_upcoming

    @property
    def is_in_past(self) -> bool:
        """
        Return true if show is in the past.
        """
        return not self._is_upcoming
