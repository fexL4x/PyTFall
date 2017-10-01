init -11 python:
    def kill_char(char):
        # Attempts to remove a character from the game world.
        # This happens automatiaclly if char.health goes 0 or below.
        char._location = "After Life"
        char.alive = False
        if char in hero.chars:
            hero.corpses.append(char)
            hero.remove_char(char)
        if char in hero.team:
            hero.team.remove(char)
        gm.remove_girl(char)

    def take_team_ap(value):
        """
        Checks the whole hero team for enough AP; if at least one teammate doesn't have enough AP, AP won't decrease, and function will return False, otherwise True
        """
        for i in hero.team:
            if i.AP - value < 0:
                return False
        for i in hero.team:
            i.AP -= value
        return True

    # Characters related:
    def get_first_name(sex="female"):
        """Gets a randomly generated first name.

        sex: male/female
        """
        if sex == "female":
            if not store.female_first_names:
                store.female_first_names = load_female_first_names(200)
            return store.female_first_names.pop()
        elif sex == "male":
            if not store.male_first_names:
                store.male_first_names = load_male_first_names(200)
            return store.male_first_names.pop()
        else:
            raise Exception("Unknow argument passed to get_first_name func!")

    def get_last_name():
        if not store.random_last_names:
            store.random_last_names = load_random_last_names(200)
        return random_last_names.pop()

    def get_team_name():
        if not hasattr(store, "random_team_names") or not store.random_team_names:
            store.random_team_names = load_team_names(50)
        return random_team_names.pop()

    def build_mob(id=None, level=1, max_out_stats=False):
        mob = Mob()
        stats = mob.STATS
        skills = mob.stats.skills.keys()

        if not id:
            id = choice(mobs.keys())

        if not id in mobs:
            raise Exception("Unknown id {} when creating a mob!".format(id))

        data = mobs[id]
        mob.id = id
        mob.min_lvl = data.get("min_lvl", 1)
        mob.name = data.get("name", id)
        mob.desc = data.get("desc", "Some Random Monsta!")

        for i in ("battle_sprite", "portrait", "origin", "locations", "base_race", "race", "front_row"):
            if i in data:
                setattr(mob, i, data[i])

        for skill, value in data.get("skills", {}).iteritems():
            if mob.stats.is_skill(skill):
                mob.stats.mod_full_skill(skill, value)
            else:
                devlog.warning(str("Skill: {} for Mob with id: {} is invalid! ".format(skill, id)))

        # Get and normalize basetraits:
        mob.traits.basetraits = set(traits[t] for t in data.get("basetraits", []))
        for trait in mob.traits.basetraits:
            mob.apply_trait(trait)

        for trait in data.get("traits", []):
            mob.apply_trait(trait)

        if "default_attack_skill" in data:
            skill = data["default_attack_skill"]
            mob.default_attack_skill = store.battle_skills[skill]
        for skill in data.get("attack_skills", []):
            mob.attack_skills.append(store.battle_skills[skill])
        for skill in data.get("magic_skills", []):
            mob.magic_skills.append(store.battle_skills[skill])

        mob.init()

        if level != 1:
            initial_levelup(mob, level, max_out_stats=max_out_stats)

        if not max_out_stats:
            for stat, value in data.get("stats", {}).iteritems():
                if stat != "luck":
                    value = int(round(mob.get_max(stat)*value/float(100)))
                setattr(mob, stat, value)

        return mob

    def build_rc(id=None, name=None, last_name=None, pattern=None, tier=0,
                 tier_kwargs=None, add_to_gameworld=True):
        ''' Creates a random character!
        id: id to choose from the rchars dictionary that holds rGirl loading data
            from JSON files, will be chosen at random if none availible.
        name: (String) Name for a girl to use. If None one will be chosen from randomNames file!
        last_name: Same thing only for last name :)
        pattern: Pattern to use when creating the character! (Options atm: Warrior,
            ServiceGirl, Prostitute, Stripper, Manager) If None, we use data or normalize in init()
        teir: Tier of the character... floats are allowed.
        add_to_gameworld: Adds to characters dictionary, should always
        be True unless character is created not to participate in the game world...
        '''
        if tier_kwargs is None:
            tier_kwargs = {}
        rg = rChar()
        Stats = rg.STATS
        Skills = rg.stats.skills.keys()

        if not id:
            id = choice(rchars.keys())

        if id in rchars:
            data = rchars[id]
            rg.id = id
        else:
            raise Exception("Unknown id {} when creating a random character!".format(id))

        # rg.id = id

        # Elements:
        if "elements" in data:
            for key in data["elements"]:
                if dice(data["elements"][key]):
                    if key not in traits:
                        key = key.split(" ")[0]
                    if key not in traits:
                        devlog.warning("Element (*Split with ' '): {} for random girl with id: {} is not a valid element for this game!".format(str(key), str(id)))
                        continue
                    rg.apply_trait(traits[key])

        # Traits next:
        if "random_traits" in data:
            for trait in data["random_traits"]:
                chance = trait[1]
                trait = trait[0]
                if dice(chance):
                    if trait in traits:
                        rg.apply_trait(traits[trait])
                    else:
                        devlog.warning("Trait: {} for random girl with id: {} is not a valid trait for this game!".format(str(trait), str(id))) # Added str() call to avoid cp850 encoding

        # Names/Origin:
        if not name:
            if not store.female_first_names:
                store.female_first_names = load_female_first_names(200)
            rg.name = get_first_name()
        else:
            rg.name = name

        if not last_name:
            rg.fullname = " ".join([rg.name, get_last_name()])

        rg.nickname = rg.name

        if "origin" not in data:
            rg.origin = "Random Girl"

        # Status next:
        if "force_status" in data:
            if data["force_status"]:
                rg.status = data["force_status"]
            else:
                rg.status = choice(["slave", "free"])

        # Location if forced:
        if "force_location" in data:
            if data["force_location"]:
                rg.location = data["force_location"]

        # Occupations:
        if pattern: # In case if there is no pattern,
            rg.traits.basetraits = set(create_traits_base(pattern))
            for t in rg.traits.basetraits:
                rg.apply_trait(t)
        # This is possibly temporary: TODO: Update after discussion:
        # if "init_basetraits" in data:
            # d = data["init_basetraits"]
            # if pattern not in d:
                # devlog.warning(str("{} Random Girl tried to apply blocked pattern: {}!".format(id, pattern)))
            # rg.occupation = choice(d)

        # Battle and Magic skills:
        if "battle_skills" in data:
            d = data["battle_skills"]
            if d in store.battle_skills:
                rg.attack_skills.append(store.battle_skills[d])
            else:
                devlog.warning(str("%s Random Girl tried to apply unknown battle skill: %s!" % (id, d)))

        if "magic_skills" in data:
            d = data["magic_skills"]
            for skill in d:
                if dice(skill[1]):
                    if skill[0] in store.battle_skills:
                        rg.magic_skills.append(store.battle_skills[skill[0]])
                    else:
                        devlog.warning(str("%s Random Girl tried to apply unknown battle skill: %s!" % (id, skill[0])))

        # SKILLS:
        if "random_skills" in data:
            d = data["random_skills"]
            for key in d:
                if key.lower() in Skills:
                    value = randint(d[key][0], d[key][1])
                    rg.stats.mod_full_skill(key)
                else:
                    devlog.warning(str("Skill: %s for random girl with id: %s is invalid! "%(key, id)))

        # STATS:
        if "random_stats" in data:
            d = data["random_stats"]
            for key in d:
                if key in Stats:
                    if key != "luck":
                        value = randint(d[key][0], d[key][1])
                        value = int(round(float(value)*100 / rg.get_max(key)))
                        rg.mod_stat(key, value)
                    elif key == "luck":
                        rg.mod_stat(key, randint(d[key][0], d[key][1]))
                else:
                    devlog.warning(str("Stat: %s for random girl with id: %s is invalid! " % (key, id)))

        # Normalizing if not all stats were supplied:
        for stat in Stats:
            if stat not in rg.stats.FIXED_MAX and getattr(rg, stat) == 0:
                setattr(rg, stat, randint(10, 25))

        # Rest of the expected data:
        for i in ("origin", "gold", "desc", "height", "full_race"):
            if i in data:
                setattr(rg, i, data[i])

        if "race" in data:
            trait = data["race"]
            if trait in traits:
                rg.apply_trait(traits[trait])
            else:
                devlog.warning("%s is not a valid race (build_rc)!" % (trait))

        # Colors in say screen:
        for key in ("color", "what_color"):
            if key in data:
                if data[key] in globals():
                    color = getattr(store, data[key])
                else:
                    try:
                        color = Color(data[key])
                    except:
                        devlog.warning("{} color supplied to {} is invalid!".format(gd[key], gd["id"]))
                        color = ivory
                rg.say_style[key] = color

        # Normalizing new girl:
        # We simply run the init method of parent class for this:
        super(rChar, rg).init()

        # And at last, leveling up and stats/skills applications:
        tier_up_to(rg, tier, **tier_kwargs)

        # And add to char! :)
        if add_to_gameworld:
            store.chars["_".join([rg.id, rg.name, rg.fullname.split(" ")[1]])] = rg

        return rg

    def give_tiered_items(char, amount=1, occ=None):
        """Gives items based on tier and class of the character.

        amount: Usually 1, this number of items will be awarded per slot.
        occ: General occupation that we equip for: ()
        """
        tier = max(min(round_int(char.tier*.5), 5), 0)
        if base_trait is None:
            base_trait = random.sample(char.basetraits)[0]
        items = tiered_items[tier]



        'body', 'head', 'feet'
        'wrist', 'amulet'
        'cape'

        'weapon'

        'misc'

        'ring' 'ring1' 'ring2'

        'smallweapon'

    def initial_levelup(char, level, max_out_stats=False):
        """
        This levels up the character, usually when it's first created.
        """
        exp = level*(level-1)*500
        char.stats.level = 1
        char.exp = 0
        char.stats.goal = 1000
        char.stats.goal_increase = 1000

        char.exp += exp

        if max_out_stats:
            for stat in char.stats.stats:
                if stat not in char.stats.FIXED_MAX:
                    setattr(char, stat, char.get_max(stat))
        # --------

    def adjust_exp(char, exp):
        '''
        Adjusts experience according to a level of character.
        We will find a better way to handle experience in the future.
        '''
        if char == hero:
            if char.level < 10:
                return int(math.ceil(char.level * exp)*1.4)
            elif char.level < 30:
                return int(math.ceil(char.level * exp)*1.3)
            elif char.level < 40:
                return int(math.ceil(char.level * exp)*1.2)
            else:
                return int(math.ceil(char.level * exp)*1.1)
        elif isinstance(char, Char):
            if char.level < 10:
                return int(math.ceil(char.level * exp)*0.9)
            elif char.level < 20:
                return int(math.ceil(char.level * exp)*0.8)
            elif char.level < 30:
                return int(math.ceil(char.level * exp)*0.75)
            elif char.level < 40:
                return int(math.ceil(char.level * exp)*0.70)
            elif char.level < 50:
                return int(math.ceil(char.level * exp)*0.65)
            elif char.level < 60:
                return int(math.ceil(char.level * exp)*0.6)
            elif char.level < 70:
                return int(math.ceil(char.level * exp)*0.5)
            else:
                return int(math.ceil(char.level * exp)*0.4)
        return int(math.ceil(char.level * exp))

    def create_traits_base(pattern):
        """
        Mostly used for NPCs and Random Characters.
        The idea is to attempt creation of interesting and dynamic blue-prints.
        For the future this prolly should return a matrix or a dict with prof-base and support traits separately...
        """
        _traits = list()
        if pattern == "Warrior":
            basetrait = choice([traits["Warrior"], traits["Mage"]])
            _traits.append(basetrait)
        elif pattern == "ServiceGirl":
            _traits.append(traits["Maid"])
        elif pattern == "Prostitute":
            _traits.append(traits["Prostitute"])
        elif pattern == "Stripper":
            _traits.append(traits["Stripper"])
        elif pattern == "Manager":
            _traits.append(traits["Manager"])
        else:
            raise Exception("Cannot create base traits list from pattern: {}".format(pattern))

        # Should never return more than two traits! That is expected by callers of this func!
        return _traits

    def build_client(id=None, gender="male", caste="Peasant", name=None, last_name=None,
                     pattern=None, likes=None, dislikes=None, tier=1):
        """
        This function creates Customers to be used in the jobs.
        Some things are initiated in __init__ and funcs/methods that call this.

        - pattern: Pattern (string) to be supplied to the create_traits_base function.
        - likes: Expects a list/set/tuple of anything a client may find attractive in a worker/building/upgrade, will be added to other likes (mostly traits), usually adds a building...
        """
        client = Customer(gender, caste)

        if not id:
            client.id = "Client" + str(random.random())

        if name:
            client.name = name
        else:
            client.name = get_first_name(gender)

        if last_name:
            client.fullname = client.name + " " + last_name
        else:
            client.fullname = client.name + " " + get_last_name()

        # Patterns:
        if not pattern:
            pattern = random.sample(client.GEN_OCCS, 1).pop()
        pattern = create_traits_base(pattern)
        for i in pattern:
            client.traits.basetraits.add(i)
            client.apply_trait(i)

        # Add a couple of client traits: <=== This may not be useful...
        trts = random.sample(tgs.client, randint(2, 5))
        for t in trts:
            client.apply_trait(t)

        # Likes:
        # Add some traits from trait groups:
        cl = set()
        cl.add(choice(tgs.breasts))
        cl.add(choice(tgs.body))
        cl.add(choice(tgs.race))
        cl = cl.union(random.sample(tgs.base, randint(1, 2)))
        cl = cl.union(random.sample(tgs.elemental, randint(2, 3)))
        cl = cl.union(random.sample(tgs.ct, randint(2, 4)))
        cl = cl.union(random.sample(tgs.sexual, randint(1, 2)))
        client.likes = cl

        if likes:
            client.likes = client.likes.union(likes)
            # We pick some of the traits to like/dislike at random.

        tier_up_to(client, tier)

        return client

    def create_arena_girls():
        rgirls = store.rchars.keys()
        for i in xrange(85):
            if not rgirls: rgirls = store.rchars.keys()
            if rgirls:
                rgirl = rgirls.pop()
                arena_girl = build_rc(id=rgirl, pattern="Warrior")
                arena_girl.arena_willing = True
                arena_girl.arena_active = False # Should prolly be moved to preparation?
                arena_girl.status = "free"

    def copy_char(char):
        """Due to some sh!tty coding on my part, just a simple deepcopy/copy will not do :(

        This func cannot be used to make a playable character that can properly interact with the game world.
        """
        if isinstance(char, PytGroup):
            char = char._first

        # new = deepcopy(char)
        # Trying to improve the performace:
        new = pickle.loads(pickle.dumps(char, -1))

        # One More Attempt through class Instantiation, does not work yet:
        # new = char.__class__()
        # Stats copy (Only for the new instance attempt)
        # new.id = char.id
        # new.location = shallowcopy(char.location)
        # new.stats = shallowcopy(char.stats)
        # new.stats.instance = new
        # # Effects (Also, just for the new instance attempt)
        # if hasattr(char, "effects"):
            # new.effects = char.effects.copy()

        # Traits copy:
        # real_traits = list(traits[t] for t in [trait.id for trait in char.traits])
        # new.traits[:] = real_traits
        new.traits[:] = list(char.traits)
        new.traits.normal = char.traits.normal.copy()
        new.traits.items = char.traits.items.copy()
        new.traits.ab_traits = char.traits.ab_traits.copy()
        new.traits.blocked_traits = char.traits.blocked_traits.copy()
        new.traits.basetraits = char.traits.basetraits.copy()

        # Equipment slots/Item mods:
        new.eqslots = char.eqslots.copy()
        new.miscitems = char.miscitems.copy()
        new.consblock = char.consblock.copy()
        new.constemp = char.constemp.copy()

        # Skills:
        # real_attack_skills = list(battle_skills[s] for s in [skill.name for skill in char.attack_skills])
        # new.attack_skills[:] = real_attack_skills
        new.attack_skills[:] = list(char.attack_skills)
        new.attack_skills.normal = char.attack_skills.normal.copy()
        new.attack_skills.items = char.attack_skills.items.copy()

        # real_magic_skills = list(battle_skills[s] for s in [skill.name for skill in char.magic_skills])
        # new.magic_skills[:] = real_magic_skills
        new.magic_skills[:] = list(char.magic_skills)
        new.magic_skills.normal = char.magic_skills.normal.copy()
        new.magic_skills.items = char.magic_skills.items.copy()

        return new

    def set_char_to_work(char, building, job=False):
        """Attempts to find the best possible job to the char in given building.

        For now it just randomly picks any fitting job or sets to None.
        In the future, this should find the best possible job and set the char to it.

        Note: Due to older logic, this function expects job argument to be None when a character is made jobless by player input or game logic!
        """
        if isinstance(char, PytGroup):
            for c in char.lst:
                set_char_to_work(c, building, job)
            return
        if job is False:
            available_jobs = list(j for j in building.jobs if j.all_occs & char.occupations)
            job = choice(available_jobs) if available_jobs else None

        # We want to remove char as a building manager if he/she leave the post, we don't do that when char is set to rest or auto-rest.
        if building.manager == char:
            sj = store.simple_jobs
            if job not in (sj["Manager"], sj["Rest"], sj["AutoRest"]):
                building.manager = None

        char.action = job
        # We prolly still want to set a workplace...
        char.workplace = building

        if job is None:
            return

        if hasattr(building, "all_workers"):
            if char not in building.all_workers:
                building.all_workers.append(char)

        # Make sure that the manager is set:
        if job == simple_jobs["Manager"]:
            building.manager = char

    def tier_up_to(char, tier, level_bios=(.9, 1.1),
                   skill_bios=(.8, 1.2), stat_bios=(.8, 1.0)):
        """Tiers up a character trying to set them up smartly

        @params:
        char: Character object or id
        tier: Tier number to level to (10 is max and basically a God)
        bios: When setting up stats and skills, uniform between the two values
              will be used.
              Level, stats and skills bioses work in the same way

        Important: Should only be used right after the character was created!
        """
        level_bios = partial(random.uniform, level_bios[0], level_bios[1])
        skill_bios = partial(random.uniform, skill_bios[0], skill_bios[1])
        stat_bios = partial(random.uniform, stat_bios[0], stat_bios[1])
        # Level with base 20
        level = tier*20
        if level:
            level = round_int(level*level_bios())
            initial_levelup(char, level)

        # Do the stats/skills:
        base_skills = set()
        base_stats = set()
        # !!! Using weight may actually confuse thing in here... this needs testing.
        # Also, it may be a good idea to do list(s) of stats/skills every ht char should have a bit of...
        for trait in char.traits.basetraits:
            skills = trait.base_skills
            total_weight_points = sum(skills.values())
            for skill, weight in skills.items():
                base_skills.add(skill)
                weight_ratio = float(weight)/total_weight_points
                sp = SKILLS_MAX[skill]*(tier*.1)
                weight_sp = weight_ratio*sp
                biosed_sp = round_int(weight_sp*skill_bios())

                char.mod_skill(skill, biosed_sp)

            stats = trait.base_stats
            total_weight_points = sum(stats.values())
            for stat, weight in stats.items():
                base_stats.add(stat)
                weight_ratio = float(weight)/total_weight_points
                sp = char.get_max(stat)
                weight_sp = weight_ratio*sp
                biosed_sp = round_int(weight_sp*stat_bios())

                char.mod_skill(skill, biosed_sp)

        # Now that we're done with baseskills, we can play with other stats/skills a little bit
        for stat in char.stats.stats:
            if stat not in char.stats.FIXED_MAX and stat not in base_stats:
                if dice(char.luck*.5):
                    value = char.get_max(stat)*.3
                    value = round_int(value*stat_bios())
                    char.mod_stat(stat, value)
                else:
                    value = char.get_max(stat)*random.uniform(.05, .15)
                    value = round_int(value*stat_bios())
                    char.mod_stat(stat, value)
        for skill in char.stats.skills:
            if skill not in base_skills:
                if dice(char.luck*.5):
                    value = (SKILLS_MAX[skill]*(tier*.1))*.3
                    value = round_int(value*skill_bios())
                    char.mod_skill(skill, value)
                else:
                    value = (SKILLS_MAX[skill]*(tier*.1))*random.uniform(.05, .15)
                    value = round_int(value*skill_bios())
                    char.mod_skill(skill, value)

        char.tier = round_int(tier) # Makes sure we can use float tiers
