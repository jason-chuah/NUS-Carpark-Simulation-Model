# Front Folder

This folder contains the frontend code for our Streamlit application.

## Structure

- `carpark_data`: This folder contains the data on carpark locations and lots.

- `graphs`: This folder contains images used in our Streamlit app.

- `Dockerfile`: The Dockerfile for building our Streamlit application as a Docker container.

- `frontend.py`: The final Streamlit application that connects to the backend model.

- `requirements.txt`: Specifies the dependencies that the frontend relies on. Make sure to install these dependencies before running the application.

- `web.py`: A test file that runs the frontend independently using simulated data. It does not connect to the backend and is useful for showcasing the functionality of our app during the testing phase. This app includes all the carparks in NUS.

## Getting Started

To set up the frontend, follow these steps:

1. Install the dependencies specified in `requirements.txt`.

```bash
pip install -r requirements.txt
```

2. To observe the functionality of our frontend, we provide a sample named `web.py` that operates independently from the backend. Execute the following command to run it:

```bash
streamlit run web.py
```

3. To run our actual frontend which connects to the backend, ensure that the Flask backend is already running. Execute the following command to run it:

```bash
streamlit run frontend.py
```
