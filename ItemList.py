import os
from Item import *

def main():
    """main menu function"""
    try:
        if os.path.exists("inventory.csv"):  # open file for reading
            InventoryFile = open("inventory.csv", 'r')

            ItemList = InventoryFile.read().split('\n')

            InventoryFile.close()

        else:  # open file for writing if it does not exist
            InventoryFile = open("inventory.csv", 'r')
            ItemList = []

        return ItemList

    except IOError:
        print("Error reading or writing to file.")


def write(ItemList):
    try:
        # initialize item count and output format
        WriteNoOfItem = 0
        WriteData = ""

        # open and clear file for writing
        WriteFile = open("inventory.csv", 'w')

        for Object in ItemList:  # get individual items from list of items
            Object = str(Object)
            Object = Object.split(",")  # convert each item into a list, splitting the data

            ItemName = Object[0]  # get item name
            ItemName = str(ItemName)
            ItemName = ItemName.strip("['")  # format item name

            ItemDescription = Object[1]  # get item description
            ItemDescription = str(ItemDescription)
            ItemDescription = ItemDescription.strip(" '")  # format item description

            ItemCost = Object[2]  # get item cost
            ItemCost = str(ItemCost)
            ItemCost = ItemCost.strip(" '")  # format item cost

            ItemAvailability = Object[3]  # get item availability
            ItemAvailability = str(ItemAvailability)
            ItemAvailability = ItemAvailability.strip(" ']")
            if WriteNoOfItem != len(ItemList) - 1:
                ItemAvailability += "\n"  # format item availability

            ItemData = "{},{},{},{}".format(ItemName, ItemDescription, ItemCost,
                                            ItemAvailability)  # format item as a string

            WriteData += ItemData  # add all items for output into a single string
            WriteNoOfItem += 1  # increase item count

        WriteFile.write(WriteData)  # write data to file
        print(WriteNoOfItem, "items saved to inventory.csv")  # print number of items saved
        WriteFile.close()  # close file

    except IOError:
        print("Error updating file.")