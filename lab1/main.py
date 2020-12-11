from single_byte_xor import SingleByteXorAttacker
from repeating_key_xor import RepeatingKeyXorAttacker
from substitution import SubstitutionAttacker, Substitution, ALPHABET, IndividualSet, Individual


def execute_task_1():
    print("======TASK 1======")
    task_1 = "Yx`7cen7v7ergrvc~yp:|rn7OXE7t~g.re97R9p97~c7d.xb{s7cv|r7v7dce~yp75.r{{x7`xe{s57vys;7p~ary7c.r7|rn7" \
             "~d75|rn5;7oxe7c.r7q~edc7{rccre75.57`~c.75|5;7c.ry7oxe75r57`~c.75r5;7c.ry75{57`~c.75n5;7vys7c.ry7ox" \
             "e7yroc7t.ve75{57`~c.75|57vpv~y;7c.ry75x57`~c.75r57vys7dx7xy97Nxb7zvn7bdr7vy7~ysro7xq7tx~yt~srytr;7" \
             "_vzz~yp7s~dcvytr;7\vd~d|~7rovz~yvc~xy;7dcvc~dc~tv{7crdcd7xe7`.vcrare7zrc.xs7nxb7qrr{7`xb{s7d.x`7c." \
             "r7urdc7erdb{c9"
    SingleByteXorAttacker.attack(task_1)


def execute_task_2():
    print("======TASK 2======")
    task_2 = "1c41023f564b2a130824570e6b47046b521f3f5208201318245e0e6b40022643072e13183e51183f5a1f3e4702245d4b28" \
             "5a1b23561965133f2413192e571e28564b3f5b0e6b50042643072e4b023f4a4b24554b3f5b0238130425564b3c564b3c5a" \
             "0727131e38564b245d0732131e3b430e39500a38564b27561f3f5619381f4b385c4b3f5b0e6b580e32401b2a500e6b5a18" \
             "6b5c05274a4b79054a6b67046b540e3f131f235a186b5c052e13192254033f130a3e470426521f22500a275f126b4a043e" \
             "131c225f076b431924510a295f126b5d0e2e574b3f5c4b3e400e6b400426564b385c193f13042d130c2e5d0e3f5a086b52" \
             "072c5c192247032613433c5b02285b4b3c5c1920560f6b47032e13092e401f6b5f0a38474b32560a391a476b4002264607" \
             "2a470e2f130a255d0e2a5f0225544b24414b2c410a2f5a0e25474b2f56182856053f1d4b185619225c1e385f1267131c39" \
             "5a1f2e13023f13192254033f13052444476b4a043e131c225f076b5d0e2e574b22474b3f5c4b2f56082243032e414b3f5b" \
             "0e6b5d0e33474b245d0e6b52186b440e275f456b710e2a414b225d4b265a052f1f4b3f5b0e395689cbaa186b5d046b401b" \
             "2a500e381d4b23471f3b4051641c0f2450186554042454072e1d08245e442f5c083e5e0e2547442f1c5a0a64123c503e02" \
             "7e040c413428592406521a21420e184a2a32492072000228622e7f64467d512f0e7f0d1a"
    RepeatingKeyXorAttacker.attack(task_2)


def execute_task_3():
    print("======TASK 3======")
    task_3 = "EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPVYWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQES" \
             "PBLWPCSVRVWFLHLWFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYULEMQTLPPLUGUYOLWDTVSQETHQEK" \
             "LPVPVSMTLEUPQEPCYAMEWWYTYWDLUULTCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUMQBQVMQCYAH" \
             "UYKEKTCASLFPYFLMVHQLUPQLHULIVYASHEUEDUEHQBVTTPQLVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCP" \
             "YFVIVFLPQLOLSSEDLVWHEUPSKCPQLWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGULXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGV" \
             "WFEBECPYASLQVDQLUYUFLUGULXALWMCSPEPVSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPOEDVMETBYUFBVTTPENLPYPQLWLRPTE" \
             "KLWZYCKVPTCSTESQPQULLGYAUMEHVPETFWMEHVPETBZMEHVPETB"
    SubstitutionAttacker(individual_set_members_count=1,
                         min_population_size=100,
                         max_population_size=1000,
                         iterations_count=500,
                         mutations_percentage=0.4,
                         best_percentage=30).attack(task_3)
    task_3_b = bytearray(task_3.lower().encode())
    keys_b = [bytearray('ekmflgdqvzntowyhxuspaibrcj'.encode())]
    key_set = IndividualSet(Individual)
    for key in keys_b:
        key_set.append(Individual(key))
    print(f"Found keys: {keys_b} with fitness {key_set.calc_fitness(task_3_b)}")
    print(f"Found text: {Substitution(ALPHABET).decrypt(task_3_b, keys_b)}")


def execute_task_4():
    print("======TASK 4======")
    task_4 = "KZBWPFHRAFHMFSNYSMNOZYBYLLLYJFBGZYYYZYEKCJVSACAEFLMAJZQAZYHIJFUNHLCGCINWFIHHHTLNVZLSHSVOZDPYSMNYJX" \
             "HMNODNHPATXFWGHZPGHCVRWYSNFUSPPETRJSIIZSAAOYLNEENGHYAMAZBYSMNSJRNGZGSEZLNGHTSTJMNSJRESFRPGQPSYFGSW" \
             "ZMBGQFBCCEZTTPOYNIVUJRVSZSCYSEYJWYHUJRVSZSCRNECPFHHZJBUHDHSNNZQKADMGFBPGBZUNVFIGNWLGCWSATVSSWWPGZH" \
             "NETEBEJFBCZDPYJWOSFDVWOTANCZIHCYIMJSIGFQLYNZZSETSYSEUMHRLAAGSEFUSKBZUEJQVTDZVCFHLAAJSFJSCNFSJKCFBC" \
             "FSPITQHZJLBMHECNHFHGNZIEWBLGNFMHNMHMFSVPVHSGGMBGCWSEZSZGSEPFQEIMQEZZJIOGPIOMNSSOFWSKCRLAAGSKNEAHBB" \
             "SKKEVTZSSOHEUTTQYMCPHZJFHGPZQOZHLCFSVYNFYYSEZGNTVRAJVTEMPADZDSVHVYJWHGQFWKTSNYHTSZFYHMAEJMNLNGFQNF" \
             "ZWSKCCJHPEHZZSZGDZDSVHVYJWHGQFWKTSNYHTSZFYHMAEDNJZQAZSCHPYSKXLHMQZNKOIOKHYMKKEIKCGSGYBPHPECKCJJKNI" \
             "STJJZMHTVRHQSGQMBWHTSPTHSNFQZKPRLYSZDYPEMGZILSDIOGGMNYZVSNHTAYGFBZZYJKQELSJXHGCJLSDTLNEHLYZHVRCJHZ" \
             "TYWAFGSHBZDTNRSESZVNJIVWFIVYSEJHFSLSHTLNQEIKQEASQJVYSEVYSEUYSMBWNSVYXEIKWYSYSEYKPESKNCGRHGSEZLNGHT" \
             "SIZHSZZHCUJWARNEHZZIWHZDZMADNGPNSYFZUWZSLXJFBCGEANWHSYSEGGNIVPFLUGCEUWTENKCJNVTDPNXEIKWYSYSFHESFPA" \
             "JSWGTYVSJIOKHRSKPEZMADLSDIVKKWSFHZBGEEATJLBOTDPMCPHHVZNYVZBGZSCHCEZZTWOOJMBYJSCYFRLSZSCYSEVYSEUNHZ" \
             "VHRFBCCZZYSEUGZDCGZDGMHDYNAFNZHTUGJJOEZBLYZDHYSHSGJMWZHWAFTIAAY"
    key_length = RepeatingKeyXorAttacker.get_key_length(bytearray(task_4.lower().encode()))
    SubstitutionAttacker(individual_set_members_count=key_length,
                         min_population_size=100,
                         max_population_size=1000,
                         iterations_count=2000,
                         mutations_percentage=0.4,
                         best_percentage=30).attack(task_4)
    task_4_b = bytearray(task_4.lower().encode())
    keys_b = [bytearray(b'fxplstobqzywraihknjcdgemvu'), bytearray(b'vkhgsroezacyutfjnwdixmlpbq'),
              bytearray(b'vrmaseubojgcinldfzphwqykxt'), bytearray(b'khqemfpwuxlabgzovstryindcj')]
    key_set = IndividualSet(Individual)
    for key in keys_b:
        key_set.append(Individual(key))
    print(f"Found keys: {keys_b} with fitness {key_set.calc_fitness(task_4_b)}")
    print(f"Found text: {Substitution(ALPHABET).decrypt(task_4_b, keys_b)}")


if __name__ == '__main__':
    # TASK 1
    execute_task_1()

    # TASK 2
    execute_task_2()

    # TASK 3
    execute_task_3()

    # TASK 4
    execute_task_4()
