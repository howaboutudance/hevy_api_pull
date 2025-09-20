# Hevy API Puller

A Python-based utility for:

- pulling workout and exercise data from the [Hevy][hevy_app] fitness app API.
- Keeping that data up to date with a webhook subscription and deployment to Google App Engine. (in-progress)

It is designed for personal analysis, backups, or integration into custom dashboards and data platforms.

---

## Features

- 🔑 API authentication with Hevy
- 📥 Retrieve workout, exercise, and set data
- 💾 Export results to JSON/CSV (planned: database storage)
- 🧪 Unit and integration test coverage (in progress)

---

### Requirements

- Python 3.12+
- `pip` for dependencies

### Setup

```bash
git clone https://github.com/howaboutudance/hevy_api_pull.git
cd hevy_api_pull
pip install -r requirements-dev.txt
```

### Environment Setup


This project uses `.env` files and dynaconf to manage setting/configuration.
To setup a new deployment.

There are three different type of configuration files used in this project

| File name | Purpose |
| --------- | ------- |
| `.env`    | Sets the environment name, defining which environment file to use |
| `config/default.yaml` | Sets configuration settings used across environments or defaults in in lieu of a setting|
| environment name file (i.e. `config/dev.yaml`) | Sets non-secret configuration settings for the environment |
| `config/.secrets.yaml` | Sets secrets used by the application, included in `.gitignore` |


1. Create a `.env` file to define the environment the code will run in (default is `DEV`)

    ```env
    ENV=DEV
    ```

2. Create an environment yaml file that matches your environment name (lowercase of the environment name with yaml extension). In this example `dev.yaml`
3. (Optional for live data pulling) Generate a Hevy API Key
4. Add the API key to `.secrets.yaml` and define the endpoint for the Hevy API in your environment file
    - .secrets.yaml

    ```yaml
    hevy_api__key: <insert key here>
    ```

    - dev.yaml

    ```yaml
    hevy_api:
    url: "https://api.hevyapp.com"
    version: "v1"
    ```

5. configure the mongodb credentials in `.secrets.yaml` and your environment yaml (lowercase environment named yaml file in config folder)
    - .secrets.yaml

    ```yaml
    mongodb__password: <insert password here>
    ```

    - dev.yaml

    ```yaml
    # example for local development
    mongodb:
    username: admin
    host: "localhost:27017"
    ```

## Development

### Development Setup + Testing

After cloning the repository and configuring the environment, you should:

- setup a virtualenv and source it
- install the development dependencies with `pip install -r requirements-dev.txt`
- start a development mongodb instance `util/podman/up.sh`
- run the unit test and integration test suites with tox `tox -e py && tox -e intg`

### Contributing

Pull requests welcome! Please:

- Create a feature branch

- Add or update tests (95% coverage is required for a PR to be accepted)

- Run the linter, formatter & test suite before submitting (using tox)

## Project Status

⚠️ Early development — expect breaking changes.

Development plans and status is tracked in a [project tracker][project_tracker], including roadmap, and feature planning.

## License

This project is licensed under the Apache 2.0 License

## Credits & Contributors

Developed by Michael Penhallegon -- @howaboutudance

&copy; 2025 Michael Penhallegon

[hevy_app]: https://www.hevyapp.com/
[project_tracker]: https://docs.google.com/document/d/1r7EXNHtVTbrEwSOk0VvGy-etlDWeVHa9e7u-y2XCzXk/edit?usp=sharing
