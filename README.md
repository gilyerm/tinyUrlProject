# TinyUrl Project

This is a Django project that provides a URL shortening service. It includes the following features:

- Create a short URL from a long URL
- Redirect from a short URL to the original long URL
- Count the number of hits for each short URL

## Installation

1. Clone the repository
2. Navigate to the project directory: `cd tinyUrlProject`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the database migrations: `python manage.py migrate`

## Running the Project

To run the project, use the following command:
`python manage.py runserver`

Then, navigate to `http://localhost:8000` in your web browser.

## Endpoints

- `POST /create`: Create a short URL. The request body should be a JSON object with a `url` key containing the long URL.
- `GET /s/<short_url>`: Redirect to the original long URL associated with the given short URL.
- `GET /*`: All other routes will return a 404 error.

## Usage

Here's an example of how to create a short URL using the `/create` endpoint:

```bash
$ curl -X POST "http://localhost:8000/create" \
-H "Content-Type: application/json" \
-d '{"url": "https://google.com"}'
```

A response similar to {'short_url': 'slKj289'} will be returned. This `short_url` can be used to redirect to the original long URL. </br>
For instance, you can enter the following URL into your web browser:
`http://localhost:8000/s/slKj289`
to be redirected to the original long URL.

Please note that 'slKj289' is just an example, and the actual short URL returned will vary as it is generated randomly by the application.
## License

This project is licensed under the terms of the MIT license.