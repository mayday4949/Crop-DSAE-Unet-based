import requests

response = requests.post("https://hello-simpleai-chatgpt-detector-single.hf.space/run/predict_zh", json={
  "data": [
    "对于OpenAI大力出奇迹的工作，自然每个人都有自己的看点。我自己最欣赏的地方是ChatGPT如何解决 “AI校正(Alignment)“这个问题。这个问题也是我们课题组这两年在探索的学术问题之一。",
]}).json()

data = response["data"]
print(data)

