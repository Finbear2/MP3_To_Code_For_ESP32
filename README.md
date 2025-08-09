# MP3 to Code For ESP32
---
A simple app that retrieves notes for an MP3 file and converts them to buzzer code compatible with certain buzzer libraries for the ESP32. One of the devices that uses this is the *PocketMage* by *Ashtf8*. 

## Before using

- ffmpeg is required due to Pydub needing to use it for exporting an MP3 preview of the code
- You'll need to install "librosa", "numpy" and "pydub" through pip. The command for this is: `pip install librosa numpy pydub`
- Please put the song you want to use in the folder called "Store_Songs_Here".
- **Chiptune songs work the best** by far. Mainly songs that are from retro games like Game Boy soundtracks.

## To use

1. Run the Python file, I recommend doing it through the terminal as I've had errors when just double-clicking the script.
2. Give the name of your Python file, not the path, because as long as it's in the song folder, you shouldn't have to specify it.
3. Specify the window frame length and the Hop length, though they are already fine-tuned for best performance for most files. If you want to keep the defaults, just press Enter and move on to the next text entry.
4. Wait for the script to extract the notes
5. Specify if you want to export it as a text file or an MP3 file.
6. **You're Done!**

## Thank You!

Just wated to say thanks for even checking this out,it means the world to me :)

# Other stuff

- The included song is "Sunday Picnic" by "Lobo Loco", you can find it at https://freemusicarchive.org/music/Lobo_Loco/RETRO/Sunday_Picnic_ID_719/


Hope you have a lovely day!