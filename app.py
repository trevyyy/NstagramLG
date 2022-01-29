import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

prompt = """A system that writes Instagram ads for digital prints.
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
Input: chocolate, espresso martini
Output: %s"""


def get_response(text):

    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt % text,
        temperature=1,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    out = response['choices'][0]['text'].split('\n')
    out = [i.strip('0123456789. ') for i in out]

    return out


st.title('Instagram post generator')
input_text = st.text_input('Input')
if input_text:
    output = get_response(input_text)
    for o in output:
        st.write(o)
