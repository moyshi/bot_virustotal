import Tele
import check_files_virostotal
import yaml
from time import sleep
import threading
import io
import os


CHAT_USERBOT = ''


d_update = {}
d_lang = {1111: {'he': 'אנא המתן הקובץ שלך בהורדה כעת',
                 'en': 'Please wait for your file to download now',
                 'it': 'Attendi il download del tuo file'},
          1112: {'he': 'מידע נוסף',
                 'en': 'More information',
                 'it': 'More information'},
          1113: {'he': 'הקובץ זוהה על ידי {} מתוך {}',
                 'en': 'The file was identified by {} out of {}',
                 'it': 'Il file è stato identificato da {} su {}'},
          1115: {'he': 'שלום {} אתה יכול לשלוח לבוט קבצים והוא יבדוק אותם מול וירוס טוטל עם מעל 70 אנטי וירוסים שונים',
                 'en': 'Hello {}, you can send the files to a bot and it will check against Total '
                                               'Virus with over 70 different antiviruses',
                 'it': 'Ciao {},'
                      ' puoi inviare i file al bot e lo controllerà Total Virus con oltre 70 antivirus diversi'},
          1114: {'he': 'לצפייה ברשימת הזיהויים',
                 'en': 'To view the list of identifications',
                 'it': 'To view the list of identifications'},
          1116: {'he': 'הקובץ נבדק כעת נסה שוב בעוד כחצי דקה',
                 'en': 'The file is being reviewed now, please try again in half a minute',
                 'it': 'The file is being reviewed now, please try again in half a minute'},
          1117: {'he': 'הקובץ ששלחת גדול מידי ניתן לשלוח קבצים עד 200MB',
                 'en': 'The file you submitted is too large, files up to 200MB can be uploaded',
                 'it': 'The file you submitted is too large, files up to 200MB can be uploaded'},
          1118: {'he': 'הגעת למגבלת השימוש החודשית שלך',
                 'en': 'usage limit exceeded',
                 'it': 'usage limit exceeded'},
          1119: {'he': 'לשינוי שפה /language',
                 'en': 'For language change /language',
                 'it': 'For language change /language'}
          }


class users:
    def __init__(self, user_id, lang):
        self.user_id = user_id
        self.time2 = 0
        self.lang = lang
        self.admin = 0
        self.useing = 0
        self.files_u = 0
        self.f_s = 0

    def file(self, update):
        if update['document']['file_unique_id'] in d_files:
            self.check_file(True, d_files[update['document']['file_unique_id']], str(update['message_id']))
        else:
            d_update[str(str(update['message_id'])) + str(self.user_id)] = update
            Tele.send_message(chat_id=self.user_id, text=d_lang[1111][self.lang])
            Tele.send_document(chat_id=CHAT_USERBOT,
                               caption=str(update['from']['id']) + ' ' + str(update['message_id']),
                               file=update['document']['file_id'])

    def check_file(self, m, file, message_id):
        update = d_update[str(message_id) + str(self.user_id)]
        if m is True:
            answer = check_files_virostotal.hash3(file)
        else:
            adds, answer = check_files_virostotal.hash2(file)
            if adds:
                self.f_s += os.path.getsize(file)
                os.remove(file)
            d_files[update['document']['file_unique_id']] = answer['resource']
            save()
        update.reply(text=answer['permalink'],
                     reply_markup=Tele.InlineKeyboard([[{d_lang[1112][self.lang]: '2'}]]))
        del d_update[str(message_id) + str(self.user_id)]

    def info(self, update):
        if self.time2 == 0:
            answer = check_files_virostotal.hash3(d_files[update['message']
                                                                ['reply_to_message']
                                                                ['document']
                                                                ['file_unique_id']])
            if answer['response_code'] == 1:
                Tele.edit_message_text(chat_id=self.user_id,
                                       message_id=update['message']['message_id'],
                                       text=answer['permalink'] + '*' + ' \n' + ' \n' + d_lang[1113][self.lang].format(
                                           answer['positives'], answer['total']) + '*',
                                       reply_markup=Tele.InlineKeyboard([[{
                                           d_lang[1114][self.lang]: '1'}]]))
            elif answer['response_code'] == -2:
                Tele.edit_message_text(chat_id=self.user_id,
                                       message_id=update['message']['message_id'],
                                       text=update['message']['text'].split()[
                                                0] + '\n' + ' \n' + '*' + d_lang[1116][self.lang] + '*',
                                       reply_markup=Tele.InlineKeyboard([[{d_lang[1112][self.lang]: '2'}]]))
            threading.Thread(target=self.time1).start()

    def all_info(self, update):
        s_z1 = ''
        s_z2 = ''
        answer = check_files_virostotal.hash3(
            d_files[update['message']['reply_to_message']['document']['file_unique_id']], True)
        for x in answer['scans']:
            if answer['scans'][x]['detected'] is True:
                if '_' in answer['scans'][x]['result']:
                    result = answer['scans'][x]['result']
                    result = result.replace("_", "\_")
                else:
                    result = answer['scans'][x]['result']
                s_z1 += ('⛔' + '*' + x + '*' + '   ' + result + '\n')
            if answer['scans'][x]['detected'] is False:
                s_z2 += ('✅' + '*' + x + '*' + '   ' + 'Undetected' + '\n')
        s_z = s_z1 + s_z2
        Tele.edit_message_text(chat_id=self.user_id,
                               message_id=update['message']['message_id'],
                               text=answer['permalink'] + '*' + ' \n' + ' \n' + d_lang[1113][self.lang].format(
                                   answer['positives'], answer['total']) + '*' + '\n' + ' \n' + s_z)

    def time1(self):
        self.time2 += 1
        sleep(30)
        self.time2 -= 1


with open('clients.yml', 'r') as date_b:
    contain = yaml.load(date_b)
if contain is None:
    d_users = {}
else:
    d_users = contain

with open('files.yml', 'r') as date_b:
    contain = yaml.load(date_b)
if contain is None:
    d_files = {}
else:
    d_files = contain


def save():
    with io.open('files.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(d_files, outfile)


def save2():
    with io.open('clients.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(d_users, outfile)
