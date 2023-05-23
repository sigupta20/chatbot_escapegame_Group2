from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

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
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I don't understand what you are trying to say !")

        return []


able_to_pick_up = ["box", "vessel"]


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
            dispatcher.utter_message(text=f"- {item}")

        return []


look_descriptions = {
    "table": "Some table description...",
    "box": "It's a box. There's something inside of it.",
    "vessel": "It's a vessel.",
}


class ActionLook(Action):
    def name(self) -> Text:
        return "action_look"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        spoken = False
        print("action look")

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'object':
                dispatcher.utter_message(text=look_descriptions[blob['value']])
                spoken = True
        if not spoken:
            dispatcher.utter_message(text="Could you repeat what you're trying to look at?")
        return []


class ActionPickUp(Action):
    def name(self) -> Text:
        return "action_pickup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_pickup")
        items_to_add = []

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'object':
                item = blob['value']
                if item not in able_to_pick_up:
                    dispatcher.utter_message(text=f"You can't pick up {item}.")
                else:
                    item_in_inventory = tracker.get_slot(item)
                    if item_in_inventory:
                        dispatcher.utter_message(text=f"You already have {item} in your inventory.")
                    else:
                        items_to_add.append(SlotSet(item, True))
                        dispatcher.utter_message(text=f"You've picked up the {item} and it is in your inventory.")

        if len(items_to_add) > 0:
            return items_to_add
        dispatcher.utter_message(text="Are you sure you spelled the item you wanted to pick up correctly?")
        return []


class ActionUse(Action):
    def name(self) -> Text:
        return "action_use"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        print("action run")
        return []
