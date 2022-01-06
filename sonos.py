#!/usr/bin/python
# encoding: utf-8

import sys
import argparse
from workflow import Workflow3 as Workflow
import os

log = None    

def main(wf):
    import soco

    # build arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)
    #fetch sonos speakers

    interface = os.getenv('interface_address')
    multi_household_env = os.getenv('multi_household')
    
    multi_household = (len(multi_household_env) > 0)

    if (len(interface) > 0):
        speakers = soco.discover(interface_addr=interface)
    else:
        if (multi_household):
            speakers = soco.discovery.scan_network(multi_household=True)
        else:
            speakers = soco.discover()    

    query = args.query
    speakerName = query.partition(';')[0]
    commands = query.partition(';')[2]
    commandResponse = commands.split()
    speakerNameList = []

    try:
        for speaker in speakers:
            speakerNameList.append(speaker.player_name)
    except TypeError:
        pass

    if len(query.split()) >= 1:
        if (multi_household):
            device = soco.discovery.scan_network_get_by_name(speakerName, multi_household=True)
        else:
            device = soco.discovery.by_name(speakerName)
        try:
            if "plpau" in query:
                if device.get_current_transport_info()['current_transport_state'] == "PLAYING":
                    device.pause()
                    toggleTitle = "Paused"
                else:
                    device.play()
                    toggleTitle = 'Playing'
                wf.add_item(title=toggleTitle, icon='lib/icons/plpau.png')

            elif "play" in query:
                device.play()
                wf.add_item(title='Playing', icon='lib/icons/play.png')

            elif "pause" in query:
                device.pause()
                wf.add_item(title='Paused', icon='lib/icons/pause.png')

            elif "volume" in query:
                value = "..."
                if len(commandResponse) > 1:
                    value = commandResponse[1]
                volArg = speakerName + '; volpcg ' + value
                chVolArg = speakerName + '; chvol ' + value
                wf.add_item('Set Volume to ' + value, subtitle='Enter a number from 0 to 100', valid=True, 
                arg=volArg, icon='lib/icons/volume.png')
                wf.add_item('Change Volume by ' + value, subtitle='Adjust the volume up or down by a relative amount', 
                valid=True, arg=chVolArg, icon='lib/icons/volume.png')
                wf.add_item("Current Volume: " + str(device.volume), icon='lib/icons/volume.png')

            elif "volpcg" in query:
                device.volume = commandResponse[1]
                wf.add_item(title='Set Volume to ' + commandResponse[1], icon='lib/icons/volume.png')

            elif "chvol" in query:
                device.set_relative_volume(commandResponse[1])
                wf.add_item(title='Changed Volume by ' + commandResponse[1], icon='lib/icons/volume.png')


            elif "next" in query:
                device.next()
                wf.add_item(title='Selecting Next Song', icon='lib/icons/next.png')

            
            elif "previous" in query:
                device.previous()
                wf.add_item(title='Selecting Previous Song', icon='lib/icons/next.png')

            elif "queue" in query:
                queue = device.get_queue()
                if len(queue) == 0:
                    wf.add_item(title='Queue is empty', 
                    subtitle='You must start playback through the Sonos app to generate a queue', valid=False, icon='lib/icons/queue.png')
                else:
                    for song in queue:
                        queueNum = str(song.item_id).partition('/')[2]

                        try:
                            queueSongTitle = song.title + " - " + song.creator
                        except:
                            queueSongTitle = song.title

                        try:
                            queueSongSub = song.album
                        except:
                            queueSongSub = ""
                            
                        wf.add_item(title=queueSongTitle, subtitle=queueSongSub, valid=True, arg=speakerName + '; plque ' + str(queueNum))


            elif "plque" in query:
                device.play_from_queue(int(commandResponse[1]) - 1)
                wf.add_item(title="Played Item " + commandResponse[1] + " on the Queue", icon='lib/icons/queue.png')

                
            elif "linein" in query:
                device.switch_to_line_in()
                wf.add_item(title='Switched to Line-in', icon='lib/icons/linein.png')
                

            elif "plmode" in query:
                wf.add_item(title='Enable Shuffle', subtitle='Enable shuffle and disable repeat', valid=True, 
                arg=speakerName + '; enshuffle', icon='lib/icons/shuffle.png')
                wf.add_item(title='Disable Shuffle', subtitle='Disable shuffle and repeat', valid=True, 
                arg=speakerName + '; disshuffle', icon='lib/icons/noshuffle.png')
                wf.add_item(title='Enable Repeat', subtitle='Enable repeat and disable shuffle', valid=True, 
                arg=speakerName + '; enrepeat', icon='lib/icons/repeat.png')
                wf.add_item(title='Enable Shuffle/Repeat', subtitle='Enable shuffle and repeat', valid=True, 
                arg=speakerName + '; enshuffrep', icon='lib/icons/shuffrep.png')

                if (device.play_mode == "SHUFFLE_NOREPEAT"):
                    playModeTitle = "Shuffle, No Repeat"
                elif (device.play_mode == "NORMAL"):
                    playModeTitle = "No Shuffle, No Repeat"
                elif (device.play_mode == "REPEAT_ALL"):
                     playModeTitle = "No Shuffle, Repeat"
                else:
                    playModeTitle = "Shuffle, Repeat"

                wf.add_item("Current Mode: " + playModeTitle, icon='lib/icons/speaker.png')


            elif "enshuffle" in query:
                device.play_mode = 'SHUFFLE_NOREPEAT'
                wf.add_item(title='Enabled Shuffle, Disabled Repeat', icon='lib/icons/shuffle.png')

            elif "disshuffle" in query:
                device.play_mode = 'NORMAL'
                wf.add_item(title='Disabled Shuffle and Repeat', icon='lib/icons/noshuffle.png')

            elif "enrepeat" in query:
                device.play_mode = 'REPEAT_ALL'
                wf.add_item(title='Enabled Repeat, Disabled Shuffle', icon='lib/icons/next.png')
            
            elif "enshuffrep" in query:
                device.play_mode = 'SHUFFLE'
                wf.add_item(title='Enabled Shuffle and Repeat', icon='lib/icons/next.png')
    
        
            else:
                try:
                    if (device.get_current_track_info()['album']):
                        currentTrackSub = device.get_current_track_info()['album'] + " / " + device.get_current_track_info()['duration']
                    elif (device.get_current_track_info()['duration'] and device.get_current_track_info()['duration'] != "NOT_IMPLEMENTED"):
                        currentTrackSub = device.get_current_track_info()['duration']
                    else:
                        currentTrackSub = ""

                    wf.add_item(title='Play/Pause', valid=True, arg=query + ' plpau', icon='lib/icons/plpau.png')
                    wf.add_item(title='Volume', valid=False, icon='lib/icons/volume.png', autocomplete=query + ' volume ')
                    wf.add_item(title='Next', valid=True, arg=query + ' next',icon='lib/icons/next.png')
                    wf.add_item(title='Previous', valid=True, arg=query + ' previous', icon='lib/icons/prev.png')
                    wf.add_item(title='Queue', valid=False, autocomplete=query + ' queue ', icon='lib/icons/queue.png')
                    wf.add_item(title='Play Mode', valid=False, autocomplete=query + ' plmode ', icon='lib/icons/shuffle.png')

                    if (not device.is_playing_line_in):
                        wf.add_item(title='Switch to Line-in', valid=True, arg=query + ' linein',icon='lib/icons/linein.png')

                    if (device.is_playing_line_in):
                        wf.add_item("Audio from Line-in Device", icon='lib/icons/nowplaying.png')
                    else:
                        wf.add_item("Current Track: " + device.get_current_track_info()['title'] + " - " + device.get_current_track_info()['artist'], 
                        subtitle=currentTrackSub, icon='lib/icons/nowplaying.png')

                   
                    wf.add_item("Status: " + device.get_current_transport_info()['current_transport_state'], icon='lib/icons/speaker.png')
                except AttributeError:
                    items = wf.filter(query, speakerNameList)

                    if not items:
                        wf.add_item(title='No Matches', icon='lib/icons/error.png', 
                        subtitle="Please enter your speaker name as it appears on the Sonos app")
                        wf.add_item(title='View all Speakers', autocomplete="", icon='lib/icons/speaker.png')
                    
                    for speaker in items:
                        wf.add_item(title=speaker, subtitle="Press enter to select",
                        autocomplete=speaker + ';', valid=False, icon='lib/icons/speaker.png') 
        except AttributeError:
            wf.add_item(title='Missing Speaker', subtitle='Please precede this command with the speaker name followed by a semicolon (ex. soco Bedroom;)',
            icon='lib/icons/error.png', autocomplete="")


    else:
        try:
            for speaker in speakers:
                wf.add_item(title=speaker.player_name, 
                subtitle=speaker.ip_address, autocomplete=speaker.player_name + ';', valid=False, uid=speaker.player_name, icon='lib/icons/speaker.png')
        except TypeError:
            wf.add_item('No Sonos Speakers Found', subtitle="Try disabling any VPNs and setting the interface_address environment variable to local IP if problem persists",
              icon='lib/icons/error.png')


    wf.send_feedback()

if __name__ == u"__main__":
     wf = Workflow(libraries=['./lib'], update_settings={'github_slug' :'karimkaylani/alfred-sonoscontroller', 'frequency' : 1})
     log = wf.logger
     sys.exit(wf.run(main)) 

if wf.update_available:
    wf.start_update()