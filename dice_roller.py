import numpy as np
import pandas as pd
import random 
import streamlit as st
from PIL import Image
from collections import Counter
import requests


st.title("Dice Roll Tracker")

#create session state to store rolls
if 'rolls' not in st.session_state:
    st.session_state['rolls']=[]

#store rolls for each dice to display picture
roll_1 = []
roll_2 = []

#define roll function
def roll():
    dice_1 = random.randint(1,6)
    dice_2 = random.randint(1,6)
    roll_1.append(dice_1)
    roll_2.append(dice_2)
    sum = dice_1 + dice_2
    st.session_state['rolls'].append(sum)
    return sum

#load in dice images
one = Image.open("Dice-Images/dice1.png")
two = Image.open("Dice-Images/dice2.png")
three = Image.open("Dice-Images/dice3.png")
four = Image.open("Dice-Images/dice4.png")
five = Image.open("Dice-Images/dice5.png")
six = Image.open("Dice-Images/dice6.png")

#create dictionary to key rolls with appropriate dice pic
img_dict = {1:one,
            2:two,
            3:three,
            4:four,
            5:five,
            6:six}

#add roll button
if st.button('Roll Dice'):
    st.header(roll())

#display pictures for each roll
width = 100

for i in range(1,7):
    for j in range(1,7):
        if [roll_1, roll_2] == [[i],[j]]:
            st.image([img_dict[i],img_dict[j]], width=width)

#show previous 5 rolls
pvs_rolls = st.session_state['rolls'][-5:]
pvs_rolls.reverse()
st.write('### Previous Rolls:')
st.markdown(pvs_rolls)

#obtain count for each dice combination
counts = Counter(st.session_state['rolls'])

#create lists of rolls and probabilities
rolls = list(range(2,13))

all_sums = []
for a in range(1,7):
    for b in range(1,7):
        sum = a+b
        all_sums.append(sum)
sums_count=Counter(all_sums)
sums_count_sorted = dict(sorted(sums_count.items()))
combo_count = list(sums_count_sorted.values())
percentages = [g/36 for g in combo_count]

#create list to store counts for each roll or 0 if not rolled yet
roll_count=[]
for k in rolls:
    if k in st.session_state['rolls']:
        roll_count.append(counts[k])
    else:
        roll_count.append(0)

#Combine lists into df
df = pd.DataFrame(
    {'Roll': rolls,
    'Fixed Probability': percentages,
    'Count': roll_count})
df.set_index('Roll', inplace = True)

#bar chart to display counts
st.write('### Roll count for each dice sum:')
st.bar_chart(df['Count'])

#define total rols and pct of total rolls
total_rolls = len(st.session_state['rolls'])
df['Pct of Total Rolls'] = df['Count']/total_rolls

st.write('### Total Number of Rolls:', total_rolls)

#calculate pct difference (Actual - Fixed)
df['Pct difference'] = df['Pct of Total Rolls'] - df['Fixed Probability']
st.write('### Probabilities and Counts for each Roll:')
st.dataframe(df)

#create button to clear history
if st.button("Clear History"):
    st.session_state['rolls'].clear(),
    st.experimental_rerun()


