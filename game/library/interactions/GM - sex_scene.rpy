init python:
    def get_simple_act(char, tags, excluded): # copypaste from jobs without the self part, allows to randomly select one of existing tags sets
        acts = list()
        for t in tags:
            if char.has_image(*t, exclude=excluded):
                acts.append(t)
        if acts:
            act = choice(acts)
        else:
            act = None
        return act
        
        
    def get_single_sex_picture(char=None, act="stripping", location="any", hidden_partner=False, variety=False, rape=False):
        """A universal function that returns most suitable sex picture depending on arguments.
        char - character id
        act - sex act; can be strip,
        location - location where is happens; the function supports following locations: park, forest, beach, dungeon, room, simple (aka simple bg/no bg), any (aka any background is fine)
        all other cases are too rare anyway, and should be handled manually
        hidden_partner - should it try to show the hidden partner pictures first, or it doesn't matter; doesn't work for strip and after_sex, obviously
        variety - should it sometimes show pictures with simple or no bg instead of correct locations for the sake of variety
        rape - is it rape or not; non-rape pictures exclude negative emotions, also dungeon location has the same effect on emotions. Does not matter for strip and after sex.
        """
        if act <> "stripping":
            if location == "dungeon" or rape:
                excluded = []
        else:
            excluded = ["in pain", "scared", "sad"] # a list of unneeded tags

        if act == "stripping":
            excluded.extend(["sleeping", "bathing", "stage", "sex"])
            if location == "beach":
                excluded.extend(["indoors"])
                if dice(50):
                    included = ["beach"]
                else:
                    included = ("beach", "swimsuit")
                if char.has_image("stripping", "beach", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "beach", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "beach", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_act(char, tags)
                    if result:
                        gm.set_img(result, exclude=excluded)
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", *included, type="reduce")
                        else:
                            gm.set_img("nude", *included, exclude=["sex"], type="reduce")
            
            elif location in ["park", "forest"]:
                excluded.extend(["indoors", "onsen", "pool", "beach"])
                if location == "forest":
                    included = ("nature", "wildness")
                else:
                    included = ("nature", "urban")
                if char.has_image("stripping", "nature", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "nature", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "nature", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_act(char, tags)
                    if result:
                        gm.set_img(result, exclude=excluded)
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", *included, type="reduce")
                        else:
                            gm.set_img("nude", *included, exclude=["sex"], type="reduce")
                            
            elif location == "dungeon":
                included = ("indoors", "dungeon")
                excluded.extend(["outdoors", "onsen", "pool", "beach", "happy", "confident", "suggestive"])
                if char.has_image("stripping", "dungeon", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "dungeon", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "dungeon", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_act(char, tags)
                    if result:
                        gm.set_img(result, exclude=excluded)
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", *included, type="reduce")
                        else:
                            gm.set_img("nude", *included, exclude=["sex"], type="reduce")

            elif location == "room":
                included = ("indoors", "living")
                excluded.extend(["outdoors", "onsen", "pool", "beach", "dungeon"])
                if char.has_image("stripping", "indoors", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "indoors", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "indoors", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_act(char, tags)
                    if result:
                        gm.set_img(result, exclude=excluded)
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", *included, type="reduce")
                        else:
                            gm.set_img("nude", *included, exclude=["sex"], type="reduce")
            else:
                tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                result = get_act(char, tags)
                if result:
                    gm.set_img(result, exclude=excluded)
                else:
                    if char.has_image ("stripping"):
                        gm.set_img("stripping", type="reduce")
                    else:
                        gm.set_img("nude", exclude=["sex"], type="reduce")
        return
            
        
    def get_sex_img_4int(char, *args, **kwargs):
        """Tries to find the best possible sex image following a complex set of logic.
        http://www.pinkpetal.org/index.php?topic=1291.msg37131#msg37131
        
        Coded for interactions module.
        """
        # First check if we have a perfect match of all tags:
        if char.has_image(*args, **kwargs):
            gm.set_img(*args, **kwargs)
            return
        
        tags = list(args)
        exclude = kwargs.get("exclude", None)
            
        # Next we give priority to partner_hidden logic:
        if "partner_hidden" in tags:
            ptags = list(t for t in tags if t not in loc_tags)
            if substitute_show_bg(char, ptags, **kwargs):
                return
            
            # No parter_hidden tags found... we subsitute partner_hidden with after_sex
            ptags = tags[:]
            ptags.remove("partner_hidden")
            if "after_sex" not in ptags:
                ptags.append("after_sex")
                
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
            ptags = list(t for t in ptags if t not in loc_tags)
            if substitute_show_bg(char, ptags, **kwargs):
                return
                
        # If threre was no partner_hidden or everything failed:
        if "partner_hidden" in tags:
            tags.remove("partner_hidden")
            
        if char.has_image(*tags, **kwargs):
            gm.set_img(*tags, **kwargs)
            return
            
        ptags = list(t for t in tags if t not in loc_tags)
        if substitute_show_bg(char, ptags, **kwargs):
            return
            
        # We could not find an image with the correct location/bgs, so we go with after_sex:
        ptags = list(t for t in tags if t not in sex_action_tags)
        if "after_sex" not in ptags:
            ptags.append("after_sex")
            
        if char.has_image(*ptags, **kwargs):
            gm.set_img(*ptags, **kwargs)
            return
        
        ptags = list(t for t in tags if t not in loc_tags)
        if substitute_show_bg(char, ptags, **kwargs):
            return
            
        # Still nothing... We try to get a picture just with the after_sex and a location followed by no_bg/simple_bg if no loc was found:
        locs = list(t for t in tags if t in loc_tags)
        if char.has_image("after_sex", *locs, **kwargs):
            gm.set_img("after_sex", *locs, **kwargs)
            return
            
        if substitute_show_bg(char, ["after_sex"], **kwargs):
            return
            
        # //This can be cleaned up and refactored one working correctly!!
        # Drop Nature First:
        if any([t for t in ["outdoors", "urban", "wildness", "suburb", "nature"] if t in tags]):
            ptags = [t for t in tags if t not in ["nature"]]
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
        if any([t for t in ["urban", "wildness", "suburb"] if t in tags]):
            ptags = [t for t in tags if t not in ["urban", "wildness", "suburb"]]
            if "outdoors" not in ptags:
                ptags.append("outdoors")
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
        if any([t for t in ["dungeon", "living", "public"] if t in tags]):
            ptags = [t for t in tags if t not in ["dungeon", "living", "public"]]
            if "indoors" not in ptags:
                ptags.append("indoors")
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
        if any([t for t in ["indoors", "outdoors"] if t in tags]):
            ptags = [t for t in tags if t not in ["indoors", "outdoors", "simple bg", "no bg"]]
            if substitute_show_bg(char, ptags, **kwargs):
                return
                
        if any([t for t in ["beach", "onsen", "pool", "stage"] if t in tags]):
            ptags = [t for t in tags if t not in ["beach", "onsen", "pool", "stage", "simple bg", "no bg"]]
            if substitute_show_bg(char, ptags, **kwargs):
                return
        
        # Finally, we just run the normal show:
        gm.set_img(*args, **kwargs)
