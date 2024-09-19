# MKU_Assignment Texas_Holdem_Calcualtor 
 A probability solver for texas holdem poker

The documnatation of the porject can be seen here:
https://github.com/LevianDanProduction/MKU_Assignment-Texas_Holdem_Calculator/blob/main/Project%20Presentation.pdf

### Overview
The **Texas Hold'em Poker Calculator** is a project designed to simulate poker games and predict outcomes using computational algorithms. The goal is to help players better understand their chances of winning in different situations.

### Key Features
- **Game Engine**: Simulates Texas Hold'em poker games, dealing with real card combinations and outcomes.
- **Poker Hand Strength**: Calculates hand strengths using a pre-generated table of all possible poker hands, including tiebreakers.
- **Prediction Algorithm**: Predicts future poker hand combinations using Monte Carlo simulations, allowing for strategic insights.
- **User Interface**: Provides a graphical representation of poker scenarios using a GUI built with Pygame.
- **Data Analysis**: Utilizes Python libraries (Pandas, Numpy) for data manipulation and insights.

### Tech Stack
- **Programming**: Python (OOP)
- **Libraries**: Itertools, Pandas, Pygame, Numpy, Random
- **Simulations**: Monte Carlo method
- **Visualization**: Power BI

### Challenges Addressed
- **Probabilities in Poker**: Computes win probabilities based on different game states and player hands.
- **Game Strategy**: Provides data-driven insights into optimal poker strategies based on simulated game outcomes.
- **Future Implementations**: Potential additions include folding, betting mechanics, and multi-deck simulations.

Instructions to run:

GUI 🃏 - need the pickle file from this part to run the others

    0. Make sure any dpependants are installed as well. eg. pygame (The requirements here are a bit unclean, will soon have a proper module list)

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
