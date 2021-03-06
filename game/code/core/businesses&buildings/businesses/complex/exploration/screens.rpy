screen building_management_leftframe_exploration_guild_mode:
    if bm_exploration_view_mode == "log":

        default focused_area_index = 0

        $ temp = sorted([a for a in fg_areas.values() if a.main and a.unlocked])
        vbox:
            xsize 320 spacing 1
            # Maps sign:
            frame:
                style_group "content"
                xalign .5 ypos 3
                xysize 200, 50
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"Maps") text_size 23 text_color ivory align .5, .8

            null height 5

            # Main Area:
            # We assume that there is always at least one area!
            $ main_area = temp[focused_area_index]
            $ img = main_area.img
            frame:
                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.9), 10, 10)
                padding 2, 2
                margin 0, 0
                xalign .5
                button:
                    align .5, .5
                    xysize 220, 130
                    background Frame(img)
                    hover_background Frame(im.MatrixColor(img, im.matrix.brightness(.05)))
                    action NullAction()
                    frame:
                        align .5, .0
                        padding 20, 2
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=.5), 5, 5)
                        text main_area.name:
                            color gold
                            hover_color red
                            style "interactions_text"
                            size 18 outlines [(1, "#3a3a3a", 0, 0)]
                            align .5, .5

            # Paging for Main Area:
            hbox:
                style_prefix "basic"
                xalign .5
                textbutton "<==":
                    action SetScreenVariable("focused_area_index", (focused_area_index - 1) % len(temp))
                textbutton "==>":
                    action SetScreenVariable("focused_area_index", (focused_area_index + 1) % len(temp))

            # Sub Areas:
            null height 5
            $ areas = sorted([a for a in fg_areas.values() if a.area == main_area.name], key=attrgetter("stage"))
            fixed:
                xalign .5
                xysize 310, 190
                vbox:
                    xalign .5
                    style_prefix "dropdown_gm2"
                    for area in areas:
                        button:
                            xysize 220, 18
                            action SetVariable("selected_log_area", area), Show("fg_log", None, area)
                            selected selected_log_area == area
                            text str(area.stage):
                                hover_color green
                                selected_color gold
                                size 12
                                xalign .02
                                yoffset 1
                            label "[area.name]":
                                text_color "#66CD00"
                                text_hover_color green
                                text_selected_color gold
                                text_size 12
                                align 1.0, .5

            # Total Main Area Stats (Data Does Not Exist Yet):
            frame:
                style_group "content"
                xalign .5
                xysize 200, 50
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"Total") text_size 23 text_color ivory align .5, .8

            vbox:
                xalign .5
                style_prefix "proper_stats"
                $ total = sum(main_area.found_items.values())
                frame:
                    xoffset 4
                    xysize 270, 27
                    xpadding 7
                    text "Items Found:":
                        color ivory
                    text "[total]":
                        style_suffix "value_text"
                        color ivory
                $ total = sum(main_area.mobs_defeated.values())
                frame:
                    xoffset 4
                    xysize 270, 27
                    xpadding 7
                    text "Mobs Crushed:":
                        color ivory
                    text "[total]":
                        style_suffix "value_text"
                        color ivory
                $ total = sum(main_area.mobs_defeated.values())
                frame:
                    xoffset 4
                    xysize 270, 27
                    xpadding 7
                    text "Chars Captured:":
                        color ivory
                    text "[main_area.chars_captured]":
                        style_suffix "value_text"
                        color ivory
    elif bm_exploration_view_mode == "team":
        # Filters:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
            style_group "proper_stats"
            xalign .5
            padding 12, 12
            margin 0, 0
            has vbox spacing 1
            label "Filters:" xalign .5
            vbox:
                style_prefix "basic"
                xalign .5
                textbutton "Reset":
                    xsize 200
                    action Function(fg_filters.clear)
                textbutton "Warriors":
                    xsize 200
                    action ModFilterSet(fg_filters, "occ_filters", "Combatant")
                textbutton "Free":
                    xsize 200
                    action ModFilterSet(fg_filters, "status_filters", "free")
                textbutton "Slaves":
                    xsize 200
                    action ModFilterSet(fg_filters, "status_filters", "slave")

        # Sorting:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
            style_group "proper_stats"
            xalign .5
            padding 12, 12
            margin 0, 0
            has vbox spacing 1
            label "Sort:" xalign .5
            vbox:
                style_prefix "basic"
                xalign .5
                textbutton "Name":
                    xsize 200
                    action SetFilter(fg_filters, "alphabetical")
                textbutton "Level":
                    xsize 200
                    action SetFilter(fg_filters, "level")
    elif bm_exploration_view_mode == "explore":
        fixed: # making sure we can align stuff...
            xysize 320, 665
            frame:
                style_group "content"
                xalign .5 ypos 3
                xysize (200, 50)
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"Maps") text_size 23 text_color ivory align (.5, .8)

            viewport:
                xysize 224, 500
                xalign .5 ypos 57
                has vbox spacing 4
                $ temp = sorted([a for a in fg_areas.values() if a.main and a.unlocked])
                if temp and not bm_mid_frame_focus:
                    $ mid_frame_focus = temp[0]

                for area in temp:
                    $ img = area.img
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.9), 10, 10)
                        padding 2, 2
                        margin 0, 0
                        button:
                            align .5, .5
                            xysize 220, 130
                            background Frame(img)
                            hover_background Frame(im.MatrixColor(img, im.matrix.brightness(.05)))
                            action SetVariable("bm_mid_frame_focus", area)
                            frame:
                                align .5, .0
                                padding 20, 2
                                background Frame(Transform("content/gfx/frame/ink_box.png", alpha=.5), 5, 5)
                                text area.name:
                                    color gold
                                    hover_color red
                                    style "interactions_text"
                                    size 18 outlines [(1, "#3a3a3a", 0, 0)]
                                    align .5, .5

screen building_management_midframe_exploration_guild_mode:
    if bm_exploration_view_mode == "log":
        vbox:
            xsize 630
            frame: # Image
                xalign .5
                padding 5, 5
                background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                add im.Scale("content/gfx/bg/buildings/log.webp", 600, 390)
    elif bm_exploration_view_mode == "explore":
        vbox:
            xsize 630
            frame: # Image
                xalign .5
                padding 5, 5
                background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                add im.Scale("content/gfx/bg/buildings/Exploration.webp", 600, 390)

            hbox:
                box_wrap 1
                spacing 2
                xalign .5
                if isinstance(bm_mid_frame_focus, FG_Area):
                    $ temp = sorted([a for a in fg_areas.values() if a.area == bm_mid_frame_focus.name], key=attrgetter("stage"))
                    for area in temp:
                        $ fbg = "content/gfx/frame/mes12.jpg"
                        $ hfbg = im.MatrixColor("content/gfx/frame/mes11.webp", im.matrix.brightness(.10))
                        button:
                            background Transform(Frame(fbg, 10, 10), alpha=.9)
                            hover_background Transform(Frame(hfbg, 10, 10), alpha=.9)
                            xysize (150, 90)
                            ymargin 1
                            ypadding 1
                            if area.unlocked:
                                $ temp = area.name
                                action Show("fg_area", dissolve, area)
                            else:
                                $ temp = "?????????"
                                action NullAction()
                            text temp color gold style "interactions_text" size 14 outlines [(1, "#3a3a3a", 0, 0)] align (.5, .01)
                            hbox:
                                align (.5, .9)
                                # Get the correct stars:
                                # python:
                                    # temp = []
                                    # for i in range(area.explored//20):
                                        # temp.append(ProportionalScale("content/gfx/bg/example/star2.png", 18, 18))
                                    # if len(temp) != 5:
                                        # if area.explored%20 >= 10:
                                            # temp.append(ProportionalScale("content/gfx/bg/example/star3.png", 18, 18))
                                    # while len(temp) != 5:
                                        # temp.append(ProportionalScale("content/gfx/bg/example/star1.png", 18, 18))
                                # for i in temp:
                                    # add i
    elif bm_exploration_view_mode == "team":
        # Backgrounds:
        frame:
            background Frame(gfxframes + "p_frame52.webp", 10, 10)
            xysize 622, 330
            yoffset -1
            xalign .5
            hbox:
                xalign .5
                box_wrap 1
                for i in xrange(18):
                    frame:
                        xysize 90, 90
                        xmargin 2
                        ymargin 2
                        background Frame(gfxframes + "p_frame53.png", 5, 5)
            # Page control buttons:
            hbox:
                style_prefix "paging_green"
                align .5, .99
                hbox:
                    spacing 1
                    $ temp = workers.page - 1 >= 0
                    button:
                        style_suffix "button_left2x"
                        tooltip "<== First Page"
                        action Function(workers.first_page)
                        sensitive temp
                    button:
                        style_suffix "button_left"
                        tooltip "<== Previous Page"
                        action Function(workers.prev_page)
                        sensitive temp
                null width 60
                hbox:
                    spacing 1
                    $ temp = workers.page + 1 < workers.max_page
                    button:
                        style_suffix "button_right"
                        tooltip "Next Page ==>"
                        action Function(workers.next_page)
                        sensitive temp
                    button:
                        style_suffix "button_right2x"
                        tooltip "Last Page ==>"
                        action Function(workers.last_page)
                        sensitive temp

        # Downframe (for the teams and team paging)
        frame:
            background Frame(gfxframes + "p_frame52.webp", 10, 10)
            xysize 700, 349
            ypos 321 xalign .5

        # Paging guild teams!
        hbox:
            style_prefix "paging_green"
            xalign .5 ypos 328
            hbox:
                spacing 1
                $ temp = guild_teams.page - 1 >= 0
                button:
                    style_suffix "button_left2x"
                    tooltip "<== First Page"
                    action guild_teams.first_page
                    sensitive temp
                button:
                    style_suffix "button_left"
                    tooltip "<== Previous Page"
                    action guild_teams.prev_page
                    sensitive temp
            null width 60
            hbox:
                spacing 1
                $ temp = guild_teams.page + 1 < guild_teams.max_page
                button:
                    style_suffix "button_right"
                    tooltip "Next Page ==>"
                    action guild_teams.next_page
                    sensitive temp
                button:
                    style_suffix "button_right2x"
                    tooltip "Last Page ==>"
                    action guild_teams.last_page
                    sensitive temp

        # We'll prolly have to do two layers, one for backgrounds and other for drags...
        draggroup:
            id "team_builder"
            for t, pos in guild_teams:
                drag:
                    drag_name t
                    xysize (310, 83)
                    draggable 0
                    droppable 1
                    pos pos
                    add gfxframes + "team_frame_1.png"
                    hbox:
                        yalign .5
                        xpos 117
                        spacing 15
                        for i in t:
                            $ img = i.show("portrait", resize=(46, 46), cache=1)
                            button:
                                xysize (46, 46)
                                background img
                                hover_background im.MatrixColor(img, im.matrix.brightness(.10))
                                action Show("fg_char_dropdown", dissolve, i, team=t, remove=True)
                                tooltip i.fullname
                    frame:
                        xysize (310, 83)
                        background gfxframes + "team_frame_2.png"
                        button:
                            background Null()
                            padding 0, 0
                            margin 0, 0
                            xpos 49 xanchor .5 yalign .5
                            xysize 78, 61
                            action Return(["fg_team", "rename", t])
                            tooltip "Rename %s Team!" % t.name
                            text t.name align .5, .5 hover_color red text_align .5
                        # Remove all teammembers:
                        $ img = im.Scale("content/gfx/interface/buttons/shape69.png", 20, 20)
                        button:
                            background img
                            hover_background im.MatrixColor(img, im.matrix.brightness(.15))
                            insensitive_background  im.Sepia(img)
                            padding 0, 0
                            margin 0, 0
                            align 1.0, 1.0
                            xysize 20, 20
                            sensitive t
                            action Return(["fg_team", "clear", t])
                            tooltip "Remove all explorers from Team %s!" % t.name

            for w, pos in workers:
                drag:
                    dragged dragged
                    droppable 0
                    tooltip w.fullname
                    drag_name w
                    pos pos
                    clicked Show("fg_char_dropdown", dissolve, w, team=None, remove=False)
                    add w.show("portrait", resize=(70, 70), cache=1)

screen building_management_rightframe_exploration_guild_mode:
    if False:
        button:
            xysize (150, 40)
            yalign .5
            action NullAction()
            tooltip "All the meetings and conversations are held in this Hall. On the noticeboard, you can take job that available for your rank. Sometimes guild members or the master himself and his Council, can offer you a rare job."
            text "Main Hall" size 15
    button:
        xysize (150, 40)
        yalign .5
        action SetVariable("bm_exploration_view_mode", "team"), Hide("fg_log")
        tooltip "You can customize your team here or hire Guild members."
        text "Team" size 15
    button:
        xysize (150, 40)
        yalign .5
        action SetVariable("bm_exploration_view_mode", "explore"), Hide("fg_log")
        tooltip ("On this screen you can organize the expedition. Also, there is a "+
                 "possibility to see all available information on the various places, enemies and items drop.")
        text "Exploration" size 15
    button:
        xysize (150, 40)
        yalign .5
        action SetVariable("bm_exploration_view_mode", "log"), Hide("fg_log")
        tooltip "For each of your teams, recorded one last adventure, which you can see here in detail."
        text "Log" size 15

# Customized screens for specific businesses:
screen fg_log(area):
    on "hide":
        action SetVariable("selected_log_area", None)

    # modal True
    zorder 10

    key "mousedown_3" action Hide("fg_log")

    default focused_log = None

    frame:
        ypos 40
        xalign .5
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        style_prefix "content"
        xysize (630, 680)

        $ fbg = "content/gfx/frame/mes11.webp"
        frame:
            background Transform(Frame(fbg, 10, 10), alpha=.9)
            xysize (620, 90)
            ymargin 1
            ypadding 1
            $ temp = area.name
            text temp color gold style "interactions_text" size 35 outlines [(1, "#3a3a3a", 0, 0)] align (.5, .3)
            hbox:
                align (.5, .9)
                # Get the correct stars:
                python:
                    temp = []
                    for i in range(area.explored//20):
                        temp.append(ProportionalScale("content/gfx/interface/icons/stars/star2.png", 18, 18))
                    if len(temp) != 5:
                        if area.explored%20 >= 10:
                            temp.append(ProportionalScale("content/gfx/interface/icons/stars/star3.png", 18, 18))
                    while len(temp) != 5:
                        temp.append(ProportionalScale("content/gfx/interface/icons/stars/star1.png", 18, 18))
                for i in temp:
                    add i

        # Buttons with logs (Events):
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
            style_prefix "dropdown_gm2"
            ypos 100 xalign .0
            ysize 346
            padding 10, 10
            has vbox xsize 220 spacing 1
            frame:
                style_group "content"
                xalign .5
                padding 15, 5
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.6), 10, 10)
                label "Events" text_size 20 text_color ivory align .5, .5

            for l in area.logs:
                button:
                    xalign .5
                    ysize 18
                    action SetScreenVariable("focused_log", l)
                    text str(l.name) size 12 xalign .02 yoffset 1
                    # Resolve the suffix:
                    if l.item:
                        text "[l.item.type]" size 12 align (1.0, .5)
                    else: # Suffix:
                        text str(l.suffix) size 12 align (1.0, .5)

        # Information (Story)
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6, yzoom=-1), 10, 10)
            ysize 346
            padding 10, 10
            ypos 100 xalign 1.0
            has vbox xsize 350 spacing 1
            frame:
                style_group "content"
                xalign .5
                padding 15, 5
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.6), 10, 10)
                label "Story" text_size 20 text_color ivory align .5, .5

            frame:
                background Frame("content/gfx/frame/ink_box.png", 10, 10)
                has viewport draggable 1 mousewheel 1
                if focused_log:
                    if focused_log.battle_log:
                        text "\n".join(focused_log.battle_log) color white
                    elif focused_log.item:
                        $ item = focused_log.item
                        vbox:
                            spacing 10 xfill 1
                            add ProportionalScale(item.icon, 100, 100) xalign .5
                            text item.desc xalign .5 color white

screen fg_area(area):
    modal True
    zorder 1

    key "mousedown_3" action Hide("fg_area")

    style_prefix "basic"

    # Left frame with Area controls
    frame:
        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
        xysize 330, 680
        ypos 40
        has vbox xsize 326 spacing 2 xalign .5
        # The idea is to add special icons for as many features as possible in the future to make Areas cool:
        # Simple buttons are temp for dev versions/beta.
        button:
            xalign .5
            xysize 300, 30
            if not area.camp:
                action ToggleField(area, "building_camp")
            else:
                action NullAction()
            python:
                if area.camp:
                    status = "Complete"
                elif area.building_camp:
                    status = area.camp_build_status + " Complete"
                else:
                    status = "Unknown"
            text "Camp status:" xalign .0
            text "[status]" xalign 1.0
        button:
            xalign .5
            xysize 300, 30
            action ToggleField(area, "capture_chars")
            text "Capture Chars:" xalign .0
            text "[area.capture_chars]" xalign 1.0

        null height 5
        button:
            xalign .5
            xysize 300, 30
            text "Days Exploring:" xalign .0
            text "[area.days]" xalign 1.0
            action NullAction()
        hbox:
            xalign .5
            imagebutton:
                yalign .5
                idle 'content/gfx/interface/buttons/prev.png'
                hover im.MatrixColor('content/gfx/interface/buttons/prev.png', im.matrix.brightness(.15))
                action SetField(area, "days", max(3, area.days-1))
            null width 5
            bar:
                align .5, 1.0
                value FieldValue(area, 'days', area.max_days-3, max_is_zero=False, style='scrollbar', offset=3, step=1)
                xmaximum 150
                thumb 'content/gfx/interface/icons/move15.png'
                tooltip "How many days do you wish for the team to spend questing?"
            null width 5
            imagebutton:
                yalign .5
                idle 'content/gfx/interface/buttons/next.png'
                hover im.MatrixColor('content/gfx/interface/buttons/next.png', im.matrix.brightness(.15))
                action SetField(area, "days", min(15, area.days+1))

        null height 5
        button:
            xalign .5
            xysize 300, 30
            text "Risk:" xalign .0
            text "[area.risk]" xalign 1.0
            action NullAction()
        hbox:
            xalign .5
            imagebutton:
                yalign .5
                idle 'content/gfx/interface/buttons/prev.png'
                hover im.MatrixColor('content/gfx/interface/buttons/prev.png', im.matrix.brightness(.15))
                action SetField(area, "risk", max(0, area.risk-1))
            null width 5
            bar:
                align .5, 1.0
                value FieldValue(area, 'risk', 100, max_is_zero=False, style='scrollbar', offset=0, step=1)
                xmaximum 150
                thumb 'content/gfx/interface/icons/move15.png'
                tooltip ("How much risk does the team take when exploring? The more significant the risk,"+
                         "the higher the reward but your team may not even return of you push this too far!")
            null width 5
            imagebutton:
                yalign .5
                idle 'content/gfx/interface/buttons/next.png'
                hover (im.MatrixColor('content/gfx/interface/buttons/next.png', im.matrix.brightness(.15)))
                action SetField(area, "risk", min(100, area.risk+1))

    # Mid-Frame:
    frame:
        ypos 40
        xalign .5
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        style_prefix "content"
        xysize (630, 680)

        $ fbg = "content/gfx/frame/mes11.webp"
        frame:
            background Transform(Frame(fbg, 10, 10), alpha=.9)
            xysize (620, 90)
            ymargin 1
            ypadding 1
            $ temp = area.name
            text temp color gold style "interactions_text" size 35 outlines [(1, "#3a3a3a", 0, 0)] align (.5, .3)

        hbox:
            align .5, .5
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                xysize (310, 410)
                xpadding 5
                frame:
                    style_group "content"
                    align (.5, .015)
                    xysize (210, 40)
                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.6), 10, 10)
                    label (u"Enemies") text_size 23 text_color ivory align .5, .5
                viewport:
                    style_prefix "proper_stats"
                    xysize (300, 340)
                    ypos 50
                    xalign .5
                    has vbox spacing 3
                    for m in area.mobs_defeated:
                        $ m = mobs[m]
                        fixed:
                            xysize 300, 65
                            frame:
                                xpos 6
                                left_padding 2
                                align .01, .5
                                xsize 197
                                text m["name"]
                            frame:
                                yalign .5
                                xanchor 1.0
                                ysize 44
                                xpadding 4
                                xminimum 28
                                xpos 233
                                $ temp = m["min_lvl"]
                                text ("Lvl\n[temp]+") style "TisaOTM" size 17 text_align .5 line_spacing -6
                            frame:
                                background Frame(Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=.75), 10, 10)
                                padding 3, 3
                                margin 0, 0
                                xysize 60, 60
                                align .99, .5
                                add ProportionalScale(m["portrait"], 57, 57) align .5, .5

            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                xysize (310, 410)
                xpadding 5
                frame:
                    style_group "content"
                    align (.5, .015)
                    xysize (210, 40)
                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.6), 10, 10)
                    label (u"Items") text_size 23 text_color ivory align .5, .5
                viewport:
                    style_prefix "proper_stats"
                    mousewheel 1
                    xysize (300, 340)
                    ypos 50
                    xalign .5
                    has vbox spacing 3
                    for i in area.found_items:
                        $ i = items[i]
                        fixed:
                            xysize 300, 65
                            frame:
                                xpos 6
                                left_padding 2
                                align .01, .5
                                xsize 197
                                text i.id
                            frame:
                                yalign .5
                                xanchor 1.0
                                ysize 40
                                xsize 35
                                xpadding 4
                                xpos 233
                                #$ temp = m["min_lvl"]
                                #text ("Lvl\n[temp]+") align (.5, .5) style "TisaOTM" size 18
                            frame:
                                background Frame(Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=.75), 10, 10)
                                padding 3, 3
                                xysize 60, 60
                                align .99, .5
                                add ProportionalScale(i.icon, 57, 57) align .5, .5

        hbox:
            spacing 20
            xalign .5 ypos 550
            python:
                temp = building.get_business("fg")
                teams = temp.teams_to_launch() if temp else []
                if teams:
                    if not temp.focus_team:
                        try:
                            temp.focus_team = teams[temp.team_to_launch_index]
                        except:
                            temp.focus_team = teams[0]

            button:
                style "paging_green_button_left2x"
                yalign .5
                action temp.prev_team_to_launch, renpy.restart_interaction
                tooltip "Previous Team"
                sensitive len(teams) > 1
            button:
                style "marble_button"
                padding 10, 10
                if teams:
                    action Function(temp.launch_team, area), Jump("building_management")
                    tooltip "Send {} on {} days long exploration run!".format(temp.focus_team.name, area.days)
                    vbox:
                        xminimum 150
                        spacing -30
                        text "Launch" style "basic_button_text" xalign .5
                        text "\n[temp.focus_team.name]" style "basic_button_text" xalign .5
                else:
                    action NullAction()
                    text "No Teams Available!" style "basic_button_text" align .5, .5

            button:
                style "paging_green_button_right2x"
                yalign .5
                action temp.next_team_to_launch, renpy.restart_interaction
                tooltip "Next Team"
                sensitive len(teams) > 1

        hbox:
            align .5, .98
            button:
                style_group "basic"
                action Hide("fg_area")
                minimum (50, 30)
                text "Back"

screen fg_char_dropdown(char, team=None, remove=False):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    default pos = renpy.get_mouse_pos()

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox

        textbutton "Profile":
            action [SetVariable("char_profile_entry", last_label),
                    SetVariable("char", char),
                    SetVariable("girls", [char]),
                    Hide("fg_char_dropdown"),
                    Hide("pyt_fg_management"),
                    Jump("char_profile")]
        textbutton "Equipment":
            action [SetVariable("came_to_equip_from", "building_management"), SetVariable("eqtarget", char), SetVariable("char", char), Hide("fg_char_dropdown"), Hide("pyt_fg_management"), Jump("char_equip")]
        if remove: # and team[0] != girl:
            textbutton "Remove from the Team":
                action [Function(team.remove, char), Function(workers.add, char), Hide("fg_char_dropdown")]

        null height 10

        textbutton "Close":
            action Hide("fg_char_dropdown")
            keysym "mouseup_3"

screen se_debugger():
    zorder 200
    # Useful SE info cause we're not getting anywhere otherwise :(
    viewport:
        xysize (1280, 720)
        scrollbars "vertical"
        mousewheel True
        has vbox

        for area in fg_areas.values():
            if area.trackers:
                text area.name
                for t in area.trackers:
                    hbox:
                        xsize 500
                        spacing 5
                        text t.team.name xalign .0
                        text t.state xalign 1.0
                    hbox:
                        xsize 500
                        spacing 5
                        text str(t.day) xalign .0
                        text str(t.days) xalign 1.0
                    null height 3
                add Solid("F00", xysize=(1280, 5))

    textbutton "Exit":
        align .5, .1
        action Hide("se_debugger")
