from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy.utils import platform as kivy_platform
import datetime


class RootWidget(BoxLayout):
    counter = NumericProperty(0)
    label_text = StringProperty("Hello, Kivy!")


class SimpleKivyApp(App):
    def build(self):
        self.root = RootWidget()
        return self.root

    def on_button_press(self):
        self.root.counter += 1
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.root.label_text = f"Pressed {self.root.counter} times @ {now}"
    def request_permissions(self):
        """Request sensitive permissions on Android when triggered from UI."""
        if kivy_platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                perms = [
                    Permission.CAMERA,
                    Permission.RECORD_AUDIO,
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                ]
                request_permissions(perms, self._permission_callback)
            except Exception as e:
                print('Permission request failed:', e)

    def _permission_callback(self, *args):
        """Handle permission request callback and update UI label.

        The callback signature can vary; common form is (permissions, grants).
        """
        try:
            if len(args) == 2:
                permissions, grants = args
                msgs = []
                for p, g in zip(permissions, grants):
                    status = 'GRANTED' if bool(g) else 'DENIED'
                    msgs.append(f"{p.split('.')[-1]}:{status}")
                self.root.label_text = "Permissions: " + ", ".join(msgs)
            else:
                # Fallback: show raw callback args
                self.root.label_text = f"Permission callback: {args}"
        except Exception as e:
            self.root.label_text = f"Permission callback error: {e}"


if __name__ == '__main__':
    SimpleKivyApp().run()
