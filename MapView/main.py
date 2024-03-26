import asyncio
from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from screeninfo import get_monitors
from kivy.core.window import Window
from kivy.clock import Clock
from datasource import Datasource


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        # додати необхідні змінні
        self.datasource = Datasource(user_id=1)
        self.car_marker = None
        self.mapview = None
        self.start = True

    def on_start(self):
        """
        Встановлює необхідні маркери, викликає функцію для оновлення мапи
        """
        Clock.schedule_interval(self.update, 5)

    def update(self, *args):
        """
        Викликається регулярно для оновлення мапи
        """
        points = self.datasource.get_new_points()
        if self.start:
            try:
                self.set_start_marker(points[0])
                self.start = False
            except IndexError:
                pass
        try:
            bump = max(points, key=lambda x: x[2])
            pothole = min(points, key=lambda x: x[2])
            for point in points:
                self.set_track_way_marker(point)
                if point == bump:
                    self.set_bump_marker(point)
                elif point == pothole:
                    self.set_pothole_marker(point)
            self.update_car_marker(points[-1])
        except ValueError:
            pass

    def update_car_marker(self, point):
        """
        Оновлює відображення маркера машини на мапі
        :param point: GPS координати
        """
        try:
            self.mapview.remove_marker(self.car_marker)
        except AttributeError:
            pass
        self.car_marker = MapMarker(lat=point[0], lon=point[1], source="images/car.png")
        self.mapview.add_marker(self.car_marker)

    def set_pothole_marker(self, point):
        """
        Встановлює маркер для ями
        :param point: GPS координати
        """
        pothole_marker = MapMarker(lat=point[0], lon=point[1], source="images/pothole.png")
        self.mapview.add_marker(pothole_marker)

    def set_bump_marker(self, point):
        """
        Встановлює маркер для лежачого поліціянта
        :param point: GPS координати
        """
        pothole_marker = MapMarker(lat=point[0], lon=point[1], source="images/bump.png")
        self.mapview.add_marker(pothole_marker)

    def set_start_marker(self, point):
        """
        Встановлює маркер для початку
        :param point: GPS координати
        """
        start_marker = MapMarker(lat=point[0], lon=point[1], source="images/start.png")
        self.mapview.add_marker(start_marker)

    def set_track_way_marker(self, point):
        """
        Встановлює маркер для пройденного шляху
        :param point: GPS координати
        """
        track_way_marker = MapMarker(lat=point[0], lon=point[1], source="images/track_way.png")
        self.mapview.add_marker(track_way_marker)

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: мапу
        """
        self.mapview = MapView(lat=50.450173, lon=30.520089, zoom=16)
        monitor = get_monitors()[0]
        Window.size = (monitor.width, monitor.height)
        return self.mapview


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
