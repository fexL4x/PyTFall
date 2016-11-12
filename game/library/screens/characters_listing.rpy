init:
    default status_filters = list()
    default location_filters = list()
    default action_filters = list()
    default occ_filters = list()
    python:
        def sorting_for_chars_list():
            return hero.chars

        def setSelection_for_chars_list(sel, lst, value="from_lst"):
            for l in lst:
                sel[l.name] = l if value == "from_lst" else None

        def charlist_or_char(as_list=False):
            if char_list_selection:
                l = [x for x in char_list_selection.values() if x is not None]
                if any(l):
                    return l;
            return [char] if as_list else char
        
label chars_list:
    scene bg gallery
    # Check if we're the screen was loaded or not:
    if not renpy.get_screen("chars_list"):
        python:
            char_lists_filters = CharsSortingForGui(sorting_for_chars_list)
            char_lists_filters.filter()
            # We create the filters only from those that our chars actually have... not need for gibberish:
            status_filters = list(set([c.status for c in hero.chars]))
            location_filters = list(set([c.location for c in hero.chars]))
            action_filters = list(set([c.action for c in hero.chars]))
            selected_filters = set(['Status', 'Site', 'Action']) #, 'Class'
            char_list_selection = { c.name: None for c in char_lists_filters.sorted }
        
        show screen chars_list(source=char_lists_filters, page=chars_list_last_page_viewed, total_pages=1)
    with dissolve
    
    python:
        while 1:

            result = ui.interact()

            if result[0] == 'control':
                if result[1] == 'return':
                    break    
            elif result[0] == "dropdown":
                if result[1] == "loc":
                    renpy.show_screen("set_location_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[1] == "home":
                    renpy.show_screen("set_home_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[1] == "action":
                    renpy.show_screen("set_action_dropdown", result[2], pos=renpy.get_mouse_pos())
            elif result[0] == 'choice':
                renpy.hide_screen("chars_list")
                char = result[1]
                jump('char_profile')
            elif result[0] == "paging":
                gs = renpy.get_screen("chars_list").scope["_kwargs"]["source"]
                if result[1] == "next":
                    gs.page += 1
                elif result[1] == "previous":
                    gs.page -= 1
                gs.page %= gs.total_pages

    hide screen chars_list
    jump mainscreen

screen chars_list(source=None, page=0, total_pages=1):
    frame:
        background Frame("content/gfx/frame/framegp2.png", 10, 10)
        pos (5, 46)
        xysize (1010, 670)
        if source.sorted:
            python:
                chars_list = list()
                chars_list.append([c for ind, c in enumerate(source.sorted) if ind % 2 == 0])
                chars_list.append([c for ind, c in enumerate(source.sorted) if ind % 2 == 1])
                page_lenght = 5
                total_pages = max(int(math.ceil(len(chars_list[0]) / float(page_lenght))), int(math.ceil(len(chars_list[1]) / float(page_lenght))))
                gs = renpy.get_screen("chars_list").scope["_kwargs"]
                gs["total_pages"] = total_pages
                
                # Per Dark's request, we remember the page:

                page = max(0, min(gs["page"], total_pages - 1))
                store.chars_list_last_page_viewed = gs["page"] = page

                chars_list[0] = chars_list[0][page*page_lenght:page*page_lenght+page_lenght]
                chars_list[1] = chars_list[1][page*page_lenght:page*page_lenght+page_lenght]
                
            # Keybinds:
            key "mousedown_4" action If(gs["page"] + 1 < gs["total_pages"], true=Show("chars_list", source=gs["source"], page=gs["page"] + 1, total_pages=gs["total_pages"]), false=NullAction())
            key "mousedown_5" action If(gs["page"] > 0, true=Show("chars_list", source=gs["source"], page=gs["page"] - 1, total_pages=gs["total_pages"]), false=NullAction())
                
            hbox:
                style_group "content"
                spacing 14
                pos (17, 15)
                for l in chars_list:
                    vbox:
                        spacing 14
                        for c in l:
                            $ char_profile_img = c.show('portrait', resize=(98, 98), cache=True)
                            $ img = "content/gfx/frame/ink_box.png"
                            button:
                                idle_background Frame(Transform(img, alpha=0.4), 10 ,10)
                                hover_background Frame(Transform(img, alpha=0.9), 10 ,10)
                                xysize (470, 115)
                                action Return(['choice', c])
                                
                                # Girl Image:
                                frame:
                                    background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                                    padding 0, 0
                                    align 0, .5
                                    xysize(100, 100)
                                    add char_profile_img align .5, .5 alpha 0.96
                                   
                                # Texts/Status:
                                frame:
                                    xpos 120
                                    xysize (335, 110)
                                    background Frame (Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10 ,10)
                                    label "[c.name]":
                                        text_size 18
                                        xpos 10
                                        yalign 0.06
                                        if c.__class__ == Char:
                                            text_color pink
                                        else:
                                            text_color ivory
                                        
                                    vbox:
                                        align (0.96, 0.035)
                                        spacing 5
                                        if c.status == "slave":
                                            add ProportionalScale("content/gfx/interface/icons/slave.png", 50, 50)
                                        else:
                                            add ProportionalScale("content/gfx/interface/icons/free.png", 50, 50)
                                        text "AP: [c.AP]" size 17 color ivory
                                        button:
                                            xysize (32, 32)
                                            action ToggleDict(char_list_selection, c.name, true_value=c, false_value=None)
                                            if char_list_selection[c.name] is None:
                                                add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (0.5, 0.5)
                                            else:
                                                add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (0.5, 0.5)
                                    
                                    vbox:
                                        yalign 0.98
                                        xpos 10
                                        # Prof-Classes
                                        python:
                                            if len(c.traits.basetraits) == 1:
                                                classes = list(c.traits.basetraits)[0].id
                                            elif len(c.traits.basetraits) == 2:
                                                classes = list(c.traits.basetraits)
                                                classes.sort()
                                                classes = ", ".join([str(t) for t in classes])
                                            else:
                                                raise Exception("Character without prof basetraits detected! line: 211, chars_lists screen")
                                        text "Classes: [classes]" color ivory size 18
                                        
                                        null height 2
                                        if c not in pytfall.ra:
                                            button:
                                                style_group "ddlist"
                                                action Return(["dropdown", "loc", c])
                                                if c.status == "slave":
                                                    alternate Return(["dropdown", "home", c])
                                                text "{image=content/gfx/interface/icons/move15.png}Location: [c.location]"
                                            button:
                                                style_group "ddlist"
                                                action Return(["dropdown", "action", c])
                                                text "{image=content/gfx/interface/icons/move15.png}Action: [c.action]"
                                        else:
                                            text "{size=15}Location: Unknown"
                                            text "{size=15}Action: Hiding"
                                        
    frame:
        background Frame(Transform("content/gfx/frame/p_frame2.png", alpha=0.55), 10 ,10)
        style_prefix "content"
        xmargin 0
        left_padding 10
        ypadding 10
        pos (1005, 47)
        xysize (270, 418)
        vbox:
            spacing 5
            viewport:
                draggable True
                mousewheel True
                has vbox xsize 253
                null height 5
                label "Filters:" xalign 0.5 text_size 35 text_color white
                hbox:
                    box_wrap True
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Status')
                        text "Status" hover_color red
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Site')
                        text "Site" hover_color brown
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Action')
                        text "Action" hover_color blue

                null height 20
                hbox:
                    box_wrap True
                    style_group "basic"
                    if "Status" in selected_filters:
                        for f in status_filters:
                            button:
                                action ModFilterSet(source, "status_filters", f)
                                text "[f]" hover_color red
                    if "Site" in selected_filters:
                        for f in location_filters:
                            button:
                                action ModFilterSet(source, "location_filters", f)
                                text "[f]" hover_color brown
                    if "Action" in selected_filters:
                        for f in action_filters:
                            button:
                                action ModFilterSet(source, "action_filters", f)
                                text "[f]" hover_color blue
                null height 50
                button:
                        xalign 0.5
                        yalign 1.0
                        style_group "basic"
                        action source.clear
                        text "Reset"
                # for block_name, filters in source.display_filters:
                    # label ("{=della_respira}{b}[block_name]:") xalign 0
                    # for item_1, item_2 in izip_longest(fillvalue=None, *[iter(filters)]*2):
                        # hbox:
                            # style_group "basic"
                            # for filter_item in [item_1, item_2]:
                                # if filter_item:
                                    # $ filter_name, filter_group, filter_key = filter_item
                                    # $ focus = source.get_focus(filter_group, filter_key)
                                    # button:
                                        # action [SelectedIf(focus), Function(source.add_filter, filter_group, filter_key)]
                                        # text "[filter_name]" size 16
            # Mass (de)selection Buttons ====================================>
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                xalign 0.5
                yalign 0.5
                # ypos 5
                xysize (250, 50)
                has hbox style_group "basic" align .5, .5 spacing 5
                hbox:
                    spacing 5
                    button: # select all on current listing, deselects them if all are selected
                        xysize (66, 40)
                        action Function(setSelection_for_chars_list, char_list_selection, chars_list[0] + chars_list[1], value=None if all(char_list_selection[x.name] for x in chars_list[0] + chars_list[1]) else "from_lst")
                        text "These"
                    button: # every of currently filtered, also in next tabs
                        xysize (66, 40)
                        action If(not all(char_list_selection.values()), [Function(setSelection_for_chars_list, char_list_selection, source.sorted)])
                        text "All"
                    button: # deselect all
                        xysize (66, 40)
                        action If(any(char_list_selection.values()), [Function(setSelection_for_chars_list, char_list_selection, source.sorted, None)])
                        text "None"
            # Mass action Buttons ====================================>
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                xalign 0.5
                yalign 0.5
                xysize (250, 200)
                has vbox style_group "basic" align .5, .5 spacing 5
                vbox:
                    button:
                        xysize (150, 40)
                        action If(any(char_list_selection.values()), [Hide("chars_list"), With(dissolve), Jump('girl_training')])
                        text "Training"
            
    use top_stripe(True)
    
