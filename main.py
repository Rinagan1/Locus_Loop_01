from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.clock import Clock
from plyer import gps

KV = '''
BoxLayout:
    orientation: "vertical"
    MapView:
        id: map_view
        lat: 55.751244
        lon: 37.618423
        zoom: 10
'''

class GPSLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start_gps)

    def start_gps(self, *args):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except NotImplementedError:
            print("GPS не поддерживается на этом устройстве")

    def on_location(self, **kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']
        print(f"Текущее местоположение: широта={lat}, долгота={lon}")
        self.add_marker(lat, lon)

    def add_marker(self, lat, lon):
        # Добавляем маркер на карту и центрируем карту на текущем местоположении
        marker = MapMarker(lat=lat, lon=lon)
        self.ids.map_view.add_widget(marker)
        self.ids.map_view.center_on(lat, lon)

class GPSApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    GPSApp().run()
