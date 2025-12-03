# README

This is a dockerized version of the Flask framework. 

## Running the project

To run a server with a Flask application for the first time, make sure you have docker installed and type:

`docker compose up`

If you visit http://localhost:5000 you can see your application running.

Once the images have been built you can start and stop the containers using:

`docker compose up`

and

`docker compose down`

The `project.py` contains the naive functional implementation: there are no security and privacy enforcement.

Your task is to implement the security and privacy model in `project.py` according to the provided project description. 

For privacy requirements, please have a look at the `PRIVACY_INPUT` dictionary object in `project.py`.

## More information
Refer to the Flask tutorials for more information.

## Testing the project
To be announced