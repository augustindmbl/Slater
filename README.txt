			SLATER TRANSITION ENERGY CALCULATION 
	   			    (27/06/2025)

CONTENT

	This toolkit provides a set of Python scripts and utilities for performing 
	atomic energy calculations. In this purpose it used a Relativistic Screened 
	Hydrogenic Model (RSHM) such as described [1]. The model could used three 
	sets of screening constants : Mendozza [1], Lanzini [2] and Faussurier [3]. 
	The interface is powered by Streamlit (https://streamlit.io/), allowing for 
	a simple and interactive use of the code.

INSTALLATION

	1) Install Python (version 3.9 or higher) if it's not already done. Download 
	the installer from https://www.python.org/downloads/windows/ and make sure 
	to check **"Add Python to PATH"** during installation. Verify that Python is
	well added to the path by typing : path <Enter> in a terminal. You should 
	see at least 3 path with "Python" in their name. To verify if everything is 
	well installed type : python --version <Enter> in the terminal. You should 
	have Python 3.X.X. 

	2) Upgrad pip (installer of library for Python) by typing : python -m pip 
	install --upgrade pip <Enter> in the terminal.

	3) Extract all the files from the SLATER.ZIP archive. 

	4) Open a terminal and go to the SLATER folder using cd <folder path> 
	<Enter>. Type pip install -r requirements.txt <Enter> to install all the 
	required library. To verify everything is well installer type : python -c 
	"import streamlit; import numpy; import streamlit-autorefresh; 
	print('All imports successful!')" <Enter>. If everything is good you should 
	have a terminal print : 'All imports successful!'. 

RUNNING THE PROGRAM

	In a terminal go to the SLATER folder using cd <folder path> <Enter> and 
	then type : streamlit run main.py <Enter>. The first time it will ask an 
	e-mail to keep aware of new versions of Streamlit, juste press <Enter>. 
	Windows will also ask if Python can access private network, accept. Then a 
	window will be opened with the interface of the program.

EXIT THE PROGRAM

	To quit the program, you have to kill the process in your terminal using 
	CTRL + C. /!\ Closing the window will not quit ther program. /!\


REFERENCES

	[1] M.A. Mendoza, J.G. Rubiano, J.M. Gil, R. Rodríguez, R. Florido, 
		P. Martel, E. Mínguez, A new set of relativistic screening constants for 
		the screened hydrogenic model, High Energy Density Physics, Volume 7, 
		Issue 3, 2011, p.169-179.

	[2] Fernando Lanzini, Héctor O. Di Rocco, Screening parameters for the 
		relativistic hydrogenic model, High Energy Density Physics, Volume 17, 
		Part B, 2015, p.240-247.

	[3] G. Faussurier, C. Blancard, P. Renaudin, Equation of state of dense 
		plasmas using a screened-hydrogenic model with ℓ-splitting, High Energy 
		Density Physics, Volume 4, Issues 3–4, 2008, p.114-123.
