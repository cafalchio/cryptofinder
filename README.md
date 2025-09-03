[![Lint](https://github.com/cafalchio/cryptofinder/actions/workflows/lint.yaml/badge.svg)](https://github.com/cafalchio/cryptofinder/actions/workflows/lint.yaml)
[![Tests](https://github.com/cafalchio/cryptofinder/actions/workflows/tests.yaml/badge.svg)](https://github.com/cafalchio/cryptofinder/actions/workflows/tests.yaml)

### Hosted at my homeserver

https://www.crypto.cafalchio.com.br


Automated scraper to find newly created crypto

#### Step 1:
* The Initial idea is to create a Database with the maximum ammount of crypto projects already created. ✅ 

#### Step 2
*  Create scrapers and api pipeline to get as many coins as possible to the database. ✅ 
  
#### Step 3
* Run the pipeline daily and check manually the new coins. ✅ 

#### Step 4
* Improve the frontend.

#### Step 5
* Release the production version.
  
Todo:
    - Automate the deployment from dev to prod every 2 days without any time out. ✅ 
    - Improve scrappers to extract more information ✅ 
    - Improve tests and logs 
    - Add automated emails 


### How to run locally

1. clone the git
2. cd /cryptofinder
3. pip install .
If there is no database
4. cd app
5. flask db init
6. flask db migrate
 
 To run scrappers
 cd /backend/scrappers
 python run scrappers

 run the server
 in /cryptofinder
 python run.py


using sqlite local:
inside /app 
    flask db init
    flask db migrate

Running on Gunicorn command:
gunicorn -w 4 'app:gunicorn_app'


### Docker

sudo docker build -t cryptofinder .
sudo docker run -d -p 10000:80 cryptofinder
