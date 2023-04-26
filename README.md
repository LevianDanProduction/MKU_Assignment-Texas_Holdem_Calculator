---
description: All the potential ways of going about calculating poker possibilities
cover: .gitbook/assets/kevin-bosc-0MkMo1d8yx8-unsplash.jpg
coverY: 0
---

# ♦ Poker Strategy

## Game Logic

Calculating different hand powers based of of:

* Hand Rank&#x20;
* Tie Breakers

Checking for different circumstances that will change the way possibilities are calculated:&#x20;

* Community cards/ Certain hands affecting the chances of anyone having a certain hand

## Math

* Probability&#x20;
  * &#x20;**Absolute possibility: e.g. pair of aces > other possible hands**
* Speculative:&#x20;
  * What could happen e.g. 4/5 probability of a specific hand&#x20;
  * Looking for a specific possibility for a hand&#x20;
  * Percentage chance for each rank and comparing that to what probabilistically wins overall
* Ways of Storing/Processing
  * Data Table - Faster once made/ Harder to account for all changes (maybe for absolute) cant make it exclusive to (Maybe Premade?)
  * Real Time - via real time math/ Slower/ Easier for specific situation and can differentiate between hand and community&#x20;
* Bar of possibility using multiple indicators&#x20;

How does the math change when there are multiple decks in one, would you have to consider a five of a kind?

## Computation/Programming

* Simulation
  * Calculating over N amount of games
  * Using a optimised Version of the program (Big o-notation)
  * Compare each result for N amount games to the absolute table or any other method etc
  * Could be used to compare to studies maybe.
