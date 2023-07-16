
# SNA_task

Test task that involves implementing a simple RESTful API using FastAPI for a social networking application.

## Installation and Setup

### Redis

To install Redis, follow the official [installation guide](https://redis.io/download) according to your operating system.

Once installed, you can start Redis by running the following command in your terminal:

-   On Unix systems (Linux/macOS):

```bash
redis-server
```

-   On Windows, navigate to your Redis installation directory and run:

```
redis-server.exe
```

To check if Redis is working correctly, you can use the Redis command-line interface `redis-cli` to send a PING command. If Redis is running, it will return PONG:

```bash
redis-cli ping
```

This should return:

`PONG` 

If you see `PONG` as the response, this means Redis is running successfully on your system.

Remember that you need to have the Redis server running in the background while you're running your FastAPI application.

### Python Dependencies

Python dependencies for the project can be installed by running:

```bash
pip install -r requirements.txt
```
    
### Running the Project

You can start the application by running:

```bash
uvicorn main:app --reload
```

## API Documentation

After starting the project, you can access the API documentation by navigating to [http://localhost:8000/docs/](http://localhost:8000/docs/) in your web browser.

Alternatively, you can use the Postman collection [template](https://www.postman.com/spacecraft-participant-12459094/workspace/sna-public/collection/24461590-2ab93b8b-9023-4a1f-a836-af138563fca5?action=share&creator=24461590) for API request examples.

To use your own Postman environment, you need to fork the collection. Right-click on the collection and select Create a Fork, or use the keyboard shortcut Ctrl + Alt + F. Name your fork and choose your workspace, then click the Fork button. This allows you to change the Bearer token according to your needs without affecting the original collection.

Once you've created an account, don't forget to add your token in the Postman collection settings under the `Post and auth` section, `Authorization` tab, `Type`: `Bearer Token`.

## Instructions for testing Redis likes caching

In this application, the Redis database is used for caching likes of posts. You can directly interact with the Redis database through the Redis command-line interface (CLI) to inspect the data in Redis:

-   Start the Redis CLI by running the `redis-cli` command in your terminal.
    
-   To view all keys in the Redis cache, use the `keys *` command. This should display a list of all keys currently stored in your Redis instance.
    
-   To retrieve a specific like, you can use the `HGET` command with the corresponding key and field. For example, if you have a post with ID 1 and a user with ID 1, you can retrieve the like using the command `HGET post:1:likes user:1`.
    
- Once you're in the Redis CLI, you can use the `HGETALL` command with the corresponding key to retrieve all likes from a specific post. For example, to retrieve all likes from a post with ID 1, you can use the command `HGETALL post:1:likes`.
    
## Clearbit

To test the Clearbit functionality, you can use `alex@clearbit.com` during registration (the result will be output to the console). This email address is also embedded in the Postman collection for testing. After signing in, you can access the route `http://localhost:8000/api/clearbit` and send a GET request. The console will output the data related to the currently active user.

If this repository is outdated and my API key is no longer functional, you can replace it in the file `app/clearbit.py`.

## Email Hunter

Email Hunter prevents the registration of "non-existent" emails, although it also blocked the registration of many of my existing emails. Therefore, a workaround has been added, allowing emails to contain the words "clearbit" and "example" for easier testing.

If the 50 verifications per month limit is reached, you can change the API key in `app/emailhunter.py`.

## Technologies Used

This application leverages several technologies and Python libraries for its functionality:

 - [FastAPI](https://fastapi.tiangolo.com/)
 - [Python-JOSE](https://github.com/mpdavis/python-jose)
 - [Passlib](https://passlib.readthedocs.io/en/stable/)
 - [Redis](https://redis.io/)
 -  [Requests](https://docs.python-requests.org/en/latest/)

## Project Structure

-   `main.py`: Contains the primary routes, creates an application instance, and sets up the Redis connection.
-   `app/clearbit.py`: Implements the Clearbit API integration.
-   `app/crud.py`: Defines the core database and Redis queries.
-   `app/database.py`: Configures the database connection.
-   `app/dependencies.py`: Defines dependencies, retrieves the current user instance.
-   `app/emailhunter.py`: Implements the Email Hunter integration.
-   `app/exceptions.py`: Handles exceptions and user behavior scenarios.
-   `app/models.py`: Defines the database models.
-   `app/schemas.py`: Defines the FastAPI schemas.
-   `app/security.py`: Handles password encryption and verification.
-   `app/routers/auth.py`: Contains the routes for user registration, authentication, and Clearbit email verification.
-   `app/routers/likes.py`: Contains the routes for adding and removing post likes.
-   `app/routers/posts.py`: Contains the routes for adding, viewing, updating, and deleting posts.