import streamlit as st
import openai
import random

openai.api_key = st.secrets["OPENAI_API_KEY"]

_prompt = """A system that writes Instagram ads for digital prints.
###
Input: beige, minimalist, botanical, plant, leaf, abstract
Output:
1. Beige? Boring? Nope. 🍂
2. That botanical feeling
3. 🧑‍🎨 Your space deserves it
4. Let the leaves fall
5. When you need that piece that goes with anything
###
Input: Scandinavian, minimalist, burnt orange, Beige, Abstract, Nordic, sunset
Output:
1. Cheers 🍊
2. This is the one
3. Let's warm things up a bit
4. 🥵 Warm up your space
5. Feel the love
###
Input: landscape, reflection, purple, gold, mountain
Output:
1. Let's head to the mountains 🚠
2. Time to reflect
3. Snuggle up and take a tea break 😌
4. From our space to yours
5. Designed to be cozy
###
Input: %s
Output:"""

orange = """Input: burnt orange
Output:
1. Cheers 🍊
2. We call this a glow-up 😎
3. Let's warm things up a bit 🔥
4. Warm things up 🥵
5. Feel the love 🧡
###"""

green = """Input: green
Output:
1. A fresh start ♻️
2. Clear the room 🌿
3. Need some air? 🌳
4. Upping the O2 🧪
5. Something new is on the way 🪴
###"""

blue = """Input: blue
Output:
1. Wash out the old 🌀
2. A rhapsody in blue 🔵
3. Feelin' blue in a good way 💙
4. Find your calm 😌
5. Blue who? 🔹
###"""

beige = """Input: beige
Output:
1. Beige? Boring? Nope. 🤩
2. Bring on the beige 🙌
3. Earth tones, anyone? 🌱
4. Nothing but neutrals 🤎
5. When you need something that goes with anything 🤝
###"""

use = """A system that writes about the emotions of colors.
###"""

io = """Input: %s
Output:"""

style = """Write a creative ad for digital artwork we have designed in the following style:

Style: %s"""


def get_color_text(text):

    prompt = use
    count = 0
    for i in [orange, green, blue]:
        if text not in i:
            prompt += i
            count += 1
    if count > 3:
        prompt += beige
    prompt += io

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt % text,
        temperature=1,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    out = response['choices'][0]['text'].split('\n')
    out = [i.strip('0123456789. ') for i in out]

    return out


def get_style_text(text):

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=style % text,
        temperature=1,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response['choices'][0]['text']


st.title('Instagram post generator')
colors = st.text_input('Colors (separate with commas)')
styles = st.text_input('Styles (separate with commas)')
if st.button('Go') and colors and styles:
    color_output = []
    style_output = []
    colors = [i.strip() for i in colors.split(',')]

    with st.spinner('Building ads...'):
        for c in colors:
            phrases = get_color_text(c)
            color_output += phrases
        for _ in range(len(color_output)):
            style_output += [get_style_text(styles)]

    final_texts = []
    for i, c in enumerate(color_output):
        final_texts += [f'{c} {style_output[i]}']
    random.shuffle(final_texts)
    for o in final_texts:
        st.write(o)
