# Lib
This is a folder for referencing classes for ease of organization

## Banner_Module
A class representing the the Wish Banner. Implements all the logic for wishing, including choosing drops based on rarities, applying pity and guarantee systems, and updating the user's wish data. This class attempts to follow the gacha rules in Genshin Impact's Limited Event Wish. 
- Hard pity for a 5 star at 90 rolls
- 50/50 to get the featured 5 star on the first 5 star roll. If the 5 star is not the featured 5 star, the next 5 star is guaranteed to be the event 5 star
- Hard pity for a 4 star at 10 rolls
- 50/50 to get one of the featured 4 stars on the first 4 star roll. If the 4 star is not a featured 4 star, the next 4 star is guaranteed to be one of the featured 4 stars

## Settings_Module
A class for loading the settings into the script.

## User_Module
A class representing a user's wish data. This includes data such as the user's five and four star pity counts and their five and four star guarantees. Also is responsible for deducting the points from the user. 