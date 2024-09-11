import gi
gi.require_version('Gdk', '4.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gdk, GObject, Gtk


class MainWindow(Gtk.ApplicationWindow):
    """This is the main window for our example app."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window settings.
        self.set_default_size(500, 500)
        self.set_title('Drag & Drop')

        # Main box.
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin_top=20)
        self.set_child(self.box)

        # Draggable widgets.
        self.box.append(DragSource(label='Item 1'))
        self.box.append(DragSource(label='Item 2'))
        self.box.append(DragSource(label='Item 3'))

        # Drop space.
        self.box.append(DropTarget(label='Drop something on me!'))


class DragSource(Gtk.Label):
    """This is the widget that we want to drag (can be anything: Label, Button, Image...)."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Drag controller (for now, you don't need to change this).
        drag_controller = Gtk.DragSource()
        drag_controller.connect('prepare', self.on_drag_prepare)
        drag_controller.connect('drag-begin', self.on_drag_begin)
        self.add_controller(drag_controller)

    def on_drag_prepare(self, _ctrl, _x, _y):
        """
        Carry the widget's information while dragging.
        Note: I don't think the string variable is really important, but
              it can be displayed if you drop your widget in a text editor.
        """
        item = Gdk.ContentProvider.new_for_value(self)
        string = Gdk.ContentProvider.new_for_value('You can choose any name for your widget.')
        return Gdk.ContentProvider.new_union([item, string])

    def on_drag_begin(self, ctrl, _drag):
        """Show the widget's icon while dragging."""
        icon = Gtk.WidgetPaintable.new(self)
        ctrl.set_icon(icon, 0, 0)


class DropTarget(Gtk.Label):
    """This is the place where we drop our widgets, (can be anything: Label, Grid, Box...)."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Label properties.
        self.set_size_request(250, 290)

        # Drop controller (just change 'set_gtypes' for now).
        drop_controller = Gtk.DropTarget.new(type=GObject.TYPE_NONE, actions=Gdk.DragAction.COPY)
        drop_controller.set_gtypes([DragSource])    # Enter a list of the draggable classes.
        drop_controller.connect('drop', self.on_drop)
        self.add_controller(drop_controller)

    def on_drop(self, _ctrl, widget, _x, _y):
        """
        What happens when you drop your widget? do whatever you want here.
        Note: This is a simple example, for a complicated work, you may need to
              link 'DropTarget' class with the 'MainWindow' class (e.g: pass the
              'MainWindow' as a parameter for 'DropTarget').
        """
        new_label = widget.get_label()
        self.set_label(new_label)


def on_activate(app):
    win = MainWindow(application=app)
    win.present()


app = Gtk.Application(application_id='com.example.App')
app.connect('activate', on_activate)
app.run(None)
