# Open Mindset app

A 💯% `Python` application using the `KivyMD` framework, integrating Artificial Intelligence features. The goal is to have a single `Python` codebase that can be built and deployed on all major native platforms: `Android`, `iOS`, `macOS`, `Linux` and `Windows`.

Some of the goals of the app:

- `KivyMD` app skeleton pattern including classique UI elements (navbar menu, top navbar, responsive, material design...)
- learn and demonstrate best programming practices in a 💯% `Python` development environment
- experiment with a lot of AI-related stuff
  - `OpenAI` `ChatGPT` API
  - `Stability AI` `text to image` API
  - plus more AI useful examples in a mobile/native app context
- document recipes for building artifacts of specific native OS
- have concrete examples of broadcasting events and react to these events through an MVC pattern
- and much more as we experiment with nice AI and existing technologies and other open-source libraries...

![GitHub release (latest by date)](https://img.shields.io/github/v/release/amwebexpert/poc-mobile-python) ![GitHub Release Date](https://img.shields.io/github/release-date/amwebexpert/poc-mobile-python) ![GitHub last commit](https://img.shields.io/github/last-commit/amwebexpert/poc-mobile-python) ![GitHub](https://img.shields.io/github/license/amwebexpert/poc-mobile-python)

* Some screen captures of the implemented features

Platform     | About screen | Chat session | Settings
------------ | ------------ | ------------ | -------------- |
Android      | <img src="stores_presence/android-about.jpg" /> | <img src="stores_presence/android-chatgpt-session.jpg" /> | <img src="stores_presence/android-settings.jpg" />
iOS          | <img src="stores_presence/ios-about.png" /> | <img src="stores_presence/ios-chatgpt-session.png" /> | <img src="stores_presence/ios-settings.png" />
Linux        | <img src="stores_presence/ubuntu-about.png" /> | <img src="stores_presence/ubuntu-chatgpt-session.png" /> | <img src="stores_presence/ubuntu-settings.png" />
Windows      | <img src="stores_presence/windows-about.png" /> | <img src="stores_presence/windows-chatgpt-session.png" /> | <img src="stores_presence/windows-settings.png" />
macOS        | <img src="stores_presence/macos-about.png" /> | <img src="stores_presence/macos-chatgpt-session.png" /> | <img src="stores_presence/macos-settings.png" />


## Table of content

- [Open Mindset app](#open-mindset-app)
  - [Table of content](#table-of-content)
  - [Getting Started](#getting-started)
    - [Startup \& hot reload](#startup--hot-reload)
    - [Simulating a mobile device on desktop](#simulating-a-mobile-device-on-desktop)
  - [Utilities](#utilities)
    - [Preview list of Material Design implemented icons](#preview-list-of-material-design-implemented-icons)
    - [DB Browser for SQLite](#db-browser-for-sqlite)
    - [Snippet to see the layout border of any widget](#snippet-to-see-the-layout-border-of-any-widget)
  - [Managing development environment](#managing-development-environment)
    - [Python on MacOS with brew](#python-on-macos-with-brew)
    - [Certify installation](#certify-installation)
    - [Virtual environment](#virtual-environment)
    - [Dependency libraries (update, freeze them or install from)](#dependency-libraries-update-freeze-them-or-install-from)
      - [References](#references)
  - [Build for Android](#build-for-android)
    - [Building for Android on Linux Ubuntu](#building-for-android-on-linux-ubuntu)
      - [References](#references-1)
    - [Building for Android on macOS](#building-for-android-on-macos)
      - [Reference](#reference)
  - [Building for iOS](docs/build_ios.md) (seperate file in docs)
  - [About Kivy framework](#about-kivy-framework)
  - [About the app name](#about-the-app-name)


## Getting Started


You may have some OS core dependencies to install (`dll` on Windows, system lib on Ubuntu, etc.) so follow the official Kivy install instructions depending on your operating system(s):

- [Kivy Framework](https://kivy.org)
- [KivyMD](https://kivymd.readthedocs.io)

Example: for Ubuntu you have to set the following environnement variable
   ```shell
    export USE_X11=1
   ```
and install the listed [OS libraries](https://kivy.org/doc/stable/installation/installation-linux.html#id1)


### Other users can start here :point_down:<a id="create-venv"></a>

Then you can install the Open Mindset app dependencies as follow. First create and activate your virtual environment:

   ```shell
    python -m venv venv
    . venv/bin/activate
   ```

Use `pip-tools` to generate `requirements.txt` file from `requirements.in`:

   ```shell
    python -m pip install pip-tools
    pip-compile requirements.in
   ```

Update the virtual environment dependencies:

   ```shell
   pip-sync
   ```

### :point_right: Missing packages for Mac OS install :point_left:
```
pip install pygame
pip install kivy==2.2.1
```

### Startup & Hot Reload

Normal startup

    python main.py

With hot-reload enabled

    DEBUG=1 python main.py

Know issue in `DEBUG` mode:

- Pressing the *space bar* from the query textinput field of the chat session triggers an unexpected hot reload event.

### Simulating a mobile device on desktop

Normal startup

    MOBILE_SIMULATION=1 python main.py

Combined with hot-reload

    DEBUG=1 MOBILE_SIMULATION=1 python main.py

## Utilities

### Preview list of Material Design implemented icons

    python scripts/icons/main.py

### DB Browser for SQLite

This native Python app makes usage of SQLite3 as it's persistence mechanism (preferences, chat session...). Although you can visualize raw data using command lines like `sqlite3 chat_sessions.db` we recommand using the [DB Browser for SQLite](https://sqlitebrowser.org/) which is a high quality, visual, open source tool to create, design, and edit database files compatible with SQLite.

### Snippet to see the layout border of any widget

Inside the `.kivy` file just add this:

```
    canvas.before:
        Color:
            rgba: 0, 1, 0, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
```

## Managing development environment

### Python on MacOS with brew

Some usefull brew commands

    brew update
    brew config
    brew leaves | xargs brew desc --eval-all
    brew cleanup

    brew install cython
    echo 'export PATH="/opt/homebrew/opt/cython/bin:$PATH"' >> ~/.zshrc

Then change your `.zshrc` aliases as [explained here](https://apple.stackexchange.com/a/461063/364767)

### Certify installation

    python ./scripts/certificates/install_certifi.py

## Build for Android

### Building for Android on Linux Ubuntu

First install the following dependencies:

* https://kivy.org/doc/stable/installation/installation-linux.html#id1

Then install these python dependencies:

    pip-compile
    pip-sync

If `pip-sync` fails you may have to use the classic way once `requirements.txt` is generated by `pip-compile`:

    pip install -r requirements.txt

Ensure both `kivy` and `kivymd` are up to date (see below reference for more detail)

    pip install https://github.com/kivy/kivy/archive/master.zip
    pip install https://github.com/kivymd/KivyMD/archive/master.zip

    buildozer android clean
    buildozer android debug deploy run

#### References

* https://stackoverflow.com/a/76644946/704681

### Building for Android on macOS

    python ~/Library/Python/3.8/lib/python/site-packages/buildozer init
    python ~/Library/Python/3.8/lib/python/site-packages/buildozer android debug deploy run

    python ~/Library/Python/3.11/lib/python/site-packages/buildozer init
    python ~/Library/Python/3.11/lib/python/site-packages/buildozer android debug deploy run

- Ugly workaround for [ssl issue](https://github.com/kivy/kivy/issues/5784):
  code /Library/Frameworks/Python.framework/Versions/Current/lib/python3.10/ssl.py

- sdkmanager path does not exist, [sdkmanager is not installed](https://github.com/kivy/buildozer/issues/927#issuecomment-533020886)

#### Reference

* https://kivy.org/doc/stable/guide/packaging-android.html


## Building for iOS

See seperate iOS build instructions [here](docs/build_ios.md).


## About Kivy framework

Why is Kivy not popular?

Basically runs on donation from people like you and me and some organisations and this is unlike other frameworks that are (or were) backed by giants like Google (Flutter) or Facebook (React Native). So, Kivy might lack marketing funds, making it less popular among other frameworks but it's still a preferred choice in Python ecosystem.

## About the app name

By definition:
> An open mindset is a tendency to be receptive to new ideas and information. Having an open mindset means being objective when approaching new things, listening to other points of view, and being willing to admit what you don't know.

I decided to give it that name since this is my life philosophy and I was looking for a real project to learn `Python` language.

## Official related websites

- [Kivy Framework](https://kivy.org)
- [KivyMD](https://kivymd.readthedocs.io)
