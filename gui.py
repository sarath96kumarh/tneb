from tkinter import ttk
import tkinter as tk
from tkinter import *
import pandas as pd
import operator
from functools import reduce

#\n spliter
def split_line(val):
    if '\n' in val:
       
        source_valsplit=val.split('\n')
        return [source_valsplit[0].strip(),source_valsplit[1].strip()]
        
        
def float_line(val):
    if '\n' in val:
       
        source_valsplit=val.split('\n')
        return [float(source_valsplit[0].strip()),float(source_valsplit[1].strip())]

#data
data=pd.read_excel('./data/data.xlsx')

#list_option
def option_list(col_name):
      #print(data[col_name])
      list_option=data[col_name].dropna().to_list()
      return list_option

#Load capacity w.r.t Speed rating data

load_capacity=['110 kmph','100 kmph','90 kmph','80 kmph','70 kmph','60 kmph','50 kmph']
cap_per=[0,0,2,4,7,10,12]
load_zip=zip(load_capacity,cap_per)
load_dict=dict(load_zip)

# Dict object creation
front_axle_dict_1=''
front_axle_dict_2=''
rear_axle_dict_1=''
rear_axle_dict_2=''
psher_axel_dict=''
single_tire_model_dict=''
dual_tire_model_dict=''

def dict_creation(model,capacity,type=0):
      global front_axle_dict_1,front_axle_dict_2,rear_axle_dict_1,rear_axle_dict_2,psher_axel_dict,single_tire_model_dict,dual_tire_model_dict
      if model!='Tires_Model':
            without_null_model=option_list(model)
            model_split=reduce(operator.concat,     [split_line(ss) if '\n' in ss else [ss] for ss in without_null_model])
            without_null_cap=option_list(capacity)
            cap_split=reduce(operator.concat,     [float_line(str(ss)) if '\n' in str(ss) else [ss] for ss in without_null_cap])
            zip_iterator = zip(model_split, cap_split)
            dcit_value = dict(zip_iterator)
            if model =='Front Axle 1_Model':
                  front_axle_dict_1=dcit_value
            if model =='Front Axle 2_Model':
                  front_axle_dict_2=dcit_value
            if model=='Rear Axle 1_Model':
                  rear_axle_dict_1=dcit_value
            if model=='Rear Axle 2_Model':
                  rear_axle_dict_2=dcit_value
            if model=='Pusher axle':
                  psher_axel_dict=dcit_value
      if model=='Tires_Model' and type=='single':
            #tire_model_dict={}
            without_null_model=option_list(model)
            model_split=reduce(operator.concat,     [split_line(ss) if '\n' in ss else [ss] for ss in without_null_model])
            #without_null_Tires_Single_dual=option_list('Tires_Single/Dual')
            #single_dual_split=reduce(operator.concat,     [split_line(ss) if '\n' in ss else [ss] for ss in without_null_Tires_Single_dual])
            without_null_cap=option_list(capacity)
            cap_split=reduce(operator.concat,     [float_line(str(ss)) if '\n' in str(ss) else [ss] for ss in without_null_cap])
            #for ss in range(0,len(model_split)):
            #     tire_model_dict[model_split[ss]][single_dual_split[ss]]=cap_split[ss]
            zip_iterator = zip(model_split, cap_split)
            single_tire_model_dict = dict(zip_iterator)
            
      if model=='Tires_Model' and type=='dual':
            #tire_model_dict={}
            without_null_model=option_list(model)
            model_split=reduce(operator.concat,     [split_line(ss) if '\n' in ss else [ss] for ss in without_null_model])
            #without_null_Tires_Single_dual=option_list('Tires_Single/Dual')
            #single_dual_split=reduce(operator.concat,     [split_line(ss) if '\n' in ss else [ss] for ss in without_null_Tires_Single_dual])
            without_null_cap=option_list(capacity)
            cap_split=reduce(operator.concat,     [float_line(str(ss)) if '\n' in str(ss) else [ss] for ss in without_null_cap])
            #for ss in range(0,len(model_split)):
            #     tire_model_dict[model_split[ss]][single_dual_split[ss]]=cap_split[ss]
            zip_iterator = zip(model_split, cap_split)
            dual_tire_model_dict = dict(zip_iterator)
      






#application

root = Tk(className='Python Examples - Window Color')
# set window size
root.geometry("1430x720")

#set window color
root.configure(bg='#1f283e')


#text box
T = Text(root, height = 5, width = 22,background='#F3EAF4',font = ("Lato,sans-serif", 14,'bold'))
T.tag_configure("tag_name", justify='center')
T.place(x=1120,y=135)


#variable
single_tire_c=0



front_cho=''
rear_cho=''
first_cal_fin_res=0
sec_cal_fin_res=0
back=0
front=0
per=0


#configuration


def display_selected(choice):
    choice = text2.get()
    print(choice)

border_color = Frame(root, background="#B3A394")
ttk.Label(border_color, text = "Configuration   ",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
border_color.place(x=40,y=50)





border_color_2_dd = Frame(root, background="#B3A394")
text2 = StringVar()
  
# Set the value you wish to see by default
text2.set("Choose here")
  
# Create options from the Option Menu
w = OptionMenu(border_color_2_dd, text2, *option_list('Configuration'),command=display_selected)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
border_color_2_dd.place(x=40,y=80)


#ENgine_model

border_color_3 = Frame(root, background="#B3A394")
ttk.Label(border_color_3, text = "Engine_Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
border_color_3.place(x=40,y=150)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text3.get()
     print(choice)

border_color_3_dd = Frame(root, background="#B3A394")
text3 = StringVar()
  
# Set the value you wish to see by default
text3.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(border_color_3_dd, text3, *option_list('Engine_Model'),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
border_color_3_dd.place(x=40,y=180)






#Transmission_Gear Box Model

boder_color_6 = Frame(root, background="#B3A394")
ttk.Label(boder_color_6, text = "Transmission_Gear",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
boder_color_6.place(x=40,y=250)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text6.get()
     print(choice)

boder_color_6_dd = Frame(root, background="#B3A394")
text6 = StringVar()
  
# Set the value you wish to see by default
text6.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(boder_color_6_dd, text6, *option_list('Transmission_Gear Box Model'),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
boder_color_6_dd.place(x=40,y=280)








#Front Axle 1_Model


def display_selected(choice):
    dict_creation('Front Axle 1_Model','Front Axle 1_Technical capacity (Kg)')
    choice = text2.get()
    front_axel_withstand_cap=front_axle_dict_1[choice]
    

border_color = Frame(root, background="#B3A394")
ttk.Label(border_color, text = "Front Axle 1_Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
border_color.place(x=300,y=50)





border_color_2_dd = Frame(root, background="#B3A394")
text2 = StringVar()
  
# Set the value you wish to see by default
text2.set("Choose here")
  
# Create options from the Option Menu
w = OptionMenu(border_color_2_dd, text2, *option_list('Front Axle 1_Model'),command=display_selected)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
border_color_2_dd.place(x=300,y=80)


#Front Axle 2_Model

border_color_3 = Frame(root, background="#B3A394")
ttk.Label(border_color_3, text = "Front Axle 2_Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
border_color_3.place(x=300,y=150)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text3.get()
     print(choice)

border_color_3_dd = Frame(root, background="#B3A394")
text3 = StringVar()
  
# Set the value you wish to see by default
text3.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(border_color_3_dd, text3, *option_list('Front Axle 2_Model'),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
border_color_3_dd.place(x=300,y=180)



# Rear Axle 1_Model

boder_color_4 = Frame(root, background="#B3A394")
ttk.Label(boder_color_4, text = "Rear Axle 1_Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
boder_color_4.place(x=300,y=250)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text4.get()
     print(choice)

boder_color_4_dd = Frame(root, background="#B3A394")
text4 = StringVar()
  
# Set the value you wish to see by default
text4.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(boder_color_4_dd, text4, *option_list('Rear Axle 1_Model'),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
boder_color_4_dd.place(x=300,y=280)



#Rear Axle 2_Model

boder_color_5 = Frame(root, background="#B3A394")
ttk.Label(boder_color_5, text = "Rear Axle 2_Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
boder_color_5.place(x=300,y=350)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text5.get()
     print(choice)

boder_color_5_dd = Frame(root, background="#B3A394")
text5 = StringVar()
  
# Set the value you wish to see by default
text5.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(boder_color_5_dd, text5, *option_list('Rear Axle 2_Model'),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
boder_color_5_dd.place(x=300,y=380)



#Pusher axle

boder_color_6 = Frame(root, background="#B3A394")
ttk.Label(boder_color_6, text = "Pusher axle",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
boder_color_6.place(x=300,y=450)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text6.get()
     print(choice)

boder_color_6_dd = Frame(root, background="#B3A394")
text6 = StringVar()
  
# Set the value you wish to see by default
text6.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(boder_color_6_dd, text6, *option_list('Pusher axle'),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
boder_color_6_dd.place(x=300,y=480)



#single trie model

boder_color_7 = Frame(root, background="#B3A394")
ttk.Label(boder_color_7, text = "Single Tires Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
boder_color_7.place(x=560,y=50)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text7.get()
     print(choice)

boder_color_7_dd = Frame(root, background="#B3A394")
text7 = StringVar()
  
# Set the value you wish to see by default
text7.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(boder_color_7_dd, text7, *set(option_list('Tires_Model')),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
boder_color_7_dd.place(x=560,y=80)


#dual tires
boder_color_8 = Frame(root, background="#B3A394")
ttk.Label(boder_color_8, text = "Dual Tires Model",background='#F87060',foreground="white",
          font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
boder_color_8.place(x=560,y=150)



def display_selected_3(choice):
     global front_cho, first_cal_fin_res
     choice = text8.get()
     print(choice)

boder_color_8_dd = Frame(root, background="#B3A394")
text8 = StringVar()
  
# Set the value you wish to see by default
text8.set("Choose here")


# Create options from the Option Menu
w = OptionMenu(boder_color_8_dd, text8, *set(option_list('Tires_Model')),command=display_selected_3)
  
# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")
  
# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")
  
# Display the Options Menu
w.grid( padx = 1, pady = 1)
boder_color_8_dd.place(x=560,y=180)



#Load capacity w.r.t Speed rating

def display_selected_9(choice_rs):
     global  sec_cal_fin_res,per
     choice_rs = text9.get()

border_color_9 = Frame(root, background="#B3A394")
ttk.Label(border_color_9, text = "w.r.t Speed rating",background='#F87060',foreground="white",
        font = ("Lato,sans-serif", 14,'bold')).grid( padx = 1, pady = 1)
border_color_9.place(x=560,y=250)



border_color_9_dd = Frame(root, background="#B3A394")
text9 = StringVar()

# Set the value you wish to see by default
text9.set("Choose here")

# Create options from the Option Menu
w = OptionMenu(border_color_9_dd, text9, *load_capacity,command=display_selected_9)

# Se the background color of Options Menu to green
w.config(font = ("Lato,sans-serif", 14,'bold'),bg="#CFD7C7", fg="black")

# Set the background color of Displayed Options to Red
w["menu"].config(bg="#CFD7C7")

# Display the Options Menu
w.grid( padx = 1, pady = 1)
border_color_9_dd.place(x=560,y=280)



root.mainloop() 