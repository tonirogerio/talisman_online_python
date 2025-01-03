def deleter(config):
    def inner():
        if config.minimized_mode == "ON":
            hwnd = win32gui.FindWindow(None, config.char_name)
            if hwnd:
                placement = win32gui.GetWindowPlacement(hwnd)
                if placement[1] == win32con.SW_SHOWMINIMIZED:  # SW_SHOWMINIMIZED é 2
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restaura a janela se estiver minimizada
                    time.sleep(1)

        # Verifica se a mochila está aberta
        if not Pointers(config.pid).is_bag_open():
            print("Open bag")
            send(config.hwnd, config.inventory)
            time.sleep(0.5)
        else:
            print("Bag is open")
            time.sleep(0.5)

        def load_images(folder):
            """
            Carrega todas as imagens da pasta sem cache.
            """
            images = {}
            for filename in os.listdir(folder):
                full_path = os.path.join(folder, filename)
                image = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    images[filename] = image
            return images

        def capture_window(hwnd):
            """
            Captura o conteúdo da janela especificada por hwnd, independentemente de sobreposições.
            """
            try:
                rect = win32gui.GetWindowRect(hwnd)
                width, height = rect[2] - rect[0], rect[3] - rect[1]

                hwnd_dc = win32gui.GetWindowDC(hwnd)
                mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
                save_dc = mfc_dc.CreateCompatibleDC()
                save_bitmap = win32ui.CreateBitmap()
                save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
                save_dc.SelectObject(save_bitmap)

                save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

                bmp_info = save_bitmap.GetInfo()
                bmp_str = save_bitmap.GetBitmapBits(True)
                img = np.frombuffer(bmp_str, dtype=np.uint8)
                img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

                save_dc.DeleteDC()
                mfc_dc.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwnd_dc)
                win32gui.DeleteObject(save_bitmap.GetHandle())

                return img[..., :3]

            except Exception as e:
                print(f"Erro ao capturar a janela: {e}")
                raise

        def get_title_bar_height():
            """
            Obtém a altura da barra de título da janela usando a API do Windows.
            """
            SM_CYCAPTION = 4  # Constante para altura da barra de título
            return ctypes.windll.user32.GetSystemMetrics(SM_CYCAPTION)

        def find_image_in_window(target_image, hwnd):
            """
            Encontra uma imagem dentro da janela especificada pelo HWND,
            descontando a barra de título da janela.
            """
            title_bar_height = get_title_bar_height()

            # Capturar a imagem da janela
            window_img = capture_window(hwnd)
            window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)

            # Localizar a imagem na janela
            result = cv2.matchTemplate(window_gray, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.9:  # Ajuste o limiar conforme necessário
                adjusted_loc = (max_loc[0], max_loc[1] - title_bar_height)
                return adjusted_loc

            return None

        def find_items_in_window(item_images, hwnd):
            """
            Localiza itens em uma janela específica.
            """
            to_delete = []
            tolerance = 3  # Tolerância em pixels para coordenadas duplicadas

            window_img = capture_window(hwnd)
            window_gray = cv2.cvtColor(window_img, cv2.COLOR_BGR2GRAY)

            for offset in bag_offsets:
                x1, y1, width, height = offset

                bag_area = window_gray[y1:y1 + height, x1:x1 + width]

                for item_name, item_image in item_images.items():
                    result = cv2.matchTemplate(bag_area, item_image, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.9
                    loc = np.where(result >= threshold)

                    for pt in zip(*loc[::-1]):
                        title_bar_height = get_title_bar_height()
                        global_x = x1 + pt[0]
                        global_y = y1 + pt[1] - title_bar_height

                        if not any(
                                abs(existing_x - global_x) <= tolerance and abs(existing_y - global_y) <= tolerance for
                                existing_x, existing_y in to_delete):
                            to_delete.append((global_x, global_y))

            return to_delete

        item_path = "Images/items"
        item_images = load_images(item_path)

        destroy_path = "Images/misc/destroy-item.bmp"
        destroy_image = cv2.imread(destroy_path, cv2.IMREAD_GRAYSCALE)
        coordinates = find_image_in_window(destroy_image, config.hwnd)

        if coordinates:
            destroy_x, destroy_y = coordinates

            bag_cords = [
                (destroy_x - 5, destroy_y - 200, destroy_x + 220, destroy_y - 15),
                (destroy_x + 250, destroy_y - 420, destroy_x + 490, destroy_y - 10),
            ]

            bag_offsets = [
                (destroy_x - 5, destroy_y - 200, destroy_x + 220, destroy_y - 15),
                (destroy_x + 250, destroy_y - 420, destroy_x + 490, destroy_y - 10),
            ]

            bag_images = []
            for x1, y1, x2, y2 in bag_cords:
                bag_img = capture_window(config.hwnd)[y1:y2, x1:x2]
                bag_images.append(bag_img)

            to_delete = find_items_in_window(item_images, config.hwnd)

            """ok_button = config.deleter_ok.split(",")
            ok_buttonX = int(ok_button[0])
            ok_buttonY = int(ok_button[1])"""

            for item in to_delete:
                x, y = int(item[0]), int(item[1])

                left(config.hwnd, x, y)
                time.sleep(0.15)
                left(config.hwnd, destroy_x, destroy_y)
                time.sleep(0.15)
                left(config.hwnd, int(cords_game["deleter_ok"][0]), int(cords_game["deleter_ok"][1]))
                time.sleep(0.15)
        else:
            print("Destroy icon not found.")
        print("Close bag")
        send(config.hwnd, config.inventory)
        time.sleep(1)
        if config.minimized_mode == "ON":
            hwnd = win32gui.FindWindow(None, config.char_name)
            if hwnd:
                placement = win32gui.GetWindowPlacement(hwnd)
                if not placement[1] == win32con.SW_SHOWMINIMIZED:  # SW_SHOWMINIMIZED é 2
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  # Minimiza a janela

    return inner
