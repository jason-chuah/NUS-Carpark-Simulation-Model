# Backend Directory Description
This directory contains 2 sub-directories: 
* code  
    This folder contains code for data cleaning and data visualisation, `model.py`, `Dockerfile`, `docker-compose.yml` and `requirements.txt`. 
* graph  
    The graphs generated in data visualisation are stored here. This directory consists of short duration graphs, duration and occupancy distribution, over months and with respect to days of week.
# Simulation Workflow
1. Receive parameters from frontend interface to backend model
   * Basic Parameters
     * `st.session_state.selected_carpark`
     * `st.session_state.total_lots`
     * `st.session_state.red_lot`
     * `st.session_state.white_lots`
     * `st.session_state.start_datetime`
     * `st.session_state.end_datetime`
     * `st.session_state.carpark_to_view`
   * Optional parameters (for event planning):
     * `st.session_state.event_start_datetime`
     * `st.session_state.event_end_datetime`
     * `st.session_state.expected_cars`
     * `st.session_state.event_carpark`
2. Based on different states given, the model will focus on `st.session_state.carpark_to_view` and return the following outputs to the interface.
3. **State 1 Carpark Closure**
   Simulate and output the red and white lots occupancy for every hour with the date range (or given time range).
4. **State 2 Event Planning**:
   Simulate and output the red and white lots occupancy for every hour with the date range (or given time range).
     * Show the clients which carpark will driver be redirected to if the selected carpark is full.
5. Remark:
   * `st.session_state.selected_carpark`, `st.session_state.carpark_to_view`, `st.session_state.event_carpark` and the redirected carpark are all limited to be one of the 6 carparks.
