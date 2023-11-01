import os

import keyboard
import time
from datetime import datetime
import json
import csv

def checkChoice():
    choice = ""
    work = True
    while work:
        try:
            choice = input('Ваш выбор: ')
            # return int(choice)
            if int(choice) == 1 or int(choice) == 2:
                work = False
                return int(choice)
            else:
                raise(ValueError)
        except:
            print("Введите 1 или 2)")


def readableText(text):
    sentence = text.split('.')
    updatedText = list()
    for i in range(1, len(sentence)):
        if len(sentence[i - 1] + sentence[i]) > 150:
            updatedText.append(sentence[i - 1] + '.\n')
        else:
            updatedText.append(sentence[i - 1] + '.' + sentence[i] + '.\n')
    return "".join(updatedText)


def takeStepsAChoices():
    choices = dict()
    choicesToStep = dict()
    with open('игра.txt', 'r', encoding='UTF-8') as file:
        steps = []
        currentStepText = ""
        for line in file:
            if line.startswith("Шаг "):
                step = currentStepText.split('\n')
                steps.append(step[-1].split('?')[0])
                try:
                    if step[-1].find('?') != -1:
                        stepChoices = step[-1].split('?')[-1].split('. ')
                        choicesDict = dict()
                        choiceToStep = dict()
                        for id, choice in enumerate(stepChoices):
                            if id != 0:
                                if id == 1:
                                    choice = choice[:-2]
                                choicesDict[id] = choice.split(' (')[0]
                                # print(choice)
                                choices[step[0].split(' ')[1][:-1]] = choicesDict
                                findStep = choice.split(')')[0].find('к Шагу ')
                                choiceToStep[id] = choice.split(')')[0][findStep + 7:]
                                choicesToStep[step[0].split(' ')[1][:-1]] = choiceToStep
                except Exception:
                    pass
                currentStepText = line
            else:
                currentStepText += line.strip()
        if currentStepText:
            steps.append(currentStepText.split('\n')[-1])
        choices['53'] = {'1': "Попробовать начать разговор с существом",
                       '2': 'Подойти к существу ближе, чтобы лучше рассмотреть его'}
        choices['55'] = {'1': "Попытаться подружиться с ним", '2': "Осторожно отойти от существа"}
        choicesToStep['53'] = {1: '54', 2: '55'}
        choicesToStep['55'] = {1: '56', 2: '57'}
        steps.pop(0)
    return steps, choices, choicesToStep


def nextStep(step, steps: list, choices: dict, choicesToSteps: dict):
    step = int(step)
    stepText = steps[step - 1]
    stepChoices = None
    nextStepId = step + 1
    if step == 60:
        return
    try:
        stepChoices = choices[f'{step}']
    except Exception:
        pass
    if stepChoices != None:
        print(readableText(stepText))
        for choice in stepChoices.keys():
            print(f'{choice}: {stepChoices[choice]}')
        choice = checkChoice()
        takeChoice(step=step, steps=steps, choices=choices, choicesToSteps=choicesToSteps, choice=choice)
    else:
        print(readableText(stepText))
        takeChoice(step=nextStepId, steps=steps, choices=choices, choicesToSteps=choicesToSteps)


def takeChoice(step, steps: list, choices: dict, choicesToSteps: dict, choice=None):
    if choice != None:
        nextStepId = choicesToSteps[f'{step}'][choice]
        nextStep(steps=steps, choices=choices, choicesToSteps=choicesToSteps, step=nextStepId)
    else:
        nextStepId = step
        game(steps=steps, choices=choices, choicesToSteps=choicesToSteps, step=nextStepId)



def game(steps: list, choices: dict, choicesToSteps: dict, step=1):
    keyboard.wait('space')
    nextStep(step, steps, choices, choicesToSteps)


def saveToJson(startTime, endTime):
    data = list()
    newData = dict()
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            data = json.load(file)
    else:
        data = []
        with open('data.json', 'w') as file:
            json.dump(data, file)
    countSaves = len(data)
    newData['startTime'] = str(startTime)
    newData['numberOfSave'] = countSaves
    newData['endTime'] = str(endTime)
    durationOfTime = (endTime - startTime)
    newData['duratuonOfTime'] = str(durationOfTime)
    data.append(newData)
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    return data


def saveToCSV(startTime, endTime):
    data = list()
    if os.path.exists('data.csv'):
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    durationOfTime = str(endTime - startTime)
    newData = [str(startTime), str(endTime), durationOfTime]
    if len(data) != 0:
        data.append(newData)
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
            return data
    else:
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(newData)
            return newData

def deleteSave(jsonData, csvData):
    countChoices = 0
    work = True
    for id, choice in enumerate(jsonData):
        countChoices += 1
        print(f"{id + 1}: начало игры: {choice['startTime']} конец игры: {choice['endTime']}")
    print('Выберите номер сохранения которое вы хотите удалить: ')
    while work:
        try:
            choice = int(input('Ваш выбор: '))
            if choice >= 1 and choice <= countChoices:
                jsonData.pop(choice - 1)
                csvData.pop(choice - 1)
                work = False
            else:
                raise ValueError
        except ValueError:
            print(f"Введите число от 1 до {countChoices})")
    with open('data.json', 'w') as file:
        file.truncate(0)
        json.dump(jsonData, file, indent=4)
    with open('data.csv', 'w', newline='') as file:
        file.truncate(0)
        writer = csv.writer(file)
        for row in csvData:
            writer.writerow(row)


if __name__ == '__main__':
    startTime = datetime.now()
    steps_and_choices = takeStepsAChoices()
    steps = steps_and_choices[0]
    choices = steps_and_choices[1]
    choicesToSteps = steps_and_choices[2]
    steps[52] = steps[52].split('.1.')[0]
    steps[54] = steps[54].split(':')[0]
    print('Добро пожаловать в игру: Таинственный лес, для начала нажми ПРОБЕЛ!')
    print('Для перехода к следующему шагу - нажми ПРОБЕЛ!')
    print()
    game(steps, choices, choicesToSteps)
    endTime = datetime.now()
    jsonData = saveToJson(startTime, endTime)
    csvData = saveToCSV(startTime, endTime)
    deleteSave(jsonData, csvData)








