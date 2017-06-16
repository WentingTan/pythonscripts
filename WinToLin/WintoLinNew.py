#Make sure you backup folders
#Manual part:

#1, /home/picarro/SI2000/AppConfig/Config/AlarmSystem/AlarmSystem_Code.ini
# and add options in supervisor.ini   

import sys, os, re, getopt, shutil, errno

if hasattr(sys, "frozen"): #we're running compiled with py2exe
    AppPath = sys.executable
else:
    AppPath = sys.argv[0]

APP_NAME = "WintoLin"



# rule: 1, what config files to pass; 2, what  
class WintoLin(object):
    def __init__(self, configPath, *args):
        
        self.dfs(configPath)

    def dfs(self, path):
        for item in os.listdir(path):
            here = os.path.join(path, item)
            if os.path.isdir(here):
                #print "In dir:", here
                self.dfs(here)
            elif os.path.isfile(here):
                filename, file_extension = os.path.splitext(here)
                if file_extension == '.ini':
                    #print "Ini file: ", here
                    self.conversion(here)
        #return
    def conversion(self, filename):
        contents = None
        f = open(filename, 'r')
        lines = f.readlines()
        contents= ''.join(lines)
        f.close()
        fout = None
        if filename.endswith("Driver.ini"):
            print "************************In file:", filename
            for i in xrange(len(lines)):
                if "../../../" in lines[i]:
                    print "-------------Ori Line-------------"
                    print lines[i]
                    lines[i] = lines[i].replace('../../../','/home/picarro/SI2000/')
                    print "--------------Changed to------------>"
                    print lines[i]
                if "../../version.ini" in lines[i]:
                    print "-------------Ori Line-------------"
                    print lines[i]
                    lines[i] = lines[i].replace('../../version.ini','/home/picarro/SI2000/AppConfig/version.ini')
                    print "--------------Changed to------------>"
                    print lines[i]
                if "HostExe/" in lines[i]:
                    print "-------------Ori Line-------------"
                    print lines[i]
                    lines[i] = lines[i].replace('HostExe/Images/analyzerUsb.hex','Firmware/CypressUSB/analyzer/analyzerUsb.hex')
                    lines[i] = lines[i].replace('HostExe/Images/dspMain.hex','Firmware/DSP/src/Debug/dspMain.hex')
                    lines[i] = lines[i].replace('HostExe/Images/top_io_map.bit','Firmware/MyHDL/Spartan3/top_io_map.bit')
                    print "--------------Changed to------------>"
                    print lines[i]
            #self.updateFile(filename, lines)
        if "supervisorEXE" in filename:
            print "************************In file:", filename
            for i in xrange(len(lines)):
                if "LaunchArgs" in lines[i]:
                    print "-------------Ori Line-------------"
                    print lines[i]
                    lines[i] = lines[i].replace('../','../../')
                    print "--------------Changed to------------>"
                    print lines[i]
        
        if filename.endswith("CommandInterface.ini"):
            print "************************In file: ", filename
            for i in xrange(len(lines)):
                if "COM1" in lines[i]:
                    print "-------------Ori Line-------------"
                    print lines[i]
                    lines[i] = lines[i].replace('COM1','/dev/ttyS0')
                    print "--------------Changed to------------>"
                    print lines[i]                    
            #self.updateFile(filename, lines)
        return
        if "HostExe" in contents or "Hostexe" in contents:
            print "************************In file:", filename
            for i in xrange(len(lines)):
                if "HostExe" in lines[i] or "Hostexe" in lines[i]:
                    print "-------------Ori Line-------------"             
                    print lines[i]
                    lines[i] = lines[i].replace('HostExe','Host/pydCaller')
                    lines[i] = lines[i].replace('Hostexe','Host/pydCaller')
                    print "--------------Changed to------------>"
                    print lines[i]
            #self.updateFile(filename, lines)

        if '.exe' in contents:
            print "************************In file:", filename
            for i in xrange(len(lines)):
                if ".exe" in lines[i]:
                    print "-------------Ori Line-------------"             
                    print lines[i]
                    lines[i] = lines[i].replace('.exe','.py')
                    print "--------------Changed to------------>"
                    print lines[i]               
            #self.updateFile(filename, lines)

        if "C:" in contents:
            print "************************In file:", filename
            for i in xrange(len(lines)):
                if "C:" in lines[i]:
                    print "-------------Ori Line-------------"
                    print lines[i]      
                    lines[i] = lines[i].replace('C:\Picarro\G2000', '/home/picarro/SI2000')
                    lines[i] = lines[i].replace('C:/Picarro/G2000', '/home/picarro/SI2000')
                    lines[i] = lines[i].replace('C:/Picarro', '/home/picarro')
                    lines[i] = lines[i].replace('C:\\Picarro', '/home/picarro')
                    lines[i] = lines[i].replace('C:','/home')
                    #lines[i] = lines[i].replace('C:\\','/home/')
                    lines[i] = lines[i].replace('\\', '/')
                    print "--------------Changed to------------>"
                    print lines[i]               
            #self.updateFile(filename, lines)
        return

    def updateFile(self, filename, lines):
        newfiledata = ''.join(lines)
        newfile = filename+ '.new'
        fout = open(newfile, 'w')
        fout.write(newfiledata)
        fout.close()
        os.remove(filename)
        os.rename(newfile, filename)
        #        match = re.search(r'(.+)C\:\\Picarro\\G2000(.+)', lines[i])

HELP_STRING = """WintoLin.py [-c<FILENAME>] [-h|--help]

Where the options can be a combination of the following:
-h, --help           print this help
-c                   specify a config file:  default = "Current Dir"
"""

def printUsage():
    print HELP_STRING

def handleCommandSwitches():
    shortOpts = 'hc:s'
    longOpts = ["help"]
    try:
        switches, args = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
    except getopt.GetoptError, E:
        print "%s %r" % (E, E)
        sys.exit(1)
    #assemble a dictionary where the keys are the switches and values are switch args...
    options = {}
    for o,a in switches:
        options.setdefault(o,a)
    if "/?" in args or "/h" in args:
        options.setdefault('-h',"")
    #Start with option defaults...
    configPath = '.'
    
    if "-h" in options or "--help" in options:
        printUsage()
        sys.exit()
    if "-c" in options:
        configPath = options["-c"]

    return configPath

configPath = handleCommandSwitches()
#CONFIG = ConfigObj(configFile)
#ini_CONFIG = copy.deepcopy(CONFIG)


if __name__ == '__main__':
    WintoLin(configPath)

    


