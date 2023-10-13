
while intro:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return None, None
        elif event.type == pg.KEYDOWN:
            if PLATFORM == "DEV":
                if event.key in (pg.K_ESCAPE, pg.K_DELETE):
                    return None, None

            if event.key in (pg.K_LEFT, pg.K_RIGHT):
                if event.key == pg.K_LEFT:
                    SELECTED_MAP_NR -= 1
                else:
                    SELECTED_MAP_NR += 1
                play_sound(sa.eat_sound)
                SELECTED_MAP_NR %= len(MAP_NAMES)
                selected_map_name = MAP_NAMES[SELECTED_MAP_NR]
                switch_map_to(selected_map_name)

            elif event.key == pg.K_1:
                play_sound(ma.click_sound)
                return selected_map_name, False
            elif event.key == pg.K_2:
                play_sound(ma.click_sound)
                return selected_map_name, True

    pg.display.update()
    CLOCK.tick(20)