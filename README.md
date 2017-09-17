# easyi3status

An easy and modular i3-status application.

## To Install

**TODO**

## To Configure

**TODO**

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
