#!/usr/bin/python
# encoding: utf-8

import sys
import argparse
from workflow import Workflow

log = None    

def main(wf):
    import soco

    # build arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)

    #fetch sonos speakers

    speakers = soco.discover()
    query = args.query
    speakerName = query.partition(';')[0]
    commands = query.partition(';')[2]
    commandResponse = commands.split()

    if len(query.split()) >= 1:
        device = soco.discovery.by_name(speakerName)

        if "plpau" in query:
            if device.get_current_transport_info()['current_transport_state'] == "PLAYING":
                device.pause()
            else:
                device.play()

        elif "play" in query:
            device.play()

        elif "pause" in query:
            device.pause()

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

        elif "chvol" in query:
            device.set_relative_volume(commandResponse[1])

        elif "next" in query:
            device.next()
        
        elif "previous" in query:
            device.previous()
        
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

        elif "plmode" in query:
            wf.add_item(title='Enable Shuffle', subtitle='Enable shuffle and disable repeat', valid=True, 
            arg=speakerName + '; enshuffle', icon='lib/icons/shuffle.png')
            wf.add_item(title='Disable Shuffle', subtitle='Disable shuffle and repeat', valid=True, 
            arg=speakerName + '; disshuffle', icon='lib/icons/noshuffle.png')
            wf.add_item(title='Enable Repeat', subtitle='Enable repeat and disable shuffle', valid=True, 
            arg=speakerName + '; enrepeat', icon='lib/icons/repeat.png')
            wf.add_item(title='Enable Shuffle/Repeat', subtitle='Enable shuffle and repeat', valid=True, 
            arg=speakerName + '; enshuffrep', icon='lib/icons/shuffrep.png')

        elif "enshuffle" in query:
            device.play_mode = 'SHUFFLE_NOREPEAT'

        elif "disshuffle" in query:
            device.play_mode = 'NORMAL'

        elif "enrepeat" in query:
            device.play_mode = 'REPEAT_ALL'
        
        elif "enshuffrep" in query:
            device.play_mode = 'SHUFFLE'
        
        else:
            wf.add_item(title='Play/Pause', valid=True, arg=query + ' plpau', icon='lib/icons/plpau.png')
            wf.add_item(title='Volume', valid=False, icon='lib/icons/volume.png', autocomplete=query + ' volume ')
            wf.add_item(title='Next', valid=True, arg=query + ' next',icon='lib/icons/next.png')
            wf.add_item(title='Previous', valid=True, arg=query + ' previous', icon='lib/icons/prev.png')
            wf.add_item(title='Queue', valid=False, autocomplete=query + ' queue ', icon='lib/icons/queue.png')
            wf.add_item(title='Play Mode', valid=False, autocomplete=query + ' plmode ', icon='lib/icons/shuffle.png')

            if (device.get_current_track_info()['album']):
                currentTrackSub = device.get_current_track_info()['album'] + " / " + device.get_current_track_info()['duration']
            else:
                currentTrackSub = device.get_current_track_info()['duration']

            wf.add_item("Current Track: " + device.get_current_track_info()['title'] + " - " + device.get_current_track_info()['artist'], 
            subtitle=currentTrackSub, icon='lib/icons/nowplaying.png')
            wf.add_item("Status: " + device.get_current_transport_info()['current_transport_state'], icon='lib/icons/speaker.png')

    else:
        for speaker in speakers:
            wf.add_item(title=speaker.player_name, 
            subtitle=speaker.ip_address, autocomplete=speaker.player_name + ';', valid=False, uid=speaker.player_name, icon='lib/icons/speaker.png')

    wf.send_feedback()

if __name__ == u"__main__":
     wf = Workflow(libraries=['./lib'], update_settings={'github_slug' :'karimkaylani/alfred-sonoscontroller', 'frequency' : 1})
     log = wf.logger
     sys.exit(wf.run(main)) 

if wf.update_available:
    wf.start_update()