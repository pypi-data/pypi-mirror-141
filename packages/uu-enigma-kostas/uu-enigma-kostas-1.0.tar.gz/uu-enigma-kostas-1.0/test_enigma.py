from enigma_run import enigma_encrypt

def test_enigma_run():
    message1 = "Hello world and the whole world this is a very long message that I use to test whether the wheels spin as they should".upper().replace(" ", "")
    message2 = "CMAAYXYKAGLPGSCMXCYAMXYKAGSCUTUTLFMKOAYPDEMTTLDMSCLSUITMSYSMTSXCMSCMKSCMXCMMATTNUPLTSCMOTCYIAG"

    assert message1 == enigma_encrypt(message2, "123")
    assert message2 == enigma_encrypt(message1, "123")