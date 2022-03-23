from f import *

api_button = [[Button.url("du-link.in", "https://shorturllink.in/member/tools/bookmarklet")],
              [Button.url("Playdisk.xyz", "https://playdisk.xyz/member/tools/bookmarklet")]]

about_text = """<b>



🤖 Name :  Shorurllink Link Convertor

🔠 Language : Python3
📚 Library     : Telethon
🧑🏻‍💻 Developer : @Ziko_0000

©️Powered By @A2z_tech
</b>"""

start_message = """<b>
Hey There, {}
🔀 I Can Convert Link To ShortLink
💬 Send Me Any Message With Links
🔗 I Will Shorten All Links In It 
🔂 Convert to <a href="https://du-link.in/member/tools/bookmarklet">ShortUrlLink</a> & <a href="https://playdisk.xyz/member/tools/bookmarklet">PlayDisk</a>

©️Powered By @A2z_tech
</b>"""
start_button = [[Button.url("Join Channel ♥️", "t.me/A2z_tech"), Button.inline("About Bot 🤖", "abt")],
                [Button.inline("Connect To Shortner 🔗", 'api')]]
import re
from a import *
from b import *
from c import *
from d import *
from e import *

# INITIALISATION
client.parse_mode = 'html'
commands = ["/start", "/api", "/help", "/about", ""]
welcome_re = re.compile('/start|/help|/about', re.IGNORECASE)


# TRIGGERS
@client.on(events.NewMessage(pattern=welcome_re))
async def welcome(e):
    chat = await e.get_chat()
    if e.raw_text.lower() == "/start" or e.raw_text.lower() == "/help":
        await client.send_message(chat, start_message.format(chat.first_name), buttons=start_button, link_preview=False)
        return
    try:
        api_key = e.raw_text.split(' ')[1]

        try:
            tapi_key = api_key.split("-")[0]
            username = api_key.split("-")[1]
            api_key = tapi_key
            del tapi_key
        except IndexError:
            username = 'Unknown'
    except IndexError:
        return

    mess = await client.send_message(chat, "<B>Please Wait\nWe Are Checking Your Api</B>")
    stype, msg = await api_checker(api_key)
    print(stype)

    if stype:
        if stype == 1:
            domain = "Shorturllink.in"
        else:
            domain = "Playdisk.xyz"
        await api_logger(chat.id, api_key, stype)
        await client.edit_message(mess,
                                  f"<b>Account Connected Sucessfully ✅\n\nAccount: {username}\nShortner: {domain}</b>")
    else:
        await client.edit_message(mess, "<b>Invailid Api Token!!</b>")


@client.on(events.NewMessage())
async def handler(e):
    chat = await e.get_chat()
    if re.search("/api|/start ", e.raw_text):
        return
    s_api, shortner_type = await info_taker(chat.id)
    if not s_api:
        await client.send_message(chat, api_message, buttons=api_button)
        return
    caption = e.raw_text
    if caption.lower() in commands:
        return

    links = await link_extractor(caption)
    if not links:
        await client.send_message(chat, "<b>No Links Found In Message 😵</b>")
        return
    if len(links) > 12:
        await client.send_message(chat,"<b>Sorry Mate U Can Only Convert 12 Links Per Post,\nReason: To Avoid Server Overloading And DDOS</b>")
        return
    nlinks = await shortner(links, s_api, shortner_type)
    caption = await link_replacer(caption, links, nlinks)
    caption = await bolder(caption)

    mess = await client.send_message(chat, e.message)
    buttons = None
    if await username_check(caption):
        buttons = [Button.inline('Remove Usernames From Message', 'reusr')]

    await client.edit_message(mess, message=caption, buttons=buttons)


@client.on(events.NewMessage(pattern="/api"))
async def api(e):
    chat = await e.get_chat()
    try:
        api_key = e.raw_text.split(" ")[1]
    except IndexError:
        await client.send_message(chat, api_message, buttons=api_button)
        return

    mess = await client.send_message(chat, "<B>Please Wait\nWe Are Checking Your Api</B>")
    stype, msg = await api_checker(api_key)
    print(stype)

    if stype:
        if stype == 1:
            domain = "Shorturllink.in"
        else:
            domain = "Playdisk.xyz"
        await api_logger(chat.id, api_key, stype)
        await client.edit_message(mess, f"<b>Account Connected Sucessfully ✅\n\nShortner: {domain}</b>")
    else:
        await client.edit_message(mess, "<b>Invailid Api Token!!</b>")


# CALLBACK-QUERY
@client.on(events.CallbackQuery(pattern="reusr"))
async def rem_user(e):
    mess = await e.get_message()
    caption = mess.raw_text
    caption = await remove_username(caption, '')
    caption = await bolder(caption)
    await client.edit_message(mess, caption)


@client.on(events.CallbackQuery(pattern="api"))
async def rem_user(e):
    mess = await e.get_message()
    await client.edit_message(mess, api_message, buttons=api_button)


@client.on(events.CallbackQuery(pattern="abt"))
async def rem_user(e):
    mess = await e.get_message()
    await client.edit_message(mess, about_text, buttons=back_button)


@client.on(events.CallbackQuery(pattern="back"))
async def rem_user(e):
    mess = await e.get_message()
    chat = await e.get_chat()
    await client.edit_message(mess, start_message.format(chat.first_name), buttons=start_button, link_preview=False)


client.run_until_disconnected()
