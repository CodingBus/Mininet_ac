"""
Hardcoded AC table to return whether or not a user is allowed to access a file.
"""

import datetime

ac_table = {("00:00:00:00:00:01", "00:00:00:00:00:02"): (6, 22),
            ("00:00:00:00:00:01", "00:00:00:00:00:04"): (12, 18),
            ("00:00:00:00:00:03", "00:00:00:00:00:02"): (0, 0),
            ("00:00:00:00:00:03", "00:00:00:00:00:04"): (0, 0)}

# Arguments are the hours of valid access. True if access granted
def getAccess(start, end):
  # Always have access
  if (start == 0 and end == 0):
    return True
  now = datetime.datetime.now()
  today_start = now.replace(hour=start, minute=0, second=0, microsecond=0)
  today_end = now.replace(hour=end, minute=0, second=0, microsecond=0)
  return today_start < now < today_end

def main():
  start, end = ac_table[("00:00:00:00:00:03", "00:00:00:00:00:04")]
  print(getAccess(start, end))
  print(datetime.datetime.now())
  return

if __name__ == "__main__":
  main()
