import win32com.client
import time
from threading import Thread
from pynput import keyboard

# Defining keystroke strings for easier mapping to UI
skill_1 = "1"
skill_2 = "2"
skill_3 = "3"
skill_4 = "4"
skill_s1 = "{INSERT}"
skill_s2 = "{DELETE}"
skill_s3 = "{HOME}"
skill_s4 = "{END}"

# Key aliases
vKeyTab = 9
vKeyLControl = 162
vKeyRControl = 163
vKeyLAlt = 164
vKeyRAlt = 165
vKeyTilde = 192

# Globals
gToggleKey = vKeyTilde
gGlobalCooldown = 2.5
gDotInterval = 3
gAllowKeystroke = False
gSkillIndex = 0
gRotation = []

# Shell used for sending keystrokes to the OS
gShell = win32com.client.Dispatch("WScript.Shell")

# Helper classes	
class Skill(object):

	def __init__(self, name, key, potency = 0, duration = 0, durationPotency = 0):
		self.Name = name
		self.Key = key
		self.Potency = potency
		self.Duration = duration
		self.DurationPotency = durationPotency

	def dps(self):
			if self.Duration == 0:
				return round(self.Potency / gGlobalCooldown, 2)
				
			return round(self.Potency / self.Duration, 2) + round(((self.Duration / gDotInterval) * self.DurationPotency) / self.Duration, 2)
		
	def damage(self):
		if self.Duration == 0:
			return self.Potency

		return self.Potency + round(((self.Duration / gDotInterval) * self.DurationPotency), 2)

	def isInterval(self):
		if self.Duration > 0:
			return True
		return False

def on_win32press(msg, data):
	global gAllowKeystroke
	global gSkillIndex

	try:
		#print("Key pressed: {}".format(data.vkCode))
		# KBDLLHOOKSTRUCT.vkCode value is the key. KBDLLHOOKSTRUCT.flags value of 0 is a key Press (128 is key Release)
		if data.vkCode == gToggleKey and data.flags == 0: 
			gAllowKeystroke = not gAllowKeystroke
			ResetSkillCounter()
			print("ROTATION: {}".format(gAllowKeystroke))
		pass
	except Exception as e: #print('special key {0} pressed'.format(key))
		print(e)
		pass

	return False;

def ResetSkillCounter():
	global gSkillIndex
	gSkillIndex = 0

def FireSkill():
	global gSkillIndex
	if gSkillIndex >= len(gRotation):
		ResetSkillCounter()
	
	skill = gRotation[gSkillIndex]
	SendKeys(skill.Key)
	gSkillIndex += 1

	print("Firing {} with key {}. DPS ({}). Damage ({}).".format(skill.Name, skill.Key, skill.dps(), skill.damage()))

def GCD():
	time.sleep(gGlobalCooldown)

def SendKeys(key):
	gShell.SendKeys(key)

def BuildRotation(skills):
	# Find all the duration spells and make sure they get casted first
	intervalSkills = [x for x in skills if x.isInterval() == True]
	intervalSkills.sort(key=lambda x: x.dps(), reverse=True)
	highestDpsDuration = intervalSkills[0].Duration

	# Now add the non-duration spells
	# NOTE: If they have a cooldown, this is where we would add that
	instantSkills = [x for x in skills if x.isInterval() == False]
	instantSkills.sort(key=lambda x: x.dps(), reverse=True)

	# Add enough filler so our dots have finished
	count = int(round(highestDpsDuration / gGlobalCooldown))
	for x in range(count):
		intervalSkills.append(instantSkills[0])
		
	# Print out the built rotation
	for i, skill in enumerate(intervalSkills):
		print("{}: {} {}/s ({}).".format(str(i).zfill(2), skill.Name.ljust(15), skill.dps(), skill.damage()))

	return intervalSkills

def Rotation():
	global gRotation
	# Build the rotation skill set array
	skills = []
	skills.append(Skill("Ruin", skill_1, 100))
	skills.append(Skill("Miasma", skill_s2, 20, 24, 35))
	skills.append(Skill("Bio", skill_2, 0, 30, 35))

	# Build the rotation using the passed in array of skills
	gRotation = BuildRotation(skills)

	while True:
		if gAllowKeystroke == True:
			FireSkill()
		GCD()
with keyboard.Listener(win32_event_filter=on_win32press) as listener:
	try:
		if __name__ == '__main__':
			# Start the thread which sends keystrokes
			keystrokeThread = Thread(target=Rotation)
			keystrokeThread.start()
			# Start the keystroke listener
			listener.join()
	except Exception as e:
		print(e)
		pass