import streamlit as st
import openai
import random
import re

openai.api_key = st.secrets["OPENAI_API_KEY"]

color = """Convert text into emojis:

orange: 🍊🧡🟠

green: 🌿💚🧩

blue: 💙🌀🔵

yellow: 💛⚠️🍋    

red: 🔥💋🌶

%s:"""

_color = """Convert text into emojis:

Add some zing to your walls with this eye-catching graphic print. The bold purples and playful design will make a statement in any room: 👾
Feel closer to the ocean with our new water ripple print 🌊 Perfect for your home, office, or any other space that could use a splash of colour: 💙
This fun, minimalist rainbow hearts print would make the perfect Valentines Day gift for your loved one! The fun and colourful illustration is perfect for adding some happiness to your walls: 🌈
%s:"""

style = """Write a creative ad for an art print we have designed in the following style:

Style: %s"""


def get_color_text(text):

    # if text in color:
    #     start = color.index(text)
    #     end = start + len(text) + 6
    #     text_to_replace = color[start:end]
    #     prompt = color.replace(text_to_replace, '') % text
    # else:
    #     prompt = color % text

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=color % text.strip('.!?'),
        temperature=1,
        max_tokens=15,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    out = response['choices'][0]['text'].split('\n')
    out = [x for x in out if x]

    return out[0]


def get_style_text(text):

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=style % text.replace(' | ', ', '),
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    out = response['choices'][0]['text'].strip('\n')
    if '\n' in out:
        out = out.split('\n')
        out.sort(key=len)
        out = out[-1]

    out = out.replace('art print', 'print')
    out = out.replace('an print', 'a print')
    out = out.replace('Our', 'This')
    out = re.sub('\bour\b', 'this', out)

    return out


st.title('Instagram post generator')
colors = st.text_input('Colors', help='Separate each style with commas e.g. "green, brown, beige"')
styles = st.text_input('Styles', help='Separate each style with pipes, e.g. "boho | minimalist | Scandi"')
styles = f'{styles}, {colors}'

if 'final_texts' not in st.session_state:
    st.session_state['final_texts'] = []

if st.button('Go') and colors and styles:
    final_texts = []

    # GPT-3
    with st.spinner('Building ads...'):
        # emojis = set()
        # colors = [c.strip() for c in colors.split(',')]
        # for c in colors:
        #     color_output = get_color_text(c)
        #     for e in color_output:
        #         emojis |= set(e)
        for _ in range(5):
            final_texts += [get_style_text(styles)]
        # emojis = [e for e in emojis if len(e.strip()) > 0]
        #
        # final_texts = []
        # k = 5 if len(emojis) > 5 else len(emojis)
        # colors_to_use = random.sample(emojis, k=k)
        # if color_output:
        # for output in style_output:
        #     final_texts += [f'{output} {get_color_text(output)}']
            # try:
            #     final_texts += [f'{output} {colors_to_use[i]}']
            # except IndexError:
            #     final_texts += [output]

    random.shuffle(final_texts)
    st.session_state['final_texts'] = final_texts

for i, o in enumerate(st.session_state['final_texts']):
    st.write('-' * 10)
    st.write(o)
