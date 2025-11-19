# NuActionGUI: Event Platform Web Application

In this `README.md` file, we focus specifically on the Event Platform Web Application implemented using NuActionGUI (hereinafter, `EventPlatformNAG`).

## NuAcionGUI Container
### Requirements
- [Docker](https://www.docker.com/).
- OCL-py library.

### Usage

1. **Prerequisites:**

Ensure you have [Docker](https://www.docker.com/) installed.

The OCL-py library is already included in the source folder.

2. **Start the container:**

Open a terminal and run:

```powershell
docker compose up --detach --build
```
This will build the images and run a `seceng-project-nag` Docker container. For subsequent runs, you can omit the `--build` flag to start faster. 

To open the shell to the `seceng-project-nag` container:
```powershell 
docker exec -it seceng-project-nag bash
```

3. **Container organization:**

The container is structured as follows:
* `src`: The source code of NuActionGUI generator. Do not change anything in this directory.
* `resrouces`: NuActionGUI generator resources. Do not change anything in this directory.
* `ocl-py` the `OCL-py` library. Do not change anything in this directory.
* `ocl-reference.pdf`: the OCL reference cheatsheet, with highlighted supported syntax in `OCL-py`. 
* `models\EventPlatformNAG` includes three models:
  * `project.dtm` is the application data model. Do not change anything in this directory.
  * `project.stm` is the `fullAccess` security model. You have to change this model according to the security requirements described in the project description.
  * `project.stm` is an empty privacy model. You have to change this model according to the privacy requirements described in the project description.
* `output\EventPlatformNAG` contains the generated application. You do not have to change anything in this directory.


4. **Run the transformation to regenerate the security and privacy enforcement:**

To compile and regenerate security and privacy aspects of a project:
```powershell
python3 src/generate.py -p EventPlatformNAG -o output -re
```
Note: if regenerating, you may have to remove the current instance of the database, located in `/output/EventPlatformNAG/instance/`.
  
5. **Run a project:**

Go to the corresponding `/output/EventPlatformNAG` directory and run:
```powershell
flask --app app.py --debug run --host=0.0.0.0
```
The app should be reachable from your local machine at `localhost:5000`.