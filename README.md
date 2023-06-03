"# chatbot_escapegame_Group2"

# Changes by Taif

03/06/2023

*Implemented the SpaCy pipeline, which allows the extraction of common English based names from a sentence.
*Troublshooted the issue where the action_pickup function was called after every prompt giving wrong uttering.
For e.g Stating that the item was already in the inventory, whereas the the pickup action was being used the first time.
*The name has to be a common English based name, AND it has to be provided in a full sentence. 




30/05/2023
Implemented Room 2
Added functionality for the key, without key door doesn't open
Key appears in the inventory on correct solution
Added Custom Name on greet

Possible issues:

Answer to the riddle is not flexible
Sequence can be skipped if the keywords for other things are known
Name cannot be one Word, whole sentence is to be provided.
