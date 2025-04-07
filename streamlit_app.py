# streamlit run .\my_translator.py

from deep_translator import GoogleTranslator
import streamlit as st
import os
import openai
from openai import OpenAI

openai_api_key = st.secrets['openai']['API_KEY']
client = OpenAI(api_key  = openai_api_key)

message_history_user = []
message_history_gpt  = []

# 앱 제목
st.title('Google Translator with GPT-4o')

# URL 입력 받기
tran_source_text = st.text_area('번역을 하고 싶은 문장을 입력해 주세요.')

language_labels = {
    '영어 (English)': 'en',
    '한국어 (Korean)': 'ko',
    '일본어 (Japanese)': 'ja',
    '중국어 (chinese)': 'zh'
}

language_type = {
    '가볍게': '격식없이 그냥 지나가듯이 가벼운 대화하는 느낌으로 해줘 ',
    '격식있게': '격식있는 대화나 문장에 쓰일 수 있는 느낌으로 해줘',
    '친근하게': '친구에게 이야기 하듯이 편안한 느낌으로 해줘',
    '공식적으로': '공식적인 문서나 이메일에 쓰일 수 있는 느낌으로 해줘',
}

label_list = list(language_labels.keys())

# key 인자를 사용해 고유 식별자 부여
selected_label1 = st.selectbox('원본 언어를 선택해 주세요.', list(language_labels.keys()), key="source_lang")

# selected_label1에서 선택된 언어를 제외한 나머지 언어들로 필터링
filtered_labels = [label for label in label_list if label != selected_label1]

selected_label2 = st.selectbox('번역할 언어를 선택해 주세요.', filtered_labels, key="target_lang")

selected_label3 = st.selectbox('윤문할 타입을 선택해 주세요.', list(language_type.keys()), key="type_lang")

source_lang = language_labels[selected_label1]
target_lang = language_labels[selected_label2]
type_lang = language_type[selected_label3]

# URL 단축 버튼
if st.button('번역하기'):
    if tran_source_text:
        
        try:
            # GoogleTranslator 사용하여 번역
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(tran_source_text)
            message_history_user.append({"role":"user", "content":translated_text})

            # gpt-4o 모델을 사용해서 챗봇 메시지를 생성하여 윤문하기
            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system", 
                "content":f"너는 영어를 윤문하는 윤문전문가야. {type_lang}."},
                *message_history_user, 
                *message_history_gpt
            ],
            temperature=0,
            max_tokens=500
            )
            message_history_gpt.append({"role":"assistant", "content":response.choices[0].message.content})
            st.success(f"원문장 : {tran_source_text}\n\n"+
                       f"번역문장 : {translated_text}\n\n"+
                       f"윤문문장({selected_label3}) : {response.choices[0].message.content}")
        except Exception as e:
            st.error(f'Error: {e}')
        pass
    else:
        st.error('Please enter a URL to shorten')
