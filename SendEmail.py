from tkinter import *
from tkinter import filedialog
import smtplib
from email.message import EmailMessage


#Global Variable
attachments = []

master = Tk()
master.title('Custom Python Email App')

#function

def attachFile():
	filename = filedialog.askopenfilename(initialdir='C:/',title='Select a file')
	attachments.append(filename)
	notif.config(fg='green', text='Attached ' + str(len(attachments)) + ' files')
	
	filename = attachments[0]
	filetype = filename.split('.')
	filetype = filetype[1]
	if filetype=="jpg" or filetype=="JPG" or filetype=="png" or filetype=="PNG":
		print("Image Detected")
	else:
		print("Document Detected")

def send():
	try:
		msg = EmailMessage()
		username = temp_username.get()
		password = temp_password.get()
		to = temp_receiver.get()
		subject = temp_subject.get()
		body = temp_body.get()
		msg['subject'] = subject
		msg['from'] = username
		msg['to'] = to
		msg.set_content(body)

		filename = attachments[0]
		filetype = filename.split('.')
		filetype = filetype[1]
		if filetype=="jpg" or filetype=="JPG" or filetype=="png" or filetype=="PNG":
			import imghdr
			with open(filename, 'rb') as f:
				file_data = f.read()
				image_type = imghdr.what(filename)
			msg.add_attachment(file_data, maintype='image', subtype=image_type, filename=f.name)

		else:
			with open(filename, 'rb') as f:
				file_data = f.read()
			msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=f.name)

		if username=="" or password=="" or to=="" or subject=="" or body=="":
			notif.config(text='All fields are required', fg="red")
			return
		else:
			finalMessage = 'Subject: {}\n\n{}'.format(subject, body)
			server = smtplib.SMTP('smtp.gmail.com',587)
			server.starttls()
			server.login(username, password)
			server.send_message(msg)
			notif.config(text='Email has been sent', fg='green')
	except error as e:
		print(error)
		notif.config(text="Error Sending email", fg="red")


def reset():
	usernameEntry.delete(0, 'end')
	passwordEntry.delete(0, 'end')
	receiverEntry.delete(0, 'end')
	subjectEntry.delete(0, 'end')
	bodyEntry.delete(0, 'end')



l1 = Label(master, text="Custom Email App", font=("Calibri",15))
l1.grid(row=0, sticky=N)
l2 = Label(master, text="Use the form below to send an email", font=("Calibri",11))
l2.grid(row=1, sticky=W, padx=5)
l3 = Label(master, text="Email", font=("Calibri",11))
l3.grid(row=2, sticky=W, padx=5)
l4 = Label(master, text="Password", font=("Calibri",11))
l4.grid(row=3, sticky=W, padx=5)
l5 = Label(master, text="To", font=("Calibri",11))
l5.grid(row=4, sticky=W, padx=5)
l6 = Label(master, text="Subject", font=("Calibri",11))
l6.grid(row=5, sticky=W, padx=5)
l7 = Label(master, text="Body", font=("Calibri",11))
l7.grid(row=6, sticky=W, padx=5)
notif = Label(master, text="", font=("Calibri",11))
notif.grid(row=7, sticky=S, padx=5)

#Storage
temp_username = StringVar()
temp_password = StringVar()
temp_receiver = StringVar()
temp_subject = StringVar()
temp_body = StringVar()

#Entries
usernameEntry = Entry(master, textvariable=temp_username)
usernameEntry.grid(row=2, column=0, )
passwordEntry = Entry(master, show="*" ,textvariable=temp_password)
passwordEntry.grid(row=3, column=0)
receiverEntry = Entry(master, textvariable=temp_receiver)
receiverEntry.grid(row=4, column=0)
subjectEntry = Entry(master, textvariable=temp_subject)
subjectEntry.grid(row=5, column=0)
bodyEntry = Entry(master, textvariable=temp_body)
bodyEntry.grid(row=6, column=0)

# b3 = Button(master, text="Attachment", command=attachFile)
# b3.grid(row=7, sticky=W)
b1 = Button(master, text="Send", command=send)
b1.grid(row=7, sticky=W, pady=15, padx=5)
b2 = Button(master, text="Reset", command=reset)
b2.grid(row=7, sticky=W, padx=45, pady=40)
b3 = Button(master, text="Attachment", command=attachFile)
b3.grid(row=7, sticky=W, padx=85, pady=40)


master.mainloop()