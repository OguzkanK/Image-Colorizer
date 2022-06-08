import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import ColorizeImage

def BrowseImage():
    filename = askopenfilename()
    imgInput.config(state="normal")
    imgInput.delete(0, len(imgInput.get()))
    imgInput.insert(0, filename)
    imgInput.config(state="readonly")

def CallColorizeImage(imgSource, save):
    if(save == True):
        colorizeButton.config(state="disabled")
        saveButton.config(state="disabled")
        ColorizeImage.ColorizeImage(imgSource, save)
        messagebox.showinfo("Image Saved", "Image Saved!")
        colorizeButton.config(state="active")
        saveButton.config(state="active")
    else:
        ColorizeImage.ColorizeImage(imgSource, save)


window = tk.Tk()
window.geometry("400x300")

frame = tk.Label(foreground="white",
                 width=20,
                 height=20,
                 font="Arial 14")

frame.pack(pady=10)

imgInput = tk.Entry(frame, width=400)
imgInput.insert(0, "Example-Images/Old-Cat.jpg")
imgInput.config(state="readonly")
imgInput.pack(padx=10, pady=10)


browseFrame = tk.Frame(frame)
browseFrame.pack()
colorizeFrame = tk.Frame(frame)
colorizeFrame.pack()
saveFrame = tk.Frame(frame)
saveFrame.pack()

browseButton = tk.Button(browseFrame, text="Browse Image", foreground="black", font="Arial 14 bold", relief="groove", command=lambda : BrowseImage())
browseButton.pack(pady=10, padx=10)

colorizeButton = tk.Button(colorizeFrame, text="Preview Colorized Image", foreground="black", font="Arial 14 bold", relief="groove",
                           command=lambda : CallColorizeImage(imgInput.get(), False))
colorizeButton.pack(pady=10)

saveButton = tk.Button(saveFrame, text="Save Colorized Image", foreground="black", font="Arial 14 bold", relief="groove",
                      command=lambda : CallColorizeImage(imgInput.get(), True))
saveButton.pack(pady=10)

window.title("Colorize Image")
window.mainloop()