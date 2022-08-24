import random
import configparser


Config = configparser.ConfigParser()
Config.read("Modules\\Date\\Set.ini")


number_list = "01234567890"
letter_list = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
symbol_list = "`-=,./;'\[]~!@#$%^&*()_+{}:\"|<>?"


def Make():
    choose_list = ""
    long = int(Config.get("Password-Format", "password_long"))
    answer = ""
    if int(Config.get("Password-Format", "password_with_number")) == 1:
        choose_list += number_list

    if int(Config.get("Password-Format", "password_with_letter")) == 1:
        choose_list += letter_list

    if int(Config.get("Password-Format", "password_with_symbol")) == 1:
        choose_list += symbol_list

    if int(Config.get("Password-Format", "password_with_symbol_underline_start")) == 1:
        long -= 1
        answer += "_"

    if int(Config.get("Password-Format", "password_with_symbol_underline_finish")) == 1:
        long -= 1

    for i in range(0, long):
        answer += choose_list[random.randint(0, len(choose_list) - 1)]
        print(answer)

    if int(Config.get("Password-Format", "password_with_symbol_underline_finish")) == 1:
        answer += "_"
        print(answer)

    return answer


if __name__ == "__main__":
    print(Make())
