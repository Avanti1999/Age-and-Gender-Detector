# Importing Necessary Libraries
import tkinter as tk                 # Importing tkinter for GUI functionalities
from tkinter import filedialog       # Importing filedialog for file dialog operations
from tkinter import *                # Importing all from tkinter module
from PIL import Image, ImageTk       # Importing Image and ImageTk from PIL (Pillow) for image processing
import numpy                         # Importing numpy for numerical operations
import numpy as np                   # Importing numpy as np for ease of use

# Loading the Model
from keras.models import load_model # type: ignore
model=load_model('Age_Gender_Detection.keras')

# Initializing the GUI
top = tk.Tk()                      # Creating the main window using Tkinter
top.geometry('800x600')            # Setting the size of the window to 800x600 pixels
top.title('Age & Gender Detector') # Setting the title of the window
top.configure(background='#CDCDCD')# Setting the background color of the window to a light grey color

# Initializing the Labels (1 for age and 1 for gender)
label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))  # Creating a label for age with specified background and font
label2 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))  # Creating a label for gender with specified background and font
sign_image = Label(top)                                                # Creating a label to display the image (without specific styling)

# Defining the Detect function which detects the age and gender of the person in the image using the model
def Detect(file_path):
    global label_packed              # Declaring global variable (if used elsewhere in the program)
    
    # Load and process the image
    image = Image.open(file_path)    # Open the image from the given file path
    image = image.resize((48, 48))   # Resize the image to 48x48 pixels
    image = numpy.expand_dims(image, axis=0) # Add an extra dimension to the image array
    image = np.array(image)          # Convert the image to a numpy array
    image = np.delete(image, 0, 1)   # Delete the second axis (channel axis) from the image array
    image = np.resize(image, (48, 48, 3)) # Resize the image to 48x48 pixels with 3 color channels
    print(image.shape)               # Print the shape of the processed image array
    
    # Define the labels for the gender
    sex_f = ["Male", "Female"]
    
    # Normalize the image data
    image = np.array([image]) / 255  # Normalize the image array to range [0, 1]
    
    # Make predictions using the pre-trained model
    pred = model.predict(image)      # Predict age and gender using the model
    age = int(np.round(pred[1][0]))  # Round the predicted age and convert to integer
    sex = int(np.round(pred[0][0]))  # Round the predicted gender and convert to integer
    
    # Print the predictions
    print("Predicted Age is " + str(age))  # Print the predicted age
    print("Predicted Gender is " + sex_f[sex])  # Print the predicted gender
    
    # Update the labels with the predictions
    label1.configure(foreground="#011638", text=age)  # Set the age label with the predicted age
    label2.configure(foreground="#011638", text=sex_f[sex])  # Set the gender label with the predicted gender

# Defining show_Detect_button function
def show_Detect_button(file_path):
    # Create a button to trigger the Detect function
    Detect_b = Button(
        top,                               # Place the button in the main window
        text="Detect Image",               # Set the text on the button
        command=lambda: Detect(file_path), # Set the command to call Detect function with file_path as argument
        padx=10,                           # Set the padding in the x direction
        pady=5                             # Set the padding in the y direction
    )
    
    # Configure the button's appearance
    Detect_b.configure(
        background="#364156",              # Set the background color of the button
        foreground='white',                # Set the text color to white
        font=('arial', 10, 'bold')         # Set the font style, size, and weight
    )
    
    # Place the button in the window with relative positioning
    Detect_b.place(
        relx=0.79,                         # Set the x position relative to the window width
        rely=0.46                          # Set the y position relative to the window height
    )

# Definig Upload Image Function
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image=im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_button(file_path)
    except:
        pass

upload=Button(top,text="Upload an Image",command=upload_image,padx=10,pady=5)
upload.configure(background="#364156",foreground='white',font=('arial',10,'bold'))
upload.pack(side='bottom',pady=50)
sign_image.pack(side='bottom',expand=True)
label1.pack(side="bottom",expand=True)
label2.pack(side="bottom",expand=True)
heading=Label(top,text="Age and Gender Detector",pady=20,font=('arial',20,"bold"))
heading.configure(background="#CDCDCD",foreground="#364156")
heading.pack()
top.mainloop()