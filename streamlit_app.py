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
st.title('✍️ 맞춤형 번역 스타일링')

# URL 입력 받기
tran_source_text = st.text_area('번역을 하고 싶은 문장을 입력해 주세요.')

language_labels = {
    '영어 (English)': 'en',
    '한국어 (Korean)': 'ko',
    '일본어 (Japanese)': 'ja',
    '중국어 (chinese)': 'zh'
}

language_type = {
    '가볍게 🪶': '일상적인 대화처럼 자연스럽고 부담 없이 표현해줘. 너무 딱딱하지 않게, 말하듯이 써줘.',
    '친근하게 😊': '친구에게 말하듯 부드럽고 편안한 어조로 윤문해줘. 간단하고 따뜻한 표현을 사용해.',
    '격식있게 🧑‍⚖️': '존중과 신뢰를 담아 말하는 느낌으로 정중하게 윤문해줘. 문장은 명확하고 단정하게.',
    '공식적으로 🏢': '비즈니스 문서나 이메일에 쓸 수 있을 정도로 격식을 갖추고 전문적으로 윤문해줘.',
    '마케팅 스타일 📣': '사용자가 이 문장을 읽고 구매나 행동을 하고 싶게 만드는, 매력적이고 감성적인 마케팅 문장으로 바꿔줘.',
    '블로그 스타일 ✍️': '스토리를 전달하듯이 감성적이고 부드럽게 윤문해줘. 자연스럽고 읽기 편한 흐름이 중요해.',
    '뉴스/보도용 📰': '중립적이고 객관적인 톤으로 정보 중심의 문장으로 윤문해줘. 간결하고 정확하게 써줘.',
    'SNS 스타일 💬': '짧고 임팩트 있게 표현해줘. 구어체, 해시태그, 이모지도 일부 포함해도 좋아. 트렌디한 느낌이면 더 좋아.'
}

example_sentences = {
    '가볍게 🪶': {
        "before": "오늘 발표 준비했어요.",
        "after": "오늘 발표 살짝 준비해봤어요~"
    },
    '친근하게 😊': {
        "before": "오늘 발표 준비했어요.",
        "after": "오늘 발표 준비했는데, 좀 떨리네요 😅"
    },
    '격식있게 🧑‍⚖️': {
        "before": "오늘 발표 준비했어요.",
        "after": "오늘 발표를 위해 필요한 내용을 충실히 준비했습니다."
    },
    '공식적으로 🏢': {
        "before": "오늘 발표 준비했어요.",
        "after": "발표를 위한 자료를 완료하였으며, 관련 내용을 검토하였습니다."
    },
    '마케팅 스타일 📣': {
        "before": "오늘 발표 준비했어요.",
        "after": "오늘, 모든 시선을 사로잡을 발표를 준비했습니다! 기대하셔도 좋아요."
    },
    '블로그 스타일 ✍️': {
        "before": "오늘 발표 준비했어요.",
        "after": "오늘은 발표가 있는 날이에요. 열심히 준비한 만큼 잘 전달되길 바라요 :)"
    },
    '뉴스/보도용 📰': {
        "before": "오늘 발표 준비했어요.",
        "after": "해당 발표는 오늘 중으로 완료될 예정이며, 주요 내용은 다음과 같다."
    },
    'SNS 스타일 💬': {
        "before": "오늘 발표 준비했어요.",
        "after": "드디어 오늘 발표 🎤 준비 완료! #프레젠테이션 #오늘의미션"
    },
}

label_list = list(language_labels.keys())

# 기본값을 '한국어 (Korean)'으로 설정
default_index = label_list.index('한국어 (Korean)')

# key 인자를 사용해 고유 식별자 부여
selected_label1 = st.selectbox('원본 언어를 선택해 주세요.', list(language_labels.keys()), index=default_index, key="source_lang")

# selected_label1에서 선택된 언어를 제외한 나머지 언어들로 필터링
filtered_labels = [label for label in label_list if label != selected_label1]

selected_label2 = st.selectbox('번역할 언어를 선택해 주세요.', filtered_labels, key="target_lang")

# 윤문 스타일 선택
selected_label3 = st.selectbox(
    '윤문할 스타일을 선택해 주세요.',
    list(language_type.keys()),
    key="type_lang",
    help="원하는 톤에 따라 문장 스타일이 달라집니다. SNS, 블로그, 마케팅, 공식 등 상황에 맞게 선택해보세요."
)

# 선택한 스타일의 예시 문장 표시
selected_example = example_sentences.get(selected_label3)
if selected_example:
    with st.expander("💡 선택한 스타일의 예시 보기"):
        st.markdown(f"**예시 원문:** {selected_example['before']}")
        st.markdown(f"**윤문 결과:** {selected_example['after']}")

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
            
            result_text = (
                f"원문장:\n{tran_source_text}\n\n"
                f"번역문장 ({selected_label2}):\n{translated_text}\n\n"
                f"윤문문장 ({selected_label3}):\n{response.choices[0].message.content}"
            )

            st.success(result_text)

            st.download_button(
                label="📥 결과를 TXT로 저장",
                data=result_text,
                file_name="translation_result.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f'Error: {e}')
        pass
    else:
        st.error('Error')
