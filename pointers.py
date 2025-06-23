import math
import re
import pymem


class Pointers:
    def __init__(self, pid):
        self.pm = pymem.Pymem()
        self.pm.open_process_from_id(pid)
        self.CLIENT = self.pm.base_address

        self.DC_POINTER = 0x012CE35C
        self.CHAR_NAME_POINTER = 0x011450EC
        self.LEVEL_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x3C4])
        self.HP_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x3B8])
        self.HP_PLUS_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0xE4])
        self.HP_BUFF_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0xE0])
        self.MAX_HP_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0xDC])

        self.MANA_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x3BC])
        self.MANA_BUFF_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x6F0])
        self.MAX_MANA_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x6EC])

        self.X_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x810])
        self.Y_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x814])

        self.BATTLE_STATUS_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x854])
        self.SIT_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x290])

        self.PET_POINTER = self.get_pointer(self.CHAR_NAME_POINTER, offsets=[0x10A8])

        self.TARGET_HP_POINTER = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x59C, 0x0, 0xC, 0x1F4, 0x15C, 0x480])
        self.TARGET_SELECT = self.get_pointer(self.CLIENT + 0x00EC05C8, offsets=[0xD0, 0x2DC, 0x24, 0xC10])
        self.TARGET_NAME_POINTER = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xB1C, 0x0, 0xC, 0x1F8, 0x43C])
        self.TARGET_NAME_POINTER_2 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xB1C, 0x0, 0xC, 0xD9C])
        self.TARGET_NAME_POINTER_3 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xB1C, 0x0, 0xC, 0xD9C, 0x9AC])

        self.TEAM_SIZE_POINTER = self.get_pointer(0x0106D328, offsets=[0x3D8])
        self.TEAM_NAME_1 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x77C, 0x0, 0xC, 0x678, 0x8B4])
        self.TEAM_NAME_2 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x34C, 0x0, 0xC, 0x678, 0x8B4])
        self.TEAM_NAME_3 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x3F4, 0x0, 0xC, 0x1F4, 0x15C])
        self.TEAM_NAME_4 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xA1C, 0x0, 0xC, 0x1F4, 0x54])

        self.BAG_OPEN_POINTER = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x5C4, 0x0, 0xC, 0x1F8, 0x42C, 0xBA0])

        self.PET_ACTIVE_POINTER = self.get_pointer(0x11450EC, offsets=[0x10A8])
        #print("Pointers initialized.", pid)

    def get_pointer(self, base_address, offsets) -> int | None:
        """
        Calcula o ponteiro final seguindo uma cadeia de offsets.
        """
        try:
            address = base_address
            for offset in offsets:  # Navega pelos offsets até o endereço final
                address = self.pm.read_int(address) + offset
            return address
        except Exception as e:
            #print(f"Erro ao calcular o ponteiro: {e}")
            return None

    def read_value(self, address, data_type="byte") -> int | float| None:
        try:
            if data_type == "byte":
                return self.pm.read_bytes(address, 1)[0]  # Lê 1 byte
            elif data_type == "int":
                return self.pm.read_int(address)  # Lê 4 bytes como inteiro
            elif data_type == "float":
                return self.pm.read_float(address)  # Lê 4 bytes como float
            else:
                print(f"Tipo de dado desconhecido: {data_type}")
                return None
        except Exception as e:
            #print(f"Erro ao ler valor ({data_type}): {e}")
            return None

    def read_string_from_pointer(self, base_pointer, offset=0, max_length=50) -> str:
        try:
            pointer_address = self.pm.read_int(base_pointer)
            final_address = pointer_address + offset
            byte_data = self.pm.read_bytes(final_address, max_length)
            string_data = byte_data.split(b'\x00', 1)[0].decode('utf-8', errors='ignore')
            return string_data
        except Exception as e:
            print(f"String Error: {e}")
            return "Offline Account"

    def get_char_name(self) -> str:
        name = self.read_string_from_pointer(self.CHAR_NAME_POINTER, offset=0xBC, max_length=50)

        if re.match(r"^[\w]+$", name):  # Alfanumérico | Alphanumeric
            return name

        # Segunda tentativa
        pointer = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0xBC])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def get_target_name(self) -> str:
        val = self.read_string_from_pointer(self.TARGET_NAME_POINTER_3, offset=0x0, max_length=50)
        if val == 'Offline Account':
            val = self.read_string_from_pointer(self.TARGET_NAME_POINTER, offset=0x9AC, max_length=50)
        return val

    def team_name_1(self) -> str:
        name = self.read_string_from_pointer(self.TEAM_NAME_1, offset=0x4F4, max_length=50)

        if re.match(r"^[\w]+$", name):  # Alfanumérico
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x77C, 0x0, 0xC, 0x678, 0x8B4, 0x4F4])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def team_name_2(self) -> str:
        name = self.read_string_from_pointer(self.TEAM_NAME_2, offset=0x4F4, max_length=50)
        if re.match(r"^[\w]+$", name):
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x34C, 0x0, 0xC, 0x678, 0x8B4, 0x4F4])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def team_name_3(self) -> str:
        name = self.read_string_from_pointer(self.TEAM_NAME_3, offset=0x54, max_length=50)
        if re.match(r"^[\w]+$", name):
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x3F4, 0x0, 0xC, 0x1F4, 0x15C, 0x54])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def team_name_4(self) -> str:
        name = self.read_string_from_pointer(self.TEAM_NAME_4, offset=0x54, max_length=50)
        if re.match(r"^[\w]+$", name):
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xA1C, 0x0, 0xC, 0x1F4, 0x54, 0x54])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def get_level(self) -> int:
        return self.read_value(self.LEVEL_POINTER, data_type="byte")

    def is_target_selected(self) -> bool:
        if self.TARGET_SELECT is None:
            print("Erro: Ponteiro TARGET_SELECT não calculado.")
            return False

        target = self.read_value(self.TARGET_SELECT, data_type="byte")  # Lê 1 byte
        return target == 1

    def target_hp(self) -> int:
        hp = self.read_value(self.TARGET_HP_POINTER, data_type="int")
        return hp

    def pet_active(self) -> bool:
        hp = self.pm.read_bool(self.PET_ACTIVE_POINTER)
        return hp

    def target_hp_full(self) -> bool:
        return self.read_value(self.TARGET_HP_POINTER, data_type="int") == 597

    def is_target_dead(self) -> bool:
        dead = self.read_value(self.TARGET_HP_POINTER, data_type="int")
        return dead == 0

    def get_hp(self) -> int:
        return self.read_value(self.HP_POINTER, data_type="int")

    def get_hp_plus(self) -> int:
        plus = self.read_value(self.HP_PLUS_POINTER, data_type="byte")
        if plus >= 100:
            return plus - 100
        else:
            return plus

    def get_hp_buff(self) -> int:
        return self.read_value(self.HP_BUFF_POINTER, data_type="int")

    def get_max_hp(self) -> int:
        base_hp = self.read_value(self.MAX_HP_POINTER, data_type="int")
        buff_hp = self.get_hp_buff()
        hp_total = base_hp + buff_hp
        plus = self.get_hp_plus()

        if plus == 1:
            return base_hp
        else:
            return math.floor(((hp_total * plus) / 100) + hp_total)

    def get_mana(self) -> int:
        return self.read_value(self.MANA_POINTER, data_type="int")

    def get_mana_buff(self) -> int:
        return self.read_value(self.MANA_BUFF_POINTER, data_type="int")

    def get_max_mana(self) -> int:
        base_mana = self.read_value(self.MAX_MANA_POINTER, data_type="int")
        buff_mana = self.get_mana_buff()
        mana_total = base_mana + buff_mana
        return mana_total

    def is_in_battle(self) -> bool:
        battle = self.read_value(self.BATTLE_STATUS_POINTER, data_type="byte")
        if battle == 1:
            #print("Battle Status")
            return True
        return False

    def is_sitting(self) -> bool:
        sitting = self.read_value(self.SIT_POINTER, data_type="byte")
        if sitting == 200:
            return True
        return False

    def get_x(self) -> int:
        x = self.read_value(self.X_POINTER, data_type="float") / 20
        return x > 0 and math.floor(x) or math.ceil(x)

    def get_y(self) -> int:
        y = self.read_value(self.Y_POINTER, data_type="float") / 20
        return y > 0 and math.floor(y) or math.ceil(y)

    def is_bag_open(self) -> bool:
        bag = self.read_value(self.BAG_OPEN_POINTER, data_type="int")
        if bag == 903:
            return True
        return False

    def get_team_size(self) -> int:
        team = self.read_value(self.TEAM_SIZE_POINTER, data_type="int")
        return team or 0

    def get_dc(self) -> int:
        dc = self.read_value(self.DC_POINTER, data_type="int")
        return dc

def main():
    # Testando o código
    pid = 972  # Substitua 972 pelo PID do processo correto
    p = Pointers(pid)

    if p.is_target_selected():
        print("Um alvo está selecionado!")
    else:
        print("Nenhum alvo está selecionado.")

    name = p.get_char_name()
    print(f"CHAR_NAME: {name}")
    level = p.get_level()
    print(f"LEVEL: {level}")
    team_name_1 = p.team_name_1()
    print(f"TEAM_NAME_1: {team_name_1}")
    team_name_2 = p.team_name_2()
    print(f"TEAM_NAME_2: {team_name_2}")
    team_name_3 = p.team_name_3()
    print(f"TEAM_NAME_3: {team_name_3}")
    team_name_4 = p.team_name_4()
    print(f"TEAM_NAME_4: {team_name_4}")
    hp = p.target_hp()
    print(f"TARGET_HP: {hp}")
    target_name = p.get_target_name()
    print(f"TARGET_NAME: {target_name}")
    get_hp = p.get_hp()
    print(f"CHAR_HP : {get_hp}")
    hp_plus = p.get_hp_plus()
    print(f"CHAR_HP_PLUS : {hp_plus}")
    hp_buff = p.get_hp_buff()
    print(f"CHAR_HP_BUFF : {hp_buff}")
    max_hp = p.get_max_hp()
    print(f"CHAR_MAX_HP : {max_hp}")
    battle = p.is_in_battle()
    print(f"CHAR_BATTLE_STATUS : {battle}")
    mana = p.get_mana()
    print(f"CHAR_MANA : {mana}")
    mana_buff = p.get_mana_buff()
    print(f"CHAR_MANA_BUFF : {mana_buff}")
    max_mana = p.get_max_mana()
    print(f"CHAR_MAX_MANA : {max_mana}")
    sit = p.is_sitting()
    print(f"CHAR_SIT : {sit}")
    x_pos = p.get_x()
    print(f"CHAR_X_POS : {x_pos}")
    y_pos = p.get_y()
    print(f"CHAR_Y_POS : {y_pos}")
    bag_open = p.is_bag_open()
    print(f"CHAR_BAG_OPEN : {bag_open}")
    team_size = p.get_team_size()
    print(f"TEAM_SIZE : {team_size}")
    dc = p.get_dc()
    print(f"CHAR_DC : {dc}")

if __name__ == "__main__":
    main()
