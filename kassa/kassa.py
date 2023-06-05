# input_state = input("Введите данные в формате: [Кафе] [Ссылка на кассу] " )
#
# kassa = input_state.split(' ')
#
# if (len(kassa) == 2 and '.iiko.it' in kassa[1]):
#     from configparser import ConfigParser
#
#     config = ConfigParser()
#
#     config.read(".env")
#     name = kassa[0].upper()
#     config["DEFAULT"][name] = "https://" + kassa[1] + ":443"
#
#     with open(".env", 'a') as config_file:
#         config.write(config_file)
# else:
#     print("Исправь ввод и все будет хорошо")
#
#
