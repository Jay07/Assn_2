
class Item():
    ''' super class for item '''
    def __init__(self, ItemName, ItemDescription, ItemCost, ItemAvailability):
        ''' constructor for item '''
        self.ItemName = ItemName
        self.ItemDescription = ItemDescription
        self.ItemCost = ItemCost
        self.ItemAvailability = ItemAvailability

    def getItemName(self):
        ''' accessor for item name '''
        return self.ItemName

    def getItemDescription(self):
        ''' accessor for item description '''
        return self.ItemDescription

    def getItemCost(self):
        ''' accessor for item cost '''
        return self.ItemCost

    def getItemAvailability(self):
        ''' accessor for item availability '''
        return self.ItemAvailability

    def setItemName(self, NewName):
        ''' modifier for item name '''
        self.ItemName = NewName

    def setItemDescription(self, NewDescription):
        ''' modifier for item description '''
        self.ItemDescription = NewDescription

    def setItemCost(self, NewCost):
        ''' modifier for item cost '''
        self.ItemCost = NewCost

    def setItemAvailability(self, NewAvailability):
        ''' modifier for item availability '''
        self.ItemAvailability = NewAvailability

    def display(self):
        ''' helper to display all item data '''
        print(self.ItemName, self.ItemDescription, self.ItemCost, self.ItemAvailability)



