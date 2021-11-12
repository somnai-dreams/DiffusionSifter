import PySimpleGUI as sg
from shutil import copyfile, move
from pathlib import Path
import os
from os import path
import json
import math
from collections import Counter


###########################################################
# Def Stuff
###########################################################

def checkMakePath(filepath):
    if path.exists(filepath) == False:
      os.makedirs(filepath)
    #   print(f'Made {filepath}')
    # else:
    #   print(f'filepath {filepath} exists.')

def archiveFile():
    move(image_100, image_processed_path)

def trashFile():
    move(image_100, image_trash_path)

def getStats():
    global p
    global t
    global t_pc
    historyStats = Counter(history.values())
    p = historyStats['100']+historyStats['75']+historyStats['50']+historyStats['25']
    t = historyStats['trash']
    t_pc = math.floor(t/(t+p)*100) if t > 0 else 0

def updateFiles(seed):
    global image_seed
    global image_100
    global image_75
    global image_50
    global image_25
    global image_output
    global window
    getStats()
    image_seed = seed
    image_100 = f'{image_100_path}/{image_seed}.png'
    image_75 = f'{image_75_path}/{image_seed}.png'
    image_50 = f'{image_50_path}/{image_seed}.png'
    image_25 = f'{image_25_path}/{image_seed}.png'
    image_output = f'{image_out_path}/{image_seed}.png'
    if 'window' in globals():
        window.Element('Progression').update(value=f'{i+1} / {len(existing)} Unprocessed')
        window.Element('Processed').update(value=f'{p} Saved')
        window.Element('Trashed').update(value=f'{t} Trashed ({t_pc}%)')
        window.Element('_100').update(image_filename=image_100)
        window.Element('_75').update(image_filename=image_75)
        window.Element('_50').update(image_filename=image_50)
        window.Element('_25').update(image_filename=image_25)

def saveHistory():
    with open(f'{image_out_path}/history.txt', mode='w+') as f:
        f.write(str(history))

def undoHistory():
    last_seed = list(history)[-1]
    last_action = history.pop(last_seed)
    if last_action == 'trash':
        move(f'{image_trash_path}/{last_seed}.png', f'{image_100_path}/{last_seed}.png')
    else:
        move(f'{image_processed_path}/{last_seed}.png', f'{image_100_path}/{last_seed}.png')
    existing.insert(i, last_seed)
    updateFiles(last_seed)
    saveHistory()

def processEvent(event_type):
    copyfile(eval(f'image_{event_type}'), image_output)
    history.update({image_seed: f'{event_type}'})
    saveHistory()
    archiveFile()
    del existing[i]
    updateFiles(existing[i])


###########################################################
#Set up folders & initial state
###########################################################

abs_root_path = '../Out/HighGuidance5000'

image_100_path = f'{abs_root_path}/100'
image_75_path = f'{abs_root_path}/75'
image_50_path = f'{abs_root_path}/50'
image_25_path = f'{abs_root_path}/25'

image_out_path = f'{abs_root_path}/curated'
checkMakePath(image_out_path)

image_processed_path = f'{image_100_path}/processed'
checkMakePath(image_processed_path)

image_trash_path = f'{image_100_path}/trash'
checkMakePath(image_trash_path)

#Check folder for files and add them to the list to process
existing = []
path,dirs,files = next(os.walk(image_100_path))
for filename in files:
    existing.append((os.path.join(path,filename).split('\\', 4)[1]).split('.',2)[0])

#Check for existing history
history = {}
try:
    with open(f'{image_out_path}/history.txt', mode='r+') as f:
        print('Loading History')
        history = eval(f.read()) #😬
except:
    print('No History')


# Init variables
image_seed = image_100 = image_75 = image_50 = image_25 = image_output = ''
i = p = t = t_pc = 0

#Check folder for files and add them to the list to process
updateFiles(existing[i])



###########################################################
# Build the layout
###########################################################

sg.theme_background_color('white')  # Remove a touch of color
# All the stuff inside your window.

layout = [
            [
                sg.Text(f'{i+1} / {len(existing)} Unprocessed', font = ("Courier New Bold", 14), text_color="black", background_color=(sg.theme_background_color()), key="Progression"),
                sg.Text(f'{p} Saved', font = ("Courier New Bold", 14), text_color="black", background_color=(sg.theme_background_color()), pad=(100, 0), key="Processed"),
                sg.Text(f'{t} Trashed ({t_pc}%)', font = ("Courier New Bold", 14), text_color="black", background_color=(sg.theme_background_color()), pad=(100, 0), key="Trashed"),
            ],
            [[
                sg.Button(image_filename=image_100, border_width=0, key="_100"), 
                sg.Button(image_filename=image_75, border_width=0, key="_75"),  
            ],
            [
                sg.Button(image_filename=image_50, border_width=0, key="_50"),
                sg.Button(image_filename=image_25, border_width=0, key="_25")
            ]],
            [
                sg.Button(image_filename='Trash.png', button_color=(sg.theme_background_color()), border_width=0, key="_delete"),
                sg.Button(image_filename='Prev.png', button_color=(sg.theme_background_color()), border_width=0, key="_prev"),
                sg.Button(image_filename='Next.png', button_color=(sg.theme_background_color()), border_width=0, key="_next")
            ]
        ]

# Create the Window
window = sg.Window('Diffusion Picker', layout, return_keyboard_events=True)



###########################################################
# Process events in the loop
###########################################################

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # Event for first image
    if event == '_100' or event == '1':
        processEvent(100)

    # Event for second image
    if event == '_75' or event == '2':
        processEvent(75)

    # Event for third image
    if event == '_50' or event == '3':
        processEvent(50)

    # Event for fourth image
    if event == '_25' or event == '0':
        processEvent(25)

    # Event for Next button
    if event == '_next' or event == 'Right:39' or event == 'd':
        if i == len(existing)-1:
            i = 0
        else:
            i += 1
        updateFiles(existing[i])

    # Event for Prev button
    if event == '_prev' or event == 'Left:37' or event == 'a':
        if i == 0:
            i = len(existing)-1
        else:
            i -= 1
        updateFiles(existing[i])

    # Event for Delete Button
    if event == '_delete' or event == 'BackSpace:8' or event == '.':
        history.update({image_seed: 'trash'})
        saveHistory()
        trashFile()
        del existing[i]
        updateFiles(existing[i])

    # Event for Undo
    if event == 'u':
        undoHistory()

    # Event for close window
    if event == sg.WIN_CLOSED: 
        break
    # print('You entered ', event)

window.close()
