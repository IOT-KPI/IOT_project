import asyncio

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.mapview import MapMarker, MapView, MapSource
from screeninfo import get_monitors
from math import sqrt

from datasource import Datasource


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        # додати необхідні змінні
        self.datasource = Datasource(user_id=1)
        self.car_marker = None
        self.mapview = None
        self.start = True
        self.button = None
        self.latitude = 0
        self.longitude = 0
        self.constant = 91.4
        self.time = 0
        self.distances = []
        self.info_popup = None

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
        check_list = []
        if len(points) != 5 and self.longitude != 0:
            total_distance = round(sum(self.distances) * self.constant, 3)
            average_speed = round(((sum(self.distances) * self.constant) / (self.time / 3600)), 3)
            self.show_info_popup(total_distance, average_speed)
        else:
            for i in range(len(points) - 1):
                distance = sqrt((points[i + 1][0] - points[i][0]) ** 2 + (points[i + 1][1] - points[i][1]) ** 2)
                self.distances.append(distance)
            self.time += 5
            self.latitude, self.longitude = points[-1][0], points[-1][1]

        if self.start:
            try:
                self.set_start_marker(points[0])
                self.start = False
            except IndexError:
                pass
        try:
            for i in range(len(points)):
                check_list.append(points[i][0])
            check_set = set(check_list)
            if len(check_set) != len(check_list):
                self.set_traffic_light_marker(points[0])
            else:
                bump = max(points, key=lambda x: x[2])
                pothole = min(points, key=lambda x: x[2])
                for point in points:
                    if points[0][3] >= 6 and points[-1][3] >= 6:
                        self.set_track_way_marker(point, "red_dot.png")
                    else:
                        self.set_track_way_marker(point, "track_way.png")
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

    def set_track_way_marker(self, point, image):
        """
        Встановлює маркер для пройденного шляху
        :param image: image
        :param point: GPS координати
        """
        track_way_marker = MapMarker(lat=point[0], lon=point[1], source="images/" + image)
        self.mapview.add_marker(track_way_marker)

    def set_traffic_light_marker(self, point):
        """
        Встановлює маркер для пройденного шляху
        :param point: GPS координати
        """
        traffic_light_marker = MapMarker(lat=point[0], lon=point[1], source="images/traffic_light.png")
        self.mapview.add_marker(traffic_light_marker)

    def change_map_source(self, instance):
        if self.mapview.map_source.url != 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png':
            new_source_url = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        else:
            new_source_url = 'https://{s}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png'
        self.mapview.map_source = MapSource(url=new_source_url)

    def show_info_popup(self, distance, speed):
        """
        Показує Popup з інформацією про відстань та швидкість
        :param distance: відстань
        :param speed: швидкість
        """
        if not self.info_popup:
            self.info_popup = Popup(title='Info', size_hint=(None, None), size=(400, 200))
            content = Label(text=f'Total distance (km): {distance}\nAverage speed (km/h): {speed}')
            self.info_popup.content = content
        self.info_popup.open()

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: мапу
        """
        self.mapview = MapView(lat=50.450173, lon=30.520089, zoom=16)
        monitor = get_monitors()[0]
        Window.size = (monitor.width, monitor.height)

        # Створення кнопки з зображенням
        self.button = ImageButton(source="images/dark_theme.png",
                                  pressed_source="images/dark_theme_press.png",
                                  size_hint=(None, None), allow_stretch=True)
        self.button.bind(on_touch_down=self.on_button_touch)
        self.mapview.add_widget(self.button)
        # self.adjust_button_size(self.mapview.size)
        self.mapview.bind(size=lambda instance, value: self.adjust_button_size(
            value))

        return self.mapview

    def adjust_button_size(self, size):
        """
        Функція для зміни розміру кнопки відповідно до розміру мапи
        :param size: новий розмір мапи
        """
        new_size = min(size) / 18
        self.button.size = (new_size, new_size)

    def on_button_touch(self, instance, touch):
        """
        Обробник події натискання на кнопку
        :param instance: екземпляр кнопки
        :param touch: дотик
        """
        if self.button.collide_point(*touch.pos):
            self.change_map_source(instance)
            self.button.switch_source()


class ImageButton(ButtonBehavior, Image):
    def __init__(self, source='', pressed_source='', **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.pressed_source = pressed_source
        self.sources = [self.source, self.pressed_source]
        self.index = 0

    def switch_source(self):
        """
        Функція для перемикання зображень кнопки
        """
        self.index = (self.index + 1) % len(self.sources)
        self.source = self.sources[self.index]


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
