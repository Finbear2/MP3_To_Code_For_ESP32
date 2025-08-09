# Test song is "Sunday Picnic" by "Lobo Loco"
# Link: https://freemusicarchive.org/music/Lobo_Loco/RETRO/Sunday_Picnic_ID_719/

import librosa
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

# *Varibles*

Note_Names = [
    "NOTE_C", "NOTE_CS", "NOTE_D", "NOTE_DS", "NOTE_E", "NOTE_F", "NOTE_FS", "NOTE_G", "NOTE_GS", "NOTE_A", "NOTE_AS", "NOTE_B"
]

Note_Frequencies = {
    "NOTE_C0": 16.35,
    "NOTE_CS0": 17.32,
    "NOTE_D0": 18.35,
    "NOTE_DS0": 19.45,
    "NOTE_E0": 20.60,
    "NOTE_F0": 21.83,
    "NOTE_FS0": 23.12,
    "NOTE_G0": 24.50,
    "NOTE_GS0": 25.96,
    "NOTE_A0": 27.50,
    "NOTE_AS0": 29.14,
    "NOTE_B0": 30.87,
    
    "NOTE_C1": 32.70,
    "NOTE_CS1": 34.65,
    "NOTE_D1": 36.71,
    "NOTE_DS1": 38.89,
    "NOTE_E1": 41.20,
    "NOTE_F1": 43.65,
    "NOTE_FS1": 46.25,
    "NOTE_G1": 49.00,
    "NOTE_GS1": 51.91,
    "NOTE_A1": 55.00,
    "NOTE_AS1": 58.27,
    "NOTE_B1": 61.74,
    
    "NOTE_C2": 65.41,
    "NOTE_CS2": 69.30,
    "NOTE_D2": 73.42,
    "NOTE_DS2": 77.78,
    "NOTE_E2": 82.41,
    "NOTE_F2": 87.31,
    "NOTE_FS2": 92.50,
    "NOTE_G2": 98.00,
    "NOTE_GS2": 103.83,
    "NOTE_A2": 110.00,
    "NOTE_AS2": 116.54,
    "NOTE_B2": 123.47,
    
    "NOTE_C3": 130.81,
    "NOTE_CS3": 138.59,
    "NOTE_D3": 146.83,
    "NOTE_DS3": 155.56,
    "NOTE_E3": 164.81,
    "NOTE_F3": 174.61,
    "NOTE_FS3": 185.00,
    "NOTE_G3": 196.00,
    "NOTE_GS3": 207.65,
    "NOTE_A3": 220.00,
    "NOTE_AS3": 233.08,
    "NOTE_B3": 246.94,
    
    "NOTE_C4": 261.63,
    "NOTE_CS4": 277.18,
    "NOTE_D4": 293.66,
    "NOTE_DS4": 311.13,
    "NOTE_E4": 329.63,
    "NOTE_F4": 349.23,
    "NOTE_FS4": 369.99,
    "NOTE_G4": 392.00,
    "NOTE_GS4": 415.30,
    "NOTE_A4": 440.00,
    "NOTE_AS4": 466.16,
    "NOTE_B4": 493.88,
    
    "NOTE_C5": 523.25,
    "NOTE_CS5": 554.37,
    "NOTE_D5": 587.33,
    "NOTE_DS5": 622.25,
    "NOTE_E5": 659.25,
    "NOTE_F5": 698.46,
    "NOTE_FS5": 739.99,
    "NOTE_G5": 783.99,
    "NOTE_GS5": 830.61,
    "NOTE_A5": 880.00,
    "NOTE_AS5": 932.33,
    "NOTE_B5": 987.77,
    
    "NOTE_C6": 1046.50,
    "NOTE_CS6": 1108.73,
    "NOTE_D6": 1174.66,
    "NOTE_DS6": 1244.51,
    "NOTE_E6": 1318.51,
    "NOTE_F6": 1396.91,
    "NOTE_FS6": 1479.98,
    "NOTE_G6": 1567.98,
    "NOTE_GS6": 1661.22,
    "NOTE_A6": 1760.00,
    "NOTE_AS6": 1864.66,
    "NOTE_B6": 1975.53,
    
    "NOTE_C7": 2093.00,
    "NOTE_CS7": 2217.46,
    "NOTE_D7": 2349.32,
    "NOTE_DS7": 2489.02,
    "NOTE_E7": 2637.02,
    "NOTE_F7": 2793.83,
    "NOTE_FS7": 2959.96,
    "NOTE_G7": 3135.96,
    "NOTE_GS7": 3322.44,
    "NOTE_A7": 3520.00,
    "NOTE_AS7": 3729.31,
    "NOTE_B7": 3951.07,
    
    "NOTE_C8": 4186.01,
    "NOTE_CS8": 4434.92,
    "NOTE_D8": 4698.63,
    "NOTE_DS8": 4978.03,
}

Minimum_Duration = 0.2

# *Functions*

def HZ_To_Note(Frequency):
    
    # Check if the frequency is over 0HZ
    
    if Frequency <= 0: return None;
    
    # Find which key on the piano the frequency is closest to
    
    Note_Number = 12 * np.log2(Frequency / 440.0) + 69
    
    Note_Index = int(round(Note_Number)) % 12
    
    # Convert the note index to a note name
    
    Note_Name = Note_Names[Note_Index]
    
    # Calculate the octave number
    
    Octave_Number = int(round(Note_Number) // 12 - 1  )

    return f"{Note_Name}{Octave_Number}"
    
def Detect_Notes(File_Path):
    
    global Minimum_Duration
    
    print("Please wait while the mp3 is being loaded...")
    
    y, sr = librosa.load(File_Path)
    
    print("MP3 loaded successfully!\n\n")

    # Get Frame Length and Hop Length from user input with defaults

    Frame_Length = int(input("Frame Length (Higher the beter, but slower. Standared is 2048) >>> ") or 2048)
    Hop_Length = int(input("Hop Length (Higher the beter, but slower. Standard is 512) >>> ") or 512)
    Minimum_Duration = float(input(f"Minimum note duration (Default is {Minimum_Duration}) >>> ") or Minimum_Duration)

    print("\n\nDetecting Notes...")

    # Get Pitches
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, n_fft=Frame_Length, hop_length=Hop_Length)
    
    Notes_With_Timings = []
    Last_Note = None
    Last_Time = None
    
    for t in range(pitches.shape[1]): # Loop over time frames
        
        Index = magnitudes[:, t].argmax() # Strongest frequency in this frame
        Frequency = pitches[Index, t]
        
        if Frequency > 0:
            
            Note = HZ_To_Note(Frequency)
            
            Time = t * Hop_Length / sr
            
            # If the note changes, record the previous notes duration
            if Note != Last_Note:
                
                if Last_Note is not None:
                    
                    Duration = Time - Last_Time
                    
                    Notes_With_Timings.append((Last_Note, Last_Time, Duration))
                    
                Last_Note = Note
                Last_Time = Time
                
    #Add the final note
    if Last_Note is not None:
        
        Duration = (len(y) / sr) - Last_Time
        
        Notes_With_Timings.append((Last_Note, Last_Time, Duration))
        
    return Notes_With_Timings

def create_tone(Frequency, Duration_MS):

    if Frequency == 0:

        return AudioSegment.silent(duration=Duration_MS)

    Generator = Sine(Frequency)
    Tone = Generator.to_audio_segment(duration=Duration_MS)
    
    return Tone - 10 

def Save_Song_As_MP3(Notes):
    
    Output = AudioSegment.silent(duration=0)
    
    for Note, Time, Duration in Notes:
        
        Frequency = Note_Frequencies.get(Note, 0)
        Tone = create_tone(Frequency, int(Duration * 1000))
        
        Output += Tone
        
    Output.export("output_song.mp3", format="mp3")
    print("MP3 generated \n \n")

Notes = Detect_Notes(input("Enter the path to the MP3 file >>> "))

print("Done!")

# declare some more varibles

Excess_Time = 0
Last_Note = None

Formatted_Notes = []

# Format the notes into the correct format

print("\nbuzzer.begin(0);")

for note, time, duration in Notes:
    
    if duration >= Minimum_Duration:
        
        if Last_Note is None or Last_Note != note:

            print(f"buzzer.sound({note}, {float((time + Excess_Time) * 1000):.0f});")

            Last_Note = note
            Excess_Time = 0
            
        else:
            
            Excess_Time += duration
            
    else:
        
        Excess_Time += duration

print("buzzer.end();\n")

User_Input_For_MP3 = input("Would you like to save the output as an mp3 file? (May have certain popping sounds when switching between notes) (y/n) >>> ").lower()

if User_Input_For_MP3 == 'y':

    Save_Song_As_MP3(Notes)

User_Input_For_Text = input("Would you like to save the output to a text file? (y/n) >>> ").lower()

if User_Input_For_Text == 'y':
    
    with open("output.txt", "w") as f:
        
        f.write("buzzer.begin(0);\n")
        
        for note, time, duration in Notes:
            
            if duration >= Minimum_Duration:
                
                if Last_Note is None or Last_Note != note:
                    
                    f.write(f"buzzer.sound({note}, {float((time + Excess_Time) * 1000):.0f});\n")
                    
                    Last_Note = note
                    Excess_Time = 0
                    
                else:
                    
                    Excess_Time += duration
                    
            else:
                
                Excess_Time += duration
                
        f.write("buzzer.end();\n")
        
    print("Output saved to output.txt")