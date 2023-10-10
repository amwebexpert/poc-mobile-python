# Build iOS
Key notes for these build instructions:
- toolchain (kivy-ios): is active with the python venv is active AND your are in the direcotry that it is installed in.
- These instructions are based on building on arm64 architecture. However, I do not think there is a difference if x86_64 arch is used (as of October 2023). In the past there have been differences.

## Current iOS TestFlight version
For those interested in seeing the latest version you can download it now to your iPhone.
1. [Download](https://testflight.apple.com/join/1gCPBjbZ) iOS TestFlight app.
2. Download Open Mindset iOS from TestFlight app. 
    - The link above will both download TestFlight to your iOS device and then provide the option to download the latest Open Mindset version for testing on your iPhone.


## Step 1: Create and activate venv
This step is the same as [create venv](../README.md#create-venv).
```
 python -m venv mindset
 source mindset/bin/activate
```
Once mindset (or venv) is activated the environment is set to the terminal regardless of the directory your are in.

```
 python -m pip install pip-tools
 pip-compile requirements.in
```
```
pip-sync
```

## Step 2: kivy-ios
Install kivy-ios to pip environment:
```
pip install kivy-ios
```

## Step 3: Create toolchain environment
After adding kivy-ios to your venv (I called mine mindset), create another diretory that will store the Xcode builds from the toolchain software package.

Navigate into KivyBuilds (name of directory I am using to store Xcode project and the toolchain environment).

A file structure I use for this work is
```
_environments/
    mindset/
KivyBuilds/
    # toolchain environment will go here
poc-mobil-python/
```


From inside KivyBuilds/ create the toolchain environemnt
```
toolchain build python3 kivy pillow libffi ffpyplayer 
```
This takes about 20 minutes with a good internet connection.

```
toolchain pip install kivymd kaki watchdog event_bus 
```

### Key Note on toolchain environment
toolchain commands are particlar to the folder where toolchain packages are installed. The gif below demonstrates how your toolchain environment works. Once inside the folder where Step 3 is executed (i.e. KivyBuilds in the file structure example), if you do `toolchain status` you will see all the packages installed. However, if you naviagate outside of that folder toolchain status will return no install pacakges.

<img src="../stores_presence/ios_build/toolchain_env_minus5.gif"/> 

### Background on toolchain/ kivy-ios
toolchain is both the (1) command and (2) pacakge/suite/collection of software availible in kivy-ios package. toolchain suite of software will will convert the python project (poc-mobile-python) to an Xcode project.

## Step 4: Create Xcode project
Again from inside your KivyBuilds/ do the following command:
```
toolchain create openmindset ~/Documents/poc-mobile-python
```
Here openmindset could be anything and the last argument is the path to the Python Kivy project.

## Step 5: Signin to Xcode

Sign in with your [Apple Developer account](https://developer.apple.com/programs/)
<img src="../stores_presence/ios_build/XcodeSignIn.gif" /> 

## Step 6: Build to simulator or iPhone
Select device and press the play button

## Build to TestFlight
1. From inside Xcode select Product menu > Archive
    - This creates a file that will be submitted to App Store Connects
2. After Archive (.xcarchive file) is created select the file from Oragnizer and click "Distribute App".
    - This can also be accessed by Window menu > Organizer
3. There will be a automated process of verifying the package meets Apple requirements
    - one issue we have had is a binary that is not accepted from the toolchain environment. The remedy to this is just delete the file and the package will get accepted.
        - File to delete: KivyBuilds/dist/root/python3/lib/python3.10/site-packages/_watchdow_fsevents.cpython-310-darwin.so
### Other iOS stuff
Note:
- Contributors are welcome to do this one, collected below some beginning instructions with some issues and solutions.
- Rosetta 2 terminal:
  - not required for arm64 machines when using kivy-ios==2.2.1
  - maybe required if you want to deploy on an `iOS iPhone Simulator`

Good article here:
- https://nrodrig1.medium.com/put-kivy-application-on-iphone-update-1cda12e79825

Directories structure (according to medium article above)
```sh
    _environments/
        venv_wshKivy/
    kivyBuilds/
        build/
        dist/
        openmindset-ios/
    openmindset/
```

Build notes and frequently used commands:

- we must clone the app from github *WITHOUT* `venv` (wipe the `venv` folder entirely in order to build ios stuff)
- when doing small code changes within the app, here are the steps to re-create the XCode Project:

```sh
    rm -rf openmindset-ios
    toolchain create openmindset /Users/andre.masson/git/perso/python-projects/openmindset
    cp /Users/andre.masson/git/perso/python-projects/openmindset/data/icon.png openmindset-ios/
    open openmindset-ios/openmindset.xcodeproj
```

### iOS build issues and solution (or workarounds)

- [creating a custom VSCode Rosetta terminal](https://dev.to/markwitt_me/creating-a-custom-vscode-terminal-profile-for-using-rosetta-on-an-m1-mac-apple-silicon-2gb2) However I discovered that the raw macOS terminal (see link below) was working in all cases while I had some obscur issues with the VSCode Rosetta terminal so be carefull
- [launch macOS terminal in Rosetta mode](https://apple.stackexchange.com/a/409774/364767)
- [command to know current rosetta mode](https://stackoverflow.com/a/67690510/704681) (1 === rosetta, 0 !== rossetta)
    - `sysctl -n sysctl.proc_translated`
    - `arch`
      - will display `arm64` for ARM architecture
      - will display `x86_64` (or `i386`) for rosetta architecture
- Very slow `iOS Simulator` [discussed here](https://stackoverflow.com/questions/59570740/bad-xcode-iphone-simulator-performance-python-kivy-app)
- duplicate symbol about `libsdl2_ttf.a` and `libfreetype.a`
  - https://github.com/kivy/kivy-ios/issues/787#issuecomment-1489027427
    Since `sdl2_ttf` now builds its own version of `libfreetype`, we will need to update some of our recipes accordingly.
    as a workaround, you're likely good to just remove `libfreetype.a` from "Frameworks, Libraries and embedded content"

For some reason you may have to downgrade cython for kivy build to succeed. The cython specific version to use:

	pip install cython==0.29.36

Bypass macOS default built in python version:

     sudo ln -fs /Library/Frameworks/Python.framework/Versions/3.10/bin/python3 /usr/local/bin/python

XCode build failure

    rsync warning: some files vanished before they could be transferred (code 24) at /AppleInternal/BuildRoot/Library/Caches/com.apple.xbs/Sources/rsync/rsync-54.120.1/rsync/main.c(996) [sender=2.6.9]
    Command PhaseScriptExecution failed with a nonzero exit code

Solution from [here](https://github.com/kivy/kivy-ios/issues/513#issuecomment-646689846)

    % cd
    % toolchain build python3 kivy openssl
    % toolchain create <my_app_name> <full_path_to_my_app_source_directory>
    % open <my_app_name>-ios/<my_app_name>.xcodeproj
