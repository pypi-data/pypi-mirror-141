#imports
import time
import main

def __init__(self):
    print(self)
    print("RA_PACKAGE LOADING")

    #get debug mode from main.py
    debugMode = main.debugMode
        
    #in conbination with debug mode: prints RA-Package Logo and whats includes
    startupinfo = True

    #delay for logo "animation"
    global delay
    delay = 0.05

    #version number of Package
    version = 1.0

    if debugMode == True:
        if (startupinfo == True):
            #logo and "animation"
            print("------------------------------------------------------------------------------------------------------------------")
            time.sleep(delay)
            print(' ')
            time.sleep(delay)
            print('|-----\             /\          |-----\   |-----  |------  |     |  |\     |  |-----  |-----\      /---------\ ')
            time.sleep(delay)
            print('|      |           /  \         |      |  |       |        |     |  | \    |  |       |      |    /  /-----   \ ')
            time.sleep(delay)
            print('|_____/           /    \        |_____/   |       |        |_____|  |  \   |  |       |_____/     |  |        | ')
            time.sleep(delay)
            print('|   \            /------\       |   \     |-----  |        |     |  |   \  |  |-----  |   \       |  |        | ')
            time.sleep(delay)
            print('|    \          /        \      |    \    |       |        |     |  |    \ |  |       |    \      |  \-----   | ')
            time.sleep(delay)
            print('|     \   und  /          \     |     \   |_____  |______  |     |  |     \|  |_____  |     \     \__________ / ')
            time.sleep(delay)
            print("------------------------------------------------------------------------------------------------------------------")
            time.sleep(delay)
            #infos about the Package
            print('|[ copyright BY LEON ARQUILLIERE UND MANUEL RAFFL. JAENNER 2021 ]                                                 |')
            time.sleep(delay)
            print("|-----------------------------------------------------------------------------------------------------------------|")
            time.sleep(delay)
            print('_____________________________________________________________')
            time.sleep(delay)
            print('|                                                           |')
            time.sleep(delay)
            print('|A cooparation between Manuel Raffl and Leon Arquilliere    |')
            time.sleep(delay)
            print('|___________________________________________________________|')
            time.sleep(delay)
            print(' ')
            print("------------------------------------------------------------------------------------------------------------------")
            time.sleep(delay)
            print("RA-Package copyright by Manuel Raffl und Leon Arquilliere")
            time.sleep(delay)
            print("Ra-Packege Version: " + str(version))
            time.sleep(delay)
            print("Funktionen:")
            time.sleep(delay)
            print("|")
            time.sleep(delay)
            print("|--> Simple math (+-*/)")
            time.sleep(delay)
            print("|--> Advanced math (%)")
            time.sleep(delay)
            print("|--> Use of variables")
            time.sleep(delay)
            print("|--> Logging (file & Mail)")
            time.sleep(delay)
            print("------------------------------------------------------------------------------------------------------------------")
            time.sleep(delay)

#end "animation"
def stopanimation():
    global delay
    if main.debugMode == True:
        print("------------------------------------------------------------------------------------------------------------------")
        time.sleep(delay*2)
        print(' ')
        time.sleep(delay*2)
        print('|-----\             /\          |-----\   |-----  |------  |     |  |\     |  |-----  |-----\      /---------\ ')
        time.sleep(delay*2)
        print('|      |           /  \         |      |  |       |        |     |  | \    |  |       |      |    /  /-----   \ ')
        time.sleep(delay*2)
        print('|_____/           /    \        |_____/   |       |        |_____|  |  \   |  |       |_____/     |  |        | ')
        time.sleep(delay*2)
        print('|   \            /------\       |   \     |-----  |        |     |  |   \  |  |-----  |   \       |  |        | ')
        time.sleep(delay*2)
        print('|    \          /        \      |    \    |       |        |     |  |    \ |  |       |    \      |  \-----   | ')
        time.sleep(delay*2)
        print('|     \   und  /          \     |     \   |_____  |______  |     |  |     \|  |_____  |     \     \__________ / ')
        time.sleep(delay*2)
        print("------------------------------------------------------------------------------------------------------------------")
        time.sleep(delay*2)
        print("Programm wird beendet ...")
        print("------------------------------------------------------------------------------------------------------------------")
        time.sleep(delay*3)
    else:
        pass;