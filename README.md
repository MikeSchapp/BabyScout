# BabyScout

Pico W projects that intefaces with BabyBuddy to record baby diaper changes, feedings, and sleep time with the push of a button. Push to start timers, and then push again to end them!

## Includes
* Code for Pico W
* STL and 3MF files for a custom enclosure

## Geting Started
1) Print out the enclosure that is detailed in the 3d folder. 
2) Fill in the secrets.json file in the firmware folder with the wifi information as well as an api key for BabyScout to use to access BabyBuddy.
    * Make sure to rename the placeholder folder to secrets.json
3) Upload the files and folders contained in the firmware folder.
4) Attach switches to the enclosure and wire them to the pico.
    * In my example I wired all of the switches to the 3.3v output of the pico, then an individual gpio pin per switch. I used 8 in my example, but feel free to add more switches and more functionality.
5) Close up th enclosure and attach to power.

## Known issues
* Currently The pico w is incapable of communicating via cloudfront tunnels. (Appears to be some bug with running out of memory)

## TODO
* Create script to automatically upload firmware to the pico w
* Add prompts to help assemble the secrets.json file
* Support multiple WIFI SSID's
* Automatic Updates?

![Opened Enclosure](assets/Inside.jpg?raw=true "Title")
![Closed Enclosure](assets/Assembled.jpg?raw=true "Title")