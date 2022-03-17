from pymongo import MongoClient
from c import *

myclient = MongoClient(DB_URI)
db = myclient['mydb']
apiDB = db['api']


async def info_taker(chat):
    data = apiDB.find_one({"chat": chat})
    if data is None:
        return False, False
    print(data)
    api = data['api']

    stype = int(data["type"])
    return api, stype

from f import *
start_message = """<b>
Hey There, {}
🔀 I Can Convert Link To ShortLink
💬 Send Me Any Message With Links
🔗 I Will Shorten All Links In It 
🔂 Convert to <a href="https://shorturllink.in/member/tools/bookmarklet">ShortUrlLink</a> & <a href="https://playdisk.xyz/member/tools/bookmarklet">PlayDisk</a>

©️Powered By @A2z_tech
</b>"""
start_button = [[Button.url("Join Channel ♥️", "t.me/A2z_tech"), Button.inline("About Bot 🤖", "abt")],
                [Button.inline("Connect To Shortner 🔗", 'api')]]

api_message = """
<b>Which Shortner Do u Want to Connect To:</b>
"""
api_button = [[Button.url("Shorturllink.in", "https://shorturllink.in/member/tools/bookmarklet")],
              [Button.url("Playdisk.xyz", "https://playdisk.xyz/member/tools/bookmarklet")]]

about_text = """<b>



🤖 Name :  Shorurllink Link Convertor

🔠 Language : Python3
📚 Library     : Telethon
🧑🏻‍💻 Developer : @Ziko_0000

©️Powered By @A2z_tech
</b>"""
async def api_logger(chat, api, stype):
    data = apiDB.find_one({"chat": chat})

    if data is None:
        apiDB.insert_one({"chat": chat, "api": api, "type": stype})
    else:
        apiDB.delete_one(data)
        apiDB.insert_one({"chat": chat, "api": api, "type": stype})
