def read_txt(txt_path):

    with open(txt_path,'r', encoding='utf-8') as file:

        parameters = {}
        for line in file:
            
            parts = line.strip().split(' ')

            if len(parts) == 2:
                key = parts[0]
                value = parts[1].strip('"')
                parameters[key] = value

        
    return(parameters)