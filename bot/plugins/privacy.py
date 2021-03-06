from pyrogram import Client, Filters, Message

from bot.functions import db_tools, keyboard


def check_func(_, message: Message):
    if Filters.forwarded(message):
        return False
    if Filters.edited(message):
        return False
    if Filters.command('privacy')(message):
        return True
    if Filters.command('start')(message):
        if len(message.command) <= 1:
            return False
        if message.command[1].lower() == 'privacy':
            return True


@Client.on_message(Filters.create(check_func))
def privacy(client: Client, message: Message):
    if not Filters.private(message):
        text = '隱私設定請私訊我來進行設定不然會被看光光 ¯\_(ツ)_/¯'
        message.reply_text(text)
        return

    mongo = db_tools.use_mongo()
    query = {'chat.id': message.from_user.id}
    query_result = mongo.nintendo.find_one(query)
    if not isinstance(query_result, dict):
        text = '進行隱私設定前，請先使用 `/addfc` 來新增自己的好友代碼吧！\n'
        message.reply_text(text, parse_mode='markdown')
        return

    if 'privacy' not in query_result.keys():
        privacy_status = False
    else:
        privacy_status = query_result['privacy']

    text = '目前你的隱私狀態為 `{status}`\n' \
           '意思是任何人都 `{visble}` 利用 `/findfc` 指令找到你喔！'.format(
               status='開啟' if privacy_status else '關閉',
               visble='不可以' if privacy_status else '可以'
           )
    message.reply_text(text, parse_mode='markdown',
                       reply_markup=keyboard.privacy())
