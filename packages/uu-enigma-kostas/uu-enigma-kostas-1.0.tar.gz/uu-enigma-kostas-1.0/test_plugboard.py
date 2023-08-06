from plugboard import Plugboard

def test_plugboard():
    #test code
    connections_to_make = {"W": "H", "A": "B", "o": "e" }
    plug = Plugboard(connections_to_make)
    # t = plug.plugboard_encrypt_the_letters("Hello world")
    # print(t)
    assert connections_to_make == {"W": "H", "A": "B", "o": "e" }
    assert plug.plugboard_encrypt_the_letters("Hello world") == "WOLLEHERLD"

