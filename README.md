Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Overview
The following functionality is available:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

## Getting Started (as user of the website):
Fyyur is not currently hosted and hence only available locally. Follow the instructions to set it up locally and see it in action:
### 1. **Fork this repository**
### 2. Backend Dependencies
#### 2.1 **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/activate
```

#### 2.2 Install pip dependencies from requirements file:
From project root, run:
```
pip install -r requirements.txt
```

### 3. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.

```
node -v
npm -v
```

Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```

### 5. Configure DB and flask
Setup a postgresql db (can be local) with name fyyur. Add credentials to a new `.env` file. Never include this file in version control. Refer to `.env-dummy` as an example file with further details.

### 4. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

### 5. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 
## Tech Stack (Dependencies)

### 1. Backend Dependencies
The tech stack includes the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
 * **Flask-WTF** for form handling


### 2. Frontend Dependencies
- HTML
- CSS
- Javascript
- Bootstrap3, which depends on npm and Node.ls


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes route handling.
                    "python app.py" to run after installing dependencies
  |── models.py *** includes the db models of sql-alchemy
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` --  Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `model.py` --  Defines the data models that set up the database tables.
* `config.py` --  Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


#### Data Handling with `Flask-WTF` Forms
The starter codes use an interactive form builder library called [Flask-WTF](https://flask-wtf.readthedocs.io/). This library provides useful functionality, such as form validation and error handling. You can peruse the Show, Venue, and Artist form builders in `forms.py` file. The WTForms are instantiated in the `app.py` file. For example, in the `create_shows()` function, the Show form is instantiated from the command: `form = ShowForm()`. To manage the request from Flask-WTF form, each field from the form has a `data` attribute containing the value from user input. For example, to handle the `venue_id` data from the Venue form, you can use: `show = Show(venue_id=form.venue_id.data)`, instead of using `request.form['venue_id']`.


### Ideas for future improvements
-----
*  Implement artist availability. An artist can list available times that they can be booked. Restrict venues from being able to create shows with artists during a show time that is outside of their availability.
* Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
* Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.


## Authors
This project is part of the [udacity Full Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044?gclid=CjwKCAiAkfucBhBBEiwAFjbkr_M8-oRE1hmGH_7LQzVlqafZmtTw7qiB1l7FpTsK9Vw-BB6kOy3B5xoC8NEQAvD_BwE&utm_campaign=19167921312_c_individuals_holidaypromo&utm_campaign=19167921312_c_individuals&utm_keyword=full%20stack%20udacity_e&utm_keyword=full%20stack%20udacity_e&utm_medium=ads_r&utm_medium=ads_r&utm_source=gsem_brand&utm_source=gsem_brand&utm_term=143524476679&utm_term=143524476679). Accordingly, the starter code comprising the frontend and some parts of the backend were provided by udacity. My contribution was to finish the backend implementation.
