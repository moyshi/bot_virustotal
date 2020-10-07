import Tele
import cliant_class
import io
import yaml
import threading
import traceback
from pyrogram import Client, Filters


CHAT_ADMIN = ''
CHAT_USERBOT = ''
TOKAEN = ''


def save():
    with io.open('clients.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(cliant_class.d_users, outfile)


def new_uzer(update):
    if 'language_code' in update['from'] and update['from']['language_code'] in cliant_class.d_lang[1115]:
        Tele.send_message(chat_id=update['chat']['id'],
                          text=cliant_class.d_lang[1115][update['from']['language_code']].format(update['from']['first_name'], update['from']['first_name']))
        Tele.send_message(chat_id=update['chat']['id'],
                          text=cliant_class.d_lang[1119][update['from']['language_code']])
        if str(update['chat']['id']) not in cliant_class.d_users:
            cliant_class.d_users[str(update['chat']['id'])] = cliant_class.users(update['chat']['id'], update['from']['language_code'])
    else:
        Tele.send_message(chat_id=update['chat']['id'],
                          text=cliant_class.d_lang[1115]['en'].format(update['from']['first_name'], update['from']['first_name']))
        Tele.send_message(chat_id=update['chat']['id'],
                          text=cliant_class.d_lang[1119]['en'])
        if str(update['chat']['id']) not in cliant_class.d_users:
            cliant_class.d_users[str(update['chat']['id'])] = cliant_class.users(update['chat']['id'], 'en')
    Tele.send_message(chat_id=CHAT_ADMIN,
                      text=len(cliant_class.d_users))
    save()


def bot():
    @Tele.bot('text')
    def message(update):
        try:
            if update['text'] == '/start' and update['chat']['type'] == 'private':
                new_uzer(update)
            else:
                if update['chat']['type'] == 'private' and str(update['chat']['id']) not in cliant_class.d_users:
                    new_uzer(update)
                if str(update['chat']['id']) in cliant_class.d_users:
                    if update['text'] == '/language':
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text='/en - English\n/it - Italian\n/he - עברית')
                    elif update['text'] == '🇱🇷English🇱🇷' or update['text'] == '/en':
                        cliant_class.d_users[str(update['chat']['id'])].lang = 'en'
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text='English')
                    elif update['text'] == '/it':
                        cliant_class.d_users[str(update['chat']['id'])].lang = 'it'
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text='Italian')
                    elif update['text'] == '🇮🇱עברית🇮🇱' or update['text'] == '/he':
                        cliant_class.d_users[str(update['chat']['id'])].lang = 'he'
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text='עברית')
                    elif cliant_class.d_users[str(update['chat']['id'])].admin == 1 and update['text'].split()[0] == '*#*#1':
                        for u in cliant_class.d_users:
                            cliant_class.d_users[u].useing += int(update['text'].split()[1])
                    elif cliant_class.d_users[str(update['chat']['id'])].admin == 1 and update['text'].split()[0] == '*#*#2':
                        for u in cliant_class.d_users:
                            cliant_class.d_users[u].useing = int(update['text'].split()[1])
                    elif cliant_class.d_users[str(update['chat']['id'])].admin == 1 and update['text'].split()[0] == '*#*#3':
                        cliant_class.d_users[update['text'].split()[1]] += update['text'].split()[2]
                    elif cliant_class.d_users[str(update['chat']['id'])].admin == 1 and cliant_class.d_users[str(update['chat']['id'])].send_h:
                        if update['text'] == '⛔cancel⛔':
                            cliant_class.d_users[str(update['chat']['id'])].send_h = False
                            Tele.send_message(chat_id=update['chat']['id'],
                                              text='בוטל',
                                              reply_markup=Tele.reply_keyboard_remove())
                        else:
                            pi_n = 0
                            for u in cliant_class.d_users:
                                if cliant_class.d_users[u].lang == 'he':
                                    mse1 = Tele.send_message(chat_id=u,
                                                      text=update['text'])
                                    if mse1 is None:
                                        del cliant_class.d_users[u]
                                    else:
                                        pi_n += 1
                            Tele.send_message(chat_id=update['chat']['id'],
                                              text='עברית ' + str(pi_n))
                            cliant_class.d_users[str(update['chat']['id'])].send_h = False
                    elif cliant_class.d_users[str(update['chat']['id'])].admin == 1 and cliant_class.d_users[str(update['chat']['id'])].send_e:
                        if update['text'] == '⛔cancel⛔':
                            cliant_class.d_users[str(update['chat']['id'])].send_e = False
                            Tele.send_message(chat_id=update['chat']['id'],
                                              text='בוטל',
                                              reply_markup=Tele.reply_keyboard_remove())
                        else:
                            pi_n = 0
                            for u in cliant_class.d_users:
                                if cliant_class.d_users[u].lang == 'en' or cliant_class.d_users[u].lang == 'it':
                                    mse1 = Tele.send_message(chat_id=u,
                                                      text=update['text'])
                                    if mse1 is None:
                                        del cliant_class.d_users[u]
                                    else:
                                        pi_n += 1
                            Tele.send_message(chat_id=update['chat']['id'],
                                              text='אנגלית ' + str(pi_n))
                            cliant_class.d_users[str(update['chat']['id'])].send_e = False
                    elif update['text'] == 'שליחת הודעה לחברי הבוט עברית' and cliant_class.d_users[str(update['chat']['id'])].admin == 1:
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text='אנא שלח את ההודעה שלך לביטול לחץ על ⛔cancel⛔',
                                          reply_markup=Tele.Keyboard([['⛔cancel⛔']]))
                        cliant_class.d_users[str(update['chat']['id'])].send_h = True
                    elif update['text'] == 'שליחת הודעה לחברי הבוט אנגלית' and cliant_class.d_users[str(update['chat']['id'])].admin == 1:
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text='אנא שלח את ההודעה שלך לביטול לחץ על ⛔cancel⛔',
                                          reply_markup=Tele.Keyboard([['⛔cancel⛔']]))
                        cliant_class.d_users[str(update['chat']['id'])].send_e = True
        except Exception as error:
            print(error)
            print(traceback.format_exc())

    @Tele.bot('document')
    def message(update):
        try:
            if str(update['chat']['id']) not in cliant_class.d_users and update['chat']['type'] == 'private':
                new_uzer(update)
            if str(update['chat']['id']) in cliant_class.d_users:
                if update['document']['file_size'] < 200000000:
                    if cliant_class.d_users[str(update['chat']['id'])].useing >= update['document']['file_size']:
                        cliant_class.d_users[str(update['chat']['id'])].file(update)
                        cliant_class.d_users[str(update['chat']['id'])].useing -= update['document']['file_size']
                        cliant_class.d_users[str(update['chat']['id'])].files_u += 1
                        save()
                    else:
                        Tele.send_message(chat_id=update['chat']['id'],
                                          text=cliant_class.d_lang[1118][
                                              cliant_class.d_users[str(update['chat']['id'])].lang])
                else:
                    Tele.send_message(chat_id=update['chat']['id'],
                                      text=cliant_class.d_lang[1117][cliant_class.d_users[str(update['chat']['id'])].lang])
        except Exception as error:
            print(error)
            print(traceback.format_exc())

    @Tele.bot('data')
    def message(update):
        try:
            if str(update['message']['chat']['id']) not in cliant_class.d_users and update['chat']['type'] == 'private':
                new_uzer(update)
            if str(update['message']['chat']['id']) in cliant_class.d_users:
                if update['data'] == '1':
                    cliant_class.d_users[str(update['message']['chat']['id'])].all_info(update)
                elif update['data'] == '2':
                    cliant_class.d_users[str(update['message']['chat']['id'])].info(update)
        except Exception as error:
            print(error)
            print(traceback.format_exc())

    Tele.account(TOKAEN)
    Tele.bot_run(multi=True)


threading.Thread(target=bot).start()
app = Client("my_account")


@app.on_message(Filters.document & Filters.chat(CHAT_USERBOT))
def my_handler(client, message):
    try:
        file_pate = client.download_media(message['document']['file_id'],
                                          file_ref=message['document']['file_ref'],
                                          block=True,
                                          file_name='./downloads/' + message['document']['file_name'])
        user_id, message_id = message['caption'].split()
        cliant_class.d_users[user_id].check_file(False, file_pate, message_id)
    except Exception as error:
        print(error)
        print(traceback.format_exc())


app.run()
