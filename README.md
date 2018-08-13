# Long Code Test for GoGoVan - *Finished extension 1* 

[Requirements](https://github.com/gilbertwat/Back-End-Developer-Interview-Questions/blob/master/long-code-test.md)

Visit petslocal-pro.herokuapp.com to see it in action although **it is advised to run it locally** as the app on heroku does not work properly due to unknown reasons.

### local installation instructions

1. git clone this repo and install Postgresql if you havent already.
2. pip install dependencies from requirements.txt
3. change the SQLALCHEMY_DATABASE_URI in config.py to your own credentials/settings according to this schema:
    ```
    postgresql+psycopg2://username:password@host:port/database
    ```
4. run the following commands in the repository:
    ```
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```
5. finally run the app using
    ```
    python manage.py runserver
    ```
6. Use Chrome with plugin/extension: "Allow-Control-Allow-Origin: *" by vitvad ([Get plugin](https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi)) in case of CORS errors 

### Perform API calls

GET /pets/{id} Fetches the pet by ID

GET /pets/{id}/matches Gets an array of "matching" customers for the given pet

GET /customers/{id} Fetches the customer by ID

GET /customers/{id}/matches Gets an array of "matching" Pets for the given customer

POST /customers/{id}/adopt?pet_id={pet_id} The Customer adopts the given Pet The Pet and Customer no longer appear in /matches queries

### Visit /subscribe
To subscribe as a customer and receive latest pets matching chosen customer's preference

