Sammie Liang section F (sammiel)

DAW 112 is a simplified music recording program. There are three instrument 
selections: piano,guitar, and drums. You can select one of them and interact 
with the virtual piano to make a recording, and click on another instrument to 
create another track. Up to 8 tracks and 40 bars of recording on each can be created. Access the editing screen for each individual track by clicking on 
its small piano icon. There, you are able to move notes around, as well as 
add and delete notes. Once you are done with editing, you can export your 
recording as an mp3 file. 

Installation:

Before running DAW 112, you will need the following modules installed:
-Pygame
-Pyaudio
-Pydub

For each of these modules, make sure that you have pip working from the command line. If not, follow the instructions here: http://pip.readthedocs.io/en/stable/installing/

Pygame Installation (From https://www.pygame.org/wiki/GettingStarted):
    For Windows:
        -In your command prompt enter:  python -m pip install pygame
    For Macs:
        -Try the pip install method. However, there are known issues with pip 
        install on Macs. 
        -If that doesn't work, follow the instructions on 
        https://www.pygame.org/wiki/MacCompile

Pyaudio Installation (from https://people.csail.mit.edu/hubert/pyaudio/):
    For Windows:
        -In your command prompt enter:  python -m pip install pyaudio
        -This will install both the PortAudio library as well as PyAudio
    For Macs:
        -Homebrew is needed to install PortAudio:
            -Download Homebrew here: https://brew.sh/
        -Then, copy and paste the same pip install command as in Windows

Pydub Installation (from https://github.com/jiaaro/pydub#installation)
    -Follow the instructions on the page to install ffmpeg or librav
        in order to open and save non-wav type files. 
    - Then, for both Windows and Macs:
        -Enter in your command prompt:  python -m pip install pydub


