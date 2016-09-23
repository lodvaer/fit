#!/usr/bin/env python3

import yaml
import os

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "food.yml")

with open(PATH) as f:
    YML = yaml.safe_load(f)

def food_sum(food, kcal = 0, p = 0):
    if type(food) == list:
        for x in food:
            kcal, p = food_sum(x, kcal, p)
    if type(food) == dict:
        if 'ingredients' in food:
            kcal, p = food_sum(food['ingredients'], kcal, p)
        else:
            qty = food['qty'] if 'qty' in food else 1
            kcal += food['kcal']*qty if 'kcal' in food else 0
            p += food['p']*qty if 'p' in food else 0
    return kcal, p

def main():
    for day, food in sorted(YML['days'].items()):
        kcal, p = food_sum(food)
        print(day.isoformat(), '\tkcal:', kcal, '\tp:', p)

if __name__ == '__main__':
    main()
