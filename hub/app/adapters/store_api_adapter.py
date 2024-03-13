import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        print("Hub: sending processed data")

        try:
            # Prepare the data to be sent
            url = f"{self.api_base_url}/processed_agent_data/"
            headers = {'Content-Type': 'application/json'}
            # Make a POST request to the Store API endpoint with the processed data
            data = f"[{','.join([i.model_dump_json() for i in processed_agent_data_batch])}]"
            response = requests.post(url, data=data, headers=headers)

            # Check if the request was successful
            if 200 <= response.status_code < 300:
                logging.info("Data successfully saved.")
                return True
            else:
                logging.error("Failed to save data.")
                return False

        except requests.exceptions.RequestException as e:
            logging.exception(f"An error occurred: {e}")
            return False

