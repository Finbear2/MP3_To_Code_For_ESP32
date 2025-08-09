import librosa
import numpy as np

# *Varibles*

Note_Names = [
    "NOTE_C", "NOTE_CS", "NOTE_D", "NOTE_DS", "NOTE_E", "NOTE_F", "NOTE_FS", "NOTE_G", "NOTE_GS", "NOTE_A", "NOTE_AS", "NOTE_B"
]

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
    
    