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
    query = str(args.query)
    response = query.split()

    if len(response) >= 1:
        device = soco.discovery.by_name(response[0])

        if "play" in query:
            device.play()

        elif "pause" in query:
            device.pause()

        elif "volume" in query:
            value = "..."
            if len(response) > 2:
                value = response[2]
            volArg = response[0] + ' volpcg ' + value
            chVolArg = response[0] + ' chvol ' + value
            wf.add_item('Set Volume to ' + value, subtitle='Enter a number from 0 to 100', valid=True, 
            arg=volArg, icon='lib/icons/volume.png')
            wf.add_item('Change Volume by ' + value, subtitle='Adjust the volume up or down by a relative amount', 
            valid=True, arg=chVolArg, icon='lib/icons/volume.png')
            wf.add_item("Current Volume: " + str(device.volume), icon='lib/icons/volume.png')

        elif "volpcg" in query:
            device.volume = response[2]

        elif "chvol" in query:
            device.set_relative_volume(response[2])

        elif "next" in query:
            device.next()
        
        elif "previous" in query:
            device.previous()
        
        elif "queue" in query:
            queue = device.get_queue()
            for song in queue:
                queueNum = str(song.item_id).partition('/')[2]
                wf.add_item(title=song.title, valid=True, arg=response[0] + ' plque ' + str(queueNum))

        elif "plque" in query:
            device.play_from_queue(int(response[2]) - 1)

        elif "plmode" in query:
            wf.add_item(title='Enable Shuffle', subtitle='Enable shuffle and disable repeat', valid=True, 
            arg=response[0] + ' enshuffle', icon='lib/icons/shuffle.png')
            wf.add_item(title='Disable Shuffle', subtitle='Disable shuffle and repeat', valid=True, 
            arg=response[0] + ' disshuffle', icon='lib/icons/noshuffle.png')
            wf.add_item(title='Enable Repeat', subtitle='Enable repeat and disable shuffle', valid=True, 
            arg=response[0] + ' enrepeat', icon='lib/icons/repeat.png')
            wf.add_item(title='Enable Shuffle/Repeat', subtitle='Enable shuffle and repeat', valid=True, 
            arg=response[0] + ' enshuffrep', icon='lib/icons/shuffrep.png')

        elif "enshuffle" in query:
            device.play_mode = 'SHUFFLE_NOREPEAT'

        elif "disshuffle" in query:
            device.play_mode = 'NORMAL'

        elif "enrepeat" in query:
            device.play_mode = 'REPEAT_ALL'
        
        elif "enshuffrep" in query:
            device.play_mode = 'SHUFFLE'
        
        else:
            wf.add_item(title='Play', valid=True, arg=query + ' play', icon='lib/icons/play.png')
            wf.add_item(title='Pause', valid=True, arg=query + ' pause', icon='lib/icons/pause.png')
            wf.add_item(title='Volume', valid=False, icon='lib/icons/volume.png', autocomplete=query + ' volume ')
            wf.add_item(title='Next', valid=True, arg=query + ' next',icon='lib/icons/next.png')
            wf.add_item(title='Previous', valid=True, arg=query + ' previous', icon='lib/icons/prev.png')
            wf.add_item(title='Queue', valid=False, autocomplete=query + ' queue ', icon='lib/icons/queue.png')
            wf.add_item(title='Play Mode', valid=False, autocomplete=query + ' plmode ', icon='lib/icons/shuffle.png')
            wf.add_item("Current Track: " + device.get_current_track_info()['title'] + " - " + device.get_current_track_info()['artist'], 
            icon='lib/icons/nowplaying.png')
            wf.add_item("Status: " + device.get_current_transport_info()['current_transport_state'], icon='lib/icons/speaker.png')

    else:
        for speaker in speakers:
            wf.add_item(title=speaker.player_name, 
            subtitle=speaker.ip_address, autocomplete=speaker.player_name, valid=False, uid=speaker.player_name, icon='lib/icons/speaker.png')

    wf.send_feedback()

if __name__ == u"__main__":
     wf = Workflow(libraries=['./lib'], update_settings={'github_slug' :'karimkaylani/alfred-sonoscontroller', 'frequency' : 7})
     log = wf.logger
     sys.exit(wf.run(main)) 

if wf.update_available:
    wf.start_update()