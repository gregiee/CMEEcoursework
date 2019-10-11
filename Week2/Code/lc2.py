# Average UK Rainfall (mm) for 1910 by month
# http://www.metoffice.gov.uk/climate/uk/datasets
rainfall = (('JAN',111.4),
            ('FEB',126.1),
            ('MAR', 49.9),
            ('APR', 95.3),
            ('MAY', 71.8),
            ('JUN', 70.2),
            ('JUL', 97.1),
            ('AUG',140.2),
            ('SEP', 27.0),
            ('OCT', 89.4),
            ('NOV',128.4),
            ('DEC',142.2),
           )

# (1) Use a list comprehension to create a list of month,rainfall tuples where
# the amount of rain was greater than 100 mm.
 
# (2) Use a list comprehension to create a list of just month names where the
# amount of rain was less than 50 mm. 

# (3) Now do (1) and (2) using conventional loops (you can choose to do 
# this before 1 and 2 !). 

greaterThan100 = [monthAndRainfall for monthAndRainfall in rainfall if monthAndRainfall[1] > 100]
print(greaterThan100)

monthNamesLessThan50 = [monthAndRainfall[0] for monthAndRainfall in rainfall if monthAndRainfall[1] < 50]
print(monthNamesLessThan50)

greaterThan100 = []
for monthAndRainfall in rainfall:
      if monthAndRainfall[1] > 100:
            greaterThan100.append(monthAndRainfall)
print(greaterThan100)

monthNamesLessThan50 = []
for monthAndRainfall in rainfall:
      if monthAndRainfall[1] <50:
            monthNamesLessThan50.append(monthAndRainfall[0])
print(monthNamesLessThan50)

