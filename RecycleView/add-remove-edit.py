"""Example showing advanced usage of RecycleView to add, remove and edit elements in a list.
Also demonstrates some animations since the adding and removing can be difficult to spot without them."""
from kivy.app import App
from kivy.animation import Animation
from kivy.properties import *
from kivy.lang.builder import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
KV = """
<EditPopup>:
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            text: root.text
            on_text: root.text = self.text
        BoxLayout:
            Button:
                text: 'Confirm'
                on_release: root.edit_element_callback(root.index, root.text)
                on_release: root.dismiss()
            Button:
                text: 'Cancel'
                on_release: root.dismiss()

<RecycleItem>:
    orientation: 'horizontal'
    Label:
        text: root.text
    Button:
        size_hint_x: .2
        text: 'Edit'
        on_release: root.owner.start_edit_element(root)
    Button:
        size_hint_x: .2
        text: 'Remove'
        on_release: root.remove()

BoxLayout:
    orientation: 'vertical'
    spacing: 10
    BoxLayout:
        size_hint_y: .1
        TextInput:
            id: newItem
        Button:
            disabled: not newItem.text
            text: 'Add'
            on_press: app.add_element(newItem.text)
    RecycleView:
        id: rv
        data: app.data
        viewclass: 'RecycleItem'
        RecycleBoxLayout:
            spacing: 10
            default_size: None, dp(80)
            default_size_hint: 1, None
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
"""

class EditPopup(Popup):
    #The popup used to edit a specific list item
    text = StringProperty()  #Stores the editing text
    index = NumericProperty()  #Stores the index of the list element to be edited
    edit_element_callback = ObjectProperty()  #Stores the function to be called when an edit is completed


class RecycleItem(RecycleDataViewBehavior, BoxLayout):
    #Class used to displa items in the recycleview list
    owner = ObjectProperty()  #Stores the widget that holds the original 'data' list that stores all the recycleview items
    index = NumericProperty()  #Stores the current index of the recycleview data that this widget is displaying
    text = StringProperty()

    #Properties below are used for animating adding and removing this element
    add = BooleanProperty(False)  #when set to True on an update, this widget will display the add animation then set this to False
    animation = ObjectProperty(allownone=True)  #stores the animation object, can be used to check if its running

    def refresh_view_attrs(self, rv, index, data):
        self.index = index  #stores the index of the list element that this widget is currently displaying
        #provide some basic animation to draw attention to the item being added
        if data['add']:
            self.opacity = 0  #sets opacity to 0 to aanimate it back to 1 for a fade-in effect
            self.animation = Animation(opacity=1, duration=0.25)
            self.animation.start(self)
            self.animation.bind(on_complete=self.animate_finish)
            self.owner.data[self.index]['add'] = False  #unset the add value so it wont play this animation every time the widget is reused
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

    def remove(self):
        if not self.animation:  #dont start animation if an animation is already going (widget was reused)
            #start a basic animation to draw attention to the item being removed
            self.animation = Animation(opacity=0, duration=0.25, x=-self.width)
            self.animation.start(self)
            self.animation.bind(on_complete=self.remove_finish)

    def remove_finish(self, *_):
        #Called after the remove animation is done, actually removes the widget and resets so this widget can be reused
        self.owner.delete_element(self.index)  #this is the actual removal.  to not animate removal, just call this in the 'remove()' function
        self.animate_finish()

    def animate_finish(self, *_):
        #reset animation variables so this widget can be re-used
        self.opacity = 1
        self.x = 0
        self.animation = None


class Test(App):
    data = ListProperty()

    def start_edit_element(self, item):
        #called by the recycle item's edit buton, opens a popup to edit the element
        popup = EditPopup(title='Edit Element', text=item.text, index=item.index, edit_element_callback=self.edit_element, size_hint=(.5, .3))
        popup.open()

    def edit_element(self, index, text):
        #the actual edit element function, changes a specific item in the list to the given text
        self.data[index]['text'] = text
        self.data[index]['add'] = True
        self.root.ids.rv.refresh_from_data()  #force refresh the recycle layout from the data list, needs to be called since ListProperty does not track editing of individual elements

    def add_element(self, text):
        #add a new element to the start of the list
        self.data.insert(0, {"text": text, "owner": self, "add": True})

    def delete_element(self, index):
        #remove a specific element from the list
        self.data.pop(index)

    def build(self):
        self.data = [{"text": "Label "+str(x+1), "owner": self, "add": False} for x in range(10)]  #generate dummy data for the recycleview
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
