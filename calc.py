#!/usr/bin/env python3

import yaml
import os

BMR = 2090

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "food.yml")

with open(PATH) as f:
    YML = yaml.safe_load(f)

def food_sum(food, kcal = 0, p = 0):
    if type(food) == list:
        for x in food:
            kcal, p = food_sum(x, kcal, p)
    if type(food) == dict:
        if 'ingredients' in food:
            kcal2, p2 = food_sum(food['ingredients'])
            qty = food['qty'] if 'qty' in food else 1
            kcal += kcal2*qty
            p += p2*qty
        else:
            qty = food['qty'] if 'qty' in food else 1
            kcal += food['kcal']*qty if 'kcal' in food else 0
            p += food['p']*qty if 'p' in food else 0
    return kcal, p

# Calculate burn using BMR and Harris-Benedict exercise multipliers.
_activity = 0
def burn(food):
    def mul():
        global _activity
        if 'activity' in food[0]:
            _activity = food[0]['activity']
        act = _activity
        if act == 0:
            return 1.2
        if act == 1:
            return 1.375
        if act == 2:
            return 1.55
        if act == 3:
            return 1.725
        if act == 4:
            return 1.9
        raise Exception(str(act)+"? No you didn't.")

    return BMR*mul()

def main():
    kg = 0
    for day, food in sorted(YML['days'].items()):
        kcal, p = food_sum(food)
        brn = burn(food)
        diff = kcal - brn
        kg += diff/7700
        fmt = "{:%Y-%m-%d}\tkcal:{:.1f}\tp:{:.1f}\tb:{:.1f}\tdiff:{:.1f}\tkg:{:.2f}"
        print(fmt.format(day, kcal, p, brn, diff, kg))

if __name__ == '__main__':
    main()
