import tkinter as tk
from tkinter import *
import re

# Define the diseases and their symptoms
disease_data = {
    'Influenza': ['fever', 'cough', 'headache', 'sore throat'],
    'Food Poisoning': ['vomiting', 'weakness', 'fever'],
    'Diarrhea': ['watery stool', 'vomiting', 'abdominal cramps'],
    'Common Cold': ['sneezing', 'runny nose', 'cough'],
    'COVID-19': ['fever', 'dry cough', 'tiredness', 'loss of taste or smell'],
    'Chickenpox': ['itching', 'skin rash', 'fever', 'fatigue'],
    'Measles': ['fever', 'cough', 'runny nose', 'conjunctivitis'],
    'Mumps': ['fever', 'swollen glands (neck)', 'muscle pain', 'loss of appetite'],
    'Tuberculosis': ['cough', 'chest pain', 'weight loss', 'night sweats'],
    'Typhoid': ['high fever', 'stomach pain', 'headache', 'weakness'],
    'Hepatitis A': ['fatigue', 'nausea', 'abdominal pain', 'jaundice'],
    'Malaria': ['fever', 'chills', 'headache', 'nausea', 'vomiting'],
    'Dengue Fever': ['high fever', 'severe headache', 'joint pain', 'pain behind the eyes'],
    'Cholera': ['profuse watery diarrhea', 'vomiting', 'leg cramps', 'dehydration'],
    'Rabies': ['fever', 'headache', 'excessive salivation', 'fear of water'],
    'Impetigo': ['red sores', 'oozing fluid', 'crusty golden-brown sores'],
    'Pneumonia': ['cough', 'fever', 'chills', 'shortness of breath'],
    'HIV/AIDS': ['fever', 'unexplained weight loss', 'extreme tiredness', 'swollen lymph nodes'],
    'Scabies': ['itching', 'skin rash', 'pimple-like irritations'],
    'Chlamydia': ['painful urination', 'lower abdominal pain', 'unusual discharge', 'rectal pain or discharge'],
    'Gonorrhea': ['painful urination', 'discharge from genitals', 'rectal pain', 'sore throat'],
    'Syphilis': ['sores (chancre) on genitals, anus, or mouth', 'rash on palms of hands or soles of feet', 'fever', 'fatigue'],
    'Ringworm': ['itching', 'skin rash', 'redness of skin']
}

# Flatten the disease_data for the autocomplete list
autocompleteList = sorted(set([symptom for symptoms in disease_data.values() for symptom in symptoms]))

# Define the autocomplete entry class
class AutocompleteEntry(tk.Entry):
    def __init__(self, autocompleteList, *args, **kwargs):
        self.listboxLength = 0
        self.parent = args[0]
        
        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)
            self.matchesFunction = matches

        # Custom return function
        if 'returnFunction' in kwargs:
            self.returnFunction = kwargs['returnFunction']
            del kwargs['returnFunction']
        else:
            def selectedValue(value):
                print(value)
            self.returnFunction = selectedValue

        tk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.bind("<Return>", self.selection)
        self.bind("<Escape>", self.deleteListbox)

        self.listboxUp = False

    def deleteListbox(self, event=None):
        if self.listboxUp:
            self.listbox.destroy()
            self.listboxUp = False

    def selection(self, event=None):
        if self.listboxUp:
            index = self.listbox.curselection()[0]
            value = self.listbox.get(tk.ACTIVE)
            self.listbox.destroy()
            self.listboxUp = False
            self.delete(0, tk.END)
            self.insert(tk.END, value)
            self.returnFunction(value)

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.deleteListbox()
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listboxLength = len(words)
                    self.listbox = tk.Listbox(self.parent,
                                              width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(
                        x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                else:
                    self.listboxLength = len(words)
                    self.listbox.config(height=self.listboxLength)

                self.listbox.delete(0, tk.END)
                for w in words:
                    self.listbox.insert(tk.END, w)
            else:
                self.deleteListbox()

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(tk.END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            self.listbox.selection_clear(first=index)
            index = str(int(index) - 1)
            if int(index) == -1:
                index = str(self.listboxLength - 1)

            self.listbox.see(index)  # Scroll!
            self.listbox.selection_set(first=index)
            self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '-1'
            else:
                index = self.listbox.curselection()[0]

            if index != tk.END:
                self.listbox.selection_clear(first=index)
                if int(index) == self.listboxLength - 1:
                    index = "0"
                else:
                    index = str(int(index) + 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]

# Function to predict disease
def prediction():
    symptoms = [symptom_entry1.get(), symptom_entry2.get(), symptom_entry3.get(), symptom_entry4.get(), symptom_entry5.get()]
    symptoms = [s for s in symptoms if s]  # Remove empty strings
    max_match = 0
    predicted_disease = "Unknown Disease"
    
    for disease, disease_symptoms in disease_data.items():
        match_count = len(set(symptoms) & set(disease_symptoms))
        if match_count > max_match:
            max_match = match_count
            predicted_disease = disease
    
    final_result.delete(0, tk.END)
    final_result.insert(0, f'You might be suffering from: {predicted_disease}')

# Set up the main application window
root = tk.Tk()
root.title("Disease Prediction")

frame = LabelFrame(root, padx=10, pady=30, highlightthickness=2)
frame.pack(padx=50, pady=50)

c = Label(frame, text="Disease Prediction System", fg='blue4')
c.grid(row=0, column=0, columnspan=3, pady=(0, 20), padx=(30, 30), sticky="nsew")
c.config(font=("Consolas", 32, 'bold'))

L1 = Label(frame, text='Symptom 1:')
L1.grid(row=1, column=0, sticky=W, pady=(0, 10), padx=(120, 0))
L1.config(font=("Consolas", 20))
symptom_entry1 = AutocompleteEntry(
    autocompleteList, frame, width=32, fg='orange', bg='black', insertbackground='orange')
symptom_entry1.grid(row=1, column=1)
symptom_entry1.config(font=('Consolas', 15, 'bold'))

L2 = Label(frame, text='Symptom 2:')
L2.grid(row=2, column=0, sticky=W, pady=(0, 10), padx=(120, 0))
L2.config(font=("Consolas", 20))
symptom_entry2 = AutocompleteEntry(
    autocompleteList, frame, width=32, fg='orange', bg='black', insertbackground='orange')
symptom_entry2.grid(row=2, column=1)
symptom_entry2.config(font=('Consolas', 15, 'bold'))

L3 = Label(frame, text='Symptom 3:')
L3.grid(row=3, column=0, sticky=W, pady=(0, 10), padx=(120, 0))
L3.config(font=("Consolas", 20))
symptom_entry3 = AutocompleteEntry(
    autocompleteList, frame, width=32, fg='orange', bg='black', insertbackground='orange')
symptom_entry3.grid(row=3, column=1)
symptom_entry3.config(font=('Consolas', 15, 'bold'))

L4 = Label(frame, text='Symptom 4:')
L4.grid(row=4, column=0, sticky=W, pady=(0, 10), padx=(120, 0))
L4.config(font=("Consolas", 20))
symptom_entry4 = AutocompleteEntry(
    autocompleteList, frame, width=32, fg='orange', bg='black', insertbackground='orange')
symptom_entry4.grid(row=4, column=1)
symptom_entry4.config(font=('Consolas', 15, 'bold'))

L5 = Label(frame, text='Symptom 5:')
L5.grid(row=5, column=0, sticky=W, pady=(0, 10), padx=(120, 0))
L5.config(font=("Consolas", 20))
symptom_entry5 = AutocompleteEntry(
    autocompleteList, frame, width=32, fg='orange', bg='black', insertbackground='orange')
symptom_entry5.grid(row=5, column=1)
symptom_entry5.config(font=('Consolas', 15, 'bold'))

# Predict Button
predict_button = tk.Button(frame, text='Predict', command=prediction, bg='red', fg='white', activebackground='red')
predict_button.config(font=('Consolas', '18', 'bold'))
predict_button.grid(row=6, column=1, pady=(10, 50), padx=(0, 180))

# Clear Button
def clear_entries():
    symptom_entry1.delete(0, END)
    symptom_entry2.delete(0, END)
    symptom_entry3.delete(0, END)
    symptom_entry4.delete(0, END)
    symptom_entry5.delete(0, END)
    final_result.delete(0, END)

clear_button = tk.Button(frame, text='Clear', bg='red', fg='white', activebackground='red', command=clear_entries)
clear_button.config(font=('Consolas', '18', 'bold'))
clear_button.grid(row=6, column=1, padx=(100, 0), pady=(10, 50), columnspan=2)

# Result Entry
final_result = Entry(frame, width=50, borderwidth=0, bg='green', fg='white', justify=CENTER, insertbackground='green')
final_result.grid(row=8, column=0, pady=(0, 20), padx=(60, 0), columnspan=2)
final_result.config(font=('Consolas', 20, 'bold'))
final_result.bind("<Key>", lambda e: "break")

tt = Label(frame, text='Note: Use at least 3 symptoms for better results')
tt.grid(row=11, column=0, columnspan=2, padx=(60, 0))
tt.config(font=('', 15, 'bold'))

root.mainloop()
