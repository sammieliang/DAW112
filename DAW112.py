#Sammie Liang (sammiel) Section F
###########################################################
#Term Project: DAW 112
###########################################################

import pygame
import threading
from pydub import AudioSegment
from pydub.playback import play
import decimal,copy,time,math
import os

#Taken from hw1.py file from https://www.cs.cmu.edu/~112/notes/hw1.html
def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#####################################
#Visuals/Animation
#####################################

class MainHelp(object):
    def __init__(self,width,height):
        self.screenWidth = width
        self.screenHeight = height
    def draw(self,screen):
        def drawTitle(self,screen,startY):
            title = "Help Screen - Main Screen"
            titleFont = pygame.font.Font(None,80)
            textSurf,textRect = createTextSurface(title,titleFont,Colors.WHITE)
            textRect.center = (self.screenWidth//2,startY//2) 
            #Centers the text on the tuple position.
            screen.blit(textSurf,textRect)
        #Because pygame's font render function doesn't support multi-line str, 
        #the instructions are stored as a list of str.
        msgs = ["Click on an instrument to go to the virtual piano screen.",
                "Click on the timeline to change the playback location.",
                "Click and drag on a track to move it.",
                "Press on the tiny piano icon on the track to access its " + 
                "editing screen.",
                "Drag the bottom scroller to shift timeline over.",
                "When playing the track, only the play, stop, and help " +
                "buttons can be pressed.",
                "When done with your composition, press export and a " + 
                "mp3 file will be created.",
                "Press any key to return to the main screen."]
        startY,diff = 200,50
        font = pygame.font.Font(None,30)
        drawTitle(self,screen,startY)
        for msg in msgs:
            textSurf,textRect = createTextSurface(msg,font,Colors.WHITE)
            textRect.center = (self.screenWidth//2,startY)
            screen.blit(textSurf,textRect)
            startY += diff #Creates space between instructions.
    def keyPressed(self,event):
        data.help = False 

class EditingHelp(object):
    def __init__(self,width,height):
        self.screenWidth = width
        self.screenHeight = height
    def draw(self,screen):
        def drawTitle(self,screen,startY):
            title = "Help Screen - Editing Screen"
            titleFont = pygame.font.Font(None,80)
            textSurf,textRect = createTextSurface(title,titleFont,Colors.WHITE)
            textRect.center = (self.screenWidth//2,startY//2)
            screen.blit(textSurf,textRect)
        msgs = ["Click on a note and then on an empty space to move it there.",
                "To add notes, press the pencil icon and click on an empty " +
                "space.",
                "To erase, press the eraser icon and click on an existing " +
                "note to delete it.",
                "Drag the scroller at the bottom to shift the timeline over.",
                "Press the back icon to return to the main screen.",
                "Press any key to return to the editing screen."]
        startY,diff = 200,50
        drawTitle(self,screen,startY)
        font = pygame.font.Font(None,30)
        for msg in msgs:
            textSurf,textRect = createTextSurface(msg,font,Colors.WHITE)
            textRect.center = (self.screenWidth//2,startY)
            screen.blit(textSurf,textRect)
            startY += diff
    def keyPressed(self,event):
        data.help = False 

class VirtualPianoHelp(object):
    def __init__(self,width,height):
        self.screenWidth = width
        self.screenHeight = height
    def draw(self,screen):
        def drawTitle(self,screen,startY):
            title = "Help Screen - Virtual Piano Screen"
            titleFont = pygame.font.Font(None,80)
            textSurf,textRect = createTextSurface(title,titleFont,Colors.WHITE)
            textRect.center = (self.screenWidth//2,startY//2)
            screen.blit(textSurf,textRect)
        msgs = ["Press and hold the corresponding letters on the keyboard to "+ 
                "play sounds.",
                "The notes you play are listed on the bottom of the screen.",
                "Press left/right arrow keys to change octaves (from 2 to 4).",
                "Click on the record button to start" + 
                "recording, and again to stop recording.",
                "Press the back icon to return the main screen.",
                "Press any key to return to the virtual piano screen."]
        startY,diff = 200,50
        font = pygame.font.Font(None,30)
        drawTitle(self,screen,startY)
        for msg in msgs:
            textSurf,textRect = createTextSurface(msg,font,Colors.WHITE)
            textRect.center = (self.screenWidth//2,startY)
            screen.blit(textSurf,textRect)
            startY += diff
    def keyPressed(self,event):
        data.help = False 

class StartScreen(object):
    def __init__(self,width,height):
        self.screenWidth =  width
        self.screenHeight = height
        self.startButtonX = width//2
        self.startButtonY = height//2
        self.backgroundImg = pygame.image.load("Icons/music.jpg")
        # Background img taken from
        # http://www.wallpapers-room.com/4168/filter/newest/black/1600x1200/11/
    def draw(self,screen):
        def drawTitle(self,screen):
            title = "DAW 112"
            font = pygame.font.Font(None,150)
            textSurf,textRect = createTextSurface(title,font,Colors.WHITE)
            titleY = 150
            textRect.center = (self.startButtonX,titleY)
            screen.blit(textSurf,textRect)
        def drawStart(self,screen):
            text = "Start"
            font = pygame.font.Font(None,50)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            textRect.center = (self.startButtonX,self.startButtonY)
            screen.blit(textSurf,textRect)
        screen.blit(self.backgroundImg,(0,0))
        drawTitle(self,screen)
        drawStart(self,screen)
    def selected(self,x,y): #Checks if user clicked on start.
        text = "Start"
        font = pygame.font.Font(None,50)
        textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
        textRect.center = (self.startButtonX,self.startButtonY)
        left,top,width,height = textRect
        right,bottom = left + width,top + height
        if left < x < right and top < y < bottom:
            data.mode = "Main Screen"

def tracksFilled(): 
    #Creates a list of 8 bools of whether the corresponding track is filled.
    totalTracks = 8
    areTracksFilled = [False]*totalTracks
    return areTracksFilled

def createNames(instrument): 
    #Creates a name list of all notes in the 3 octave range.
    if instrument != "Drums":
        keyNames = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
        startCount = 2
    else:
        keyNames = ["Kick","Rimshot","Snare","LowTom","MidTom","HiTom",
                    "OpenHH","ClosedHH","PedalHH","Extra","Ride","Cymbal"]
        startCount = 1
    result = []
    totalOctaves = 3
    for i in range(totalOctaves):
        for index in range(len(keyNames)):
            name = keyNames[index] + str(startCount)
            result.append(name)
        startCount += 1
    return result

class data(object): 
    #Holds all of the information, especially for communication between 
    #the program running and the audio functions
    keyPressed, pianoKeyNames = [],[] #Current keys/notes being pressed/played
    mode = "Start Screen"
    currOctave = 3
    playPianoAudio = False
    play = stop = exit = record = False
    add = erase = help = export = False
    trackSelected = None
    trackDrag, scrollDrag = False, False
    tracksFilled = tracksFilled()
    pianoNames = createNames("Piano")
    drumNames = createNames("Drums")
    currNotesRecorded, currPosRecorded= [],[]
    totalNotesRecorded, totalPosRecorded= [],[]
    pianoLabels, drumLabels, trackNames = [],[],[]
    instrumentSelected = ""
    selectedNote = ""
    masterTimeScrubberX = 0 #Tracks timeScrubber pos in curr mode user is in.
    trackOffset, scrollOffset = 0,0
    def reset(): #Resets everything for the purpose of testing.
        data.keyPressed, data.pianoKeyNames = [],[]
        data.mode = "Start Screen"
        data.currOctave = 3
        data.playPianoAudio = False
        data.play = data.stop = data.exit = data.record = False
        data.add = data.erase = data.help = False
        data.trackSelected = None
        data.trackDrag, data.scrollDrag = False,False
        data.tracksFilled = tracksFilled()
        data.pianoNames = createNames("Piano")
        data.drumNames = createNames("Drums")
        data.currNotesRecorded, data.currPosRecorded= [],[]
        data.totalNotesRecorded, data.totalPosRecorded= [],[]
        data.pianoLabels, data.drumLabels, data.trackNames = [],[],[]
        data.instrumentSelected = ""
        data.selectedNote = ""
        data.masterTimeScrubberX = 0
        data.trackOffset, data.scrollOffset = 0,0

class Colors(object): #Stores all the color rgb tuples used in draw functions
    DIM_GRAY = (110,110,110)
    GRAY = (128,128,128)
    COD_GRAY = (30,30,30)
    MINE_SHAFT = (60,60,60)
    EMPEROR = (80,80,80)
    RED = (255,0,0)
    WHITE = (255,255,255)
    NERO = (40,40,40)
    BLACK = (0,0,0)
    ARTIC_BLUE = (59,145,163)
    NOBEL = (150,150,150)
    LIGHT_MAGENTA = (174,101,193)
    NIGHT_RIDER = (50,50,50)
    DOVE_GRAY = (105,105,105)
    LIGHT_BLUE = (173,216,230)
    DARK_GRAY = (20,20,20)

class Screen(object):
    def __init__(self,width,height):
        #play,stop icons from Studio One 3
        self.screenWidth = width
        self.screenHeight = height
        self.play = pygame.image.load("Icons/play.png")
        self.playWidth, self.playHeight = (self.play.get_width(),
                                           self.play.get_height())
        self.stop = pygame.image.load("Icons/stop.png") 
        self.stopWidth, self.stopHeight = (self.stop.get_width(),
                                           self.stop.get_height())
        self.activeplay = pygame.image.load("Icons/activeplay.png")
        self.activestop = pygame.image.load("Icons/activestop.png")
              
class Main_Screen(Screen):
    def __init__(self,width,height):
        super().__init__(width,height)
        self.edit = pygame.image.load("Icons/edit.png")
        #Edit icon from Studio One 3
        self.pianoImage = pygame.image.load("Icons/piano.png")
        #Piano image from https://www.shareicon.net/keyboard-music-piano-
        #electronic-organ-musical-instrument-synthesizer-music-and-multimedia-
        #814108
        self.drumsImage = pygame.image.load("Icons/drums.png")
        #Drum icon from http://prairieprince.com/drum-kit-icon/
        self.guitarImage = pygame.image.load("Icons/guitar.png")
        #Guitar icon from 
        #https://www.iconexperience.com/o_collection/icons/?icon=guitar
    instrumentHeight = 160
    timelineX, timelineY = 280,160
    barWidth = 40
    bottomTimelineY = 720
    trackHeight = 65
    trackY = 200
    playY = stopY = 750
    exportX,exportY = 1275,755
    exportWidth,exportHeight = 100,30
    helpX, helpY = 25,755
    def draw(self,screen):
        def drawInstrumentSelection(self,screen):
            instrumentHeight = Main_Screen.instrumentHeight
            instrumentX = 0
            numberOfSelections = 3
            instrumentWidth = self.screenWidth//numberOfSelections
            pianoX, pianoY = 120,30
            guitarX, guitarY = pianoX + instrumentWidth, pianoY//2
            drumsX, drumsY = guitarX + instrumentWidth, pianoY//2
            pygame.draw.rect(screen,Colors.DIM_GRAY,
                             pygame.Rect(0,0,self.screenWidth,instrumentHeight))
            screen.blit(self.pianoImage,(pianoX,pianoY))
            screen.blit(self.guitarImage,(guitarX,guitarY))
            screen.blit(self.drumsImage,(drumsX,drumsY))
            while instrumentX < self.screenWidth:
                #Draw a line to separate the instrument selections.
                pygame.draw.line(screen,Colors.GRAY,(instrumentX,0),
                                (instrumentX,instrumentHeight))
                instrumentX += instrumentWidth
        def drawTimeline(self,screen):
            def drawTimelineBarLabels(self,screen):
                #Labels the nth full bar across the timeline
                label = str(count//barCount)
                font = pygame.font.Font(None, 20)
                textSurf,textRect = createTextSurface(label,font,Colors.EMPEROR)
                textRect.center = (timelineX + barWidth//2,
                                   timelineY + barHeight//2)
                screen.blit(textSurf,textRect)
            timelineX, timelineY = Main_Screen.timelineX, Main_Screen.timelineY
            barWidth = barHeight = Main_Screen.barWidth
            bottomY = Main_Screen.bottomTimelineY
            pygame.draw.rect(screen,Colors.COD_GRAY,pygame.Rect(0,
                             timelineY,self.screenWidth,barHeight))
            #Shifts label accordingly with offset:
            count = int(data.scrollOffset/barWidth)
            barCount = 4 #Every 4 increments is a bar in the timeline. 
            while timelineX < self.screenWidth+data.scrollOffset:
                if count % barCount == 0:
                    #If we are at a full bar, draw a full line down.
                    pygame.draw.line(screen,Colors.MINE_SHAFT,(timelineX,
                                    timelineY),(timelineX,bottomY))
                    drawTimelineBarLabels(self,screen)
                else:
                    #If not at a bar, draw a slightly shorter line down. 
                    pygame.draw.line(screen,Colors.MINE_SHAFT,(timelineX,
                                    timelineY + barHeight//2),
                                    (timelineX,bottomY))
                timelineX += barWidth
                count += 1
        def drawTracks(self,screen):
            def drawTrackInfo(self,screen,trackCount,initTrackY,trackY,height,
                              width):
                def drawTrackButtons(self,screen,initTrackY,trackY,width,
                                     height):
                    def drawDeleteButton(self,screen,trackY,width,height):
                        deleteX = width//4
                        deleteY = trackY + 2*(height//3)
                        deleteWidth = width//2
                        deleteHeight = height//4
                        pygame.draw.rect(screen,Colors.RED,pygame.Rect(
                                         deleteX,deleteY,deleteWidth,
                                         deleteHeight))
                        text = "Delete"
                        font = pygame.font.Font(None,20)
                        textSurf,textRect = createTextSurface(text,
                                                              font,Colors.WHITE)
                        textRect.center = (deleteX + deleteWidth//2,deleteY + 
                                           deleteHeight//2)
                        screen.blit(textSurf,textRect)
                    def drawEditButton(self,screen,initTrackY,trackY,height):
                        editCenter = (initTrackY + height//3,trackY + height//3)
                        screen.blit(self.edit,editCenter)
                    drawEditButton(self,screen,initTrackY,trackY,height)
                    drawDeleteButton(self,screen,trackY,width,height)
                def drawTrackName(self,screen,trackCount,trackY,width,height):
                    if trackCount < len(data.trackNames):
                        name = data.trackNames[trackCount]
                        font = pygame.font.Font(None,30)
                        textSurf,textRect = createTextSurface(name,font,
                                                              Colors.WHITE)
                        textRect.center = (width//2,(trackY+(height//3)))
                        screen.blit(textSurf,textRect)
                #Checks whether the track we are currently looking at is filled.
                if trackCount < len(data.trackNames):
                    drawTrackButtons(self,screen,initTrackY,trackY,width,height)
                    drawTrackName(self,screen,trackCount,trackY,width,height)
            trackY = initTrackY = Main_Screen.trackY
            trackWidth, trackHeight = (Main_Screen.timelineX, 
                                       Main_Screen.trackHeight)
            trackCount = 0
            while trackY < self.screenHeight-2*trackHeight:
                #Draw track box on the left. 
                pygame.draw.rect(screen,Colors.MINE_SHAFT,pygame.Rect(0,
                                 trackY,trackWidth,trackHeight))
                #Draws the rest of the track.
                pygame.draw.rect(screen,Colors.NERO,pygame.Rect(trackWidth,
                                 trackY,self.screenWidth,trackHeight))
                #Draws line separating track box from rest of the track.
                pygame.draw.line(screen,Colors.BLACK,(0,trackY),
                                (self.screenWidth,trackY))
                if data.tracksFilled[trackCount]: 
                    #Only draw track info if there is a created track there.
                    drawTrackInfo(self,screen,trackCount,initTrackY,trackY,
                                  trackHeight,trackWidth)
                trackY += trackHeight
                trackCount += 1
        def drawRecordedTrack(self,screen):
            def drawTrack(self,screen):
                pygame.draw.rect(screen,Colors.ARTIC_BLUE,pygame.Rect(
                                 startX,trackY,recordedTrackWidth,trackHeight))
                pygame.draw.rect(screen,Colors.BLACK,pygame.Rect(startX,
                                 trackY,recordedTrackWidth,trackHeight),1)
            trackY,trackHeight = Main_Screen.trackY,Main_Screen.trackHeight
            trackX = Main_Screen.timelineX
            barWidth = Main_Screen.barWidth
            trackCount = 0
            while trackY < self.screenHeight-2*trackHeight:
                if data.tracksFilled[trackCount]:
                    #Double checks that there are notes recorded for the track.
                    if trackCount < len(data.totalNotesRecorded):
                        startX = (data.totalPosRecorded[trackCount][0] 
                                 - data.scrollOffset)
                        endX = (data.totalPosRecorded[trackCount][-1]+ 
                               barWidth - data.scrollOffset)
                        #Stops moving track if user drags it too far left.
                        if startX < trackX:
                            startX = trackX
                        #Only draw the track if it is actually there in the 
                        #current view of the timeline.
                        if endX > startX:
                            recordedTrackWidth = endX-startX
                            drawTrack(self,screen)
                trackY += trackHeight
                trackCount += 1
        def drawPlayMenu(self,screen): #Draws play & stop buttons on the bottom
            play = self.play
            stop = self.stop
            if data.play:
                play = self.activeplay
            elif data.stop:
                stop = self.activestop
            playCenter = (self.screenWidth//2, Main_Screen.playY)
            stopCenter = (playCenter[0] + self.playWidth*2, Main_Screen.stopY)
            screen.blit(play,playCenter)
            screen.blit(stop,stopCenter)
        def drawExportButton(self,screen):
            exportX, exportY = Main_Screen.exportX, Main_Screen.exportY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            pygame.draw.rect(screen,Colors.DIM_GRAY,pygame.Rect(exportX,
                             exportY,width,height))
            text = "Export"
            font = pygame.font.Font(None,25)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            textRect.center = (exportX + (width//2),(exportY+(height//2)))
            screen.blit(textSurf,textRect)
        def drawHelpButton(self,screen):
            helpX, helpY = Main_Screen.helpX, Main_Screen.helpY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            pygame.draw.rect(screen,Colors.DIM_GRAY,pygame.Rect(helpX,
                             helpY,width,height))
            text = "Help"
            font = pygame.font.Font(None,25)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            textRect.center = (helpX + (width//2),(helpY+(height//2)))
            screen.blit(textSurf,textRect)
        drawExportButton(self,screen)
        drawHelpButton(self,screen)
        drawInstrumentSelection(self,screen)
        drawTracks(self,screen)
        drawTimeline(self,screen)
        drawPlayMenu(self,screen)
        drawRecordedTrack(self,screen)
    def selected(self,x,y,timeScrubber):
        def changeTime(self,x,y,timeScrubber): 
            #If user clicks on timeline, scrubber moves to wherever they click. 
            timelineX, timelineY = Main_Screen.timelineX, Main_Screen.timelineY
            barWidth = timelineHeight = Main_Screen.barWidth
            #Snaps selection to nearest 1/4th bar:
            selectedX = roundHalfUp(x/barWidth)*barWidth 
            if (timelineX < x < self.screenWidth and timelineY < y < 
                timelineY + timelineHeight):
                timeScrubber.x = selectedX
        def playbackSelected(self,x,y):
            playLeft = self.screenWidth//2
            playRight = playLeft + self.playWidth
            playTop = Main_Screen.playY
            playBottom = playTop + self.playHeight
            stopLeft = playRight + self.playWidth
            stopRight = stopLeft + self.stopWidth
            stopTop = playTop 
            stopBottom = stopTop + self.stopHeight
            if playLeft <= x <= playRight and playTop <= y <= playBottom:
                data.play = not(data.play)
                data.stop = False
            elif (stopLeft <= x <= stopRight and stopTop <= y <= stopBottom):
                data.stop = not(data.stop)
                data.play = False
                data.scrollOffset = 0
        def instrumentSelected(self,x,y):
            instrumentNumber = 3
            def pianoSelected(self,x,y):
                pianoLeft,pianoTop = 0,0
                pianoRight = self.screenWidth//instrumentNumber
                pianoBottom = Main_Screen.instrumentHeight
                if pianoLeft < x < pianoRight and pianoTop < y < pianoBottom:
                    return True
                return False
            def guitarSelected(self,x,y):
                guitarLeft = self.screenWidth//instrumentNumber
                guitarRight = 2*guitarLeft
                guitarTop = 0
                guitarBottom = Main_Screen.instrumentHeight
                if guitarLeft < x < guitarRight and guitarTop<y<guitarBottom:
                    return True
                return False
            def drumsSelected(self,x,y):
                drumsLeft = 2*(self.screenWidth//instrumentNumber)
                drumsRight = self.screenWidth
                drumsTop = 0
                drumsBottom = Main_Screen.instrumentHeight
                if drumsLeft < x < drumsRight and drumsTop < y < drumsBottom:
                    return True
                return False
            totalTracks = 8
            if not(data.play) and len(data.trackNames) < totalTracks:
                selected = False
                if pianoSelected(self,x,y):
                    data.instrumentSelected = "Piano"
                    selected = True
                elif guitarSelected(self,x,y):
                    data.instrumentSelected = "Guitar"
                    selected = True
                elif drumsSelected(self,x,y):
                    data.instrumentSelected = "Drums"
                    selected = True
                if data.instrumentSelected != "" and selected == True:
                    #If user selects instrument, reset notes & virtual piano. 
                    data.mode = "Virtual Piano"
                    data.currOctave = 3
                    data.currNotesRecorded,data.currPosRecorded= [],[]
        def trackSelected(self,x,y,timeScrubber):
            def trackButtonsSelected(self,x,y,startY,height,width,initTrackY,
                                     trackCount,timeScrubber):
                def editButtonSelected(self,x,y,trackY,height,initTrackY,
                                       trackCount,timeScrubber):
                    editLeft = initTrackY + height//3
                    editRight = editLeft + self.edit.get_width()
                    editTop = trackY + height//3
                    editBottom = editTop + self.edit.get_height()
                    if (editLeft <= x <= editRight and editTop <= y <= 
                        editBottom):
                        data.mode = "Editing Screen"
                        data.trackSelected = trackCount
                        #Set curr notes to whatever track selected. 
                        data.currNotesRecorded = (
                        data.totalNotesRecorded[trackCount])
                        data.currPosRecorded= (
                        data.totalPosRecorded[trackCount])
                        timeScrubber.reset()
                        return True
                    return False
                def deleteButtonSelected(self,x,y,startY,height,width,
                                         trackCount):

                    deleteX, deleteY = width//4, startY + 2*(height//3)
                    deleteWidth, deleteHeight = width//2, height//4
                    if (deleteX < x < deleteX + deleteWidth and deleteY < y < 
                        deleteY + deleteHeight):
                        trackNotes = data.totalNotesRecorded[trackCount]
                        trackTimes = data.totalPosRecorded[trackCount]
                        data.totalNotesRecorded.remove(trackNotes)
                        data.totalPosRecorded.remove(trackTimes)
                        if False in data.tracksFilled: 
                            index = data.tracksFilled.index(False)
                        else:
                            index = len(data.tracksFilled)
                            trackCount = index - 1
                        #When an instrument is deleted, all the instruments 
                        #after move up one, so only last track becomes empty.
                        data.tracksFilled[index-1] = False
                        trackName = data.trackNames[trackCount]
                        data.trackNames.remove(trackName)
                        return True
                    return False
                if data.tracksFilled[trackCount]:
                    if (editButtonSelected(self,x,y,startY,height,initTrackY,
                        trackCount,timeScrubber) or deleteButtonSelected(self,
                        x,y,startY,height,width,trackCount)):
                        return True
                    return False
            def isMovingTrack(self,x,y,trackY,height,width,trackCount,barWidth):
                #If user is clicking on the track, allow it to be dragged.
                if (data.tracksFilled[trackCount] and 
                    data.totalNotesRecorded != []):
                    trackSelected = data.totalPosRecorded[trackCount]
                    selectedX = int(x/barWidth)*barWidth
                    if trackY < y < trackY + height:
                        if selectedX in trackSelected:
                            if data.trackDrag == False:
                                data.trackDrag = True
                                return True
            if not data.play:
                trackY,trackHeight = Main_Screen.trackY,Main_Screen.trackHeight
                width = Main_Screen.timelineX
                barWidth = Main_Screen.barWidth
                initTrackY = trackY
                trackCount = 0
                while trackY < self.screenHeight-2*trackHeight:
                    #Go through each track and see if user has selected any 
                    #buttons or tracks.
                    if trackButtonsSelected(self,x,y,trackY,trackHeight,width,
                        initTrackY,trackCount,timeScrubber):
                        data.scrollOffset = 0
                        break
                    elif isMovingTrack(self,x,y,trackY,trackHeight,width,
                         trackCount,barWidth) == True:
                        break
                    else:
                        trackY += trackHeight
                        trackCount += 1
        def exportSelected(self,x,y):
            exportX, exportY = Main_Screen.exportX, Main_Screen.exportY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            if exportX < x < exportX + width and exportY < y < exportY + height:
                if data.totalNotesRecorded != []:
                    data.play = False
                    data.export = True
                    exportRecording()
                    data.export = False
        def helpSelected(self,x,y):
            helpX, helpY = Main_Screen.helpX, Main_Screen.helpY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            if helpX < x < helpX + width and helpY < y < helpY + height:
                data.help = True
        changeTime(self,x,y,timeScrubber)
        playbackSelected(self,x,y)
        instrumentSelected(self,x,y)
        trackSelected(self,x,y,timeScrubber)
        exportSelected(self,x,y)
        helpSelected(self,x,y)
    def moveTrack(self,x,y): 
        #Allows user to click on & drag a track to move it. 
        trackY, trackHeight = Main_Screen.trackY, Main_Screen.trackHeight
        trackX = Main_Screen.timelineX
        barWidth = Main_Screen.barWidth
        trackCount = 0
        while trackY < self.screenHeight-2*trackHeight:
            if data.tracksFilled[trackCount] and data.totalNotesRecorded != []:
                trackSelected = data.totalPosRecorded[trackCount]
                selectedX = int(x/barWidth)*barWidth
                #Check if the user is dragging within the bounds of track.
                if (trackX <= selectedX <= self.screenWidth and 
                    trackY < y < trackY + trackHeight):
                    data.trackOffset = selectedX - trackSelected[0]
                    for i in range(len(trackSelected)):
                        trackSelected[i] += data.trackOffset
                    data.totalPosRecorded[trackCount] = trackSelected
                    break
            trackY += trackHeight
            trackCount += 1
                
class Scroller(object): #Used to shift the timeline to access more bars.
    def __init__(self,screenWidth):
        self.mainScreenX,self.editingScreenY = 0,0
        self.mainScreenY = 720
        self.editingScreenY = 732
        self.screenWidth = screenWidth
        self.height = 10
        self.scrollerX = 0
        self.scrollerWidth = 40
    def draw(self,screen):
        if data.mode == "Main Screen":
            x,y = self.mainScreenX,self.mainScreenY
        elif data.mode == "Editing Screen":
            x,y = self.mainScreenX,self.editingScreenY
        def drawScrollerBackground(self,x,y):
            pygame.draw.rect(screen,Colors.NIGHT_RIDER,pygame.Rect(x,y,
                             self.screenWidth,self.height))
            #Outline the rectangle drawn black:
            pygame.draw.rect(screen,Colors.BLACK,pygame.Rect(x,y,
                             self.screenWidth,self.height),1)
        def drawScroller(self,y):
            pygame.draw.rect(screen,Colors.DIM_GRAY,pygame.Rect(
                             self.scrollerX,y,self.scrollerWidth,self.height-2))
        drawScrollerBackground(self,x,y)
        drawScroller(self,y)
    def selectScroller(self,x,y):
        if data.mode != "Virtual Piano":
            if data.mode == "Main Screen":
                scrollerY = self.mainScreenY
            elif data.mode == "Editing Screen":
                scrollerY = self.editingScreenY
            if (self.scrollerX < x < self.scrollerX + self.scrollerWidth and 
                scrollerY < y < scrollerY + self.height):
                data.scrollDrag = True
    def moveScroller(self,x,y): #Shift timeline over when scroller is dragged.
        if data.mode == "Main Screen":
            scrollerY = self.mainScreenY
        elif data.mode == "Editing Screen":
            scrollerY = self.editingScreenY
        barWidth = Main_Screen.barWidth
        #Snap to the nearest 1/4th bar:
        selectedX = int(x/self.scrollerWidth)*self.scrollerWidth
        if (0 <= selectedX <= self.screenWidth and scrollerY < y < 
            scrollerY + self.height):
            barCount = 4 #A bar is every four barWidths
            data.scrollOffset = barCount*selectedX #Move timeline one bar over.
            self.scrollerX = selectedX
        
class Editing_Screen(Screen):
    def __init__(self,width,height):
        super().__init__(width,height)
        #Add and erase buttons from Studio One 3
        self.backButton = pygame.image.load("Icons/editingBack.jpg")
        self.add = pygame.image.load("Icons/add.png")
        self.activeAdd = pygame.image.load("Icons/activeadd.png")
        self.erase = pygame.image.load("Icons/erase.png")
        self.activeErase = pygame.image.load("Icons/activeerase.png")
        #backButton from http://img.freepik.com/free-icon/arrow-back-button_318-
        #70659.jpg?size=338&ext=jpg
    timelineY = 80
    bottomTimelineY = 730
    pianoRollY = 120
    helpWidth,helpHeight = 100,30
    helpX, helpY = 25,755
    addX, addY = 1200,750
    noteWidth, noteHeight = 40,17
    def draw(self,screen):
        if data.trackNames[data.trackSelected] != "Drums":
            labels = data.pianoLabels
            names = data.pianoNames
        else:
            labels = data.drumLabels
            names = data.drumNames
        def drawTimeline(self,screen):
            timelineX, timelineY = (Main_Screen.timelineX, 
                                    Editing_Screen.timelineY)
            barWidth = barHeight = Main_Screen.barWidth
            barCount = 4
            bottomY = Editing_Screen.bottomTimelineY
            pygame.draw.rect(screen,Colors.COD_GRAY,pygame.Rect(0,timelineY,
                             self.screenWidth,barHeight))
            count = int(data.scrollOffset/barWidth)
            while timelineX < self.screenWidth + data.scrollOffset:
                if count % barCount == 0:
                    pygame.draw.line(screen,Colors.MINE_SHAFT,(timelineX,
                                     timelineY),(timelineX,bottomY))
                    label = str(count//barCount)
                    font = pygame.font.Font(None, 20)
                    textSurf,textRect = createTextSurface(label,font,
                                                          Colors.EMPEROR)
                    textRect.center = (timelineX + barWidth//2,timelineY + 
                                                               barHeight//2)
                    screen.blit(textSurf,textRect)
                else:
                    pygame.draw.line(screen,Colors.MINE_SHAFT,(timelineX,
                            timelineY + barHeight//2), (timelineX,bottomY))
                timelineX += barWidth
                count += 1
        def drawHeader(self,screen): 
            #Displays title to show which instrument the user is editing.
            instrument = data.trackNames[data.trackSelected]
            text = "Editing Screen : " + instrument 
            font = pygame.font.Font(None,40)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            headerHeight = 40
            textRect.center = (self.screenWidth//2,headerHeight)
            screen.blit(textSurf,textRect)
        def drawPianoRoll(self,screen): 
            #Displays the labels of all the selected instrument's notes on left
            startY,startX = Editing_Screen.pianoRollY,Main_Screen.timelineX
            barHeight = Main_Screen.barWidth
            noteCountTotal = 36
            height = (self.screenHeight-startY-barHeight)//noteCountTotal
            count = 0
            while startY < self.screenHeight-4*height:
                pygame.draw.rect(screen,Colors.MINE_SHAFT,pygame.Rect(
                                 0,startY,self.screenWidth//5,height))
                pygame.draw.rect(screen,Colors.NERO,pygame.Rect(280,startY,
                                 self.screenWidth,height))
                pygame.draw.line(screen,Colors.BLACK,(0,startY),
                                (self.screenWidth,startY))
                label = names[count]
                font = pygame.font.Font(None, 20)
                TextSurf, TextRect = createTextSurface(label,font,Colors.NOBEL)
                TextRect.center = (startX//2,startY+height//2)
                screen.blit(TextSurf,TextRect)
                startY += height
                count += 1
        def drawPlayMenu(self,screen):
            play = self.play
            stop = self.stop
            if data.play:
                play = self.activeplay
            elif data.stop:
                stop = self.activestop
            playCenter = (self.screenWidth//2, Main_Screen.playY)
            stopCenter = (playCenter[0] + self.playWidth*2, Main_Screen.stopY)
            screen.blit(play,playCenter)
            screen.blit(stop,stopCenter)
        def drawButtons(self,screen): #Draws add and erase buttons
            backX = backY = 10
            screen.blit(self.backButton,(backX,backY))
            add = self.add
            erase = self.erase
            if data.add:
                add = self.activeAdd
            elif data.erase:
                erase = self.activeErase
            addCenter = (Editing_Screen.addX, Editing_Screen.addY)
            eraseCenter = (addCenter[0] + add.get_width(), Editing_Screen.addY)
            screen.blit(add,addCenter)
            screen.blit(erase,eraseCenter)
        def drawMidi(self,screen): #Draws all recorded notes for selected track 
            width,height = Editing_Screen.noteWidth,Editing_Screen.noteHeight
            if data.currNotesRecorded != []:
                for i in range(len(data.currNotesRecorded)):
                    notes = data.currNotesRecorded[i]
                    xPos = data.currPosRecorded[i] - data.scrollOffset
                    for note in notes:
                        startY, noteCountTotal = labels[note], 36
                        #Check if note is still within view with offset:
                        if xPos >= Main_Screen.timelineX: 
                            #If note is selected, highlight it magenta.
                            if (data.selectedNote != "" and 
                                note == data.selectedNote[0] and xPos == 
                                data.selectedNote[1] - data.scrollOffset):
                                pygame.draw.rect(screen,
                                    Colors.LIGHT_MAGENTA,pygame.Rect(xPos,
                                        startY,width,height))
                            else:
                                pygame.draw.rect(screen,Colors.ARTIC_BLUE,
                                    pygame.Rect(xPos,startY,width,height))
                            pygame.draw.rect(screen,Colors.BLACK,
                                    pygame.Rect(xPos,startY,width,height),1)
        def drawHelpButton(self,screen):
            helpX, helpY = Main_Screen.helpX, Main_Screen.helpY
            width, height = Editing_Screen.helpWidth, Editing_Screen.helpHeight
            pygame.draw.rect(screen,Colors.DIM_GRAY,pygame.Rect(helpX,
                             helpY,width,height))
            text = "Help"
            font = pygame.font.Font(None,25)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            textRect.center = (helpX + (width//2),(helpY+(height//2)))
            screen.blit(textSurf,textRect)
        drawPianoRoll(self,screen)
        drawTimeline(self,screen)
        drawPlayMenu(self,screen)
        drawButtons(self,screen)
        drawMidi(self,screen)
        drawHeader(self,screen)
        drawHelpButton(self,screen)
    def selected(self,x,y,timeScrubber):
        if data.trackNames[data.trackSelected] != "Drums":
            #Piano & guitar share same notes, so guitar uses piano labels too.
            labels = data.pianoLabels
            names = data.pianoNames
        else:
            labels = data.drumLabels
            names = data.drumNames
        def helpSelected(self,x,y):
            helpX, helpY = Main_Screen.helpX, Main_Screen.helpY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            if helpX < x < helpX + width and helpY < y < helpY + height:
                data.help = True
        def playbackSelected(self,x,y):
            playLeft = self.screenWidth//2
            playRight = playLeft + self.playWidth
            playTop = Main_Screen.playY
            playBottom = playTop + self.playHeight
            stopLeft = playRight + self.playWidth
            stopRight = stopLeft + self.stopWidth
            stopTop = playTop 
            stopBottom = stopTop + self.stopHeight
            if playLeft <= x <= playRight and playTop <= y <= playBottom:
                data.play = not(data.play)
                data.stop = False
            elif (stopLeft <= x <= stopRight and stopTop <= y <= stopBottom):
                data.stop = not(data.stop)
                data.play = False
                data.scrollOffset = 0
        def editMidiSelected(self,x,y):#Checks if add/erase buttons are clicked
            addLeft = Editing_Screen.addX
            addRight = addLeft + self.add.get_width()
            addTop = Editing_Screen.addY
            addBottom = addTop + self.add.get_height()
            eraseLeft = addRight
            eraseRight = eraseLeft + self.erase.get_width()
            eraseTop = addTop
            eraseBottom = addBottom
            if (addLeft <= x <= addRight and addTop <= y <= addBottom):
                data.erase = False
                data.add = not(data.add)
            elif (eraseLeft<=x<=eraseRight and eraseTop<=y<=eraseBottom):
                data.erase = not(data.erase)
                data.add = False
        def backSelected(self,x,y,timeScrubber):
            backLeft = 10
            backRight = backLeft + self.backButton.get_width()
            backTop = backLeft
            backBottom = backTop + self.backButton.get_height()
            if backLeft <= x <= backRight and backTop <= y <= backBottom:
                data.add = data.erase = False
                data.play = data.stop = False
                timeScrubber.reset()
                data.scrollOffset = 0
                data.selectedNote = ""
                data.mode = "Main Screen"
        def noteSelected(self,x,y): #Checks if an existing note is pressed.
            if data.selectedNote == "" and not (data.add or data.erase):
                noteWidth, noteHeight = (Editing_Screen.noteWidth,
                                        Editing_Screen.noteHeight)
                for i,notes in enumerate(data.currNotesRecorded):
                    for note in notes:
                        left = data.currPosRecorded[i]
                        offsetLeft = left - data.scrollOffset
                        right = offsetLeft + noteWidth
                        top = labels[note]
                        bottom = top + noteHeight
                        if (offsetLeft <= x <= right and top <= y <= bottom):
                            data.selectedNote = (note,left,top)
                            return
            data.selectedNote = ""
        def moveSelectedNote(self,x,y): 
            #Moves selected note to selected empty space.
            def moveNoteInTrack(self,newX,note,newNote,i):
                #Adds notes if new position exists already in data.currTimes
                newI = data.currPosRecorded.index(newX)
                #If user clicks on existing note instead, do nothing.
                if newNote in data.currNotesRecorded[newI]:
                    return 
                else:
                    data.currNotesRecorded[i].remove(note)
                    data.currNotesRecorded[newI].append(newNote)
            def moveNoteOutsideTrack(self,newX,note,newNote,i):
                #Moves the note outside the bounds of existing track.
                #Check the end bounds of the positions.
                if newX > data.currPosRecorded[-1]:
                    data.currPosRecorded.append(newX)
                    data.currNotesRecorded[i].remove(note)
                    data.currNotesRecorded.append([newNote])
                elif newX < data.currPosRecorded[0]:
                    data.currPosRecorded.insert(0,newX)
                    data.currNotesRecorded[i].remove(note)
                    data.currNotesRecorded.insert(0,[newNote])
                else:
                    #If position is in track bounds, but 
                    #not already in data.currPosRecorded
                    for index,times in enumerate(data.currPosRecorded):
                        if times > newX:
                            data.currPosRecorded.insert(index,newX)
                            data.currNotesRecorded[i].remove(note)
                            data.currNotesRecorded.insert(index,[newNote])
                            return
            if data.selectedNote != "" and (not(data.erase) and not(data.add)):
                note = data.selectedNote[0]
                noteWidth, noteHeight = (Editing_Screen.noteWidth,
                                        Editing_Screen.noteHeight)
                #Finds the nearest note and pos to space where user clicked.
                newX = int(x/noteWidth)*noteWidth + data.scrollOffset
                newY = math.ceil(y/noteHeight)*noteHeight
                minX,maxX = Main_Screen.timelineX,self.screenWidth
                minY = data.pianoLabels["C2"]
                maxY = data.pianoLabels["B4"] + noteHeight
                oldX,oldY = data.selectedNote[1], labels[note]
                if (minX <= newX <= maxX and minY <= newY <= maxY):
                    noteChange = (newY-oldY)//noteHeight
                    newIndex = names.index(note) + noteChange
                    newNote = names[newIndex]
                    i = data.currPosRecorded.index(oldX)
                    #If user clicks on the same note again instead, do nothing.
                    if newX == oldX and note == newNote:    return
                    elif newX in data.currPosRecorded:
                        moveNoteInTrack(self,newX,note,newNote,i)
                    else:
                        moveNoteOutsideTrack(self,newX,note,newNote,i)
        def addNote(self,x,y):
            def addNoteOutsideTrack(): #Similar to moveNoteOutsideTrack
                if newX > data.currPosRecorded[-1]:
                    data.currPosRecorded.append(newX)
                    data.currNotesRecorded.append([newNote])
                elif newX < data.currPosRecorded[0]:
                    data.currPosRecorded.insert(0,newX)
                    data.currNotesRecorded.insert(0,[newNote])
                else:
                    for index,times in enumerate(data.currPosRecorded):
                        if times > newX:
                            data.currPosRecorded.insert(index,newX)
                            data.currNotesRecorded.insert(index,[newNote])
                            return
            noteWidth, noteHeight = (Editing_Screen.noteWidth,
                                     Editing_Screen.noteHeight)
            newX = int(x/noteWidth)*noteWidth
            newY = math.ceil(y/noteHeight)*noteHeight
            minX,maxX = Main_Screen.timelineX, self.screenWidth
            minY = data.pianoLabels["C2"]
            maxY = data.pianoLabels["B4"] + noteHeight
            if minX <= newX <= maxX and minY <= newY <= maxY:
                noteIndex = (newY - minY)//noteHeight 
                newNote = names[noteIndex]
                if newX in data.currPosRecorded:
                    newI = data.currPosRecorded.index(newX)
                    if newNote in data.currNotesRecorded[newI]:     
                        return
                    else:   
                        data.currNotesRecorded[newI].append(newNote)
                else:
                    addNoteOutsideTrack()
        def eraseNote(self,x,y):
            noteWidth, noteHeight = (Editing_Screen.noteWidth,
                                     Editing_Screen.noteHeight)
            selectedX = int(x/noteWidth)*noteWidth
            selectedY = math.ceil(y/noteHeight)*noteHeight
            minX,maxX = Main_Screen.timelineX, self.screenWidth
            minY = data.pianoLabels["C2"]
            maxY = data.pianoLabels["B4"] + noteHeight
            if minX <= selectedX <= maxX and minY <= selectedY <= maxY:
                noteIndex = (selectedY-minY)//noteHeight
                note = names[noteIndex]
                #Checks if user clicked on a existing note, not an empty space.
                if selectedX in data.currPosRecorded:
                    i = data.currPosRecorded.index(selectedX)
                    if note in data.currNotesRecorded[i]:
                        data.currNotesRecorded[i].remove(note)
        helpSelected(self,x,y)
        playbackSelected(self,x,y)
        backSelected(self,x,y,timeScrubber)
        moveSelectedNote(self,x,y)
        noteSelected(self,x,y)
        editMidiSelected(self,x,y)
        if data.erase:  
            eraseNote(self,x,y)
        if data.add:    
            addNote(self,x,y)

def createLabelsDict(screenHeight,instrument):
    #Creates dict that maps each note to its y location in piano roll labelling 
    if instrument != "Drums":
        order = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
    else:
        order = ["Kick","Rimshot","Snare","LowTom","MidTom","HiTom","OpenHH",
                 "ClosedHH","PedalHH","Extra","Ride","Cymbal"]
    labelsList = dict()
    startY, timelineHeight = 120, 40
    noteCountTotal = 36
    height = (screenHeight-startY-timelineHeight)//noteCountTotal
    octave, totalNotesInOctave = 1, 12
    for i in range(noteCountTotal):
        index = i % totalNotesInOctave
        if index == 0:  octave += 1
        if instrument != "Drums":   note = order[index] + str(octave)
        #Octave-1 since the drum samples are labelled from 1-3, not 2-4 octaves
        else:   note = order[index] + str(octave-1)
        labelsList[note] = startY
        startY += height
    return labelsList

class Virtual_Piano(object):
    pianoXPos = 140
    pianoYPos = 160
    keyWidth = 140
    keyHeight = 400
    recordX = 1200
    recordY = 650
    def __init__(self):
        #keyOrder are the keyboard keys matching w/ notes in instrumentKeyOrder
        self.keyOrder = ["A","W","S","E","D","F","T","G","Y","H","U","J"]
        self.instrumentKeyOrder = ["C","Db","D","Eb","E","F","Gb","G","Ab",
                                   "A","Bb","B"]
        #Matches the notes in whether they are a white or black key.
        W = "White" 
        B = "Black"
        self.colorKeyOrder = [W,B,W,B,W,W,B,W,B,W,B,W]
        self.backButton = pygame.image.load("Icons/back.jpeg")
        #Back button is the same as the editing back button.
        self.record = pygame.image.load("Icons/record.png")
        self.activerecord = pygame.image.load("Icons/activerecord.png")
        #Record buttons from Studio One 3
    def drawPiano(self,screen):
        keyX = Virtual_Piano.pianoXPos
        keyWidth,keyHeight = Virtual_Piano.keyWidth,Virtual_Piano.keyHeight
        #Draw white keys first
        for i,key in enumerate(self.colorKeyOrder):
            if key == "White":
                Virtual_Piano.drawKeys(self,screen,keyWidth,keyHeight,key,i,
                                       keyX)
                keyX += keyWidth
        #And then black keys.
        keyX = Virtual_Piano.pianoXPos
        for i,key in enumerate(self.colorKeyOrder):
            if key == "Black":
                width = keyWidth//2
                keyX += int(1.55*width)
                height = int(.75*keyHeight) 
                Virtual_Piano.drawKeys(self,screen,width,height,key,i,keyX)
                if (i + 2 > len(self.colorKeyOrder) - 1 or 
                    self.colorKeyOrder[i+1] != "White" or 
                    self.colorKeyOrder[i+2] != "Black"):
                    keyX += width//2 + keyWidth
                else:
                    keyX += width//2
    def drawKeys(self,screen,width,height,key,i,keyX):
        screenWidth,screenHeight = screen.get_size()
        pianoYPos = Virtual_Piano.pianoYPos
        def drawKey(self,screen,key,width,height,i,keyX):
            if key == "White":
                pygame.draw.rect(screen,Colors.WHITE,(keyX,pianoYPos,
                                 width,height))
                #Outline the key. 
                pygame.draw.rect(screen,Colors.BLACK,(keyX,pianoYPos,
                                 width,height),1)
            elif key == "Black":
               pygame.draw.rect(screen,Colors.DOVE_GRAY, pygame.Rect(keyX,
                                pianoYPos,width,height))
            if self.keyOrder[i] in data.keyPressed:
                pygame.draw.rect(screen,Colors.LIGHT_BLUE,(keyX,pianoYPos,
                                                        width,height))
                pygame.draw.rect(screen,Colors.BLACK,(keyX,pianoYPos,
                                                      width,height),1)
        def drawLabel(self,screen,width,height,i,keyX):
            #Labels each key according to the keyboard key it is mapped to.
            letter = self.keyOrder[i]
            label = pygame.font.Font(None, 35)
            TextSurf, TextRect = createTextSurface(letter,label,(0,0,0))
            TextRect.center = (keyX+width//2,pianoYPos+height-10)
            screen.blit(TextSurf,TextRect)
        def drawOctave(self,screen):
            octave = str(data.currOctave)
            label = pygame.font.Font(None, 80)
            textSurf, textRect = createTextSurface("Octave: " + octave,label,
                                                   Colors.WHITE)
            octaveY = 80
            textRect.center = (screenWidth//2,octaveY)
            screen.blit(textSurf,textRect)
        drawKey(self,screen,key,width,height,i,keyX)
        drawLabel(self,screen,width,height,i,keyX)
        drawOctave(self,screen)
    def drawButtons(self,screen):
        def drawBackAndRecordButtons(self,screen):
            screen.blit(self.backButton,(10,10))
            if data.record:
                recordImg = self.activerecord
            else:
                recordImg = self.record
            recordX, recordY = Virtual_Piano.recordX, Virtual_Piano.recordY
            screen.blit(recordImg,(recordX,recordY))
            #Label the record button.
            text = "Record"
            font = pygame.font.Font(None,25)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            recordLeft = Virtual_Piano.recordX
            recordRight = recordLeft + self.record.get_width()
            recordTop = Virtual_Piano.recordY
            recordBottom = recordTop + self.record.get_height()
            textRect.center = ((recordRight+recordLeft)//2,recordBottom+20)
            screen.blit(textSurf,textRect)
        def drawHelpButton(self,screen):
            helpX, helpY = Main_Screen.helpX, Main_Screen.helpY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            pygame.draw.rect(screen,Colors.DIM_GRAY,pygame.Rect(helpX,
                             helpY,width,height))
            text = "Help"
            font = pygame.font.Font(None,25)
            textSurf,textRect = createTextSurface(text,font,Colors.WHITE)
            textRect.center = (helpX + (width//2),(helpY+(height//2)))
            screen.blit(textSurf,textRect)
        drawBackAndRecordButtons(self,screen)
        drawHelpButton(self,screen)
    def drawAllKeyNames(self,screen,x,y):
        #Displays on the bottom of screen all the keys currently being played.
        text = ",".join(sorted(data.pianoKeyNames))
        font = pygame.font.Font(None, 80)
        textSurf, textRect = createTextSurface(text,font,Colors.WHITE)
        keyY = y-30
        textRect.center = (x//2,keyY)
        screen.blit(textSurf,textRect) 
    def buttonsSelected(self,x,y,timeScrubber):
        def helpSelected(self,x,y):
            helpX, helpY = Main_Screen.helpX, Main_Screen.helpY
            width, height = Main_Screen.exportWidth, Main_Screen.exportHeight
            if helpX < x < helpX + width and helpY < y < helpY + height:
                data.help = True
        def recordSelected(self,x,y):
            recordLeft = Virtual_Piano.recordX
            recordRight = recordLeft + self.record.get_width()
            recordTop = Virtual_Piano.recordY
            recordBottom = recordTop + self.record.get_height()
            if (recordLeft <= x <= recordRight and recordTop <= y <= 
                recordBottom):
                data.record = not(data.record)
        def backSelected(self,x,y):
            backLeft = 10
            backRight = backLeft + self.backButton.get_width()
            backTop = backLeft
            backBottom = backTop + self.backButton.get_height()
            if backLeft <= x <= backRight and backTop <= y <= backBottom:
                data.mode = "Main Screen"
                data.record = False
                data.stop = False
                data.play = False
                timeScrubber.reset()
                #If the user recorded something and pressed back, end recording
                if data.currNotesRecorded != []:
                    endRecording(timeScrubber)
        recordSelected(self,x,y)
        helpSelected(self,x,y)
        backSelected(self,x,y)
    def pianoKeyPressed(self,event):
        maxOctave, minOctave = 4,2
        key = pygame.key.name(event.key).upper()
        if event.type == pygame.KEYDOWN:
            #Check if user pressed a valid key that is not already pressed
            if key in self.keyOrder and key not in data.keyPressed:
                data.keyPressed.append(key)
                index = self.keyOrder.index(key)
                pianoKey = self.instrumentKeyOrder[index]
                data.pianoKeyNames.append(pianoKey + str(data.currOctave))
            elif key == "LEFT" and data.currOctave != minOctave:
                data.currOctave -= 1
                data.keyPressed,data.pianoKeyNames = [],[]
            elif key == "RIGHT" and data.currOctave != maxOctave:
                data.currOctave += 1
                data.keyPressed,data.pianoKeyNames = [],[]
        else:
            if key in data.keyPressed:
                pianoKey = self.instrumentKeyOrder[self.keyOrder.index(key)]
                data.keyPressed.remove(key)
                data.pianoKeyNames.remove(pianoKey + str(data.currOctave))

class Drums(Virtual_Piano):
    #Because the names of the notes are different from drums
    def __init__(self):
        self.drumKeyOrder = ["Kick","Rimshot","Snare","LowTom","MidTom",
                                   "HiTom","OpenHH","ClosedHH","PedalHH",
                                   "Extra","Ride","Cymbal"]
        super().__init__()
    def drumsKeyPressed(self,event):
        maxOctave, minOctave = 4,2
        key = pygame.key.name(event.key).upper()
        if event.type == pygame.KEYDOWN:
            if key in self.keyOrder and key not in data.keyPressed:
                data.keyPressed.append(key)
                index = self.keyOrder.index(key)
                pianoKey = self.drumKeyOrder[index]
                data.pianoKeyNames.append(pianoKey + str(data.currOctave-1))
            elif key == "LEFT" and data.currOctave != minOctave:
                data.currOctave -= 1
                data.keyPressed,data.pianoKeyNames = [],[]
            elif key == "RIGHT" and data.currOctave != maxOctave:
                data.currOctave += 1
                data.keyPressed,data.pianoKeyNames = [],[]
        else:
            if key in data.keyPressed:
                pianoKey = self.drumKeyOrder[self.keyOrder.index(key)]
                data.keyPressed.remove(key)
                data.pianoKeyNames.remove(pianoKey + str(data.currOctave-1))

#Taken from https://pythonprogramming.net/displaying-text-pygame-screen/
def createTextSurface(text, font,color): 
    #Renders text and returns the dimensions of the rectangle for text.
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect() 

class TimeScrubber(object):
    def __init__(self,width,height):
        self.screenWidth = width
        self.x = 280
        self.screenHeight = height
        self.y = 160
        self.barWidth = 40
    def reset(self):
        self.x = 280
        self.y = 160
    def move(self,scroller,speed):
        if data.play:
            self.x += speed
            if self.x >= self.screenWidth:
                barCount = 4
                change = barCount*self.barWidth #Move an entire bar over
                if data.scrollOffset < barCount*self.screenWidth - change:
                    scroller.scrollerX += self.barWidth
                    data.scrollOffset += change
                    self.x -= change
                else:
                    self.x = self.screenWidth
        elif data.stop:
            self.x = 280
        elif not(data.play) and not(data.stop):
            #If user pauses, snap scrubber to nearest 1/4th bar.
            self.x = (roundHalfUp(self.x/self.barWidth))*self.barWidth
    def draw(self,screen):
        bottomY = 720
        pygame.draw.line(screen,Colors.WHITE,(self.x,self.y),
                        (self.x,bottomY))

class EditingScreenTimeScrubber(TimeScrubber):
    #Editing scrubber has different pos & dimension from main screen one. 
    def __init__(self,width,height):
        super().__init__(width,height)
        self.y = 80
    def reset(self):
        self.x = 280
        self.y = 80
    def draw(self,screen):
        bottomY = 730
        pygame.draw.line(screen,Colors.WHITE,(self.x,self.y),(self.x,
                         bottomY))

def keyPressed(event,piano,drums,width,height):
    def helpKeyPressed(event,width,height):
        if data.mode == "Main Screen":
            mainHelp = MainHelp(width,height)
            mainHelp.keyPressed(event)
        elif data.mode == "Editing Screen":
            editingHelp = EditingHelp(width,height)
            editingHelp.keyPressed(event)
        else:
            virtualPianoHelp = VirtualPianoHelp(width,height)
            virtualPianoHelp.keyPressed(event)
    if data.help == True:
        helpKeyPressed(event,width,height)
    else:
        if data.mode == "Virtual Piano":
            if data.instrumentSelected != "Drums":
                piano.pianoKeyPressed(event)
            else:
                drums.drumsKeyPressed(event)

def mousePressed(event,piano,mainScreen,editingScreen,scroller,timeScrubber,
                 width,height,editingTimeScrubber):
    x,y = event.pos
    if not(data.help):
        if data.mode == "Main Screen":
            mainScreen.selected(x,y,timeScrubber)
            scroller.selectScroller(x,y)
        elif data.mode == "Virtual Piano":
            piano.buttonsSelected(x,y,timeScrubber)
        elif data.mode == "Editing Screen":
            editingScreen.selected(x,y,editingTimeScrubber)
            scroller.selectScroller(x,y)
        elif data.mode == "Start Screen":
            startScreen = StartScreen(width,height)
            startScreen.selected(x,y)
        #If the user pressed stop/changed from main screen to editing screen, 
        #reset position of scroller
        if data.scrollOffset == 0:
            scroller.scrollerX = 0

def drawHelp(screen,width,height): #Calls the appropriate help screen.
    if data.mode == "Main Screen":
        mainHelp = MainHelp(width,height)
        mainHelp.draw(screen)
    elif data.mode == "Editing Screen":
        editingHelp = EditingHelp(width,height)
        editingHelp.draw(screen)
    else:
        virtualPianoHelp = VirtualPianoHelp(width,height)
        virtualPianoHelp.draw(screen)

def redrawAll(screen,piano,mainScreen,timeScrubber,editingScreen,
    editingTimeScrubber,scroller,width,height):
    def drawBackground(screen,width,height):
        #Help screen and virtual piano screen has slightly lighter background.
        if data.help or data.mode == "Virtual Piano":
            pygame.draw.rect(screen,(50,50,50),pygame.Rect(0,0,width,height))
        elif data.mode == "Start Screen":
            return 
        else:
            pygame.draw.rect(screen,(20,20,20),pygame.Rect(0,0,width,height))
    drawBackground(screen,width,height)
    if data.help:
        drawHelp(screen,width,height)
    else:
        if data.mode == "Virtual Piano":
            piano.drawPiano(screen)
            piano.drawButtons(screen)
            piano.drawAllKeyNames(screen,width,height)
        elif data.mode == "Main Screen":
            mainScreen.draw(screen)
            timeScrubber.draw(screen)
            scroller.draw(screen)
        elif data.mode == "Editing Screen":
            editingScreen.draw(screen)
            editingTimeScrubber.draw(screen)
            scroller.draw(screen)
        elif data.mode == "Start Screen":
            startScreen = StartScreen(width,height)
            startScreen.draw(screen)

def timerFired(timeScrubber,editingTimeScrubber,scroller,SCREEN_WIDTH):
    def record():
        data.play = True
        barWidth = 40
        timeScrubber.move(scroller,2) #Simulate the timeScrubber moving.
        #If the scrubber is within 1 of the barWidth and that position doesn't 
        #already have notes, add the notes played.
        if (roundHalfUp(timeScrubber.x) % barWidth <= 1 and 
            (roundHalfUp(timeScrubber.x/barWidth))*barWidth not in 
            data.currPosRecorded):
            x = copy.deepcopy(data.pianoKeyNames)
            timeScrubberLoc = (roundHalfUp(timeScrubber.x/barWidth))*barWidth
            data.currNotesRecorded.append((x))
            data.currPosRecorded.append(timeScrubberLoc)
    if not(data.help):
        if data.mode == "Main Screen":
            timeScrubber.move(scroller,2)
            data.masterTimeScrubberX = timeScrubber.x
            time.sleep(0.02)
        elif data.mode == "Editing Screen":
            editingTimeScrubber.move(scroller,2)
            data.masterTimeScrubberX = editingTimeScrubber.x
        elif data.mode == "Virtual Piano":
            if data.record == True:
                record()
            else:
                endRecording(timeScrubber)

def endRecording(timeScrubber): 
    #Add the recorded notes and update and reset accordingly.
    data.stop = True
    data.play = False
    timeScrubber.reset()
    if (data.currNotesRecorded != [] and data.currNotesRecorded not in
        data.totalNotesRecorded):
        if False in data.tracksFilled: #If the track is empty
            index = data.tracksFilled.index(False)
            data.trackSelected = index
            data.trackNames.append(data.instrumentSelected)
        data.totalNotesRecorded.append(data.currNotesRecorded)
        data.totalPosRecorded.append(
                                        data.currPosRecorded)
        data.tracksFilled[data.trackSelected] = True
        data.instrumentSelected = ""

#Modified from http://openbookproject.net/thinkcs/python/english3e/pygame.html
def main():
    def createLabels():
        data.pianoLabels = createLabelsDict(SCREEN_HEIGHT,"Piano")  
        data.drumLabels = createLabelsDict(SCREEN_HEIGHT,"Drums") 
    def eventActions():
        if event.type == pygame.QUIT:   
            data.exit = True
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keyPressed(event,piano,drums,SCREEN_WIDTH,SCREEN_HEIGHT)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed(event,piano,mainScreen,editingScreen,scroller,
                         timeScrubber,SCREEN_WIDTH,SCREEN_HEIGHT,
                         editingTimeScrubber)
        elif event.type == pygame.MOUSEBUTTONUP:
            data.trackDrag = data.scrollDrag = False
            data.trackOffset = 0
        elif event.type == pygame.MOUSEMOTION and (data.trackDrag or 
                                                   data.scrollDrag):
            x,y = pygame.mouse.get_pos()
            if data.trackDrag:  
                mainScreen.moveTrack(x,y)
            else:               
                scroller.moveScroller(x,y)
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1400,800                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    piano = Virtual_Piano()
    drums = Drums()
    mainScreen = Main_Screen(SCREEN_WIDTH,SCREEN_HEIGHT)
    timeScrubber = TimeScrubber(SCREEN_WIDTH,SCREEN_HEIGHT)
    editingTimeScrubber = EditingScreenTimeScrubber(SCREEN_WIDTH,SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    editingScreen = Editing_Screen(SCREEN_WIDTH,SCREEN_HEIGHT)
    createLabels()
    scroller = Scroller(SCREEN_WIDTH)
    while not data.exit:
        for event in pygame.event.get():
            eventActions()
        redrawAll(screen,piano,mainScreen,timeScrubber,editingScreen,
                  editingTimeScrubber,scroller,SCREEN_WIDTH,SCREEN_HEIGHT)
        clock.tick(40) #Limits the program at max 40 frames per second
        timerFired(timeScrubber,editingTimeScrubber,scroller,SCREEN_WIDTH)
        pygame.display.flip()
    pygame.quit()

#####################################
#Audio
#####################################

def playAudio():
    while not data.exit:
        if data.mode == "Virtual Piano" and data.pianoKeyNames != []:
            playPianoSounds()
        elif data.play and data.totalNotesRecorded != [] and (data.mode != 
            "Virtual Piano"):
            if data.mode == "Main Screen":
                mainPlaybackAudio()
            elif data.mode == "Editing Screen":
                editingPlaybackAudio()
        else:
            time.sleep(0.01) #If no audio playing, wait for a little, so the 
            #while loop doesn't constantly run doing nothing.

#Piano samples converted from aiff to wav from 
#http://theremin.music.uiowa.edu/MISpiano.html
#Drum samples taken from XLN Audio's Addictive Drums 2 library and 
#converted from midi to wav in Studio One.
#Guitar samples taken from AAS's Strum GS-2 library and converted 
#from midi to wav in Studio One.

def playPianoSounds():
    instrument = data.instrumentSelected
    if len(data.pianoKeyNames) >= 1:
        combinedSound = None
        for pianoKey in data.pianoKeyNames:
            filename = pianoKey+".wav"
            sound = AudioSegment.from_file(instrument + "/" + filename)
            if combinedSound == None:
                combinedSound = sound
            else:
                #Overlay all of the pressed notes together.
                combinedSound = combinedSound.overlay(sound)
        if combinedSound != None:   
            play(combinedSound)
        else:
            time.sleep(0.01) #If nothing played, wait to save CPU power again.
    else:
        time.sleep(0.01)

def editingPlaybackAudio():
    def combineSound(combinedSound):
        if len(notes) >= 1:
            for note in notes:
                sound = AudioSegment.from_file(instrument + "/" + note + ".wav")
                if combinedSound == None:   
                    combinedSound = sound
                else:       
                    combinedSound = combinedSound.overlay(sound)
        return combinedSound
    barWidth = Main_Screen.barWidth
    instrument = data.trackNames[data.trackSelected]
    timeScrubberLoc = ((roundHalfUp(data.masterTimeScrubberX/barWidth))
                        *barWidth +  data.scrollOffset)
    toleranceRange = 10 #Range to compensate between latency between 
                        #animations and playing audio.
    if (roundHalfUp(data.masterTimeScrubberX) % barWidth <= toleranceRange and 
        timeScrubberLoc in data.currPosRecorded):
        index = data.currPosRecorded.index(timeScrubberLoc)
        notes = data.currNotesRecorded[index]
        combinedSound = None
        combinedSound = combineSound(combinedSound)
        if combinedSound != None:       
            play(combinedSound)
        else:       
            time.sleep(0.01)
    else:           
        time.sleep(0.01)

def consolidateTracks(): #Combines all of the notes and positions across tracks.
    consolidatedNotesRecorded = []
    consolidatedPosRecorded= []
    consolidatedInstruments = []
    for i,trackNotesRecorded in enumerate(data.totalNotesRecorded):
        PosRecorded= data.totalPosRecorded[i]
        instrument = data.trackNames[i]
        for index,notesRecorded in enumerate(trackNotesRecorded):
            consolidatedInstruments.append(instrument)
            consolidatedNotesRecorded.append(notesRecorded)
            consolidatedPosRecorded.append(PosRecorded[index])
    return (consolidatedNotesRecorded,consolidatedPosRecorded,
           consolidatedInstruments)
    
def mainPlaybackAudio():
    def combineSound(combinedSound):
        if len(notes) >= 1:
            for note in notes:
                sound = AudioSegment.from_file(instruments[i] + "/" + note + 
                                               ".wav")
                if combinedSound == None:   
                    combinedSound = sound
                else:   
                    combinedSound = combinedSound.overlay(sound) 
            return combinedSound
    barWidth = Main_Screen.barWidth
    timeScrubberLoc = ((roundHalfUp(data.masterTimeScrubberX/barWidth))
                        *barWidth + data.scrollOffset)
    notesRecorded,posRecorded,instruments = consolidateTracks()
    combinedSound = None
    toleranceRange = 10
    if (roundHalfUp(data.masterTimeScrubberX) % barWidth <= toleranceRange and 
        timeScrubberLoc in posRecorded):
        for i,times in enumerate(posRecorded):
            if times == timeScrubberLoc:
                index = posRecorded.index(timeScrubberLoc,i)
                notes = notesRecorded[index]     
                combinedSound = combineSound(combinedSound)
        if combinedSound != None:   
            play(combinedSound)
        else:   
            time.sleep(0.01)
    else:       
        time.sleep(0.01)      

def exportRecording():
    def createFile(): #Allows for as many exports as user wishes.
        #If Song1.mp3 already exists, make a Song2.mp3 and so on. 
        label = 1
        while os.path.exists("Song" + str(label) + ".mp3"):
            label += 1
        exportedSound.export("Exported Songs" + "/" + 
                             "Song" + str(label) + ".mp3",format = "mp3")
    def combineSound(combinedSound):
        if len(notes) >= 1:
            for note in notes: 
                sound = AudioSegment.from_file(instruments[i] + "/" 
                                               + note + ".wav")
                if combinedSound == None:   
                    combinedSound = sound
                else:
                    combinedSound = combinedSound.overlay(sound)
        return combinedSound
    notesRecorded,PosRecorded,instruments = consolidateTracks()
    startTime,increment = Main_Screen.timelineX, Main_Screen.barWidth
    currTime, endTime = startTime,max(PosRecorded) + increment
    exportedSound = None
    while currTime != endTime:
        combinedSound = None
        if currTime in PosRecorded:
            for i,time in enumerate(PosRecorded):
                if time == currTime:
                    index = PosRecorded.index(time,i)
                    notes = notesRecorded[index]
                    combinedSound = combineSound(combinedSound)
        if combinedSound == None:
            combinedSound = AudioSegment.from_file("Silence.wav")
        if exportedSound == None:   exportedSound = combinedSound
        else:
            exportedSound += combinedSound
            currTime += increment
    createFile()

#####################################
#RunProgram
#####################################

#Modified from hw1.py file from https://www.cs.cmu.edu/~112/notes/hw1.html
if __name__ == "__main__":
    #testAll()
    t1 = threading.Thread(target=playAudio,args=())
    t1.start()
    main()