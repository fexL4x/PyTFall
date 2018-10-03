init python:
    # Note: We may get this from grouping traits, but that still feels a bit clumsy atm.
    base_trait_presets = {
    "Combatant": (["Warrior", "Mage"], ["Warrior", "Knight"],
                  ["Warrior", "Shooter"], ["Warrior", "Assassin"]),
    "Warrior": (["Warrior"], ["Knight"], ["Warrior", "Knight"]),
    "Caster": (["Mage"], ["Mage", "Warrior"]),
    "Assassin": (["Assassin"], ["Assassin", "Shooter"]),
    "Healer": (["Healer"], ["Healer", "Mage"], ["Healer", "Maid"]),
    "SIW": (["Prostitute", "Stripper"], ),
    "Prostitute": (["Prostitute"], ),
    "Stripper": (["Stripper"], ["Stripper", "Maid"]),
    "Maid": (["Maid"], ["Barmaid"], ["Cleaner"]),
    "Specialist": (["Manager", "Barmaid"], ["Manager", "Stripper"], ["Manager", "Healer"],
                   ["Manager", "Mage"]),
    "Manager": (["Manager"], )
    }

    base_traits_groups = {"Combatant": ["Combatant", "Warrior", "Caster", "Assassin"],
                          "SIW": ["SIW", "Prostitute", "Stripper"],
                          "Healer": ["Healer"],
                          "Server": ["Maid"],
                          "Specialist": ["Specialist", "Manager"]}

init python:
    def hyperlink_styler(link):
        return style.hyperlink_text

    def hyperlink_clicked(link):
        return link

    def hyperlink_hovered(link):
        return None
         
    style.default.hyperlink_functions = (hyperlink_styler, hyperlink_clicked, hyperlink_hovered)