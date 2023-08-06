print("Started <Pycraft_Installer>")

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *

import subprocess, time, os, json, threading, sys, shutil, platform

def runInstaller():
    base_folder = os.path.dirname(__file__)

    try:
        with open(os.path.join(base_folder, ("Data_Files\\InstallerConfig.json")), 'r') as openFile:
            SavedData = json.load(openFile)
    except Exception as Message:
        PycPath = None
        Repair = {"PATH":None}
        with open(os.path.join(base_folder, ("Data_Files\\InstallerConfig.json")), 'w') as openFile:
            json.dump(Repair, openFile)
    else:
        PycPath = SavedData["PATH"]


    def Close():
        if messagebox.askokcancel("Pycraft Setup Wizard", "Are you sure you want to cancel the install?"):
            quit()


    def CreateText(root, OUTPUTtext):
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, OUTPUTtext)
        text["state"] = DISABLED
        text.place(x=200, y=80)
        root.update_idletasks()

                
    def Start(root):
        root = CreateDisplay(root)

        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        if not PycPath == None:
            ButtonPos = (760, 500)
            Label(root, text="Modify Your Install", background='white', font=(None, 20)).place(x=200, y=35)
            
            text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
            text.insert(INSERT, f"Welcome back to Pycraft's Setup Wizard, we have detected you already have an install of Pycraft on your system, this gives you 3 available options.\n\nWould you like to update, modify or uninstall your version of Pycraft?\n\nThis will modify the installation of Pycraft at: {PycPath}")
            text["state"] = DISABLED
            text.place(x=200, y=80)
            
            Button(root, text='Update', command=lambda: Update_Screen_1(root)).place(x=680, y=500)
            RepairButton = Button(root, text='Repair')
            RepairButton["state"] = DISABLED
            RepairButton.place(x=600, y=500)
            Button(root, text='Uninstall', command=lambda: Uninstall_Screen_1(root)).place(x=520, y=500)
        else:
            if platform.system() == "Windows":
                try:
                    sys.version
                    EnterText = "Welcome to Pycraft's Setup Wizard, here we will guide you through your install and setup of the latest stable version of Pycraft, if you wish to install the BETA versions of the game, please tick the box below and then once you are satisfied with your choice, please press the continue button, you can press the back button to navigate to the previous menu or choose to exit Pycraft's Setup Wizard by closing the GUI. \n\nThere are a few steps to this install but this shouldn't take long."
                    IfCompat = NORMAL
                    ButtonPos = (680, 500)
                except:
                    IfCompat = DISABLED
                    EnterText = "Welcome to Pycraft's Setup Wizard, here we will guide you through your install and setup of the latest stable version of Pycraft, if you wish to install the BETA versions of the game, please tick the box below and then once you are satisfied with your choice, please press the continue button, you can press the back button to navigate to the previous menu or choose to exit Pycraft's Setup Wizard by closing the GUI. \n\nThere are a few steps to this install but this shouldn't take long.\n\nIn order to install Pycraft you will need to have a suitable version of Python installed on your system, ideally this needs to be 3.7 or greater -with version checking coming in a later version-. If you want to install Pycraft stand-alone then on the releases page of the project (here: https://github.com/PycraftDeveloper/Pycraft/releases) please download the (.exe) version."
            else:
                IfCompat = DISABLED
                EnterText = "Welcome to Pycraft's Setup Wizard, here we will guide you through your install and setup of the latest stable version of Pycraft, if you wish to install the BETA versions of the game, please tick the box below and then once you are satisfied with your choice, please press the continue button, you can press the back button to navigate to the previous menu or choose to exit Pycraft's Setup Wizard by closing the GUI. \n\nThere are a few steps to this install but this shouldn't take long.\n\nCurrently this installer is Windows only, but more OS's will be supported in later editions"
            text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
            text.insert(INSERT, EnterText)
            text["state"] = DISABLED
            text.place(x=200, y=40)
        
            global ChooseBETA, BETAchoice
            BETAchoice = BooleanVar(value=ChooseBETA)
            
            def isChecked():
                global ChooseBETA
                
                if BETAchoice.get() == True:
                    ChooseBETA = True
                else:
                    ChooseBETA = False
                
            Checkbutton(root, text='I want to install a BETA version of Pycraft', variable=BETAchoice, onvalue=True, offvalue=False, command=isChecked).place(x=200, y=500)
            
            ContinueButton = Button(root, text='Continue', command=lambda: InstalInfo(root))
            ContinueButton.place(x=760, y=500)
            ContinueButton["state"] = IfCompat
        
        
        Button(root, text='Quit', command=Close).place(x=ButtonPos[0], y=ButtonPos[1])
        
    def OutdatedDetector():
        try:
            import urllib.request as urlOpener
            urlOpener.urlopen('https://www.google.com', timeout=1)
            
            List = subprocess.check_output([sys.executable, "-m","pip","list","--outdated"], False)

            if b"Python-Pycraft" in List:
                return True
            else:
                return False
        except Exception as Message:
            ErrorMessage = "IntegratedInstaller > IntegInstaller > CheckVersions: "+str(Message)
        
    
    def Update_Screen_3(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Updating Pycraft - Part 1 - Removing old files", background='white', font=(None, 15)).place(x=200, y=35)
        
        OUTPUTtext = "Querying versions"
        CreateText(root, OUTPUTtext)

        import main
        version = main.QueryVersion()
        OUTPUTtext += f"\nPreparing to remove {version} and additional files"
        CreateText(root, OUTPUTtext)
        
        FileArray = search_files(PycPath)
        import site
        AdditionalFileArray = search_files(site.getuserbase()+"\\Python310\\site-packages")
        
        FileArray = FileArray+AdditionalFileArray
        OUTPUTtext += f"\nIdentified {len(FileArray)} files to remove"
        CreateText(root, OUTPUTtext)
        
        global running_Uninstall, completion_percent
        completion_percent = 0
        running_Uninstall = True
        threading.Thread(target=remove_files, args=(FileArray, True,)).start()

        OUTPUTtext += f"\nRemoving {version}"
        CreateText(root, OUTPUTtext)
                        
        def Render_Progressbar():
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += completion_percent
            root.update()
            
        while running_Uninstall == True:
            root.after(50, Render_Progressbar())
            
        OUTPUTtext += f"\nSuccessfully removed {version} and additional files"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nCleaning Up"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nDone"
        CreateText(root, OUTPUTtext)
        
        Update_Screen_4(root)
        
    def FinishedUpdate(root):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Finished Updating Pycraft", background='white', font=(None, 20)).place(x=200, y=40)

        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, f"It might be useful to test and say something here ")
        text["state"] = DISABLED
        text.place(x=200, y=80)
            
    def Update_Screen_4(root):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Updating Pycraft - Part 2 - Installing new files", background='white', font=(None, 20)).place(x=200, y=40)
                
        OUTPUTtext = "Querying versions"
        CreateText(root, OUTPUTtext)
        
        i = 0
        
        global finished, ThreadError

        ThreadError = None
            
        OUTPUTtext += f"\nDownloading and installing Pycraft and the latest versions of it's dependencies (This will take a moment)"
        CreateText(root, OUTPUTtext)
        
        choice = "Latest"
        threading.Thread(target=DownloadandInstall, args=(choice,)).start()
        
        finished = False
        start = time.perf_counter()
        global InstallError
        InstallError = None
        while finished == False:
            if not InstallError == None:
                messagebox.showerror("An error ocurred", f"We were unable to install the additional files Pycraft needs in-order to update.\n\nFull Error Message: {InstallError}")
                quit()
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += i
            root.update_idletasks()
            i += 1
            time.sleep(0.01)
            
        installtime = time.perf_counter()-start
        
        OUTPUTtext += f" - done in {round(installtime, 4)} seconds"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nSuccessfully installed: Pycraft"
        CreateText(root, OUTPUTtext)
                        
        OUTPUTtext += "\nMoving Pycraft to selected install location"
        CreateText(root, OUTPUTtext)
        
        
        def MoveFiles(PycPath):
            global ThreadError
            
            temp = str(CurrentLocation.decode('UTF-8'))[:-1]
            try:
                shutil.copytree(fr"{temp}\Pycraft", PycPath)
                shutil.copyfile(base_folder+"/Installer.py", PycPath+"/Installer.py")
                shutil.copyfile(base_folder+"/Data_Files/InstallerConfig.json", PycPath+"/Data_Files/InstallerConfig.json")
            except Exception as Message:
                global InstallError
                InstallError = Message
            else:
                ThreadError = None
                
            global finished
            finished = True
            
            
        finished = False
        InstallError = None
        
        threading.Thread(target=GetPath).start()
        
        while finished == False:
            if not InstallError == None:
                messagebox.showwarning("Install Warning", "An error has occurred during the install of Pycraft, this installer is new so this is likely to occur, also this error will display on versions of Pycraft that are older than Pycraft v0.9.4. This error is not serious but many not lead to a smooth experience.")
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += i
            root.update_idletasks()
            i += 1
            time.sleep(0.01)
            
        finished = False
        
        threading.Thread(target=MoveFiles).start()
        
        while finished == False:
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += i
            root.update_idletasks()
            i += 1
            time.sleep(0.01)
            
        if ThreadError == None:
            OUTPUTtext += " - done"
            CreateText(root, OUTPUTtext)
        else:
            OUTPUTtext += " - error"
            CreateText(root, OUTPUTtext)
            while not ThreadError == None:
                print(ThreadError)
                
                if str(ThreadError)[0:13] == "[WinError 32]":
                    messagebox.showerror("File is in use in another process", "We cannot remove the previous folder because it is in use by another program, please try again")
                    try:
                        shutil.rmtree(Dir+"/Pycraft")
                    except Exception as Message:
                        ThreadError = Message
                        continue
                            
                    OUTPUTtext += " - done"
                    CreateText(root, OUTPUTtext)
                if str(ThreadError)[0:14] == "[WinError 183]":
                    ans = messagebox.askyesno("A duplicate folder was detected", "We were unable to complete the install because a folder called 'Pycraft' already exists on your system, would you like to replace this file (and move the old one to trash?)")
                    if ans == True:
                        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
                        OUTPUTtext += "\nRemoving old files"
                        CreateText(root, OUTPUTtext)
                        
                        try:
                            shutil.rmtree(Dir+"/Pycraft")
                        except Exception as Message:
                            ThreadError = Message
                            continue
                        
                        OUTPUTtext += " - done"
                        CreateText(root, OUTPUTtext)
                        
                        OUTPUTtext += f"\nMoving Pycraft to selected install location"
                        CreateText(root, OUTPUTtext)
                        
                        finished = False
            
                        RelocateFiles = threading.Thread(target=MoveFiles, args=PycPath)
                        RelocateFiles.start()
                        
                        while finished == False:
                            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
                            CompletionProgressbar.place(x=200, y=500)
                            CompletionProgressbar['value'] += i
                            root.update_idletasks()
                            i += 1
                            time.sleep(0.01)
                            
                        OUTPUTtext += " - done"
                        CreateText(root, OUTPUTtext)
                else:
                    messagebox.showerror("An error has occurred", f"We were unable to move Pycraft to the requested install location.\n\nFull Error Message:\n{ThreadError}")
                    quit()
            
        OUTPUTtext += "\nSuccessfully Updated Pycraft"
        CreateText(root, OUTPUTtext)
        
        Button(root, text='Continue', command=lambda: FinishedUpdate(root)).place(x=760, y=500)
        root.update_idletasks()


    def Update_Screen_2(root):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Checking for updates", background='white', font=(None, 15)).place(x=200, y=35)
        
        ContinueButtonState, BackButtonState = DISABLED, DISABLED
        
        def UpdateOptions(ContinueButtonState, BackButtonState):
            ContinueButton = Button(root, text='Continue', command=lambda: Update_Screen_3(root))
            ContinueButton.place(x=760, y=500)
            ContinueButton['state'] = ContinueButtonState
            BackButton = Button(root, text='Back', command=lambda: Start(root))
            BackButton.place(x=680, y=500)
            BackButton['state'] = BackButtonState
            
        UpdateOptions(ContinueButtonState, BackButtonState)
        
        ans = messagebox.askquestion("Permissions manager", "Can we have permission to download files from the internet and also modify files on this PC during the update process?")
        retry = True
        
        while retry == True:
            if ans == "yes":
                retry = False
                break
            else:
                ans2 = messagebox.askquestion("Caution", "We did not receive permission to download files from the internet and modify files on this PC, as a result we cannot install Pycraft, would you like to amend this decision (yes) or quit the installer (no)?")
                if ans2 == "no":
                    sys.exit()
                else:
                    retry = True
                    ans = messagebox.askquestion("Permissions manager", "Can we have permission to download files from the internet and also modify files on this PC at any time using this Installer?")

        OUTPUTtext = "Querying versions"
        CreateText(root, OUTPUTtext)
        
        import main
        version = main.QueryVersion()
        OUTPUTtext += f"\nFound current install as {version}"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += "\nChecking for updates online. (This might take a bit of time to complete)"
        CreateText(root, OUTPUTtext)
        
        Outdated = OutdatedDetector()
        if Outdated == False:
            OUTPUTtext += "\nYou already have the latest version of Pycraft"
            CreateText(root, OUTPUTtext)
            ContinueButtonState, BackButtonState = DISABLED, NORMAL
            UpdateOptions(ContinueButtonState, BackButtonState)
        else:
            OUTPUTtext += "\nThere are updates available on this PC, press 'continue' to start the update"
            CreateText(root, OUTPUTtext)
            ContinueButtonState, BackButtonState = NORMAL, NORMAL
            UpdateOptions(ContinueButtonState, BackButtonState)
            

    def Update_Screen_1(root):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Preparing to update Pycraft", background='white', font=(None, 15)).place(x=200, y=35)
        
        EnterText = "Welcome to Pycraft's update utility, here we will uninstall all of Pycraft's files as well as its additional data with the exception of your saved data, then reinstall the latest version.\nThe update utility will prompt for both accessing and downloading files from the internet and for the manipulation and removal of some of your files.\n\nIf an update is available then you can continue through the update utility, if not then you can return back to the 'Modify Your Install' screen.\n\n"
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, EnterText)
        text["state"] = DISABLED
        text.place(x=200, y=40)
        
        Button(root, text='Continue', command=lambda: Update_Screen_2(root)).place(x=760, y=500)
        Button(root, text='Back', command=lambda: Start(root)).place(x=680, y=500)
        
    def search_files(directory):
        arr = []
        print(f"Scanning {directory}")
        for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                arr.append(f"{dirpath}\{name}")
        return arr
    
    def remove_files(FileArray, keep_save=False):
        global completion_percent
        try:
            global running_Uninstall
            for i in range(len(FileArray)):
                completion_percent = (100/len(FileArray))*i
                try:
                    if keep_save == True:
                        if not ("Data_Files" in FileArray[i] or "distutils" in FileArray[i] or "pip" in FileArray[i] or "setuptools" in FileArray[i] or "pkg_resources" in FileArray[i] or "README" in FileArray[i]):
                            os.remove(FileArray[i])
                    else:
                        if not ("distutils" in FileArray[i] or "pip" in FileArray[i] or "setuptools" in FileArray[i] or "pkg_resources" in FileArray[i] or "README" in FileArray[i]):
                            os.remove(FileArray[i])

                except Exception as Message:
                    print(Message)
                    
            running_Uninstall = False
        except Exception as Message:
            print(Message)
            running_Uninstall = False
        
        
    def Finish_Uninstall(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Successfully uninstalled Pycraft", background='white', font=(None, 15)).place(x=200, y=35)

        EnterText = "Pycraft has been removed from your computer, you can re-install the project at any time from GitHub, SourceForge or PyPi. If you have experienced any bugs or have any suggestions then feel free to share them on the project page!"
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, EnterText)
        text["state"] = DISABLED
        text.place(x=200, y=40)
        import sys
        Button(root, text='Quit', command=sys.exit).place(x=760, y=500)
        
        root.mainloop()
        
        
    def Remove_All(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Uninstalling Pycraft and all additional files", background='white', font=(None, 15)).place(x=200, y=35)

        OUTPUTtext = "Querying versions"
        CreateText(root, OUTPUTtext)
        
        import main
        version = main.QueryVersion()
        OUTPUTtext += f"\nPreparing to remove {version} and additional files"
        CreateText(root, OUTPUTtext)
        
        FileArray = search_files(PycPath)
        import site
        AdditionalFileArray = search_files(site.getuserbase()+"\\Python310\\site-packages")
        
        FileArray = FileArray+AdditionalFileArray
        OUTPUTtext += f"\nIdentified {len(FileArray)} files to remove"
        CreateText(root, OUTPUTtext)
        
        global running_Uninstall, completion_percent
        completion_percent = 0
        running_Uninstall = True
        threading.Thread(target=remove_files, args=(FileArray,)).start()

        OUTPUTtext += f"\nRemoving {version}"
        CreateText(root, OUTPUTtext)
                
        i = 0
        
        def Render_Progressbar():
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += completion_percent
            root.update()
            
        while running_Uninstall == True:
            root.after(50, Render_Progressbar())
            
        OUTPUTtext += f"\nSuccessfully removed {version} and additional files"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nCleaning Up"
        CreateText(root, OUTPUTtext)
        try:
            os.rmdir(PycPath)
        except:
            pass
        
        OUTPUTtext += f"\nDone"
        CreateText(root, OUTPUTtext)
        Finish_Uninstall(root)

    
    def Remove_But_Keep_Save(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Uninstalling Pycraft and all additional files but keeping save data", background='white', font=(None, 15)).place(x=200, y=35)
        
        OUTPUTtext = "Querying versions"
        CreateText(root, OUTPUTtext)

        import main
        version = main.QueryVersion()
        OUTPUTtext += f"\nPreparing to remove {version} and additional files"
        CreateText(root, OUTPUTtext)
        
        FileArray = search_files(PycPath)
        import site
        AdditionalFileArray = search_files(site.getuserbase()+"\\Python310\\site-packages")
        
        FileArray = FileArray+AdditionalFileArray
        OUTPUTtext += f"\nIdentified {len(FileArray)} files to remove"
        CreateText(root, OUTPUTtext)
        
        global running_Uninstall, completion_percent
        completion_percent = 0
        running_Uninstall = True
        threading.Thread(target=remove_files, args=(FileArray, True,)).start()

        OUTPUTtext += f"\nRemoving {version}"
        CreateText(root, OUTPUTtext)
                        
        def Render_Progressbar():
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += completion_percent
            root.update()
            
        while running_Uninstall == True:
            root.after(50, Render_Progressbar())
            
        OUTPUTtext += f"\nSuccessfully removed {version} and additional files"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nCleaning Up"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nDone"
        CreateText(root, OUTPUTtext)
        
        Finish_Uninstall(root)
        
        
    def Remove_But_Leave(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Uninstalling Pycraft but keeping additional files", background='white', font=(None, 15)).place(x=200, y=35)
        OUTPUTtext = "Querying versions"
        CreateText(root, OUTPUTtext)
        
        import main
        version = main.QueryVersion()
        OUTPUTtext += f"\nPreparing to remove {version}"
        CreateText(root, OUTPUTtext)
                
        FileArray = search_files(PycPath)
        
        OUTPUTtext += f"\nIdentified {len(FileArray)} files to remove"
        CreateText(root, OUTPUTtext)
        
        global running_Uninstall, completion_percent
        completion_percent = 0
        running_Uninstall = True
        threading.Thread(target=remove_files, args=(FileArray,))#.start()
        
        OUTPUTtext += f"\nRemoving {version}"
        CreateText(root, OUTPUTtext)
                
        i = 0
        
        def Render_Progressbar():
            CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
            CompletionProgressbar.place(x=200, y=500)
            CompletionProgressbar['value'] += completion_percent
            root.update()
            
        while running_Uninstall == True:
            root.after(50, Render_Progressbar())
            
        OUTPUTtext += f"\nSuccessfully removed {version}"
        CreateText(root, OUTPUTtext)
        
        OUTPUTtext += f"\nCleaning Up"
        CreateText(root, OUTPUTtext)
        try:
            os.rmdir(PycPath)
        except:
            pass
        
        OUTPUTtext += f"\nDone"
        CreateText(root, OUTPUTtext)

        Finish_Uninstall(root)
        
        
    def Uninstall_Screen_1(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Modify Your Install - Uninstall", background='white', font=(None, 20)).place(x=200, y=35)
        
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, "You have arrived at Pycraft's uninstall utility, here you can remove Pycraft from your system and/or remove the project's additional files, these will be sent to your recycle bin so you have the option to change your mind.\n\nIf you want to feel free to feedback any bugs, ideas or suggestions to the developers who's contact you can find here: https://github.com/PycraftDeveloper/Pycraft")
        text["state"] = DISABLED
        text.place(x=200, y=80)
        
        
        def GetConformation():
            if messagebox.askokcancel("Are you sure with your decision", "Please now take the time to make sure you have chosen correctly as some options will clear all settings and progress made!\n\nPress OK to continue the uninstall process") == True:
                ans = messagebox.askquestion("Permissions manager", "Can we have permission to remove and change some files on your PC?")
                while ans == "no":
                    ans2 = messagebox.askquestion("Caution", "We did not receive permission to remove and modify files on this PC, as a result we cannot uninstall Pycraft, would you like to amend this decision (yes) or close the installer (no)?")
                    if ans2 == "no":
                        quit()
                    else:
                        ans = messagebox.askquestion("Permissions manager", "Can we have permission to remove and change some files on your PC?")
                
                if Uninstall_Option.get() == 1:
                    Remove_But_Keep_Save(root)
                elif Uninstall_Option.get() == 2:
                    Remove_But_Leave(root)
                else:
                    Remove_All(root)
        Button(root, text='Back', command=lambda: Start(root)).place(x=680, y=500)
        Button(root, text='Continue', command=GetConformation).place(x=760, y=500)
        
        Uninstall_Option = IntVar()
        
        Radiobutton(root, text="Remove Pycraft and additional files but keep save data", variable=Uninstall_Option, value=1).place(x=200, y=200)
        Radiobutton(root, text="Remove Pycraft but leave additional files", variable=Uninstall_Option, value=2).place(x=200, y=225)
        Radiobutton(root, text="Remove everything", variable=Uninstall_Option, value=3).place(x=200, y=250)
        Uninstall_Option.set(1)
        
        root.mainloop()
        
        
    def open_img(root, file):
        try:
            import PIL.Image as NotTkinter_Image
            import PIL.ImageTk as NotTkinter_ImageTK  
            global render, load
            try:
                load = NotTkinter_Image.open(file)
            except Exception as Message:
                print(Message)
            render = NotTkinter_ImageTK.PhotoImage(load)
            img = Label(root, image=render)
            img.image = render
            img.place(x=-3, y=-5)
        except Exception as Message:
            messagebox.showerror("Module Not Found", f"This installer requires the module Pillow, this should have been installed automatically if you got this installer from PyPi, or are running this as a (.exe) file.\nIf you have grabbed this installer from GitHub then I advice you to install PIl with the command:\n\npip install pillow\n\nShould any further problems occur then feel free to contact the devloper with the links available at: https://github.com/PycraftDeveloper/Pycraft\n\nFull Error Message: {Message}")
            quit()
            
            
    def CreateDisplay(root):
        try:
            geometry = root.winfo_geometry().split("+")
            Xpos, Ypos = geometry[1], geometry[2]
            root.destroy()
        except:
            Xpos, Ypos = 0, 0
            pass
        root = Tk()
        root.title("Pycraft Setup Wizard")
        root.resizable(False, False)
        root.configure(bg='white')
        root.geometry(f"850x537+{int(Xpos)}+{int(Ypos)}")
        open_img(root, os.path.join(base_folder, ("Resources\Installer_Resources\Banner.png")))
        return root
            
            
    def DownloadandInstall(choice):
        try:
            if choice == "Latest":
                subprocess.check_call([sys.executable, "-m","pip","install","python-pycraft"], False)
            else: #["none", "Pycraft-v0.9.1", "Pycraft-v0.9.2", "Pycraft-v0.9.3"]
                if choice == "Pycraft-v0.9.1":
                    subprocess.check_call([sys.executable, "-m","pip","install","python-pycraft==0.9.1"], False)
                elif choice == "Pycraft-v0.9.2":
                    subprocess.check_call([sys.executable, "-m","pip","install","python-pycraft==0.9.2"], False)
                else:
                    subprocess.check_call([sys.executable, "-m","pip","install","python-pycraft"], False)
        except Exception as Message:
            global InstallError
            InstallError = Message
        else:
            global finished
            finished = True
        
        
    def GetPath():
        temp = subprocess.check_output([sys.executable, "-m","pip","show","python-pycraft"], False)
        global CurrentLocation
        
        tempARR = temp.split(b"\n")
        
        for i in range(len(tempARR)):
            for j in range(len(tempARR[i])):
                if tempARR[i][j:j+10] == b"Location: ":
                    CurrentLocation = tempARR[i][j+10:]
                    
        global finished
        finished = True
        
        
    def GetLocat(root, choice):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Set Install Location", background='white', font=(None, 20)).place(x=200, y=40)
        
        OUTPUTtext = "Now we need to ask one final thing before we start the install, where would you like to store Pycraft?"
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, OUTPUTtext)
        text["state"] = DISABLED
        text.place(x=200, y=80)
        
        global Dir
        Dir = str(base_folder)
        
        
        def GetDir():
            global Dir
            Dir = filedialog.askdirectory()
            
            if len(Dir) >= 80:
                Dir2 = Dir[:80]+"..."
            else:
                Dir2 = Dir
                
            global CurrentLocat

            CurrentLocat.destroy()
            CurrentLocat = Label(root, text=("  "+Dir2+"  "), background='white', relief=RIDGE)
            CurrentLocat.place(x=313, y=152.5)
            
            root.update_idletasks()
            
            
        def GoBack():
            global ChooseBETA
            if ChooseBETA == True:
                SelectVersion(root)
            else:
                InstalInfo(root, ChooseBETA)
            
                
        Button(root, text="Choose file location", command=GetDir).place(x=200, y=150)
        
        global CurrentLocat
        CurrentLocat = Label(root, text=("  "+Dir+"  "), background='white', relief=RIDGE)
        CurrentLocat.place(x=313, y=152.5)
        
        Button(root, text='Continue', command=lambda: Install(root, choice)).place(x=760, y=500)
        Button(root, text='Back', command=GoBack).place(x=680, y=500)
        
        root.update_idletasks()
        
        
    def finishedGUI(root, choice):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Successfully Installed Pycraft", background='white', font=(None, 20)).place(x=200, y=40)
        
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, f"Successfully installed {choice} we hope that you enjoy using this project. This installer can be opened from Pycraft by clicking on the 'Installer' option on the main menu. The installer will appear differently when you open it from Pycraft, from there you will be able to change these settings again under the 'Modify' section, but you also have the option to 'Repair', 'Uninstall' and 'Update' Pycraft. For now though we have finished the install but we have some final options which will be applied when the GUI closes:\nDo you want to add Pycraft to the desktop?\nAdditionally do you want to add Pycraft to the start (recommended)?\nYou also have the option to view the release notes for this install as well.\nThanks for installing Pycraft!")
        text["state"] = DISABLED
        text.place(x=200, y=80)
        
        CS = BooleanVar(value=True)
        CSS = BooleanVar(value=False)
        RelNot = BooleanVar(value=True)
        
        global CreateDSKShortcut, CreateSTRTShortcut, ReleaseNotes, Dir
        
        CreateDSKShortcut = True
        CreateSTRTShortcut = False
        ReleaseNotes = True
        
        Config = {"PATH":Dir}
        with open(os.path.join(base_folder, ("Data_Files\\InstallerConfig.json")), 'w') as openFile:
            json.dump(Config, openFile)
        
        
        def DesktopisChecked():
            global CreateDSKShortcut
            CreateDSKShortcut = CS.get()
            
            
        def StartisChecked():
            global CreateSTRTShortcut
            CreateSTRTShortcut = CSS.get()
        
        
        def ToggleRelNot():
            global ReleaseNotes
            ReleaseNotes = RelNot.get()
            
            
        def OnExit():
            global Dir
            try:
                if CreateDSKShortcut == True:
                    import os, win32com.client
                    
                    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                    
                    shell = win32com.client.Dispatch("WScript.Shell")
                    
                    shortcut = shell.CreateShortCut(os.path.join(desktop, 'Pycraft.lnk'))
                    shortcut.Targetpath = Dir+"/Pycraft/main.py"
                    shortcut.IconLocation = Dir+"/Pycraft/Resources/Folder_Resources/FolderIcon.ico"
                    shortcut.save()
                    
                if CreateSTRTShortcut == True:
                    try:
                        from win32com.shell import shell, shellcon
                        import win32com.client
                        import os
                        
                        start = shell.SHGetSpecialFolderPath(0,shellcon.CSIDL_COMMON_STARTMENU)

                        shell = win32com.client.Dispatch("WScript.Shell")
                        shortcut = shell.CreateShortCut(os.path.join(start, 'Programs\\Pycraft.lnk'))
                        shortcut.Targetpath = Dir+"/Pycraft/main.py"
                        shortcut.IconLocation = Dir+"/Pycraft/Resources/Folder_Resources/FolderIcon.ico"
                        shortcut.save()
                    except:
                        messagebox.showwarning("Permission Denied", "You need to run this program as an administrator to be able to use this function")
                    
                if ReleaseNotes == True:
                    import webbrowser
                    webbrowser.open('https://github.com/PycraftDeveloper/Pycraft')
            except Exception as Message:
                messagebox.showerror("An error occurred", f"Pycraft has successfully installed but some of your final configurations have not been made, this will change in later versions of Pycraft but a quick fix is trying to restart the installer, files downloaded already will be automatically skipped in the download and install. Also this is an early version of the installer, small issues like this will be fixed in later versions of Pycraft that are build around the installer.\n\nFull error message: {Message}")
            quit()


        Checkbutton(root, text="Create desktop shortcut on exit", variable=CS, onvalue=True, offvalue=False, command=DesktopisChecked).place(x=200, y=250)
        Checkbutton(root, text="Create shortcut to start on exit", variable=CSS, onvalue=True, offvalue=False, command=StartisChecked).place(x=200, y=275)
        Checkbutton(root, text="View more details about Pycraft online (on GitHub)", variable=RelNot, onvalue=True, offvalue=False, command=ToggleRelNot).place(x=200, y=300)
        
        Button(root, text='Finish', command=OnExit).place(x=760, y=500)
        
        root.update_idletasks()


    def Install(root, choice):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Downloading and installing Pycraft", background='white', font=(None, 20)).place(x=200, y=40)
                
        ans = messagebox.askquestion("Permissions manager", "Can we have permission to download files from the internet and also modify files on this PC at any time using this Installer?")
        retry = True
        
        while retry == True:
            if ans == "yes":
                retry = False

                OUTPUTtext = "Querying versions"
                CreateText(root, OUTPUTtext)
                
                i = 0
                
                global finished, Dir, CurrentLocation, ThreadError

                ThreadError = None
                CurrentLocation = None
                infoVers = None
                
                if choice == "Latest":
                    OUTPUTtext += f"\nFound latest version as: Pycraft v0.9.3"
                    CreateText(root, OUTPUTtext)
                    infoVers = f"Pycraft v0.9.3"
                else:
                    OUTPUTtext += f"\nFound requested version as: {choice}"
                    CreateText(root, OUTPUTtext)
                    infoVers = choice
                    
                OUTPUTtext += f"\nDownloading and installing {infoVers} and the latest versions of it's dependencies (This will take a moment)"
                CreateText(root, OUTPUTtext)
                
                threading.Thread(target=DownloadandInstall, args=(choice,)).start()
                
                finished = False
                start = time.perf_counter()
                global InstallError
                InstallError = None
                while finished == False:
                    if not InstallError == None:
                        messagebox.showerror("An error ocurred", f"We were unable to install the additional files Pycraft needs in-order to install.\n\nFull Error Message: {InstallError}")
                        quit()
                    CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
                    CompletionProgressbar.place(x=200, y=500)
                    CompletionProgressbar['value'] += i
                    root.update_idletasks()
                    i += 1
                    time.sleep(0.01)
                    
                installtime = time.perf_counter()-start
                
                OUTPUTtext += f" - done in {round(installtime, 4)} seconds"
                CreateText(root, OUTPUTtext)
                
                dependencies = ['wheel', 'Gputil', 'Moderngl', 'Moderngl-window', 'Numpy', 'Pillow', 'Psutil', 'Py-Cpuinfo', 'PyAutoGUI', 'Pygame', 'PyOpenGL', 'PyOpenGL-Accelerate', 'PyWaveFront', 'Tabulate']
                
                for i in range(len(dependencies)):
                    OUTPUTtext += f"\nSuccessfully installed: {dependencies[i]}"
                    CreateText(root, OUTPUTtext)
                                
                OUTPUTtext += "\nMoving Pycraft to selected install location"
                CreateText(root, OUTPUTtext)
                
                
                def MoveFiles():
                    global Dir
                    global CurrentLocation
                    global ThreadError
                    
                    temp = str(CurrentLocation.decode('UTF-8'))[:-1]
                    try:
                        shutil.copytree(fr"{temp}\Pycraft", Dir+"/Pycraft")
                        shutil.copyfile(base_folder+"/Installer.py", Dir+"/Pycraft/Installer.py")
                        shutil.copyfile(base_folder+"/Data_Files/InstallerConfig.json", Dir+"/Pycraft/Data_Files/InstallerConfig.json")
                    except Exception as Message:
                        global InstallError
                        InstallError = Message
                    else:
                        ThreadError = None
                    global finished
                    finished = True
                    
                    
                finished = False
                InstallError = None
                
                threading.Thread(target=GetPath).start()
                
                while finished == False:
                    if not InstallError == None:
                        messagebox.showwarning("Install Warning", "An error has occurred during the install of Pycraft, this installer is new so this is likely to occur, also this error will display on versions of Pycraft that are older than Pycraft v0.9.4. This error is not serious but many not lead to a smooth experience.")
                    CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
                    CompletionProgressbar.place(x=200, y=500)
                    CompletionProgressbar['value'] += i
                    root.update_idletasks()
                    i += 1
                    time.sleep(0.01)
                    
                finished = False
                
                threading.Thread(target=MoveFiles).start()
                
                while finished == False:
                    CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
                    CompletionProgressbar.place(x=200, y=500)
                    CompletionProgressbar['value'] += i
                    root.update_idletasks()
                    i += 1
                    time.sleep(0.01)
                    
                if ThreadError == None:
                    OUTPUTtext += " - done"
                    CreateText(root, OUTPUTtext)
                else:
                    OUTPUTtext += " - error"
                    CreateText(root, OUTPUTtext)
                    while not ThreadError == None:
                        print(ThreadError)
                        
                        if str(ThreadError)[0:13] == "[WinError 32]":
                            messagebox.showerror("File is in use in another process", "We cannot remove the previous folder because it is in use by another program, please try again")
                            try:
                                shutil.rmtree(Dir+"/Pycraft")
                            except Exception as Message:
                                ThreadError = Message
                                continue
                                    
                            OUTPUTtext += " - done"
                            CreateText(root, OUTPUTtext)
                        if str(ThreadError)[0:14] == "[WinError 183]":
                            ans = messagebox.askyesno("A duplicate folder was detected", "We were unable to complete the install because a folder called 'Pycraft' already exists on your system, would you like to replace this file (and move the old one to trash?)")
                            if ans == True:
                                text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
                                OUTPUTtext += "\nRemoving old files"
                                CreateText(root, OUTPUTtext)
                                
                                try:
                                    shutil.rmtree(Dir+"/Pycraft")
                                except Exception as Message:
                                    ThreadError = Message
                                    continue
                                
                                OUTPUTtext += " - done"
                                CreateText(root, OUTPUTtext)
                                
                                OUTPUTtext += f"\nMoving Pycraft to selected install location"
                                CreateText(root, OUTPUTtext)
                                
                                finished = False
                    
                                RelocateFiles = threading.Thread(target=MoveFiles)
                                RelocateFiles.start()
                                
                                while finished == False:
                                    CompletionProgressbar = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
                                    CompletionProgressbar.place(x=200, y=500)
                                    CompletionProgressbar['value'] += i
                                    root.update_idletasks()
                                    i += 1
                                    time.sleep(0.01)
                                    
                                OUTPUTtext += " - done"
                                CreateText(root, OUTPUTtext)
                        else:
                            messagebox.showerror("An error has occurred", f"We were unable to move Pycraft to the requested install location.\n\nFull Error Message:\n{ThreadError}")
                            quit()
                    
                OUTPUTtext += "\nSuccessfully Installed Pycraft"
                CreateText(root, OUTPUTtext)
                
                Button(root, text='Continue', command=lambda: finishedGUI(root, choice)).place(x=760, y=500)
                root.update_idletasks()
            else:
                ans2 = messagebox.askquestion("Caution", "We did not receive permission to download files from the internet and modify files on this PC, as a result we cannot install Pycraft, would you like to amend this decision (yes) or close the installer (no)?")
                if ans2 == "no":
                    quit()
                else:
                    retry = True
                    ans = messagebox.askquestion("Permissions manager", "Can we have permission to download files from the internet and also modify files on this PC at any time using this Installer?")


    def SelectVersion(root):
        root = CreateDisplay(root)
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        
        if ChooseBETA == True:
            Label(root, text="Please choose your Pycraft version to install.\nYou may want to move them to dedicated folders because the installer will overwrite any previous folder in your install location (which you can do on the next page).", background='white', font=(None, 20)).place(x=200, y=40)
            
            continueButton = Button(root, text='Continue')
            continueButton.place(x=760, y=500)
            continueButton["state"] = DISABLED
            
            versions = ["none", "Pycraft-v0.9.1", "Pycraft-v0.9.2", "Pycraft-v0.9.3"]
            
            VersionChoice = StringVar()
            VersionChoice.set(versions[0])
            
            
            def display_selected(choice):
                choice = VersionChoice.get()
                continueButton = Button(root, text='Continue', command=lambda: GetLocat(root, choice)) # This needs changing to the get directory window
                continueButton.place(x=760, y=500)
                continueButton["state"] = NORMAL
                root.update_idletasks()
                
                
            text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
            text.insert(INSERT, "Below there is a dropdown box, please choose the Pycraft version to install, only versions of Pycraft published on PyPi are available for download.\nAfter making your choice, please press continue to start the install.")
            text["state"] = DISABLED
            text.place(x=200, y=80)
        
            OptionMenu(root, VersionChoice, *versions, command=display_selected).place(x=200, y=150)
        else:
            Label(root, text="Installing the latest version of Pycraft", background='white', font=(None, 20)).place(x=200, y=40)
            
            text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
            text.insert(INSERT, "Downloading and installing the latest version of Pycraft")
            text["state"] = DISABLED
            text.place(x=200, y=80)
        
        
    def InstalInfo(root):
        root = CreateDisplay(root)
        
        Label(root, text="Pycraft's Installation Assistant", background='white', font=(None, 20)).place(x=200, y=0)
        Label(root, text="Important Information", background='white', font=(None, 20)).place(x=200, y=35)
        
        text = Text(root, wrap=WORD, relief=FLAT, font=(None, 10))
        text.insert(INSERT, "Please read the below information, once you have familiarised yourself with the information, please tick the box to say that you have and then press continue to start the installation. Use the scroll wheel to scroll the text.\n\nYou can find Pycraft's GitHub repository here for more information: https://github.com/PycraftDeveloper/Pycraft\n\nThe program will be updated frequently and I shall do my best to keep this up to date too. I also want to add that you are welcome to view and change the program and share it with your friends. If you find any bugs or errors, please feel free to comment in the comments section any feedback so I can improve my program, it will all be much appreciated and give as much detail as you wish to give out.\n\n\nLicence\nMIT License\n\nCopyright (c) 2021 Thomas Jebbo\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
        text["state"] = DISABLED
        text.place(x=200, y=80)
        
        var1 = IntVar()
        
        
        def ChooseNextStep():
            if ChooseBETA == True:
                SelectVersion(root)
            else:
                choice = "Latest"
                GetLocat(root, choice)
        
        
        def ButtonCheck():
            data = var1.get()
            if data == None or data == 0:
                continueButton = Button(root, text='Continue')
                continueButton.place(x=760, y=500)
                continueButton["state"] = DISABLED
            else:
                continueButton = Button(root, text='Continue', command=ChooseNextStep)
                continueButton.place(x=760, y=500)
                continueButton["state"] = NORMAL
                root.update_idletasks()
                
                
        ButtonCheck()
        
        Radiobutton(root, text='I have not read the above text', variable=var1, value=0, command=ButtonCheck).place(x=200, y=475)
        Radiobutton(root, text='I have read the above text', variable=var1, value=1, command=ButtonCheck).place(x=200, y=500)
            
        Button(root, text='Back', command=lambda: Start(root)).place(x=680, y=500)
        
        
    root = None

    global ChooseBETA
    ChooseBETA = False

    root = CreateDisplay(root)

    Start(root)

    root.mainloop()
    
if __name__ == "__main__":
    runInstaller()