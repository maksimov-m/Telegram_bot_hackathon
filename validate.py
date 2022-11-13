import datetime


# Если строка с датой является верной то выводим True
# В противном случае False
def isValidate(date : str) -> bool:
    try:
        dt_q = datetime.datetime.strptime(date, "%Y-%m-%d")
        if dt_q > datetime.datetime.now():
            return False
    except ValueError:
        return  False
    return  True


# Если дата в строке указывает на будущее - True
# В противном - False
def isNextDate(date: str) -> bool:
    dt_q = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return datetime.datetime.now() < dt_q


# Если фамилия/имя/отчество не содержит сторонних символов - True
# В противном False
def isValidateLSP(data: str) -> bool:
    return data.isalpha()

# Если номер соответствует
def isValidatPhoneNumber(number : str) -> bool:
    return (len(number) == 11) and number.isdigit()


def isSex(data : str):
    if data.lower() == "муж":
        return "male"
    if data.lower() == "жен":
        return  "female"
    return None