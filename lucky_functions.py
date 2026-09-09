#lucky_functions.py
def calculate_lucky_name(name):
    sum_result_name = 0
    for char in name:
        if char.isalpha():
          sum_result_name += (ord(char) - ord('a') + 1)

    while sum_result_name > 9:
        name = str(sum_result_name)
        sum_result_name = 0

        for char in name:
          if char.isdigit():
            sum_result_name += (ord(char) - ord('0'))
    return sum_result_name

def calculate_lucky_bday(bday):
    sum_result_bday = 0
    for char in bday:
       if char.isdigit():
         sum_result_bday += (ord(char) - ord('0'))

    while sum_result_bday > 9:
      bday_num = str(sum_result_bday)
      sum_result_bday = 0

      for char in bday_num:
       if char.isdigit():
         sum_result_bday += (ord(char) - ord('0'))
    return sum_result_bday