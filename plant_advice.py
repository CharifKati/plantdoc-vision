"""
PlantDoc Vision — Disease Advice Library
Keyed exactly by PlantVillage folder/class names.
Each entry contains:
  - display_name: human-readable label
  - status: "healthy" | "disease" | "deficiency"
  - severity: "none" | "low" | "medium" | "high"
  - description: short plain-english explanation of the condition
  - symptoms: what to look for on the leaf
  - actions: list of concrete recommended actions (ordered by priority)
  - consult_expert: bool — whether to strongly recommend a professional
"""

PLANT_ADVICE = {

    # ──────────────────────────────────────────────
    # APPLE
    # ──────────────────────────────────────────────
    "Apple___Apple_scab": {
        "display_name": "Apple — Apple Scab",
        "status": "disease",
        "severity": "high",
        "description": "A fungal disease caused by Venturia inaequalis. One of the most damaging apple diseases worldwide, especially in wet, cool springs.",
        "symptoms": [
            "Olive-green to brown velvety spots on leaves",
            "Leaves may yellow and drop early",
            "Scabby, cracked lesions on fruit",
        ],
        "actions": [
            "Remove and destroy all fallen leaves and infected fruit — do not compost",
            "Apply fungicide (captan, myclobutanil, or copper-based) at bud break and repeat every 7-10 days during wet periods",
            "Prune to improve airflow through the canopy",
            "Avoid overhead irrigation — water at the base",
        ],
        "consult_expert": False,
    },

    "Apple___Black_rot": {
        "display_name": "Apple — Black Rot",
        "status": "disease",
        "severity": "high",
        "description": "Caused by the fungus Botryosphaeria obtusa. Affects fruit, leaves, and bark. Common in warm, humid conditions.",
        "symptoms": [
            "Purple spots on leaves that enlarge and turn brown with a purple border ('frog-eye' leaf spot)",
            "Rotting fruit that turns black and shrivels (mummification)",
            "Cankers on branches with reddish-brown bark",
        ],
        "actions": [
            "Prune out all dead or cankered wood at least 15 cm below visible infection",
            "Remove and destroy mummified fruit from the tree and ground",
            "Apply fungicide (captan or thiophanate-methyl) from pink bud through summer",
            "Disinfect pruning tools with 70% alcohol between cuts",
        ],
        "consult_expert": False,
    },

    "Apple___Cedar_apple_rust": {
        "display_name": "Apple — Cedar Apple Rust",
        "status": "disease",
        "severity": "medium",
        "description": "A fungal disease (Gymnosporangium juniperi-virginianae) that requires two hosts to complete its life cycle: apple/crabapple and Eastern red cedar or juniper.",
        "symptoms": [
            "Bright orange-yellow spots on the upper leaf surface",
            "Tube-like structures (aecia) on the underside of leaves",
            "Distorted or dropping leaves in heavy infections",
        ],
        "actions": [
            "Apply fungicide (myclobutanil or propiconazole) starting at pink bud stage, repeat every 7-10 days through petal fall",
            "Remove nearby Eastern red cedar or juniper trees if feasible",
            "Remove orange galls from cedars in late winter before spores release",
        ],
        "consult_expert": False,
    },

    "Apple___healthy": {
        "display_name": "Apple — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "The leaf appears healthy with no signs of disease or deficiency.",
        "symptoms": [],
        "actions": [
            "Continue current care routine",
            "Monitor weekly during the growing season for early signs of scab or rust",
            "Maintain a regular pruning schedule to ensure good airflow",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # BLUEBERRY
    # ──────────────────────────────────────────────
    "Blueberry___healthy": {
        "display_name": "Blueberry — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Maintain soil pH between 4.5 and 5.5 — critical for blueberries",
            "Monitor for mummy berry and stem canker in spring",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # CHERRY
    # ──────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "display_name": "Cherry — Powdery Mildew",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Podosphaera clandestina. Thrives in warm days, cool nights, and humid conditions without direct rainfall on leaves.",
        "symptoms": [
            "White powdery coating on young leaves and shoots",
            "Leaves may curl, distort, or turn yellow",
            "Reduced fruit size and quality in heavy infections",
        ],
        "actions": [
            "Apply sulfur-based or potassium bicarbonate fungicide at first sign of infection",
            "Remove and destroy heavily infected shoots",
            "Improve airflow through pruning",
            "Avoid excess nitrogen fertilizer — soft growth is more vulnerable",
        ],
        "consult_expert": False,
    },

    "Cherry_(including_sour)___healthy": {
        "display_name": "Cherry — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor for brown rot during fruit development",
            "Check for shot hole fungus symptoms after wet periods",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # CORN (MAIZE)
    # ──────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "display_name": "Corn — Gray Leaf Spot (Cercospora)",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Cercospora zeae-maydis. One of the most yield-limiting corn diseases in humid regions. Favored by warm temperatures and extended periods of leaf wetness.",
        "symptoms": [
            "Rectangular, tan to gray lesions bounded by leaf veins",
            "Lesions run parallel to leaf veins giving a 'window pane' appearance",
            "Severe infection causes leaves to die back from the tip",
        ],
        "actions": [
            "Apply foliar fungicide (strobilurin or triazole class) at tasseling if disease is present on the ear leaf or above",
            "Rotate crops — avoid continuous corn planting",
            "Till under corn debris to reduce inoculum for next season",
        ],
        "consult_expert": True,
    },

    "Corn_(maize)___Common_rust_": {
        "display_name": "Corn — Common Rust",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Puccinia sorghi. Spreads via airborne spores. Severity depends heavily on hybrid susceptibility and timing of infection.",
        "symptoms": [
            "Oval to elongated brick-red pustules scattered on both leaf surfaces",
            "Pustules may turn dark brown/black as the season progresses",
            "Heavy infection causes premature leaf death",
        ],
        "actions": [
            "Apply fungicide (triazole or strobilurin) if rust appears before tasseling on susceptible hybrids",
            "Monitor fields twice weekly during cool, humid periods",
            "Prioritize treatment on seed corn fields",
        ],
        "consult_expert": False,
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "display_name": "Corn — Northern Leaf Blight",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Exserohilum turcicum. Can cause significant yield losses when it infects early and affects the ear leaf and above.",
        "symptoms": [
            "Long, cigar-shaped gray-green to tan lesions (2.5-15 cm)",
            "Lesions may have a 'dirty' appearance with dark spores in humid conditions",
            "Lesions can coalesce to kill large areas of leaf tissue",
        ],
        "actions": [
            "Apply fungicide (propiconazole, azoxystrobin) at tasseling if upper canopy leaves are affected",
            "Scout fields at VT (tasseling) stage to make treatment decisions",
            "Rotate away from corn for at least one season",
            "Incorporate or till infected residue after harvest",
        ],
        "consult_expert": True,
    },

    "Corn_(maize)___healthy": {
        "display_name": "Corn — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Scout for early rust or blight symptoms weekly from V6 through tasseling",
            "Check soil nitrogen levels if leaves show yellowing",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # GRAPE
    # ──────────────────────────────────────────────
    "Grape___Black_rot": {
        "display_name": "Grape — Black Rot",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Guignardia bidwellii. Can destroy an entire crop in a wet year. Mummified berries are the primary overwintering source.",
        "symptoms": [
            "Circular tan lesions with a dark brown border on leaves",
            "Small black dots (pycnidia) visible in the tan lesion center",
            "Berries turn brown, shrivel, and become hard black mummies",
        ],
        "actions": [
            "Remove and destroy all mummified berries on and under the vine immediately",
            "Apply fungicide (myclobutanil, captan, or mancozeb) starting at bud break, every 10-14 days through fruit set",
            "Prune to open the canopy — wet, shaded conditions favor infection",
            "Train shoots upward to keep fruit zone airy and dry",
        ],
        "consult_expert": False,
    },

    "Grape___Esca_(Black_Measles)": {
        "display_name": "Grape — Esca (Black Measles)",
        "status": "disease",
        "severity": "high",
        "description": "A complex wood disease with no cure. Management focuses on slowing progression. Caused by several fungi including Phaeomoniella chlamydospora.",
        "symptoms": [
            "Tiger-stripe pattern of yellowing/reddening between leaf veins",
            "Small, dark spots on berries (the 'measles' symptom)",
            "Sudden vine collapse ('apoplexy') in hot weather",
            "Internal wood shows brown streaking when cut",
        ],
        "actions": [
            "Remove and burn severely affected vines — do not compost",
            "Prune out infected wood back to healthy tissue during dry weather",
            "Seal all large pruning wounds with wound protectant immediately",
            "Avoid pruning during wet conditions when spores are released",
        ],
        "consult_expert": True,
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "display_name": "Grape — Leaf Blight (Isariopsis Leaf Spot)",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Isariopsis clavispora. More common in tropical and subtropical regions. Primarily affects leaves and reduces photosynthetic capacity.",
        "symptoms": [
            "Irregular dark brown spots on the upper leaf surface",
            "Grayish fungal growth on the underside of spots",
            "Severe defoliation in advanced cases",
        ],
        "actions": [
            "Apply copper-based or mancozeb fungicide at first sign of infection",
            "Remove heavily infected leaves and dispose of away from the vineyard",
            "Improve canopy airflow through leaf removal in the fruit zone",
        ],
        "consult_expert": False,
    },

    "Grape___healthy": {
        "display_name": "Grape — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor weekly for powdery mildew and downy mildew during shoot growth",
            "Check fruit zone leaves for early black rot lesions after rain events",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # ORANGE
    # ──────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "display_name": "Orange — Huanglongbing (Citrus Greening)",
        "status": "disease",
        "severity": "high",
        "description": "Caused by the bacterium Candidatus Liberibacter asiaticus, spread by the Asian citrus psyllid. There is currently NO cure — HLB is fatal to citrus trees.",
        "symptoms": [
            "Asymmetric (blotchy) yellowing of leaves — unlike the symmetric pattern of nutrient deficiencies",
            "Fruit remains green at the bottom even when ripe, and is small and misshapen",
            "Fruit is bitter and unusable",
            "General tree decline over years",
        ],
        "actions": [
            "Report suspected HLB to your local agricultural authority immediately — it is a notifiable disease in many regions",
            "Control the Asian citrus psyllid vector aggressively with insecticides (imidacloprid, spirotetramat)",
            "Remove and destroy infected trees to prevent spread to healthy trees",
            "Do NOT move plant material from infected areas",
        ],
        "consult_expert": True,
    },

    # ──────────────────────────────────────────────
    # PEACH
    # ──────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "display_name": "Peach — Bacterial Spot",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Xanthomonas arboricola pv. pruni. Spread by rain splash and wind during wet conditions. Affects leaves, fruit, and twigs.",
        "symptoms": [
            "Small, water-soaked spots on leaves that turn brown with a yellow halo",
            "Spots may fall out leaving a 'shot hole' appearance",
            "Shallow, dark, sunken spots on fruit surface",
            "Fruit cracking around lesion sites",
        ],
        "actions": [
            "Apply copper-based bactericide starting at shuck split, repeat every 5-7 days during wet weather",
            "Prune to improve airflow and reduce leaf wetness duration",
            "Avoid working in the orchard when foliage is wet",
            "Remove heavily infected twigs during dormant pruning",
        ],
        "consult_expert": False,
    },

    "Peach___healthy": {
        "display_name": "Peach — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor for peach leaf curl in spring — apply copper before bud swell",
            "Check for brown rot as fruit approaches maturity",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # PEPPER
    # ──────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "display_name": "Bell Pepper — Bacterial Spot",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Xanthomonas euvesicatoria. Thrives in warm (24-30 C), wet, windy conditions. Spreads rapidly through rain splash and contact.",
        "symptoms": [
            "Small, water-soaked lesions on leaves that turn brown with yellow halos",
            "Lesions on fruit appear as raised, scabby spots",
            "Severe defoliation exposes fruit to sunscald",
        ],
        "actions": [
            "Apply copper bactericide + mancozeb combination every 5-7 days during warm, wet weather",
            "Start applications at transplant — prevention is far more effective than cure",
            "Remove infected plant debris from the field immediately",
            "Switch to drip irrigation and water early in the day",
        ],
        "consult_expert": False,
    },

    "Pepper,_bell___healthy": {
        "display_name": "Bell Pepper — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor for aphids and thrips which can vector viruses",
            "Watch for signs of phytophthora crown rot in wet areas of the field",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # POTATO
    # ──────────────────────────────────────────────
    "Potato___Early_blight": {
        "display_name": "Potato — Early Blight",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Alternaria solani. Primarily a stress-related disease — plants under nutrient stress, drought, or pest pressure are most vulnerable.",
        "symptoms": [
            "Dark brown lesions with concentric rings forming a 'target board' or 'bulls-eye' pattern",
            "Lesions surrounded by yellow tissue",
            "Starts on older, lower leaves and progresses upward",
        ],
        "actions": [
            "Apply fungicide (chlorothalonil, mancozeb, or azoxystrobin) at first sign — repeat every 7-10 days",
            "Ensure adequate nitrogen fertility — deficient plants are far more susceptible",
            "Remove and dispose of infected leaves",
            "Avoid overhead irrigation in the evening",
        ],
        "consult_expert": False,
    },

    "Potato___Late_blight": {
        "display_name": "Potato — Late Blight",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Phytophthora infestans — the pathogen behind the Irish Potato Famine. An oomycete, not a true fungus. Spreads explosively under cool, wet conditions and can destroy a field in days.",
        "symptoms": [
            "Water-soaked, pale green lesions that rapidly turn dark brown/black",
            "White fluffy sporulation visible on the underside of lesions in humid conditions",
            "Distinctive foul odor from infected tissue",
            "Entire plant collapse in severe cases",
        ],
        "actions": [
            "Apply fungicide immediately — use oomycete-specific products (metalaxyl, cymoxanil, or mandipropamid). Standard fungicides are NOT effective.",
            "Remove and bag (do not compost) all infected plant material",
            "Hill soil up around stems to protect tubers from spore wash-down",
            "Do not harvest for at least 2 weeks after foliage dies to allow skin set and reduce tuber infection",
        ],
        "consult_expert": True,
    },

    "Potato___healthy": {
        "display_name": "Potato — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor weekly for early or late blight symptoms, especially after rain",
            "Watch for Colorado potato beetle damage which stresses plants",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # RASPBERRY
    # ──────────────────────────────────────────────
    "Raspberry___healthy": {
        "display_name": "Raspberry — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Remove and destroy old floricanes (2-year-old canes) after fruiting",
            "Monitor for orange rust or spur blight in wet seasons",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # SOYBEAN
    # ──────────────────────────────────────────────
    "Soybean___healthy": {
        "display_name": "Soybean — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Scout for Asian soybean rust if in a high-risk region",
            "Monitor for sudden death syndrome symptoms at R3-R5 (pod fill) stages",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # SQUASH
    # ──────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "display_name": "Squash — Powdery Mildew",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Podosphaera xanthii. Unlike most fungal diseases, powdery mildew does NOT need wet leaves — it thrives in warm, dry days with high humidity at night.",
        "symptoms": [
            "White powdery patches on upper and lower leaf surfaces",
            "Infected leaves yellow and die prematurely",
            "Reduced fruit size and sweetness due to loss of leaf area",
        ],
        "actions": [
            "Apply potassium bicarbonate, sulfur, or neem oil at first sign — these work best as early interventions",
            "For advanced infections use systemic fungicide (myclobutanil or trifloxystrobin)",
            "Remove heavily infected leaves to reduce spore load",
            "Avoid excess nitrogen — lush growth is more susceptible",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # STRAWBERRY
    # ──────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "display_name": "Strawberry — Leaf Scorch",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Diplocarpon earlianum. One of the most common strawberry leaf diseases. Rarely kills plants outright but weakens them and reduces yield over time.",
        "symptoms": [
            "Small, irregular dark purple spots on the upper leaf surface",
            "Spots enlarge and centers turn reddish-brown to gray",
            "Entire leaf may turn reddish-purple and wither — resembling drought scorch",
        ],
        "actions": [
            "Remove old and infected leaves — especially after renovation mowing",
            "Apply fungicide (captan or myclobutanil) from early spring through harvest",
            "Ensure good drainage — saturated soils worsen the disease",
            "Renovate matted rows promptly after harvest (mow, thin, fertilize)",
        ],
        "consult_expert": False,
    },

    "Strawberry___healthy": {
        "display_name": "Strawberry — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor for gray mold (Botrytis) as fruit develops — most critical at flowering",
            "Check for two-spotted spider mites during hot, dry periods",
        ],
        "consult_expert": False,
    },

    # ──────────────────────────────────────────────
    # TOMATO
    # ──────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "display_name": "Tomato — Bacterial Spot",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Xanthomonas species. Spreads rapidly through rain, wind, and contact. Thrives in warm (24-30 C), wet conditions.",
        "symptoms": [
            "Small, dark brown, water-soaked spots on leaves with yellow halos",
            "Spots may merge causing large necrotic areas and defoliation",
            "Raised, scabby dark spots on fruit — especially under the shoulders",
        ],
        "actions": [
            "Apply copper bactericide + mancozeb every 5-7 days during wet weather",
            "Start applications at transplant — prevention is far more effective than cure",
            "Remove infected plant debris from the field immediately",
            "Switch to drip irrigation and water early in the day",
        ],
        "consult_expert": False,
    },

    "Tomato___Early_blight": {
        "display_name": "Tomato — Early Blight",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Alternaria solani. A very common tomato disease that typically appears mid-season on stressed or aging plants.",
        "symptoms": [
            "Dark brown concentric ring lesions ('target board' pattern) on older lower leaves",
            "Yellow tissue surrounding lesions",
            "Premature yellowing and dropping of lower leaves",
            "Stem lesions (collar rot) in seedlings",
        ],
        "actions": [
            "Apply fungicide (chlorothalonil, mancozeb, or azoxystrobin) every 7-10 days starting at first symptom",
            "Remove and dispose of infected lower leaves to slow spread",
            "Stake or cage plants to keep foliage off the soil",
            "Mulch under plants to prevent soil-splash spread",
        ],
        "consult_expert": False,
    },

    "Tomato___Late_blight": {
        "display_name": "Tomato — Late Blight",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Phytophthora infestans — same pathogen as potato late blight. Spreads explosively in cool (10-20 C), wet conditions. Can destroy a planting within days.",
        "symptoms": [
            "Large, water-soaked, pale green to brown lesions on leaves",
            "White fluffy sporulation on the underside of lesions in humid conditions",
            "Dark brown lesions on stems and petioles",
            "Fruit develops large, firm, greasy brown rot",
        ],
        "actions": [
            "Apply oomycete-specific fungicide immediately (metalaxyl, cymoxanil, or mandipropamid) — standard fungicides are NOT effective",
            "Remove and bag all infected plant material — do not compost",
            "Avoid overhead watering — switch to drip and water in the morning",
            "Destroy all crop debris at end of season",
        ],
        "consult_expert": True,
    },

    "Tomato___Leaf_Mold": {
        "display_name": "Tomato — Leaf Mold",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Passalora fulva. Primarily a greenhouse and high-tunnel disease, thriving in high humidity (above 85%) and moderate temperatures.",
        "symptoms": [
            "Pale green to yellow spots on the upper leaf surface",
            "Olive-green to brown velvety fungal growth on the underside of spots",
            "Leaves curl upward and wither in severe cases",
        ],
        "actions": [
            "Reduce humidity — improve ventilation, increase plant spacing, avoid overhead irrigation",
            "Apply fungicide (chlorothalonil or copper-based) at first sign",
            "Remove and destroy infected leaves",
            "Use resistant varieties in high-humidity environments",
        ],
        "consult_expert": False,
    },

    "Tomato___Septoria_leaf_spot": {
        "display_name": "Tomato — Septoria Leaf Spot",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Septoria lycopersici. One of the most destructive tomato foliage diseases. Spreads rapidly during warm, wet weather via rain splash.",
        "symptoms": [
            "Small circular spots with dark brown borders and light gray or tan centers",
            "Tiny black dots (pycnidia) visible in the center of spots",
            "Starts on lower leaves and progresses upward",
            "Severe defoliation reduces fruit size and causes sunscald",
        ],
        "actions": [
            "Apply fungicide (chlorothalonil, mancozeb, or copper-based) every 7-10 days from first symptom",
            "Remove and dispose of infected lower leaves immediately — do not compost",
            "Mulch under plants to prevent soil-splash onto leaves",
            "Stake or cage plants to improve airflow and keep foliage off the ground",
            "Rotate tomatoes to a new bed — the pathogen overwinters in soil and debris",
        ],
        "consult_expert": False,
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "display_name": "Tomato — Spider Mites (Two-Spotted)",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Tetranychus urticae. Not a fungal disease — this is a pest infestation. Thrives in hot, dry conditions. Populations can explode rapidly.",
        "symptoms": [
            "Fine yellow stippling on the upper leaf surface",
            "Fine webbing on the underside of leaves and between leaflets",
            "Leaves turn bronze, dry out, and drop in severe cases",
            "Tiny moving dots (mites) visible with a hand lens on leaf undersides",
        ],
        "actions": [
            "Apply miticide (abamectin, bifenazate, or spiromesifen) — rotate between chemical classes to prevent resistance",
            "Spray the undersides of leaves thoroughly where mites live and lay eggs",
            "Increase humidity and irrigation — mites hate wet conditions",
            "Introduce predatory mites (Phytoseiulus persimilis) as a biological control in greenhouse settings",
            "Avoid broad-spectrum insecticides that kill natural predators",
        ],
        "consult_expert": False,
    },

    "Tomato___Target_Spot": {
        "display_name": "Tomato — Target Spot",
        "status": "disease",
        "severity": "medium",
        "description": "Caused by Corynespora cassiicola. Common in warm, humid conditions. Affects leaves, stems, and fruit.",
        "symptoms": [
            "Brown circular lesions with concentric rings forming a target pattern",
            "Yellow halo surrounding lesions",
            "Starts on older lower leaves and progresses upward",
            "Small, dark, sunken spots on fruit",
        ],
        "actions": [
            "Apply fungicide (chlorothalonil or azoxystrobin) every 7-10 days from first symptom",
            "Remove and destroy infected leaves — do not compost",
            "Stake plants and mulch soil to reduce splash spread",
            "Improve airflow through pruning and correct plant spacing",
            "Rotate tomatoes to a different bed next season",
        ],
        "consult_expert": False,
    },

    "Tomato___Tomato_mosaic_virus": {
        "display_name": "Tomato — Tomato Mosaic Virus",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Tomato mosaic virus (ToMV). Highly stable and spreads easily through contact, tools, and infected seed. No cure once a plant is infected.",
        "symptoms": [
            "Mosaic pattern of light and dark green areas on leaves",
            "Leaves may be distorted, curled, or reduced in size",
            "Stunted plant growth",
            "Fruit may show internal browning",
        ],
        "actions": [
            "Remove and destroy infected plants immediately — do not compost",
            "Disinfect all tools with 10% bleach or 70% alcohol between plants",
            "Wash hands thoroughly before handling plants",
            "Use certified virus-free seed and resistant varieties for next season",
            "Control aphids and other insects that can spread the virus",
        ],
        "consult_expert": True,
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "display_name": "Tomato — Yellow Leaf Curl Virus",
        "status": "disease",
        "severity": "high",
        "description": "Caused by Tomato yellow leaf curl virus (TYLCV), transmitted exclusively by the silverleaf whitefly (Bemisia tabaci). No cure — management focuses on vector control.",
        "symptoms": [
            "Upward curling and yellowing of leaf margins",
            "Leaves are small and cupped with a leathery texture",
            "Severe stunting of the whole plant",
            "Flowers drop without setting fruit in heavy infections",
        ],
        "actions": [
            "Control whitefly populations aggressively with insecticide (imidacloprid, spiromesifen) or reflective mulch to repel whiteflies",
            "Remove and destroy infected plants immediately to reduce virus reservoir",
            "Use yellow sticky traps to monitor whitefly populations",
            "Plant resistant varieties (TYLCV-resistant cultivars) in subsequent seasons",
            "Use insect-proof netting in greenhouse or nursery settings",
        ],
        "consult_expert": True,
    },

    "Tomato___healthy": {
        "display_name": "Tomato — Healthy",
        "status": "healthy",
        "severity": "none",
        "description": "No disease or deficiency detected.",
        "symptoms": [],
        "actions": [
            "Monitor weekly for early and late blight, especially after rain",
            "Check undersides of leaves for spider mites during hot, dry periods",
            "Ensure consistent watering to prevent blossom end rot",
        ],
        "consult_expert": False,
    },

}


# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────

def get_advice(class_name: str) -> dict:
    """
    Look up advice by exact PlantVillage class name.
    Returns a dict with all advice fields, or a generic fallback entry.

    Usage:
        advice = get_advice("Tomato___Early_blight")
        print(advice["display_name"])
        for action in advice["actions"]:
            print("-", action)
    """
    return PLANT_ADVICE.get(class_name, {
        "display_name": class_name.replace("___", " -- ").replace("_", " "),
        "status": "unknown",
        "severity": "unknown",
        "description": "No specific advice available for this class yet.",
        "symptoms": [],
        "actions": ["Consult a local agricultural extension officer or plant pathologist."],
        "consult_expert": True,
    })


def get_top3_advice(predictions: list) -> list:
    """
    Given a list of (class_name, confidence_score) tuples sorted by confidence descending,
    return the top-3 advice dicts with the confidence score attached.

    Usage:
        predictions = [
            ("Tomato___Early_blight", 0.87),
            ("Tomato___Late_blight", 0.09),
            ("Tomato___healthy", 0.04),
        ]
        results = get_top3_advice(predictions)
        for r in results:
            print(r["display_name"], r["confidence"])
    """
    results = []
    for class_name, score in predictions[:3]:
        entry = get_advice(class_name).copy()
        entry["confidence"] = round(score * 100, 1)
        results.append(entry)
    return results


# ──────────────────────────────────────────────
# Quick sanity check
# ──────────────────────────────────────────────
if __name__ == "__main__":
    test_predictions = [
        ("Tomato___Early_blight", 0.87),
        ("Potato___Late_blight", 0.09),
        ("Apple___healthy", 0.04),
    ]

    print("=== get_top3_advice() demo ===\n")
    for entry in get_top3_advice(test_predictions):
        print(f"[{entry['confidence']}%] {entry['display_name']} | {entry['status'].upper()} | severity: {entry['severity']}")
        print(f"  Expert required: {entry['consult_expert']}")
        print(f"  First action: {entry['actions'][0]}\n")

    print("=== All registered classes ===")
    for key in PLANT_ADVICE:
        a = PLANT_ADVICE[key]
        print(f"  {key:<55} [{a['status']}]")