# Alfred Sonos Controller

> Control playback of your Sonos speakers straight from Alfred!

[![INSERT YOUR GRAPHIC HERE](https://i.imgur.com/r8UZWT7.jpg)]()

## Installation

<a href="https://github.com/karimkaylani/alfred-sonoscontroller/releases/latest/download/sonoscontroller.alfredworkflow" target="_blank">Download</a>

- Download and open the alfredworkflow file to install the workflow

## Features 

- Play, Pause, Next, Previous
- Set/Change Volume
- View Queue
- Play Songs from Queue (only tested on Spotify playing through Sonos app)
- Control Shuffle/Repeat

## Usage

Type <code>soco</code> into Alfred, select your device, and then control it on the following screen

[![INSERT YOUR GRAPHIC HERE](http://g.recordit.co/7jTaMJQSPE.gif)]()


## Hotkeys

Hotkeys are added by adding a hotkey trigger on the flowchart and connecting it to the run script block with a text argument that follows this syntax

<code>(sonosName); (command)</code>

ex:

<code>Bedroom; next</code>

[![INSERT YOUR GRAPHIC HERE](https://i.imgur.com/R94Vye3.jpg)]()

 Commands:

 <code>plpau</code> - Play/Pause Sonos device

<code>play</code> - Play Sonos device

<code>pause</code> - Pause Sonos device

<code>volpcg [value]</code> - Set volume to specified value (ex. <code>Bedroom; volpcg 50</code>)

<code>chvol [value]</code> - Change volume by a specified value

<code>next</code> - Go to the next song

<code>previous</code> - Go to the previous song

<code>enshuffle</code> - Enable shuffle and disable repeat

<code>disshuffle</code> - Disable shuffle and disable repeat

<code>enrepeat</code> - Enable repeat and disable shuffle

<code>enshuffrep</code> - Enable shuffle and repeat

<code>plque [position in queue]</code> - Play a song in a certain position in queue (only tested on Spotify playing through Sonos app)

## Acknowledgements

This workflow was built using [deanishe's Alfred-Workflow](http://www.deanishe.net/alfred-workflow/)

Huge shoutout to the team behind [SoCo](http://python-soco.com/) which this workflow uses heavily

---

## License
This workflow is released under the [MIT license](http://opensource.org/licenses/mit-license.php)
