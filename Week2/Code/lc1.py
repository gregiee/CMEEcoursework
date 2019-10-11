birds = ( ('Passerculus sandwichensis','Savannah sparrow',18.7),
          ('Delichon urbica','House martin',19),
          ('Junco phaeonotus','Yellow-eyed junco',19.5),
          ('Junco hyemalis','Dark-eyed junco',19.6),
          ('Tachycineata bicolor','Tree swallow',20.2),
         )

#(1) Write three separate list comprehensions that create three different
# lists containing the latin names, common names and mean body masses for
# each species in birds, respectively. 

# (2) Now do the same using conventional loops (you can choose to do this 
# before 1 !). 



latinNames_lc = [bird[0] for bird in birds]
print('latin names: ') 
print(latinNames_lc)

commonNames_lc = [bird[1] for bird in birds]
print('common names: ')
print(commonNames_lc)

bodyMasses_lc = [bird[2] for bird in birds]
print('body masses: ')
print(bodyMasses_lc)


latinNames_loop, commonNames_loop, bodyMasses_loop =  ([] for i in range(3))
for bird in birds:
    latinNames_loop.append(bird[0])
    commonNames_loop.append(bird[1])
    bodyMasses_loop.append(bird[2])
print('latin names: ') 
print(latinNames_loop)
print('common names: ')
print(commonNames_loop)
print('body masses: ')
print(bodyMasses_loop)