import random
from random import uniform
from math import fsum

FIVE_STAR_POOL = ['Diluc (Pyro)', 'Jean (Anemo)', 'Keqing (Electro)', 'Mona (Hydro)', 'Qiqi (Cryo)']
FOUR_STAR_POOL = [
	'Amber (Pyro)',
	'Lisa (Electro)',
	'Kaeya (Cryo)',
	'Barbara (Hydro)',
	'Razor (Electro)',
	'Bennet (Pyro)',
	'Noelle (Geo)',
	'Fischl (Electro)',
	'Sucrose (Anemo)',
	'Beidou (Electro)',
	'Ningguang (Geo)',
	'Xiangling (Pyro)',
	'Xingqiu (Hydro)',
	'Chongyun (Cryo)',
	'Diona (Cryo)',
	'Xinyan (Pyro)',
	'Rosaria (Cryo)',
	'Yanfei (Pyro)',
	'Sayu (Anemo)',
	'Kujou Sara (Electro)',
	'Gorou (Geo)',
	'Thoma (Pyro)',
	'Yun Jin (Geo)'
]

THREE_STAR_POOL = [
	'Thrilling Tales of Dragon Slayers'
]

DROP_RARITIES = ['3', '4', '5']
DROP_RATES = [.933, .06, .007]

FIVE_STAR_PITY = 90
FOUR_STAR_PITY = 10

Command = 'Banner'

class Banner:
	def __init__(self, Parent=None, event_five_star=None, event_four_stars=None, additional_four_stars=None):
		self.Parent = Parent
		self.event_five_star = event_five_star
		self.event_four_stars = event_four_stars

		# Add any additional characters to the pool in case the base pool is not up to date
		for addition in additional_four_stars:
			if not addition in FOUR_STAR_POOL:
				FOUR_STAR_POOL.append(addition)
		
		# Make it so that the pools are separate to prevent double chances of getting event characters
		for character in self.event_four_stars:
			if character in FOUR_STAR_POOL:
				FOUR_STAR_POOL.remove(character)
			else: 
				self.log("Could not find character: " + character + " in four star pool. Make sure this character exists and is spelled correctly.")

	def roll_banner(self, times, userdata):
		self.log("Rolling banner")
		drop_rarities = self.get_drop_rarities(times)

		drop_rarities = self.apply_pity(drop_rarities, userdata)

		self.log("About to get drops from rarities")
		drops = self.get_drops_from_rarities(drop_rarities, userdata)

		self.log("After rolling, pity is: five star: " + str(userdata.five_star_pity) + " four star: " + str(userdata.four_star_pity))

		return drops
	
	def get_drop_rarities(self, times):

		self.log("Getting rarities")
		results = select(DROP_RARITIES, times, DROP_RATES)
		self.log("Finished getting rarities")
		return results

	def apply_pity(self, rarities, userdata):
		self.log("Applying pities: five star: " + str(userdata.five_star_pity) + " four star: " + str(userdata.four_star_pity))
		four_star_pity_count = userdata.four_star_pity
		five_star_pity_count = userdata.five_star_pity

		for i in range(len(rarities)):
			if rarities[i] is not DROP_RARITIES[2] and five_star_pity_count == FIVE_STAR_PITY - 1:
				# Pity case for 5 star. TODO: Implement soft pity logic
				# Change this drop to be a five star, and reset pity counts
				rarities[i] = DROP_RARITIES[2]
				five_star_pity_count = 0
				four_star_pity_count = 0
			elif rarities[i] is not DROP_RARITIES[1] and four_star_pity_count == FOUR_STAR_PITY - 1:
				# Pity case for 4 star. 
				# Change this drop to be a four star, reset four star pity count only
				rarities[i] = DROP_RARITIES[1]
				four_star_pity_count = 0
				five_star_pity_count += 1
			elif rarities[i] is DROP_RARITIES[2]:
				# Hit 5 star early, reset five star pity count
				five_star_pity_count = 0
			elif rarities[i] is DROP_RARITIES[1]:
				# Hit 4 star early, reset four star pity count
				four_star_pity_count = 0
				five_star_pity_count += 1
			else:
				# Got a three star, increment pity counts
				four_star_pity_count += 1
				five_star_pity_count += 1

		self.log("Finished applying pities")
		userdata.update_pity_counts(five_star_pity_count, four_star_pity_count)

		return rarities
	
	def get_drops_from_rarities(self, rarities, userdata):
		drops_rarity_map = {
			3: [],
			4: [],
			5: []
		}

		self.log("Starting to get drops from rarities")
		for i in range(len(rarities)): 
			rarity = rarities[i]
			drop = self.select_drop_from_pool(rarity, userdata)
			self.log("Drop is  " + str(drop))
			self.log("Rarity  is  " + str(rarity))
			drop = drop + " (" + rarity + " star)"
			drops_rarity_map[int(rarity)].append(drop)

		drops = []
		if len(rarities) < 5:
			drops = drops_rarity_map[5] + drops_rarity_map[4] + drops_rarity_map[3]
		else:
			num_three_stars = len(drops_rarity_map[3])
			three_stars = [str(num_three_stars) + ' 3 star drops']
			drops = drops_rarity_map[5] + drops_rarity_map[4] + three_stars
		
		self.log("Finished getting drops: " + str(drops))

		return drops

	def select_drop_from_pool(self, rarity, userdata):
		if rarity is DROP_RARITIES[0]:
			return THREE_STAR_POOL[0]
		elif rarity is DROP_RARITIES[1]:
			# If the wish has a four star guarantee, then pick from the pool of event four stars
			# Set four star guarantee to false
			if userdata.four_star_guarantee == True and self.event_four_stars:
				userdata.four_star_guarantee = False
				return self.random_choice(self.event_four_stars)

			# If the wish has no guarantee, perform a 50/50. If the result is true, choose from the pool of event four stars
			# Otherwise, choose from the pool of general four stars and set the four star guarantee to true for the next wish.
			get_event_character = self.random_choice([False, True])
			if get_event_character and len(self.event_four_stars) > 0:
				return self.random_choice(self.event_four_stars)

			random_drop = self.random_choice(FOUR_STAR_POOL)

			if not random_drop in self.event_four_stars:
				userdata.four_star_guarantee = True
			
			return random_drop
		else:
			# If the wish has a five star guarantee, then return the event five star
			# Set the four star guarantee to false
			if userdata.five_star_guarantee == True and self.event_five_star:
				userdata.five_star_guarantee = False
				return self.event_five_star

			# If the wish has no guarantee, perform a 50/50. If the result is true, return the event five star character
			# Otherwise, choose from the pool of general five stars and set the five star guarantee to true for the next wish
			get_event_character = self.random_choice([False, True])
			if get_event_character and self.event_five_star:
				return self.event_five_star
			
			userdata.five_star_guarantee = True
			return self.random_choice(FIVE_STAR_POOL)
	
	def log(self, message):
		self.Parent.Log(Command, message)

	def random_choice(self, pool):
		random_gen = random.SystemRandom() # Add more randomness by using the OS

		# Shuffle the pool a few times to add randomness
		num_shuffles = 10
		for _ in range(num_shuffles):
			random_gen.shuffle(pool)
			self.log(str(pool))

		# Select a random item from the pool after it has been shuffled
		index = random_gen.randint(0, len(pool) - 1)
		self.log(str(index))
		return pool[index]

#---------------------------
#   Util Functions (Do not need a object to be used)
#---------------------------

# Taken from: https://stackoverflow.com/questions/59000464/why-is-my-implementation-of-numpy-random-choice-faster
# We aren't able to import numpy to use choices, and we cannot use random.choices since it's unsupported in python 2.7.13. 
def select(array, total_count, probability):
    probability_accumulative = []
    last_element = 0
    for i in range(len(probability)):
        probability_accumulative.append(last_element + probability[i])
        last_element = probability_accumulative[i]

    result = []
    if(len(array) != len(probability)):
        return
    elif(fsum(probability) != 1.0):
        return
    else:
        for i in range(total_count):
            rand = uniform(0, 1)
            for j in range(len(probability_accumulative)):
                if(rand < probability_accumulative[j]):
                    result.append(array[j])
                    break
    return result


