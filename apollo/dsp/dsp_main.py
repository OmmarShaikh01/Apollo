class Apollo_Player:
    """
    """
    def __init__(self, UI):
        """Constructor"""
        self.UI = UI


class DSP_Main:
    """
    """
    def __init__(self, UI):
        """Constructor"""
        self.UI = UI
        self.Apollo_Player = Apollo_Player(self.UI)

if __name__ == "__main__":
    from apollo.app.apollo_main import ApolloExecute
    app = ApolloExecute()
    app.Execute()
