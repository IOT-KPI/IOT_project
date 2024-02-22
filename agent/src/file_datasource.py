from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

    def read(self, accelerometer_data, gps_data, parking_data) -> (AggregatedData, Parking):
        """Метод повертає дані отримані з датчиків"""
        x, y, z = map(int, next(accelerometer_data))
        longitude, latitude = map(float, next(gps_data))
        empty_count = int(next(parking_data)[0])
        return AggregatedData(
            Accelerometer(x, y, z),
            Gps(longitude, latitude),
            datetime.now(),
            config.USER_ID
        ), Parking(
            empty_count,
            Gps(longitude, latitude)
        )

    def startReading(self):
        """Метод повинен викликатись перед початком читання даних"""
        accelerometer_file = open(self.accelerometer_filename, "r")
        gps_file = open(self.gps_filename, "r")
        parking_file = open(self.parking_filename, "r")
        next(accelerometer_file)
        next(gps_file)
        next(parking_file)
        accelerometer_data, gps_data, parking_data = reader(accelerometer_file), reader(gps_file), reader(parking_file)
        return accelerometer_data, gps_data, parking_data, accelerometer_file, gps_file, parking_file

    def stopReading(self, *args):
        """Метод повинен викликатись для закінчення читання даних"""
        for file in args:
            file.close()
