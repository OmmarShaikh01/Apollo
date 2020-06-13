def modules_installer():
    import pip 
    command = ["install",
                "PyQt5",
                "pyo",
                "mutagen",
                "watchdog",
                "av",
                "pyqtgraph",
                "musicbrainzngs",
                "tinytag"]
    pip.main(command)

modules_installer()