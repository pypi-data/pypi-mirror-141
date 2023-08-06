import pathlib
import uuid
import argparse

def info(args, message):
    if args.shout:
        print(f"✨ {message}")

def warning(args, message):
    if args.shout:
        print(f"⚠️ {message}")

def error(args, message):
    if args.shout:
        print(f"❌ {message}")

def done(args, message):
    if args.shout:
        print(f"✔️  {message}")
        
        
def align_block(args, block):

    block = block.strip('}').strip('{')
    lines = filter(lambda line: line.strip(), block.split(';'))   
    
    lefts, rights = list(), list()
    max_line_length = 0
    
    for line in lines:
        parts = line.split(':')
        lpart = parts[0].strip()
        rpart = ":".join(parts[1:])
        
        lefts.append(lpart)
        rights.append(rpart)
        
        max_line_length = max(max_line_length, len(lpart))
        
    new_block = "{\n"
    
    
    
    for left, right in zip(lefts, rights):
        new_block += " " * args.indent                  + \
                    left                                + \
                    " " * (max_line_length - len(left)) + \
                    " " * args.lmargin                  + \
                    ":"                                 + \
                    " " * args.rmargin                  + \
                    right                               + \
                    ";\n"
                    
    new_block += "}"
    
    
    return new_block

def write_block(args, block, file):
    file.write(align_block(args, block))


def align_css_file(args):
    
    with open(args.filepath, 'r', encoding = 'utf-8') as f:
            
        new_filename = f"{uuid.uuid4().hex}.css"
        
        with open(new_filename, 'w', encoding = 'utf-8') as new_f:
            
            block         = str()
            reading_block = False
            
            for line in f:
                for character in line:

                    if reading_block:
                        block += character
                        
                        if character == '}':
                            reading_block = False
                            write_block(args, block, new_f)
                            block = str()
                            
                    elif character == '{':
                        reading_block = True
                        block         = str(character)
                        
                    else:
                        new_f.write(str(character))
            
            done(args, "File was fully processed!")
            
    info(args, "Renaming files...")
    args.filepath.unlink()
    pathlib.Path(new_filename).rename(args.filepath)
    done(args, "Files were successfully renamed!")

    
            
            
        
        
        
    


def main():

    parser = argparse.ArgumentParser(description = "Aligner of css param-value splitter")
    
    parser.add_argument("filepath", type = pathlib.Path, help = "Set path of the file which you want to align")
    
    #? Aligning settings
    #? _ = space character
    #? div {
    #?  ____border____:____1px solid black;
    #?   ↑         ↑    ↑
    #? indent lmargin  rmargin
    #?
    #? }
    parser.add_argument("-i", "--indent",  type = int, help = "Set indnet for inner valuses of the block", default = 4)
    parser.add_argument("-l", "--lmargin", type = int, help = "Set spaces amount before `:` character",    default = 2)
    parser.add_argument("-r", "--rmargin", type = int, help = "Set spaces amount after `:` character",     default = 2)
    
    
    #? io options
    parser.add_argument("-s", "--shout",        action = "store_true", help = "Forces programm to print info, warnings or critiacal errors messages to console. Default is False")
    
    args = parser.parse_args()
    
    
    if args.filepath.exists():
        info(args, f"Aligning file: {args.filepath}")
        
        align_css_file(args)
        
        done(args, f"Congrats! File was successfully aligned!")
    else:
        error(args, "Specified file path does not exist!")

if __name__ == '__main__':
    main()