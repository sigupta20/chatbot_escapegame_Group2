let config;

config = {
    "name": "Magical Chamber in Hogwarts",
    "rooms": [
        {
            "escape_room_name": "Magical Chamber in Hogwarts",
            "chatbot_name": "magical-guide",
            "user_name": "Magical Wizard",
            "messagebox_caption": "type......",
            "send_button_caption": "Send",
            "id": "magical-chamber-room",
            "background-image": "harry-potter-theme-image.jpg",
            "api_url": "http://localhost:5005",
            "welcome-message": "Hi Wizard ! Welcome to the Hogwart's dark chambers where you are trapped by evil Lord Voldemort! He wants you to be trapped here forever. But you must find your way to escape, so that you can return to Hogwart's. You have to escape from this chamber by passing from various rooms and find artifacts, solve puzzles to unlock yourself from each room. You can ask for help/hint if you lost in game. Good luck!\n You can choose one option:- Start or Instructions"
        }
    ]
};

export { config }
