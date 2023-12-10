def check_to_continue():
    while True:
        cont = input("Do you want to continue modify(y/n): ").strip().lower()
        if cont == "y" or cont == "yes":
            return True
        elif cont == "n" or cont == "no":
            return False
        else:
            print("I don`t know what you want, please answer 'y' as 'yes' or 'n' as 'no'\n")


def inputs(prompts: list, types: list, allowed_int_values=None):
    response = list()
    for id, prompt in enumerate(prompts):
        if types[id] == str:
            while True:
                res = input(prompt).strip()
                if not res:
                    print("Your input can`t be empty")
                    continue
                else:
                    response.append(res)
                    break
        else:
            while True:
                try:
                    res = int(input(prompt).strip())
                    if res not in allowed_int_values:
                        print(f"Your input have to be in: {allowed_int_values}")
                    else:
                        response.append(str(res))
                        break
                except ValueError:
                    print("Incorrect input")
            pass
    return response
