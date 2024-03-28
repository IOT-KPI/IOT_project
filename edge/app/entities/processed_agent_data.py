from pydantic import BaseModel
from app.entities.agent_data import AgentData, TrafficData


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData
    traffic_data: TrafficData
