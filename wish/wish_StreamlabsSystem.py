#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references


import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings

from Banner_Module import Banner
from User_Module import UserData

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Genshin Wish"
Website = "https://www.streamlabs.com"
Description = "Performs a wish on the genshin standard banner"
Creator = "Derek Phan"
Version = "1.0.0"
Command = '!wish'
Cost = 160

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

# Mapping of users to UserData objects. Used to store important wish info in memory for reuse. TODO: Load this in from a file to allow storage via disk
user_wish_data = {}


#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    '''
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"
    '''
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    '''
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        Parent.SendStreamMessage(ScriptSettings.Response)    # Send your message to chat
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
    '''
    if data.GetParam(0) != Command and data.GetParam(0) != '!gift':
        return

    parsed_points = int(data.GetParam(1))

    if data.GetParam(0) == '!gift':
        Parent.AddPoints(data.User, data.UserName, parsed_points)
        return

    if parsed_points > Cost * 10:
        log("Too many wishes at once. Max is 10 rolls at a time.")
        return

    user = data.User
    userName = data.UserName
    user_points = Parent.GetPoints(user)

    if parsed_points > user_points:
        send_message("@" + userName + ": insufficient points for requested wishes. Broke bitch.")
        return

    log("num points is " + str(parsed_points))
    num_rolls = calculate_num_rolls(parsed_points)

    event_banner = Banner(Parent, "Zhongli (Geo)", ["Chongyun (Cryo)", "Xingqiu (Hydro)", "Beidou (Electro)"])

    log("Finding user data")
    userdata = initialize_user_data(user, userName)

    drops = event_banner.roll_banner(num_rolls, userdata)

    send_result_message(drops, userdata)
    #send_whisper_message(user,  'Five star pity: ' + str(userdata.five_star_pity))

    userdata.deduct_points(num_rolls * Cost)

    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

def calculate_num_rolls(points):
    log("Calculating num rolls")
    num_rolls = points // Cost

    return num_rolls

def initialize_user_data(user, username):
    if not user_wish_data.get(user, None):
        user_wish_data[user] = UserData(Parent, user, username)

    return user_wish_data[user]

def send_result_message(drops, userdata):
    drops_message = ''
    if len(drops) == 2:
        drops_message = ' and '.join(drops)
    else:
        drops_message = ', '.join(drops)

    drop_results = '@' + userdata.username + ' got ' + drops_message + ' from the event banner. Five star pity: ' + str(userdata.five_star_pity)
    send_message(drop_results)

def send_message(message):
    log("Sending stream message")
    Parent.SendStreamMessage(message)

def send_whisper_message(user, message):
    log("Sending a whisper message to " + user)
    Parent.SendStreamWhisper(user, message)

def log(message):
    Parent.Log(Command, message)
    return


#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    # TODO: Add writes to a file to store UserData on disk
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
