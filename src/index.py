from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from bs4 import BeautifulSoup
import urllib.parse
app = FastAPI()

@app.get("/novel/{novel}")
def get_novel_info(novel):
    response = requests.get(f"https://raw.githubusercontent.com/luanwillianzh/Novel-Reader-Data/refs/heads/main/{novel}/info.json", verify=False).json()
    return response

@app.get("/novel/{novel}/chapter/{chapter}")
def get_chapter(novel, chapter):
  try:
    response = requests.get(f"https://raw.githubusercontent.com/luanwillianzh/Novel-Reader-Data/refs/heads/main/{novel}/{chapter}.html", verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.select_one("h1").text.strip().replace("\n", " ")
    try:
      subtitle = soup.select_one("h2").text.strip().replace("\n", " ")
    except:
      subtitle = ""
    content = str(soup.select_one("div.epcontent.entry-content"))
    return {"title": title, "subtitle": subtitle, "content": content}
  except Exception as e:
    return {"error": e}

@app.get("/search/{text}")
def search(text):
    resp = requests.get("https://raw.githubusercontent.com/luanwillianzh/Novel-Reader-Data/refs/heads/main/info.json").json()
    try:
      return {"sucesso": true, "resultado": [ {"nome": resp[novel_id]["nome"], "url": novel_id, "cover": resp[novel_id]["cover"]} for novel_id in resp if urllib.parse.unquote_plus(text.lower()) in str(resp[novel_id]).lower() ]}
    except:
      return {"sucesso": true, "resultado": [ {"nome": resp[novel_id]["nome"], "url": novel_id, "cover": resp[novel_id]["cover"]} for novel_id in resp ]}
