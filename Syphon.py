import sys

def invalid_name(item, item_class):
    for i in item:
        if not i in "ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz_":
            if item[0] in "1234567890":
                raise NameError(f"Invalid Name for '{item}' {item_class}")
                
def for_loop_but_a_function(list1, text):
    text = text.split(" ")
    for item1 in list1:
        if item1[:-1] == text[0]:
            return [item1[:-1], "YES"]
        elif item1[:-1]+"&" == text[0]:
            return [item1[:-1], "IMMUTABLE"]
    return None
    
def for_loop(list1, text):
    text = text.split()
    for i in list1:
        if len(text) > 2:
            if text[1] == '+=':
                return ["Addition", i, text[2]]
            if text[1] == '-=':
                return ["Subtraction", i, text[2]]
        if i == text[0]:
            return ["Variable Reassignment", i]
        if text[0][-3:] == '++;':
            return ["Increment Operator", i]
        elif text[0][-3:] == '--;':
            return ["Decrement Operator", i]
    return ["Unknown Error"]
                
def syphon_interpreter(filename, tokens):
    file = open(filename + '.py', 'w')
    indents = 0
    for index, token in enumerate(tokens):
        if token == "FUNCTION:":
            indents += 1
            func = tokens.index('FUNCTION:')
            tokens[func + 2] = tokens[func + 2][1:-1]
            file.write(f'def {tokens[func + 1]}(')
            tokens[func + 2] = tokens[func + 2].split(',')
            if tokens[func + 2][0] == tokens[func + 2][-1]:
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
            pos = tokens.index('FOR LOOP:')
            tokens[pos + 1] = tokens[pos + 1][1:-1].split(';')
            conditional = []
            for i in tokens[pos + 1]:
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
            file.write('\t'*(indents-1)+f'{var} = {default_value}\n')
            file.write('\t'*(indents-1)+f'while {conditional[1]}:\n')
            if conditional[2][1:] == '++':
                conditional[2] = conditional[2][:1]+' += 1'
            elif conditional[2][1:] == '--':
                conditional[2] = conditional[2][:1]+' -= 1'
            file.write('\t'*indents+f'{conditional[2]}\n')
        if token == "IF STATEMENT:":
            indents += 1
            pos = tokens.index('IF STATEMENT:')
            file.write('\t'*(indents-1)+f'if {tokens[pos +1]}:\n')
        if token == "VARIABLE:":
            var = tokens.index('VARIABLE:')
            if tokens[var + 4][0] == '&':
                tokens[var + 4] = tokens[var + 4][1:].upper()
            if 'console.print' in tokens[var + 4]:
                raise ValueError("Variables cant be set to 'print' yet lol")
            if tokens[var + 2] == "IMMUTABLE":
                tokens[var + 3] = tokens[var + 3].upper()
            elif tokens [var + 2] == "MUTABLE":
                tokens[var + 3] = tokens[var + 3]
            if tokens[var + 4] == "DECLARED":
                if tokens[var + 1] == "INT":
                    file.write(f"{tokens[var + 3]} = 0\n")
                elif tokens[var + 1] == "STR":
                    file.write(f"{tokens[var + 3]} = ''\n")
                elif tokens[var + 1] == "FLOAT":
                    file.write(f"{tokens[var + 3]} = 0.0\n")
                elif tokens[var + 1] == "BOOL":
                    file.write(f"{tokens[var + 3]} = False\n")
                elif tokens[var + 1] == "ARRAY":
                    file.write(f"{tokens[var + 3]} = []\n")
            elif tokens[var + 4][:16] == 'console.readline':
                if tokens[var + 1] == "INT":
                    file.write(f"{tokens[var + 3]} = int(input{tokens[var + 4][16:]})\n")
                elif tokens[var + 1] == "STR":
                    file.write(f"{tokens[var + 3]} = input{tokens[var + 4][16:]}\n")
                elif tokens[var + 1] == "FLOAT":
                    file.write(f"{tokens[var + 3]} = float(input{tokens[var + 4][16:]})\n")
                elif tokens[var + 1] == "BOOL":
                    file.write(f"{tokens[var + 3]} = bool(input{tokens[var + 4][16:]})\n")
            else:
                file.write(f"{tokens[var + 3]} = {tokens[var + 4]}\n")
            tokens.pop(var)
        if token == "END":
            indents -= 1
            tokens = tokens[tokens.index("END") + 1:]
        if 'return' in token and indents > 0:
            file.write('\t'*indents+token+'\n\n')
        if token == '\n':
            file.write(token)
        if 'console.print' in token:
            current_line = tokens[tokens.index(token)]
            if current_line[current_line.index(")")] == current_line[-1]:
                file.write('\t'*indents+f'print{current_line[current_line.index("(") : current_line.index(")")+1]}\n')

            elif current_line[current_line.index(")") + 1] == ")":
                file.write('\t'*indents+f'print{current_line[current_line.index("(") : current_line.index(")")+1]})\n')
        if 'console.readline' in token and tokens[tokens.index(token) -2][-1] != "E":
            current_line = tokens[tokens.index(token)]
            file.write('\t'*indents+f'input{current_line[current_line.index("(") : current_line.index(")")+1]}\n')
        if token == 'FUNCTION CALL:':
            func_name = tokens[tokens.index(token)+1]
            call_value = tokens[tokens.index(token)+2]
            if call_value[1] == "&":
                call_value = f"({call_value[2:-1].upper()})"
            file.write('\t'*indents+func_name+call_value+'\n\n')
        if token == 'COMMENT:':
            comment = tokens[tokens.index(token)+1]
            file.write('\t'*indents+"#"+comment)
        if token == "VAR REASSIGNMENT:":
            current_line = tokens.index(token)
            file.write('\t'*indents+tokens[current_line + 1]+" = "+tokens[current_line + 2]+'\n')
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
    file.close()

def syphon_tokenizer(filepath):
    filepath = filepath[2:-2]   # Removes Brackets + Single Quotes
    if not filepath[-4:] == '.syp':
        raise NameError("File Extension is incorrect, Syphon uses '.syp'")
    file = open(filepath, "r")
    variables = []
    supported_variable_types = ['int ', 'str ', 'float ', 'bool ', 'array ']
    tokens = []
    Function = False
    for index, line in enumerate(file):
        for_loop_result = for_loop_but_a_function(supported_variable_types, line)
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
            tokens.append(func_params)
            tokens.append(func_type)
            Function = True
            
        elif 'if (' in line:
            tokens.append('IF STATEMENT:')
            if line[line.index('{') - 1] == ')':
                statement = line[line.index('if (') + 4:line.index('{') - 1]
            else:
                statement = line[line.index('if (') + 4:line.index('{') - 2]
            tokens.append(statement)
            
        elif 'for (' in line:
            tokens.append('FOR LOOP:')
            conditional = line[line.index('for (')+4:line.index('{')].strip()
            tokens.append(conditional)
            
        elif 'call' in line:
            func_name = line[line.index('call ') + 4:line.index('(')].strip()
            invalid_name(func_name, 'Function Call (Unknown Function Name)')
            func_params = line[line.index('('):line.index(')') + 1].strip()
            tokens.append("FUNCTION CALL:")
            tokens.append(func_name)
            tokens.append(func_params)
            
        # Variables
        elif type(for_loop_result).__name__ == "list":
            tokens.append("VARIABLE:")
            if "=" in line:
                var_name, var_value = line[line.index(for_loop_result[0]):].split("=")
                name = var_name.split(" ")
                var_type = for_loop_result[0].strip()
                var_value = var_value.strip()
                if 'console.readline' in var_value:
                    pass
                
                elif var_value in variables:
                    if variables[variables.index(var_value) + 1] != var_type.upper():
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
                            if not var_value.index('.') > 0 and not var_value.index('.') < len(var_value):
                                raise ValueError("Type 'float' variable is set to an incorrect type")
                        except:
                            raise ValueError("Type 'float' variable is set to an invalid type")
                    
                elif var_type == "bool":
                    if var_value != "True" and var_value != 'False':
                        raise ValueError("Type 'bool' variable is set to an incorrect type")
                        
                elif var_type == "array":
                    if var_value[0] != "[" and var_value[-1] != "]":
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
            
            
        elif '}' in line:
            line = line.strip()
            tokens.append("END")
            
        elif line == "\n":
            tokens.append('\n')
            # Whitespace
        
        elif line == '++':
            pass
            
        elif 'console.readline' in line or 'console.print' in line or 'return' in line:
            line = line.strip()
            tokens.append(line)
            
        elif '//' in line:
            tokens.append('COMMENT:')
            tokens.append(line[2:])
            
        # When adding more stuff add it above this;
        # These are the blackhole statements vvv
        elif for_loop(variables, line)[0] == "Unknown Error":
            raise NameError(f"Variable '{line.split()[0]}' is undefined")
            
        elif for_loop(variables, line)[0] == "Variable Reassignment":
            var_value = "".join(line).split()[-1]
            tokens.append("VAR REASSIGNMENT:")
            if for_loop(variables, line)[-1][0] == '&':
                raise SyntaxError("Immutable value cannot be reassigned")
            tokens.append(for_loop(variables, line)[-1])
            tokens.append(var_value)
            
        elif for_loop(variables, line)[0] == "Increment Operator":
            tokens.append("INCREMENT OPERATOR:")
            name = for_loop(variables, line)[1]
            if name[0] == '&':
                raise SyntaxError("Immutable value cannot be incremented")
            tokens.append(name)
                
        elif for_loop(variables, line)[0] == "Decrement Operator":
            tokens.append("DECREMENT OPERATOR:")
            name = for_loop(variables, line)[1]
            if name[0] == '&':
                raise SyntaxError("Immutable value cannot be decremented")
            tokens.append(name)
            
        elif for_loop(variables, line)[0] == "Addition":
            tokens.append("ADDITION:")
            name = for_loop(variables, line)[1]
            if name[0] == '&':
                raise SyntaxError("Immutable values cannot be changed")
            tokens.append(name)
            value_added = "".join(line).split()[-1]
            try:
                is_this_variable_defined = variables[variables.index(value_added)]
            except:
                raise SyntaxError(f"Variable '{value_added}' is undefined")
            if value_added[0] == "&":
                value_added = value_added[1:].upper()
            else:
                value_added = value_added.lower()
            tokens.append(value_added)
            
        elif for_loop(variables, line)[0] == "Subtraction":
            tokens.append("SUBTRACTION:")
            name = for_loop(variables, line)[1]
            if name[0] == '&':
                raise SyntaxError("Immutable values cannot be changed")
            tokens.append(name)
            value_added = "".join(line).split()[-1]
            try:
                is_this_variable_defined = variables[variables.index(value_added)]
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

syphon_tokenizer(str(sys.argv[1:]))
