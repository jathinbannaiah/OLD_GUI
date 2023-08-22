# Added the drawing features, that reads the cli file and draws a 2d depictions of the model with zoom features
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import os
from READ_CLI import ReadCLI
from CSV_ import CSV_file
from layer_configuration import Layer_config
import tkinter.font as tkFont
from help import hover_data
import threading
from final_Simulator import Animate
from gcode import GCODE

# read_object = ReadCLI()
# csv_obj = CSV_file()
# layer_config_obj = Layer_config()
DEFAULT_FAN_SPEED = 127  # Default Parameter values, the same values will be loaded into the csv files initially
DEFAULT_EXTRUDER_TEMPERATURE = 190  # To change default values, you need to make changes in the CSV_ .py file also
DEFAULT_BED_TEMPERATURE = 90
DEFAULT_SPEED = 100
DEFAULT_POWER = 200
DEFAULT_HEAT_ABSORPTION_EFFICIENCY = 80
DEFAULT_LASER_BEAM_DIAMETER = 0.0875
DEFAULT_RECOATER_TIME = 15
FLAG = "side"


class GUI:
    def __init__(self):
        self.read_object = ReadCLI()
        self.csv_obj = CSV_file()
        self.layer_config_obj = Layer_config()
        self.gcode = GCODE()
        self.window = tk.Tk()
        self.custom_font = tkFont.Font(family="Arial", size=9, weight="bold")
        self.window.title('Layer specific parameter Configuration')
        self.window.geometry('1600x800')
        self.window.resizable(0,
                              0)  # To lock the window size, so the GUI doesn't get jumbled when the size window size changes
        self.cli_file_path = tk.StringVar()
        self.layer_var_start = tk.StringVar()
        self.layer_var_end = tk.StringVar()
        self.temp_view = tk.StringVar()
        self.total_layers = 0
        self.file_path = None
        self.parameters = []
        self.zoom_flag = False
        self.count_layer = 0
        self.flag = "side"
        self.view = "Side"
        self.canvas = tk.Canvas(self.window, width=800, height=800,
                                bg="gray")  # Initialising the canvas window to display the model
        self.canvas.place(x=800, y=0)
        self.zoom_level = 1.0
        self.zoom_factor = 1.2  # Modify the zoom factor to change the rate of the zoom
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<MouseWheel>",lambda event: self.zoom(event))
        self.create_widgets()

    def create_widgets(self):
        path_label = ttk.Label(self.window, text="CLI File Path:", font=self.custom_font)
        path_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        path_label.bind("<Enter>", lambda event: self.show_textbox(0,
                                                                   event))  # To show reference text when mouse key hovers over the labels

        self.path_entry = ttk.Entry(self.window, textvariable=self.cli_file_path, width=50)
        self.path_entry.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        browse_button = ttk.Button(self.window, text="+", command=self.browse_file, width=2)
        browse_button.place(x=510, y=10)

        ok_button = ttk.Button(self.window, text="OK", command=self.check_file_path)
        ok_button.grid(row=0, column=4, padx=10, pady=10)

        view_flip_button = ttk.Button(self.window,text=">^",command=self.top_view_drawing,width=4)
        view_flip_button.place(x=768,y=3)

        layer_start_label = ttk.Label(self.window, text='Layer number, Start_offset:', font=self.custom_font)
        layer_start_label.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        layer_start_label.bind("<Enter>", lambda event: self.show_textbox(1, event))

        layer_start_dropdown = ttk.Combobox(self.window, textvariable=self.layer_var_start, state="normal")
        layer_start_dropdown.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        layer_start_dropdown.bind("<<ComboboxSelected>>", self.on_layer_selected)

        layer_end_label = ttk.Label(self.window, text='Stop_offset:', font=self.custom_font)
        layer_end_label.place(x=400, y=55)
        layer_end_dropdown = ttk.Combobox(self.window, textvariable=self.layer_var_end, state="normal")
        layer_end_dropdown.place(x=480, y=55)

        fan_speed_label = ttk.Label(self.window, text="Fan speed:", font=self.custom_font)
        fan_speed_label.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.fan_speed_entry = ttk.Entry(self.window)
        fan_speed_label.bind("<Enter>", lambda event: self.show_textbox(2, event))

        extruder_temp_label = ttk.Label(self.window, text="Extruder temperature:", font=self.custom_font)
        extruder_temp_label.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        extruder_temp_label.bind("<Enter>", lambda event: self.show_textbox(3, event))
        self.extruder_temp_entry = ttk.Entry(self.window)

        bed_temp_label = ttk.Label(self.window, text="Bed temperature:", font=self.custom_font)
        bed_temp_label.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        bed_temp_label.bind("<Enter>", lambda event: self.show_textbox(4, event))
        self.bed_temp_entry = ttk.Entry(self.window)

        speed_label = ttk.Label(self.window, text="Travel Speed", font=self.custom_font)
        speed_label.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        speed_label.bind("<Enter>", lambda event: self.show_textbox(5, event))
        self.speed_entry = ttk.Entry(self.window)

        power_label = ttk.Label(self.window, text="Laser Power", font=self.custom_font)
        power_label.grid(row=6, column=1, padx=10, pady=10, sticky='w')
        power_label.bind("<Enter>", lambda event: self.show_textbox(6, event))
        self.power_entry = ttk.Entry(self.window)

        heat_absorption_label = ttk.Label(self.window, text="Heat source absorption efficiency", font=self.custom_font)
        heat_absorption_label.grid(row=7, column=1, padx=10, pady=10, sticky='w')
        heat_absorption_label.bind("<Enter>", lambda event: self.show_textbox(7, event))
        self.heat_absorption_entry = ttk.Entry(self.window)

        laser_diameter_label = ttk.Label(self.window, text="Laser beam diameter", font=self.custom_font)
        laser_diameter_label.grid(row=8, column=1, padx=10, pady=10, sticky='w')
        laser_diameter_label.bind("<Enter>", lambda event: self.show_textbox(8, event))
        self.laser_diameter_entry = ttk.Entry(self.window)

        recoater_time_label = ttk.Label(self.window, text="Recoater time", font=self.custom_font)
        recoater_time_label.grid(row=9, column=1, padx=10, pady=10, sticky='w')
        recoater_time_label.bind("<Enter>", lambda event: self.show_textbox(9, event))
        self.recoater_time_entry = ttk.Entry(self.window)

        save_button = ttk.Button(self.window, text="Save", command=self.save_parameters)
        # save_button.grid(row=10, column=1, columnspan=2, padx=10, pady=10)
        save_button.place(x=210,y=407)

        reset_button = ttk.Button(self.window, text="Reset", command=self.reset_window)
        reset_button.place(x=295, y=407)

        simulate_button = ttk.Button(self.window, text="Simulate", command=self.animate)
        simulate_button.place(x=380, y=407)
        zoom_button = ttk.Button(self.window, text='*',command=self.custom_animate,width=4)
        zoom_button.place(x=455,y=407)
        gcode_button = ttk.Button(self.window, text="Generate Gcode", command=lambda: self.gcode.convert_cli_to_gcode(self.file_path,"output_gcode.txt"))
        gcode_button.place(x=495,y=407)

    def check_file_path(self):
        self.file_path = self.cli_file_path.get()
        if os.path.isfile(self.file_path):
            self.read_object.read_cli_file(self.file_path)  # To generate the printer_attributes and printer_movement files
            self.read_object.close_files()
            self.csv_obj.csv_handling()  # To generate the csv file with default parameter values
            self.count_layer = self.csv_obj.num_layers
            layer_start_dropdown = self.window.grid_slaves(row=1, column=2)[0]  # Find the layer dropdown widget
            layer_start_dropdown['values'] = tuple(range(1, self.count_layer + 1))
            print("Number of layers:", self.csv_obj.num_layers)
            self.show_file_properties()
            #self.drawing(self.file_path)
        else:
            messagebox.showerror("File Not Found", "The specified file does not exist.")

    def on_layer_selected(self, *args):
        selected_layer = self.layer_var_start.get()
        if selected_layer:
            layer_end_dropdown = ttk.Combobox(self.window,
                                              textvariable=self.layer_var_end)  # overwriting the initial widget to solve scope issues
            layer_end_dropdown.place(x=480, y=55)
            second_dropdown_start = int(selected_layer)
            layer_end_dropdown['values'] = tuple(range(second_dropdown_start + 1, self.count_layer + 1))
            self.fan_speed_entry.grid(row=2, column=2, padx=5, pady=5,
                                      sticky='w')  # Enabling the parameter grids only after vallid start and stop offsets are entered
            self.extruder_temp_entry.grid(row=3, column=2, padx=5, pady=5, sticky='w')
            self.bed_temp_entry.grid(row=4, column=2, padx=5, pady=5, sticky='w')
            self.speed_entry.grid(row=5, column=2, padx=5, pady=5, sticky='w')
            self.power_entry.grid(row=6, column=2, padx=5, pady=5, sticky='w')
            self.heat_absorption_entry.grid(row=7, column=2, padx=5, pady=5, sticky='w')
            self.laser_diameter_entry.grid(row=8, column=2, padx=5, pady=5, sticky='w')
            self.recoater_time_entry.grid(row=9, column=2, padx=5, pady=5, sticky='w')

        else:
            self.fan_speed_entry.grid_remove()
            self.extruder_temp_entry.grid_remove()
            self.bed_temp_entry.grid_remove()
            self.speed_entry.grid_remove()
            self.power_entry.grid_remove()
            self.heat_absorption_entry.grid_remove()
            self.laser_diameter_entry.grid_remove()
            self.recoater_time_entry.grid_remove()

    def save_parameters(self):
        fan_speed = self.fan_speed_entry.get()
        extruder_temp = self.extruder_temp_entry.get()
        bed_temp = self.bed_temp_entry.get()
        speed = self.speed_entry.get()
        power = self.power_entry.get()
        heat_absorption = self.heat_absorption_entry.get()
        laser_diameter = self.laser_diameter_entry.get()
        recoater_time = self.recoater_time_entry.get()
        start = self.layer_var_start.get()
        end = self.layer_var_end.get()
        if fan_speed == "" and extruder_temp == "" and bed_temp == "" and speed == "" and power == "":
            messagebox.showerror(title="Warning!", message="You have not specified the values for any parameters.")
        if fan_speed == '' or not isinstance(fan_speed,(int,float)):  # Checking if new values are assigned for each parameter and if not then assigning default values
            fan_speed = DEFAULT_FAN_SPEED
        if extruder_temp == '' or not isinstance(extruder_temp,(int,float)):
            extruder_temp = DEFAULT_EXTRUDER_TEMPERATURE
        if bed_temp == '' or not isinstance(bed_temp,(int,float)):
            bed_temp = DEFAULT_BED_TEMPERATURE
        if speed == '' or not isinstance(speed,(int,float)):
            speed = DEFAULT_SPEED
        if power == '' or not isinstance(power,(int,float)):
            power = DEFAULT_POWER
        if heat_absorption == '' or not isinstance(heat_absorption,(int,float)):
            heat_absorption = DEFAULT_HEAT_ABSORPTION_EFFICIENCY
        if laser_diameter == '' or not isinstance(laser_diameter,(int,float)):
            laser_diameter = DEFAULT_LASER_BEAM_DIAMETER
        if recoater_time == '' or not isinstance(recoater_time,(int,float)):
            recoater_time = DEFAULT_RECOATER_TIME
        print(start, end)
        if start == "" or end == "":  # Checking if start or stop offset variables are blanks
            messagebox.showerror(title="Error!", message="Please don't leave the layer number entries blank.")
        else:
            is_ok = messagebox.askokcancel(title="Save?",
                                           message=f"The following configurations were made for the \n Layers {start} to {end} " \
                                                   f"\n Fan Speed: {fan_speed} \n Extruder Temperature: {extruder_temp} \n Bed Temperature: {bed_temp} " \
                                                   f"\n Speed: {speed} \n Power: {power}" \
                                                   f"\n Heat absorption efficiency: {heat_absorption} \n laser beam diameter: {laser_diameter}" \
                                                   f"\n recoater time: {recoater_time}")

            if is_ok:  # If the user confirms to save the data
                start = int(start)
                end = int(end)
                for i in range(start, end + 1):
                    layer_number = i
                    if layer_number and fan_speed and extruder_temp and bed_temp:
                        self.parameters.append(
                            [f"Layer {layer_number}", fan_speed, extruder_temp, bed_temp, speed, power, heat_absorption,
                             laser_diameter, recoater_time])
                    temp_config_values = [f"Layer {layer_number}", fan_speed, extruder_temp, bed_temp, speed, power,
                                          heat_absorption, laser_diameter, recoater_time]
                    self.layer_config_obj.config(temp_config_values)
                    self.clear_entries()

    def clear_entries(self):  # Function to clear the parameter grid entries
        self.layer_var_start.set("")
        self.layer_var_end.set("")
        self.fan_speed_entry.delete(0, tk.END)
        self.extruder_temp_entry.delete(0, tk.END)
        self.bed_temp_entry.delete(0, tk.END)
        self.power_entry.delete(0, tk.END)
        self.speed_entry.delete(0, tk.END)
        self.recoater_time_entry.delete(0, tk.END)
        self.laser_diameter_entry.delete(0, tk.END)
        self.heat_absorption_entry.delete(0, tk.END)

    def reset_window(self):  # Function to clear the whole window
        self.path_entry.delete(0, tk.END)
        self.clear_entries()
        self.canvas.delete("all")
        self.read_object.close_files()
        try:
            self.animation.clear()
        except:
            print("turtle not created")
            pass
        self.window.destroy()
        self.__init__()
    def show_textbox(self, flag, event):  # To display a textbox whenever the mouse hovers over a label
        x_,y_ = self.window.winfo_pointerxy()
        label = event.widget
        textbox = tk.Text(self.window, height=4, width=55, borderwidth=2, relief=tk.SOLID, highlightthickness=1)
        textbox.configure(bg="light gray",fg='blue')
        textbox.insert(tk.END, f"{hover_data[flag]}")
        textbox.place(x=120, y=450)

        def hide_textbox(event):
            textbox.destroy()

        label.bind("<Leave>", hide_textbox)

    def browse_file(self):  # To access the file manager to select the file path
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            self.cli_file_path.set(file_path)

    def drawing(self, path):  # Function to generate the 2d model from the given cli file
        self.canvas.delete("all")
        timeout = 20
        timer = threading.Timer(timeout, self.timeout_handler)
        try:
            with open(path, 'r') as file:
                timer.start()
                for line in file:
                    if line.startswith("$$UNITS"):
                        unit = float(line.split("/")[1])
                        unit = unit * 3
                    if line.startswith("$$LAYER"):
                        z = 800 - float(line.split("/")[
                                            1]) * unit  # Because the origin is at the top left corner, therefore to invert the image

                    if line.startswith("$$POLYLINE") :
                        line_list = line.split(",")
                        start = 3
                        end = int(line_list[2])
                        temp_x = float(line_list[start]) * unit
                        for i in range(start + 2, start + end * 2 - 2, 2):
                            self.canvas.create_line(temp_x, z, float(line_list[i]) * unit, z)
                            temp_x = float(line_list[i]) * unit

                    if line.startswith("$$HATCHES"):                 # worked on hatch logic
                        line_list1 = line.split("/")[1]
                        lenght = len(line_list1)
                        line_list = line.split(",")
                        #print(line_list)
                        start = 2
                        end = len(line_list[2:])

                        temp_x = float(line_list[start]) * unit
                        for i in range(start + 2, start+end*4 -2, 2):
                            self.canvas.create_line(temp_x, z, float(line_list[i]) * unit, z)
                            temp_x = float(line_list[i]) * unit
                            #print(i)

            timer.cancel()
            self.flag = "top"
            # self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # self.canvas.bind("<MouseWheel>",
            #                  lambda event: self.zoom(event))  # Binding the mouse wheel to the zoom function
        except TimeoutError:
            messagebox.showerror(title="Time Out!",
                                 message="The Drawing function has taken too long to respond\n You can continue with the configuration")
            print("Function execution time out")
            return

    def top_view_drawing(self):  # Function to generate the 2d model from the given cli file
        self.canvas.delete("all")
        path = self.file_path
        if self.flag == "side":
            self.drawing(self.file_path)
        else:
            timeout = 20
            timer = threading.Timer(timeout, self.timeout_handler)
            try:
                with open(path, 'r') as file:
                    timer.start()
                    for line in file:
                        if line.startswith("$$UNITS"):
                            unit = float(line.split("/")[1])
                            unit = unit * 3
                        if line.startswith("$$LAYER"):
                            z = 800 - float(line.split("/")[
                                                1]) * unit  # Because the origin is at the top left corner, therefore to invert the image

                        if line.startswith("$$POLYLINE") or line.startswith("$$HATCHES"):
                            line_list = line.split(",")
                            start = 3
                            end = int(line_list[2])
                            temp_x = float(line_list[start]) * unit
                            temp_y = float(line_list[start+1]) * unit
                            for i in range(start + 2, start + end * 2 - 2, 2):
                                self.canvas.create_line(temp_x, temp_y, float(line_list[i]) * unit, float(line_list[i+1]) * unit)
                                temp_x = float(line_list[i]) * unit
                                temp_y = float(line_list[i+1]) * unit

                        if line.startswith("$$HATCHES"):  # worked on hatch logic
                            line_list1 = line.split("/")[1]
                            line_list = line.split(",")
                            # print(line_list)
                            start = 2
                            end = len(line_list[2:])
                            temp_x = float(line_list[start]) * unit
                            temp_y = float(line_list[start+1]) * unit
                            for i in range(start + 2, start + end - 2, 2):
                                self.canvas.create_line(temp_x, temp_y, float(line_list[i]) * unit, float(line_list[i+1]) * unit)
                                temp_x = float(line_list[i]) * unit
                                temp_y = float(line_list[i+1]) * unit
                                # print(i)

                timer.cancel()
                self.flag = "side"
                # self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                # self.canvas.bind("<MouseWheel>",
                #                  lambda event: self.zoom(event))  # Binding the mouse wheel to the zoom function
            except TimeoutError:
                messagebox.showerror(title="Time Out!",
                                     message="The Drawing function has taken too long to respond\n You can continue with the configuration")
                print("Function execution time out")
                return

    def zoom(self, event):  # Initialising the zoom attributes: "event" is a default return fof the canvas function
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if event.delta > 0:
            self.zoom_in(x, y)
        else:
            self.zoom_out(x, y)

    def zoom_in(self, x, y):  # zoom in function
        self.zoom_level *= self.zoom_factor
        self.canvas.scale("all", x, y, self.zoom_factor, self.zoom_factor)

    def zoom_out(self, x, y):  # zoon out function
        self.zoom_level /= self.zoom_factor
        self.canvas.scale("all", x, y, 1 / self.zoom_factor, 1 / self.zoom_factor)

    def timeout_handler(self, signum, frame):  # function to handle the timeout errors
        raise TimeoutError("Function execution timed out")

    def start(self):
        self.window.mainloop()

    def animate(self):
        self.sub_window = tk.Tk()
        self.sub_window.title('View')
        self.sub_window.geometry('400x200')
        self.sub_window.resizable(0,
                                  0)  # To lock the window size, so the GUI doesn't get jumbled when the size window size changes
        temp_var = tk.StringVar()

        view_label = ttk.Label(self.sub_window, text="View(Top or Side)", font="Arial 7")
        view_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        view_dropdown = ttk.Combobox(self.sub_window,state="normal")
        view_dropdown.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        view_dropdown['values'] = ("top", "side")
        start_layer = ttk.Label(self.sub_window, text="Start",font="Arial 7")
        start_layer.grid(row=1,column=1,padx=10,pady=10,sticky='w')
        start_layer_dropdown = ttk.Combobox(self.sub_window,state='normal')
        start_layer_dropdown['values'] = tuple(range(1, self.count_layer + 1))
        start_layer_dropdown.grid(row=1,column=2,padx=10,pady=10,sticky='w')
        end_layer = ttk.Label(self.sub_window, text="Stop", font="Arial 7")
        end_layer.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        end_layer_dropdown = ttk.Combobox(self.sub_window, state='normal')
        #sel_layer = int(start_layer_dropdown.get())
        end_layer_dropdown['values'] = tuple(range(1, self.count_layer + 1))
        end_layer_dropdown.grid(row=2, column=2, padx=10, pady=10, sticky='w')
        ok = ttk.Button(self.sub_window, text="OK", command=lambda: self.start_animation(view_dropdown.get(),start_layer_dropdown.get(),end_layer_dropdown.get()))
        ok.grid(row=3, column=4, padx=10, pady=10)
        #end_layer_dropdown.bind("<<ComboboxSelected>>", lambda event: self.start_animation(view_dropdown.get(),start_layer_dropdown.get(),end_layer_dropdown.get()))
        print(view_dropdown.get()
              )

        # ok_view = ttk.Button(self.sub_window, text="Ok")
        # ok_view.grid(row=2, column=1, padx=10, pady=10)

    def custom_animate(self):
        self.zoom_flag = True
        self.animate()

    def start_animation(self,view,start,stop):
        print("view",view)
        self.sub_window.destroy()
        self.animation = Animate(r"C:\Users\NetFabb\PycharmProjects\CLItoG\printer_movement_.txt", r"C:\Users\NetFabb\PycharmProjects\CLItoG\printer_attributes_.txt",view,self.zoom_flag,start,stop,self.count_layer)
        self.animation.mainloop()

    def show_file_properties(self):
        file_flag = "Error"
        data_list = []
        if self.file_path.endswith(".cli"):
            file_flag = "OK"
        with open("printer_attributes_.txt") as data_file:
            for line in data_file:
                if line.startswith("$$VERSION"):
                    version = line.split("/")[1]
                    data_list.append(f"Version: {version}")
                elif line.startswith("$$DATE"):
                    date = line.split("/")[1]
                    data_list.append(f"Date: {date}")
                elif line.startswith("$$DIMENSION"):
                    dimension = line.split("/")[1]
                    data_list.append(f"Dimensions: {dimension}")
                elif line.startswith("$$LAYER"):
                    layer = line.split("/")[1]
                    data_list.append(f"Layers: {layer}")
                elif line.startswith("$$UNITS"):
                    units = line.split("/")[1]
                    data_list.append(f"Units: {units}")
            textbox = tk.Text(self.window, height=15, width=40, borderwidth=2, relief=tk.SOLID, highlightthickness=1)
            textbox.configure(bg="blue", fg='light blue')
            temp_string = "File Properties \n"
            for i in data_list:
                temp_string = temp_string + i
            temp_string = temp_string + "Status:" + file_flag

            textbox.insert(tk.END, temp_string)
            textbox.place(x=10, y=530)





obj = GUI()
obj.start()
