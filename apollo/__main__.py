import sys, os

sys.path.append(os.path.split(os.path.dirname(__file__))[0])
print(">>", os.path.split(os.path.dirname(__file__))[0])

from apollo.app import ApolloExecute

app = ApolloExecute()
app.Execute()