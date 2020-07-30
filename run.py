# coded by: salism3
# 30 - 07 - 2020

import igparser, time, sys, os, random, shutil
from igparser import dump, action, exception
from colorama import Fore, Back, init
from glob import glob
from getpass import getpass
init(autoreset = True)

ses = None
total_enter = 0
current_func = None

W = Fore.WHITE
B = Fore.BLACK
C = Fore.CYAN
R = Fore.RED
G = Fore.GREEN
MA = Fore.MAGENTA
Y = Fore.YELLOW
ERR = f"   {R}[!]{W} " 
QUE = f"   {MA}[?]{W} "
INF = f"   {MA}[+]{W} " 
DAN = f"{R} [!]"

logo = f"""
   {MA}╔═╗{W}┬┌┬┐┌─┐┬  ┌─┐  {MA}╔╦╗{W}┌─┐┌─┐┬─┐┌─┐┌┬┐
   {MA}╚═╗{W}││││├─┘│  ├┤    {MA}║{W} ├─┤│ ┬├┬┘├─┤│││
   {MA}╚═╝{W}┴┴ ┴┴  ┴─┘└─┘   {MA}╩{W} ┴ ┴└─┘┴└─┴ ┴┴ ┴ v{MA}0.1"""

def randomstring(num):
	char = list("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM")
	rv = "".join([random.choice(char) for _ in range(num)])
	return rv

def input_(text, que = True, looping = True):
	if looping:
		for _ in range(8):
			rv = input((QUE if que else "") + text + MA)
			if rv.strip():
				return rv
			else:
				print(f"   {R}[!]{W} blank input\n")
		else:
			print(f"   {R}[!]{W} Dah lah maless !!!")
			enter()

	else:
		return input((QUE if que else "") + text + MA)


def select(min, max, text = "   >>> ", error_msg = "input not valid", que = False):
	for _ in range(8):
		try:
			data = int(input_(W + text, que = que, looping = False))
			if data in range(min, max + 1):
				return data
		except ValueError:
			pass
		print(f"   {R}[!]{W} {error_msg}\n")
	else:
		print(f"   {R}[!]{W} Dah lah maless !!!")
		enter()

def confirm_execute():
	text = "yes" + str(random.randint(0,999)).zfill(3)
	if input_(f"type '{text}' to confirm: ", looping = False) != text:
		print(ERR + "operation cancelled!")
		enter()

def check_login(cookies = None):
	global ses
	if not cookies:
		try:
			cookies = open("cookies.txt").read()
		except:
			return False
	ses = igparser.Account(cookies)
	return ses.logged

def show_select_menu(menu, back = True):
	for i, x in enumerate(menu):
		print(f"   {MA}{i + 1}).{W} {x}")

	if back:
		print(f"   {MA}0).{W} Back")

	return select(0 if back else 1, len(menu))

def updateFunc(func):
	def inner():
		global current_func
		current_func = func
		func()
	return inner

def banner():
	os.system("cls" if os.name == "nt" else "clear")
	text = random.choice([
		f"   {Back.WHITE}{B}" + "by: salismazaya from xiuzcode".center(37),
		f"   {Back.WHITE}{B}" + "donate: https://cutt.ly/salismazaya".center(37),
	])
	print(logo)
	print(text)
	print()

@updateFunc
def home():
	banner()
	print(f"""   {MA}1).{W} Go to Menu
   {MA}2).{W} Login
   {MA}3).{W} Logout
   {MA}0).{W} Exit""")
	pilih = select(0,3)
	if pilih == 0:
		banner()
		print("    Thank you for use this tool ^_^")
	elif pilih == 1:
		if not check_login():
			print(ERR + "You must login!")
			enter()
		else:
			menu()
	elif pilih == 2:
		if not check_login():
			login()
		else:
			print(ERR + "You has been login!")
			enter()
	elif pilih == 3:
		confirm_execute()
		os.remove("cookies.txt")
		print()
		print(INF + "Done!")
		enter()

def login():
	global ses
	os.system("cls" if os.name == "nt" else "clear")
	print(f"""               
			 {R}[WARNING]{W}

   1. Your account can be banned if you use this
   2. After successfully logging in your account will
      automatically comment on the author
      profile photo and like
   3. Don't use this for crime
   4. Everything the user does is not the responsibility
      of the author
   5. By using this the user is considered to
      understand and comply with the above provisions
      """)

	cookies = input_("Your Instagram Cookies: ")
	ses = igparser.Account(cookies)
	try:
		msg = ["Hello I'M TAGRAM User", "Halo bro gw user Tagram btw toolnya keren banget", "be yourself and never surrender"]
		time.sleep(1)
	except:
		pass
	if ses.logged:
		try:
			action.like_post(ses, "2361434083693518607")
			action.comment_post(ses, "2361434083693518607", "Hello I'M TAGRAM User ^_^")
		except:
			pass
		open("cookies.txt", "w").write(cookies)
		print(f"{INF}Successully Login!")
		enter()
	else:
		print(ERR + "Cookies Not Valid!")
		enter()

@updateFunc
def menu():
	banner()

	list_menu = [
		"Spam Like in Home",
		"Spam Like in People",
		"Mass Unlike in Home",
		"Mass Unlike in People",
		"Mass Follow Back",
		"Mass Unfollow",
		"Mass Download Photo in Home",
		"Mass Download Photo in People",
		"Delete Output"
	]

	print(f"   Login as  : {G}{ses.name[:22]}")
	print(f"   UID       : {G}{ses.id}\n")
	print(f"{MA}   No.{W} Menu\n{Y}   --- ----")
	pilih = show_select_menu(list_menu)
	if pilih == 0:
		home()
		exit()

	banner()
	print(f"\n   {MA}Selected:{W} {list_menu[pilih - 1]}")

	before_done = None

	if pilih == 1:
		limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
		func = lambda: action.more_dump(dump.post_home, args = [ses], limit = limit)
		execute_func = lambda data: action.like_post(ses, data.id)

	elif pilih == 2:
		target = input_("Username Target: ")
		limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
		func = lambda: action.more_dump(dump.post_people, args = [ses], kwargs = {"usernamePeople":target}, limit = limit)
		execute_func = lambda data: action.like_post(ses, data.id)

	elif pilih == 3:
		#msg = input_("Comment: ")
		limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
		func = lambda: action.more_dump(dump.post_home, args = [ses], limit = limit)
		execute_func = lambda data: action.unlike_post(ses, data.id)

	elif pilih == 4:
		target = input_("Username Target: ")
		#msg = input_("Comment: ")
		limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
		func = lambda: action.more_dump(dump.post_people, args = [ses], kwargs = {"usernamePeople":target}, limit = limit)
		execute_func = lambda data: action.unlike_post(ses, data.id)

	elif pilih == 5:
		limit = select(1, 1000, text = "Limit: ", error_msg = "min: 1, max: 1000", que = True)
		func = lambda: action.more_dump(dump.follower_people, args = [ses], kwargs = {"idPeople":ses.id}, limit = limit)
		execute_func = lambda data: action.follow_people(ses, data.username, idPeople = data.id)

	elif pilih == 6:
		limit = select(1, 1000, text = "Limit: ", error_msg = "min: 1, max: 1000", que = True)
		func = lambda: action.more_dump(dump.following_people, args = [ses], kwargs = {"idPeople":ses.id}, limit = limit)
		execute_func = lambda data: action.unfollow_people(ses, data.username, idPeople = data.id)

	elif pilih == 7:
		folder = "output/" + randomstring(10)
		limit = select(1, 5000, text = "Limit: ", error_msg = "min: 1, max: 5000", que = True)
		func = lambda: action.more_dump(dump.post_home, args = [ses], limit = limit)
		os.mkdir(folder)
		execute_func = lambda data: open(f"{folder}/{randomstring(10)}" + (".jpg" if ".jpg" in data.data["display_url"] else ".mp4"), "wb").write(ses.session.get(data.data["display_url"]).content)
		before_done = lambda: print(f"{INF}file saved in folder: {folder}")

	elif pilih == 8:
		folder = "output/" + randomstring(10)
		target = input_("Username Target: ")
		limit = select(1, 5000, text = "Limit: ", error_msg = "min: 1, max: 5000", que = True)
		func = lambda: action.more_dump(dump.post_people, args = [ses], kwargs = {"usernamePeople":target}, limit = limit)
		os.mkdir(folder)
		execute_func = lambda data: open(f"{folder}/{randomstring(10)}" + (".jpg" if ".jpg" in data.data["display_url"] else ".mp4"), "wb").write(ses.session.get(data.data["display_url"]).content)
		before_done = lambda: print(f"{INF}file saved in folder: {folder}")
	elif pilih == 9:
		deleter_menu()
		exit()

	confirm_execute()
	print()
	print(INF + "Getting data ...")
	data = func()
	# print(data)
	print(f"{INF}Total: {G}{len(data)}")
	time.sleep(1)
	procces(execute_func, data, before_done = before_done)

def deleter_menu():
	banner()
	pilih = show_select_menu(["Delete Empty Folder in Output", "Delete All Output"])
	if pilih == 1:
		confirm_execute()
		for x in glob("output/*"):
			try:
				if not os.listdir(x):
					os.rmdir(x)
			except:
				pass
		print(INF + "Done!")
	elif pilih == 2:
		confirm_execute()
		for x in glob("output/*"):
			try:
				shutil.rmtree(x)
			except:
				pass
		print(INF + "Done!")
	enter()

def procces(func, list_, before_done = None):
	count = 0
	total = len(list_)
	for x in list_:
		count += 1
		try:
			data = func(x)
		except exception.Error429:
			time.sleep(245 + random.random())
			func(x)
			a = 0
		count_proccess(count, total)
		time.sleep(random.random())
	print()
	if callable(before_done):
		before_done()
	print(INF + "Done!")
	enter()

def count_proccess(count, total):
	angka = str(count * 100 / total)
	a, b = angka.split(".")

	angka = f"{a}.{b[:2].ljust(2, ' ')} %"

	sys.stdout.write(f"\r{INF}Proccess: {G}{angka}{W}")
	sys.stdout.flush()

def enter():
	global total_enter
	total_enter += 1
	if total_enter > 8:
		exit()
	getpass(f"\n   {MA}[{W} Press Enter to Back {MA}]{W}")
	current_func()
	exit()
	
try:
	home()
except KeyboardInterrupt:
	exit(ERR + "Exit: Ok")
except Exception as e:
	print(ERR + str(e))
