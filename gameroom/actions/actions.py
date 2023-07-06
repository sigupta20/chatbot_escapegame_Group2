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

class ActionUseKeyAndMoveToRoom3(Action):
    def name(self):
        return "action_use_key_and_move_to_room_3"

    def run(self, dispatcher, tracker, domain):
        has_key = tracker.get_slot('key')

        if has_key:
            dispatcher.utter_message(text="Awesome, we are out of the basement now and entered into the Prisons of Azkaban.")
            dispatcher.utter_message(text="Now, you must help to escape a prisoner, who was also trapped here by Lord Volde...! He will guide you to escape from the prison walls. You need to call his name, so that the cell can appear, which is hidden by magic and you will be able to see him. Your hint: He's a prisoner of Azkaban and harry potter's godfather! If you don't know his name, look for some clues in the room.")
            return [SlotSet("current_room", "room_3")]
        else:
            dispatcher.utter_message(text="You tried to open the door, but it's locked. You need a key.")
            return []

class ActionBlack(Action):
    def name(self):
        return "action_black"

    def run(self, dispatcher, tracker, domain):
        current_room = tracker.get_slot('current_room')
        tom_solved = tracker.get_slot('tom_solved')

        if current_room == "room_3" and tom_solved==False:
            dispatcher.utter_message(tom_solved)
            dispatcher.utter_message(text="Sirius: Hey, little wizard ! It's me Sirius black.\n You must help me out of the bars so that I can help you escape the chambers.\n For that, you need to call the name of an evil wizard ( you know who !) which is the key to open the cell. Call his name loudly and bars will disappear.\n Your hint: It's the other name of evil Lord Voldemort.... Who's he? Hint: If you don't know his name, look for some clues in the room.")
            return [SlotSet("black_solved", True)]
        else:
            return []

class ActionTom(Action):
    def name(self):
        return "action_tom"

    def run(self, dispatcher, tracker, domain):
        current_room = tracker.get_slot('current_room')
        tom_solved = tracker.get_slot('tom_solved')
        has_wand = tracker.get_slot('wand')

        if current_room == "room_3" and tom_solved==False and has_wand==False:
            dispatcher.utter_message(text="Sirius: Super, I am out of the bars now. You need to help me find my wand. Look around the room for some clues.")
            return [SlotSet("tom_solved", True)]
        elif current_room == "room_3" and tom_solved==False and has_wand==True:
            dispatcher.utter_message(text="Sirius: Well done! You finally found my wand. Let's hurry up. We are at the prison walls now. You have to cast Alohomora with me. I am too weak to cast it myself.")
            return [SlotSet("tom_solved", True)]
        else:
            return []
        
class ActionAlohomora(Action):
    def name(self):
        return "action_alohomora"

    def run(self, dispatcher, tracker, domain):
        current_room = tracker.get_slot('current_room')
        tom_solved = tracker.get_slot('tom_solved')
        has_wand = tracker.get_slot('wand')

        if current_room == "room_3" and tom_solved==True:
            dispatcher.utter_message(text="Congratulations you little Wizard! We are out of the chambers now. You have really done a good job here. It was not easy, but you made it happen. You can return to Hogwarts now. This is the end of the game....!")
            return [SlotSet("alohomora", True)]
        else:
            return []






# class ActionUseKeyOnDoor(Action):
#     def name(self):
#         return "action_use_key_on_door"

#     def run(self, dispatcher, tracker, domain):
#         has_key = tracker.get_slot('key')

#         if has_key:
#             dispatcher.utter_message(text="Awesome, we are out of the basement now and entered into the Prisons of Azkaban.")
#             dispatcher.utter_message(text="Now, you must help to escape a prisoner, who was also trapped here by Lord Volde...! He will guide you to escape from the prison walls. You need to call his name, so that the cell can appear, which is hidden by magic and you will be able to see him. Your hint: He's a prisoner of Azkaban and harry potter's godfather!")
#         else:
#             dispatcher.utter_message(text="You tried to open the door, but it's locked. You need a key.")

#         return []

class ActionUseWandontheWalls(Action):
    def name(self):
        return "action_use_wand_on_walls"

    def run(self, dispatcher, tracker, domain):
        has_wand = tracker.get_slot('wand')

        if has_wand:
            dispatcher.utter_message(text="Super, wand is illuminating now, cast the spell - Alohomora!")
        else:
            dispatcher.utter_message(text="You tried to unlock the prison walls, but it's locked. You need a wand.")

        return []


able_to_pick_up = ["charm", "potion", "vessel", "key", "po-charm", "enchanted_vessel", "wand"]


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
    "table": "It is a black carved table. It has a concealment charm the top of it. We can try to inspect it.",
    "box": "It's a wooden box. There's a potion inside of it. May be we should it pick it.",
    "potion": "It is a magical potion which makes a spell work.",
    "vessel": "It's a transfiguration vessel. People used these vessels, to mix things together. It can be super useful.",
    "chamber": "It a very dark and withered chamber. Seems quite old and cold. But I can see something. I can see a table, a box in the corner and a transfiguration vessel lying on the ground. Tell me which item you want to look?",
    "charm": "It's a concealment charm to make, used by wizards to make things disappear.",
    "book": "In your hands, you hold an autobiography of the infamous Salazar Slytherin, its pages whispering ancient secrets. You note the signature of Tom Riddle imprinted at the end, an ominous shadow of its past owner. Its presence in this room raises a sense of curiosity and you can't help but wonder, could this book hold significant clues for your journey ahead? Don't forget this moment.",
    "prison": "The atmosphere is heavy in this space; it's reminiscent of a prison. To your right, a worn and faded picture clings onto the wall, its story seemingly lost to time. On the left, an unaccompanied book rests on a shelf, a solitary testament to knowledge and solitude. And nestled away in the corner, an almirah stands, its imposing silhouette shrouded in mystery and anticipation.",
    "almirah": "It's an old magical piece and I can see a magical wand inside it",
    "wand": "This is Sirius's wand, one of powerful wands exists. I am not sure, why it is here.",
    "picture": "As your eyes land on the aged picture hanging to your right, you recognize the face instantly - Sirius Black. His disheveled dark hair, his eyes brimming with rebellion, and his knowing grin all contribute to his unmistakable personality. The name 'Sirius Black' is inscribed beneath the frame on a worn-out brass plaque, perhaps a clue to unravel in this game."
}


# class ActionLook(Action):
#     def name(self) -> Text:
#         return "action_look"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         spoken = False
#         print("action_look")
#         room_1 = tracker.get_slot('current_room')

#         for blob in tracker.latest_message['entities']:
#             if blob['entity'] == 'object':
#                 dispatcher.utter_message(text=look_descriptions[blob['value']])
#                 spoken = True

            
#         if not spoken:
#             dispatcher.utter_message(room_1)
#         return []
class ActionLook(Action):
    def name(self) -> Text:
        return "action_look"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        spoken = False
        print("action_look")
        room = tracker.get_slot('current_room')
        has_key = tracker.get_slot('key')
        third_riddle_solved = tracker.get_slot('third_riddle_solved')
        alohomora = tracker.get_slot('alohomora')

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'object':
                if blob['value'] in look_descriptions:
                    dispatcher.utter_message(text=look_descriptions[blob['value']])
                    spoken = True
                else:
                    if(room == "room_1"):
                        dispatcher.utter_message(text="It a very dark and withered chamber. Seems quite old and cold. But I can see something. I can see a table, a box in the corner and a transfiguration vessel lying on the ground. Tell me which item you want to look?")
                    elif(room == "room_2" and not(third_riddle_solved)):
                        dispatcher.utter_message(text="The spectral figure of Celina manifests before your eyes, her phantom form floating eerily above the ground. The ethereal glow of her spectral image illuminates the space around, casting an array of haunting shadows that dance around the room.")
                    elif(room == "room_2" and third_riddle_solved):
                            dispatcher.utter_message(text="The spectral figure of Celina manifests before your eyes, her phantom form floating eerily above the ground. As her spectral image glows softly, you notice a metallic glint on the floor beneath her. A solitary key lies there, quietly beckoning for you to claim it.")
                    elif(room == "room_3"):
                        dispatcher.utter_message(text="The atmosphere is heavy in this space; it's reminiscent of a prison. To your right, a worn and faded picture clings onto the wall, its story seemingly lost to time. On the left, an unaccompanied book rests on a shelf, a solitary testament to knowledge and solitude. And nestled away in the corner, an almirah stands, its imposing silhouette shrouded in mystery and anticipation. ")
                    elif(alohomora == True and alohomora == False):
                        dispatcher.utter_message(text="You find yourself standing once again within the familiar, enchanting halls of Hogwarts. A rush of anticipation courses through your veins as you can hardly contain the excitement to share the tales of your extraordinary adventures with your friends. Each twist, each turn, every spell cast and mystery solved - you've got a story for the ages and can't wait to relive it with your comrades.")
                    spoken = True
        if not spoken:
            if(room == "room_1"):
                        dispatcher.utter_message(text="It a very dark and withered chamber. Seems quite old and cold. But I can see something. I can see a table, a box in the corner and a transfiguration vessel lying on the ground. Tell me which item you want to look?")
            elif(room == "room_2" and not(third_riddle_solved)):
                        dispatcher.utter_message(text="The spectral figure of Celina manifests before your eyes, her phantom form floating eerily above the ground. The ethereal glow of her spectral image illuminates the space around, casting an array of haunting shadows that dance around the room.")
            elif(room == "room_2" and third_riddle_solved):
                        dispatcher.utter_message(text="The spectral figure of Celina manifests before your eyes, her phantom form floating eerily above the ground. As her spectral image glows softly, you notice a metallic glint on the floor beneath her. A solitary key lies there, quietly beckoning for you to claim it.")
            elif(room == "room_3" and alohomora == False):
                        dispatcher.utter_message(text="The atmosphere is heavy in this space; it's reminiscent of a prison. To your right, a worn and faded picture clings onto the wall, its story seemingly lost to time. On the left, an unaccompanied book rests on a shelf, a solitary testament to knowledge and solitude. And nestled away in the corner, an almirah stands, its imposing silhouette shrouded in mystery and anticipation. ")
            elif(alohomora == True):
                        dispatcher.utter_message(text="You find yourself standing once again within the familiar, enchanting halls of Hogwarts. A rush of anticipation courses through your veins as you can hardly contain the excitement to share the tales of your extraordinary adventures with your friends. Each twist, each turn, every spell cast and mystery solved - you've got a story for the ages and can't wait to relive it with your comrades.")
           
            # dispatcher.utter_message(text="Sorry, I don't understand what you are trying to look at!")
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
        tom_solved = tracker.get_slot('tom_solved')

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
                        if item == 'wand' and tom_solved:
                            dispatcher.utter_message(text=f"Sirius: Well done! You finally found my wand. Let's hurry up. We are at the prison walls now. You have to cast Alohomora with me. I am too weak to cast it myself.")


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
    ('wand', 'walls'): "Super, wand is illuminating now, cast the spell - Alohomora!"
}
combinations.update({(i2, i1): v for (i1, i2), v in combinations.items()})

combination_results = {
    ('charm', 'potion'): "po-charm",
    ('potion', 'charm'): "po-charm",
    ('po-charm', 'vessel'): "enchanted_vessel",
    ('vessel', 'po-charm'): "enchanted_vessel"
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
        has_enchanted_vessel = tracker.get_slot('enchanted_vessel')  # Check if the enchanted_vessel is in the inventory

        if has_enchanted_vessel:
            dispatcher.utter_message(text="Good job ! Now you must hurry to the basement and you will find Celina there. Ask her way to escape from basement. She is a ghost and she will ask riddles to help you escape from the basement. Go down and call her name !")
            return [SlotSet("enchanted_vessel", False), SlotSet("evanseco_performed",True)] 
        else:
            dispatcher.utter_message(text="You don't have correct items in your inventory to cast the spell. Please check your inventory or pickup the item(s) to cast the spell.")

        return [SlotSet("evanseco_performed",True)]

class ActionMoveToRoom2(Action):
    def name(self):
        return "action_move_to_room_2"

    async def run(self, dispatcher, tracker, domain):
        evanseco_performed = tracker.get_slot('evanseco_performed')

        if evanseco_performed:
            dispatcher.utter_message(text="""Celina: Look who's there! Another Victim. Are you also trapped in the chamber little wizard? 
              Ha ha ha ha..... How about let's stay here forever? ;) 
              Unless you answer my three riddles. Each riddle has a meaning which resembles me.
              Combine them and make a meaningful sentence. If you give me the right sentence, I give you the key to run away from basement. 
              Riddle-1:- It can be seen, it can be felt, but it never heard, and never smelt. It comes every day at the end of time, and witches and Dracula love it cause now it's their time.""")
            return [SlotSet("current_room", "room_2")]
        else:
            dispatcher.utter_message(text="You attempted to call Celina, but she seems unable to hear you. It might be better to first find a way out of this room, and try calling her once you're in the next chamber.")
            return []


class ActionCheckFirstRiddle(Action):
    def name(self) -> Text:
        return "action_check_first_riddle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_room = tracker.get_slot('current_room')

        if current_room == "room_2":
            dispatcher.utter_message(text="That's the right answer! \n  Riddle-2:- It has mighty tall walls, all the riches, and also a dark prison to capture all the evil.")
            return [SlotSet("first_riddle_solved", True)]
        
        else:
            return [SlotSet("first_riddle_solved", False)]
        
class ActionCheckSecondRiddle(Action):
    def name(self) -> Text:
        return "action_check_second_riddle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_room = tracker.get_slot('current_room')
        first_riddle_solved = tracker.get_slot('first_riddle_solved')
        second_riddle_solved = tracker.get_slot('second_riddle_solved')

        if current_room == "room_2" and first_riddle_solved and not(second_riddle_solved):
            dispatcher.utter_message(text="Right again! Just one more and you are through! \n  Riddle-3:- Possesses magical powers, has never been seen without her magical cloak, and the black cat keeps flying around on broomsticks wearing her hat.")
            return [SlotSet("second_riddle_solved", True)]
        
        else:
            return [SlotSet("second_riddle_solved", False)]

class ActionCheckThirdRiddle(Action):
    def name(self) -> Text:
        return "action_check_third_riddle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_room = tracker.get_slot('current_room')
        second_riddle_solved = tracker.get_slot('second_riddle_solved')
        third_riddle_solved = tracker.get_slot('third_riddle_solved')

        if current_room == "room_2" and second_riddle_solved and not(third_riddle_solved):
            dispatcher.utter_message(text="Celina: Well done , Little Wizard! Here's your key. You can pick the key and use in the basement door to unlock it.")
            return [SlotSet("third_riddle_solved", True)]
        
        else:
            return [SlotSet("third_riddle_solved", False)]

# class ActionMoveToRoom2(Action):
#     def name(self):
#         return "action_move_to_room_2"

#     async def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message(text="""Celina: Look who's there! Another Victim. Are you also trapped in the chamber little wizard? 
#           Ha ha ha ha..... How about let's stay here forever? ;) 
#           Unless you answer my three riddles. Each riddle has a meaning which resembles me.
#           Combine them and make a meaningful sentence. If you give me the right sentence, I give you the key to run away from basement. 
#           Riddle-1:- It can be seen, it can be felt, but it never heard, and never smelt. It comes every day at the end of time, and witches and Dracula love it cause now it's their time. 
#           Riddle-2:- It has mighty tall walls, all the riches, and also a dark prison to capture all the evil.
#           Riddle-3:- Possesses magical powers, has never been seen without her magical cloak, and the black cat keeps flying around on broomsticks wearing her hat.""")
#         return [SlotSet("current_room", "room_2")]


# class ActionMoveToRoom2(Action):
#     def name(self):
#         return "action_move_to_room_2"

#     async def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message(text="Celina: Look who's there! Another Victim. Are you also trapped in the chamber little wizard? \
#           \ Ha ha ha ha..... How about let's stay here forever? ;) \n unless you answer my three riddles. Each riddle has a meaning which resembles me.\n 
#           Combine them and make a meaningful sentence. If you give me the right sentence, I give you the key to run away from basement. \n
#           \ Riddle-1:- It can be seen, it can be felt, but it never heard, and never smelt. It comes every day at the end of time, and witches and Dracula love it cause now it's their time. \n
#           \ Riddle-2:- It has mighty tall walls, all the riches, and also a dark prison to capture all the evil.\n
#           \ Riddle-3:- Possesses magical powers, has never been seen without her magical cloak, and the black cat keeps flying around on broomsticks wearing her hat.")
#         return [SlotSet("current_room", "room_2")]

# class ActionMoveToRoom3(Action):
#     def name(self):
#         return "action_move_to_room_3"

#     async def run(self, dispatcher, tracker, domain):
#         return [SlotSet("current_room", "room_3")]

class ActionShowMap(Action):
    def name(self):
        return "action_show_map"

    async def run(self, dispatcher, tracker, domain):
        room = tracker.get_slot('current_room')
        dispatcher.utter_message(text=f"You are currently in {room}.")
