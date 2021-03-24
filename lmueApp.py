import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math

LOAD_GRID_SIZE = 10

class App:
    def __init__(self, root):
        # Create a container
        self.main_frame = tkinter.Frame(root)
        self.main_frame.pack()
        self.draw_frame = tkinter.Frame(self.main_frame, relief=tkinter.GROOVE, bd=1, padx=5, pady=5)
        self.ctrl_frame = tkinter.Frame(self.main_frame, relief=tkinter.GROOVE, bd=1, padx=5, pady=5)
        self.load_frame = tkinter.Frame(self.main_frame, relief=tkinter.GROOVE, bd=1, padx=5, pady=5)
        self.object_frame = tkinter.Frame(self.main_frame, relief=tkinter.GROOVE, bd=1, padx=5, pady=5)
        self.track_frame = tkinter.Frame(self.main_frame, relief=tkinter.GROOVE, bd=1, padx=5, pady=5)

        self.draw_frame.pack(side=tkinter.TOP, padx=5, pady=5)
        self.load_frame.pack(side=tkinter.RIGHT, padx=5, pady=5)
        self.ctrl_frame.pack(side=tkinter.TOP, padx=5, pady=5)
        self.track_frame.pack(side=tkinter.TOP, padx=5, pady=5)
        self.object_frame.pack(side=tkinter.TOP, padx=5, pady=5)

        self.load_coo = {'x': [], 'y': []}
        # DRAW FRAME
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.line = []
        self.canvas = FigureCanvasTkAgg(self.fig, self.draw_frame)
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        # TRACK FRAME
        tkinter.Label(self.track_frame, text="TRACK", pady=5).pack()
        tkinter.Label(self.track_frame, text="Radius", width=10, anchor='e').pack(side=tkinter.LEFT)
        tkinter.Entry(self.track_frame, width=8).pack(side=tkinter.LEFT)
        tkinter.Label(self.track_frame, text="Überhöhung", width=10, anchor='e').pack(side=tkinter.LEFT)
        self.ue_entry = tkinter.Entry(self.track_frame, width=8)
        self.ue_entry.pack(side=tkinter.LEFT)
        tkinter.Label(self.track_frame, text="ni", width=10, anchor='e').pack(side=tkinter.LEFT)
        tkinter.Entry(self.track_frame, width=8).pack(side=tkinter.LEFT)

        # CONTROL FRAME
        tkinter.Label(self.ctrl_frame, text="CONTROL").pack()
        self.rotate_button = tkinter.Button(self.ctrl_frame, text="Rotate Load", command=self.rotate_load)
        self.rotate_button.pack(side=tkinter.LEFT)

        # OBJECT FRAME
        tkinter.Label(self.object_frame, text="OBJECT").pack()

        # LOAD FRAME
        tkinter.Label(self.load_frame, text="LOAD").pack()

        self.validate_load_entry_wrapper = (self.load_frame.register(self.validate_load_entry),
                                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.loadGrid = [tkinter.Frame(self.load_frame, padx=2, pady=2) for i in range(LOAD_GRID_SIZE)]

        for idx, i in enumerate(self.loadGrid):
            i.pack(side=tkinter.TOP)
            tkinter.Label(i, text="Point {}".format(idx)).pack(side=tkinter.LEFT)
            tkinter.Entry(i, bd=3, width=10, validate='key', validatecommand=self.validate_load_entry_wrapper).pack(side=tkinter.LEFT)
            tkinter.Entry(i, bd=3, width=10).pack(side=tkinter.LEFT)

        tkinter.Button(self.load_frame, text="Redraw", command=self.draw_load, padx=8, pady=8).pack()

        self.draw_load()

    def validate_load_entry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def draw_load(self):
        self.load_coo['x'] = [float(i.winfo_children()[1].get()) for i in self.loadGrid if i.winfo_children()[1].get() != '']
        self.load_coo['y'] = [float(i.winfo_children()[2].get()) for i in self.loadGrid if i.winfo_children()[2].get() != '']
        self.ax.clear()
        self.line, = self.ax.plot(self.load_coo['x'], self.load_coo['y'])
        self.canvas.draw()

    def rotate_load(self):
        phi = math.sin(float(self.ue_entry.get())/1435)
        print(phi)
        rot = [(x*math.cos(phi) - y*math.sin(phi), x*math.sin(phi) + y*math.cos(phi))
               for (x, y) in zip(self.load_coo['x'], self.load_coo['y'])]
        self.load_coo['x'] = [i[0] for i in rot]
        self.load_coo['y'] = [i[1] for i in rot]
        self.ax.clear()
        self.line, = self.ax.plot(self.load_coo['x'], self.load_coo['y'])
        self.canvas.draw()

root = tkinter.Tk()
app = App(root)
root.mainloop()