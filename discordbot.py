import discord
import numpy
from discord.ext import commands
from discord import app_commands
import json
import os
import random
dictionary_of_minerals = {
    "Rhodium": 50000,
    "Gold": 20000,
    "Platinum": 10000,
    "Palladium": 20000,
    "Silver": 300,
    "Cobalt": 200,
    "Nickel": 100,
    "Tin": 20,
    "Copper": 10,
    "Zinc": 10,
    "Iron": 10,
    "Bauxite": 10,
    "Coal": 10
}
dictionary_of_minerals_1 = {
    'Iridium': 500000,
    'Osmium' : 200000,
    'Ruthenium': 100000,
    'Hafnium': 200000,
    'Tantalum': 3000,
    'Tellurium': 2000,
    'Indium':1000,
    'Gallium':200,
    'Scandium':100,
    'Thorium':100,
    'Lithium':100,
    'Beryllium':100
}
inverse_dictionary_of_minerals_1 = {index: ore for index, ore in enumerate(dictionary_of_minerals_1)}
inverse_dictionary_of_minerals = {index: ore for index, ore in enumerate(dictionary_of_minerals)}
def get_mineral_by_index(index):

    minerals_list = list(dictionary_of_minerals.keys())
    if isinstance(index, int): # Is an integer

        if 0 <= index < len(minerals_list): # index is greater than 0 and the index does not exceed the index of the minerals_list
            print(f"working: {index}")
            return minerals_list[index]
        else:
            print("eoreoreoreo")
            return "Index out of range"
    else:
        print("eoreoreoreo")
        return "Index must be an integer."
def convert_keys_to_strings(data): #converting to store in the json file
    if isinstance(data, dict):
        return {str(key): convert_keys_to_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_strings(element) for element in data]
    else:
        return data
def save_user_data(data):# Writing to json file
    try:
        with open('user_data.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.flush() 
            os.fsync(file.fileno()) 
        print("SAVED DATA successfully")
    except PermissionError:
        print("Error: Permission denied. Cannot write to file.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_user_data():
    file_path = os.path.join(os.getcwd(), 'user_data.json')  
    try:
        if os.path.exists(file_path): 
            with open(file_path, 'r') as file:
                data = json.load(file)
                return convert_keys_to_strings(data)
        else:
            print(f"No user_data.json file found at {file_path}. Initializing empty data.")
            return {}  
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {file_path}. Initializing empty data.")
        return {}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}
def load_user_data_lists():
      with open('lists.txt', 'r') as file:
            lists = file.read().strip().split('\n')
            print(lists)
            return lists
    

def update_user_data(discord_user_id, username, id): #Checking if it exists
    global user_data
    if 'username' not in user_data[discord_user_id]:
        user_data[discord_user_id]['username'] = str(discord_user_id)
    if discord_user_id not in user_data:
        user_data[discord_user_id] = {}  #Creating a new section for the user
    
    user_data[discord_user_id][username] = id 
    data = user_data
    save_user_data(data)
def update_user_data_gamble(discord_user_id, earnings = None, upgrades = False, ores = False):
    global user_data
    discord_user_id = str(discord_user_id)
    not_in_dict(discord_user_id,"ore_ore_upgrades","0")
    
    if discord_user_id not in user_data:
        user_data[discord_user_id] = {}
        print("clearing")
    if 'money' not in user_data[discord_user_id]:
        user_data[discord_user_id]['money'] = "1000"
        print('adding')
    if 'ore_upgrades' not in user_data[discord_user_id]:
        user_data[discord_user_id]['ore_upgrades'] = "0"
    if 'ore_ore_upgrades' not in user_data[discord_user_id]:
        user_data[discord_user_id]['ore_ore_upgrades'] = "0"
    
        print('adding_upgrade')
    if 'username' not in user_data[discord_user_id]:
        user_data[discord_user_id]['username'] = str(discord_user_id)
    if ores:
        user_data[discord_user_id]['money'] = int(user_data[discord_user_id]['money']) - (int(user_data[discord_user_id]['ore_ore_upgrades']) + 1)* 1000
        user_data[discord_user_id]['ore_ore_upgrades'] = int(user_data[discord_user_id]['ore_ore_upgrades']) + 1
    if upgrades:
        user_data[discord_user_id]['money'] = int(user_data[discord_user_id]['money']) - (int(user_data[discord_user_id]['ore_upgrades']) + 1)* 1000
        user_data[discord_user_id]['ore_upgrades'] = int(user_data[discord_user_id]['ore_upgrades']) + 1

        
    if earnings:
        upgrade = float(user_data[str(discord_user_id)]['ore_ore_upgrades'])
        if upgrade:
            earnings = (float(float(upgrade) *.10) + 1) * float(earnings)
        print(earnings,"earnings")
        mathing = int(float(user_data[discord_user_id]['money'])) + int(earnings)
        user_data[discord_user_id]['money'] = str(mathing)
        print(user_data[discord_user_id]['money'])
        #ds
    save_user_data(user_data)

def see_balance(discord_user_id) -> int:
    global user_data
    discord_user_id = str(discord_user_id)
    if discord_user_id not in user_data:
        user_data[discord_user_id] = {}

    if 'money' not in user_data[discord_user_id]:
        user_data[discord_user_id]['money'] = "1000"

    return user_data[discord_user_id]['money']

intents = discord.Intents.default()
intents.message_content = True
global user_data
user_data = load_user_data()
client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot is ready")

def mine(discord_user_id, mine): #Mines for money
    print("thre mine value is ",mine)
    minimun_value = 1
    if str(discord_user_id) in user_data:
     
        if 'ore_upgrades' in user_data[str(discord_user_id)]:
            try:
                
                upgrade = int(user_data[str(discord_user_id)]['ore_upgrades'])
              
                minimun_value = 100 * upgrade
            except ValueError:
                print("Error: 'ore_upgrade' value is not an integer.")
    print("minimun", minimun_value)

    mineral_mined = random.randint(minimun_value,10000) 
    if mine == 0:
        if mineral_mined >=1 and mineral_mined <=7000:
            print(1)
            mineral_index = random.randint(8,12)
            mineral = inverse_dictionary_of_minerals[mineral_index] 
            
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        elif mineral_mined >= 7001 and mineral_mined <= 8500:
            print(2)
            mineral_index = 7
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        elif mineral_mined >= 8501 and mineral_mined <= 9300:
            print(3)
            mineral_index = 6
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9301 and mineral_mined <= 9700:
            print(4)
            mineral_index = 5
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9701 and mineral_mined <= 9900:
            print(5)
            mineral_index = 4
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9901 and mineral_mined <= 9990:
            print(6)
            mineral_index = 2
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9991 and mineral_mined <= 9996:
            print(7)
            mineral_index = random.choice([1,3])
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
        else:
            print(8)
            mineral_index = 0
            mineral = inverse_dictionary_of_minerals[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals[str(mineral)])
            return mineral_index
    elif mine == 1:
        print("Mine one is being used!")
        if mineral_mined >=1 and mineral_mined <=7000:
            print(1)
            mineral_index = random.randint(8,11)
            mineral = inverse_dictionary_of_minerals_1[mineral_index] 
            
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        elif mineral_mined >= 7001 and mineral_mined <= 8500:
            print(2)
            mineral_index = 7
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        elif mineral_mined >= 8501 and mineral_mined <= 9300:
            print(3)
            mineral_index = 6
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9301 and mineral_mined <= 9700:
            print(4)
            mineral_index = 5
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9701 and mineral_mined <= 9900:
            print(5)
            mineral_index = 4
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9901 and mineral_mined <= 9990:
            print(6)
            mineral_index = 2
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        elif mineral_mined >= 9991 and mineral_mined <= 9996:
            print(7)
            mineral_index = random.choice([1,3])
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index
        else:
            print(8)
            mineral_index = 0
            mineral = inverse_dictionary_of_minerals_1[mineral_index]
            update_user_data_gamble(discord_user_id, dictionary_of_minerals_1[str(mineral)])
            return mineral_index

def not_in_dict(discord_user_id, label,value,usernamestuff = False):
    if str(discord_user_id) not in user_data:
        user_data[str(discord_user_id)] = {}
    if usernamestuff:
        if label not in user_data[str(discord_user_id)]:
            user_data[str(discord_user_id)][label] = str(value)
        user_data[str(discord_user_id)][label] = str(value)
        return
    if label not in user_data[discord_user_id]:
        user_data[discord_user_id][label] = str(value)

    save_user_data(user_data)

@client.tree.command(name="upgrade_mining_luck", description="Increases the luck you you getting a rare ore!!!")
async def upgrade_mining_luck(interaction: discord.Interaction,):
    default_upgrade = 1000
    if  str(interaction.user.id) not in user_data:
        user_data[str(interaction.user.id)] = {}

    if 'money' not in user_data[str(interaction.user.id)]:
        user_data[str(interaction.user.id)]['money'] = "1000"
    not_in_dict(interaction.user.id,'username',interaction.user.name,True )

    if 'ore_upgrades' not in user_data[str(interaction.user.id)]:
        user_data[str(interaction.user.id)]['ore_upgrades'] = "0"
    upgrade_cost = (int(user_data[str(interaction.user.id)]['ore_upgrades']) + 1) * default_upgrade
    print(upgrade_cost,"upgrade_cost")
    if int(user_data[str(interaction.user.id)]['ore_upgrades']) >= 75:
        await interaction.response.send_message("Hold it!!! You have hit max upgrade please wait untill a new update so u can mine to your heats content <3!")
        return
    if int(user_data[str(interaction.user.id)]['money']) < upgrade_cost:
        await interaction.response.send_message("Opps! You dont have enough money.\n Please use /upgrade_mining_luck_cost to see the cost of the next upgrade!")
        return
    else:
        update_user_data_gamble(discord_user_id=str(interaction.user.id),upgrades=True)
        upgrade_level = user_data[str(interaction.user.id)]['ore_upgrades']
        await interaction.response.send_message(f"Success! You have upgraded mining luck to {upgrade_level}!")
@client.tree.command(name="upgrade_ore_value", description="Increases the ore value so you gain more moeny!!!")
async def upgrade_ore_value(interaction: discord.Interaction,):
    default_upgrade = 1000
    if  str(interaction.user.id) not in user_data:
        user_data[str(interaction.user.id)] = {}

    if 'money' not in user_data[str(interaction.user.id)]:
        user_data[str(interaction.user.id)]['money'] = "1000"
    not_in_dict(interaction.user.id,'username',interaction.user.name,True )

    not_in_dict(str(interaction.user.id),"ore_ore_upgrades","0")
    upgrade_cost = (int(user_data[str(interaction.user.id)]['ore_ore_upgrades']) + 1) * default_upgrade
    print(upgrade_cost,"upgrade_cost")
    if int(user_data[str(interaction.user.id)]['ore_ore_upgrades']) >= 75:
        await interaction.response.send_message("Hold it!!! You have hit max upgrade please wait untill a new update so u can mine to your heats content <3!")
        return
    if int(user_data[str(interaction.user.id)]['money']) <= upgrade_cost:
        await interaction.response.send_message("Opps! You dont have enough money.\n Please use /upgrade_ore_value_cost to see the cost of the next upgrade!")
        return
    else:
        update_user_data_gamble(discord_user_id=str(interaction.user.id),ores=True)
        upgrade_level = user_data[str(interaction.user.id)]['ore_ore_upgrades']
        await interaction.response.send_message(f"Success! You have upgraded ore value to {upgrade_level}!")
  


@client.tree.command(name="upgrade_mining_luck_cost", description="Shows the cost to upgrade your mining luck!")
async def upgrade_mining_luck_cost(interaction: discord.Interaction):
    not_in_dict(str(interaction.user.id),"ore_upgrades","0")
    upgrade = int(user_data[str(interaction.user.id)]['ore_upgrades']) + 1
    await interaction.response.send_message(f"The cost of you next upgrade is ${upgrade *1000}!")
    
@client.tree.command(name="upgrade_ore_value_cost", description="Lets you see the cost of your next upgrade!")
async def upgrade_ore_value_cost(interaction: discord.Interaction):
    not_in_dict(str(interaction.user.id),"ore_ore_upgrades","0")
    upgrade = int(user_data[str(interaction.user.id)]['ore_ore_upgrades']) + 1
    await interaction.response.send_message(f"The cost of you next upgrade is ${upgrade *1000}!")
def mine_buying_price(mine):
    mine = int(mine) + 1
    mine = str(mine)
    mine_cost = mine + "0000"
    for i in range(int(mine)):
        mine_cost = mine_cost + "0"
    return int(mine_cost)
def buying_mine(discord_user_id,mine):
    mine_cost = mine_buying_price(discord_user_id, mine)
    user_data[discord_user_id]['mine'] = int(user_data[discord_user_id]['mine']) + 1
    user_data[discord_user_id]['ore_upgrades'] = str(0)
    user_data[discord_user_id]['ore_ore_upgrades'] = str(0)
    update_user_data_gamble(discord_user_id,-int(mine_cost))

@client.tree.command(name="buy_mine", description="buy a upgraded mine for better ores")
async def buy_mine(interaction: discord.Interaction):
    not_in_dict(interaction.user.id,'username',interaction.user.name,True )
    not_in_dict(str(interaction.user.id),'ore_ore_upgrades',"0")
    not_in_dict(str(interaction.user.id),'ore_upgrades',"0")
    not_in_dict(str(interaction.user.id),'mine',"0")
    if int(user_data[str(interaction.user.id)]['money']) >= 100000:
        buying_mine(str(interaction.user.id),((user_data[str(interaction.user.id)]['mine'])))
        await interaction.response.send_message(f"Success! You have bought mine {int(user_data[str(interaction.user.id)]['mine']) + 1}")
    else:
        await interaction.response.send_message(f"You need {mine_buying_price(str(interaction.user.id),user_data[str(interaction.user.id)]['mine']) - int(user_data[str(interaction.user.id)]['money'])}")



@client.tree.command(name="mine_for_money", description="mines for money")
async def mine_for_money(interaction: discord.Interaction):
    not_in_dict(interaction.user.id,'username',interaction.user.name,True )
    not_in_dict(str(interaction.user.id),'ore_ore_upgrades',"0")
    not_in_dict(str(interaction.user.id),'mine',"0")
    print(interaction.user.name,"mined")
    mineral = mine(str(interaction.user.id),int(user_data[str(interaction.user.id)]['mine']))
    if int(user_data[str(interaction.user.id)]['mine']) == 0:
        mineral = inverse_dictionary_of_minerals[mineral]
        earnings = dictionary_of_minerals[mineral]
    elif int(user_data[str(interaction.user.id)]['mine']) == 1:
        mineral = inverse_dictionary_of_minerals_1[mineral]
        earnings = dictionary_of_minerals_1[mineral]
        print(mineral)
    multplr1 = int(user_data[str(interaction.user.id)]['ore_ore_upgrades']) *.10
   
    multplr = (float(user_data[str(interaction.user.id)]['ore_ore_upgrades']) + multplr1)
    upgrade = float(user_data[str(interaction.user.id)]['ore_ore_upgrades'])
    earnings1 = (float(upgrade *.10) + 1) * float(earnings) #each upgrade increase earnings by 10%
    current_mine = int(user_data[str(interaction.user.id)]["mine"])
    if multplr <= 0 and current_mine == 1:
        await interaction.response.send_message(f"you mined {mineral} and got ${int(dictionary_of_minerals_1[mineral])}.")
    elif multplr <= 0 and current_mine == 0:
        await interaction.response.send_message(f"you mined {mineral} and got ${int(dictionary_of_minerals[mineral])}.")
    else:
        await interaction.response.send_message(f"you mined {mineral} and got ${int(earnings1)}.")
        
@client.tree.command(name="show_balance", description="Lets you see your balance")
async def show_balance(interaction: discord.Interaction):
     not_in_dict(interaction.user.id,'username',interaction.user.name,True )
     blns = see_balance(interaction.user.id)
     await interaction.response.send_message(f"Your balance: ${blns}.")

@client.tree.command(name="gamble", description="gambles and the lower the change the more you earn")
@app_commands.describe(bet="The amount you want to bet",maxx="The highest range of the random number(the highest is 100)",bettingnumber="The number that you are betting on (lowest number possible is 1)" )
async def gamble(interaction: discord.Interaction, bet: int, maxx:int,bettingnumber:int):
    not_in_dict(str(interaction.user.id),"money",1000)
    if str(interaction.user.id) in user_data: 
        if 'money' in user_data[str(interaction.user.id)]:
            if int(user_data[str(interaction.user.id)]['money']) <=0:
                await interaction.response.send_message(f"Oops! Your out of money. Go mining for money! (/mine_for_money)")
                return
        maxx = numpy.clip(maxx,2,100) # limiting what the maxx is
    bet = numpy.clip(bet,10,int(user_data[str(interaction.user.id)]['money']))
    winning_number = random.randint(1,maxx)
    earning = 0

    if bet < 0:
        bet = bet * -1
    if winning_number == bettingnumber:
        earning = (maxx * bet) - bet
        sebl = int(see_balance(interaction.user.id)) #sebl = see balance
        await interaction.response.send_message(f"Congrats! You earned ${earning}. Winning number {winning_number} out of {maxx}. Your new balance ${sebl + earning}")
        update_user_data_gamble(earnings=earning,discord_user_id=interaction.user.id)
    else:
        sebl = int(see_balance(interaction.user.id))
        
        await interaction.response.send_message(f"You lost ${bet}. Winning number {winning_number} out of {maxx}. Your new balance ${sebl - bet}")
        update_user_data_gamble(earnings=-bet,discord_user_id=interaction.user.id)

client.run("-----------------------------------------------------------") # use your discord bot token