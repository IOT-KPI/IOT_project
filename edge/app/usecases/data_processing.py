from app.entities.agent_data import AgentData, TrafficData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentData,
    traffic_data: TrafficData
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        traffic_data:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    if agent_data.accelerometer.y < -8000:
        road_state = "big bumps"
    elif -8000 <= agent_data.accelerometer.y < -2000:
        road_state = "dribble"
    elif -2000 <= agent_data.accelerometer.y < 2000:
        road_state = "smooth road"
    elif 2000 <= agent_data.accelerometer.y < 8000:
        road_state = "small bumps"
    else:
        road_state = "humps"

    return ProcessedAgentData(road_state=road_state,
                              agent_data=agent_data, traffic_data=traffic_data)
