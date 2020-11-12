import os, sys, re
import apollo

parent_dir = apollo.__path__[0]

class Qtstyle:
    
    def __init__(self):...
    
    @classmethod
    def stylesheet(cls, theme = None):
        
        if theme == None:
            theme = cls.theme()
            
        with open(os.path.join(parent_dir, "resources", "qtstyle", "stylesheet.txt")) as style:
            new_stylesheet = style.read().split("\n")
            
        # replaces theme specific values to the values in the styesheet and return the output
        stylesheet = ""
        for line in new_stylesheet:
            for element, value in theme.items():
                if re.search(f"[($)]{element}(?!-)", line):
                    stylesheet += f"{line.replace(f'${element}', value)}\n"
                    break
            else:
                stylesheet += f"{line}\n"
                
        # replaces global values
        
        with open(os.path.join(parent_dir, "resources", "qtstyle", "theme_stylesheet.txt"), 'w') as style:
            style.write(stylesheet)
        return stylesheet    
    
    @classmethod
    def theme(cls, name = "GRAY_100"):
        with open(os.path.join(parent_dir, "resources", "qtstyle", "themes", f"{name}.json")) as theme:
            theme_dict = eval(theme.read())["THEME"]
        return theme_dict
        
if __name__ == "__main__":
    parent_dir = os.getcwd().rsplit("\\", 2)[0] # moves path pointer to main directory
    print(Qtstyle().stylesheet(Qtstyle().theme()))
    
    
