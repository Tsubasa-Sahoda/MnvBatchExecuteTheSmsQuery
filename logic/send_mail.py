######################################################################
#  send_email.py
#
#＜処理内容＞
#  emailを送信する
#
#＜修正履歴＞
#  2021.01.12 : 新規作成
#  2021.01.27 : sendEmail_Report追加
#  2021.02.04 : 関数の型アノテーション追記
#  2021.10.18 : 異常終了Email送信を実装
#
######################################################################
import os
import smtplib
import common.config as conf
from email import message as mailmsg
from datetime import datetime as dt

# 環境変数
# conf = conf.config()

# テスト
conf = conf.testConfig()

CUR_DIR = os.getcwd()

EMAIL_TEMP_END = CUR_DIR + conf.SUCESS_MAIL_TEMP
EMAIL_TEMP_ABEND = CUR_DIR + conf.ERROR_MAIL_TEMP
EMAIL = conf.mail
TEST_FLAG = conf.flag['test']


##---------------------------------------------------------
## テンプレートを読む
##---------------------------------------------------------
def getMailTemplate(tempfile: str, procName: str, logMsg: str):

	dt_now = dt.now()

	with open(tempfile, 'r', encoding='cp932') as f:
		datalist = f.readlines()

	head = "".join(datalist[1])
	body = "".join(datalist[4:])

	head = head.replace('%処理名%', procName).replace('%処理日付%', dt_now.strftime('%Y年%m月%d日'))
	body = body.replace('%処理名%', procName).replace('%詳細ログ%', logMsg)

	if TEST_FLAG:
		head = '[テスト]' + head

	return head, body


##---------------------------------------------------------
## 処理終了Emailを送信する
##---------------------------------------------------------
def sendEmail_ProcEnd(procName: str, logMsg: str) -> None:

	subject, content = getMailTemplate(EMAIL_TEMP_END, procName, logMsg)

	msg = mailmsg.EmailMessage()
	msg.set_content(content);
	msg['Subject'] = subject
	msg['From'] = EMAIL['from']
	msg['To'] = EMAIL['to']

	with smtplib.SMTP(EMAIL['host'], EMAIL['port'], timeout=EMAIL['timeout']) as server:
		server.send_message(msg)


##---------------------------------------------------------
## 異常終了Emailを送信する
##---------------------------------------------------------
def sendEmail_ProcAbend(procName: str, logMsg: str) -> None:

	subject, content = getMailTemplate(EMAIL_TEMP_ABEND, procName, logMsg)

	msg = mailmsg.EmailMessage()
	msg.set_content(content);
	msg['Subject'] = subject
	msg['From'] = EMAIL['from']
	msg['To'] = EMAIL['to2']

	with smtplib.SMTP(EMAIL['host'], EMAIL['port'], timeout=EMAIL['timeout']) as server:
		server.send_message(msg)


##===================================================================
if __name__ == "__main__":

	procName = 'TestProc'
	logMsg = 'aaaaaaaaa'

	head, body = getMailTemplate(EMAIL_TEMP_END, "", logMsg)

	sendEmail_ProcEnd(procName, logMsg)

