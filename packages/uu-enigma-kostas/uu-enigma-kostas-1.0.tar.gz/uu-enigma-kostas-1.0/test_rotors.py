
from rotors import Rotor, Reflector
#test code
# for rotors
def test_rotors():
    decrypts = ["ZIRRCYWC", "UDHHRSTR", "GFKKWCOW", "YLWWMSJM", "TPQQXJFX"]
    for i, decrypt in zip(range(0,5), decrypts):
        rotor = Rotor(i)
        # print(rotor.wiring_dict)
        # print(rotor.rottor_encrypt_the_letter("Hello bro"))
        # print(rotor.rottor_decrypt_the_letter(decrypts[i]))
        # print(rotor.notchposition)
        
        # assert rotor.rottor_encrypt_the_letter("Hello bro") == decrypts[i]
        # assert rotor.rottor_decrypt_the_letter(decrypts[i]) == "HELLOBRO"

test_rotors()

# test code
# for reflectors
def test_reflectors():
    refl = Reflector(1)
    # print(refl.part1_of_pairs)
    # print(refl.part2_of_pairs)
    # print(refl.wiring_dict)
    # print(refl.reflector_change_the_letter("Hello bro"))
    # print(refl.reflector_change_the_letter("LAHHGNKG"))
    assert refl.reflector_change_the_letter("Hello bro") == "LAHHGNKG"
    assert refl.reflector_change_the_letter("LAHHGNKG") == "HELLOBRO"

test_reflectors()