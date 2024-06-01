# Description

A simple Bayesian Network of factors regaurding vaccination during a zombie outbreak. 

Variables:
- M: Mandate vaccine
- F: Fear of zombies
- P: Proximity (close)
- S: Size of outbreak (large)
- V: Vaccinated
- I: Not Infected
- B: Don't Bite and infect family members
- T: Money for vacation

The Vaccinated table in the PDF was derived by summing the following values when true, respectively:
-	M: 0.15 (Obeying the mandate is important only to few people)
-	F: 0.6 (Fear was the highest motivator for being vaccinated)
-	P: 0.05 (Proximity had little effect, because by the time zombies are close, most vaccination clinics are already overrun)
-	S: 0.2 (The size of the outbreak is important, but many don’t realize the danger if they aren’t afraid of zombies, and haven’t seen them yet in person)

The code explores every combination (T/F) of variables M, F, P, S, and orders the results by utility (high to low):
- Utility(T: Having money for vacation) = 55
- Utility(I: Not being infected) = 60
- Utility(B: Not biting and infecting family) = 80
  
NOTES:
- See the attached PDF for a visualization of the Bayesian Network
- With pgmpy, you can optionally define state_names for variable states, rather than using indexes