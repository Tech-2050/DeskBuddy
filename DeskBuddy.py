from m5stack import * # Import the required librarys 
from m5stack_ui import *
from uiflow import *
import time
import network
import urequests
import random
from IoTcloud.AWS import AWS

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xc3bf40) #Set the screen colour to yellow

station = network.WLAN(network.STA_IF) #Connect to Wi-Fi network
station.active(True)
station.connect("SSID", "PASSWORD")
station.isconnected()


emotion = 'eyes' #Set up all of the starting values for variables
start_time = (rtc.datetime()[6]) + ((rtc.datetime()[5]) * 60) + ((rtc.datetime()[4]) * 60 * 60)
mute = False
newface = False
t = 0
stop = True
URL = 'TOKEN' # IFTTT webhooks token

def page4(): # Page to request action on another device
  global mute, aws 
  # Setup all of the widgets
  cofferequest = M5Label('Request a coffee', x=13, y=56, color=0x000, font=FONT_MONT_14, parent=None)
  walkrequest = M5Label('Request a walk', x=13, y=97, color=0x000, font=FONT_MONT_14, parent=None)
  requestplay = M5Label('Request to play an', x=13, y=136, color=0x000, font=FONT_MONT_14, parent=None)
  title = M5Label('Contact other devices', x=38, y=0, color=0x000, font=FONT_MONT_22, parent=None)
  coffee = M5Btn(text='Request', x=194, y=48, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  walk = M5Btn(text='Request', x=194, y=88, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  game = M5Btn(text='Request', x=194, y=127, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  joke = M5Btn(text='Send', x=194, y=167, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  sendjoke = M5Label('Send a joke', x=16, y=176, color=0x000, font=FONT_MONT_14, parent=None)
  onlinegame = M5Label('online game', x=13, y=148, color=0x000, font=FONT_MONT_14, parent=None)
  meetup = M5Label('meetup', x=13, y=71, color=0x000, font=FONT_MONT_14, parent=None)
  
  time.sleep(5)
  
  while True:
  
    def coffee_pressed(): # When the button is pressed publish 'coffee' to aws iot core
      global aws
      aws.publish(str('core2/env'),str('coffee'))
      pass
    coffee.pressed(coffee_pressed)
    
    def walk_pressed():
        global aws
        aws.publish(str('core2/env'),str('walk'))
        pass
    walk.pressed(walk_pressed)
    
    def game_pressed():
        global aws
        aws.publish(str('core2/env'),str('game'))
        pass
    game.pressed(game_pressed)
    
    def joke_pressed():
        global aws
        aws.publish(str('core2/env'),str('joke'))
        pass
    joke.pressed(joke_pressed)
    
    if (btnA.isPressed()) == True: # Go to the previous page when the A button is pressed
        # Hide contact device items
        cofferequest.set_hidden(True)
        walkrequest.set_hidden(True)
        requestplay.set_hidden(True)
        title.set_hidden(True)
        coffee.set_hidden(True)
        walk.set_hidden(True)
        game.set_hidden(True)
        joke.set_hidden(True)
        sendjoke.set_hidden(True)
        onlinegame.set_hidden(True)
        meetup.set_hidden(True)
  
        page3()
    elif (btnB.isPressed()) == True: # Set everything to mute when the B button is pressed
      if mute == True:
        mute = False
        rgb.setColorAll(0x000000)
        pass
      elif mute == False:
        mute = True
        rgb.setColorAll(0xf00000)
        pass
    elif (btnC.isPressed()) == True:# Go to the next page when the A button is pressed
      # Hide contact device items
      cofferequest.set_hidden(True)
      walkrequest.set_hidden(True)
      requestplay.set_hidden(True)
      title.set_hidden(True)
      coffee.set_hidden(True)
      walk.set_hidden(True)
      game.set_hidden(True)
      joke.set_hidden(True)
      sendjoke.set_hidden(True)
      onlinegame.set_hidden(True)
      meetup.set_hidden(True)
  
      homescreen()



def page3():
  global maintitle, mintitle, sectitle, stopstart, Seconds, Minutes, Secondtext, minutetext, SecondsliderText, MinutesliderText, mute
  # Setup all of the widgets 
  maintitle = M5Label('Countdown Timer', x=32, y=8, color=0x000, font=FONT_MONT_28, parent=None)
  mintitle = M5Label('Min:', x=19, y=52, color=0x000, font=FONT_MONT_24, parent=None)
  sectitle = M5Label('Sec:', x=21, y=85, color=0x000, font=FONT_MONT_24, parent=None)
  stopstart = M5Btn(text='Stop/start', x=184, y=70, w=90, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  Seconds = M5Slider(x=35, y=144, w=250, h=12, min=0, max=60, bg_c=0x08A2B0, color=0x08A2B0, parent=None)
  Minutes = M5Slider(x=35, y=193, w=250, h=12, min=0, max=60, bg_c=0x08A2B0, color=0x08A2B0, parent=None)
  Secondtext = M5Label('Seconds', x=38, y=165, color=0x000, font=FONT_MONT_14, parent=None)
  minutetext = M5Label('Minutes', x=35, y=217, color=0x000, font=FONT_MONT_14, parent=None)
  SecondsliderText = M5Label('Text', x=184, y=165, color=0x000, font=FONT_MONT_14, parent=None)
  MinutesliderText = M5Label('Text', x=184, y=217, color=0x000, font=FONT_MONT_14, parent=None)
  
  def countdown(t): # Everything needed to countdown to 0 from the time entered on the sliders
    global maintitle, mintitle, sectitle, stopstart, Seconds, Minutes, Secondtext, minutetext, SecondsliderText, MinutesliderText, mute
    while t: # Keep repeating until time is none
        completed = True 
        mins, secs = divmod(t, 60) # Calculate the seconds and minutes to display
        Time = M5Label((str(secs)), x=92, y=85, color=0x000, font=FONT_MONT_32, parent=None) # Display the calculated time
        Time2 = M5Label((str(mins)), x=92, y=53, color=0x000, font=FONT_MONT_32, parent=None)
        t -= 1 # Take 1 second off the timer
        
        if (stopstart.get_state()) == True: # Check if the timer stop button has been pressed
          Time.set_hidden(True) # Hide seconds and minutes
          Time2.set_hidden(True)
          t = None
          completed = False
        
        elif (btnA.wasPressed()) == True:
          maintitle.set_hidden(True)
          mintitle.set_hidden(True)
          sectitle.set_hidden(True)
          stopstart.set_hidden(True)
          Seconds.set_hidden(True)
          Minutes.set_hidden(True)
          Secondtext.set_hidden(True)
          minutetext.set_hidden(True)
          SecondsliderText.set_hidden(True)
          MinutesliderText.set_hidden(True)
          t = None
      	  page2()
        elif (btnC.wasPressed()) == True:
          maintitle.set_hidden(True)
          mintitle.set_hidden(True)
          sectitle.set_hidden(True)
          stopstart.set_hidden(True)
          Seconds.set_hidden(True)
          Minutes.set_hidden(True)
          Secondtext.set_hidden(True)
          minutetext.set_hidden(True)
          SecondsliderText.set_hidden(True)
          MinutesliderText.set_hidden(True)
          t = None
          page4()
        
        time.sleep(1)
        Time.set_hidden(True)
        Time2.set_hidden(True)
    if completed == True and mute == False: # When timer is completed and mute is not set turn on vibration and flash the RGB leds white
      for i in range(20):
        rgb.setColorAll(0xffffff)
        power.setVibrationEnable(True)
        time.sleep(0.2)
        rgb.setColorAll(0x000000)
        power.setVibrationEnable(False)
        time.sleep(0.2)
  
  
  time.sleep(5) # Wait 5 seconds
  while True: # Repeat forever
    SecondsliderText.set_text(str(Seconds.get_value())) # Get the value of the sliders
    MinutesliderText.set_text(str(Minutes.get_value()))
    
    if (btnA.wasPressed()) == True: # If the A button is pressed go to the previous page
      maintitle.set_hidden(True)
      mintitle.set_hidden(True)
      sectitle.set_hidden(True)
      stopstart.set_hidden(True)
      Seconds.set_hidden(True)
      Minutes.set_hidden(True)
      Secondtext.set_hidden(True)
      minutetext.set_hidden(True)
      SecondsliderText.set_hidden(True)
      MinutesliderText.set_hidden(True)
      page2()
    elif (btnB.isPressed()) == True: # If the B button is pressed mute everything
      if mute == True:
        mute = False
        pass
        rgb.setColorAll(0x000000)
      elif mute == False:
        mute = True
        rgb.setColorAll(0xf00000)
        pass
    elif (btnC.wasPressed()) == True:# If the C button is pressed go to the next page
      mintitle.set_hidden(True)
      maintitle.set_hidden(True)
      sectitle.set_hidden(True)
      stopstart.set_hidden(True)
      Seconds.set_hidden(True)
      Minutes.set_hidden(True)
      Secondtext.set_hidden(True)
      minutetext.set_hidden(True)
      SecondsliderText.set_hidden(True)
      MinutesliderText.set_hidden(True)
      page4()
    elif (stopstart.get_state()) == True: # If the start button is pressed start the stopwatch
      countdown((Minutes.get_value() * 60) + Seconds.get_value())


def page2(): # Stopwatch page
  global title, Sec, Min, t, mute
  # Setup all of the widgets 
  image0 = M5Img("res/stopwatch.png", x=7, y=49, parent=None)
  Sec = M5Label(('0'), x=195, y=86, color=0x000, font=FONT_MONT_48, parent=None)
  Min = M5Label(('0'), x=124, y=86, color=0x000, font=FONT_MONT_48, parent=None)
  colon = M5Label(':', x=175, y=90, color=0x000, font=FONT_MONT_40, parent=None)
  maintitle = M5Label('Stopwatch', x=84, y=6, color=0x000, font=FONT_MONT_28, parent=None)
  stopstart = M5Btn(text='Start', x=85, y=157, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_20, parent=None)
  stopbtn = M5Btn(text='Stop', x=160, y=157, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_20, parent=None)
  reset = M5Btn(text='Reset', x=120, y=195, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_20, parent=None)

  def startstopwatch(): # Function to setup to start the stopwatch
    global t, Sec, Min, mute
  
    while True: # Repeat forever
      Sec.set_hidden(True) # Show the seconds and minutes
      Min.set_hidden(True)
      t = t + 1 
      mins, secs = divmod(t, 60) # Calculate the seconds and minutes from the t variable
      Sec = M5Label((str(secs)), x=195, y=86, color=0x000, font=FONT_MONT_48, parent=None) # Show the time on the screen
      Min = M5Label((str(mins)), x=124, y=86, color=0x000, font=FONT_MONT_48, parent=None)
      Sec.set_hidden(False) # Hide the seconds and minutes
      Min.set_hidden(False)
      if (stopbtn.get_state()) == True: # Exit the repeat forever if the stop button is pressed
        break
      time.sleep(1) # Wait for 1 second
  
  time.sleep(3) # Wait for 3 seconds
  while True: # Repeat forever
    if (stopstart.get_state()) == True: # If the start button is pressed call the startstopwatch function
      startstopwatch() 
    elif (reset.get_state()) == True: # If the reset button is pressed
      Sec.set_hidden(True) # Hide minutes and seconds
      Min.set_hidden(True)
      t = 0 # Set the time to 0
      mins, secs = divmod(t, 60) # Calculate the minutes and seconds
      Sec = M5Label((str(secs)), x=195, y=86, color=0x000, font=FONT_MONT_48, parent=None) # Output the minutes and seconds to the screen
      Min = M5Label((str(mins)), x=124, y=86, color=0x000, font=FONT_MONT_48, parent=None)    
    elif (btnA.isPressed()) == True: # If the A button is pressed go to the previous page
      image0.set_hidden(True)
      Sec.set_hidden(True)
      Min.set_hidden(True)
      colon.set_hidden(True)
      maintitle.set_hidden(True)
      stopstart.set_hidden(True)
      stopbtn.set_hidden(True)
      reset.set_hidden(True)
      page1()
    elif (btnB.isPressed()) == True: # If the B button is pressed mute everything
      if mute == True:
        mute = False
        rgb.setColorAll(0x000000)
        pass
      elif mute == False:
        mute = True
        rgb.setColorAll(0xf00000)
        pass
    elif (btnC.isPressed()) == True: # If the C button is pressed go to the next page
      image0.set_hidden(True)
      Sec.set_hidden(True)
      Min.set_hidden(True)
      colon.set_hidden(True)
      maintitle.set_hidden(True)
      stopstart.set_hidden(True)
      stopbtn.set_hidden(True)
      reset.set_hidden(True)
      page3()





def sleepy(): # Returns what to tell the user when the display shows the sleepy emotion
  global URL # Setup then global variables
  def joke():
    global URL
    #Create a joke, from https://code.sololearn.com/cF4n42PAWsqW#py
    #Random Joke Generator V 1.2
    #Use This if you ran out of jokes
    #NOTICE: May Contain some puns instead of jokes
    #Puns for cringeness only
    #By DerpyOmnister
    #INPUT WHAT KIND OF JOKE YOU WANT
    #List: Puns, bar joke, knock knock, dumb-funny
    Joke = random.choice(["pun", "bar_joke", "knock_knock", "dumb_funny"])

    #joke Loops for specific types

    if Joke == "pun":
        pun = random.choice(["Why Couldn't The bike Stand on it's own? It was Two Tired!", "Whoever Stole My Copy of Microsoft Office is in Big Trouble! You got my word!", "Need an ark? I Noah Guy!", "Frog Parking Only! Any one else will be toad away.", "Renewable Energy? I'm a big Fan!", "Becoming a vegetarian is a huge missed steak!", "Have you ever eight a clock? It's so time-consuming!"])
        return(str(pun))


    elif Joke == "bar_joke":
        bar = random.choice(["'Poor Old fool,' thought the well-dressed gentleman as he watched an old man fish in a puddle outside a pub. So he invited the old man inside for a drink. As they sipped their whiskeys, the gentleman thought he'd humor the old man and asked, 'So how many have you caught today?' The old man replied, 'Your the eighth", "Infinitely many mathematicians walk into a bar. The first says, 'I'll have a beer.' The second says, 'I'll have half a beer.' The third says, 'I'll have a quarter of a beer.' Before anyone else can speak, the barman fills up exactly two glasses of beer and serves them. 'Come on, now,' he says to the group, 'You guys have got to learn your limits.'", "At an all-you-can-eat buffet, my nine-year-old was excited to find a chocolate milk machine. But her aunt did not approve. 'Chocolate milk for dinner?' she asked. 'It's delicious!' said my daughter. Her aunt shrugged. 'Well, its 8 a.m. somewhere.'", "The barman says, 'We don’t serve time travelers in here.' A time traveler walks into a bar."])
        return(str(bar))

        
    elif Joke == "knock_knock":
        knock_knock = random.choice(["'Knock-Knock!' 'Who's There?' 'Control Freak' 'Con-' 'Now you say Control Freak Who.'", "'Knock-Knock!' 'Who's There?' 'Ho-Ho' 'Ho-Ho Who?' 'You could use a little work on your santa impression.'", "'Knock-Knock!' 'Who's There?' 'Santa' 'Santa Who?' 'I santa email I'd be here and I'm still waiting out in the cold!'", "'Knock-Knock!' 'Who's there?' 'Snow' 'Snow Who?' 'Snow Use! I forgot my name again.'"])
        return(str(knock_knock))

        
    elif Joke == "dumb_funny":
        reg = random.choice(["Client: Please remove the unnecessary circle at the end of the sentence.  Me: You mean … the period?  Client: I don’t care what you designers call it; it is unsightly. Delete it.", "When asked for his name by the coffee shop clerk, my brother-in-law answered, 'Marc, with a C.' Minutes later, he was handed his coffee with his name written on the side: Cark.", "An insurance agent called our medical office. One of our doctors had filled out a medically necessary leave-of-absence form for a patient, but, the agent said, the patient had altered it. The giveaway? The return-to-work date had been changed to February 30.", "A defendant isn't happy with how things are going in court, so he gives the judge a hard time.  Judge: 'Where do you work?'  Defendant: 'Here and there.'  Judge: 'What do you do for a living?'  Defendant: 'This and that.'  Judge: 'Take him away.'  Defendant: 'Wait; when will I get out?'  Judge: 'Sooner or later.'", "A first-grade teacher can’t believe her student isn’t hepped up about the Super Bowl. 'It’s a huge event. Why aren’t you excited?'   'Because I’m not a football fan. My parents love basketball, so I do too,' says the student.  'Well, that’s a lousy reason,' says the teacher. 'What if your parents were morons? What would you be then?'  'Then I’d be a football fan.'", "While on patrol, I arrested a burglar who’d injured himself running from a home. He told me he’d broken in and unhooked the phone before searching for valuables. But he’d panicked when he heard a woman’s voice. I entered the house and heard the same voice: “If you’d like to make a call, please hang up and try your call again.”"])
        return(str(reg))

  randomchoice = random.randint(1, 3) # Pick a random number between 1 and 3
  
  if randomchoice == 1: 
    return(joke()) # Return the output with a random joke from the joke function
  elif randomchoice == 2:
    return('do some yoga')
    response = urequests.post("http://maker.ifttt.com/sleepy/game/with/key/" + URL) # Send the yoga IFTTT request
  elif randomchoice == 3:
    return('go for a walk')
    response = urequests.post("http://maker.ifttt.com/trigger/walk/with/key/" + URL) # Send the walk IFTTT request

def angry(): # Returns what to tell the user when the display shows the angry emotion
  global URL # Setup then global variables
  randomchoice = random.randint(1, 3) # Pick a random number between 1 and 3
  
  if randomchoice == 1:
    return('step away from the screen')
  elif randomchoice == 2:
    return('Look out a window')
  elif randomchoice == 3:
    return('Watch a funny animal playlist')
    response = urequests.post("http://maker.ifttt.com/trigger/sad/with/key/" + URL) # Send the sad IFTTT request 

def sad(): # Returns what to tell the user when the display shows the sad emotion
  global URL # Setup then global variables
  randomchoice = random.randint(1, 3) # Pick a random number between 1 and 3
  
  if randomchoice == 1:
    return('Listen to some new music')
  elif randomchoice == 2:
    return('Call a friend')
  elif randomchoice == 3:
    return('Watch a funny animal playlist')
    response = urequests.post("http://maker.ifttt.com/trigger/sad/with/key/" + URL) # Send the sad IFTTT request 
    

def walk(): # Returns what to tell the user when they receive a request for a walk from another device
  global stop, URL # Setup then global variables
  # Setup the widgets for the page
  title = M5Label('Activity request from', x=28, y=0, color=0x000, font=FONT_MONT_22, parent=None)
  label0 = M5Label('another device', x=62, y=24, color=0x000, font=FONT_MONT_22, parent=None)
  label1 = M5Label('Another device has ', x=153, y=60, color=0x000, font=FONT_MONT_14, parent=None)
  continuebtn = M5Btn(text='Continue', x=243, y=201, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
  activity = M5Label('a walk', x=230, y=80, color=0x000, font=FONT_MONT_14, parent=None)
  label2 = M5Label('requested', x=153, y=80, color=0x000, font=FONT_MONT_14, parent=None)
  label3 = M5Label('A link to your nearest', x=144, y=113, color=0x000, font=FONT_MONT_14, parent=None)
  label4 = M5Label('park has been', x=142, y=130, color=0x000, font=FONT_MONT_14, parent=None)
  label5 = M5Label('sent to your phone', x=143, y=146, color=0x000, font=FONT_MONT_14, parent=None)
  image0 = M5Img("res/walking.png", x=14, y=75, parent=None)
  
  while True: # Repeat forever
    if (continuebtn.get_state()) == True: # If the continuebtn is pressed go back to the homepage
      title.set_hidden(True)
      label0.set_hidden(True)
      label1.set_hidden(True)
      continuebtn.set_hidden(True)
      activity.set_hidden(True)
      label2.set_hidden(True)
      label3.set_hidden(True)
      label4.set_hidden(True)
      label5.set_hidden(True)
      image0.set_hidden(True)
      stop = True
      homepage()
    time.sleep(1)

def coffee(): # Returns what to tell the user when they receive a request for a coffee from another device
  global stop, URL # Setup then global variables
  # Setup the widgets for the page
  import urequests
  # Setup the widgets for the page
  title = M5Label('Activity request from', x=28, y=0, color=0x000, font=FONT_MONT_22, parent=None)
  label0 = M5Label('another device', x=62, y=24, color=0x000, font=FONT_MONT_22, parent=None)
  label1 = M5Label('Another device has ', x=153, y=60, color=0x000, font=FONT_MONT_14, parent=None)
  continuebtn = M5Btn(text='Continue', x=243, y=201, w=70, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  activity = M5Label(' a coffee', x=229, y=80, color=0x000, font=FONT_MONT_14, parent=None)
  label2 = M5Label('requested', x=153, y=80, color=0x000, font=FONT_MONT_14, parent=None)
  label3 = M5Label('A link to your nearest', x=144, y=113, color=0x000, font=FONT_MONT_14, parent=None)
  label4 = M5Label('coffee shop has been', x=142, y=130, color=0x000, font=FONT_MONT_14, parent=None)
  label5 = M5Label('sent to your phone', x=143, y=146, color=0x000, font=FONT_MONT_14, parent=None)
  image0 = M5Img("res/coffee.png", x=46, y=108, parent=None)
  response = urequests.post("http://maker.ifttt.com/trigger/coffee/with/key/" + URL)
  while True: # Repeat forever
    if (continuebtn.get_state()) == True: # If the continuebtn is pressed go back to the homepage
      title.set_hidden(True)
      label0.set_hidden(True)
      label1.set_hidden(True)
      continuebtn.set_hidden(True)
      activity.set_hidden(True)
      label2.set_hidden(True)
      label3.set_hidden(True)
      label4.set_hidden(True)
      label5.set_hidden(True)
      image0.set_hidden(True)
      stop = True
      homepage()
    time.sleep(1)

def game(): # Returns what to tell the user when they receive a request for an online game from another device
  global stop, URL
  title = M5Label('Activity request from', x=28, y=0, color=0x000, font=FONT_MONT_22, parent=None)
  label0 = M5Label('another device', x=62, y=24, color=0x000, font=FONT_MONT_22, parent=None)
  label1 = M5Label('Another device has ', x=153, y=57, color=0x000, font=FONT_MONT_14, parent=None)
  continuebtn = M5Btn(text='Continue', x=243, y=201, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
  activity = M5Label('to play', x=229, y=69, color=0x000, font=FONT_MONT_14, parent=None)
  label2 = M5Label('requested', x=153, y=69, color=0x000, font=FONT_MONT_14, parent=None)
  label3 = M5Label(' A link to an online', x=144, y=113, color=0x000, font=FONT_MONT_14, parent=None)
  label4 = M5Label('game has been', x=142, y=130, color=0x000, font=FONT_MONT_14, parent=None)
  label5 = M5Label('sent to your phone', x=143, y=146, color=0x000, font=FONT_MONT_14, parent=None)
  label6 = M5Label('an online game', x=149, y=83, color=0x000, font=FONT_MONT_14, parent=None)
  image0 = M5Img("res/game.png", x=46, y=108, parent=None)
  response = urequests.post("http://maker.ifttt.com/trigger/game/with/key/" + URL)
  
  while True: # Repeat forever
    if (continuebtn.get_state()) == True: # If the continuebtn is pressed go back to the homepage
      title.set_hidden(True)
      label0.set_hidden(True)
      label1.set_hidden(True)
      continuebtn.set_hidden(True)
      activity.set_hidden(True)
      label2.set_hidden(True)
      label3.set_hidden(True)
      label4.set_hidden(True)
      label5.set_hidden(True)
      image0.set_hidden(True)
      stop = True
      homepage()
    time.sleep(1)
  
def jokeaws(): # Returns what to tell the user when they receive a request for an online game from another device
  global stop, URL # Setup the global variables
  # Setup the items on the display
  title = M5Label('Activity request from', x=28, y=0, color=0x000, font=FONT_MONT_22, parent=None)
  label0 = M5Label('another device', x=62, y=24, color=0x000, font=FONT_MONT_22, parent=None)
  label1 = M5Label('Another device has ', x=153, y=57, color=0x000, font=FONT_MONT_14, parent=None)
  continuebtn = M5Btn(text='Continue', x=243, y=201, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
  activity = M5Label('to play', x=229, y=69, color=0x000, font=FONT_MONT_14, parent=None)
  label2 = M5Label('requested', x=153, y=69, color=0x000, font=FONT_MONT_14, parent=None)
  label3 = M5Label((joke()), x=144, y=113, color=0x000, font=FONT_MONT_14, parent=None)

  while True: # Repeat forever
    if (continuebtn.get_state()) == True: # If the continuebtn is pressed go back to the homepage
      title.set_hidden(True)
      label0.set_hidden(True)
      label1.set_hidden(True)
      continuebtn.set_hidden(True)
      activity.set_hidden(True)
      label2.set_hidden(True)
      label3.set_hidden(True)
      stop = True
      homepage()
    time.sleep(1)
  
  
def homescreen(): # The main homescreen of the device
  global emotion, start_time, mute, newface, aws, image0, image1, info, intotitle, stop, URL # Setup the global variables
  sleepyrun = False # Set the starting states of the variables
  angryrun = False
  sadrun = False
  stop = True
  suggestiongiven = 0
  if emotion == 'eyes': # If the emotion is eyes show the eyes images
    image0 = M5Img("res/eyes.png", x=0, y=0, parent=None)
    image1 = M5Img("res/eyesleft.png", x=0, y=0, parent=None)
  elif emotion == 'sleepy':
    image0 = M5Img("res/sleepy.png", x=0, y=0, parent=None)
    image1 = M5Img("res/sleepy.png", x=0, y=0, parent=None)
    
  while stop == True: 
    currenttime = (rtc.datetime()[6]) + ((rtc.datetime()[5]) * 60) + ((rtc.datetime()[4]) * 60 * 60) # Get the currenttime
    if emotion == 'eyes': # If the emotion is eyes show the eyes images
      image0.set_hidden(True)
      image1.set_hidden(True)
      image0 = M5Img("res/eyes.png", x=0, y=0, parent=None)
      image1 = M5Img("res/eyesleft.png", x=0, y=0, parent=None)
      if newface == True and mute == False:
        rgb.setColorAll(0xffffff)
        power.setVibrationEnable(True)
        time.sleep(0.2)
        rgb.setColorAll(0x000000)
        power.setVibrationEnable(False)
        time.sleep(0.2)
        newface = False
        
    elif emotion == 'sleepy': # If the emotion is eyes show the sleepy images
      image0.set_hidden(True)
      image1.set_hidden(True)
      image0 = M5Img("res/sleepy.png", x=0, y=0, parent=None)
      image1 = M5Img("res/sleepy.png", x=0, y=0, parent=None)
      
    
      if (currenttime - facechangetime) > 20:
        emotion = 'eyes'
      
      if sleepyrun == False:
        infotitle = M5Label('Desk buddy is tired, take a break', x=30, y=22, color=0x000, font=FONT_MONT_14, parent=None)
        info = label0 = M5Label((str(sleepy())), x=15, y=38, color=0x000, font=FONT_MONT_14, parent=None)
        sleepyrun = True
        suggestiongiven = 0
        response = urequests.post("http://maker.ifttt.com/trigger/sleepy/with/key/" + URL)
      if newface == True and mute == False:
        for i in range(3):
          rgb.setColorAll(0xffffff)
          power.setVibrationEnable(True)
          time.sleep(1)
          rgb.setColorAll(0x000000)
          power.setVibrationEnable(False)
          time.sleep(0.5)
          newface = False
          
    elif emotion == 'angry': # If the emotion is eyes show the angry images
      image0.set_hidden(True)
      image1.set_hidden(True)
      response = urequests.post("http://maker.ifttt.com/trigger/angry/with/key/" + URL)
      if suggestiongiven > 2:
        info.set_hidden(True)
        infotitle.set_hidden(True)
      image0 = M5Img("res/angry.png", x=0, y=0, parent=None)
      image1 = M5Img("res/angry.png", x=0, y=0, parent=None)
      
      if (currenttime - facechangetime) > 20:
        emotion = 'eyes'
      
      if angryrun == False:
        infotitle = M5Label('Desk buddy is angry, take a break', x=30, y=22, color=0x000, font=FONT_MONT_14, parent=None)
        info = label0 = M5Label((str(angry())), x=15, y=38, color=0x000, font=FONT_MONT_14, parent=None)
        suggestiongiven = 0
        angryrun = True
      if newface == True and mute == False:
        for i in range(3):
          rgb.setColorAll(0xffffff)
          power.setVibrationEnable(True)
          time.sleep(1)
          rgb.setColorAll(0x000000)
          power.setVibrationEnable(False)
          time.sleep(0.5)
          newface = False
      
    elif emotion == 'sad':# If the emotion is eyes show the sad images
      response = urequests.post("http://maker.ifttt.com/trigger/sad/with/key/" + URL)
      image0.set_hidden(True)
      image1.set_hidden(True)
      if suggestiongiven > 2:
        info.set_hidden(True)
        infotitle.set_hidden(True)
      image0 = M5Img("res/sad.png", x=0, y=40, parent=None)
      image1 = M5Img("res/sad.png", x=0, y=40, parent=None)
      if (currenttime - facechangetime) > 20:
        emotion = 'eyes'
        
      if sadrun == False:
        infotitle = M5Label('Desk buddy is sad, take a break', x=30, y=22, color=0x000, font=FONT_MONT_14, parent=None)
        info = label0 = M5Label((str(sad())), x=15, y=38, color=0x000, font=FONT_MONT_14, parent=None)
        suggestiongiven = 0
        sadrun = True
      if newface == True and mute == False:
        for i in range(3):
          rgb.setColorAll(0xffffff)
          power.setVibrationEnable(True)
          time.sleep(1)
          rgb.setColorAll(0x000000)
          power.setVibrationEnable(False)
          time.sleep(0.5)
          newface = False

    newtime = (rtc.datetime()[6]) + ((rtc.datetime()[5]) * 60) + ((rtc.datetime()[4]) * 60 * 60) # Set the newtime to the time
    
    image0.set_hidden(True) # Alternate between image0 and image1
    image1.set_hidden(False)
    time.sleep(2)
    image0.set_hidden(False)
    image1.set_hidden(True)
    time.sleep(2)
    
    if (btnA.isPressed()) == True: # If the A button is pressed go to page 4
      image0.set_hidden(True)
      image1.set_hidden(True)
      page4()
    elif (btnB.isPressed()) == True: # If the B button is pressed set mute to True and show the red on the RGB lights
      if mute == True:
        mute = False
        rgb.setColorAll(0x000000)
      elif mute == False:
        mute = True
        rgb.setColorAll(0xf00000)
    elif (btnC.isPressed()) == True: # If the C button is pressed to the the first page
      
      image0.set_hidden(True)
      image1.set_hidden(True)
      page1()
      
    
      suggestiongiven = suggestiongiven + 1
  
  image0.set_hidden(True) # Hide both of the images
  image1.set_hidden(True)


def page1(): # To-do list page
  global title, mute # Setup the global variables

  # To-Do List Items
  recordbtn1 = M5Btn(text='Record', x=110, y=50, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  label0 = M5Label('To Do List', x=78, y=8, color=0x000, font=FONT_MONT_34, parent=None)
  item1 = M5Label('Item 1', x=45, y=58, color=0x000, font=FONT_MONT_14, parent=None)
  item2 = M5Label('Item 2', x=45, y=98, color=0x000, font=FONT_MONT_14, parent=None)
  item3 = M5Label('Item 3', x=45, y=138, color=0x000, font=FONT_MONT_14, parent=None)
  item4 = M5Label('Item 4', x=45, y=178, color=0x000, font=FONT_MONT_14, parent=None)
  recordbtn2 = M5Btn(text='Record', x=110, y=90, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  recordbtn3 = M5Btn(text='Record', x=110, y=130, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  recordbtn4 = M5Btn(text='Record', x=110, y=170, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  playbtn1 = M5Btn(text='Play', x=200, y=50, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  playbtn2 = M5Btn(text='Play', x=200, y=90, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  playbtn3 = M5Btn(text='Play', x=200, y=130, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
  playbtn4 = M5Btn(text='Play', x=200, y=170, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)

  def recordbtn1_pressed(): # If the recordbtn1 is pressed then record 5 seconds of audio
    mic.record2file(5, 'item1.wav') # Record 5 seconds from the microphone to item1.wav
    recordbtn1 = M5Btn(text='Recorded', x=110, y=50, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None) # Change the button text to Recorded
    pass
  recordbtn1.pressed(recordbtn1_pressed) # Call the recordbtn1_pressed function when recordbtn1 is pressed
  
  def recordbtn2_pressed():
    mic.record2file(5, 'item2.wav')
    recordbtn2 = M5Btn(text='Recorded', x=110, y=90, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
    pass
  recordbtn2.pressed(recordbtn2_pressed)
  
  def recordbtn3_pressed():
    mic.record2file(5, 'item3.wav')
    recordbtn3 = M5Btn(text='Recorded', x=110, y=130, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
    pass
  recordbtn3.pressed(recordbtn3_pressed)
  
  def recordbtn4_pressed():
    mic.record2file(5, 'item4.wav')
    recordbtn4 = M5Btn(text='Recorded', x=110, y=170, w=80, h=30, bg_c=0xc3bf40, text_c=0x000000, font=FONT_MONT_14, parent=None)
    pass
  recordbtn4.pressed(recordbtn4_pressed)
  
  def playbtn1_pressed(): # If the playbtn1 is pressed then play the item1.wav through the speakers on the device
    speaker.playWAV('item1.wav', rate=44100)
    pass
  playbtn1.pressed(playbtn1_pressed)
  
  def playbtn2_pressed():
    speaker.playWAV('item2.wav', rate=44100)
    pass
  playbtn2.pressed(playbtn2_pressed)
  
  def playbtn3_pressed():
    speaker.playWAV('item3.wav', rate=44100)
    pass
  playbtn3.pressed(playbtn3_pressed)
  
  def playbtn4_pressed():
    speaker.playWAV('item4.wav', rate=44100)
    pass
  playbtn4.pressed(playbtn4_pressed)

  time.sleep(3) # Wait for 3 seconds
  while True: # Repeat forever
    recordbtn1.pressed(recordbtn1_pressed) # Constantly check if any of the buttons have been pressed and
    recordbtn2.pressed(recordbtn2_pressed) # if so call the respective functions
    recordbtn3.pressed(recordbtn3_pressed)
    recordbtn4.pressed(recordbtn4_pressed)
    playbtn1.pressed(playbtn1_pressed)
    playbtn2.pressed(playbtn2_pressed)
    playbtn3.pressed(playbtn3_pressed)
    playbtn4.pressed(playbtn4_pressed)
    
    if (btnA.isPressed()) == True: # If the A button is pressed then go back to the homescreen
      # Hide To-Do list items
      label0.set_hidden(True)
      item1.set_hidden(True)
      item2.set_hidden(True)
      item3.set_hidden(True)
      item4.set_hidden(True)
      recordbtn1.set_hidden(True)
      recordbtn2.set_hidden(True)
      recordbtn3.set_hidden(True)
      recordbtn4.set_hidden(True)
      playbtn1.set_hidden(True)
      playbtn2.set_hidden(True)
      playbtn3.set_hidden(True)
      playbtn4.set_hidden(True)
  	 
      homescreen()
    elif (btnB.isPressed()) == True: # If the B button is pressed then mute everything
      if mute == True:
        mute = False
        rgb.setColorAll(0x000000)
      elif mute == False:
        mute = True
        rgb.setColorAll(0xf00000)
    elif (btnC.isPressed()) == True: # If the C button is pressed then go to page 2
      # Hide To-Do list items
      label0.set_hidden(True)
      item1.set_hidden(True)
      item2.set_hidden(True)
      item3.set_hidden(True)
      item4.set_hidden(True)
      recordbtn1.set_hidden(True)
      recordbtn2.set_hidden(True)
      recordbtn3.set_hidden(True)
      recordbtn4.set_hidden(True)
      playbtn1.set_hidden(True)
      playbtn2.set_hidden(True)
      playbtn3.set_hidden(True)
      playbtn4.set_hidden(True)

      page2()


def fun_core2_msg_(topic_data): # Run this function when any data is received from core2/msg in AWS IOT core  
    global image0, image1, infotitle, info, stop # Setup the global variables

    if 'coffee' == (str(topic_data)): # If the message received is coffee then
      stop = False # Stop the eyes from being animated
      coffee() # Call the coffee function

    elif (str(topic_data)) == 'game': # If the message received is game then
      stop = False # Stop the eyes from being animated
      game() # Call the game function
    elif 'joke' == (str(topic_data)): # If the message received is joke then
      stop = False # Stop the eyes from being animated
      jokeaws() # Call the joke function
    elif 'walk' == (str(topic_data)): # If the message received is walk then
      stop = False # Stop the eyes from being animated
      walk() # Call the walk function


# Setup the aws communication and subscribe to the core2/msg to receive messages
aws = AWS(things_name='ENV_TEST', host='a1l7aj7j9zpprt-ats.iot.us-west-2.amazonaws.com', port=8883, keepalive=60, cert_file_path="/flash/res/certificate.pem.crt", private_key_path="/flash/res/private.pem.key")
aws.subscribe(str('core2/msg'), fun_core2_msg_)
aws.start()

homescreen() # Run the homepage function
