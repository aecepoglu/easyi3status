
### Configuration:

    mkdir ~/.easyi3config
    touch ~/.easyi3config/__init__.py

Then copy your modules into **~/.easyi3config** folder

    #place this in your i3 config
    bar {
    	status_command python -u /path/to/easyi3status/mystatus.py
    }

And you're ready to go
