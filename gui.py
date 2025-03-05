import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") # make these customizable at some point
from tkinter import filedialog
import json
from utils import *
from core import render
from datetime import datetime

class Application:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("800x600")
        
        self.create_widgets()


        self.app.mainloop()

    def create_widgets(self):
        self.mainframe =  ctk.CTkFrame(self.app)
        self.mainframe.pack(padx=10,pady=10,fill='both', expand=True)
        
        self.mainframe.grid_columnconfigure(0,weight=4, uniform="equal")
        self.mainframe.grid_columnconfigure(1,weight=6, uniform="equal")


        self.parameters_frame = ctk.CTkFrame(self.mainframe, corner_radius=2)
        self.parameters_frame.grid(column=0, sticky="nsew")
        #self.parameters_frame.grid_columnconfigure(0,weight=2)
        #self.parameters_frame.grid_columnconfigure(1,weight=1)
        #self.parameters_frame.grid_columnconfigure(2,weight=2)
        #frame for each row?
        self.camera_label = ctk.CTkLabel(self.parameters_frame, text="Camera (x,y,z)", corner_radius=2)
        self.camera_label.grid(row=0, column=0, sticky="w", padx=5)

        self.camera_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='0,0,0', corner_radius=2)
        self.camera_entry.grid(row=0, column=1, sticky='w')

        self.look_label = ctk.CTkLabel(self.parameters_frame, text='Look at (x,y,z)', corner_radius=2)
        self.look_label.grid(row=0, column=2, sticky='w', padx=5)

        self.look_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='0,0,0', corner_radius=2)
        self.look_entry.grid(row=0, column=3, sticky='w')

        self.camera_button = ctk.CTkButton(self.parameters_frame, text='Confirm', corner_radius=2)
        self.camera_button.grid(row=0, column=4, sticky='we', padx=5)

        self.lights_label = ctk.CTkLabel(self.parameters_frame, text='Light (x,y,z)', corner_radius=2)
        self.lights_label.grid(row=1, column=0)

        self.lights_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='0,0,0', corner_radius=2)
        self.lights_entry.grid(row=1, column=1)

        self.lightIntensity_label = ctk.CTkLabel(self.parameters_frame, text='Intensity (r,g,b)', corner_radius=2)
        self.lightIntensity_label.grid(row=1, column=2)

        self.lightIntensity_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='1,1,1', corner_radius=2)
        self.lightIntensity_entry.grid(row=1,column=3)

        self.light_button = ctk.CTkButton(self.parameters_frame, text='Confirm', corner_radius=2)
        self.light_button.grid(row=1, column=4)

        self.shapes_label = ctk.CTkLabel(self.parameters_frame, text='Shape (x,y,z,R)', corner_radius=2)
        self.shapes_label.grid(row=2, column=0)

        self.shapes_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='1,0,0,1', corner_radius=2)
        self.shapes_entry.grid(row=2, column=1)

        self.shapeColor_label = ctk.CTkLabel(self.parameters_frame, text='Color (r,g,b)', corner_radius=2)
        self.shapeColor_label.grid(row=2, column=2)

        self.shapeColor_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='0.5,0.5,0.5', corner_radius=2)
        self.shapeColor_entry.grid(row=2, column=3)

        self.shape_button = ctk.CTkButton(self.parameters_frame, text='Confirm', corner_radius=2)
        self.shape_button.grid(row=2, column=4)

        self.width_label = ctk.CTkLabel(self.parameters_frame, text='Width', corner_radius=2)
        self.width_label.grid(row=3, column=0)

        self.width_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='320', corner_radius=2)
        self.width_entry.grid(row=3, column=1)

        self.height_label = ctk.CTkLabel(self.parameters_frame, text='Height', corner_radius=2)
        self.height_label.grid(row=3, column=2)

        self.height_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='240', corner_radius=2)
        self.height_entry.grid(row=3, column=3)

        self.resolution_button = ctk.CTkButton(self.parameters_frame, text='Confirm', corner_radius=2)
        self.resolution_button.grid(row=3, column=4)

        self.samplesPerPixel_label = ctk.CTkLabel(self.parameters_frame, text='SPP', corner_radius=2)
        self.samplesPerPixel_label.grid(row=4, column=0)

        self.samplesPerPixel_entry = ctk.CTkEntry(self.parameters_frame, placeholder_text='2', corner_radius=2)
        self.samplesPerPixel_entry.grid(row=4, column=1)

        self.samplesPerPixel_button = ctk.CTkButton(self.parameters_frame, text='Confirm', corner_radius=2)
        self.samplesPerPixel_button.grid(row=4, column=4)


        self.loadCurrentScene_button = ctk.CTkButton(self.parameters_frame, text='Load scene with current params', corner_radius=2)
        self.loadCurrentScene_button.grid(row=5, column=1, columnspan=2, sticky='we', pady=5)

        self.emptyLabel = ctk.CTkLabel(self.parameters_frame, text='Alternatively...')
        self.emptyLabel.grid(row=6, column=0)

        self.loadExistingScene_button = ctk.CTkButton(self.parameters_frame, text='Load predefined scene from file', corner_radius=2, command=self.loadCustomScene)
        self.loadExistingScene_button.grid(row=6, column=1, columnspan=2, sticky='we', pady=5)

        self.infoLabel = ctk.CTkLabel(self.parameters_frame, text='Scene info below', corner_radius=2)
        self.infoLabel.grid(row=7,pady=5)

        self.infoBox = ctk.CTkTextbox(self.parameters_frame, corner_radius=2)
        self.infoBox.grid(row=8, rowspan=4, column=0, columnspan=4,pady=5, sticky='nsew')
        self.infoBox.configure(state='disabled')

        self.render_button = ctk.CTkButton(self.parameters_frame, corner_radius=2, text='Render', command=self.start_rendering)
        self.render_button.grid(row=6,column=4)

        
        self.render_frame = ctk.CTkFrame(self.mainframe)
        self.render_frame.grid(column=1, sticky="nsew")

        placeholder = ctk.CTkLabel(self.render_frame, text="gigalongasaaaaaaaaaaaaaaaaaaaaaaa")
        placeholder.pack()

    

    def loadCustomScene(self):
        file = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")] # cba
        )

        with open(file, 'r') as f:
            data = json.load(f)

        print(data)
        
        scene, num_threads = load_scene(data)

        self.writeToBox(scene, num_threads)

        self.scene=scene
        # print(scene.camera.eye.y)
        # print(scene.shapes[0].color.y) # looks good

    def writeToBox(self,scene, num_threads):
        width = scene.width
        height = scene.height
        spp = scene.samples_per_pixel

        cameraEye = scene.camera.eye
        cameraEye = [cameraEye.x,cameraEye.y,cameraEye.z]
        cameraLookAt = scene.camera.lookat
        cameraLookAt = [cameraLookAt.x,cameraLookAt.y,cameraLookAt.z]
        cameraDistance = scene.camera.distance

        shapes = scene.shapes
        shapes = [[[shape.position.x,shape.position.y,shape.position.z],shape.radius,[shape.color.x,shape.color.y,shape.color.z]] for shape in shapes]
        print(shapes)
        lights = scene.lights
        lights = [[[light.position.x,light.position.y,light.position.z],[light.intensity.x,light.intensity.y,light.intensity.z]] for light in lights]
        print(lights)
        self.infoBox.configure(state='normal')
        self.infoBox.delete('1.0', 'end')

        self.infoBox.insert('1.0', f'Width: {width}\n')
        self.infoBox.insert('2.0', f'Height: {height}\n')
        self.infoBox.insert('3.0', f'SPP: {spp}\n')
        self.infoBox.insert('4.0', f'Eye: {cameraEye}\n')
        self.infoBox.insert('5.0', f'Look at: {cameraLookAt}\n')
        self.infoBox.insert('6.0', f'dist: {cameraDistance}\n')
        self.infoBox.insert('7.0', f'Shapes: {shapes}\n')
        self.infoBox.insert('8.0', f'Lights: {lights}\n')



    def start_rendering(self):
        print("Rendering started")
        pixels = render(self.scene)
        curr_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_png(pixels,self.scene.width,self.scene.height,f"test-{curr_datetime}.png")

    def pause_rendering(self):
        print("Rendering paused")

    def stop_rendering(self):
        print("Rendering stopped")


if __name__ == "__main__":
    app = Application()
