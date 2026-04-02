import customtkinter
import subprocess
import threading
import customtkinter as ctk
from PIL import Image
import urllib.request
import io
import sys
import requests
from io import BytesIO

customtkinter.set_appearance_mode("dark")

def button_callback():
    subprocess.run(['playerctl', 'play-pause'], capture_output=True, text=True)

def button_previous():
    subprocess.run(['playerctl', 'previous'], capture_output=True, text=True)

def button_next():
    subprocess.run(['playerctl', 'next'], capture_output=True, text=True)

def load_image(url, label_widget):
    try:
        # Download and open image
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data)) #
        
        # Convert to CTkImage
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(100, 100))
        
        # Update UI from main thread
        label_widget.configure(image=ctk_image, text="")
        label_widget.image = ctk_image # Keep reference
    except Exception as e:
        print(f"Error: {e}")

def get_cover_art_url():
    try:
        # Run the playerctl command to get the artUrl
        result = subprocess.run(
            ['playerctl', 'metadata', '--format', '{{ mpris:artUrl }}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        if url:
            return url
        else:
            return "No cover art URL found."

    except subprocess.CalledProcessError as e:
        # Handle cases where no player is running or the command fails
        return f"Error: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: 'playerctl' command not found. Please ensure it is installed and in your PATH."

def update():
    track_position = subprocess.run(['playerctl', 'position', '--format', '"{{duration(position)}}"'], capture_output=True, text=True)
    track_position_string = track_position.stdout
    track_position_string_float = track_position_string.replace(':', '.')
    track_position_output = track_position_string_float.replace('"', '')

    if track_position_output == '':
        ebloid = 0
    else:
        ebloid = float(track_position_output)

    track_length = subprocess.run(['playerctl', 'metadata', '--format', '"{{duration(mpris:length)}}"'], capture_output=True, text=True)
    track_length_string = track_length.stdout
    track_length_string_float = track_length_string.replace(":", ".")
    track_length_output = track_length_string_float.replace('"', '')

    if track_length_output == '':
        daun = 0
    else:
        daun = float(track_position_output)

    try:
        cover_url = get_cover_art_url()

        clean_path = cover_url.replace("file://", "")

        pil_dark_image = Image.open(clean_path)

        image = customtkinter.CTkImage(
            light_image=pil_dark_image,
            size=(200, 200) # Width x Height
        )
    except FileNotFoundError:
        response = requests.get("https://i.pinimg.com/736x/a9/29/16/a92916d371b56dbbbde21dd289aa13c8.jpg")
        
        pil_image = Image.open(BytesIO(response.content))  #("/home/xsailent/.config/waybar/scripts/not_found.jpg")
        image = customtkinter.CTkImage(
            light_image=pil_image,
            size=(200, 200) # Width x Height
        )

    artist = subprocess.run(['playerctl', 'metadata', '--format', '"{{ artist }}"'], capture_output=True, text=True)
    artist_string = artist.stdout
    artist_output = artist_string.replace('"', '')    

    title = subprocess.run(['playerctl', 'metadata', '--format', '"{{ title }}"'], capture_output=True, text=True)
    title_string = title.stdout
    title_output = title_string.replace('"', '')

    if title_output == '':
        title_output = "Nothing played"

    if artist_output == '':
        artist_output = "Nothing played"

    artist_tex.configure(text=artist_output)
    title_label.configure(text=title_output)

    artist_label.configure(image=image)

    app.after(1000, update)

app = customtkinter.CTk()
app.geometry("550x500")
app.resizable(False, False)
app.title("xsalo playerctl player")

label = customtkinter.CTkLabel(app, font=("Arial", 28), text="Now playing:")
label.grid(row=1, column=0, padx=10, pady=20)

artist_tex = customtkinter.CTkLabel(app, font=("Arial", 20), text="as")
artist_tex.grid(row=3, column=0, padx=30)

title_label = customtkinter.CTkLabel(app, font=("Arial", 18))
title_label.grid(row=4, column=0, padx=30, pady=10)

button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
button_frame.grid(row=6, column=0, pady=10, sticky="new")
app.grid_columnconfigure(0, weight=1)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

button1 = customtkinter.CTkButton(button_frame, text="⏮", height=55, font=("Arial", 26), command=button_previous)
button1.grid(row=0, column=0, padx=0)

button = customtkinter.CTkButton(button_frame, text="⏸", height=55, font=("Arial", 26), command=button_callback)
button.grid(row=0, column=1, padx=0)

button2 = customtkinter.CTkButton(button_frame, text="⏭", height=55, font=("Arial", 26), command=button_next)
button2.grid(row=0, column=2, padx=0)

try:
    artist_label = customtkinter.CTkLabel(app, text="")
    artist_label.grid(row=2, column=0, padx=30, pady=10)
except FileNotFoundError:
    artist_label = customtkinter.CTkLabel(app, text="")#, image=image_govna)
    artist_label.grid(row=2, column=0, padx=30, pady=10)

#slider = customtkinter.CTkSlider(app, from_=0, to=daun)
#slider.grid(row=5, column=0, padx=30)

#slider.set(update().ebloid)

update()

app.mainloop()
