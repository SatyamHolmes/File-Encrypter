import tkinter as tk
from tkinter import filedialog
import gzip as gz
import shutil
import pyAesCrypt
from os import stat,remove
import re

class Application(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.filelabel=tk.Label(self,text="File:  ")
		self.filelabel.grid(column=0,row=0)
		self.filebox=tk.Entry(self,bd=0,width=50)
		self.filebox.grid(column=1,row=0)
		self.browse=tk.Button(self,text="Browse",command=self.browsefile)
		self.browse.grid(column=2,row=0,padx=10)
		self.passlabel=tk.Label(self,text="Password:  ")
		self.passlabel.grid(column=0,row=1)
		self.passbox=tk.Entry(self,bd=0,width=50)
		self.passbox.grid(column=1,row=1,pady=10)
		self.verifypasslabel=tk.Label(self,text="Verify Password:  ")
		self.verifypasslabel.grid(column=0,row=2)
		self.verifypassbox=tk.Entry(self,bd=0,width=50)
		self.verifypassbox.grid(column=1,row=2,pady=10)
		self.savelabel=tk.Label(self,text="save:  ")
		self.savelabel.grid(column=0,row=3)
		self.savebox=tk.Entry(self,bd=0,width=50)
		self.savebox.grid(column=1,row=3)
		self.savebrowse=tk.Button(self,text="Browse",command=self.browsedest)
		self.savebrowse.grid(column=2,row=3,padx=10)
		self.encryptbutton=tk.Button(self,text="Encrypt",command=self.encrypt)
		self.encryptbutton.grid(column=0,row=4,pady=10)
		self.err=tk.StringVar()   #contains the infromative messages for user 
		self.errmsg=tk.Label(self,textvariable=self.err)
		self.errmsg.grid(column=1,row=4)
		self.decryptbutton=tk.Button(self,text="Decrypt",command=self.decrypt)
		self.decryptbutton.grid(column=2,row=4,pady=10)

	def browsefile(self):
		file=filedialog.askopenfilename(initialdir='/')
		self.filebox.insert(0,file)

	def browsedest(self):
		save=filedialog.askdirectory(initialdir='/')
		self.savebox.insert(0,save)	

	def encrypt(self):
		try:
			if(self.filebox.get()!="" and re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",self.passbox.get()) and self.passbox.get()==self.verifypassbox.get()):
				filename=self.filebox.get().split('/')[-1]
				with open(self.filebox.get(), 'rb') as f_in, gz.open(filename+'.gz', 'wb') as f_out:
					shutil.copyfileobj(f_in,f_out)
		
				with open(filename+".gz",'rb') as fIn, open(self.savebox.get()+"/"+filename+".aes", "wb") as fOut:
					pyAesCrypt.encryptStream(fIn, fOut, self.passbox.get(),64*1024)
				remove(filename+".gz")
				self.err.set("Encryption Successfull")
			else:
				if(self.filebox.get()==""):
					self.err.set("File not specified")
				elif(not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",self.passbox.get())):	
					self.err.set("Password must contain atleast 1 capital letter, 1 small letter, 1 number and 8 digits long")
				else:
					self.err.set("Passwords do not match")
				#self.errmsg.grid(column=1,row=4)
		except FileNotFoundError:
			self.err.set("Invalid File or save location")
		finally:
			self.filebox.delete(0,tk.END)
			self.passbox.delete(0,tk.END)
			self.verifypassbox.delete(0,tk.END)
			self.savebox.delete(0,tk.END)

	def decrypt(self):
		filename=self.filebox.get().split('/')[-1]
		try:
			if(self.filebox.get()!=""  and filename.split('.')[-1]=='aes' and re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",self.passbox.get()) and self.passbox.get()==self.verifypassbox.get()):
				encFileSize = stat(self.filebox.get()).st_size
				with open(self.filebox.get(), "rb") as fIn, open(filename+".gz", "wb") as fOut:
					pyAesCrypt.decryptStream(fIn, fOut,self.passbox.get(),64*1024, encFileSize)
		
				with gz.open(filename+".gz", 'rb') as f_in, open(self.savebox.get()+"/"+filename.split('.')[0]+"."+filename.split('.')[1], 'wb') as f_out:
						shutil.copyfileobj(f_in,f_out)
				remove(filename+".gz")
				self.err.set("Decryption Successfull")
			else:
				if(self.filebox.get()==""):
					self.err.set("File not specified")
				elif(not filename.split('.')[-1]=='aes'):
					self.err.set("Invalid encrypted file")
				elif(not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",self.passbox.get())):	
					self.err.set("Password must contain atleast 1 capital letter, 1 small letter, 1 number and 8 digits long")
				else:
					self.err.set("Passwords do not match")
		except ValueError:
			self.err.set("Invalid password")
		except FileNotFoundError:
			self.err.set("Invalid File or save location")
		finally:
			self.filebox.delete(0,tk.END)
			self.passbox.delete(0,tk.END)
			self.verifypassbox.delete(0,tk.END)
			self.savebox.delete(0,tk.END)
		
root=tk.Tk()
app=Application(master=root)
app.mainloop()