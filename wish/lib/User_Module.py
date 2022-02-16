Command = 'UserData'

class UserData:
	def __init__(self, Parent, user, username, five_star_pity=0, four_star_pity=0, five_star_guarantee=False, four_star_guarantee=False):
		self.Parent = Parent
		self.user = user
		self.username = username
		self.five_star_pity = five_star_pity
		self.four_star_pity = four_star_pity
		self.five_star_guarantee = five_star_guarantee
		self.four_star_guarantee = four_star_guarantee
	
	def update_pity_counts(self, five_star_pity, four_star_pity):
		self.log("Updating pity counts for user " + self.username)
		self.five_star_pity = five_star_pity
		self.four_star_pity = four_star_pity

	def update_guarantees(self, five_star_guarantee, four_star_guarantee):
		self.log("Updating guarantees for user " + self.username)
		self.five_star_guarantee = five_star_guarantee
		self.four_star_guarantee = four_star_guarantee

	def deduct_points(self, points):
		self.log("Deducting " + str(points) + " points from user: " + self.username)
		self.Parent.RemovePoints(self.user, self.username, points)

	def log(self, message):
		self.Parent.Log(Command, message)