# AutoFlair

AutoFlair is a Python script that automates the process of setting room temperatures based on an Airbnb calendar. 
It uses the Flair API to update room temperatures based on occupancy.

## Script Description

The `AutoFlair.py` script performs the following tasks:
1. Fetches an iCal file from a specified URL.
2. Checks if the current date is occupied based on events in the iCal file.
3. Uses the Flair API to set room temperatures based on occupancy.

## GitHub Actions Workflow

The GitHub Actions workflow defined in `.github/workflows/daily-job.yml` runs the `AutoFlair.py` script daily at 
18:00 UTC. It performs the following steps:

1. Checks out the repository.
2. Sets up Python and Conda.
3. Installs dependencies from `environment.yml`.
4. Exports `requirements.txt` from the Conda environment.
5. Caches pip dependencies.
6. Installs dependencies from `requirements.txt`.
7. Runs the `AutoFlair.py` script.

## Setup for Development

To set up the project for local development, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/AutoFlair.git
    cd AutoFlair
    ```

2. **Set up the development container:**
    - Open the project in Visual Studio Code.
    - Install the Remote - Containers extension.
    - Reopen the project in the container.

3. **Create the Conda environment:**
    The environment will be created automatically when the container is built, as specified in [devcontainer.json](http://_vscodecontentref_/4).

4. **Set environment variables:**
    - Create a [.env](http://_vscodecontentref_/5) file in the project root with the following content:
    ```env
    FLAIR_CLIENT_ID=your_flair_client_id
    FLAIR_CLIENT_SECRET=your_flair_client_secret
    ICAL_URL=your_ical_url
    AWAY_TEMP_C=10
    OCCUPIED_TEMP_C=18.34
    ```

## Usage

To use the script, follow these steps:

1. **Fork the repository:**
    - Go to the GitHub page of the repository.
    - Click the "Fork" button to create a copy of the repository in your GitHub account.

2. **Update GitHub Secrets:**
    - Go to the "Settings" tab of your forked repository.
    - Click on "Secrets" in the left sidebar.
    - Add the following secrets:
        - `FLAIR_CLIENT_ID`
        - `FLAIR_CLIENT_SECRET`
        - `ICAL_URL`
        - `AWAY_TEMP_C` (optional, default is 10)
        - `OCCUPIED_TEMP_C` (optional, default is 18.34)

3. **Run the script using GitHub Actions:**
    - The script will run automatically based on the schedule defined in [daily-job.yml](http://_vscodecontentref_/6).
    - You can also trigger the workflow manually from the "Actions" tab in your GitHub repository.

## License

This project is licensed under the MIT License.