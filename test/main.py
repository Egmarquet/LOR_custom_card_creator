if __name__ == '__main__':
    name = "Maximum Cow"
    hp = "4"
    pwr = "3"
    mp = "3"
    text = "<Quick Attack>: I attack the enemy nexus and summmon 3 [Small Cows] with <fearsome>"
    frame_path = frames.UNIT_COMMON
    img_path = "..\\test\\test_images\\test_dab.png"
    kws = ['barrier']
    tribe = "Elite"
    region = "noxus"
    uc = UnitCard(frame_path)
    uc.name = name
    uc.img_path = img_path
    uc.tribe = tribe
    uc.mana = "1"
    uc.hp = "10"
    uc.text = text
    uc.img_path = img_path
    # adds .15 seconds to execution
    start = time.time()
    uc.render()
    end = time.time()
    print(end - start)
    display(uc.out)
