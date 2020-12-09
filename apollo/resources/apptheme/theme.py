import os, sys, re

from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from PyQt5 import pyrcc

from apollo.utils import ConfigManager, dedenter
import apollo

root_path = os.path.join(apollo.__path__[0], "resources", "apptheme")

# automated tests are remaining to be add

class Theme:
    """
    Controls all the theme related functions 
    """
    def __init__(self):
        self.Config_manager = ConfigManager()    
        
    def GetAvaliableThemes(self):
        """
        Scans the theme Directory to get new Themes for applications
        """
        ThemeDir = os.path.join(root_path, "theme")
        self.Config_manager.Setvalue("", "APPTHEMES")            
        
        for File in os.listdir(ThemeDir):
            File, Ext = (os.path.splitext(File))
            
            # scans for a pallet file and make a theme directory for it and move the pallet file inside it 
            if (Ext == ".json" and not os.path.isdir(os.path.join(ThemeDir, File))):            
                os.mkdir(os.path.join(ThemeDir, File))
                
                NewDir = os.path.join(ThemeDir, File)
                NewFname = os.path.join(ThemeDir, File, f'{File}.json')
                OldFname = os.path.join(ThemeDir, f'{File}.json')
                os.rename(OldFname, NewFname)                                         
                
                # gets the theme inside the theme Folder
                ThemePallet = self.GetTheme(NewFname)
                StyleSheet = self.GenStylesheet(ThemePallet)
                ResourceFile = self.GenTheme_Icons(ThemePallet, NewDir, os.path.join(root_path, "svg"))
                with open(os.path.join(NewDir, f"{File}.qss"), "w") as FH1,\
                     open(os.path.join(NewDir, f"{File}.qrc"), "w") as FH2:
                    FH1.write(StyleSheet)
                    FH2.write(ResourceFile)
                    
                self.Config_manager.Setvalue(File, "APPTHEMES")            
                                
            elif (os.path.isdir(os.path.join(ThemeDir, File))):
                self.Config_manager.Setvalue(File, "APPTHEMES")
            
            else:
                continue
                
        # Updates all values in config
        self.Config_manager.writeConfig()
        return self.Config_manager.Getvalue("APPTHEMES")
                
    def GetTheme(self, file):
        """
        filename for the theme dict to load and returns a dict
        
        :Args:
            name: String
                name of the theme file without extension
        """
        with open(file) as theme:
            theme_dict = eval(theme.read())["THEME"]
        return theme_dict
    
    def LoadStyleSheet(self, Name = "GRAY_100"):        
        ThemeDir = os.path.join(root_path, "theme", Name)
        if os.path.isdir(ThemeDir):            
            resources = list(filter(lambda File: os.path.splitext(File)[1] in [".qrc", ".qss"], os.listdir(ThemeDir)))
            resources = list(map(lambda File: os.path.join(ThemeDir, File), resources))
            if len(resources) == 2:
                return resources
                    
    ############################################################################    
    # Resourece Generation Functions
    ############################################################################

    def GenStylesheet(self, pallete):
        """
        stylesheet is used to replace all the placeholder values with the theme values
        and returns a string
        
        :Args:
            theme: Dict
                dict where keys are the stylesheet
                placeholders and the hex values to replace them with
        """
        with open(os.path.join(root_path, "stylesheet.css")) as style:
            new_stylesheet = style.read().split("\n")
            
        # Replaces the placeholders with the actual hex colours in the CSS
        stylesheet = ""
        for line in new_stylesheet:
            for element, value in pallete.items():
                # all values of the dict are checked for an occurance on
                # the specific line if value found replaces it and exits loop
                if re.search(f"[($)]{element}(?!-)", line):
                    stylesheet += f"{line.replace(f'${element}', value)}\n"
                    break
            else:
                stylesheet += f"{line}\n"
        return stylesheet    
        
    
    def ScanDir_Images(self, path, include = [".svg"]):
        # works for no subdir
        Files = (os.listdir(path))
        return Files    
    
    def ImageOverlay(self, Image, Theme, Dest, Color: QtGui.QColor, size = (128, 128)):
        
        """"""
        Icon = QtGui.QIcon(Image).pixmap(QtCore.QSize(size[0], size[1]))
        
        Painter = QtGui.QPainter(Icon)
        Painter.setBrush(Color)
        Painter.setPen(Color)
        Painter.setCompositionMode(Painter.CompositionMode_SourceIn)
        Painter.drawRect(Icon.rect())
        Painter.end()
        
        if not os.path.isdir(os.path.join(Dest, "png")):            
            os.mkdir(os.path.join(Dest, "png"))
        if not Icon.isNull():
            name = os.path.splitext(os.path.split(Image)[1])[0]
            Icon.save(os.path.join(Dest, "png", f"{name}_{size[0]}X{size[1]}_{Theme}.png"), "PNG")
        return os.path.join(Dest, "png", f"{name}_{size[0]}X{size[1]}_{Theme}.png")
        
    def GenTheme_Icons(self, theme, Dest, ImgDir):
        paths = []
        for Image in self.ScanDir_Images(ImgDir):
            Image = os.path.join(ImgDir, Image)            
            for ThemeName in ["icon-01", "icon-02", "icon-03", "inverse-01", "disabled-02", "disabled-03"]:                
                Path = self.ImageOverlay(Image, ThemeName, Dest, QtGui.QColor(theme.get(ThemeName)))
                paths.append(Path)
        return self.GenIconResource(paths)
                
    def GenIconResource(self, Files):
        HEADER = """
        <RCC>
            <qresource prefix="icon_pack">                       
        """
        
        BODY = "\n".join([f"{' '*8}<file>{File}</file>" for File in Files])
        
        FOOTER = """
            </qresource>
        </RCC>
        """        
        String = "\n".join([dedenter(HEADER, 8), BODY, dedenter(FOOTER, 8)])    
        return String
    
    def DefaultPallete(self):
        JSON = """
                {
            "THEME":{
                "ui-background" : "#161616",
                "interactive-01" : "#0f62fe",
                "interactive-02" : "#6f6f6f",
                "interactive-03" : "#ffffff",
                "interactive-04" : "#4589ff",
                "danger" : "#da1e28",
                "ui-01" : "#262626",
                "ui-02" : "#393939",
                "ui-02-alt" : "#525252",
                "ui-03" : "#393939",
                "ui-04" : "#6f6f6f",
                "ui-05" : "#f4f4f4",
                "button-separator" : "#161616",
                "decorative-01" : "#525252",
                "text-01" : "#f4f4f4",
                "text-02" : "#c6c6c6",
                "text-03" : "#6f6f6f",
                "text-04" : "#ffffff",
                "text-05" : "#8d8d8d",
                "text-error" : "#ff8389",
                "link-01" : "#78a9ff",
                "inverse-link" : "#0f62fe",
                "icon-01" : "#f4f4f4",
                "icon-02" : "#c6c6c6",
                "icon-03" : "#ffffff",
                "field-01" : "#262626",
                "field-02" : "#393939",
                "inverse-01" : "#161616",
                "inverse-02" : "#f4f4f4",
                "support-01" : "#fa4d56",
                "support-02" : "#42be65",
                "support-03" : "#f1c21b",
                "support-04" : "#4589ff",
                "inverse-support-01" : "#da1e28",
                "inverse-support-02" : "#24a148",
                "inverse-support-03" : "#f1c21b",
                "inverse-support-04" : "#0043ce",
                "focus" : "#ffffff",
                "inverse-focus-ui" : "#0f62fe",
                "hover-primary" : "#0353e9",
                "hover-primary-text" : "#a6c8ff",
                "hover-secondary" : "#606060",
                "hover-tertiary" : "#f4f4f4",
                "hover-ui" : "#353535",
                "hover-ui-light" : "#525252",
                "hover-selected-ui" : "#4c4c4c",
                "hover-danger" : "#ba1b23",
                "hover-row" : "#353535",
                "inverse-hover-ui" : "#e5e5e5",
                "active-primary" : "#002d9c",
                "active-secondary" : "#393939",
                "active-tertiary" : "#c6c6c6",
                "active-ui" : "#525252",
                "active-danger" : "#750e13",
                "selected-ui" : "#393939",
                "highlight" : "#001d6c",
                "skeleton-01" : "#353535",
                "skeleton-02" : "#393939",
                "visited-link" : "#be95ff",
                "disabled-01" : "#262626",
                "disabled-02" : "#525252",
                "disabled-03" : "#6f6f6f"
            }
        }
        """
        return dedenter(JSON[1:-1], 8)
        
if __name__ == "__main__":
    App = QtWidgets.QApplication([])
    Inst = Theme()
    #Inst.GetAvaliableThemes()
    
