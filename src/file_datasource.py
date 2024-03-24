import csv
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
from domain.accelerometer import Accelerometer
from domain.gps import Gps


class CircularIterator:
    def __init__(self, lst):
        self.lst = lst
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.lst[self.index]
        self.index = (self.index + 1) % len(self.lst)
        return result
class FileDatasource:
    def __init__(self,a,b,c) -> None:
        self.gps_iter = None
        self.accelerometer_iter = None
        self.parking_iter = None

    def readAggregatedData(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        return AggregatedData(
            Accelerometer(*next(self.accelerometer_iter)),
            Gps(*next(self.gps_iter)),
            datetime.now(),
        )

    def readParking(self) -> Parking:
        data = next(self.parking_iter)
        return Parking(
            data[0], #empty_count
            Gps(*data[1:]),
        )


    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.gps_iter = CircularIterator(read_gps())
        self.accelerometer_iter = CircularIterator(read_accelerometer())
        self.parking_iter = CircularIterator(read_parking())

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        pass

def read_gps(file_name = "data/gps.csv"):
    """ читає координати з gps.csv
    :param file_name: gps.csv
    :return: [(50.450386085935094, 30.524547100067142),...]
    """
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        coordinates = [(float(lat), float(lon)) for lat, lon in reader]
    return coordinates

def read_accelerometer(file_name = "data/accelerometer.csv"):
    """ читає координати з accelerometer.csv
    :param file_name: accelerometer.csv
    :return: [(-17, 4, 16516),...]
    """
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        accelerometer_data = [(int(x), int(y), int(z)) for x, y, z in reader]
    return accelerometer_data

def read_parking(file_name = "data/parking.csv"):
    """ читає координати з accelerometer.csv
    :param file_name: parking.csv
    :return: [(39, 50.451757508676074, 30.522413170763514),...]
    """
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        data = [(int(empty_count), float(lat), float(lon)) for empty_count, lat, lon in reader]
    return data

