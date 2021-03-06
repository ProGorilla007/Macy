# Macy

# DEMO
---


# Features

Macy let the users share their customized information in a moment. 
It can be used in a casual scene to any business scene. Think it as digitalized form of business card.

# Libraries

* Materialize
* django-sass
* jquery
* emergence.min.js
  ```
    python manage.py sass Macy/static/Macy/scss/ Macy/static/Macy/css/ --watch 
  ```
* django-cleanup 5.1.0
* factory_boy
* coverage
* pillow
* qrcode-6.1
* ...

# Usage
1. Tap the card
2. Edit your info
3. Be creative with your personalized business card

# Available Custom Commands
* create non activated users 
```
python manage.py create_users <number of users>
```

* create dummy links for specified user
```
python manage.py create_users <user_id> <number of links>
```

# Note


# Author

* Takumi & Kaisei
* takumiminohara.site

# License

"Macy" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

"Macy" is Confidential.
