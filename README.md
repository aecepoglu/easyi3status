# easyi3status

An easy and modular i3-status application.

## To Install

pip installer is on its way.

To install manually:

1. `git clone git@github.com:aecepoglu/easyi3status.git`
2. edit your `~/.i3/config` like so

    bar {
        status_command python3 /YOUR/PATH/TO/easyi3status/__init__.py
        font pango:Monospace Sans Mono, Icons 10
    }
3. Add a module (follow the instructions here: [link](http://easyi3status.herokuapp.com/assets/1))
4. Create the file `~/.config/easyi3status/config.yaml` like so:

    modules:

## To Configure

The [yaml](http://yaml.org) configuration file is at `~/.config/easyi3status/config.yaml`.

It must have a `modules` list under which you must enter the names of your modules (in the order you want them to appear left to right).

Each module will have a `name` and a `config` section. Here is an example:

    modules:
    - name: weather
      config:
        city: 6955677
        appid: <MY SECRET APP ID>
        units: metric
        language: tr
        minWindSpeed: 5
        wantedHours: [6,9,18,21]
    - name: maildir
      config:
        path: /home/sahip/mail/inbox
    - name: maildir
      config:
        path: /home/sahip/mail/dbb
        label: dbb
        hideIfZero: true
    - name: date
      config:
        format: '%d-%m-%Y %H:%M'

### i3 Configuration

    # place this in your i3 config
    bar {
		status_command easyi3status
		font pango:Monospace Sans Mono, Icons 10 # Replace with your favorite font with Unicode support.
    }

And you're ready to go. You'll need to restart *i3* for the changes to take effect.

## Plugins

[this list](http://easyi3status.herokuapp.com/assets) has all the plugins you can install. Choose one and follow its instructions to install.

### Creating your own plugin

Plugins are written in *python3*.

#### 1. Write the plugin code

Create a file called *myNewPlugin.py* in `~/.config/easyi3status/modules` and put this code in it:

```python
from statusModule import EasyI3StatusModule

class Module(EasyI3StatusModule):
	validDuration = 5

	def __init__(self, config):
		self.values = [{
			'full_text': 'hello'
		}, {
			'full_text': 'world'
		}]

	def update(self):
		pass
```

What we did is:

1. defined a class called `Module` that extends `EasyI3StatusModule`. This is mandatory
2. A module needs to set `values`. `values` is a list of dicts. These dicts are blocks that will be shown in your i3 status bar. What you can*(and should)* put in each block is [explained by i3wm](https://i3wm.org/docs/i3bar-protocol.html#_blocks_in_detail)
  * `full_text`: what text to show
3. easyi3status will call ask your plugin to update its values every `validDuration` seconds by calling the `update` method.
4. In our update method we didn't feel like updating the values, so we just `pass`ed.

#### Update config

Putting the source code of a module in the right folder doesn't finish the job.  
We need to enter our plugin's name in under the `modules` section of `~/.config/easyi3status/config.yaml` for it to show up.

```
modules:
# you'll (probably) have a bunch of configs for your existing modules here
# ...
- name: myNewPlugin #this matches the name of the python file (except the .py part)
```

#### 3. Done

That's right. We can now test our module.

Restart i3

You should see `hello world` in your status bar now!

#### 4. Updating values

To make our plugin change its text, we just need to modify `values` in `update` method.

Lets make it show a counter so it starts from 0 and increments every 5 seconds.

```python
...
	def __init__(self, config):
		...
		self.counter = 0
...
	def update(self):
		#self.values[0] is the block that says 'hello', and values[1] says 'world'
		# I only need to update the 'full_text' field.
		self.values[1]['full_text'] = str(self.counter)
		self.counter = self.counter + 1
```
And when you test it again, you'll see it showing the following lines one after the other

```
hello 0
hello 1
hello 2
hello 3
...
```

You may have noticed that before it said `hello 0`, it said `hello world` for 5 seconds. That's because first the `__init__` is called, and 5 seconds later the `update` is called. You could work your python magic to solve it yourself. (calling `update` from `__init__` could be a solution)

#### 5. Using config

Modify the `config.yaml` like so:

```
- name: myNewPlugin
  config:
    xyz: "aecepoglu"
```

And modify `__init__` and `update` methods like so:

```python
...
	def __init__(self, config):
		self.counter = 0
		self.xyz = config['xyz']

		self.values = [{
			'full_text': 'hello'
		}, {
			'full_text': self.xyz
		}]
	
	def update(self):
		self.values[1]['full_text'] = self.xyz + ' ' + str(self.counter)
		self.counter = self.counter + 1
```

And now we have a plugin that shows:

```
hello aecepoglu
hello aecepoglu 0
hello aecepoglu 1
hello aecepoglu 2
...
```

#### 6. Share your plugin

Just submit your plugin [here](http://easyi3status.herokuapp.com/assets). Enter its github url (eg. http://github.com/aecepoglu/easyi3status-date-plugin) to *Repo URL* field.
