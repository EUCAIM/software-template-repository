# Software Container Template

This repository provides a reference template for software providers who want to package their applications as Docker containers compatible with the EUCAIM runtime environment.

**For more details check the [EUCAIM Software Packaging Guide v1.4](#)**

The platform requires containers to:

* Run applications as a non-root user.
* Support dynamic UID/GID assignment at runtime.
* Preserve platform security controls implemented in the provided entrypoint.
* Allow application-specific startup commands through Docker `CMD`.
* Read node's data from a infra-specific path
* Write application's output in a infra-specific path


## Repository Structure

```text
software-template-repository/
├── README.md
├── LICENSE
├── docs/
│   └── ...
└── container_name/
    ├── dockerfile
    ├── entrypoint.sh
    └── app/
        └── <application files>
    └── test/ 
        ├── example_dataset/ 
        │   └── <sample input data>
        └── results/
            	└── <expected output files>
```

#### Files

| File                           | Description                                                                                                 |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `README.md`                    | Template documentation and usage instructions.                                                              |
| `LICENSE`                      | License terms and conditions governing the use, distribution, and modification of this project.                                                              |
| `docs/`                        | Optional documentation for your application.                                                                |
| `container_name/dockerfile`    | Reference Dockerfile to build your application image.                                                       |
| `container_name/entrypoint.sh` | Platform-managed startup script. Performs runtime user configuration and launches the application securely. |
| `container_name/app/`          | Place your application source code, binaries, scripts, and assets here.                                     |


## Important Requirements

#### Do Not Modify `entrypoint.sh`

The provided `entrypoint.sh` is responsible for:

* Creating or updating the runtime user.
* Mapping host UID and GID values.
* Fixing file ownership where required.
* Dropping root privileges.
* Launching the application as a non-root user.

The platform relies on this behavior for security and compatibility.

Application providers should not replace or bypass this script.


## How Application Startup Works

The template uses the following pattern:

```dockerfile
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python3", "/app/main.py"]
```

At container startup:

1. `entrypoint.sh` executes first.
2. Runtime UID/GID mappings are applied.
3. A non-root user is configured.
4. The command specified by `CMD` is executed using `gosu`.

Example:

```dockerfile
CMD ["python3", "/app/script.py"]
```

Results in:

```bash
gosu application-user python3 /app/script.py
```


## Creating Your Application Container

### Step 1: Copy Your Application

Place your application files inside:

```text
container_name/app/
```

Example:

```text
container_name/
├── dockerfile
├── entrypoint.sh
└── app/
    ├── server.py
    ├── requirements.txt
    └── models/
└── test/
```

### Step 2: Install Dependencies

Modify the Dockerfile to install your application's dependencies.

Example:

```dockerfile
FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip gosu

COPY entrypoint.sh /app/entrypoint.sh
COPY app/ /app/

RUN chown -R root:root /app && chmod 755 /app/main.py /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python3", "/app/server.py"]
```

### Step 3: Define Your Startup Command

Specify how your application should start using `CMD`.

Examples:

##### Python application
```dockerfile
CMD ["python3", "/app/server.py"]
```
##### Node.js application
```dockerfile
CMD ["node", "/app/index.js"]
```
##### Java application
```dockerfile
CMD ["java", "-jar", "/app/application.jar"]
```
##### Custom executable
```dockerfile
CMD ["/app/bin/my-service"]
```

The platform injects runtime values used by the entrypoint:

| Variable    | Description                                           |
| ----------- | ----------------------------------------------------- |
| `HOST_UID`  | User ID that should own and execute the application.  |
| `HOST_GID`  | Group ID that should own and execute the application. |
| `HOST_USER` | Runtime username created inside the container.        |

These values are managed automatically by the platform and should not be hardcoded.


### Step 4: Building the Docker Image

From the `container_name` directory:

```bash
docker build -t my-application:v1.0 .
```

Verify that the image was created successfully:

```bash
docker images | grep my-application
```

Expected output:

```text
my-application   latest   <IMAGE_ID>   <DATE>   <SIZE>
```

### Step 5: Testing the Image

Each application submission must include a representative test dataset and the corresponding expected results.

```text
test/
├── example_dataset/
│   ├── sample1.dat
│   ├── sample2.dat
│   └── config.json
└── results/
    ├── sample1_output.json
    ├── sample2_output.json
    └── summary.csv
```

The test dataset should:

* Be small enough to execute quickly.
* Exercise the primary functionality of the application.
* Produce deterministic outputs.
* Not contain confidential or proprietary information.


Application providers must demonstrate that the image can execute successfully against the supplied test dataset.

Assume:

* Input data is located in `test/example_dataset`
* Output files are written to `test/output`
* Expected outputs are stored in `test/results`

Create a temporary output directory:

```bash
mkdir -p test/output
```

Run the container:

```bash
docker run --rm \
  -e HOST_UID=$(id -u) \
  -e HOST_GID=$(id -g) \
  -e HOST_USER=$(whoami) \
  -v $(pwd)/test/example_dataset:/data:ro \
  -v $(pwd)/test/output:/sandbox \
  my-application:v1.0    \
  python3 /app/script.py --input /data/input  --output /sandbox/output
```

The application should process the files in:

```text
/data/input
```

and generate outputs in:

```text
/sandbox/output
```

#### Validating Results

Compare the generated output with the expected results:

```bash
diff -r test/output test/results
```

No output indicates that the generated files match the expected results.

Alternatively:

```bash
diff -rq test/output test/results
```

Expected output:

```text
(no differences reported)
```

The platform entrypoint will still execute first and will then launch the specified command as the configured non-root user.

## Support

If your application cannot run correctly within this template, provide the following information when contacting EUCAIM to (support@eucaim)[support_eucaim@example]:

* Dockerfile
* Application startup command (`CMD`)
* Container logs
* Dependency requirements
* Test dataset description
* Expected output description

This information will help validate compatibility with the platform runtime environment.

## Security Guidelines

Applications should:

* Avoid requiring root privileges.
* Store writable data in designated application directories.
* Use relative paths where possible.
* Handle termination signals correctly (`SIGTERM`, `SIGINT`).
* Write logs to stdout/stderr.

Applications should not:

* Modify `/etc/passwd` or `/etc/group`.
* Replace the provided entrypoint.
* Attempt privilege escalation.

