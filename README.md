# MKU_Assignment Texas_Holdem_Calcualtor 
 A probability solver for texas holdem poker

The documnatation of the porject can be seen [here](Project Presentation.pdf)

Instructions to run:

GUI 🃏 - need the pickle file from this part to run the others

    0. Make sure any dpependants are installed as well. eg. pygame

    1. Navigate to tablegen.py
    2. Run the file to generate a data table called card6.csv
    3. Then go into line 1066 and remove the intructed hashtags so that the code to generate a picke file called hand_to_row_2.pickle works
    4. Run the program to have the pickle file generated
    5. You can now recomment the part of the code that generates the file

    6. enjoy your calculator :|

Simulator:
    1. ensure your pickle file exists. 
    2. open and run screenSim.py

    ⚠️ When imputting card hands/ commiunity, make sure that you are typing as if you are writing an anctual python list.

Predictor:
    1. ensure your pickle file exists. 
    2. open predictor.py
    3. run it as it is to have a random hand predicted, or inject your own state by uncommenting 264 and replacing with values. 
