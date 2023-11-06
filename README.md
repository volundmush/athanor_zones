# Athanor Zones

## CONTACT INFO

**Name:** Volund

**Email:** volundmush@gmail.com

**PayPal:** volundmush@gmail.com

**Discord:** VolundMush

**Discord Channel:** https://discord.gg/Sxuz3QNU8U

**Patreon:** https://www.patreon.com/volund

**Home Repository:** https://github.com/volundmush/athanor_factions

## TERMS AND CONDITIONS

MIT license. In short: go nuts, but give credit where credit is due.

Please see the included LICENSE.txt for the legalese.

## DETAILS

This is a Plugin for [Athanor](https://github.com/volundmush/athanor) which provides a hierarchial Zone system for Evennia, meant for organizing rooms into a tree-like structure.

## FEATURES
* Hierarchial ZoneDB typeclass.
* Evennia Lock-system integration for Zone Control.



## OKAY, BUT HOW DO I USE IT?
Glad you asked!

If you haven't already, you'll need to install Evennia and Athanor. Follow the instructions at [Athanor](https://github.com/volundmush/athanor) about that.

Then, you can install athanor_zones using ```pip install git+git://github.com/volundmush/athanor_zones```

Once installed, the plugin must be added to your athanor.init() call in settings.py. It should look something like this:

```python
import athanor as _athanor, sys as _sys
_athanor.init(_sys.modules[__name__], plugins=[
    "athanor_factions",
    "athanor_zones"
])
```

Afterwards, you'll need to run evennia migrate athanor_zones to create the database tables.

Once that's done, reload Evennia and the commands should be accessible.

## FAQ 
  __Q:__ This is cool! How can I help?  
  __A:__ [Patreon](https://www.patreon.com/volund) support is always welcome. If you can code and have cool ideas or bug fixes, feel free to fork, edit, and pull request! Join our [discord](https://discord.gg/Sxuz3QNU8U) to really get cranking away though.

  __Q:__ I found a bug! What do I do?  
  __A:__ Post it on this GitHub's Issues tracker. I'll see what I can do when I have time. ... or you can try to fix it yourself and submit a Pull Request. That's cool too.

  __Q:__ The heck is an Athanor? Why name something this?
  __A:__ An Athanor is a furnace used in alchemy. It's a place where things are forged and refined. I thought it was a fitting name for a library that's meant to be used to build other things.

## Special Thanks
  * The Evennia Project.
  * All of my Patrons on Patreon.
  * Anyone who contributes to this project or my other ones.
