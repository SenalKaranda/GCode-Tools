# Glass Bed GCode Mod
#### A Python app that modifies a GCode file and inserts code to configure the following settings for the first 3 layers, in an attempt to make printing on Glass Beds less annoying in terms of initial adhesion. 

# Purpose
I got my hands on a glass bed for my printer recently (after I messed up my magnetic one), and I quickly ran into the issue of my prints not adhering to the plate (as early as the first layer). I found some fixes across the internet that mentioned changing settings on the first couple layers, but didn't want to do this by hand for every print. I haven't looked into whether or not other slicers do a better job, but I plan on sticking to Cura for a while, so I decided to throw this script together.

# Modifications
- Print Speed (5, 40, 150)
- Nozzle Temp (210, 200, 190)
- Bed Temp (70, 65, 60)
#### Note: The third layer is used to set default values for all layers subsequent to layers 1 and 2.

# Requirements
### This script assumes the following:
- You are using files created by Cura and an Ender V3 SE.
- You are using an Ender 3 v3 SE
- You don't mind a cobbled together python app (at least at first).
