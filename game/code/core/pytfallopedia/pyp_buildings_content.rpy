screen pyp_buildings_and_businesses():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/b_and_b.webp"

        vbox:
            ypos 400
            text ("You can buy buildings and expand them with workable businesses or housing capacity for the slaves that are in your ownership. "+
                  " Free characters do not require such housing and will take care of their own dwelling, as such, you cannot control where their 'home' is at (at least not in the Beta).")
            null height 10
            text ("There are also 'Apartments' for sale at the realtor, where MC can live in. "+
                  "Better apartments, just as better or upgraded housing provide greater overnight bonuses.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_buildings():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/building.webp"

        vbox:
            ypos 400
            text ("Each building allows the player to build a subset of upgrades and businesses. "+
                  "Buildings have their own stats. They are run by managers, which can be either the player (Manage class required) or by a free character hired in the city.")
            null height 10
            text ("Buildings have Tiers as well, you'd typically want characters with higher tier than "+
                  "the buildings to work there, although lack of such may be compensated by upgrades and excellent management.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_businesses():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/businesses.webp"

        vbox:
            ypos 400
            text ("Businesses are the simplest way to make money in the game if you have the investment required to get one running efficiently.")
            null height 10
            text ("Just as buildings that host them, businesses can be updated and expanded. Upgrades require resources which can be acquired in the city (through actions, events or plainly bought in the shops).")
            null height 10
            text ("Capacity enables your workers to serve more customers at any given time and usually just cost Gold.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_clients():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/clients.webp"

        vbox:
            ypos 400
            text ("Clients are the bread and butter of the businesses.")
            null height 10
            text ("Higher Fame Building stats attract a higher number, and higher Reputation attracts a better class of Customer.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_building_stats():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .01
            add "content/gfx/interface/pyp/building_stats.webp"

        vbox:
            ypos 190
            text ("Buildings have a small number of Stats. Those have maximums that depend on the quality of the building.")
            null height 10
            text ("Stats such as Dirt and Threat can ruin the reputation of a building if you let them get out of control, however, in smaller Buildings, you never have to worry about them.")

        vbox:
            spacing 8
            ypos 280
            label "Stats:" text_size 25
            hbox:
                spacing 2
                viewport:
                    draggable 1
                    mousewheel 1
                    scrollbars "vertical"
                    xysize 970, 330
                    has vbox spacing 8
                    vbox:
                        label "Dirt"
                        text ("Accumulates when a building is worked or even (in much smaller numbers) if it stands idle."+
                        "As long as the working capacity remains insignificant, Dirt will be removed automatically by the workers in the Building and will NEVER accumulate.")
                        text "In more significant buildings, it will pay off to have dedicated cleaners and maybe even upgrades to facilitate them."
                    vbox:
                        label "Character"
                        text ("Reversed Obedience. Higher Character means that greater penalties for forcing any undesirable"+
                              " action and a character will generally not accept any task they are not expected to perform. Useful for jobs like Barmaid.")
                    vbox:
                        label "Threat"
                        text ("Same as for Dirt, a threat is only essential in larger Buildings. Clients will leave the buildings"+
                              " that have a very high threat level. Very unfavorable events may happen in such cases as well (customers starting a brawl for example).")
                    vbox:
                        label "Fame"
                        text "Fame can be increased by advertising and your workers' favorable performance. Higher fame will attract more clients."
                    vbox:
                        label "Reputation"
                        text ("Reputation can be increased through some advertising (usually the expensive kind). "+
                              "Higher reputation may attract better clients (which means more tips). At the present stage of development, this building stat is less critical than fame.")
                    vbox:
                        label "Slots and Capacity"
                        text "Buildings have internal and external space which can be consumed to build businesses or upgrades. Capacity is the number of clients and slaves this building can host."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_advertising():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/advertising.webp"

        vbox:
            ypos 400
            text ("Advertising can be used to attract more and better clients through increasing Fame and Reputation of the building...")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_manager():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/manager.webp"

        vbox:
            ypos 400
            text ("Managers can provide a great many effects to workers in the building. "+
                  "You can choose what Managers should prioritize in Building Controls. "+
                  "This is the most expensive class to hire so it might not be sound "+
                  "to hire one for a low tier building, "+
                  "but higher tiered businesses will suffer without proper management.")
            null height 10
            text ("The manager may participate in building activities and"+
                  " do other jobs (especially if (s)he have more than one class) is permitted by Building Controls.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_buildings_controls():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/controls.webp"

        vbox:
            ypos 500
            text ("Building Controls allows you to customize Manager behavior and "+
                  "control some other concerns (such as auto-cleaning). These will be expanded as the development moves forward.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_workers():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/workers.webp"

        vbox:
            ypos 400
            text ("The player can hire or buy workers and set their workplace and action to take within that workplace. More businesses will allow a larger range of activities. "+
                  "Slaves can be purchased in the Slave Market or through items and events. Free workers can be hired through interaction in the City or in the Employment Agency.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_jobs():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        frame:
            align .5, .05
            add "content/gfx/interface/pyp/jobs.webp"

        vbox:
            ypos 400
            text ("Businesses have Jobs attached to them, and you will be able to set actions"+
                  " which are allowed within the building. Some roles (such as a manager), allow only one worker, others will enable any number of such.")
            null height 10
            text ("If a worker becomes injured or exhausted and unable to perform, "+
                  "his/her action will be set to 'Auto-Rest'. Once in better, the worker will be placed to do whatever activity they used to be doing!")
            null height 10
            text ("Workers may choose to partake in another activity if they are "+
                  "inactive and such a thing is allowed by a rule set in Building controls (Barmaid may decide to do some cleaning if needed for example).")
            null height 10
            text ("There are many Jobs available for workers, and more can be unlocked "+
                  "by adding more businesses. To perform a task, open workable capacity is often required. Once the work is done, the working capacity is released and can be occupied by another client.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_simulation():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "pyp"
        hbox:
            yalign .5
            spacing 2
            text ("The business simulation is achieved by a process-based discrete-event simulation framework."+
                  " The working day is split into 100 Discrete Units of time, 10 more are added to allow your workers to wrap the day up. "+
                  "As long as you have active workers, the working day will continue. "+
                  "There is a rush hour closer to 60DU during which client flow is significantly increased."):
                      xsize 530
            frame:
                add "content/gfx/interface/pyp/simulation.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"
