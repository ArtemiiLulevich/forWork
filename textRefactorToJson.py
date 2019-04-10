while True:
    print("""
This program quotes strings for further use in requests to the API

Select file location:
1) By absolute path
2) In same folder
0) To exit""")

    selection = input()

    if selection == '1':
        path = input("Enter absolute path: ")
    elif selection == '2':
        path = input("Enter file name: ").lower()
        if path.endswith('.txt') is not True:# add file format if user doesn't enter it
            path += '.txt'
    else:
        break
    
    new_file_name = input("Enter new file name: ").lower()

    if new_file_name.endswith('.txt') is not True:# add file format if user doesn't enter it
            new_file_name += '.txt'
    barcodes = list()

    with open(path, 'r') as file_barcode:
        for line in file_barcode:
            barcodes.append(line.strip('\n"!#$%^&*()')) # delete simbols: \n"!#$%^&*() from start end end of a string

    for x in range(len(barcodes)):
        if x == len(barcodes)-1:
            ref_barcode = '"' + barcodes[x] + '"'
        else:
            ref_barcode = '"' + barcodes[x] + '",'
        
        barcodes[x] = ref_barcode
        #print(ref_barcode)

    with open(new_file_name, 'w') as ref_file_barcodes:
        for x in range(len(barcodes)):
            print(barcodes[x], file=ref_file_barcodes)

    print("File {} created.".format(new_file_name))
    print()
