from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config
from domain.traffic import Traffic


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
        traffic_filename: str
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.traffic_filename = traffic_filename

    def read(self, accelerometer_data, gps_data, parking_data, traffic_data) -> (AggregatedData, Parking, Traffic):
        """Метод повертає дані отримані з датчиків"""
        x, y, z = map(int, next(accelerometer_data))
        longitude, latitude = map(float, next(gps_data))
        empty_count = int(next(parking_data)[0])
        vehicle_count = int(next(traffic_data)[0])
        return AggregatedData(
            Accelerometer(x, y, z),
            Gps(longitude, latitude),
            datetime.now(),
            config.USER_ID
        ), Parking(
            empty_count,
            Gps(longitude, latitude)
        ), Traffic(
            vehicle_count
        )

    def startReading(self):
        """Метод повинен викликатись перед початком читання даних"""
        accelerometer_file = open(self.accelerometer_filename, "r")
        gps_file = open(self.gps_filename, "r")
        parking_file = open(self.parking_filename, "r")
        traffic_file = open(self.traffic_filename, "r")
        next(accelerometer_file)
        next(gps_file)
        next(parking_file)
        next(traffic_file)
        accelerometer_data, gps_data, parking_data, traffic_data = reader(accelerometer_file), reader(gps_file), reader(parking_file), reader(traffic_file)
        return accelerometer_data, gps_data, parking_data, traffic_data, accelerometer_file, gps_file, parking_file, traffic_file

    def stopReading(self, *args):
        """Метод повинен викликатись для закінчення читання даних"""
        for file in args:
            file.close()
