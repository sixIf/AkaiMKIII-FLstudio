# name=CustomMk3ArmRecording
import transport 
from itertools import chain
import midi 
import ui 
import playlist
import transport
import channels
import arrangement
import general
import launchMapPages
import screen
import plugins
import time
import device
import mixer
import math
import general
import plugins
import patterns
from midi import *
import utils

class AkaiProgram():
    
    def __init__(self, CCPad, ProgPad, Knobs):
        self.CCPad = CCPad[0:16]
        self.ProgPad = ProgPad[0:16]
        self.Knobs = Knobs

    def disarmAllTracks(self):
        print('Disarm Tracks')
        trackNo = mixer.trackCount()
        for track in range(trackNo):
            if mixer.isTrackArmed(track):
                mixer.armTrack(track)

    def handleEvent(self, event):
        if event.data1 in self.Knobs and event.data2 > -1:
            self.handleKnobs(event)        
        if (event.midiId == midi.MIDI_CONTROLCHANGE):
            if event.data1 in self.CCPad[0:8] and event.data2 < 1:
                self.handleCCPadBankOne(event)
            elif event.data1 in self.CCPad[-8:] and event.data2 < 1:
                self.handleCCPadBankTwo(event)
        elif (event.midiId == midi.MIDI_PROGRAMCHANGE):
            if event.data1 in self.ProgPad[0:8] and event.data2 < 1:
                self.handleProgPadBankOne(event)
            elif event.data1 in self.ProgPad[-8:] and event.data2 < 1:
                self.handleProgPadBankTwo(event)

    def handleKnobs(self, event):
        print('unassigned')

    def handleJoystick(self, event):
        print('unassigned')

    def handleCCPadBankTwo(self, event):
        print('unassigned')

    def handleCCPadBankOne(self, event):
        print('unassigned')

    def handleProgPadBankTwo(self, event):
        print('unassigned')

    def handleProgPadBankOne(self, event):
        print('unassigned')
    
class LiveLoop(AkaiProgram):
    '''
        *******PADS*******
        
        CCPad_Bank_1:       
                            (PAD 1) - Arm Record Mixer Channel 1
                            (PAD 2) - Arm Record Mixer Channel 2
                            (PAD 3) - Arm Record Mixer Channel 3
                            (PAD 4) - Arm Record Mixer Channel 4
                            (PAD 5) - Pattern / Song mode
                            (PAD 6) - Play
                            (PAD 7) - Stop
                            (PAD 8) - Record

        
        CCPad_Bank_2:       
                            (PAD 1) - Pattern 1
                            (PAD 2) - Pattern 2
                            (PAD 3) - Pattern 3
                            (PAD 4) - Pattern 4                            
                            (PAD 5) - Channel Rack Instr 1
                            (PAD 6) - Channel Rack Instr 2
                            (PAD 7) - Channel Rack Instr 3
                            (PAD 8) - Channel Rack Instr 4

        Knobs:    
                            (Knob 1) - Mixer 1 Volume
                            (Knob 2) - Mixer 2 Volume
                            (Knob 3) - Mixer 3 Volume
                            (Knob 4) - Mixer 4 Volume                          
                            (Knob 5) - Unassigned
                            (Knob 6) - Unassigned
                            (Knob 7) - Unassigned
                            (Knob 8) - Unassigned                           
    '''    
    def __init__(self, CCPad_Bank, ProgPad_Bank, Knobs):
        AkaiProgram.__init__(self, CCPad_Bank, ProgPad_Bank, Knobs)

    def handleKnobs(self, event):
        print('Handle Knobs')
        Knobs_top = self.Knobs[0:4]
        Knobs_bottom = self.Knobs[-4:]        
        if event.data1 in Knobs_top:
            mixerIndex = Knobs_top.index(event.data1) + 1                
            increment = 0.01 if event.data2 < 10 else -0.01 # When we set knobs to 'relative' in Akai Editor, the values are between 1-4 when increasing, between 123-127 when decreasing   
            mixer.setTrackVolume((mixerIndex),mixer.getTrackVolume(mixerIndex) + increment)
        elif event.data1 in Knobs_bottom:
            print('unassigned knob')

    def handleJoystick():
        print('unassigned joystick')

    def handleCCPadBankTwo(self, event):
        print('handleCCPadBankTwo')
        CCPad_Bank_2 = self.CCPad[-8:]
        CCPad_Bank_2_top = CCPad_Bank_2[0:4]
        CCPad_Bank_2_bottom = CCPad_Bank_2[-4:]    
        if event.data1 in CCPad_Bank_2_bottom:
            patternIndex = CCPad_Bank_2_bottom.index(event.data1) + 1
            patterns.jumpToPattern(patternIndex)
        elif event.data1 in CCPad_Bank_2_top:
            channelIndex = CCPad_Bank_2_top.index(event.data1)
            channels.selectOneChannel(channelIndex)

    def handleCCPadBankOne(self, event):
        print('handleCCPadBankOne')
        CCPad_Bank_1 = self.CCPad[0:8]
        CCPad_Bank_1_top = CCPad_Bank_1[0:4]
        CCPad_Bank_1_bottom = CCPad_Bank_1[-4:]
        
        if event.data1 in CCPad_Bank_1_top:
            padTriggered = CCPad_Bank_1_top.index(event.data1)
            print("padTriggered: ", padTriggered)
            if padTriggered == 0:
                transport.setLoopMode()
            elif padTriggered == 1:
                transport.start()
            elif padTriggered == 2:
                transport.stop()
            elif padTriggered == 3:
                transport.record()
        elif event.data1 in CCPad_Bank_1_bottom:
            mixerIndex = CCPad_Bank_1_bottom.index(event.data1) + 1
            if mixer.isTrackArmed(mixerIndex):
                self.disarmAllTracks()
            else:
                self.disarmAllTracks()
                mixer.armTrack(mixerIndex)


# Init Akai programs

LiveLoop_CCPad = list(range(30,46))
liveLoop_ProgPad = list(range(0,16))
liveLoop_Knobs = range(79,87)
liveLoop = LiveLoop(LiveLoop_CCPad, liveLoop_ProgPad, liveLoop_Knobs)

# FL studio Events
def actualPluginName():
    plugins.getPluginName(channels.channelNumber())
    return actualPluginName

def OnInit():
	print('Akai MPK Mini Script by Skeul \nYour Device port number is:', device.getPortNumber())
	port = device.getPortNumber()
	print('MIDI Device name:', device.getName())

def OnMidiMsg(event):      
    event.handled = False 
    print('MidiId: ', event.midiId, 'EventData1: ', event.data1, 'EventData2: ', event.data2, ' eventMidiChan', event.midiChan, 'controlchange midi: ', midi.MIDI_CONTROLCHANGE, ' prog midi: ', midi.MIDI_PROGRAMCHANGE) 
    if event.midiChan == 10: # LiveLoop program
        liveLoop.handleEvent(event)
        event.handled = True
