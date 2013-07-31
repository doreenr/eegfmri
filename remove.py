
def remove(lister, val):
   return [value for value in lister if value != val]

def remove_range(lister, val):
   return [value for value in lister if value < val]