
RotorHazard builds on the [Delta5 Race Timer](https://github.com/scottgchin/delta5_race_timer), and supports up to 8 nodes.



Easy mange and update your RotorHazard installation. 
		
Additional features like nodes flashing also included.
		
		
		If you want all hardware functionalities - visit:

		[Instructables page](https://www.instructables.com/id/RotorHazard-Updater/)
		
Link:
https://www.instructables.com/id/RotorHazard-Updater/
		
		or check how_to folder - look for PDF file.
		
		Software is designed to run using python 2.7.
		Will be updated to be python 3 friendly, when
		RotorHazard software will be converted as well.

		Commands to download the repo onto Raspberry Pi or Linux system:
		
			cd ~
			sudo apt install zip unzip
			wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip
			unzip tempota.zip
			rm tempota.zip
			mv RH-ota-* RH-ota
		
		Commands to open the software:
			
			sudo apt install python --> if needed
			
			cd ~/RH-ota
			python update.py


## Major Features
* Timing and event management on local server hardware
* Modern, mobile-friendly, and responsive
* Confidently calibrate in seconds with visual interface
* Fix calibration issues retroactively after race is complete
* Never miss a lap; recover laps with full accuracy by reviewing RSSI history
* Improved filtering works both indoors and outdoors without adjustment, even in difficult multipathing environments
* Improved synchronization and timing accuracy
* Manage pilots, heats, classes, and race formats
* Full manual control of results for race organizer
* Statistics broken out by event, class, heat, and round
* Sends realtime lap data to livetime
* LED and audio support to indicate race staging, starts, and other events
* JSON API to retrieve timing data from other systems

## Hardware and Software Setup
To build and configure the system, follow the instructions here:<br />
[doc/Hardware Setup.md](doc/Hardware%20Setup.md)<br />
[doc/Software Setup.md](doc/Software%20Setup.md)

An easy-to-build single node version of RotorHazard may also be constructed -- see [doc/USB Nodes.md](doc/USB%20Nodes.md) for more info.

**Note:** The 'master' branch in the GitHub repository will usually contain the latest development code, which may not be stable. To install the latest stable release, please follow the instructions in the [doc/Software Setup.md](doc/Software%20Setup.md) document (for version upgrading see the '[Updating an existing installation](doc/Software%20Setup.md#update)' section at the end).

## User Guide
For initial setup and running races, follow these instructions: [doc/User Guide.md](doc/User%20Guide.md)

## Migrating from/to Delta5
RotorHazard uses the same hardware, but different code for the nodes. Re-flash your Arduinos as in the [setup instructions](doc/Software%20Setup.md#receiver-nodes-arduinos) whenever you switch between the two projects.

## Additional Resources
Links to external resources are available from the [Wiki](https://github.com/RotorHazard/RotorHazard/wiki), including extended tutorials, video content, and a Raspberry Pi setup/install/upgrade/node flashing tool.

## Contributors
* Michael Niggel
* Eric Thomas
* Klaus Michael Schneider
* Mark Hale
* Cerberus Velvet
* David Just
* Scott Chin and other [Delta5](https://github.com/scottgchin/delta5_race_timer) Contributors

### Supported by:
[![Propwashed Logo](doc/img/Propwashed-Logo-200w.png)](https://propwashed.com)

### Translators
* Dutch: Kenny Van Der Sypt
* German: Klaus Michael Schneider
* Spanish: Ramon Hernandez Roldan
* French: Yannick M.
* Polish: Mariusz Misiurek and Paweł Fabiszewski

## Feedback

Discuss RotorHazard on Facebook:  https://www.facebook.com/groups/rotorhazard

To report bugs or request features, please post a GitHub issue [here](https://github.com/RotorHazard/RotorHazard/issues).

Community contributions are welcome and encouraged; see the [Development.md](doc/Development.md) doc for more info.
