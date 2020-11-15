import os, sys, re
import apollo
from apollo.utils import ConfigManager

parent_dir = apollo.__path__[0]

class Qtstyle:
    """
    Qstyle is used to create a CSS for the given theme
    
    >>> Qtstyle.stylesheet('GRAY_100')
    """
    
    def __init__(self):...
    
    @classmethod
    def stylesheet(cls, theme = "GRAY_100"):
        """
        stylesheet is used to replace all the placeholder values with the theme values
        and returns a string
        
        :Args:
            theme: Dict
                dict where keys are the stylesheet
                placeholders and the hex values to replace them with
        """    
        
        CONF_MANG = ConfigManager()
        CONF_MANG.Setvalue(theme, "ACTIVETHEME")
        CONF_MANG.writeConfig("config.cfg")
        
        theme = cls.theme(theme)
        with open(os.path.join(parent_dir, "resources", "qtstyle", "stylesheet.txt")) as style:
            new_stylesheet = style.read().split("\n")
            
        # Replaces the placeholders with the actual hex colours in the CSS
        stylesheet = ""
        for line in new_stylesheet:
            for element, value in theme.items():
                # all values of the dict are checked for an occurance on
                # the specific line if value found replaces it and exits loop
                if re.search(f"[($)]{element}(?!-)", line):
                    stylesheet += f"{line.replace(f'${element}', value)}\n"
                    break
            else:
                stylesheet += f"{line}\n"
                
        # replaces global values and writes to a file
        with open(os.path.join(parent_dir, "resources", "qtstyle", "theme_stylesheet.txt"), 'w') as style:
            style.write(stylesheet)
        return stylesheet    
    
    @classmethod
    def theme(cls, name):
        """
        filename for the theme dict to load and returns a dict
        
        :Args:
            name: String
                name of the theme file without extension
        """
        with open(os.path.join(parent_dir, "resources", "qtstyle", "themes", f"{name}.json")) as theme:
            theme_dict = eval(theme.read())["THEME"]
        return theme_dict
        
if __name__ == "__main__":
    parent_dir = os.getcwd().rsplit("\\", 2)[0] # moves path pointer to main directory
    print(Qtstyle.stylesheet(Qtstyle().theme()))
    
    
