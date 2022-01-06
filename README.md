# Alfred Sonos Controller

> Control playback of your Sonos speakers straight from Alfred!

[![INSERT YOUR GRAPHIC HERE](https://i.imgur.com/r5QBNKI.jpg)]()

## Installation

<a href="https://github.com/karimkaylani/alfred-sonoscontroller/releases/latest/download/sonoscontroller.alfredworkflow" target="_blank">Download</a>

- Download and open the alfredworkflow file to install the workflow

## Features 

- Play, Pause, Next, Previous
- Set/Change Volume
- View Queue
- Play Songs from Queue (only tested on Spotify playing through Sonos app)
- Switch to line-in playback (if supported on device)
- Control Shuffle/Repeat

## Usage

Type <code>soco</code> into Alfred, select or search your device, and then control it on the following screen

[![INSERT YOUR GRAPHIC HERE](http://g.recordit.co/7jTaMJQSPE.gif)]()


## Hotkeys

Hotkeys are added by adding a hotkey trigger on the workflow flowchart (open Alfred Preferences -> Workflows -> Sonos Controller, then right click in the empty space -> Triggers -> Hotkey) and connecting it to the run script block with a text argument that follows the following syntax. You can also edit the preset hotkey triggers by right clicking them and selecting configure object.

<code>(sonosName); (command)</code>

ex:

<code>Bedroom; next</code>

[![INSERT YOUR GRAPHIC HERE](https://i.imgur.com/R94Vye3.jpg)]()

[![INSERT YOUR GRAPHIC HERE](https://i.imgur.com/s0IHQoZ.jpg)]()

 Commands:

 <code>plpau</code> - Play/Pause Sonos device

<code>play</code> - Play Sonos device

<code>pause</code> - Pause Sonos device

<code>volpcg [value]</code> - Set volume to specified value (ex. <code>Bedroom; volpcg 50</code>)

<code>chvol [value]</code> - Change volume by a specified value

<code>next</code> - Go to the next song

<code>previous</code> - Go to the previous song

<code>linein</code> - Switch playback to line-in

<code>enshuffle</code> - Enable shuffle and disable repeat

<code>disshuffle</code> - Disable shuffle and disable repeat

<code>enrepeat</code> - Enable repeat and disable shuffle

<code>enshuffrep</code> - Enable shuffle and repeat

<code>plque [position in queue]</code> - Play a song in a certain position in queue (only tested on Spotify playing through Sonos app)

## Troubleshooting

If you find yourself getting the <code>No Speakers Found</code> error, it may be due to an incorrect interface address. This can be caused by having a VPN active, which unfortunatley Sonos does not support.

If you are still recieving this error, you can try manually setting the interface address to your local IP address on your machine (which can be found under your Network settings) by doing the following:

1. Open Alfred Preferences -> Workflows -> SonosController and press the [x] button in the top right corner

    This screen should appear:

    [![INSERT YOUR GRAPHIC HERE](https://i.imgur.com/sl3eily.jpg)]()

2. Double click under the value column on interface_address and enter in the address of your local IP

If you have multiple households on your network (or if you have a split S1 / S2 system), got to the Workflows setting (as described above) and set the value for "multi_household" to "true".

## Acknowledgements

This workflow was built using [deanishe's Alfred-Workflow](http://www.deanishe.net/alfred-workflow/)

Huge shoutout to the team behind [SoCo](http://python-soco.com/) which this workflow uses heavily

Multi Household support added by Clancy Childs

---

## License
This workflow is released under the [MIT license](http://opensource.org/licenses/mit-license.php)
