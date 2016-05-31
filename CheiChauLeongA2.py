from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button,ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from ItemList import *
from Item import *

class ItemHire(App):
    ''' ItemHire is a Kivy App for Hiring and Returning of Items '''
    def build(self):
        ''' build the Kivy App from the kv file '''
        self.title="Equipment Hire"
        self.root=Builder.load_file("ItemHire.kv")
        self.ListItem() # run list of items to show data on GUI and append to lists
        return self.root

    def on_stop(self):
        ''' write to file when App closes '''
        write(ItemList)

    def ListItem(self):
        ''' list items '''
        self.ItemDict={} # initialize dictionary
        for Object in ItemList:
            Object = str(Object)
            Detail = Object.split(',')
            for Data in Detail:
                ItemDetailsList.append(Data) # append each individual item detail to list
            if Detail[3] == "in":
                ButtonColor = [0, 0, 1, 1] # set button color
            else:
                ButtonColor = [0, 1, 0, 1] # set button color
            self.ItemDict[Detail[0]]=Button(text=Detail[0], background_color=ButtonColor) # create button
            self.ItemDict[Detail[0]].bind(on_press=lambda a:self.ItemState()) # bind function to button
            self.root.ids.item.add_widget(self.ItemDict[Detail[0]]) # add button to GUI

    def ShowLabel(self):
        ''' show basic labels '''
        if self.root.ids.list.state == "down":  # list items is selected
            self.root.ids.label.text = "Choose action from the left menu, then select items on the right"
            self.ItemNameList = [] # initialize name list
            for Object in ItemList: # loop for each item
                Object = str(Object)
                Details = Object.split(',')
                self.ItemNameList.append(Details[0]) # append item name to name list
            for Name in self.ItemNameList:
                if self.ItemDict[Name].background_color == [1, 0, 1, 1]:  # change button color
                    self.ItemDict[Name].background_color = [0, 0, 1, 1]
        elif self.root.ids.hire.state == "down": # hire items is selected
            self.root.ids.label.text = "Select available items to hire"
        elif self.root.ids.ret.state == "down": # return items is selected
            self.root.ids.label.text = "Select available items to return"

    def ItemState(self):
        ''' check for whether the item button has been pressed down '''
        if self.root.ids.list.state == "down":  # list items is selected
            self.ChangeLabel()
        elif self.root.ids.hire.state == "down": # hire items is selected
            self.HireItem()
        elif self.root.ids.ret.state == "down": # return items is selected
            self.ReturnItem()

    def ChangeLabel(self):
        ''' display label when item is selected in list items '''
        self.ItemNameList = [] # initialize name list
        for Object in ItemList: # loop for each item
            Object = str(Object)
            Detail = Object.split(',')
            self.ItemNameList.append(Detail[0]) # append name to name list
        i=0 # counter for each individual detail
        for Name in self.ItemNameList: # loop for each item
            a=i # item name
            b=i+1 # item description
            c=i+2 # item cost
            d=i+3 # item availability
            if self.ItemDict[Name].state=="down": # item button is selected and is in list
                self.root.ids.label.text="{} ({}), ${:.2f} is {}".format(ItemDetailsList[a],ItemDetailsList[b],float(ItemDetailsList[c]),ItemDetailsList[d])
                break
            i+=4 # next item

    def HireItem(self):
        ''' hire item '''
        self.ItemNameList = [] # initilize name list
        self.HireItemDict = {} # initialize dictionary
        for Object in ItemList: # loop for each item
            Object = str(Object)
            Detail = Object.split(',')
            self.ItemNameList.append(Detail[0]) # append name to name list
            self.HireItemDict[Detail[0]] = Detail[2] # enter item name and item cost into dictionary
        InitialPrice=0.0 # set initial price
        HireItemName="" # set output string
        record="" # set selected items
        for Name in self.ItemNameList: # loop for each item
            if self.ItemDict[Name].state=="down": # item is selected for hire
                if self.ItemDict[Name].background_color==[0, 0, 1, 1]: # item available for hire
                    for Item in self.ItemNameList: # loop for each item available for hire
                        if self.ItemDict[Item].background_color==[1,0,1,1]: # select item to hire
                            if record == "":
                                record += Item # check if items are selected
                            else:
                                record += ',' + Item
                    if record!="":
                        self.ItemDict[Name].background_color = [1, 0, 1, 1] # change button color
                        data=record.split(',')
                        for element in data:
                            if HireItemName=="": # first item selected
                                HireItemName+=self.ItemDict[element].text # add price of items
                                InitialPrice += float(self.HireItemDict[self.ItemDict[element].text]) # generate output string
                            else: # other items selected
                                HireItemName+= ","+self.ItemDict[element].text # add price of items
                                InitialPrice += float(self.HireItemDict[self.ItemDict[element].text]) # generate output string
                        InitialPrice += float(self.HireItemDict[self.ItemDict[Name].text]) # add price of items
                        HireItemName += "," + self.ItemDict[Name].text # generate output string
                        self.root.ids.label.text="Hiring:{} for ${:.2f}".format(HireItemName,InitialPrice)
                    elif record=="":
                        self.ItemDict[Name].background_color = [1, 0, 1, 1]
                        InitialPrice += float(self.HireItemDict[self.ItemDict[Name].text]) # add price of items
                        HireItemName += self.ItemDict[Name].text # generate output string
                        self.root.ids.label.text = "Hiring:{} for ${:.2f}".format(HireItemName, float(InitialPrice))

                elif self.ItemDict[Name].background_color==[1,0,1,1]: # confirming to hire selected items
                    self.ItemDict[Name].background_color=[0,0,1,1] # change button color
                    for Name in self.ItemNameList:
                        if self.ItemDict[Name].background_color == [1, 0, 1, 1]: # item has been selected for hire
                            InitialPrice += float(self.HireItemDict[self.ItemDict[Name].text]) # add price of items
                            HireItemName += self.ItemDict[Name].text # generate output string
                            self.root.ids.label.text = "Hiring:{} for ${:.2f}".format(HireItemName, float(InitialPrice))

                elif self.ItemDict[Name].background_color == [0, 1, 0, 1]:  # item not available for hired
                    self.root.ids.label.text = "Hiring: no items for {:.2f}".format(InitialPrice)


    def ReturnItem(self):
        ''' return item '''
        self.ItemNameList = [] # initialize name list
        for Object in ItemList: # loop for each item
            Object = str(Object)
            Detail = Object.split(',')
            self.ItemNameList.append(Detail[0]) # append name to name list
        ReturnItemName = "" # set output string
        record = "" # set selected items
        for Name in self.ItemNameList: # loop for each item
            if self.ItemDict[Name].state == "down": # item is selected for return
                if self.ItemDict[Name].background_color == [0, 1, 0, 1]: # item is available for return
                    for Item in self.ItemNameList: # loop for each item available to return
                        if self.ItemDict[Item].background_color == [1, 0, 1, 1]: # select item to return
                            if record == "":
                                record += Item # check if items are selected
                            else:
                                record += ',' + Item
                    if record != "":
                        self.ItemDict[Name].background_color = [1, 0, 1, 1] # change button color
                        data = record.split(',')
                        for element in data:
                            if ReturnItemName == "": # first item selected
                                ReturnItemName += self.ItemDict[element].text # generate output string
                            else: # other items selected
                                ReturnItemName +=  "," + self.ItemDict[element].text # generate output string
                        ReturnItemName += "," + self.ItemDict[Name].text # generate output string
                        self.root.ids.label.text = "Returning:{}".format(ReturnItemName)
                    elif record == "":
                        self.ItemDict[Name].background_color = [1, 0, 1, 1] # change button color
                        ReturnItemName += self.ItemDict[Name].text # generate output string
                        self.root.ids.label.text = "Returning:{}".format(ReturnItemName)

                elif self.ItemDict[Name].background_color == [1, 0, 1, 1]: # confirming to return selected items
                    self.ItemDict[Name].background_color = [0, 1, 0, 1] # change button color
                    for Name in self.ItemNameList:
                        if self.ItemDict[Name].background_color == [1, 0, 1, 1]: # item has been selected for return
                            ReturnItemName += self.ItemDict[Name].text # generate output string
                            self.root.ids.label.text = "Returning:{}".format(ReturnItemName)

                elif self.ItemDict[Name].background_color == [0, 0, 1, 1]:  # item is already on hired
                    self.root.ids.label.text = "Returning: no items on hire"


    def ConfirmButton(self):
        ''' adjusts the state of the button when hired or returned '''
        if self.root.ids.hire.state == "down": # hire items is elected
            self.ItemNameList = [] # initialize name list
            for Object in ItemList: # loop for each item
                Object = str(Object)
                Detail = Object.split(',')
                self.ItemNameList.append(Detail[0]) # append name to name list
            i = 3
            for Name in self.ItemNameList:
                if self.ItemDict[Name].background_color == [1, 0, 1, 1]: # item is selected for hire
                    self.ItemDict[Name].background_color = [0, 1, 0, 1] # change color to show item is on hire
                    ItemDetailsList[i]="out" # change item availability
                i += 4 # check next item

            self.root.ids.list.state="down"
            self.root.ids.hire.state="normal"
        elif self.root.ids.ret.state == "down":  # return items is selected
            self.ItemNameList = [] # initialize name list
            for Object in ItemList: # loop for each item
                Object = str(Object)
                Detail = Object.split(',')
                self.ItemNameList.append(Detail[0]) # append name to name list
            i = 3
            for Name in self.ItemNameList:
                if self.ItemDict[Name].background_color == [1, 0, 1, 1]: # item is selected for return
                    self.ItemDict[Name].background_color = [0, 0, 1, 1] # change color to show item is not on hire
                    ItemDetailsList[i] = "in" # change item availability
                i += 4 # check next item

            self.root.ids.list.state = "down"
            self.root.ids.ret.state = "normal"

    def AddItem(self):
        ''' add new item for hire '''
        AddItemDict = {} # initialize dictionary
        box = BoxLayout(orientation="vertical") # create box layout
        AddItemDict['AddItemName'] = TextInput(text="") # get item name
        AddItemDict['AddItemDescription'] = TextInput(text="") # get item description
        AddItemDict['AddItemCost'] = TextInput(text="") # get item cost
        AddItemDict['label'] = Label(text="Enter detail for new item") # create label
        box.add_widget(Label(text="Item Name:")) # create label for getting item name
        box.add_widget(AddItemDict['AddItemName']) # activate function to get item name
        box.add_widget(Label(text="Description:")) # create label for getting item description
        box.add_widget(AddItemDict['AddItemDescription']) # activate function to get item description
        box.add_widget(Label(text="Price Per Day:")) # create label for getting item cost
        box.add_widget(AddItemDict['AddItemCost']) # activate function to get item cost

        box.add_widget(Button(text="Save Item",id="save",on_press=lambda a:self.ValidateItem(popup,AddItemDict))) # add save button and bind validation function
        box.add_widget(Button(text="Cancel",id="cancel",on_press=lambda a:self.cancel(popup))) # add cancel button and bind cancel function
        box.add_widget(AddItemDict['label']) # activate function for label
        popup=Popup(title="Add item",content=box) # create popup
        popup.open() # open popup

    def cancel(self,popup):
        ''' close popup '''
        popup.dismiss() # close popup

    def ValidateItem(self,popup,item):
        ''' validate new item '''
        if len(item['AddItemName'].text) == 0:  # if item name is empty
            item['label'].text = "All fields must be completed"
        elif len(item['AddItemDescription'].text) == 0:  # if item description is empty
            item['label'].text = "All fields must be completed"
        elif len(item['AddItemCost'].text) == 0: # if item cost is empty
            item['label'].text = "All fields must be completed"
        else: # fields are all filled in
            try: # exception handling
                float(item['AddItemCost'].text) # convert to float
                if float(item['AddItemCost'].text) < 0:  # if item cost is negative
                    item['label'].text = "Price must not be negative"
                else: # item is valid
                    self.ItemDict[item['AddItemName'].text] = Button(text=item['AddItemName'].text, background_color=[0, 0, 1, 1]) # create button for new item
                    self.ItemDict[item['AddItemName'].text].bind(on_press=lambda a: self.ItemState()) # bind function to new button
                    self.root.ids.item.add_widget(self.ItemDict[item['AddItemName'].text]) # add new button to GUI
                    AddItemAvailability = 'in' # set item availability
                    ItemData = "{},{},{},{}".format(item['AddItemName'].text, item['AddItemDescription'].text, item['AddItemCost'].text, AddItemAvailability)  # format the data
                    ItemList.append(ItemData)  # append the new data into ItemList
                    ItemDetailsList.append(item['AddItemName'].text) # append item name into list
                    ItemDetailsList.append(item['AddItemDescription'].text) # append item description into list
                    ItemDetailsList.append(item['AddItemCost'].text) # append item cost into list
                    ItemDetailsList.append(AddItemAvailability) # append item availability in list
                    popup.dismiss() # close popup
            except (ValueError) or (AttributeError): # unable to convert to float means item cost is not a number
                item['label'].text = "Error. Price must be a valid number"

ItemDetailsList=[]
ItemList = main()
ItemHire().run()