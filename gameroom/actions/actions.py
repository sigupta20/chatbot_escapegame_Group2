from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
# from rasa.shared.core.events import Event
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#

# Provide Name



class ActionUseKeyOnDoor(Action):
    def name(self):
        return "action_use_key_on_door"

    def run(self, dispatcher, tracker, domain):
        has_key = tracker.get_slot('key')

        if has_key:
            dispatcher.utter_message(text="Awesome, we are out of the basement now and entered into the Prisons of Azkaban.")
            dispatcher.utter_message(text="First, escape the prisoner and he will guide you to escape from here. You need to call his name, so that the cell can appear and you will be able to see him. Your hint: He's a prisoner of Azkaban and harry potter's godfather!")
        else:
            dispatcher.utter_message(text="You tried to open the door, but it's locked. You need a key.")

        return []






able_to_pick_up = ["charm", "potion", "vessel", "key", "po-charm", "scroll", "wand"]


class ActionInventory(Action):
    def name(self) -> Text:
        return "action_inventory"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        print("action_inventory")
        print(tracker.slots)
        items_in_inventory = [item for item in able_to_pick_up if tracker.get_slot(item)]

        if len(items_in_inventory) == 0:
            dispatcher.utter_message(text="There are no items in your inventory.")
            return []

        dispatcher.utter_message(text="These are the items in your inventory:")
        for item in items_in_inventory:
            dispatcher.utter_message(text=f"-{item}")

        return []



look_descriptions = {
    "table": "It is a black carved table. It has a concealment charm and a map on the top of it. We can inspect them one by one.",
    "box": "It's a wooden box. There's a potion inside of it. May be we should it pick it.",
    "potion": "It is a magical potion which makes a spell work.",
    "vessel": "It's a transfiguration vessel. People used these vessels, to mix things together. It can be super useful.",
    "room": "It a very dark and withered room. Seems quite old and cold. But I can see something. I can see a table, a box in the corner and a transfiguration vessel lying on the ground. Tell me which item you want to look?",
    "charm": "It's a concealment charm to make, used by wizards to make things disappear.",
    "map": "It is a map of Hogwarts. Doesn't look that important.",
    "prison": "It's a dark and scary prison. As far as I can see, I can only see spider's web and an old almirah in the corner",
    "almirah": "It's an old magical piece and I can see a magical wand inside it",
    "wand": "This is snap's wand, one of powerful wands exists. I am not sure, why it is here."
}


class ActionLook(Action):
    def name(self) -> Text:
        return "action_look"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        spoken = False
        print("action_look")

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'object':
                dispatcher.utter_message(text=look_descriptions[blob['value']])
                spoken = True
        if not spoken:
            dispatcher.utter_message(text="Could you specify clearly, what you're trying to look?")
        return []


class ActionPickUp(Action):
    def name(self) -> Text:
        return "action_pickup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_pickup")
        items_to_add = []
        item_picked_up = False  # flag to track whether an item was picked up

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'object':
                item = blob['value']
                if item not in able_to_pick_up:
                    dispatcher.utter_message(text=f"You can't pick up {item}.")
                else:
                    item_in_inventory = tracker.get_slot(item)
                    if item_in_inventory:
                        dispatcher.utter_message(text=f"You already have {item} in your inventory.")
                        item_picked_up = True # set the flag to True
                    else:
                        items_to_add.append(SlotSet(item, True))
                        # tracker.slots[item] = True # directly set the slot
                        dispatcher.utter_message(text=f"You've picked up the {item} and it is in your inventory.")
                        item_picked_up = True # set the flag to True
                        if item == 'wand':
                            dispatcher.utter_message(text=f"Sirius: Well done! You finally found the snape's wand. Let's hurry up. We are at the door now. To unlock the prison, use the wand and cast spell Alohomora !")


        if len(items_to_add) > 0:
            return items_to_add
        # Only send the message if no items were picked up
        if not item_picked_up:
            dispatcher.utter_message(text="Are you sure you spelled the item you wanted to pick up correctly?")
        return []

combinations = {
    ('charm', 'potion'): "Wow, you have created Po-charm, now put it inside vessel and we are ready...",
    ('po-charm', 'vessel'): "Super! Now time to use your wand harry and cast spell - Evanseco-Sofortum !",
    ('key', 'door'): "Why put the key back in the box? It's probably super useful.",
    ('wand', 'prison'): "Super, wand is illuminating now, say - Alohomora"
}
combinations.update({(i2, i1): v for (i1, i2), v in combinations.items()})

combination_results = {
    ('charm', 'potion'): "po-charm",
    ('potion', 'charm'): "po-charm",
    ('po-charm', 'vessel'): "scroll",
    ('vessel', 'po-charm'): "scroll"
}





class ActionUse(Action):
    def name(self) -> Text:
        return "action_use"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_use")
        entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'object']
        if len(entities) == 0:
            dispatcher.utter_message(text="I think you want to combine items but something is unclear.")
            dispatcher.utter_message(text="Could you retry and make sure you spelled the items correctly?.")
            return []
        elif len(entities) == 1:
            dispatcher.utter_message(text="I think you want to combine items but something is unclear or missing.")
            dispatcher.utter_message(text=f"I could only make out that you wanted to use {entities[0]}.")
            dispatcher.utter_message(text="Could you retry and make sure you spelled the items correctly?.")
            return []
        elif len(entities) > 2:
            dispatcher.utter_message(text="I think you want to combine items but something is unclear.")
            dispatcher.utter_message(text=f"I could only make out that you wanted to combine {' and '.join(entities)}.")
            dispatcher.utter_message(text="You can only combine two items at a time.")
            return []
        # there are two items and they are confirmed
        item1, item2 = entities

        # Inventory Challenge
        # check if the items are in the inventory
        if not (tracker.get_slot(item1) and tracker.get_slot(item2)):
            dispatcher.utter_message(text="You don't have these items in your inventory.")
            return []



        if (item1, item2) in combinations.keys():
            dispatcher.utter_message(text=combinations[(item1, item2)])
            if (item1, item2) in combination_results.keys():
                new_item = combination_results[(item1, item2)]
                return [SlotSet(item1, False), SlotSet(item2, False), SlotSet(new_item, True)]
            else:
                return [SlotSet(item1, False), SlotSet(item2, False)]  # deduct the items
        else:
            dispatcher.utter_message(text=f"I don't think combining {item1} with {item2} makes sense.")

        return []


class ActionCastSpell(Action):
    def name(self) -> Text:
        return "action_cast_spell"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        has_scroll = tracker.get_slot('scroll')  # Check if the wand is in the inventory

        if has_scroll:
            dispatcher.utter_message(text="Good job ! Now you must hurry to the basement and you will find Celina there. She is a ghost and she will ask riddles to escape from the basement. Go down and call her name !")
            return [SlotSet("scroll", False)] 
        else:
            dispatcher.utter_message(text="Drawing on all your focus, you delicately swirled your wand, your heart racing with anticipation. \nYet, despite your best efforts, the intended spell fizzled out, manifesting as a mere spark at the wand's tip and a puff of smoke that swiftly dissipated into the air. \nIt seems your knowledge is not sufficient to cast this particular spell just yet. \nAs a cloud of frustration sweeps over you, it occurs to you that perhaps you should explore your surroundings for a spell scroll, an ancient written guide that might hold the secrets to mastering this arcane art.")

        return []