#@mrlokaman 
#@lntechnical
from pyrogram import Client, filters
import requests 
import json 
import os

DB_URL = os.environ.get("DB_URL","")
TOKEN = os.environ.get("TOKEN", "")
API_ID = int(os.environ.get("API_ID",12345))
API_HASH = os.environ.get("API_HASH","")
BITLY_TOKEN = os.environ.get("BITLY_TOKEN","")

mongo = pymongo.MongoClient(DB_URL)
db = mongo["bitly"]
dbcol = db["USER"]

headers = {
    'Authorization': BITLY_TOKEN,
    'Content-Type': 'application/json',
}


app = Client("bitlybot" ,bot_token = TOKEN ,api_id = API_ID ,api_hash = API_HASH )

@app.on_message(filters.private & filters.command(['start']))
async def start(client,message):
  user_id = int(message.chat.id)
  user_det = {"_id":user_id}
  try:
  	dbcol.insert_one(user_det)
  	await message.reply_text(f"Hello {message .from_user.first_name}\nhello i am bit.ly short link genrator\n made with love by @mrlokaman ", reply_to_message_id = message.message_id,reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Support 🇮🇳" ,url="https://t.me/lntechnical") ],[InlineKeyboardButton("Subscribe 🧐", url="https://youtube.com/c/LNtechnical") ]   ]  ) )
  except:
          await message.reply_text(f"Hello {message .from_user.first_name}\nhello i am bit.ly short link genrator\n made with love by @mrlokaman ", reply_to_message_id = message.message_id,reply_markup=InlineKeyboardMarkup(
            [ [ InlineKeyboardButton("Support 🇮🇳" ,url="https://t.me/lntechnical") ],[InlineKeyboardButton("Subscribe 🧐", url="https://youtube.com/c/LNtechnical") ]   ]  ) )
           
  
@app.on_message(filters.private & filters.regex("http|https"))
async def Bitly(client,message):
  URL = message.text
  DOMAIN = "bit.ly"
  value  = {'long_url': URL , 'domain': DOMAIN}
  data = json.dumps(value)
  try:
    r = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers,data = data )
    result = r.json()
    link = result["link"]
    await message.reply_text(f"```{link}```", reply_to_message_id= message.message_id)
  except Exception as e :
    await message.reply_text(e)
    
app.run()
    
