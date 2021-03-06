from time import sleep
import os
import sys
import json
from modules import clear_the_screen, bcolors, logo_top, image_show, ota_image
from ConfigParser import ConfigParser

parser = ConfigParser()

updater_version = '2.2.9n'  ### version of THIS program - has nothing to do with the RH version
                            ### it reffers to the API level of newest contained nodes firmware 
                            ### third number reffers to actual verion of the updater itself

homedir = os.path.expanduser('~')

if os.path.exists("./updater-config.json"):
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
        data = json.load(config_file)

preffered_RH_version = data['RH_version']

if preffered_RH_version == 'master':
    firmware_version = 'master'
if preffered_RH_version == 'beta':
    firmware_version = 'beta'
if preffered_RH_version == 'stable':
    firmware_version = 'stable'
if preffered_RH_version == 'custom':
    firmware_version = 'stable'

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False 

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']

def config_check():
    if not os.path.exists("./updater-config.json"):
        print("""
        Looks that you haven't set up config file yet.
        Please read about configuration process - point 5
        and next enter configuration wizard - point 6.""")

def compatibility():               ### adds compatibility and fixes with previous versions
    os.system("python ./prev_comp.py")

if not os.path.exists(homedir+"/.ota_markers/ota_config.txt"):
    os.system("cp "+homedir+"/RH-ota/resources/ota_config.txt "+homedir+"/.ota_markers/ota_config.txt")


def parser_write():
    try:
        with open('/home/'+user+'/.ota_markers/ota_config.txt', 'wb') as configfile:
            parser.write(configfile)
    except IOError as up :
        print("Config file does not exist and could not be created.")

def log_send():
    selection = str(raw_input("\n\n\tDo you want to send a log file for a review to the developer? [y/n] "))
    if selection=='y' or selection =='yes':
        if not parser.getint('added_functions','curl_installed'):
            if not os.system("sudo apt install curl cowsay"):
                parser.set('added_functions','curl_installed','1')
                parser_write()
        log_name = str(raw_input("\n\tPlease enter your name so we know who sent a log file: "))
        print("\n\tPlease wait, file is being uploaded...\n")
        os.system("rm ./log_data/log_name.txt > /dev/null 2>&1")
        os.system("rm ./log_data/log_code.txt > /dev/null 2>&1")
        os.system("echo "+log_name+" > ./log_data/log_name.txt")
        os.system("curl --upload-file ./log_data/log.txt https://transfer.sh/"+log_name+"_log.txt | tee -a ./log_data/log_code.txt")
        print("\n")
        os.system("sed -i 's/https:\/\/transfer.sh\///g' ./log_data/log_code.txt")
        os.system("sed -i 's/\/"+log_name+"_log.txt//g' ./log_data/log_code.txt")
        print("\n___________________________\n")
        print("\nTell your favourite developer those:\n")
        print("User name: "+log_name)
        f = open("./log_data/log_code.txt","r")
        for line in f:
            code = line
        print("\nUser code: "+code)
        print("\n___________________________\n") 
        raw_input("\n\nHit 'Enter' to continue\n\n")
        if not os.system("cowsay You are awesome! Fly safe."):
            sleep(3)
        main_menu()
    if selection=='n' or selection =='no':
        print("\n\n\tOK - you log file is stored under 'log.txt' name in RH-ota directory.")
        raw_input("\n\n\tHit 'Enter' to continue\n\n")
        main_menu()
    else:
        log_send()

def updated_check():
    if os.path.exists("/home/"+user+"/.ota_markers/.was_updated"):
        clear_the_screen()
        logo_top()
        print(""" {bold}
        Software was updated recently to the new version.

        You can read update notes now or check them later.


         {endc}  {green} 
        'r' - read update notes {endc}

        's' - skip and don't show again
        """.format(bold=bcolors.BOLD, underline=bcolors.UNDERLINE_S
                   , endc=bcolors.ENDC_S, blue=bcolors.BLUE_S
                   , yellow=bcolors.YELLOW_S
                   , red=bcolors.RED_S
                   , green=bcolors.GREEN
                   , orange=bcolors.ORANGE_S))
        selection = str(raw_input())
        if selection == 'r':
            os.system("less ./docs/update-notes.txt")
        if selection == 's':
            pass
        else:
            updated_check()
        os.system("rm /home/"+user+"/.ota_markers/.was_updated >/dev/null 2>&1")

def first():
    compatibility()
    parser.read('/home/'+user+'/.ota_markers/ota_config.txt')
    clear_the_screen()
    print("\n\n")
    image_show()
    print("\t\t\t "+bcolors.BOLD+"Updater version: "+str(updater_version)+bcolors.ENDC)
    sleep(1)
    updated_check()
    #os.system("sudo systemctl stop rotorhazard > /dev/null 2>&1")

def avr_dude():
    clear_the_screen()
    logo_top()
    menu = """
            {red}
                        AVRDUDE MENU
            {blue}    
                1 - Install avrdude {endc}{yellow}
                2 - Go back {endc}
        """.format(bold=bcolors.BOLD, underline=bcolors.UNDERLINE_S
                   , endc=bcolors.ENDC_S, blue=bcolors.BLUE
                   , yellow=bcolors.YELLOW
                   , red=bcolors.RED
                   , green=bcolors.GREEN
                   , orange=bcolors.ORANGE_S)
    print(menu)
    selection=str(raw_input(""))
    if selection=='1' : 
        os.system("sudo apt-get update")
        os.system("sudo apt-get install avrdude -y")
        print ("\nDone\n")
    if selection=='2' : 
        main_menu()
    else:
        avr_dude()

def serial_menu():
    clear_the_screen()
    logo_top()
    def serial_content():
        os.system("echo 'enable_uart=1'| sudo tee -a /boot/config.txt")
        os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
        #os.system("echo 'functionality added' | tee -a ~/.ota_markers/.serialok")
        parser.set('added_functions','serial_added','1')
        parser_write()
        print("""
        
        Serial port enabled successfully
        You have to reboot Raspberry now. Ok?
        
        r - Reboot now{yellow}
        b - Go back{endc}""".format(bold=bcolors.BOLD, underline=bcolors.UNDERLINE
           , endc=bcolors.ENDC, blue=bcolors.BLUE
           , yellow=bcolors.YELLOW
           , red=bcolors.RED
           , green=bcolors.GREEN
           , orange=bcolors.ORANGE_S))
        selection=str(raw_input(""))
        if selection=='r':
            os.system("sudo reboot")
        if selection== 'b':
            features_menu()
    print("""
    
    
        Serial port has to be enabled. 
        Without it Arduinos cannot be programmed.
        Do you want to enable it now?""")
    selection=str(raw_input("\n\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
    if selection == 'y':
        if parser.getint('added_functions','serial_added'):
            print("\n\n\t\tLooks like you already enabled Serial port. \n\t\tDo you want to continue anyway?\n")
            selection=str(raw_input("\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
            if selection=='y':
                serial_content()
            if selection =='a':
                features_menu()
            else:
                serial_menu()
        else:
            serial_content()
    if selection == 'a':
        features_menu()
    else:
        serial_menu()

def aliases_menu():
    clear_the_screen()
    def aliases_content():
        os.system("cat ./resources/aliases.txt | tee -a ~/.bashrc")
        parser.set('added_functions','aliases_1','1')
        parser.set('added_functions','aliases_2','1')
        parser_write()
        print("\n\n\t\t    Aliases added successfully")
        sleep(3)
        features_menu()
    print("""
    
    
    Aliases in Linux act like shortcuts or referances to another commands. 
    You can use them every time when you operates in the terminal window. 
    For example instead of typing 'python ~/RotorHazard/src/server/server.py' 
    you can just type 'ss' (server start) etc. Aliases can be modified and added 
    anytime you want. You just have to open '~./bashrc' file in text editor 
    - like 'nano'. After that you have reboot or type 'source ~/.bashrc'. 
    
    {bold}
        Alias            What it does    
        
        ss       -->    starts the RotorHazard server
        cfg       -->    opens RH config.json file
        rh        -->    goes to server file directory
        py        -->    insted of 'python' - pure laziness
        sts        -->    stops RH service if was started
        otadir   -->    goes to RH server file directory
        ota        -->    opens this software
        als        -->    opens the file that containes aliases
        rld        -->    reloads aliases file 
        rcfg        -->    opens raspberry's configuration 
        gitota      -->    clones OTA repository
        otacfg   -->    opens updater conf. file
        otacpcfg -->    copies ota conf. file.
        home     -->    go to the home directory (without '~' sign)\n
    {endc}
        Do you want to use above aliases in your system?
        Reboot should be performed after adding those""".format(bold=bcolors.BOLD, endc=bcolors.ENDC))
    selection=str(raw_input("\n\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
    if selection == 'y':
        if parser.getint('added_functions','aliases_1'):
            print("\n\n\t\tLooks like you already have aliases added. \n\t\tDo you want to continue anyway?\n")
            selection=str(raw_input("\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
            if selection=='y':
                aliases_content()
            if selection =='a':
                features_menu()
            else:
                aliases_menu()
        else:
            aliases_content()
    if selection == 'a':
        features_menu()
    else:
        aliases_menu()

def self_updater():
    def add_updater():
        clear_the_screen()
        logo_top()
        print("""\n
    Permissions required so 'zip' and 'unzip' program can be downloaded.
    Performed only during first instance of entering this sub-menu\n""")
        sleep(2)
        os.system("sudo echo")
        os.system("sudo apt install zip unzip")
        os.system("""echo 'alias updateupdater=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null""")
        os.system("""echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null""")
        parser.set('added_functions','updater_planted','1')
        parser_write()
    if parser.getint('added_functions','updater_planted') == 0:
        add_updater()
    clear_the_screen()
    logo_top()
    print(bcolors.BOLD+"""
    If you want to update this program and download new firmware, 
    prepared for Arduino nodes - so you can next flash them 
    - you can just hit 'u' now. You can also type 'updateupdater'
    or 'uu' in the terminal window.\n
    Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+bcolors.BOLD+""",
    so you allways know what firmware version updater contains.
    For example "2.2.5c" contains nodes firmware with "API level 22".
    Self-updater will test your internet connection during every update."""+bcolors.ENDC+"""\n""")
    print(bcolors.GREEN+"""
        Update now by pressing 'u'"""+bcolors.ENDC+"""\n""")
    print(bcolors.YELLOW+"""\t\tGo back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
    selection=str(raw_input(""))
    if selection=='b':
        features_menu()
    if selection=='u':
        os.system(". ./open_scripts.sh; updater_from_ota")
    else :
        self_updater()

def features_menu():
    clear_the_screen()
    logo_top()
    features = '''

                              {red}{bold}{underline}FEATURES MENU{endc}

        {blue}{bold} 
                        1 - Install AVRDUDE
                        
                        2 - Enable serial protocol {endc} {bold}
                        
                        3 - Access Point and Internet 
                        
                        4 - Show actual Pi's GPIO
                        
                        5 - Useful aliases
                        
                        6 - Update OTA software {endc} {yellow}{bold}
                            
                        e - Exit to main menu {endc}

        '''.format(bold=bcolors.BOLD, underline=bcolors.UNDERLINE
                   , endc=bcolors.ENDC, blue=bcolors.BLUE
                   , yellow=bcolors.YELLOW
                   , red=bcolors.RED)

    print(features)
    selection=str(raw_input(""))
    if selection=='1':
        avr_dude()
    if selection== '2':
        serial_menu()
    if selection=='3':
        os.system("python ./net_and_ap.py")
    if selection=='4':
        if not parser.getint('added_functions','pinout_installed'):
            print("Some additional software has to be added so action can be performed. Ok?\n[yes/no]\n")
            while True:
                selection = str(raw_input())
                if selection == 'y' or selection == 'yes':
                    if not os.system("sudo apt-get install python3-gpiozero"):
                        parser.set('added_functions','pinout_installed','1')
                        parser_write()
                        break
                    else:
                        print("\nFailed to install required package.\n")
                        sleep(2)
                        break
                if selection == 'n' or selection == 'no':
                    break
                else:
                    continue
        if parser.getint('added_functions','pinout_installed'):
            os.system("pinout")
            selection = str(raw_input("\nDone? Hit 'Enter'\n"))
        else:
            print("\nAdditional software needed. Please re-enter this menu.\n")
            sleep(3)
    if selection=='5':
        aliases_menu()
    if selection=='6':
        self_updater()
    if selection=='e':
        main_menu()
    else:
        features_menu()

def first_time():
    def update_notes():
        clear_the_screen()
        os.system("less ./docs/update-notes.txt")
    def second_page():
        clear_the_screen()
        print("""


                {underline}{bold}CONFIGURATION PROCESS{endc}


            {bold} 
            Software configuration process can be assisted with a wizard. 
            You have to enter point 5. of Main Menu and apply right values.
            It will configure this software, not RotorHazard server itself. 
            Thing like amount of used LEDs or password to admin page of RotorHazard
            should be configured separately - check RotorHazard Manager in Main Menu.


            Possible RotorHazard server versions:

            >  {blue}  'stable' {endc} {bold}- last stable release (can be from before few days or few months) {endc}
            
            >  {blue}  'beta'   {endc} {bold}- last 'beta' release (usually has about few weeks, quite stable) {endc}
            
            >  {blue}  'master' {endc} {bold}- absolutely newest features implemented (even if not well tested)  {endc}  

            """.format(bold=bcolors.BOLD_S, underline=bcolors.UNDERLINE_S
                       , endc=bcolors.ENDC, blue=bcolors.BLUE
                       , yellow=bcolors.YELLOW_S
                       , red=bcolors.RED_S
                       , orange=bcolors.ORANGE_S))
        print("\n\n\t\t'f' - first page'"+bcolors.GREEN+"\t'u' - update notes'"+bcolors.ENDC+bcolors.YELLOW+"\t'b' - back to menu"+bcolors.ENDC+"\n\n")
        selection=str(raw_input(""))
        if selection=='f':
            first_page()
        if selection=='b':
            main_menu()
        if selection=='u':
            update_notes()
        else :
            second_page()
    def first_page():
        clear_the_screen()
        print(bcolors.BOLD + """

        You can use all implemented features, but if you want to be able to program
        Arduino-based nodes - enter Features menu and begin with first 2 points.

        Also remember about setting up config file - check second page.  

        This program has ability to perform 'self-updates'. Check "Features menu".

        More info about whole poject that this software is a part of: 
        https://www.instructables.com/id/RotorHazard-Updater/
        and in how_to folder - look for PDF file.\n
        New features and changes - see update notes section.
        If you found any bug - please report via GitHub or Facebook.\n
                Enjoy!
                                            Szafran
        """ + bcolors.ENDC)

        menu = '''{green}
            s - second page {endc}
        
            u -  update notes {yellow}
        
            b - back to main menu {endc}
        '''.format(green=bcolors.GREEN, endc=bcolors.ENDC, yellow=bcolors.YELLOW)
        print(menu)
        selection=str(raw_input(""))
        if selection=='s':
            second_page()
        if selection=='u':
            update_notes()
        if selection=='b':
            main_menu()
        else :
            first_page()
    first_page()

def end():
        parser_write()
        clear_the_screen()
        print("\n\n")
        ota_image()
        print("\t\t\t\t   "+bcolors.BOLD+"Happy flyin'!"+bcolors.ENDC+"\n")
        sleep(1.3)
        clear_the_screen()
        sys.exit()

def main_menu():
    clear_the_screen()
    logo_top()
    config_check()
    menu = """
    
                              {red}{bold}{underline}MAIN MENU{endc}
                
    {blue}{bold}
                        1 - RotorHazard Manager
                        
                        2 - Nodes flash and update {endc} {bold}
                        
                        3 - Start the server now
                        
                        4 - Additional features
                        
                        5 - Info + first time here
                        
                        6 - Configuration wizard {endc}{yellow}
                        
                        e - Exit {endc}
                        
    """.format(bold=bcolors.BOLD, underline=bcolors.UNDERLINE
                       , endc=bcolors.ENDC, blue=bcolors.BLUE
                       , yellow=bcolors.YELLOW
                       , red=bcolors.RED
                       , orange=bcolors.ORANGE)
    print(menu)
    selection=str(raw_input())
    if selection=='1':
        os.system("python ./rpi_update.py")   ### opens raspberry updating file
    if selection=='2':
        os.system("python ./nodes_update.py")   ### opens nodes updating file
    if selection=='3':
        clear_the_screen()
        os.system(". ./open_scripts.sh; server_start")
    if selection=='4':
        features_menu()
    if selection=='5':
        first_time()
    if selection=='6':
        os.system("python ./conf_wizard_ota.py")
    if selection == 'logme':
        os.system(". ./open_scripts.sh; log_me")
        log_send()
    if selection=='e':
        end()
    if selection=='2dev':
        os.system("python ./.dev/done_nodes_update_dev.py")   ### opens nodes updating file
    else:
        main_menu()

if __name__ == "__main__":
    first()
    main_menu()


