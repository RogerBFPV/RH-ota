from time import sleep
import os
import platform
import sys
from modules import check_if_string_in_file
from ConfigParser import ConfigParser
parser = ConfigParser()

homedir = os.path.expanduser('~')

for i in range (3):
	aliases_1_FLAG = False
	aliases_2_FLAG = False
	installation_FLAG = False
	updater_FLAG = False
	serial_FLAG = False
	pinout_FLAG = False

	if os.path.exists(homedir+"/.ota_markers") == False:
		os.system("mkdir "+homedir+"/.ota_markers")
	if os.path.exists(homedir+"/.aliases_added") == True:
		if os.path.exists(homedir+"/.ota_markers/.aliases_added") == False:
			os.system("cp "+homedir+"/.aliases_added "+homedir+"/.ota_markers/.aliases_added ")
		os.system("rm "+homedir+"/.aliases_added")
		if os.path.exists(homedir+"/.ota_markers/.aliases_added") == False:
			os.system("cp "+homedir+"/.updater_self "+homedir+"/.ota_markers/.updater_self ")
		os.system("rm "+homedir+"/.updater_self")
		if os.path.exists(homedir+"/.ota_markers/.installation-check_file.txt") == False:
			os.system("cp /home/"+user+"/.old_RotorHazard.old/.installation-check_file.txt "+homedir+"/.ota_markers/.installation-check_file.txt")
		os.system("rm "+homedir+"/.installation-check_file.txt")
	if os.path.exists(homedir+"/.serialok") == True:
		if os.path.exists(homedir+"/.ota_markers/.serialok") == False:
			os.system("cp "+homedir+"/.serialok "+homedir+"/.ota_markers/.serialok")
		os.system("rm "+homedir+"/.serialok")
	if os.path.exists(homedir+"/.bashrc") == True:
		if check_if_string_in_file(homedir+'/.bashrc', 'RotorHazard OTA Manager updated'):
			os.system("sed -i 's/alias updateupdater/# alias updateupdater/g' "+homedir+"/.bashrc")
			os.system("sed -i 's/RotorHazard OTA Manager updated/old alias/g' "+homedir+"/.bashrc")
			os.system("echo 'alias updateupdater=\"cd ~ && sudo cp ~/RH-ota/self.py ~/.ota_markers/self.py && sudo python ~/.ota_markers/self.py \"  # part of self-updater' | tee -a ~/.bashrc >/dev/null")
		if check_if_string_in_file(homedir+'/.bashrc', 'starts the server'):
			os.system("sed -i 's/alias ss/# alias ss/g' "+homedir+"/.bashrc")
			os.system("sed -i 's/starts the server/old alias/g' "+homedir+"/.bashrc")
			os.system("echo 'alias ss=\"cd ~/RotorHazard/src/server && python server.py\"   #  starts the RH-server' | tee -a ~/.bashrc >/dev/null")
		if check_if_string_in_file(homedir+'/.bashrc', 'opens updating script'):
			os.system("sed -i 's/alias ota=/# alias ota=/g' "+homedir+"/.bashrc")
			os.system("sed -i 's/opens updating script/old alias/g' "+homedir+"/.bashrc")
			os.system("echo 'alias ota=\"cd ~/RH-ota && python update.py\"  # opens updating soft' | tee -a ~/.bashrc >/dev/null")
		if check_if_string_in_file(homedir+'/.bashrc', 'part of self-updater'):
			os.system("sed -i 's/part of self-updater/part of self updater/g' "+homedir+"/.bashrc")
			os.system("echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null")
			if os.path.exists(homedir+"/.ota_markers/.aliases2_added") == False:
				os.system("echo 'alias otacfg=\"nano ~/RH-ota/updater-config.json \"  # opens updater conf. file' | tee -a ~/.bashrc >/dev/null")
				os.system("echo 'alias otacpcfg=\"cd ~/RH-ota && cp distr-updater-config.json updater-config.json \"  # copies ota conf. file' | tee -a ~/.bashrc >/dev/null")
				os.system("echo 'alias home=\"cd ~ \"  # go homedir (without ~ sign)' | tee -a ~/.bashrc >/dev/null")
				os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases2_added >/dev/null")
		if os.path.exists("./updater-config.json") == True:
			if not check_if_string_in_file(homedir+'/RH-ota/updater-config.json', '"pins_assignment"'):
				os.system("sed -i 's/\"debug_mode\" : 0/\"debug_mode\" : 0,/g' "+homedir+"/RH-ota/updater-config.json")
				os.system("sed -i 's/\"debug_mode\" : 1/\"debug_mode\" : 1,/g' "+homedir+"/RH-ota/updater-config.json")
				os.system("sed -i 's/}/	\"pins_assignment\" : \"default\" /g' "+homedir+"/RH-ota/updater-config.json")
				os.system("echo '}' | tee -a "+homedir+"/RH-ota/updater-config.json >/dev/null 2>&1")
			if check_if_string_in_file(homedir+'/RH-ota/updater-config.json', '"pins_assignment"'):
				if not check_if_string_in_file(homedir+'/RH-ota/updater-config.json', '"updates_without_pdf"'):
					os.system("sed -i 's/\"pins_assignment\" : \"default\"/\"pins_assignment\" : \"default\",/g' "+homedir+"/RH-ota/updater-config.json")
					os.system("sed -i 's/\"pins_assignment\" : \"custom\"/\"pins_assignment\" : \"custom\",/g' "+homedir+"/RH-ota/updater-config.json")
					os.system("sed -i 's/\"pins_assignment\" : \"PCB\"/\"pins_assignment\" : \"PCB\",/g' "+homedir+"/RH-ota/updater-config.json")
					os.system("sed -i 's/}/	\"updates_without_pdf\" : 0 /g' "+homedir+"/RH-ota/updater-config.json")
					os.system("echo '}' | tee -a "+homedir+"/RH-ota/updater-config.json >/dev/null 2>&1")
	if os.path.exists(homedir+"/.ota_markers/.serialok") == True:
		serial_FLAG=True
	if os.path.exists(homedir+"/.ota_markers/.installation-check_file.txt") == True:
		installation_FLAG = True
	if os.path.exists(homedir+"/.ota_markers/.pinout_added"):
		pinout_FLAG=True
	if os.path.exists(homedir+"/.ota_markers/.aliases_added") == True:
		aliases_1_FLAG=True
	if os.path.exists(homedir+"/.ota_markers/.aliases2_added"):
		aliases_2_FLAG=True
	if os.path.exists(homedir+"/.ota_markers/.updater_self") == True:
		updater_FLAG=True
	if not os.path.exists(homedir+"/.ota_markers/ota_config.txt"):
		os.system("cp "+homedir+"/RH-ota/ota_config.txt "+homedir+"/.ota_markers/ota_config.txt")
	parser.read(homedir+'/.ota_markers/ota_config.txt')
	if aliases_1_FLAG==True:
		parser.set('added_functions','aliases_1','1')
	if aliases_2_FLAG==True:
		parser.set('added_functions','aliases_2','1')
	if installation_FLAG==True:
		parser.set('added_functions','installation_done','1')
	if updater_FLAG==True:
		parser.set('added_functions','updater_planted','1')
	if pinout_FLAG ==True:
		parser.set('added_functions','pinout_installed','1')
	if serial_FLAG==True:
		parser.set('added_functions','serial_added','1')
	with open(homedir+'/.ota_markers/ota_config.txt', 'wb') as configfile:
		parser.write(configfile)
	#os.system("rm "+homedir+"/.ota_markers/.* >/dev/null 2>&1")

	if os.stat(homedir+'/.ota_markers/ota_config.txt').st_size == 0:
		os.system("rm "+homedir+"/.ota_markers/ota_config.txt")
		continue
	else:
		break
