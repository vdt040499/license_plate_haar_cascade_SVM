def check_plate(upper_text, lower_text):
  # Xét điều kiện nửa biển số trên có 4 kí tự, nửa biển số dưới có 4 hoặc 5 kí tự
  if len(upper_text) == 4 and (len(lower_text) == 4 or len(lower_text) == 5):
    # check char at index 2 is character
    if ord(upper_text[2]) > 64 and ord(upper_text[2]) < 91:
      # Xét điều kiện hai kí tự đầu phải là số
      if (ord(upper_text[0]) > 47 and ord(upper_text[0]) < 58) and (ord(upper_text[1]) > 47 and ord(upper_text[1]) < 58):
        return True
  return False

def check_four_chars(lower_text):
  # trường hợp số lượng kí tự nửa biển số dưới bẳng 4
  if len(lower_text) == 4:
    # Xét điều kiện các kí tự ở nửa dưới biển số bắt buộc phải là số
    if (ord(lower_text[0]) > 47 and ord(lower_text[0]) < 58) and (ord(lower_text[1]) > 47 and ord(lower_text[1]) < 58) and (ord(lower_text[2]) > 47 and ord(lower_text[2]) < 58) and (ord(lower_text[3]) > 47 and ord(lower_text[3]) < 58):
      return True
  return False

def check_five_chars(lower_text):
  # trường hợp số lượng kí tự nửa biển số dưới bẳng 5
  if len(lower_text) == 5:
    # Xét điều kiện các kí tự ở nửa dưới biển số bắt buộc phải là số
    if (ord(lower_text[0]) > 47 and ord(lower_text[0]) < 58) and (ord(lower_text[1]) > 47 and ord(lower_text[1]) < 58) and (ord(lower_text[2]) > 47 and ord(lower_text[2]) < 58) and (ord(lower_text[3]) > 47 and ord(lower_text[3]) < 58) and (ord(lower_text[4]) > 47 and ord(lower_text[4]) < 58):
      return True
  return False