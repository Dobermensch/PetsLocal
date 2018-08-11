Long Code Test for GoGoVan

Finished APIS Need to add extentions

Visit petslocal-pro.herokuapp.com to see it in action. Add Pets and Customers on petslocal-pro.herokuapp.com

Perform other API calls

GET /pets/{id} Fetches the pet by ID

GET /pets/{id}/matches Gets an array of "matching" customers for the given pet

GET /customers/{id} Fetches the customer by ID

GET /customers/{id}/matches Gets an array of "matching" Pets for the given customer

POST /customers/{id}/adopt?pet_id={pet_id} The Customer adopts the given Pet The Pet and Customer no longer appear in /matches queries
