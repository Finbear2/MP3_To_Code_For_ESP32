# Test song is "Mutant Club" by "HoliznaCC0"
# Link: https://freemusicarchive.org/music/holiznacc0/power-pop/mutant-club/

import librosa
import numpy as np

# *Varibles*

Note_Names = [
    "NOTE_C", "NOTE_CS", "NOTE_D", "NOTE_DS", "NOTE_E", "NOTE_F", "NOTE_FS", "NOTE_G", "NOTE_GS", "NOTE_A", "NOTE_AS", "NOTE_B"
]

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
    
    y, sr = librosa.load(File_Path)

    # Get Frame Length and Hop Length from user input with defaults

    Frame_Length = int(input("Frame Length (Higher the beter, but slower. Standared is 2048) >>> ") or 2048)
    Hop_Length = int(input("Hop Length (Higher the beter, but slower. Standared is 512) >>> ") or 512)
    
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

Notes = Detect_Notes(input("Enter the path to the MP3 file >>> "))

for note, time, duration in Notes:
    print(f"Note: {note}, Time: {time:.2f}s, Duration: {duration:.2f}s")
    
input("Press Enter to exit...")