### Installation

    git clone https://bitbucket.org/aecepoglu/easyi3status.git
    pip install -r requirements.txt

### Configuration:

    mkdir ~/.easyi3status
    touch ~/.easyi3status/__init__.py

Then copy your modules into **~/.easyi3status** folder

    #place this in your i3 config
    bar {
    	status_command python -u /path/to/easyi3status/mystatus.py
    }

And you're ready to go
