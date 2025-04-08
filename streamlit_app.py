from deep_translator import GoogleTranslator
import streamlit as st
import openai
import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI

st.set_page_config(
    page_title="맞춤형 번역 스타일링",
    layout="wide"  # <- 페이지 너비를 넓게 설정!
)

# OpenAI API 설정
openai_api_key = st.secrets['openai']['API_KEY']
client = OpenAI(api_key=openai_api_key)

# 세션 상태 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 언어 및 스타일 설정
kst_now = datetime.datetime.now(ZoneInfo("Asia/Seoul"))
timestamp = kst_now.strftime("%Y%m%d_%H%M%S")

language_labels = {
    '영어 (English)': 'en',
    '한국어 (Korean)': 'ko',
    '일본어 (Japanese)': 'ja',
    '중국어 (chinese)': 'zh-CN'
}

language_type = {
    '가볍게 🧒🏻': '일상적인 대화처럼 자연스럽고 부담 없이 표현해줘. 너무 딱딱하지 않게, 말하듯이 써줘.',
    '친근하게 😊': '친구에게 말하듯 부드럽고 편안한 어조로 윤문해줘. 간단하고 따뜻한 표현을 사용해.',
    '격식있게 🧑\u200d⚖️': '존중과 신뢰를 담아 말하는 느낌으로 정중하게 윤문해줘. 문장은 명확하고 단정하게.',
    '공식적으로 🏢': '비즈니스 문서나 이메일에 쓸 수 있을 정도로 격식을 갖추고 전문적으로 윤문해줘.',
    '마케팅 스타일 📣': '사용자가 이 문장을 읽고 구매나 행동을 하고 싶게 만드는, 매력적이고 감성적인 마케팅 문장으로 바꿔줘.',
    '블로그 스타일 ✍️': '스토리를 전달하듯이 감성적이고 부드럽게 윤문해줘. 자연스럽고 읽기 편한 흐름이 중요해.',
    '뉴스/보도용 📰': '중립적이고 객관적인 톤으로 정보 중심의 문장으로 윤문해줘. 간결하고 정확하게 써줘.',
    'SNS 스타일 💬': '짧고 임팩트 있게 표현해줘. 구어체, 해시태그, 이모지도 일부 포함해도 좋아. 트렌디한 느낌이면 더 좋아.'
}

example_sentences = {
    '가볍게 🧒🏻': {"before": "오늘 발표 준비했어요.", "after": "오늘 발표 살짝 준비해봤어요~"},
    '친근하게 😊': {"before": "오늘 발표 준비했어요.", "after": "오늘 발표 준비했는데, 좀 떨리네요 😅"},
    '격식있게 🧑\u200d⚖️': {"before": "오늘 발표 준비했어요.", "after": "오늘 발표를 위해 필요한 내용을 충실히 준비했습니다."},
    '공식적으로 🏢': {"before": "오늘 발표 준비했어요.", "after": "발표를 위한 자료를 완료하였으며, 관련 내용을 검토하였습니다."},
    '마케팅 스타일 📣': {"before": "오늘 발표 준비했어요.", "after": "오늘, 모든 시선을 사로잡을 발표를 준비했습니다! 기대하셔도 좋아요."},
    '블로그 스타일 ✍️': {"before": "오늘 발표 준비했어요.", "after": "오늘은 발표가 있는 날이에요. 열심히 준비한 만큼 잘 전달되길 바라요 :)"},
    '뉴스/보도용 📰': {"before": "오늘 발표 준비했어요.", "after": "해당 발표는 오늘 중으로 완료될 예정이며, 주요 내용은 다음과 같다."},
    'SNS 스타일 💬': {"before": "오늘 발표 준비했어요.", "after": "드디어 오늘 발표 🎤 준비 완료! #프레젠테이션 #오늘의미션"}
}

# 언어 선택 설정
label_list = list(language_labels.keys())
default_index = label_list.index('한국어 (Korean)')

# 화면 2분할
col1, col2 = st.columns([6, 4])

with col1:
    st.title('✍️ 맞춤형 번역 스타일링')

    tran_source_text = st.text_area('번역을 하고 싶은 문장을 입력해 주세요.')

    selected_label1 = st.selectbox('원본 언어를 선택해 주세요.', list(language_labels.keys()), index=default_index, key="source_lang")
    filtered_labels = [label for label in label_list if label != selected_label1]
    selected_label2 = st.selectbox('번역할 언어를 선택해 주세요.', filtered_labels, key="target_lang")

    selected_label3 = st.selectbox(
        '윤문할 스타일을 선택해 주세요.',
        list(language_type.keys()),
        key="type_lang",
        help="원하는 톤에 따라 문장 스타일이 달라집니다. SNS, 블로그, 마케팅, 공식 등 상황에 맞게 선택해보세요."
    )

    # 예시 표시
    selected_example = example_sentences.get(selected_label3)
    if selected_example:
        with st.expander(f"💡 선택한 스타일({selected_label3})의 예시 보기"):
            st.markdown(f"**예시 원문:** {selected_example['before']}")
            st.markdown(f"**윤문 결과:** {selected_example['after']}")

    # 번역 버튼 클릭 시 동작
    if st.button('번역하기'):
        if tran_source_text:
            try:
                source_lang = language_labels[selected_label1]
                target_lang = language_labels[selected_label2]
                type_lang = language_type[selected_label3]

                translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(tran_source_text)
                message_history_user = [{"role": "user", "content": translated_text}]

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"너는 영어를 윤문하는 윤문전문가야. {type_lang}."},
                        *message_history_user
                    ],
                    temperature=0,
                    max_tokens=500
                )

                gptMessage = response.choices[0].message.content.strip()

                result_text = (
                    f"원문장:\n{tran_source_text}\n\n"
                    f"번역문장 ({selected_label2}):\n{translated_text}\n\n"
                    f"윤문문장 ({selected_label3}):\n{gptMessage}"
                )

                st.success(result_text)

                st.download_button(
                    label="📥 결과를 TXT로 저장",
                    data=result_text,
                    file_name=f"translation_result_{timestamp}.txt",
                    mime="text/plain"
                )

                st.session_state.history.append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "original": tran_source_text,
                    "translated": translated_text,
                    "polished": gptMessage,
                    "source_lang": selected_label1,
                    "target_lang": selected_label2,
                    "tone": selected_label3
                })

            except Exception as e:
                st.error(f'Error: {e}')
        else:
            st.error('번역할 문장을 입력해 주세요.')

with col2:
    st.title('🕘 히스토리(최근 5개까지)')

    if st.session_state.history:
        # for item in reversed(st.session_state.history):
        for item in sorted(st.session_state.history, key=lambda x: x['timestamp'], reverse=True)[:5]:
            st.markdown(
            f"**🕒 {item['timestamp']}**\n\n"
            f"- 원문: {item['original']}\n\n"
            f"- 번역({item['target_lang']}): {item['translated']}\n\n"
            f"- 윤문({item['tone']}): {item['polished']}\n\n"
            "---"
            )
    else:
        st.info("아직 번역된 내용이 없습니다.")
