# Tsaaro SynD Application Installer


## Using Pyinstaller


PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.
The minimum required version is now Python 3.6. The last version supporting Python 2.7 was PyInstaller 3.6. 


#### Installation:


PyInstaller is a normal Python package. You can download the archive from PyPi, but it is easier to install using pip where it is available:


        pip install pyinstaller
        

To verify whether pyinstaller is installed succeccfully:


        pyinstaller --version
        
    
#### To convert .py file to an executable:

In command prompt, move to the directory where the corresponding file which needs to be converted into an executable file is present, and enter the following command:


        pyinstaller --onefile cli_fire.py
        
        
Here, **cli_fire.py** is the file name that needs to be converted. The build was successful and the output was the following:


        INFO: PyInstaller: 3.6
        INFO: Python: 3.8.5 (conda)
        INFO: Platform: Windows-10-10.0.19041-SP0
        INFO: wrote C:\Users\vimal\Desktop\Programs\Tsaaro\SynDApp-feature\engine\test\cli_fire.spec
        INFO: UPX is not available.
        INFO: Extending PYTHONPATH with paths
        ['C:\\Users\\vimal\\Desktop\\Programs\\Tsaaro\\SynDApp-feature\\engine\\test',
        'C:\\Users\\vimal\\Desktop\\Programs\\Tsaaro\\SynDApp-feature\\engine\\test']
        INFO: checking Analysis
        .
        .
        .
        INFO: Building EXE from EXE-00.toc
        INFO: Appending archive to EXE C:\Users\vimal\Desktop\Programs\Tsaaro\SynDApp-feature\engine\test\dist\cli_fire.exe
        INFO: Building EXE from EXE-00.toc completed successfully.
        
        
It created two directories **dist** and **build** and a file **cli_fire.spec** in the working directory.


    ..test\
        __pycache__\
        build\
            cli_fire\
        dist\
            cli_fire.exe
        cli_fire.py
        cli_fire.spec


when I run the **cli_fire.exe** in dist directory with the following command:


        C:\...\engine\test\dist>cli_fire -h
 
        
I got a traceback:


        Traceback (most recent call last):
          File "cli_fire.py", line 1, in <module>
        ModuleNotFoundError: No module named 'fire'
        [18396] Failed to execute script cli_fire
 
        
**cli_fire.py**


    import fire
    from getpass import getpass
    
    class Auth(object):
        def login(self, username = None):
            if username == None:
                username = input("Username: ")
            pw = getpass("Password: ")
            return username, pw
    
    class Calculator(object):
      def add(self, x, y):
        return x + y
    
      def multiply(self, x, y):
         return x * y

    class tsaaro(object):
        def __init__(self):
            self.auth = Auth()
            self.math = Calculator()
    
    fire.Fire(tsaaro)
 
    
To solve this error, we need to specify the **fire** module in the **hiddenimports=[]** of cli_fire.spec file, we can do this by **--hidden-import** flag in the command:


    pyinstaller --onefile --hidden-import "fire" cli_fire.py

    
or specify the module 'fire' in cli_fire.spec file


    a = Analysis(['cli_fire.py'],
     pathex=['C:\\Users\\vimal\\Desktop\\Programs\\Tsaaro\\SynDApp-feature\\engine\\test'],
     .
     .
     hiddenimports=['fire'],
     .
 
 
     .
This is the possible solution for **ModuleNotFoundError**, but this doen't seem to work in this case, we are getting the same error.


    C:\...\engine\test\dist>cli_fire -h

    Traceback (most recent call last):
      File "cli_fire.py", line 1, in <module>
    ModuleNotFoundError: No module named 'fire'
    [10804] Failed to execute script cli_fire


This should be working fine by this situation, the there is an unknown error in the background which couldn't be solved by almost all the possible solutions available in the resources.


Apparently, In order to convert .py file into an executable, we have an alternate python module **auto-py-to-exe**.


## Using Auto-py-to-exe


Auto-py-to-exe is a .py to .exe converter using a simple graphical interface and PyInstaller in Python.


#### Prerequisites:
* Python : 3.6-3.10
* Default browser (ex: chrome)


#### Installation:
You can install this project using PyPI:


    pip install auto-py-to-exe

    
Then to run it, execute the following in the terminal:


    auto-py-to-exe


If it didn't run and produces the output as:

    
    'auto-py-to-exe' is not recognized as an internal or external command,
    operable program or batch file.

    
Execute the following command to run it:


    python -m auto_py_to_exe

    
It will open a user interface,



Select the file which needs to be converted into executable by clicking the browse button or mention the path of the file in the corresponding space provided in **Script Location**. And, to make the executale as one file, select **One File** button below Script Location.


![auto-py-to-exe file location](https://drive.google.com/file/d/1LOgW8XpgstnTSgHqgpef5iDfHw7o3N7c/view?usp=sharing)


In the **Advanced** section, mention **fire** in the **--hidden-import** input under "what to bundle, where to search" part.


![auto-py-to-exe hidden import](https://drive.google.com/file/d/1kivkDFmHhKWiJBaaTaQrPClVGqsJuc4m/view?usp=sharing)


Then click on **CONVERT .PY TO .EXE**


![auto-py-to-exe convert](https://drive.google.com/file/d/1k9uO0Q7btbBBvJN22hXOoPiP_Ig4w9-1/view?usp=sharing)


Successful execution will look like this,


![auto-py-to-exe output](https://drive.google.com/file/d/1TiIdX7FU_iqxv4tAIPuq46sNAbfofmCc/view?usp=sharing)


This will create an **output** directory in the directory in which the .py file is present.


    ..engine\test\
        __pycache__\
        output\
            cli_fire.exe
        cli_fire.py



Now, to run the executable, execute the following command:


    C:\...\output>cli_fire 


Successful execution will produce an output like this:


    NAME
        cli_fire.py
    SYNOPSIS
        cli_fire.py GROUP
    GROUPS
        GROUP is one of the following:
         auth
         math





