# NUS Carpark Simulation Model
## Description
Welcome to our project! We are a group of students from National University of Singapore (NUS). 

NUS operates a variety of car parks, including those designated for season pass holders and visitors. The primary objective of this project is to develop a user-friendly interface that facilitates and allows the planning of car park closures, the re-routing of vehicles, and the reassignment of season and visitor lots. This initiative addresses the need for efficient management of car park resources to enhance the overall campus experience.

## Key Project Goals
1. Data Cleaning and Understanding: The project begins with a meticulous data cleaning process, ensuring the accuracy and reliability of the collected data. This stage serves as a foundation for the subsequent analysis.

2. Arrival Rate Analysis: The project seeks to gain in-depth insights into the arrival rates of season pass holders and visitors at NUS car parks throughout the year. 

3. Discrete-Event Simulation Modeling: Leveraging the collected data, the project aims to develop a discrete-event simulation model. This model will be instrumental in evaluating various planning scenarios, simulating parking activities, and assessing their impact on the overall infrastructure.

4. Interface Development: Developing a web-based interface that facilitates and allows for planning of various scenarios.

## Getting Started
To get started with the NUS Carpark Simulation Model project, you will need to ensure that you have the required prerequisites installed. This section will guide you through.

### Prerequisites 
1. **Python**: The project is written in python, so you need to have Python installed. You can install Python [here](https://www.python.org/downloads/).
2. **Pip**: pip is a package manager for Python and is usually included with Python installations. You can install pip [here](https://pip.pypa.io/en/stable/installation/).
3. **Git**: We recommend having Git installed for version control and easy project management. You can install Git [here](https://git-scm.com/downloads).
4. **Docker**: This project utilizes Docker for containerization. Ensure you have Docker installed to run the application in a containerized environment. To install Docker, follow the official Docker installation guide [here](https://docs.docker.com/get-docker/).


## How to Run

Follow these steps to run the application:

1. **Clone the Git Repository:**
   ```sh
   git clone https://github.com/tanszejing/dsa3101-2310-15-carpark.git
   cd dsa3101-2310-15-carpark
   ```
2. **Make sure you are in the root of the cloned local repository and run Docker Compose:**
   ```sh
   docker compose up
   ```
3. **Open your web browser and navigate to http://localhost:8501 to view the running application.**


## Running the application locally without Docker

To run our application locally without using Docker, follow these steps:

1. **Clone the Git Repository:**
   ```sh
   git clone https://github.com/tanszejing/dsa3101-2310-15-carpark.git 
   cd dsa3101-2310-15-carpark
   ```
2. **Install the dependencies required.**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Backend Flask App:**
   ```sh
   cd back
   python flask1.py
   ```
4. **Update frontend.py configuration:**
   ```sh
   cd ../front
   ```
   In the 'front' folder, open the `frontend.py` file. Change line 221 from: `requests.post('http://flask-app:5000/simulate', json=data)` to : `requests.post('http://127.0.0.1:5000/simulate', json=data)`. This ensures that the Streamlit app connects to the locally running Flask app which is running at http://127.0.0.1:5000 

5. **Run the Streamlit App:**
   ```sh
   streamlit run frontend.py
   ```
   The front-end interface should now be accessible at the Streamlit default address, usually http://localhost:8501







