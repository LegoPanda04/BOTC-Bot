This is a bot to make Blood on the Clocktower scripts automatically in Discord.

To use, run the **bot.py** script while providing a valid bot token in **bot.key**. All required packages *should* be in **requirements.txt**. You can whitelist users for advanced commands by adding their discord ID to **whitelist.txt**. All commands are documented in the script or by using the command **$help**.

All scripts are located in the **data** folder. To add a new role, open the **Roles.csv** file and add the role. Having \\\* is neccesary to ensure that the difficulty gets correctly parsed by the bot. The roles sheet is ***not*** sorted by the bot, so the order you add roles is the order within a class that will be displayed. *For this reason, I would reccomend keeping the ****Roles.csv**** sorted alphabetically.*

If a file is not saved, it is because it has invalid characters. You will need to remake the file if this happens, and it is evident by there being an incomplete file without the .csv estension in the **data** folder.

That is really about it. 
