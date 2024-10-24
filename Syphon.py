import sys

def invalid_name(item, item_class):
    for i in item:
        if not i in "ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz_":
            if item[0] in "1234567890":
                raise NameError(f"Invalid Name for '{item}' {item_class}")
                
def is_this_variable_defined(list1, text):
    text = text.strip().split(" ")
    for item1 in list1:
        if item1[:-1] == text[0]:
            return [item1[:-1], "YES"]
        elif item1[:-1]+"&" == text[0]:
            return [item1[:-1], "IMMUTABLE"]
    return None

def variable_operation(list1, text):
    text = text.split()
    for i in list1:
        i = i.strip()
        if len(text) > 2:
            if text[1] == '+=':
                return ["Addition", i, text[2]]
            if text[1] == '-=':
                return ["Subtraction", i, text[2]]
            if text[1] == '*=':
                return ["Multiplication", i, text[2]]
            if text[1] == '/=':
                return ["Division", i, text[2]]
            if text[0] in list1:
                return ["Variable Reassignment", i, text[2]]
        if text[0][-3:] == '++;':
            return ["Increment Operator", text[0][:-3]]
        if text[0][-3:] == '--;':
            return ["Decrement Operator", text[0][:-3]]
        if text[0].strip() == '}':
            return ["End of file", i]
        if i == text[0] or i == text[1]:
            return ["Variable Reassignment", i]
    return ["Unknown Error"]
                
def syphon_interpreter(filename, tokens):
    with open(filename + '.py', 'w') as file:
        indents = 0
        for index, token in enumerate(tokens):
            if token == "FUNCTION:":
                indents += 1
                func = tokens.index('FUNCTION:')
                tokens[func + 2] = tokens[func + 2][1:-1]
                file.write(f'def {tokens[func + 1]}(')
                tokens[func + 2] = tokens[func + 2].split(',')
                if tokens[func + 2][0] == tokens[func + 2][-1] and tokens[func + 2][0] != 'NO PARAMS':
                    param = str(tokens[func + 2])[2:-2].split(' ')
                    if param != ['']:
                        default_value = "NONE"
                        for i in tokens[func + 2]:
                            if '=' in i:
                                default_value = i[i.index('=') + 1]
                        if default_value != "NONE":
                            file.write(f'{param[1]}: {param[0]} = {default_value}')
                        else:
                            file.write(f'{param[1]}: {param[0]}')
                elif tokens[func + 2][0] == 'NO PARAMS':
                    pass
                    # No parameters, no write
                else:
                    for i in tokens[func + 2]:
                        i = i.split(' ')
                        if i[0] == '':
                            i = i[1:]
                        if i == tokens[func + 2][-1].split(' ')[1:]:
                            if '=' in i:
                                default_value = i[i.index('=') + 1]
                                file.write(f'{i[1]}: {i[i.index(i[1]) - 1]} = {default_value}')
                            else:
                                file.write(f'{i[1]}: {i[i.index(i[1]) - 1]}')
                        else:
                            if '=' in i:
                                try:
                                    defualt_value = i[i.index('=') + 1]
                                    file.write(f'{i[1]}: {i[i.index(i[1]) - 1]} = {defualt_value}, ')
                                except:
                                    raise SyntaxError("Missing/Unknown Parameter Type")
                            else:
                                try:
                                    file.write(f'{i[1]}: {i[i.index(i[1]) - 1]}, ')
                                except:
                                    raise SyntaxError("Missing/Unknown Parameter Type")
                file.write(f') -> {tokens[func + 3]}:\n')
            if token == "FOR LOOP:":
                indents += 1
                tokens[index + 1] = tokens[index + 1][1:-1].split(';')
                conditional = []
                for i in tokens[index + 1]:
                    i = i.strip()
                    conditional.append(i)
                type_, var = conditional[0].split(' ')
                if type_ == 'int':
                    default_value = 0
                elif type_ == 'str':
                    default_value = "''"
                elif type_ == 'float':
                    default_value = 0.0
                elif type_ == 'bool':
                    default_value = False
                elif type_ == 'array':
                    default_value = "[]"
                if conditional[2][1:] == '++':
                    conditional[2] = conditional[2][:1]+' += 1'
                    I_coded_this_weird = "+ 1"
                elif conditional[2][1:] == '--':
                    conditional[2] = conditional[2][:1]+' -= 1'
                    I_coded_this_weird = "- 1"
                if conditional[1][4:8] == 'len(':
                    if conditional[1][8] == '&':
                        conditional[1] = conditional[1][:8]+conditional[1][9:-1].upper()+')'
                file.write('\t'*(indents-1)+f'{var} = {default_value}\n')
                file.write('\t'*(indents-1)+f'while {conditional[1]} {I_coded_this_weird}:\n')

                file.write('\t'*indents+f'{conditional[2]}\n')
            if token == "FOREACH LOOP:":
                indents += 1
                if tokens[index+3][0] == '&':
                    tokens[index+3] = tokens[index+3][1:].upper()
                file.write('\t'*(indents-1)+f"for {tokens[index+2]} in {tokens[index+3]}:\n")
            if token == "WHILE LOOP:":
                indents += 1
                file.write('\t'*(indents-1)+f'while {tokens[index+1][1:-1].strip()}:\n')
            if token == "IF STATEMENT:":
                indents += 1
                file.write('\t'*(indents-1)+f'if {tokens[index+1]}:\n')
            if token == "ELIF STATEMENT:":
                file.write('\t'*(indents-1)+f'elif {tokens[index + 1]}:\n')
            if token == "ELSE STATEMENT:":
                file.write('\t'*(indents-1)+'else:\n')
            if token == "VARIABLE:":
                var = index
                if tokens[var + 4][0] == '&':
                    tokens[var + 4] = tokens[var + 4][1:].upper()
                if 'console.print' in tokens[var + 4]:
                    raise ValueError("Variables cant be set to 'print' yet lol")
                if tokens[var + 2] == "IMMUTABLE":
                    tokens[var + 3] = tokens[var + 3].upper()
                if tokens[var + 1] == "ARRAY":
                    tokens[var + 1] = "ANY"
                tokens[var + 3] = f"{tokens[var + 3]}: {tokens[var + 1].lower()}"
                if tokens[var + 4] == "DECLARED":
                    if tokens[var + 1] == "INT":
                        file.write('\t'*indents+f"{tokens[var + 3]} = 0\n")
                    elif tokens[var + 1] == "STR":
                        file.write('\t'*indents+f"{tokens[var + 3]} = ''\n")
                    elif tokens[var + 1] == "FLOAT":
                        file.write('\t'*indents+f"{tokens[var + 3]} = 0.0\n")
                    elif tokens[var + 1] == "BOOL":
                        file.write('\t'*indents+f"{tokens[var + 3]} = False\n")
                    elif tokens[var + 1] == "ARRAY":
                        file.write('\t'*indents+f"{tokens[var + 3]} = []\n")
                elif tokens[var + 4][:6] == 'input(':
                    if tokens[var + 1] == "INT":
                        file.write('\t'*indents+f"{tokens[var + 3]} = int(input({tokens[var + 4][6:]})\n")
                    elif tokens[var + 1] == "STR":
                        file.write('\t'*indents+f"{tokens[var + 3]} = input{tokens[var + 4][16:]}\n")
                    elif tokens[var + 1] == "FLOAT":
                        file.write('\t'*indents+f"{tokens[var + 3]} = float(input{tokens[var + 4][16:]})\n")
                    elif tokens[var + 1] == "BOOL":
                        file.write('\t'*indents+f"{tokens[var + 3]} = bool(input{tokens[var + 4][16:]})\n")
                    elif tokens[var + 1] == "ARRAY":
                        file.write('\t'*indents+f"{tokens[var + 3]} = input({tokens[var + 3]}).split(' ')")
                else:
                    file.write('\t'*indents+f"{tokens[var + 3]} = {tokens[var + 4]}\n")
            if token == "END":
                indents -= 1
                #tokens = tokens[tokens.index("END") + 1:]
            if token == 'RETURN:' and indents > 0:
                if tokens[index + 1] == 'INPUT:':
                    file.write('\t'*indents+f'return (input({tokens[index + 2]}))\n')
                else:
                    file.write('\t'*indents+'return '+tokens[index + 1]+'\n')
            if token == 'INPUT:' and tokens[index - 1] != 'RETURN:':
                file.write('\t'*indents+f'input({tokens[index + 1]})\n')
            if token == 'APPEND:':
                file.write('\t'*indents+tokens[index + 1]+'\n')
            if token == 'PRINT:':
                file.write('\t'*indents+f'print({tokens[index + 1]})\n')
            if token == '\n':
                file.write(token)
            if token == 'FUNCTION CALL:':
                func_name = tokens[index+1]
                call_value = tokens[index+2]
                if call_value[1] == "&":
                    call_value = f"({call_value[2:-1].upper()})"
                file.write('\t'*indents+func_name+' = '+func_name+call_value+'\n')
            if token == 'COMMENT:':
                comment = tokens[tokens.index(token)+1]
                file.write('\t'*indents+"#"+comment)
            if token == 'MULTI-LINE COMMENT:' or token == 'MULTI-LINE END':
                file.write('"""\n')
            # "Oh why have 2 types of token that do the same thing??" -You probably
            # DEBUGGING PURPOSEESEFEJFOIWJEF OWIEJFOIWJE OIJWFJ
            if token == "VAR REASSIGNMENT:":
                file.write('\t'*indents+tokens[index + 1]+" = "+tokens[index + 2]+'\n')
            if token == "INCREMENT OPERATOR:":
                current_line = tokens.index(token)
                file.write('\t'*indents+tokens[current_line + 1]+" += 1\n")
            if token == "DECREMENT OPERATOR:":
                current_line = tokens.index(token)
                file.write('\t'*indents+tokens[current_line + 1]+" -= 1\n")
            if token == "ADDITION:":
                current_line = tokens.index(token)
                file.write('\t'*indents+tokens[current_line + 1]+" += "+tokens[current_line + 2]+"\n")
            if token == "SUBTRACTION:":
                current_line = tokens.index(token)
                file.write('\t'*indents+tokens[current_line + 1]+" -= "+tokens[current_line + 2]+"\n")
            if token == "MULTIPLICATION:":
                current_line = tokens.index(token)
                file.write('\t'*indents+tokens[current_line + 1]+" *= "+tokens[current_line + 2]+"\n")
            if token == "DIVISION:":
                current_line = tokens.index(token)
                file.write('\t'*indents+tokens[current_line + 1]+" /= "+tokens[current_line + 2]+"\n")
    file.close()

def syphon_tokenizer(filepath, mode=''):
    if not filepath[-4:] == '.syp':
        raise NameError("File Extension is incorrect, Syphon uses '.syp'")
    with open(filepath, "r") as file:
        variables = []
        supported_variable_types = ['int ', 'str ', 'float ', 'bool ', 'array ']
        tokens = []
        Function = False
        for index, line in enumerate(file):
            for_loop_result = is_this_variable_defined(supported_variable_types, line)
            if 'fn ' in line:
                try:
                    func_type, func_name = line[line.index('fn ') + 3:line.index('(')].strip().split(' ')
                except:
                    raise SyntaxError("Function Syntax in Syphon is 'fn [return type] [function name] ([parameters]) {[logic]}'")
                invalid_name(func_name, 'Function')
                func_params = line[line.index('('):line.index('{')].strip()
                invalid_name(func_params, 'Function Parameters')
                tokens.append(f'FUNCTION:')
                tokens.append(func_name)
                if func_params.split() != ['()']:
                    for i in func_params[1:-1].split(','):
                        type_, var = i.split(' ')
                        variables.append(var)
                        variables.append(type_)
                    tokens.append(func_params)
                else:
                    tokens.append('.NO PARAMS.')
                tokens.append(func_type)
                Function = True
            
            elif 'elif (' in line:
                tokens.append('ELIF STATEMENT:')
                if not 'IF STATEMENT:' in tokens:
                    raise SyntaxError("ELIF Statement must follow an IF Statement!")
                if line[line.index('{') - 1] == ')':
                    statement = line[line.index('if (') + 4:line.index('{') - 1]
                else:
                    statement = line[line.index('if (') + 4:line.index('{') - 2]
                statement = statement.strip()
                if statement[0] == "&":
                    statement = statement[1:].upper()
                tokens.append(statement)
                
            elif 'if (' in line:
                tokens.append('IF STATEMENT:')
                if line[line.index('{') - 1] == ')':
                    statement = line[line.index('if (') + 4:line.index('{') - 1]
                else:
                    statement = line[line.index('if (') + 4:line.index('{') - 2]
                statement = statement.strip()
                if statement[0] == "&":
                    statement = statement[1:].upper()
                tokens.append(statement)
                
            elif '} else {' in line:
                tokens.append('ELSE STATEMENT:')
                    
            elif 'for (' in line:
                tokens.append('FOR LOOP:')
                conditional = line[line.index('for (')+4:line.index('{')].strip()
                tokens.append(conditional)
            
            elif 'foreach (' in line:
                tokens.append('FOREACH LOOP:')
                stuff = line[line.index('foreach (')+8:line.index('{')].strip()
                # print(stuff[1:-1].split('; '))
                var, iterable = stuff[1:-1].split('; ')
                tokens.append(var.split(' ')[0])
                tokens.append(var.split(' ')[1])
                variables.append(var.split(' ')[1])
                variables.append(var.split(' ')[0])
                tokens.append(iterable)
            
            elif 'while (' in line:
                tokens.append('WHILE LOOP:')
                conditional = line[line.index('while (')+6:line.index('{')].strip()
                comparator_list = ['=', '!']
                conditional_list = ['(']
                index = ''
                for idx, part in enumerate(conditional[1:-1].split('=')):
                    part = part.strip()
                    if part[-1] in comparator_list:
                        index = comparator_list[comparator_list.index(part[-1])]
                        part = part[:-1]
                        part = part.strip()
                    if part[0] == '&':
                        part = part[1:].upper()
                    if not part == conditional[1:-1].split('=')[-1].strip():
                        part = part+' '
                    conditional_list.append(part)
                conditional_list.insert(2, index+'= ')
                conditional_list.append(f'{conditional_list[-1].strip()})')
                conditional_list.pop(-2)
                conditional_list = ''.join(conditional_list)
                tokens.append(conditional_list)
                    
            elif 'call' in line:
                func_name = line[line.index('call ') + 4:line.index('(')].strip()
                invalid_name(func_name, 'Function Call (Unknown Function Name)')
                func_params = line[line.index('('):line.index(')') + 1].strip()
                tokens.append("FUNCTION CALL:")
                tokens.append(func_name)
                tokens.append(func_params)
                func_name_is_defined = False
                for indx, tkns in enumerate(tokens):
                    if tkns == 'FUNCTION:' and tokens[indx + 1] == func_name:
                        func_type = tokens[indx + 3]
                        func_name_is_defined = True
                if func_name_is_defined:
                    variables.append(func_name)
                else:
                    raise NameError(f'Function \'{func_name}\' is undefined!')
                variables.append(func_type)
                    
            # Variables
            elif type(for_loop_result).__name__ == "list":
                tokens.append("VARIABLE:")
                if "=" in line:
                    var_name, var_value = line[line.index(for_loop_result[0]):].split("=")
                    name = var_name.split(" ")
                    var_type = for_loop_result[0].strip()
                    var_value = var_value.strip()
                        
                    if var_value in variables or '&'+var_value in variables:
                        if '&'+var_value in variables:
                            new_var_value = '&'+var_value
                            var_value = var_value.upper()
                        if variables[variables.index(new_var_value) + 1] != var_type.upper():
                            raise ValueError("Variable set to variable of different type")
                            
                        elif name[1] in variables:
                            raise SyntaxError(f"Variable '{name[1]}' is already defined")
                            
                        elif var_type == "int":
                            for char in var_value:
                                if not char in "1234567890":
                                    raise ValueError("Type 'int' variable set to incorrect type")
                                        
                        elif var_type == "float":
                            for char in var_value:
                                if not char in "1234567890.":
                                    raise ValueError("Type 'float' variable is set to an incorrect type")
                                    
                            try:
                                if not var_value.index('.') < len(var_value):
                                    raise ValueError("Type 'float' variable is set to an incorrect type")
                            except:
                                raise ValueError("Type 'float' variable is set to an invalid type")
                            
                        elif var_type == "bool":
                            if var_value != "True" and    var_value != 'False':
                                raise ValueError("Type 'bool' variable is set to an incorrect type")
                        
                        elif var_type == "array":
                            if not '[' in var_value and not ']' in var_value:
                                raise ValueError("Type 'array' variable is set to an incorrect type")
                                
                    tokens.append(var_type.upper())
                    if name[0][-1] == "&":
                        tokens.append("IMMUTABLE")
                        variables.append("&"+name[1])
                    else:
                        tokens.append("MUTABLE")
                        variables.append(name[1])
                    tokens.append(name[1])
                    variables.append(var_type.upper())
                    tokens.append(var_value.strip())
                else:
                    var_name = line[line.index(for_loop_result[0]):]
                    name = var_name.split(" ")
                    if name[0][-1] == "&":
                        raise SyntaxError("Immutable Variables must be declared with a value")
                    var_type = for_loop_result[0].strip()
                    tokens.append(var_type.upper())
                    tokens.append("MUTABLE")
                    tokens.append(name[1].strip()[:-1])
                    tokens.append("DECLARED")
                    variables.append(name[1][:-1])
                    variables.append(var_type.upper())
                    
            elif '} ' in line or '}\n' in line:
                line = line.strip()
                tokens.append("END")
                    
            elif line == "\n":
                tokens.append('\n')
                # Whitespace
                
            elif line == '++':
                pass
                
            elif 'return' in line:
                line = line.strip()
                try:
                    output = line[line.index('(') + 1:-1]
                except:
                    raise SyntaxError("Missing Parentheses around return value")
                tokens.append('RETURN:')
                if 'console.readline' in output:
                    tokens.append('INPUT:')
                    output = output[output.index('(') + 1:-1]
                tokens.append(output)
                    
            elif 'console.readline' in line and not '=' in line:
                for i in line.split(' '):
                    if i in variables:
                        pass 
                    # SHOULD NOT RUN vvv
                line = line.strip()
                tokens.append('INPUT:')
                func_input = line[index + 9:-1]
                tokens.append(func_input)
                
            elif 'console.print' in line:
                line = line.strip()
                tokens.append('PRINT:')
                func_input = line[line.index('print') + 6:-1]
                func_input = func_input.split(' ')
                if func_input[0][0] == '&':
                    func_input[0] = func_input[0][1:].upper()
                func_input = ' '.join(func_input)
                tokens.append(func_input)
                    
            elif '//' in line:
                tokens.append('COMMENT:')
                tokens.append(line[2:])
            
            elif '/*' in line:
                tokens.append('MULTI-LINE COMMENT:')
            
            elif '*/' in line:
                tokens.append('MULTI-LINE END')
                
            elif '.append' in line:
                tokens.append('APPEND:')
                tokens.append(line.strip())
                    
            # When adding more stuff add it above this;
            # These are the blackhole statements vvv
            elif variable_operation(variables, line)[0] == "Unknown Error":
                raise NameError(f"Variable '{line.split()[0]}' is undefined")
            
            elif variable_operation(variables, line)[0] == "Variable Reassignment":
                if line.split()[0] == 'int':
                    line = line.split()[1:]
                    line = ' '.join(line)
                if line.split()[2][:16] == 'console.readline':
                    var_value = 'input'+line[line.index('readline(')+8:-1]
                else:
                    var_value = line.split('=')[-1].strip()
                tokens.append("VAR REASSIGNMENT:")
                if variable_operation(variables, line)[-1][0] == '&':
                    raise SyntaxError("Immutable value cannot be reassigned")
                tokens.append(variable_operation(variables, line)[-1])
                tokens.append(var_value)
                    
            elif variable_operation(variables, line)[0] == "Increment Operator":
                tokens.append("INCREMENT OPERATOR:")
                name = variable_operation(variables, line)[1]
                if name[-1] == ';':
                    name = name[:-1]
                if name[0] == '&':
                    raise SyntaxError("Immutable value cannot be incremented")
                tokens.append(name)
                        
            elif variable_operation(variables, line)[0] == "Decrement Operator":
                tokens.append("DECREMENT OPERATOR:")
                name = variable_operation(variables, line)[1]
                if name[0] == '&':
                    raise SyntaxError("Immutable value cannot be decremented")
                tokens.append(name)
                    
            elif variable_operation(variables, line)[0] == "Addition":
                tokens.append("ADDITION:")
                name = variable_operation(variables, line)[1]
                if name[0] == '&':
                    raise SyntaxError("Immutable values cannot be changed")
                tokens.append(name)
                value_added = "".join(line).split()[-1]
                try:
                    is_this_variable_defined_ = variables[variables.index(value_added)]
                except:
                    raise SyntaxError(f"Variable '{value_added}' is undefined")
                if value_added[0] == "&":
                    value_added = value_added[1:].upper()
                else:
                    value_added = value_added.lower()
                tokens.append(value_added)
                    
            elif variable_operation(variables, line)[0] == "Subtraction":
                tokens.append("SUBTRACTION:")
                name = variable_operation(variables, line)[1]
                if name[0] == '&':
                    raise SyntaxError("Immutable values cannot be changed")
                tokens.append(name)
                value_added = "".join(line).split()[-1]
                try:
                    is_this_variable_defined_ = variables[variables.index(value_added)]
                except:
                    raise SyntaxError(f"Variable '{value_added}' is undefined")
                if value_added[0] == "&":
                    value_added = value_added[1:].upper()
                else:
                    value_added = value_added.lower()
                tokens.append(value_added)
                
            elif variable_operation(variables, line)[0] == "Multiplication":
                tokens.append("MULTIPLICATION:")
                name = variable_operation(variables, line)[1]
                if name[0] == '&':
                    raise SyntaxError("Immutable values cannot be changed")
                tokens.append(name)
                value_added = "".join(line).split()[-1]
                for i in value_added: 
                    if not i in '1234567890':
                        try:
                            is_this_variable_defined_ = variables[variables.index(value_added)]
                        except:
                            raise SyntaxError(f"Variable '{value_added}' is undefined")
                if value_added[0] == "&":
                    value_added = value_added[1:].upper()
                else:
                    value_added = value_added.lower()
                tokens.append(value_added)
                
            elif variable_operation(variables, line)[0] == "Division":
                tokens.append("DIVISION:")
                name = variable_operation(variables, line)[1]
                if name[0] == '&':
                    raise SyntaxError("Immutable values cannot be changed")
                tokens.append(name)
                value_added = "".join(line).split()[-1]
                try:
                    is_this_variable_defined_ = variables[variables.index(value_added)]
                except:
                    raise SyntaxError(f"Variable '{value_added}' is undefined")
                if value_added[0] == "&":
                    value_added = value_added[1:].upper()
                else:
                    value_added = value_added.lower()
                tokens.append(value_added)
                        
        file.close()
        #print(variables)
        #print(tokens)
        syphon_interpreter(filepath[:-4], tokens)

syphon_tokenizer(str(sys.argv[1:])[2:-2])
