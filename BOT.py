from win32gui import FindWindow, GetWindowDC, GetClientRect, GetWindowRect, ReleaseDC, DeleteObject, EnumWindows, IsWindowVisible, GetWindowText
from win32ui import CreateDCFromHandle, CreateBitmap
from win32con import SRCCOPY
from PIL import Image
from numpy import *
from ctypes import windll
from json import load
from pyautogui import locate, moveTo
from operator import itemgetter
from zipfile import ZipFile
from threading import Thread
from time import time, sleep
from datetime import datetime
from urllib.request import urlopen
from os import listdir
from telebot import TeleBot
from getmac import get_mac_address
from platform import release

def getMac( ):
	if release( ) == '10':
		mac = get_mac_address( interface = "Ethernet" )
	else:
		mac = get_mac_address( interface = "Conexión de área local" )
	if mac == None:
		mac = get_mac_address( interface = "Conexión de red inalámbrica" )
	mac = mac.replace( ':', '' )
	mac = mac.upper( )
	return mac

def dateOverInternet( ):
	page = urlopen( 'http://just-the-time.appspot.com/' )
	page = page.read( ).split( )
	date = page[ 0 ].decode( 'UTF-8', errors = 'ignore' ).split( '-' ) 
	year = int( date[ 0 ] )
	month = int( date[ 1 ] )
	day = int( date[ 2 ] )
	return datetime( year, month, day )

def dateAfk( ):
	
	bot = TeleBot( '' )
	registed = []
	page = urlopen( '' )
	page = page.readlines()

	for line in page:
		registed.append( line.decode( 'UTF-8' ).split( ' ' ) )

	for mac in registed:
		if getMac( ) == mac[ 0 ]:
			date = mac[ 1 ].split( '-' )
			year = int( date[ 0 ] )
			month = int( date[ 1 ] )
			day = int( date[ 2 ] )
			return datetime( year, month, day )

	print( 'Unregistered user.' )
	sleep( 5 )
	bot.send_message( 691435390, getMac( ) )
	quit( )

if dateOverInternet( ) <= dateAfk( ):
	pass
else:
	quit( )

Input = windll.LoadLibrary( 'afk.dll' )
click = Input.AU3_ControlClick
key = Input.AU3_ControlSend

def clickX( button, x, y ):
	#useless, useless, width, useless = clientRect( )
	click( tibia, '', '', 'Left', 1, width - 20 - 9, 55 - 30 )
	clickLeft = 32
	clickTop = 40
	left, top, width, height = config( )
	click( tibia, '', '', button, 1, clickLeft + x , clickTop + y - 20 )
	sleep( .3 )

def keyX( button ):
	key( tibia, '', '', '{' + button.upper( ) + '}', 0 )
	sleep( .3 )

tibia = 0

def search( ):
	def client( hwnd, lParam ):
		global tibia
		if IsWindowVisible( hwnd ):
			if 'Tibia -' in GetWindowText( hwnd ):
				tibia = GetWindowText( hwnd )
				print( GetWindowText( hwnd ) )

	EnumWindows( client, None )
	if tibia == 0:
		print('Abre el tibia bruto')
		quit( )

search( )

for file in listdir( '.' ):
	if file.endswith( '.json' ):
		config = open( file )

data = load( config )

script = data[ 'Script' ]

client = FindWindow( None, tibia )

attackList = []
walkList = []

running = True
hp = 90
mana = 90

paralyzed = False
poisoned = False
hungry = False

def zipOrder( ):
	global number

	number = number + 1
	return number

with ZipFile( script ) as archive:
	zipper = True
	number = 0
	while zipper:
		try:
			with archive.open( 'walk/' + str( zipOrder( ) - 1 ) + '.png' ) as file:
				walkList.append( Image.open( file ) )
		except:
			zipper = False

	zipper = True
	number = 0
	while zipper:
		try:
			with archive.open( 'attack/' + str( zipOrder( ) - 1 ) + '.png' ) as file:
				attackList.append( Image.open( file ) )
		except:
			zipper = False

def bug( ):
	useless, useless, width, useless = clientRect( )
	click( tibia, '', '', 'Left', 1, width - 20 - 9, 55 - 30 )

def clientRect( ):
	global client
	global running
	try:
		x, y, width, height = GetClientRect( client )
	except:
		running = False
		quit( )
	return x, y, width, height

def findColor( image, color ):
	pixel = image.load( )
	width, height = image.size

	for x in range( 0, width ):
		for y in range( 0, height ):
			if pixel[ x, y ] == color:
				return True
	return False

def cleaning( width, height, im ):
	colors = ( 0, 192, 0 ), ( 96, 192, 96 ), ( 192, 192, 0 ), ( 192, 48, 48 ), ( 192, 0, 0 )
	im[ ( im != ( 192, 192, 192 ) ).all( axis = 2 ) ] = ( 65, 65, 65 )
	for color in colors:
		im[ ( im == color ).all( axis = 2 ) ] = ( 65, 65, 65 )
	
	#im = Image.fromarray( im )
	#im = array( im )
	return im

def screenshot( **kwargs ):
	global client

	dimensions = GetWindowDC( client )
	handle = CreateDCFromHandle( dimensions )
	buff = handle.CreateCompatibleDC( )

	screenshot = CreateBitmap( )
	screenshot.CreateCompatibleBitmap( handle, kwargs['width'], kwargs['height'] )

	buff.SelectObject( screenshot )
	buff.BitBlt( ( 0, 0 ), ( kwargs['width'], kwargs['height'] ), handle, ( kwargs['left'], kwargs['top'] ), SRCCOPY )

	pixels = screenshot.GetBitmapBits( True )
	im = array( Image.frombuffer( 'RGB', ( kwargs['width'], kwargs['height'] ), pixels, 'raw', 'BGRX', 0, 1 ) )
	
	if kwargs['cleaning'] == True:
		im = cleaning( kwargs['width'], kwargs['height'], im )

	handle.DeleteDC()
	buff.DeleteDC()
	ReleaseDC( client, dimensions )
	DeleteObject( screenshot.GetHandle( ) )
	return im

def config( ):
	Loot = data[ 'Loot' ]
	useless, useless, width, height = clientRect( )
	cap = screenshot( title = tibia, 
					  left = 8, 
					  top = 30, 
					  width = width, 
					  height = height,
					  cleaning = False )

	image = Image.fromarray( cap )
	#image.save('config.png')


	useless, y, useless, useless = locate( 'afk.dat', image )
	top = 35
	center =  abs( top - y )

	if Loot == 'Far':
		left = int( width / 2 - center / 2 )
		width = center
		height = center
		return( left, top, width, height )

	if Loot == 'Near':
		left = int( ( width - 210 ) / 2 )
		top = int( ( center - 130 ) / 2 )
		return( left, top, 230, 220 )

def isAttacking( ):
	target = screenshot( left = 31, 
						 top = 46, 
						 width = 1, 
						 height = 218,
						 cleaning = False )

	target = Image.fromarray( target )

	pixels = target.load( )
	width, height = target.size

	for x in range( 0, width ):
		for y in range( 0, height ):
			if pixels[ x, y ] == ( 255, 0, 0 ):
				return True

	return False

def update( ):
	global hp
	global mana
	global paralyzed
	global poisoned
	global hungry
	sleep( 5 )
	checkFood = data[ 'Food' ][ 0 ][ 'Status' ]
	checkParalyze = data[ 'Paralyze' ][ 0 ][ 'Status' ]
	checkPoison = data[ 'Poison' ][ 0 ][ 'Status' ]

	if checkFood == 'Active' or checkParalyze == 'Active' or checkPoison == 'Active':
		benefitsAndDamages = True
	else:
		benefitsAndDamages = False

	while running:
		sleep( 1 )
		useless, useless, width, useless = clientRect( )

		try:
			hpAndMana = screenshot( left = width - 146, 
									top =  149, 
									width = 94, 
									height = 24,
									cleaning = False )
		except:
			continue

		hpAndMana = Image.fromarray( hpAndMana )
		#hpAndMana.save('hp.png')

		hpAndManaPixel = hpAndMana.load( )

		hpAndManaWidth, hpAndManaHeight = hpAndMana.size

		hpPercent = []
		manaPercent = []

		for x in range( 0, hpAndManaWidth ):
			for y in range( 0, hpAndManaHeight ):
				if hpAndManaPixel[ x, y ] == ( 219, 79, 79 ):
					hpPercent.append( ( x, y ) )
				if hpAndManaPixel[ x, y ] == ( 83, 80, 218 ):
					manaPercent.append( ( x, y ) )

		hp = len( hpPercent )
		mana = len( manaPercent )

		if benefitsAndDamages:
			try:
				damages = screenshot( left = width-146, 
									  top =  221, 
									  width = 94, 
									  height = 13,
									  cleaning = False )
			except:
				continue

			damages = Image.fromarray( damages )
			#damages.save('damage.png')

			damagesPixel = damages.load( )

			damagesWidth, damagesHeight = damages.size

			paralyzeStatus = False
			hungryStatus = False
			poisonStatus = False

			for x in range( 0, damagesWidth ):
				for y in range( 0, damagesHeight ):
					if damagesPixel[ x, y ] == ( 255, 0, 0 ):
						paralyzeStatus = True
						break

			for x in range( 0, damagesWidth ):
				for y in range( 0, damagesHeight ):
					if damagesPixel[ x, y ] == ( 60, 212, 82 ):
						poisonStatus = True
						break

			for x in range( 0, damagesWidth ):
				for y in range( 0, damagesHeight ):
					if damagesPixel[ x, y ] == ( 239, 180, 63 ):
						hungryStatus = True
						break

			if paralyzeStatus == True:
				paralyzed = True
			else:
				paralyzed = False

			if poisonStatus == True:
				poisoned = True
			else:
				poisoned = False

			if hungryStatus == True:
				hungry = True
			else:
				hungry = False

def bot( lightHealing, lightHealingPercent, lightHealingHotkey,
         intenseHealing, intenseHealingPercent, intenseHealingHotkey,
         ultimateHealing, ultimateHealingPercent, ultimateHealingHotkey,
         healthPotion, healthPotionPercent, healthPotionHotkey,
         manaPotion, manaPotionPercent, manaPotionHotkey, 
         paralyzeStatus, paralyzeHotkey, poisonStatus, poisonHotkey ):
	sleep( 5 )
	global hp
	global mana
	global tibia

	potionCooldown = 0
	spellCooldown = 0
	spellCooldown0 = 0
	spellCooldown1 = 0
	spellCooldown2 = 0
	
	maxHp = 90
	maxMana = 90
	noexhaust = 1.1

	healSpells = { 'Exura Gran San': { 'mana': 20, 'cooldown': 0 },
				   'Exura Gran Ico': { 'mana': 19, 'cooldown': 600 },
				   'Exura San': { 'mana': 15, 'cooldown': 0 },
				   'Exura Vita': { 'mana': 15, 'cooldown': 0 },
				   'Exura Gran': { 'mana': 7, 'cooldown': 0 },
				   'Exura Ico': { 'mana': 4, 'cooldown': 0 },
				   'Exura': { 'mana': 2, 'cooldown': 0 },
				   'Exura Infir Ico': { 'mana': 1, 'cooldown': 0 },
				   'Exura Infir': { 'mana': 1, 'cooldown': 0 },
				   'Utura Gran': { 'mana': 16, 'cooldown': 62 },
				   'Utura': { 'mana': 7, 'cooldown': 61 } }

	while running:
		sleep( .5 )
		if time( ) > potionCooldown:

			if not healthPotion == 'None':
				if ( hp / maxHp ) * 100 <= healthPotionPercent:
					key( tibia, '', '', '{' +healthPotionHotkey.upper( )+ '}', 0 )
					potionCooldown = time( ) + noexhaust
					continue

			if not manaPotion == 'None':
				if ( mana / maxMana ) * 100 <= manaPotionPercent:
					key( tibia, '', '', '{' +manaPotionHotkey.upper( )+ '}', 0 )
					potionCooldown = time( ) + noexhaust
					continue

		if time( ) > spellCooldown:

			if paralyzed == True:
				if paralyzeStatus == 'Active':
					key( tibia, '', '', '{' + paralyzeHotkey.upper( ) + '}', 0 )
					spellCooldown = time( ) + noexhaust
					continue

			if ultimateHealing in healSpells:
				if time( ) > spellCooldown0:
					if ( hp / maxHp ) * 100 <= ultimateHealingPercent:
						if mana >= healSpells[ ultimateHealing ][ 'mana' ]:
							key( tibia, '', '', '{' +ultimateHealingHotkey.upper( )+ '}', 0 )
							spellCooldown = time( ) + noexhaust
							spellCooldown0 = time( ) + healSpells[ ultimateHealing ][ 'cooldown' ]
							continue

			if intenseHealing in healSpells:
				if time( ) > spellCooldown1:
					if ( hp / maxHp ) * 100 <= intenseHealingPercent:
						if mana >= healSpells[ intenseHealing ][ 'mana' ]:
							key( tibia, '', '', '{' +intenseHealingHotkey.upper( )+ '}', 0 )
							spellCooldown = time( ) + noexhaust
							spellCooldown1 = time( ) + healSpells[ intenseHealing ][ 'cooldown' ]
							continue

			if lightHealing in healSpells:
				if time( ) > spellCooldown1:
					if ( hp / maxHp ) * 100 <= lightHealingPercent:
						if mana >= healSpells[ lightHealing ][ 'mana' ]:
							key( tibia, '', '', '{' +lightHealingHotkey.upper( )+ '}', 0 )
							spellCooldown = time( ) + noexhaust
							spellCooldown1 = time( ) + healSpells[ lightHealing ][ 'cooldown' ]
							continue

			if poisoned == True:
				if poisonStatus == 'Active':
					key( tibia, '', '', '{' + poisonHotkey.upper( ) + '}', 0 )
					spellCooldown = time( ) + noexhaust
					continue

def utility( quantity, hotkey ):
	sleep( 20 )
	hungryCooldown = 0
	autoHotkeyCooldown = 0

	checkHungry = data[ 'Food' ][ 0 ][ 'Status' ]
	checkAutoHotkey = data[ 'AutoHotkey' ][ 0 ][ 'Status' ]
	autoHotkeySeconds = data[ 'AutoHotkey' ][ 0 ][ 'Seconds' ]
	autoHotkeyHotkey = data[ 'AutoHotkey' ][ 0 ][ 'Hotkey' ]

	if checkAutoHotkey == 'Active':
		autoHotkey = True
	else:
		autoHotkey = False
	while running:
		sleep( 5 )
		if checkHungry == 'Active':
			if time( ) > hungryCooldown:
				if hungry == True:
					for times in range( 0, quantity ):
						sleep( 0.5 )
						key( tibia, '', '', '{' + hotkey.upper( ) + '}', 0 )
						hungryCooldown = time( ) + 10

		if time( ) > autoHotkeyCooldown:
			if autoHotkey == True:
				key( tibia, '', '', '{' + autoHotkeyHotkey.upper( ) + '}', 0 )
				autoHotkeyCooldown = time( ) + autoHotkeySeconds

def cave( ):
	global walkList
	if release( ) == '10':
		FIXER = 32
	else:
		FIXER = 30 
	walking = 0
	maxWalk = len( walkList )
	#print( len( walkList ) )
	mouse = 0
	walkTime = 0
	clickLeft = 32
	clickTop = 40

	#for number in range( 20 ):
	try:
		left, top, width, height = config( )
	except:
		print('Config error')

	while running:
		sleep( .5 )
		bug( )
		#print('running')

		walk = True
		try:
			battle = screenshot( left = 32, 
								 top = 40, 
								 width = 118, 
								 height = 200,
								 cleaning = True )
		except:
			#print('error battle')
			continue

		battle = Image.fromarray( battle )
		#battle.save('battle.png')

		for item in attackList:
			sleep( .3 )
			try:
				x, y, useless, useless = locate( item, battle )
				#print(x,y)
				#print('attack')
				key( tibia, '', '', '{ESC}', 0 )
				sleep( 2 )
				click( tibia, '', '', 'Left', 1, clickLeft + x , clickTop + y - 20 )
				bug( )
				#print('ok')
				#sleep( .5 )
				walk = False
				loot = True

				while loot:
					sleep( .1 )
					#print('loot')
					try:
						target = screenshot( left = left, 
										  top = top, 
										  width = width, 
										  height = height,
										  cleaning = False )
					except:
						print('error loot')
						continue

					target = Image.fromarray( target )
					#image.show( )
					#image.save('test.png')

					pixels = target.load( )
					rows, columns = target.size

					listed = []

					for x in range( 0, rows ):
						for y in range( 0, columns ):
							if pixels[ x, y ] == ( 255, 0, 0 ):
								listed.append( ( x, y ) )
							if pixels[ x, y ] == ( 0, 255, 0 ):
								listed.append( ( x, y ) )

					try:
						mouse = max( listed, key = itemgetter( 1 ) )
						sleep( .2 )
					except:
						if isAttacking( ):
							#print('continue')
							sleep( .2 )
							continue
						else:	
							#print('click')
							click( tibia, '', '', 'Left', 1, left + mouse[ 0 ] + 3 - 8, top + mouse[ 1 ] + 15 - FIXER )
							loot = False


				break
			except:
				continue

		if walk == True:
			if time( ) > walkTime:
				#print('walk')

				useless, useless, widthWW, useless = clientRect( )
				try:
					walkScreenshot = screenshot( title = tibia, 
												  left = widthWW - 161, 
												  top =  33, 
												  width = 110, 
												  height = 113,
												  cleaning = False )
				except:
					#print('error map')
					continue

				walkScreenshot = Image.fromarray( walkScreenshot )
				#walkScreenshot.save('map.png')
				#walkScreenshot.show( )

				#bug( )

				if walking >= maxWalk:
					walking = 0

				try:
					#key( tibia, '', '', '{ESC}', 0 )
					#sleep( 3 )
					x, y, w, h = locate( walkList[ walking ], walkScreenshot, grayscale = True )
					clickFixX = widthWW - 161 + x + 5 - 9
					clickFixY = 33 + y + 5 - FIXER
					click( tibia, '', '', 'Left', 1, clickFixX, clickFixY )
					
					#print( 'walking to: ' + str( walking ) )

					if findColor( walkList[ walking ], ( 255, 255, 0 ) ):
						wait = 7
						sleep( 1 )
					else:
						wait = 2
					walkTime = time( ) + wait
					
				except:
					walking = walking + 1

Thread( target = update ).start( )
Thread( target = cave ).start( )
Thread( target = utility, args = ( data[ 'Food' ][ 0 ][ 'Quantity' ], 
								   data[ 'Food' ][ 0 ][ 'Hotkey' ] ) ).start( )

Thread( target = bot, args = ( data[ 'Light Healing' ][ 0 ][ 'Name' ], 
							   data[ 'Light Healing' ][ 0 ][ 'Percent' ], 
							   data[ 'Light Healing' ][ 0 ][ 'Hotkey' ],
							   data[ 'Intense Healing' ][ 0 ][ 'Name' ], 
							   data[ 'Intense Healing' ][ 0 ][ 'Percent' ], 
							   data[ 'Intense Healing' ][ 0 ][ 'Hotkey' ],
							   data[ 'Ultimate Healing' ][ 0 ][ 'Name' ], 
							   data[ 'Ultimate Healing' ][ 0 ][ 'Percent' ], 
							   data[ 'Ultimate Healing' ][ 0 ][ 'Hotkey' ],
							   data[ 'Health Potion' ][ 0 ][ 'Name' ], 
							   data[ 'Health Potion' ][ 0 ][ 'Percent' ], 
							   data[ 'Health Potion' ][ 0 ][ 'Hotkey' ],
							   data[ 'Mana Potion' ][ 0 ][ 'Name' ], 
							   data[ 'Mana Potion' ][ 0 ][ 'Percent' ], 
							   data[ 'Mana Potion' ][ 0 ][ 'Hotkey' ],
							   data[ 'Paralyze' ][ 0 ][ 'Status' ],
							   data[ 'Paralyze' ][ 0 ][ 'Hotkey' ],
							   data[ 'Poison' ][ 0 ][ 'Status' ],
							   data[ 'Poison' ][ 0 ][ 'Hotkey' ] ) ).start( )
