bay_list = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
            'A11', 'A12', 'A13']
SPECIFIC_BAY = ''


def location(bay, row):
    sku464 = '464'
    sku444 = '444'
    where =  {'A1' :[ { 1 : [sku464, sku444]}, { 2 : [None, None ]}, { 3 : [None, None ]}],
              'A2' :[ { 1 : [sku464, None]}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A3' :[ { 1 : [None, None]}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A4' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A5' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A6' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A7' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A8' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A9' :[ { 1 : ['L', 'R']}, { 2 : [sku444, 'R' ]}, { 3 : ['L', 'R' ]}],
              'A10' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A11' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A12' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
              'A13' :[ { 1 : ['L', 'R']}, { 2 : ['L', 'R' ]}, { 3 : ['L', 'R' ]}],
}
    if row == 1:
        row = 0
    elif row == 2:
        row = 1
    elif row == 3:
        row = 2
        return(where.get(bay)[row])
    return(where.get(bay)[row])


def sku(product):
    ''' Type product number '464' or '444' without quotes'''
    if product  == '464' or product == '444':
        pallet = product
    return(pallet)


def store():
    #bay = input('Please chose bay: ')
    #row = int(input('Please chose row: '))
    #bay_and_row = location(bay.upper(), row)
    #print('Location:', bay, 'Row:', row, 'contains', bay_and_row.get(row))
    toStore = input('What would you like to store? ')
    COUNTER = 0
    for bays in bay_list:
        
        bay_and_row = location(bays, COUNTER)
        
        print(location(bays, COUNTER))
        
    
    #print(bay_and_row)
    #print(bay_and_row.get(row)[0])
    #print(bay_and_row.get(row))
    #indexing = bay_and_row.get(row).index(toStore)
    
    #if None in bay_and_row.get(COUNTER) or None in bay_and_row.get(COUNTER):
#        bay_and_row.get(COUNTER).pop(indexing)
#        bay_and_row.get(COUNTER).insert(indexing, toStore)
#        print(bay_and_row.get(COUNTER))
            
#    else:
#        print('There is no room here')


def retrieve():
    bay = input('Please chose bay: ')
    row = int(input('Please chose row: '))
    bay_and_row = location(bay.upper(), row)
    print('Location:', bay.upper(), 'Row:', row, 'contains', bay_and_row.get(row))

    toRetrieve = input('What would you like to retrieve?: ')
    
    if toRetrieve == bay_and_row.get(row)[0] or toRetrieve == bay_and_row.get(row)[1]:
        indexing = bay_and_row.get(row).index(toRetrieve)
        del bay_and_row.get(row)[indexing]
        bay_and_row.get(row).insert(indexing, None)

        print(indexing)
        print(bay_and_row.get(row))
    

