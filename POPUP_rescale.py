import tkinter as tk

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
            return False


def POPUP_rescale(master, scaling_factor_in):
    
    rescale_check = None
    scaling_factor = None

    def check(string):
        
        nonlocal rescale_check, scaling_factor
        
        if string == 'yes':
            
            if is_float(factorentry.get()) == False:
                
                print("Error: Scaling factor must be a floating point number!")
                
                tk.messagebox.showinfo('Error', 'Scaling factor must be a floating point number!')
            else: 
                
                scaling_factor = float(factorentry.get())
                print(f"Scaling factor is float: {scaling_factor}")
                
                goodfact = tk.messagebox.askquestion('Please check', f'Is this the correct scaling factor {scaling_factor}?')
                
                if goodfact == "yes":
                    rescale_check = True
                    window.destroy()
                
        if string == 'no':
            
            rescale_check = False
            scaling_factor = 1
            window.destroy()
            

    #create GUI
    if master == None:
        window = tk.Tk()
    else:
        window = tk.Toplevel(master)

    window.geometry("300x300")
    window.title('Rescale source image?')

    ###################################
    # define the widgets:
        
    label = tk.Label(window, text= 'Do you want to rescale the source image?')
    label.grid(row=0, column=0, padx=10, pady=5, sticky="n,w")
    
    factorlabel = tk.Label(window, text= 'Scaling factor:')
    factorlabel.grid(row=1, column=0, padx=5, pady=30, sticky="n,w")
    factorentry = tk.Entry(window, width=6)
    factorentry.insert(0,str(scaling_factor_in))
    factorentry.grid(row=1, column=1, padx=5, pady=30, sticky="n,w")
    
    yesbutton = tk.Button(window, text='YES', command=lambda: check('yes'))
    yesbutton.grid(row=2, column=0, padx=10, pady=30, sticky="n,w")
    
    nobutton = tk.Button(window, text='NO', command=lambda: check('no'))
    nobutton.grid(row=2, column=1, padx=10, pady=30, sticky="n,w")

    ##################################
    # some tkinter window configuration:
    
    if master == None:
        window.mainloop()
    else:
        window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
        window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        window.grab_set()
        master.wait_window(window)

    return rescale_check, scaling_factor

# Create the window and run
if __name__ == "__main__":
    print(POPUP_rescale(master = None, scaling_factor_in = 1.666))
