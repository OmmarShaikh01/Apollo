import sys, os

sys.path.append(os.path.dirname(__file__))
print(os.path.dirname(__file__))

from apollo.app.apollo_main import ApolloExecute

app = ApolloExecute()
app.Execute()
