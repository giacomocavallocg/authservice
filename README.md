# Cooking Blog Auth Service

This toy project implements an authentication microservice for a cooking blog website. The project is written in Python 3.11 and uses Flask as the web application framework.

## Project structure

```
├── app/
│ ├── db/               # db folder for sqllite development database
│ ├── main/             # main folter containing the flask web app
│ ├── test/             # Unit tests using PyUnit
│ ├── requirements.txt
│ ├── Dockerfile
│ ├── entrypoint.sh       # entry point script for Docker
│ ├── wsgi.py             # WSGI configuration
│ ├── Cooking Env.postman_environment.json  # Postman environment
│ ├── Cooking Registration.postman_collection.json # Postman collection

```

## Implementation

This project implements a REST API with registration and authentication services.

### Registation

Registration is performed using the `POST /auth/registration` endpoint. It accepts the following body:

```json
{
  "email": "paolo.rossi@tim.it",
  "password": "super.S4cure.Passw0rd",
  "name": "paolo",
  "surname": "rossi",
  "age:": 33,
  "use2fa": false
}
```

Where `password` must contain at least one uppercase letter, one lowercase letter, a number, a symbol, and be at least 8 characters long. `use2fa` indicates whether the user wants to enable two-factor authentication.

The API response does not have a body.

### Login

Login is performed with the `POST /auth/login` endpoint. It accepts the following body:

```json
{
  "email": "paolo.rossi@tim.it",
  "password": "super.S4cure.Passw0rd"
}
```

If two-factor authentication is not enabled and the credentials are correct, the API response contains the following body:

```json
{
  "token": "JWT-TOKEN"
}
```

Else, if two-factor authentication is enabled, the response is the following:

```json
{
  "request_id": "3c9bc1e5-d22e-4590-bc54-ff415255367b",
  "validation_endpoint": "127.0.0.1:8080/auth/2fa"
}
```

Where `request_id` is a unique identifier that represents the two-factor authentication request, and `validation_endpoint` is the endpoint to call for the second authentication. The user also receives an email containing an `otp` (for simplicity, in this application, the OTP is printed to the console).

### Two Factor Autentication

The two-factor authentication is performed with the `POST /auth/2fa` endpoint. It accepts the following body:

```json
{
  "request_id": "3c9bc1e5-d22e-4590-bc54-ff415255367b",
  "otp": "8DZ0CD"
}
```

Where `request_id` is the one received in the first step of authentication, and the `otp` is sent via email. If the credentials are correct, the system returns a valid JWT token:

```json
{
  "token": "JWT-TOKEN"
}
```

### User API

To check if the token is valid and has not expired, two endpoints can be used:

- `GET /users`: returns information about all users
- `POST /users/me`: returns information about the current user

Note that the token duration is 1 hour.

### Error handling

The error response has the following structure:

```json
{
  "code": "001",
  "message": "unauthorize operation"
}
```

where `code` is a unique error code and `message` is a brief description of the error.

### How to local run

```bash
cd app/
flask --app main.app:create_app run
```

It deploys a web server on localhost that listens on port 5000.

## Test

Pytest unit tests are provided in the `test` folder.

Tasks can be executed with:

```bash
cd app/
pytest
```

## How to run with Docker

A Dockerfile is provided to build and distribute an image. The Docker entrypoint allows you to run a development environment, production, or execute the unit tests.

The entrypoint of the Dockerfile is the `entrypoint.sh` script, which takes one positional argument that can be:

- `test` to run unit tests
- `dev` to run the service in development mode with an SQLite file as the database
- `prod` to run the service in production mode

### Build image

To build an image named `cookingauthservice`, run the following command:

```bash
 docker build -t cookingauthservice .
```

### Run test

To run tests inside the Docker container, use the following command:

```bash
docker run --rm cookingauthservice test
```

### Run development server

To run the development server, use the following command:

```bash
docker run --rm -it -p 8080:8080 cookingauthservice dev
```

To reuse the development database across different container executions, you can set a named volume for the `app/db` folder.

```bash
docker run --rm -it -v appdb:/app/db -p 8080:8080 cookingauthservice dev
```

### Run production server

To run the container in production, two environment variables must be set:

- JWT_SECRET_KEY: the jwt secret key
- SQL_DATABASE_URI: the db uri

The following command runs the service using a different SQLite file database:

```bash
docker run --rm -it -p 8080:8080 -e JWT_SECRET_KEY=ksachldchbksdlcj -e SQL_DATABASE_URI=sqlite:////app/db/cookingauthdb_prod.db cookingauthservice prod
```

## Tests with Postman

To test the web API, you can use [Postman](https://www.postman.com/downloads/).

The `app` folder contains a Postman collection (`Cooking Registration.postman_collection.json`) and an environment file (`Cooking Env.postman_environment.json`) that can be [loaded](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/) into the Postman application to test the web API.
