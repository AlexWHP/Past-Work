# Strategy Game (Retired)
Foundational code of a strategy game and early building of a game engine

## Disclaimer
Warning - This is a copy of the files I originally had, however, I have since switched PC and this is not in a working state at all. It exists to display knowledge of C and C++ alongside the ability of self-directed learning and work. Reviewing my code, there is a significant amount wrong with it, for example I have created large quantities of files for similar classes and functions alongside a great difficulty to follow along with what is occuring due to a lack of comments and docstrings. Reflecting on it, I would almost change everything, however I am still proud of the extent in which I was able to push this project, especially given the afforementioned flaws.

## Description
This game aimed to aleviate late game performance issues of grand strategy games by utilising an object orientated approach to the tiles that formed the foundation of the game. For the testing ground I modelled Ireland, the four provinces (Ulster, Connaught, Leinser, and Munster) and their constituent counties (32 in total). It possesed a functional window which allowed for selection of three tiers of bitmaps (Aiming to sacrifice memory for performance) and checking each layer if it had been formed. Intended mechanics were to incorporate conquest, production, population, and formation of greater areas.

## Performance improvement
To improve performance I intended on ticking down the nodal tree structure. By ticking I mean the calculation of the reward of mechanics on a regular basis. For other games this presents a major issue as towards the late game they can become bloated with added buildings and modifiers as well as the smaller parts becoming more and more arbritrary as you grow larger. My solution was to abstract once certain conditions were met with these building and modifiers carrying up the tree.

As an example, the game checks for formation in territory -> region -> provinces or Ireland -> Leinster -> Meath but if I controlled all of the provinces in Leinster and combined my provinces I would perform one set of calculations for one region rather than nine sets for provinces. Extended to a far larger scale at an increase at computation early on, late game performance would be significantly better. As a benefit towards this, these more abstracted areas could have greater mechanics associated with them that are inheritited by their parents. 

TLDR - As the game progresses, there are less things to be ticked whilst keeping a healthy level of abstraction for the player. Improving performance into the lategame and keeping controlled land relevant.

