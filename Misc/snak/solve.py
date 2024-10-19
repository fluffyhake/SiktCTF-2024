from pwn import *

r = remote('challenges.ctf.sikt.no', 5010)


def find_coordinates(playing_field, character):
    for row, entry in enumerate(playing_field):
        column_index = entry.find(character)
        if column_index != -1:
            return {"x": column_index, "y": row}
    return {"x": None, "y": None}

def send_command_and_recieve_new_playing_field(command):
    try:
        r.sendline(command)
        playing_field = r.recvuntil(b't): ')
        playing_field = playing_field.decode("utf-8").split("\n")


        score = playing_field[1]
        playing_field.pop(0)
        playing_field.pop(0)
        playing_field.pop(-1)
        return [playing_field, score]
    except Exception as e:
        print(f"Error occurde: {e}")
        raise


if __name__ == "__main__":
    score = ""
    print(r.recvuntil(b'[Y/n]: '))
    r.sendline("Y")
    playing_field = r.recvuntil(b't): ')

    playing_field = playing_field.decode("utf-8").split("\n")
    playing_field.pop(0)
    playing_field.pop(0)
    playing_field.pop(-1)

    while True:
        pprint(playing_field)

        print(score)
        if "99" in score:
            r.interactive()
            break

  

        player_coordinates = find_coordinates(playing_field, "o")
        point_coordinates = find_coordinates(playing_field, "g")

        print(player_coordinates)
        print(point_coordinates)

        

        if(player_coordinates["y"] > point_coordinates["y"]):
            command = "1"

        elif(player_coordinates["y"] < point_coordinates["y"]):
            command = "2"

        elif(player_coordinates["x"] > point_coordinates["x"]):
            command = "3"

        elif(player_coordinates["x"] < point_coordinates["x"]):
            command = "4"



        result = send_command_and_recieve_new_playing_field(command)


        playing_field = result[0]
        score = result[1]
