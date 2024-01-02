import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from PIL import Image
import subprocess
import importlib.util
import model
import ctypes

class MyGUI():
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme('blue')
        myappid = "Iris Model"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        app = ctk.CTk()
        app.geometry("800x500")
        app.title("Iris Model")
        app.iconbitmap("assets/icone_program.ico")

        app.columnconfigure(0, weight=2)
        #app.columnconfigure(2, weight=1)
        app.columnconfigure(1, weight=6)
        app.rowconfigure(3, weight=1)
        app.rowconfigure((0,2), weight=2)
        
        #Title Page
        home_frame=ctk.CTkFrame(app,corner_radius=30)
        label_page=ctk.CTkLabel(home_frame, text="Iris Model", font=("Arial", 26))
        label_page.grid_configure(column=1, row=0, padx=20,)
        home_image=Image.open("assets/home.png")
        home=ctk.CTkLabel(home_frame, image=ctk.CTkImage(home_image, size=(100,100)),)
        home.grid_configure(column=0, row=0)
        
        home_frame.grid_configure(row=0, columnspan=3, sticky="ew", padx=200)

        #textbox=tk.Text(app, height=3 ,font=("Arial", 16)) #Text Field
        #textbox.pack()

        #myentry= ctk.CTkEntry(app, width=350, height=40)
        #myentry.pack(pady=20)#TextField with 1 line

        #---Import Frame---
        file_frame=ctk.CTkFrame(app, height=50, corner_radius=10)

        label_insert=ctk.CTkLabel(file_frame, text="Insert a CSV file", font=("Arial", 18)) #Text 
        label_insert.grid_configure(row=1, column=0, sticky='ew',  padx=20, pady=20)
        #Import Button
        file_image=Image.open("assets/icon.png")
        self.file_path = tk.StringVar()
        btn_insert=ctk.CTkButton(file_frame, text="Import", font=("Arial", 18), image=ctk.CTkImage(dark_image=file_image, size=(20,20)), compound="top", command=self.browse_file)
        btn_insert.grid_configure(row=2, column=0, sticky='we', padx=20, ipady=2)
        
        #Output File Label
        self.label = ctk.CTkLabel(file_frame, textvariable=self.file_path)
        self.label.grid_configure(row=3, column=0, sticky="we", padx=10, pady=10)
        
        file_frame.grid_configure(row=2, column=0, padx=10)#sticky="ns")


        #Result Button
        btn_result=ctk.CTkButton(app, text="Result", font=("Arial", 18), command=self.show_result)
        btn_result.grid_configure(row=3, columnspan=3, padx=200, pady=20, ipady=5, ipadx=50)#sticky="ew")

        #---- Frame Model -----
        model_frame= ctk.CTkFrame(app, height=50, corner_radius=10)
        model_frame.columnconfigure(0, weight=1)
        model_frame.columnconfigure(1, weight=2)
        model_frame.rowconfigure((0,1,2), weight=1)

        #DropDown Model    
        text=ctk.CTkLabel(model_frame, text="Choose an algorithm", font=("Arial", 14))
        text.grid_configure(row=0,column=0, padx=10, pady=3)

        self.list= ctk.CTkComboBox(model_frame, values=["SVM","Tensorflow","KNN"],command=self.change_option)
        self.list.grid_configure(row=0, column=1)
        
        #DropDown Kernel Option
        self.textOption=ctk.StringVar(value="Choose the type of kernel")
        self.labelOption=ctk.CTkLabel(model_frame, textvariable=self.textOption, font=("Arial", 14))
        self.labelOption.grid_configure(row=1,column=0, padx=10, pady=3)
        self.svm_values=["Linear","Rbf","Sigmoid"]
        self.option_var=ctk.StringVar(value=self.svm_values[0])
        self.option_list= ctk.CTkComboBox(model_frame, values=self.svm_values, variable=self.option_var,command=self.change_var)
        self.option_list.grid_configure(row=1, column=1, pady=20)

        self.pourcentage=ctk.IntVar()
        
        self.slider=ctk.CTkSlider(model_frame, from_=0.5, to=0.9, number_of_steps=4, command=self.show_message)
        self.slider.grid_configure(column=1, row=2)
        self.text_slider=ctk.CTkLabel(model_frame, text="%d %% of Training Dataset" % (self.slider.get()*100))
        self.text_slider.grid_configure(row=2, column=0)
        model_frame.grid_configure(row=2, column=1, ipady=20, ipadx=5)
        
        #Result Label
        self.result = tk.StringVar()
        
        app.mainloop()
    
    def show_message(self):
        # To change text in left of slider
        self.text_slider.configure(text="%d %% of Training Dataset" % (self.slider.get()*100))
    
    def change_var(self, value):
        # To display the value clicked
        self.option_var.set(value)
        print(value)

    def change_option(self, value):
        algorithm=self.list.get()
        print(f"Selected Model: {value}")
        if algorithm == "SVM":
            #To change value of Option Menu
            self.option_list.configure(values=self.svm_values)
            #To display the first value of The List 
            self.option_var.set(self.svm_values[0])
            #To change the text 
            self.textOption.set("Choose the type of kernel")
            #To change the state
            self.option_list.configure(state="normal")
        elif algorithm == "KNN":
            knn_values=["1","3","5","7","9"]
            self.option_list.configure(values=knn_values)
            self.option_var.set(knn_values[0])
            self.textOption.set("Choose the number of neighbour")
            self.option_list.configure(state="normal")
        elif algorithm == "Tensorflow":
            self.option_list.configure(state="disabled")
            print("TensorFlow Selected")
        else:
            print("Error")

    def browse_file(self):
        # Open a file dialog to get the file path
        file_path = tk.filedialog.askopenfilename()

        if not file_path:
            error="Error: No file selected."
            self.file_path.set(error)
            self.label.configure(text_color="red")
            return

        # Check if the file has a .csv extension
        if not file_path.lower().endswith('.csv'):
            error="Error: It isn't a CSV file"
            self.file_path.set(error)
            self.label.configure(text_color="yellow")
        else:
            self.file_path.set(file_path)
            self.label.configure(text_color="white")

        
    def show_result(self):
        # Get the model choosed
        algorithm=self.list.get()
        # Get the option choosed (2 DropDown)
        option=self.option_list.get()
        # Get the percentage
        self.pourcentage=round(1-self.slider.get(),2)
        print("Pourcentage: ",self.pourcentage)
        if algorithm == "SVM":
            accuracy_result=model.svm(self.pourcentage, option.lower())
        elif algorithm == "KNN":
            accuracy_result=model.knn(self.pourcentage, int(option))
        elif algorithm == "Tensorflow":
            option="None"
            accuracy_result=0
        else:
            print("Error")
        #Display the Result
        self.result.set(f"Algorithm: {algorithm}\nOption: {option}\nTesting Set Pourcentage: {self.pourcentage*100}%\n\nAccuracy = {accuracy_result*100:.2f}%")
        #Display The Box with Result
        CTkMessagebox(title="Result of ML", message=self.result.get(), icon="check")

MyGUI()
