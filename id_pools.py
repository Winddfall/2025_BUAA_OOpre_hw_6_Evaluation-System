# --- ID 池定义 ---
adventurer_id_pool = [
# 原有人名
"Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace",
"Maximus", "Seraphina", "Kaelen", "Lyra", "Orion", "Thorn",
"Zephyr", "Isolde", "Corvus", "Ember", "Finnian", "Rowan",

# 传统风格人名（新增）
"Arthur", "Brianna", "Cedric", "Daphne", "Eldric", "Fiona", "Gavin",
"Hilda", "Igor", "Jasmine", "Kyle", "Lila", "Marius", "Nora", "Owen",
"Penelope", "Quentin", "Rosalind", "Silas", "Tabitha", "Ulysses", "Vera",
"Warren", "Xena", "Yannick", "Zara", "Alaric", "Bianca", "Casper", "Diana",
"Ewan", "Freya", "Gideon", "Hannah", "Ivan", "Jade", "Kara", "Leland",
"Maya", "Nico", "Ophelia", "Percy", "Quinn", "Roland", "Sage", "Tobias",
"Uriah", "Violet", "Walter", "Xander", "Yvette", "Zachary", "Amelia", "Benjamin",
"Clara", "Damian", "Elena", "Felix", "Greta", "Henry", "Ivy", "Jasper",

# 奇幻风格人名（新增）
"Aelar", "Bree", "Corin", "Dara", "Eldar", "Faelon", "Gimble",
"Hilda", "Ithilwen", "Jorndan", "Kael", "Lirael", "Mordecai", "Nerys",
"Oona", "Phelan", "Qara", "Riona", "Soren", "Tahlia", "Uthar", "Vex",
"Wren", "Xan", "Yasha", "Zedd", "Arwen", "Borin", "Calen", "Drizzt",
"Elara", "Fenrir", "Gimli", "Hilda", "Inigo", "Jynx", "Kili", "Luna",
"Mordred", "Nyx", "Odin", "Pandora", "Questor", "Raven", "Sable", "Thorne",
"Umbra", "Vaelin", "Wulfgar", "Xylia", "Yorick", "Zelda", "Astra", "Bramble",
"Cypher", "Dusk", "Ember", "Falcon", "Glimmer", "Hearth", "Ironwill", "Jynara",

# 异域风格人名（新增）
"Akira", "Bao", "Chiyo", "Dai", "Emiko", "Fujin", "Goro",
"Hana", "Ichiro", "Jun", "Kimi", "Ling", "Mako", "Nori", "Osamu",
"Ping", "Qiu", "Ryo", "Sato", "Takeshi", "Uma", "Vinh", "Wei",
"Xiao", "Yuki", "Zhen", "Aziz", "Banu", "Cem", "Dilara", "Ehsan",
"Farid", "Gul", "Hakan", "Iman", "Jalal", "Kamal", "Laleh", "Mehmet",
"Nadia", "Omar", "Parisa", "Qasim", "Rana", "Sami", "Tara", "Umar",
"Vera", "Waleed", "Xanthe", "Yusuf", "Zara", "Aiden", "Brynn", "Cora",
"Dex", "Elio", "Flora", "Grey", "Hugo", "Iris", "Jax", "Kai",

# 新增冒险家风格名字
"Stormwind", "Ironfist", "Moonwhisper", "Darkthorn", "Brightshield",
"Swiftfoot", "Stonehelm", "Shadowstep", "Dragonheart", "Wolfsbane",
"Eagleeye", "Bearclaw", "Ravenwing", "Lionheart", "Viperstrike",
"Phoenixrise", "Grimbold", "Starfall", "Ironvein", "Silverleaf",
"Blackthorn", "Goldfury", "Ironwill", "Steelshank", "Coppertoe",
"Bronzebrow", "Platinumbrow", "Diamondeye", "Emeraldsong", "Rubyrose",
"Sapphirewave", "Amethystveil", "Topaztide", "Onyxshadow", "Pearlshine",
"Cobaltwind", "Crimsonfury", "Ivorylight", "Jadeclaw", "Jetblack",
"Quartzshield", "Opalight", "Tourmaline", "Garnetfist", "Aquamarine",
"Peridot", "Lapis", "Malachite", "Obsidian", "Turquoise"
]

# 药水ID池
bottle_id_pool = [
# 原有药水扩展
"HealPotion", "ManaPotion", "SpeedPotion", "StrengthPotion", "DexterityPotion",
"ElixirOfLife", "Mageblood", "Swiftbrew", "Titan'sTonic", "ShadowDraught",
"GlimmerleafAura", "DragonbreathSerum", "FrostfireExtract", "SoulEssence", "Witch'sBane",

# 治疗类药水
"VitalityVial", "RegenerationElixir", "WoundWash", "LifeforceLotion", "HeartmendDraught",
"RejuvenationPotion", "BloodbindTincture", "AnimaElixir", "ScarlessSalve", "VigorVineExtract",
"PulsePotion", "LifegivingLiqueur", "ReviveDew", "HealthHoney", "VitalizingVodka",
"CureAllConcoction", "HealingHaze", "MendMead", "LifebloomBrew", "RestorativeRum",
"CellRegenTonic", "TraumaTonic", "ScarFadeSolution", "VitalSpiritSip", "PulseRestorePotion",
"WoundWeaveElixir", "BoneBondBalm", "MuscleMendMist", "OrganOintment", "NerveNurseNectar",
"BloodBoostBeverage", "FleshFixFluid", "AuraHealAmpoule", "SpiritSootheSip", "VitalityVortexVial",

# 魔法类药水
"ArcaneAmbrose", "Wizard'sWine", "ManaMead", "Spellcaster'sSip", "Enchanter'sElixir",
"MagickaMarmalade", "Sorcerer'sSap", "WandWash", "MysticMead", "CharmChaser",
"Conjurer'sCordial", "HexHoney", "IncantationInfusion", "MagicMilk", "RuneRum",
"SorcerySyrup", "Witch'sWort", "Wizard'sWellwater", "MysteryMead", "EnchantmentElixir",
"ArcaneAmpoule", "ManaMist", "SpellSip", "CharmChaser", "Wizard'sWash",
"MagicMist", "EnchantElixir", "SorcerySoda", "ConjureConcoction", "RuneRefresh",
"MysticMist", "Witch'sWash", "Wizard'sWard", "ArcaneAura", "MagickaMist",

# 属性增强类药水
"BrawnBrew", "CunningConcoction", "DexterityDew", "EnduranceElixir", "FocusFluid",
"GuileGrog", "HardinessHooch", "IntellectInfusion", "JudgmentJuice", "KeennessKoolaid",
"LuckLiquor", "MightMead", "NimblenessNectar", "ObservantOil", "PowerPotion",
"QuicknessQuaff", "ResolveRum", "StrengthSuds", "ToughnessTonic", "VigorVodka",
"AgilityAmpoule", "BraveryBrew", "ClevernessCordial", "DiligenceDraught", "EnergyElixir",
"FortitudeFluid", "GritGrog", "HasteHoney", "IntuitionInfusion", "JuggernautJuice",
"KnowledgeKombucha", "LeadershipLiqueur", "MentalMightMead", "NimbleNectar", "OversightOil",

# 特殊效果药水
"InvisibilityInfusion", "LevitationLiqueur", "FireResistFizz", "FrostFendFizz",
"ShockShieldSoda", "PoisonProofPotion", "FearlessFlask", "NightVisionNectar",
"WaterBreathingWine", "FlightPotion", "TeleportTonic", "ShapeShiftSyrup",
"TimeTwistTincture", "IllusionElixir", "SummoningSap", "BanishBrew", "CurseCureConcoction",
"BlessedBeverage", "HolyHoney", "Demon'sDreadDrink", "Angel'sAmbrosia", "Dragon'sDraught",
"PhoenixPotion", "UnicornUrine", "GriffinGrog", "MermaidMead", "SphinxSpirit",
"KrakenKoolaid", "HydraHooch", "ChimeraCordial", "WyvernWine", "BeholderBrew",

# 新增特殊效果药水
"GhostformGrog", "GiantGrowthGuzzle", "ShrinkSerum", "PhasingPotion", "EtherealElixir",
"DetectMagicDew", "TrueSightTonic", "MagicResistRum", "CurseCastingConcoction", "BlessingBrew",
"SummonSteedSip", "MinionMead", "ElementalEssence", "WeatherWardWine", "EarthquakeElixir",
"StormSip", "SunshineSoda", "MoonlightMead", "StarshineSyrup", "VoidVodka",
"LightLiqueur", "DarkDraught", "SoundlessSip", "SilenceSolution", "EchoElixir",
"TelepathyTonic", "MindShieldMead", "CharmResistRum", "FearFendFluid", "IllusionImmunityInfusion",
"TimeSlowTincture", "HasteHooch", "RegrowLimbLotion", "UndeadUnholyUrn", "HolyBlessingBalm",
"DemonDetectionDraught", "AngelAllureAmpoule", "DragonDreadDew", "FaeFriendFizz", "DwarfDelightDram",
"ElfEaseElixir", "OrcOomphOil", "TrollToughTonic", "GoblinGleeGrog", "KoboldKickKoolaid",
"GiantsGrowGuzzle", "DragonfireDefenseDew", "LycanthropyLotion", "VampirismVodka", "FeyFrenzyFluid",
"ElementalFormElixir", "MetamorphosisMead", "PolymorphPotion", "ShapeShiftSyrup", "DisguiseDew",
"CamouflageConcoction", "StealthSip", "AmbushAmpoule", "Assassin'sElixir", "SpySyrup",
"Scout'sSolution", "Ranger'sRefresh", "Tracker'sTonic", "Hunter'sHooch", "Predator'sPotion",
"PreyProtectionPotion", "HerbHunterHelper", "Miner'sMightMead", "Smith'sStrengthSip", "Crafter'sCordial",
"Merchant'sMuseMead", "Bard'sBoostBeverage", "Cleric'sBlessingBrew", "Fighter'sFortitudeFluid", "Rogue'sRuseRum",
"Wizard'sWisdomWine", "Warlock'sWitWash", "Paladin'sPurityPotion", "Ranger'sResilienceRefresh", "Monk'sMentalMead"
]

# 剑类装备ID池
sword_id_pool = [
    # 原有剑类装备
    "IronSword", "SteelLongsword", "ElvenShortsword", "DwarvenWaraxe", "OrcishScimitar",
    "VampiricBlade", "FlamingGreatsword", "FrostbrandSabre", "LightningLongsword",
    "HolyAvenger", "DemonSlayer", "DragontoothDagger", "EtherealEdge", "AdamantineClaymore",
    "MithrilRapier", "VoidReaver", "StarsteelSabre", "MoonlitMesser", "SunforgedSword",
    "CopperDagger", "BronzeSword", "SilverBlade", "GoldSword", "PlatinumSword",
    "TitaniumSword", "DiamondSword", "CrystalSword", "BoneSword", "WoodenSword",
    "StoneSword", "ObsidianSword", "RubySword", "SapphireSword", "EmeraldSword",
    "TopazSword", "AmethystSword", "GarnetSword", "PearlSword", "IvorySword",
    "EbonySword", "MahoganySword", "OakSword", "PineSword", "MapleSword",
    "BirchSword", "CedarSword", "ElmSword", "AshSword", "HickorySword",
    "WalnutSword", "CherrySword", "RosewoodSword", "TeakSword", "BambooSword",
    "RattanSword", "ReedSword", "CaneSword", "BambooSword", "WillowSword"
]

# 魔法书类装备ID池
magicbook_id_pool = [
    # 原有魔法类装备
    "MagicStaff", "WandOfAges", "SunstoneBow", "Serpent'sFang", "CelestialScepter",
    "YewLongbow", "CrossbowOfAccuracy", "ElvenShortbow", "DwarvenHandcannon", "OrcishJavelin",
    "PoisonedDarts", "FireArrowQuiver", "IceSpear", "ThunderBolt", "StarfuryBow",
    "ShadowArrow", "HolyArrow", "DragonboneBow", "EtherealArrow", "MithrilCrossbow",
    "FireWand", "FrostStaff", "ThunderRod", "ShadowOrb", "HolyMace",
    "ArcaneScepter", "NatureWand", "DeathStaff", "LifeCane", "ChaosOrb",
    "OrderScepter", "ElementalStaff", "CosmicWand", "VoidScepter", "LightMace",
    "SpellbookOfFire", "TomeOfIce", "GrimoireOfLightning", "BookOfShadows", "CodexOfLight",
    "ScrollOfArcane", "TabletOfNature", "ParchmentOfDeath", "VolumeOfLife", "ManualOfChaos",
    "CompendiumOfOrder", "EncyclopediaOfElements", "DictionaryOfCosmos", "LexiconOfVoid", "GlossaryOfLight",
    "SpellbookOfFlames", "TomeOfFrost", "GrimoireOfThunder", "BookOfDarkness", "CodexOfHoliness",
    "ScrollOfMagic", "TabletOfEarth", "ParchmentOfWind", "VolumeOfWater", "ManualOfSpirit",
    "CompendiumOfMind", "EncyclopediaOfSoul", "DictionaryOfTime", "LexiconOfSpace", "GlossaryOfDimension"
]

# 防具类装备ID池
armour_id_pool = [
    # 原有防具装备
    "LeatherArmor", "SteelShield", "GoldenAxe", "MythrilBlade", "ObsidianPlate",
    "RunedBuckler", "WarhammerOfGiants", "VoidwalkerCloak", "CrimsonGreaves",
    "IronHelm", "SteelCap", "ElvenCirclet", "DwarvenHelm", "OrcishSkullcap",
    "VampiricCowl", "FlamingHelm", "FrostedCrown", "LightningHeadguard",
    "HolyCrown", "DemonHorns", "DragonhideHelm", "EtherealCowl", "AdamantineHelmet",
    "LeatherJerkin", "ChainShirt", "PlateMail", "ElvenSilkVest", "DwarvenPlate",
    "OrcishWarbelt", "VampiricCloak", "FlamingCuirass", "FrostedBreastplate",
    "LightningMail", "HolyRobe", "DemonHide", "DragonScaleArmor", "EtherealTunic",
    "IronGauntlets", "SteelGreaves", "ElvenGloves", "DwarvenBoots", "OrcishBracers",
    "VampiricGrips", "FlamingGauntlets", "FrostedBoots", "LightningBracers",
    "HolySandals", "DemonClaws", "DragontoothGreaves", "EtherealGloves", "AdamantineSabatons",
    "WoodenShield", "IronBuckler", "SteelShield", "ElvenShield", "DwarvenTowerShield",
    "OrcishSpikedShield", "VampiricAegis", "FlamingShield", "FrostedBarrier",
    "LightningShield", "HolyAura", "DemonShield", "DragonShield", "EtherealBarrier",
    "AmuletOfHealth", "RingOfProtection", "CloakOfInvisibility", "BeltOfStrength",
    "BootsOfSpeed", "GauntletsOfPower", "NecklaceOfMana", "EarringsOfDexterity",
    "RingOfRegeneration", "CrownOfWisdom", "BraceletOfFortitude", "PendantOfCourage",
    "AnkletOfAgility", "TalismanOfLuck", "CharmOfProtection",
    "LeatherCap", "ChainHood", "PlateHelmet", "SilkHood", "ScaleHelm",
    "BoneHelmet", "WoodenHelmet", "StoneHelmet", "CrystalHelmet", "GemHelmet",
    "LeatherVest", "ChainVest", "PlateArmor", "SilkRobe", "ScaleArmor",
    "BoneArmor", "WoodenArmor", "StoneArmor", "CrystalArmor", "GemArmor",
    "LeatherGloves", "ChainGloves", "PlateGauntlets", "SilkGloves", "ScaleGloves",
    "BoneGloves", "WoodenGloves", "StoneGloves", "CrystalGloves", "GemGloves",
    "LeatherBoots", "ChainBoots", "PlateBoots", "SilkBoots", "ScaleBoots",
    "BoneBoots", "WoodenBoots", "StoneBoots", "CrystalBoots", "GemBoots"
]

# 法术ID池
spell_id_pool = [
# 原有法术扩展
"Fireball", "Heal", "IceLance", "Thunderclap", "ShadowBolt", "HolyLight",
"ArcaneMissile", "Rejuvenate", "ChainLightning", "DrainLife", "FrostNova",
"EarthShield", "Sunfire", "Moonbeam", "Starfall",

# 元素类法术 - 火
"FireBolt", "FlameStrike", "FireShield", "Inferno", "Incinerate", "FlameWave",
"FireballBarrage", "Ignite", "Scorch", "SearingRay", "Firestorm", "MoltenBlast",
"Blaze", "EmberShower", "PhoenixFlame",
"Cauterize", "Wildfire", "FlameWard", "AshCloud", "LavaFlow",
"FireJet", "Burnout", "FurnaceBlast", "Kindle", "Pyroblast",
"Combustion", "MagmaEruption", "HeatWave", "FireAura", "Dragon'sBreath",

# 元素类法术 - 水/冰
"FrostBolt", "IceStorm", "FrostArmor", "Freeze", "IceBarrier", "Blizzard",
"Hailstorm", "Frostbite", "ChillTouch", "Glacier", "IceSpike", "FrostWave",
"SleetStorm", "Permafrost", "AquaJet",
"WaterWhip", "TidalWave", "FrostLance", "IceSpear", "Snowstorm",
"IcyGrasp", "FrostNova", "FrozenOrb", "MistForm", "Drown",
"WaterBreathing", "Tsunami", "HailBarrage", "FrostWard", "Crystalize",

# 元素类法术 - 雷/电
"LightningBolt", "Thunderstorm", "Electrocute", "Shock", "LightningShield",
"ThunderWave", "StormSurge", "StaticCharge", "LightningArc", "ElectricNova",
"ThunderClap", "BoltOfLightning", "EnergyBlast", "PlasmaBall", "ShockingGrasp",
"Thunderbolt", "LightningChain", "ElectricalAura", "StormShield", "BallLightning",
"ThunderousRoar", "ElectrostaticField", "LightningBlast", "Jolt", "TeslaCoil",
"LightningStorm", "ThunderShield", "ElectricArmor", "Charge", "StormCall",

# 元素类法术 - 土/自然
"Earthquake", "RockSlide", "VineGrasp", "ThornWhip", "Nature'sBloom", "RootBind",
"StoneSkin", "MudSlide", "Barkskin", "Regrowth", "Sprout", "WildGrowth", "EarthBolt",
"CrystalSpike", "Nature'sWrath",
"Entangle", "RockShield", "EarthenGrip", "MossCover", "BramblePatch",
"Quicksand", "CrystalForest", "Mountain'sWrath", "RootNetwork", "ThornBarrier",
"Nature'sBlessing", "GrowthSurge", "FungalInfestation", "InsectSwarm", "VenomousSting",
"VineLash", "SeedBomb", "WoodenGolem", "RockGolem", "EarthPrison",

# 神圣/光明类法术
"HolySmite", "DivineProtection", "Bless", "Purify", "Resurrect", "HolyAura",
"GuardianAngel", "LightOfDivinity", "SacredShield", "DivineIntervention",
"HolyNova", "BlessedStrike", "Radiance", "Illumination", "HeavenlyLight",
"HolyBolt", "DivineShield", "BlessedAura", "LightBlast", "Purification",
"DivineFavor", "HolyRetribution", "AngelicGuardian", "LuminousShield", "Sanctify",
"HallowedGround", "DivineHealing", "HolyWard", "SacredFlame", "RighteousSmite",
"CelestialBlessing", "AngelicWings", "DivineWrath", "LightWell", "Halo",

# 暗影/亡灵类法术
"ShadowBall", "Darkness", "Curse", "Hex", "NecroticBolt", "ShadowForm",
"RaiseDead", "DrainSoul", "VampiricTouch", "DarkPact", "ShadowStep", "UnholyFrenzy",
"SoulReaper", "Plague", "DarknessEmbrace",
"ShadowBoltVolley", "UnholyAura", "NecroticPlague", "VampiricEmbrace", "DarknessWave",
"SoulDrain", "RaiseSkeleton", "SummonZombie", "Boneyard", "CarrionSwarm",
"UnholyBolt", "ShadowShield", "DemonSummon", "FelFire", "SoulFire",
"DarkCommand", "MindRot", "CorpseExplosion", "UnholyStrength", "ShadowCloak",
"NecromanticAura", "LichForm", "VampireLord", "DarkRitual", "SoulPrison",

# Arcane/魔法类法术
"MagicMissile", "ArcaneExplosion", "Teleport", "Invisibility", "ManaShield",
"Polymorph", "Counterspell", "ArcaneBarrage", "MagicWeapon", "SpellPower",
"ArcaneIntellect", "ManaBurn", "SummonFamiliar", "ConjureFood", "ArcanePrison",
"ArcaneBolt", "MagicShield", "Telekinesis", "ManaLeak", "SpellSteal",
"ArcaneMissiles", "MagicBarrier", "TeleportationCircle", "InvisibleSphere", "ManaRegen",
"ArcaneVortex", "MagicNegation", "CounterMagic", "ArcanePower", "SpellReflection",
"ConjureWater", "SummonElemental", "MagicArmor", "ArcaneGuardian", "ManaBomb",
"ArcaneExplosion", "TelepathicLink", "MagicDetection", "ArcaneEye", "SpellBreach",

# 精神/心灵类法术
"MindControl", "Telepathy", "Fear", "Charm", "Sleep", "Confusion",
"CalmEmotions", "MindBlast", "PsychicScream", "Telekinesis", "Clairvoyance",
"Premonition", "MentalShield", "ThoughtShield", "PsychicLink",
"MindReading", "EmotionControl", "Hallucination", "PhobiaInducement", "CalmMind",
"MentalBreak", "PsychicBarrier", "TelepathicBond", "MindWipe", "MemoryExtract",
"ThoughtProjection", "MentalSuggestion", "Empathy", "MindHeal", "PsychicAssault",
"EmotionSiphon", "FearAura", "CalmAura", "MindShackle", "TelepathicCommand",
"MentalStrength", "PsychicShield", "MemoryAlter", "ThoughtSteal", "MindMeld"
]