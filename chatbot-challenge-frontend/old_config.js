let config;

config = {
    "name": "hello world",
    "rooms": [
        {
            "escape_room_name": "Lokal Demo",
            "chatbot_name": "local-bot",
            "user_name": "Oha Oha Oha",
            "messagebox_caption": "hmmm?...",
            "send_button_caption": "oha?",
            "user_name": "you",
            "id": "lokal",
            "background-image": "local-bot-background-image.jpg",
            "api_url": "http://localhost:5005",
            "welcome-message": "does it wörk?"
        },
        {
            "escape_room_name": "Under the sea",
            "chatbot_name": "Neptun",
            "user_name": "Erika Musterfrau",
            "messagebox_caption": "Type here...",
            "send_button_caption": "Swim",
            "user_name": "Erika Musterfrau",
            "id": "under-the-sea",
            "background-image": "under-the-sea-background-image.jpg",
            "api_url": "https://vm014.qu.tu-berlin.de/api5005",
            "welcome-message": "You are under the sea."
        },
        {
            "escape_room_name": "House of horrors",
            "chatbot_name": "Susie",
            "id": "house-of-horrors",
            "api_url": "https://vm014.qu.tu-berlin.de/api5005",
            "welcome-message": "You are in the horror house."
        },
        {
            "escape_room_name": "Jazz Club",
            "id": "jazz-club",
            "api_url": "https://vm014.qu.tu-berlin.de/api5005",
            "welcome-message": "You are in the Jazz Club escape room.",
            "background-image": "jazz-club-background-image.png",
            "chatbot-avatar": "jazz_club_avatar1.jpg",
            "user-avatar": "jazz_club_avatar2.jpg"
        }
    ]
};

export { config }
