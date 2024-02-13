# Poegie
Poegie is as delirium orb reroll and data collection tool. It is a deli roll (hoagie, like the sandwich) for path of exile (poe) so. Thus, poegie. 

The main features are: aid to help prevent rerolling over desired deli orbs in the harvest bench, a profits calculator, and data collection to keep track of what deli orbs you have rolled. It is designed to be Path of Exile ToS compliant.

Poegie is still early in its development, so there may be issues!
# Installation
## Prerequisites (AutoHotKey)
Poegie uses AutoHotKey to intercept inputs. This is what allows the app to stop you from rolling over things. The app relies on the AutoHotKey executable and is expected to be in the PATH.

Download and install v1.X (not version 2) from the [ahk website](https://www.autohotkey.com/download/)
## Download poegie
- Download `main.zip` from the [latest releases](https://github.com/Philimanjar0/poegie/releases) tab. 
- Unzip it wherever you would like. 
- Run `main.exe`
	- Windows Defender might complain. Pyinstaller is used to build the exe, which is typically also used to pack malware. Windows knows this and throws a fit. Poegie is not malware.
	- Windows might remove the exe. Just disable it to run it once, and turn it back on.
- If you want to see some logging, you can run it from a command prompt instead.

## Side Dishes
I recommend using X-Mouse Button Control and binding scroll wheel up/down to left click, and configure it for PoE only. This is helpful in general, but particularly helpful for rolling the the harvest bench when you cannot roll over what you want.

# How to use
There are 3 tabs that each do their own thing: config, profits calculator, and data collection. The config tab is the main tab used for rerolling. The other two tabs are helpful as references.
## Config
- The app needs to know were your harvest bench is on the screen. Click the "set bench location." Drag and resize the window to match your harvest bench as closely as possible.
- Select the desired deli orbs you dont want to roll over in the list.
- Enable "allow input blocking" to enable the app to block your left click inputs if you roll into a desired deli orb.

## Data
The data tab keeps track of the number of times you have rolled in to each orb. It only keeps track if you have This **does not** keep track of the quantity of orbs. Rolling stacks of 1 and 10 are treated the same. You can reset these, or export the values to a CSV.

The motivation behind this tab is to gain a better understanding of the weights of each item by collecting as much data as possible.

## Calculator
The calculator tab is helpful to calculate if rolling deli orbs will be profitable on average*.
- Input the base costs. How many orbs can you buy in bulk for a divine? How much lifeforce can you buy for a divine?
- Input what you plan to sell. Select each orb that you will sell, and how many you can sell for a divine.
- Click calculate to see the expected return.

*Important caveat. This assumes EQUAL weighting between each orb. This may not actually be true, so the accuracy may not be correct.

# Path of Exile ToS compliance*
Historically, external overlays and tools are generally okay if they do not aid in gameplay and do not do any work for the player that the player would not do themselves. The rule of thumb is that no human input should correspond to more than one in game action. 

- Poegie will not send inputs for the user, or perform any action for the user.
- Poegie does not read any game data. It is an overlay that relies on computer vision and item text for object recognition.
- Poegie does not interact with an GGG online services or API.

*If there are any ToS concerns, especially if you are GGG staff. Please contact me directly. This is intended as tool and service for the community, not a weapon to create an unfair advantage for its users.

# Bug reporting
You have two options for bug reporting
- There is a bug report/feature request channel in the [discord](https://discord.gg/EhKBMFpZ).
- Create a github issue

# Help and discussion
Join the discord for help, bugs, discussion, and whatever else. 
