import json 


def user_input(type_: str) -> str:
    inp = input(f"please input your {type_}: ")
    
    if inp and inp != "\n":
        return inp.strip()

    else:
        return user_input(type_)

def first_load() -> bool:
    try:
        with open("secrets.json", "r") as file:
            file = json.load(file)
            client_id = file["client_id"]
            client_secret = file["client_secret"]
            playlist_id = file["playlist_id"]

    except FileNotFoundError:
        print("creating secrets file")
        adder = {"client_id": "", "client_secret": "", "playlist_id": ""}
        with open("secrets.json", "w") as file:
            json.dump(adder, file, indent= 4)

        first_load()
    
    else:
        if not client_id:
            client_id = user_input("client id")

        if not client_secret:
            client_secret = user_input("client secret")

        if not playlist_id:
            playlist_link = user_input("playlist link")
            playlist_id = playlist_link.split("?")[0].split("/")[-1]

        adder = {"client_id": client_id, "client_secret": client_secret, "playlist_id": playlist_id}
        
        with open("secrets.json", "w") as file:
            json.dump(adder, file, indent= 4)
    
    return True

