import pytest 

from apollo.app.dataproviders import SQLTableModel 


#### Fixtures ################################################################# 
@pytest.fixture(scope = "class") 
def DataModel(): 
    Table = SQLTableModel(":memory:") 
        return Table 

#### Tests ####################################################################
class Test_SQLTaleModel:
    """
    Test Class for SQLTableModel
    """
    @pytest.mark.skip()
    def test_LoadingData(self, DataModel):
        DataModel.LoadTable("library") 