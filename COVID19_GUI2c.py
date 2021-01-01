import os
import xlsxwriter
import numpy as np
import pandas as pd
from tkinter import *
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from tkinter.filedialog import askdirectory


def input_window():
	
	def get_input():
		try:
			N = int(k_N.get())
			r0 = float(k_r0.get())
			rho = float(k_rh0.get())
			alpha = float(k_alpha.get())
			gamma = float(k_gamma.get())
		except ValueError:
			err1 = Tk()
			err1.title("Error Message")
			err1.geometry('300x100')
			label_e0 = Label(err1, text="Please enter Numbers only",width=30,font=("bold", 12), anchor=W)
			label_e0.pack()
			err1.mainloop()
		except:
			err2 = Tk()
			err2.title("Error Message")
			err2.geometry('300x100')
			label_e1 = Label(err1, text="Unexpected Error. Please contact Administrator",width=30,font=("bold", 12), anchor=W)
			label_e1.pack()
			err1.mainloop()
		
		ext = k_ext.get()
		st_date = entry_6.get()
		t_temp = k_t_max.get()
		
		if t_temp == "":
			t_max = 1000
		else:
			t_max = int(t_temp)
			
		k_parameters = N, r0, rho, alpha, gamma, t_max, ext, st_date
		win1.destroy()
		seir_model(k_parameters)
	
	win1 = Tk()
	win1.title("COVID-19")
	# win1.iconbitmap(r"covid_icon.ico")
	win1.geometry('600x600')

	k_N = StringVar()
	k_r0 = StringVar()
	k_rh0 = StringVar()
	k_alpha = StringVar()
	k_gamma = StringVar()
	k_t_max = StringVar()
	k_ext = StringVar()
	k_state = StringVar()
	
	label_0 = Label(win1, text="SEIR Model with Social Distancing",width=30,font=("bold", 20))
	label_0.place(x=20,y=30)

	# on change dropdown value
	def change_dropdown(*args):
		entry_1.delete(0, END)
		state = k_state.get()
		if state == 'Maharashtra':
			entry_1.insert(0, 122000000)
		elif state == 'Delhi':
			entry_1.insert(0, 30260000)
		elif state == 'UP':
			entry_1.insert(0, 235000000)
		elif state == 'Tamilnadu':
			entry_1.insert(0, 235000000)
		elif state == 'Bangalore':
			entry_1.insert(0, 235000000)
		else:
			entry_1.insert(0, 0)
		

	choices = {'Maharashtra','Delhi','UP','Tamilnadu','Bangalore','Others'}
	k_state.set('Maharashtra') # set the default option

	Label(win1, text="Select State", width=40, font=("bold", 10), anchor=E).place(x=30,y=95)
	popupMenu = OptionMenu(win1, k_state, *choices)
	popupMenu.place(x=400,y=90)
	k_state.trace('w', change_dropdown)

	label_1 = Label(win1, text="Total Population :", width=40, font=("bold", 10), anchor=E)
	label_1.place(x=30,y=130)
	entry_1 = Entry(win1,textvar=k_N)
	entry_1.insert(END, 122000000)
	entry_1.place(x=400,y=130)

	label_2 = Label(win1, text="r0 (Basic Reproductive Rate) :",width=40,font=("bold", 10), anchor=E)
	label_2.place(x=30,y=180)
	entry_2 = Entry(win1,textvar=k_r0)
	entry_2.place(x=400,y=180)

	label_3 = Label(win1, text="rh0 (Social distancing parameter ranging from 0-1) :",width=40,font=("bold", 10), anchor=E)
	label_3.place(x=30,y=220)
	entry_3 = Entry(win1,textvar=k_rh0)
	entry_3.place(x=400,y=230)
	label_3a = Label(win1, text="    ==> (0 = perfect quarantine, 1 = no distancing at all)", width=52, font=("bold", 8), anchor=E)
	label_3a.place(x=30,y=240)
	
	label_4 = Label(win1, text="Simulations (Number of time simulation to be run)",width=40,font=("bold", 10), anchor=E)
	label_4.place(x=30,y=280)
	entry_4 = Entry(win1,textvar=k_t_max)
	entry_4.insert(0, 1000)
	entry_4.place(x=400,y=280)
	
	label_al = Label(win1, text="alpha :",width=40,font=("bold", 10), anchor=E)
	label_al.place(x=30,y=330)
	entry_al = Entry(win1,textvar=k_alpha)
	entry_al.insert(0, 0.2)
	entry_al.place(x=400,y=330)

	label_gm = Label(win1, text="gamma :",width=40,font=("bold", 10), anchor=E)
	label_gm.place(x=30,y=380)
	entry_gm = Entry(win1,textvar=k_gamma)
	entry_gm.insert(0, 0.15)
	entry_gm.place(x=400,y=380)

	label_5 = Label(win1, text="Provide a Simulation name : ",width=40,font=("bold", 10), anchor=E)
	label_5.place(x=30,y=430)
	entry_5 = Entry(win1,textvar=k_ext)
	entry_5.place(x=400,y=430)
	
	label_6 = Label(win1, text="First COVID Confirmation Date : ",width=40,font=("bold", 10), anchor=E)
	label_6.place(x=30,y=480)
	entry_6 = DateEntry(win1, width=17, background='darkblue', foreground='white', borderwidth=2, year=2020)
	entry_6.place(x=400,y=480)
	
	Button(win1, text='Submit',width=20,bg='brown',fg='white',command=get_input).place(x=200,y=530)
	win1.mainloop()

def seir_model(k_parameters):

	def seir_model_with_soc_dist(init_vals, params, t):
			S_0, E_0, I_0, R_0 = init_vals
			S, E, I, R = [S_0], [E_0], [I_0], [R_0]
			alpha, beta, gamma, rho = params
			dt = t[1] - t[0]
			for _ in t[1:]:
					next_S = S[-1] - (rho*beta*S[-1]*I[-1])*dt
					next_E = E[-1] + (rho*beta*S[-1]*I[-1] - alpha*E[-1])*dt
					next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
					next_R = R[-1] + (gamma*I[-1])*dt
					S.append(next_S)
					E.append(next_E)
					I.append(next_I)
					R.append(next_R)
			return np.stack([S, E, I, R]).T    

	N, r0, rho, alpha, gamma, t_max, ext, st_date = k_parameters

	dt = .1
	t = np.linspace(0, t_max, int(t_max/dt) + 1)

	""" S_0, E_0, I_0, R_0 """
	init_vals = 1 - 1/N, 1/N, 0, 0 

	beta = r0 * gamma

	params = alpha, beta, gamma, rho

	results = seir_model_with_soc_dist(init_vals, params, t)

	t_80 = int(t_max * 10 / 80)

	# convert numpy to DF
	df = pd.DataFrame(results,columns=("S", "E", "I", "R"))

	# Calculate Average of every other 80 simulations 
	x=0
	y=80
	E_avg = []
	I_avg = []
	for i in range(t_80):
			next_E = df.E[x:y].mean()
			next_I = df.I[x:y].mean()
			E_avg.append(next_E)
			I_avg.append(next_I)
			x = y
			y = y + 80
			i = i + 1

	results_EI = pd.DataFrame(
			{'E': E_avg,
			 'I': I_avg,
			})

	results_avg = pd.DataFrame(columns=["Date","Infected","Hospitalized","ICU"])

	# Calculate Count of Infected and Exposed for the given Population and the expected Start Date
	results_avg["Date"] = pd.date_range(start=st_date, periods=len(results_EI), freq='D')
	# results_avg["Exposed"] = results_EI["E"].apply(lambda x: round(x * N))
	results_avg["Infected"] = results_EI["I"].apply(lambda x: round(x * N))
	results_avg["Hospitalized"] = results_avg["Infected"].apply(lambda x: round(x * 0.15))
	results_avg["ICU"] = results_avg["Infected"].apply(lambda x: round(x * 0.05))

	plt.figure(figsize = [8,4])
	# plt.plot(results_avg["Date"],results_avg["Exposed"])
	plt.plot(results_avg["Date"],results_avg["Infected"])
	plt.plot(results_avg["Date"],results_avg["Hospitalized"])
	plt.plot(results_avg["Date"],results_avg["ICU"])

	plt.legend(['Infected','Hospitalized','ICU'])
	plt.xlabel("Date")
	plt.xticks(rotation=90)
	plt.title("SIER model with social distancing for Population=%.d \nrho=%.2f, r0 = %.1f, alpha=%.2f, gamma=%.2f" %(N, rho, r0, alpha, gamma))
	plt.tight_layout()
	plt.savefig("Average_Plot.png",dpi=150)
	# plt.show()

	# Peak Infected, Hospitalized & ICU per week
	tot_wk = round(len(results_avg)/7)
	x=0
	y=7
	Inf_max = []
	Hos_max = []
	ICU_max = []
	Week_no = []
	for i in range(tot_wk):
			next_Inf = results_avg.Infected[x:y].max()
			next_Hos = results_avg.Hospitalized[x:y].max()
			next_ICU = results_avg.ICU[x:y].max()
			Inf_max.append(next_Inf)
			Hos_max.append(next_Hos)
			ICU_max.append(next_ICU)
			Week_no.append(i)
			x = y
			y = y + 7
			i = i + 1

	Date_max = pd.date_range(start='2/1/2020', periods=len(Week_no), freq='W-SAT')

	results_peak = pd.DataFrame(
			{'Week_Number': Week_no,
			 'Date': Date_max,
			 'Peak_Infected': Inf_max,
			 'Peak_Hospitalized': Hos_max,
			 'Peak_ICU': ICU_max,
			})

	plt.figure(figsize = [8,4])
	plt.plot(results_peak["Week_Number"],results_peak["Peak_Infected"])
	plt.plot(results_peak["Week_Number"],results_peak["Peak_Hospitalized"])
	plt.plot(results_peak["Week_Number"],results_peak["Peak_ICU"])
	plt.legend(['Peak Infected','Peak Hospitalized','Peak ICU'])
	plt.xlabel("Week Number")
	plt.title("SIER model with social distancing for Population=%.d \nrho=%.2f, r0 = %.1f, alpha=%.2f, gamma=%.2f" %(N, rho, r0, alpha, gamma))
	plt.savefig("Weekly_Peak_Plot.png", dpi = 150)
	# plt.show()

# Create Dashboard window
	
	# win2 = Tk()
	win2 = Toplevel()
	win2.title("COVID-19 Prediction")
	# win2.geometry('600x600')
	
	#HEADER
	label_0 = Label(win2, text="SEIR Model with Social Distancing", font=("bold", 14), relief=RAISED, fg="#3F4D68")
	label_0.grid(row=0, column=0, columnspan=2, pady=10, padx=40)

	frame1=Frame(win2, borderwidth=2)
	frame2=Frame(win2)
	frame3=Frame(win2)
	frame4=Frame(win2)

	#DESCRIPTION
	label_2 = Label(win2, text="Indian Data:", anchor=W, font=("bold", 10), relief=GROOVE, fg="#3F4D68")
	label_2.grid(row=2, columnspan=2)
	label_2a = Label(win2, text="https://www.mygov.in/covid-19")
	label_2a.grid(row=3, column=0, columnspan=2)
	label_3 = Label(win2, text="      ")
	label_3.grid(row=4, columnspan=2)
	label_3 = Label(win2, text="Setup simulation:", anchor=S, font=("bold", 10), relief=GROOVE, fg="#3F4D68")
	label_3.grid(row=5, columnspan=2)

	#Frame1
	label_1 = Label(frame1, text="Population :", width=20, anchor=E)
	label_1.grid(row=0, column=0)
	label_2 = Label(frame1, text="r0 :", width=20, anchor=E)
	label_2.grid(row=1, column=0)
	label_2 = Label(frame1, text="rho :", width=20, anchor=E)
	label_2.grid(row=2, column=0)
	label_2 = Label(frame1, text="alpha :", width=20, anchor=E)
	label_2.grid(row=3, column=0)
	label_2 = Label(frame1, text="gamma :", width=20, anchor=E)
	label_2.grid(row=4, column=0)

	#Frame2
	label_1 = Label(frame2, text=N, relief=SUNKEN, width=10, anchor=W, justify=LEFT)
	label_1.grid(row=0, column=0)
	label_2 = Label(frame2, text=r0, relief=SUNKEN, width=10, anchor=W)
	label_2.grid(row=1, column=0)
	label_2 = Label(frame2, text=rho, relief=SUNKEN, width=10, anchor=W)
	label_2.grid(row=2, column=0)
	label_2 = Label(frame2, text=alpha, relief=SUNKEN, width=10, anchor=W)
	label_2.grid(row=3, column=0)
	label_2 = Label(frame2, text=gamma, relief=SUNKEN, width=10, anchor=W)
	label_2.grid(row=4, column=0)

	#Frame 1 & Frame 2 - GRID
	frame1.grid(row=6, column=0, padx=40, sticky=E)
	frame2.grid(row=6, column=1, padx=40, sticky=W)

	#Summary
	label_1 = Label(win2, text="Summary Dashboard", font=("bold", 14), relief=RAISED, fg="#3F4D68")
	label_1.grid(row=7, column=0, columnspan=2, pady=10)

	label_2 = Label(win2, text="Simulation Result:", font=("bold", 10), relief=GROOVE, fg="#3F4D68")
	label_2.grid(row=8, column=0, columnspan=2)

	#GRAPH
	load = Image.open("Average_Plot.png")
	load = load.resize((500, 250), Image.ANTIALIAS)
	render = ImageTk.PhotoImage(load)
	img = Label(win2, image=render)
	img.image = render
	img.grid(row=0, column=3, rowspan=9, padx=10)
	

	#Frame3
	label_1 = Label(frame3, text="Peak Infected :", width=20, anchor=E)
	label_1.grid(row=0, column=0)
	label_2 = Label(frame3, text="Peak Hospitalized :", width=20, anchor=E)
	label_2.grid(row=1, column=0)
	label_2 = Label(frame3, text="Peak ICU :", width=20, anchor=E)
	label_2.grid(row=2, column=0)

	#Frame4
	PI = results_avg["Infected"].max()
	PH = results_avg["Hospitalized"].max()
	PU = results_avg["ICU"].max()
	label_1 = Label(frame4, text=PI, relief=SUNKEN, width=10, anchor=W, justify=LEFT)
	label_1.grid(row=0, column=0)
	label_2 = Label(frame4, text=PH, relief=SUNKEN, width=10, anchor=W)
	label_2.grid(row=1, column=0)
	label_2 = Label(frame4, text=PU, relief=SUNKEN, width=10, anchor=W)
	label_2.grid(row=2, column=0)

	#Frame 3 & Frame 4 - GRID
	frame3.grid(row=10, column=0, padx=40, sticky=E)
	frame4.grid(row=10, column=1, padx=40, sticky=W)

	label_3 = Label(win2, text="      ")
	label_3.grid(row=11, columnspan=2)

	#Download Dashboard
	
	def get_dash():
	
		path = askdirectory(title='Select Folder') # shows dialog box and return the path
				
		workbook = xlsxwriter.Workbook(path + '/SEIR_Dashboard_%s.xlsx' % ext)
		worksheet = workbook.add_worksheet()

		# Set the columns widths.
		worksheet.set_column('A:A', 20)

		# Insert the images
		worksheet.insert_image('D1', 'Weekly_Peak_Plot.png')
		worksheet.insert_image('D21', 'Average_Plot.png')

		worksheet.write('A2', "Indian Data:")
		worksheet.write('A3', "https://www.mygov.in/covid-19")

		worksheet.write('A5', "Setup simulation:")
		worksheet.write('A6', "Population:")
		worksheet.write('B6', N)
		worksheet.write('A7', "r0:")
		worksheet.write('B7', r0)
		worksheet.write('A8', "rho:")
		worksheet.write('B8', rho)
		worksheet.write('A9', "Alpha:")
		worksheet.write('B9', alpha)
		worksheet.write('A10', "Gamma:")
		worksheet.write('B10', gamma)

		worksheet.write('A12', "Simulation Result:")
		worksheet.write('A13', "Peak Infected:")
		worksheet.write('B13', PI)
		worksheet.write('A14', "Peak Hospitalized:")
		worksheet.write('B14', PH)
		worksheet.write('A15', "Peak ICU:")
		worksheet.write('B15', PU)

		workbook.close()
		
		results_avg.to_csv(path + "/prediction_daywise_%s.csv" % ext)
		results_peak.to_csv(path + "/prediction_weekwise_%s.csv" % ext)

		
	def exit_p():
		os.remove("Weekly_Peak_Plot.png")
		os.remove("Average_Plot.png")
		win2.destroy()
	
	# dash_param1 = N, r0, rho, alpha, gamma
	# dash_param2 = results_avg
	Button(win2, text='Download the Reports', width=25, bg='brown', fg='white', command=get_dash).grid(row=9, column=3)
	Button(win2, text='Exit', width=25, bg='brown', fg='white', command=exit_p).grid(row=10, column=3, pady=5)
	
	win2.mainloop()

print("Input the Parameters")
input_window()

print("End of process")
