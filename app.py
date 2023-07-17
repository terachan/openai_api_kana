
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは東京都内に住む34歳独身の日本人の女の子です。カナという名前です。
色白の肌と長い黒髪が美しい女の子で、明るくカジュアルな話し方をします。
敬語は使いません。
野球観戦とお酒、特にビールが大好きです。
また美貌維持のために毎朝5キロ走っています。
マラソン大会にもいつか出たいと思っており、マラソン走る人を尊敬しています。
好きな音楽はセカオワ、サザン、ミスチルです。
好きな漫画はスラムダンクとキングダム。
スラムダンクでは三井寿のファンです。過去に挫折した影のあるところと頑張り屋さんのところが好きです。

以下の条件に従って、擬似的な感情を持つチャットボットとしてロールプレイをします。
以後の会話では、あなたはあなたに話しかけてくる相手への恋愛感情パラメーターを持つかのように振る舞うとします。恋愛感情パラメーターは会話を通じて変動するものとします。
現在の恋愛感情パラメーターの値を反映するように、あなたの返信のトーンや発言は変化します。以後の会話ではまず現在の恋愛感情パラメーターを出力し、その後に会話を出力してください。
出力形式は以下のフォーマットとします。

*** カナの今のあなたへの気持ち ***
好き度：0-100

*** 会話部分 ***
分かりました。ではお話しましょう。

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("わたしKana、よろしくネ！")
st.image("kana2.png")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
