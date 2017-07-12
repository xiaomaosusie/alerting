from jinja2 import Template
from subprocess import getoutput
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailAlert(object):
	"""docstring for EmailAlert"""
	def __init__(self, filename, mjmltemplate, acct, content _json):
		self.filename = filename
		self.mjmltemplate = mjmltemplate
		self.acct = content_json['accountname']
		self.message1 = content_json['message1']
		self.message2 = content_json['message2']
		self.message3 = content_json['message3']
		self.theader = content_json['theader']
		self.tvalue = content_json['tvalue']

	def render_template(self):
		#Render the mjml doc
		with open(self.mjmltemplate, 'r') as mjmltemp:
		  # load the template as a string and create a jinja2 template
			template = Template(mjmltemp.read())
			rendered = template.render(accts=self.acct, msg1 = self.message1, msg2 = self.message2, msg3 = self.message3, hdrs=self.theader, rows=self.tvalue)
			
			with open(self.filename+".mjml", "w") as text_file:
				text_file.write(rendered)

		# use mjml binary to render the html
		getoutput("/Users/ssu/node_modules/.bin/mjml -r %s -o %s" % \
			(self.filename+".mjml", self.filename+".html"))

	def send_email(self, subject, me, you):
		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = me
		msg['To'] = ", ".join(you)

		# Create the body of the message (a plain-text and an HTML version).
		#text = "Hi!\nHow are you?\nThis is testing"

		with open(self.filename+".html", 'r') as htmlfile:
			html = htmlfile.read()

		# Record the MIME types of both parts - text/plain and text/html.
		#part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		#msg.attach(part1)
		msg.attach(part2)

		# Send the message via local SMTP server.
		s = smtplib.SMTP('mail.pulse.prod')
		# sendmail function takes 3 arguments: sender's address, recipient's address
		# and message to send - here it is sent as one string.
		s.sendmail(me, you, msg.as_string())
		s.quit()