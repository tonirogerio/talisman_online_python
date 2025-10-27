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
        self.GOLD_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x410])

        self.MANA_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x3BC])
        self.MANA_BUFF_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x6F0])
        self.MAX_MANA_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x6EC])

        self.X_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x810])
        self.Y_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x814])

        self.BATTLE_STATUS_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x854])
        self.SIT_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x290])

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
        self.BAG_1 = self.get_pointer(0x011450EC, offsets=[0x838, 0xC4, 0x0, 0x8, 0x10])
        self.BAG_2 = self.get_pointer(0x011450EC, offsets=[0x838, 0xC4, 0x4, 0x8, 0x10])
        self.MOUNT_STATUS_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x8B0])
        self.BUFFS_QUANTITY_POINTER = self.get_pointer(self.CLIENT + 0x00C20980, offsets=[0xCBC])

        self.PET_ACTIVE_POINTER = self.get_pointer(0x11450EC, offsets=[0x10A8])

        # self.LOOT_POINTER = self.get_pointer(0x012C05C8, offsets=[0xD0, 0x7F4, 0x0, 0x24, 0x40])
        self.LOOT_POINTER = self.get_pointer(self.CLIENT + 0x00EC05C8, offsets=[0xD0, 0x7F4, 0x0, 0x24, 0x40])
        self.LOOT_WINDOW = 0x0105B958

        self.FIRST_LINK_SUR = self.get_pointer(0x012CE2DC, offsets=[0x18, 0x8C, 0x3C])

        self.TARGET_ID = 0x115CB20
        self.base = 0x0107C6B0
        self.basei = 0x0

        # Limites para busca bidirecional
        self.BASE_MIN = 0x0000CE00  # Limite inferior para busca
        self.BASE_MAX = 0x0EFFFFFF  # Limite superior para busca

        self.ZOOM_POINTER = self.get_pointer(0x116FFF4, offsets=[0x64])
        self.ROTATION_POINTER = self.get_pointer(0x116FFF4, offsets=[0x5C])
        self.ANGLE_POINTER = self.get_pointer(0x116FFF4, offsets=[0x60])
        self.CONFIRM_BOX_POINTER = 0x012CE35C
        self.LOCATION_POINTER = self.get_pointer(0x011450EC, offsets=[0x7F8, 0xF4])
        self.LOCATION_POINTER_2 = self.get_pointer(0x011450EC, offsets=[0x7F8, 0xF4, 0x44C])
        self.NOTIFICATION_POINTER = 0x0117097C
        self.DIALOG_POINTER = self.get_pointer(0x0117B27C, offsets=[0x70, 0x56C, 0xC, 0x4, 0x42C, 0x1F8, 0x240])
        self.SIN_PASSIVE = self.get_pointer(0x11450EC, offsets=[0x3E4])
        self.MONK_PASSIVE = self.get_pointer(0x11450EC, offsets=[0x3E0])
        self.SYSTEM_MENU_POINTER = 0x012DC1F5

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

    def read_string_from_pointer(self, base_pointer, offset=0, max_length=50) -> str | None:
        try:
            pointer_address = self.pm.read_int(base_pointer)
            final_address = pointer_address + offset
            byte_data = self.pm.read_bytes(final_address, max_length)
            string_data = byte_data.split(b'\x00', 1)[0].decode('utf-8', errors='ignore')
            return string_data
        except Exception as e:
            #print(f"String Error: {e}")
            return None

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

    def get_gold(self) -> int:
        """returns a string as: f'{gold}{silver}{copper}'"""
        return self.read_value(self.GOLD_POINTER, data_type="int")

    def bag_1_quantity(self) -> int:
        return self.read_value(self.BAG_1, data_type="int")

    def bag_2_quantity(self) -> int:
        return self.read_value(self.BAG_2, data_type="int")

    def mount(self) -> bool:
        mount = self.read_value(self.MOUNT_STATUS_POINTER, data_type="int")
        return bool(mount)

    def get_target_id(self):
        id = self.read_value(self.TARGET_ID, data_type="int")
        # print(f"Target ID: {id}")
        if id is None:
            print("Erro ao ler ID")
            return None  # Retorna None de forma explícita para evitar erros

        try:
            return hex(id)[2:].upper()
        except Exception as e:
            print(f"Erro ao converter ID para hexadecimal: {e}")
            return None  # Retorna None se houver qualquer erro na conversão

    def get_id(self):
        id = self.read_value(self.TARGET_ID, data_type="int")
        # print(f"ID: {id}")
        return id


    def search_id(self):
        final_pointer = 0
        max_attempts = 3  # Número máximo de tentativas completas
        erro_count = 0  # Contador para limitar mensagens de erro

        for attempt in range(max_attempts):
            try:
                # Obtém o ID do alvo
                targetid = self.get_target_id()
                if targetid is None:
                    print("Reiniciando busca: ID do alvo não encontrado")
                    continue  # Passa para a próxima tentativa

                found = False
                erro_count = 0  # Reinicia contador de erros para cada nova tentativa

                # Busca crescente (do base atual até BASE_MAX)
                current_base = self.base
                while current_base <= self.BASE_MAX:
                    # Lê o valor no endereço base atual
                    a = self.read_value(current_base + self.basei, "int")
                    if a is None:
                        # Limita mensagens de erro
                        erro_count += 1
                        if erro_count <= 1:
                            print("Erro de leitura na busca crescente, pulando para próxima tentativa...")
                        # Reinicia a busca completamente em vez de continuar com erros
                        break

                    b = a + 0x8

                    # Lê o valor no endereço calculado
                    c_value = self.read_value(b, "int")
                    if c_value is None:
                        # Avança para o próximo endereço sem mostrar erro
                        current_base += 0x4
                        continue

                    c = hex(c_value)[2:].upper()

                    if c == targetid:
                        final_pointer = current_base
                        found = True
                        break
                    else:
                        current_base += 0x4

                # Se houve erro na busca crescente, reinicia a tentativa
                if erro_count > 0:
                    continue

                # Se não encontrou na busca crescente, tenta busca decrescente
                if not found:
                    print("Iniciando busca decrescente...")
                    current_base = self.base - 0x4
                    erro_count = 0  # Reinicia contador para a busca decrescente

                    while current_base >= self.BASE_MIN:
                        # Lê o valor no endereço base atual
                        a = self.read_value(current_base + self.basei, "int")
                        if a is None:
                            # Limita mensagens de erro
                            erro_count += 1
                            if erro_count <= 1:
                                print("Erro de leitura na busca decrescente, pulando para próxima tentativa...")
                            # Reinicia a busca completamente em vez de continuar com erros
                            break

                        b = a + 0x8

                        # Lê o valor no endereço calculado
                        c_value = self.read_value(b, "int")
                        if c_value is None:
                            # Avança para o próximo endereço sem mostrar erro
                            current_base -= 0x4
                            continue

                        c = hex(c_value)[2:].upper()

                        if c == targetid:
                            final_pointer = current_base
                            found = True
                            break
                        else:
                            current_base -= 0x4

                # Se houve erro na busca decrescente, reinicia a tentativa
                if erro_count > 0:
                    continue

                # Se encontrou o alvo em qualquer uma das buscas
                if found:
                    # Lê o ponteiro final e as coordenadas em uma única verificação
                    pointer = self.read_value(final_pointer + self.basei, "int")
                    if pointer is None:
                        print("Reiniciando: falha ao ler ponteiro final")
                        continue

                    # Lê as coordenadas X e Y
                    x_value = self.read_value(pointer + 0x810, "float")
                    y_value = self.read_value(pointer + 0x814, "float")

                    # Verifica se ambas as coordenadas foram lidas com sucesso
                    if x_value is None or y_value is None:
                        print("Reiniciando: falha ao ler coordenadas")
                        continue

                    # Calcula as coordenadas finais
                    target_x = int(x_value / 20)
                    target_y = int(y_value / 20)

                    # Atualiza o ponteiro base para a próxima busca
                    self.base = final_pointer

                    # Retorna os valores encontrados
                    return target_x, target_y, pointer
                else:
                    print("Alvo não encontrado, reiniciando busca...")

            except Exception as e:
                print(f"Erro durante a busca: {e}. Reiniciando...")

        # Se chegou aqui, todas as tentativas falharam
        print("Falha em todas as tentativas de busca. Reiniciando o processo...")
        return None, None, None  # Retorna None para indicar falha

    def is_loot(self):
        loot = self.read_value(self.LOOT_POINTER, data_type="int")
        return loot

    def write_position(self, pointer, x, y):
        try:
            basex = pointer + 0x810
            basey = pointer + 0x814

            # print(f"Escrevendo posição - X: {x} em {hex(basex)}, Y: {y} em {hex(basey)}")

            self.pm.write_float(basex, float(x))
            self.pm.write_float(basey, float(y))
            return True

        except Exception as e:
            print(f"Erro ao definir posição: {e}")
            return False

    def write_camera(self, z, r, a):
        zoom = self.ZOOM_POINTER
        rotation = self.ROTATION_POINTER
        angle = self.ANGLE_POINTER
        self.pm.write_float(zoom, float(z))
        self.pm.write_float(rotation, float(r))
        self.pm.write_float(angle, float(a))

    def loot_window(self):
        l = self.read_value(self.LOOT_WINDOW, data_type="int")

        if l is None:
            return 0

        if l == 1:
            return True
        else:
            return False

    def get_sur_info(self):
        info = self.read_string_from_pointer(self.FIRST_LINK_SUR, offset=0x64, max_length=100)
        print(info)

        # Extrai o nome e as coordenadas usando expressões regulares
        name_match = re.search(r'text="([^"]+)\s*\[(-?\d+),(-?\d+)\]"', info)

        if name_match:
            name = name_match.group(1).strip()
            x_coord = name_match.group(2)
            y_coord = name_match.group(3)

            # Retorna um dicionário com as informações formatadas
            return {
                'name': name,
                'coords': f'{x_coord},{y_coord}'
            }

    def confirm_box(self):
        confirm = self.read_value(self.CONFIRM_BOX_POINTER, data_type="int")
        if confirm == 1:
            return True
        else:
            return False

    def get_location(self):

        location = self.read_string_from_pointer(self.LOCATION_POINTER, offset=0x44C, max_length=100)
        if location and re.match(r"^[\w ']+$", location):
            #print(f"Char location: {location}")
            return location
        else:
            pointer_address = self.pm.read_int(self.LOCATION_POINTER)
            pointer_address = pointer_address + 0x44C
            second_pointer = self.read_string_from_pointer(pointer_address, offset=0x0, max_length=100)
            if second_pointer:
                #print(f"Char location (2): {second_pointer}")
                return second_pointer

    def get_location_2(self):

        location_2 = self.read_string_from_pointer(self.LOCATION_POINTER_2, offset=0x0, max_length=100)

        return location_2


    def get_notification(self):
        pointer = self.read_value(self.NOTIFICATION_POINTER, data_type="int")
        if pointer >= 1:
            print(f"Notification: {pointer}")
            return True
        else:
            return False

    def get_dialog(self):
        dialog = self.read_value(self.DIALOG_POINTER, data_type="int")
        if dialog == 16775:
            return True
        else:
            return False

    def get_sin_combo(self):
        passive = self.read_value(self.SIN_PASSIVE, data_type="int")
        return passive

    def get_monk_combo(self):
        passive = self.read_value(self.MONK_PASSIVE, data_type="int")
        return passive

    def get_system_menu(self):
        system = self.read_value(self.SYSTEM_MENU_POINTER, data_type="int")
        if system == 1610612736:
            return True
        else:
            return False


def main():
    # Testando o código
    pid = 2356  # Substitua 972 pelo PID do processo correto
    p = Pointers(pid)

    if p.is_target_selected():
        print("Target selected")
    else:
        print("No target selected")

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
    print(f"GET_LOCATION : {p.get_location()}")
    print(f"CHAR_LOCATION_2 : {p.get_location_2()}")
    print(f"GET_SURR_INFO : {p.get_sur_info()}")
    print(f"SYSTEM_MENU : {p.get_system_menu()}")
    print(f"DIALOG : {p.get_dialog()}")
    print(f"SIN_COMBO : {p.get_sin_combo()}")
    print(f"MONK_COMBO : {p.get_monk_combo()}")
    print(f"NOTIFICATION : {p.get_notification()}")
    print(f"GOLD : {p.get_gold()}")
    print(f"TARGET_ID : {p.get_target_id()}")
    print(f"BAG1 : {p.bag_1_quantity()}")
    print(f"BAG2 : {p.bag_2_quantity()}")
    print(f"mounted : {p.mount()}")
    t_ptr = p.search_id()
    print(f"search_id : {t_ptr}")
    #p.write_camera(10000, 0, 50)
    print(f"is_loot : {p.is_loot()}")

if __name__ == "__main__":
    main()
