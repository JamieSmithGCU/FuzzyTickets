## Required imports
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl


Level_Of_Loyalty = ctrl.Antecedent(np.arange(0, 6, 1), 'Level of Loyalty')
Merchandise_Purchased = ctrl.Antecedent(np.arange(0, 6, 1), 'Merchandise Purchased')
Remaining_Tickets = ctrl.Antecedent(np.arange(0, 6, 1), 'Remaining Tickets')
Discount_Amount = ctrl.Consequent(np.arange(0, 16, 1), 'Discount Amount')


Level_Of_Loyalty['Low'] = fuzz.gaussmf(Level_Of_Loyalty.universe, -2.776e-17, 1.062)
Level_Of_Loyalty['Medium'] = fuzz.gaussmf(Level_Of_Loyalty.universe, 2.5, 1.062)
Level_Of_Loyalty['High'] = fuzz.gaussmf(Level_Of_Loyalty.universe, 5, 1.062)


Merchandise_Purchased['None'] = fuzz.gaussmf(Merchandise_Purchased.universe, 2.776e-17, 0.8846)
Merchandise_Purchased['Some'] = fuzz.gaussmf(Merchandise_Purchased.universe, 2.5, 0.8846)
Merchandise_Purchased['Alot'] = fuzz.gaussmf(Merchandise_Purchased.universe, 5, 0.8846)


Remaining_Tickets['Low'] = fuzz.gaussmf(Remaining_Tickets.universe, -6.94e-17, 0.8845)
Remaining_Tickets['Medium']= fuzz.gaussmf(Remaining_Tickets.universe, 2.5, 0.8845)
Remaining_Tickets['High'] = fuzz.gaussmf(Remaining_Tickets.universe, 5, 0.8845)


Discount_Amount['None'] = fuzz.trapmf(Discount_Amount.universe, [-3.38, -0.375, 0, 0])
Discount_Amount['Low'] = fuzz.trapmf(Discount_Amount.universe, [0, 3.38, 4.12, 7.12])
Discount_Amount['Medium'] = fuzz.trapmf(Discount_Amount.universe, [4.125, 7.125, 7.875, 10.88])
Discount_Amount['High'] = fuzz.trapmf(Discount_Amount.universe, [7.875, 10.88, 11.62, 14.62])
Discount_Amount['Very High'] = fuzz.trapmf(Discount_Amount.universe, [11.6, 14.984693877551, 15.4, 18.4])

# You can see how these look with .view()
# Level_Of_Loyalty.view()
# plt.show()
# Merchandise_Purchased.view()
# plt.show()
# Remaining_Tickets.view()
# plt.show()
# Discount_Amount.view()
# plt.show()


## Rules
rule1 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['None'] & Remaining_Tickets['High'], Discount_Amount['Low'])
rule2 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['None'] & Remaining_Tickets['Medium'], Discount_Amount['None'])
rule3 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['None'] & Remaining_Tickets['Low'], Discount_Amount['None'])
rule4 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Some'] & Remaining_Tickets['High'], Discount_Amount['Medium'])
rule5 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Medium'], Discount_Amount['Low'])
rule6 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Low'], Discount_Amount['Low'])
rule7 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['High'], Discount_Amount['Medium'])
rule8 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Medium'], Discount_Amount['Low'])
rule9 = ctrl.Rule(Level_Of_Loyalty['Low'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Low'], Discount_Amount['Low'])
rule10 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['None'] & Remaining_Tickets['Low'], Discount_Amount['Low'])
rule11 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['None'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])
rule12 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['None'] & Remaining_Tickets['High'], Discount_Amount['Medium'])
rule13 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Low'], Discount_Amount['Low'])
rule14 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])
rule15 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Some'] & Remaining_Tickets['High'], Discount_Amount['High'])
rule16 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Low'], Discount_Amount['Low'])
rule17 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])
rule18 = ctrl.Rule(Level_Of_Loyalty['Medium'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['High'], Discount_Amount['High'])
rule19 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['None'] & Remaining_Tickets['Low'], Discount_Amount['Medium'])
rule20 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['None'] & Remaining_Tickets['Medium'], Discount_Amount['Medium'])
rule21 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['None'] & Remaining_Tickets['High'], Discount_Amount['High'])
rule22 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Low'], Discount_Amount['Medium'])
rule23 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Some'] & Remaining_Tickets['Medium'], Discount_Amount['High'])
rule24 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Some'] & Remaining_Tickets['High'], Discount_Amount['Very High'])
rule25 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Low'], Discount_Amount['High'])
rule26 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['Medium'], Discount_Amount['Very High'])
rule27 = ctrl.Rule(Level_Of_Loyalty['High'] & Merchandise_Purchased['Alot'] & Remaining_Tickets['High'], Discount_Amount['Very High'])

# rule1.view()
# plt.show()
# rule2.view()
# plt.show()
# etc...

discount_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])

discount = ctrl.ControlSystemSimulation(discount_ctrl)


# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
discount.input['Level of Loyalty'] = 5
discount.input['Merchandise Purchased'] = 5
discount.input['Remaining Tickets'] = 5

# Crunch the numbers
discount.compute()

print(discount.output['Discount Amount'].round(2))
Discount_Amount.view(sim=discount)
plt.show()


