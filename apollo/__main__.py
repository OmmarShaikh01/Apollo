import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

from apollo.app.apollo_exe import ApolloExecute

app = ApolloExecute()
app.Execute()


