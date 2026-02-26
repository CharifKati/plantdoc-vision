import os
import shutil

PLANTVILLAGE_PATH = "plantvillage_dataset/color"
PLANTDOC_PATH     = "PlantDoc-Dataset/train"
OUTPUT_PATH       = "merged_dataset"
PLANT_ADVICE_PATH = "plant_advice.py"

CLASS_MAP = {
    "Apple Scab Leaf":                          "Apple___Apple_scab",
    "Apple leaf":                               "Apple___healthy",
    "Apple rust leaf":                          "Apple___Cedar_apple_rust",
    "Bell_pepper leaf":                         "Pepper,_bell___healthy",
    "Bell_pepper leaf spot":                    "Pepper,_bell___Bacterial_spot",
    "Blueberry leaf":                           "Blueberry___healthy",
    "Cherry leaf":                              "Cherry_(including_sour)___healthy",
    "Corn Gray leaf spot":                      "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn leaf blight":                         "Corn_(maize)___Northern_Leaf_Blight",
    "Corn rust leaf":                           "Corn_(maize)___Common_rust_",
    "Peach leaf":                               "Peach___healthy",
    "Potato leaf early blight":                 "Potato___Early_blight",
    "Potato leaf late blight":                  "Potato___Late_blight",
    "Raspberry leaf":                           "Raspberry___healthy",
    "Soyabean leaf":                            "Soybean___healthy",
    "Squash Powdery mildew leaf":               "Squash___Powdery_mildew",
    "Strawberry leaf":                          "Strawberry___healthy",
    "Tomato Early blight leaf":                 "Tomato___Early_blight",
    "Tomato Septoria leaf spot":                "Tomato___Septoria_leaf_spot",
    "Tomato leaf":                              "Tomato___healthy",
    "Tomato leaf bacterial spot":               "Tomato___Bacterial_spot",
    "Tomato leaf late blight":                  "Tomato___Late_blight",
    "Tomato leaf mosaic virus":                 "Tomato___Tomato_mosaic_virus",
    "Tomato leaf yellow virus":                 "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato mold leaf":                         "Tomato___Leaf_Mold",
    "Tomato two spotted spider mites leaf":     "Tomato___Spider_mites Two-spotted_spider_mite",
    "grape leaf":                               "Grape___healthy",
    "grape leaf black rot":                     "Grape___Black_rot",
}

# ── New advice entries for classes that exist in PlantVillage but were
#    missing from plant_advice.py. Same structure as existing entries.
NEW_ADVICE_ENTRIES = {
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
}


def get_existing_advice_keys():
    """Read plant_advice.py and extract all keys already in PLANT_ADVICE dict."""
    keys = set()
    try:
        with open(PLANT_ADVICE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith('"') and stripped.endswith('": {'):
                    key = stripped[1:stripped.index('"', 1)]
                    keys.add(key)
    except FileNotFoundError:
        print(f"Warning: {PLANT_ADVICE_PATH} not found — skipping advice update.")
    return keys


def format_advice_entry(key, entry):
    """Format a single advice entry as a Python dict block matching the existing style."""
    lines = []
    lines.append(f'    "{key}": {{')
    lines.append(f'        "display_name": "{entry["display_name"]}",')
    lines.append(f'        "status": "{entry["status"]}",')
    lines.append(f'        "severity": "{entry["severity"]}",')
    lines.append(f'        "description": "{entry["description"]}",')
    lines.append(f'        "symptoms": [')
    for s in entry["symptoms"]:
        lines.append(f'            "{s}",')
    lines.append(f'        ],')
    lines.append(f'        "actions": [')
    for a in entry["actions"]:
        lines.append(f'            "{a}",')
    lines.append(f'        ],')
    lines.append(f'        "consult_expert": {entry["consult_expert"]},')
    lines.append(f'    }},')
    return "\n".join(lines)


def update_plant_advice(new_keys_needed):
    """Append missing entries to plant_advice.py before the closing helper functions."""
    missing = {k: v for k, v in NEW_ADVICE_ENTRIES.items() if k in new_keys_needed}
    if not missing:
        print("plant_advice.py is already up to date — no new entries needed.")
        return

    try:
        with open(PLANT_ADVICE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Insert new entries just before the closing helper functions comment
        insert_marker = "# ──────────────────────────────────────────────\n# Helper functions"
        if insert_marker not in content:
            print("Warning: Could not find insertion marker in plant_advice.py — entries printed below instead.")
            for key, entry in missing.items():
                print(f"\n{format_advice_entry(key, entry)}")
            return

        new_blocks = "\n\n".join(format_advice_entry(k, v) for k, v in missing.items())
        section_header = "    # ──────────────────────────────────────────────\n    # NEW ENTRIES (added by merge_datasets.py)\n    # ──────────────────────────────────────────────\n"
        insertion = f"\n{section_header}{new_blocks}\n\n"

        updated_content = content.replace(insert_marker, insertion + insert_marker)

        with open(PLANT_ADVICE_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"\nplant_advice.py updated — added {len(missing)} new entries:")
        for key in missing:
            print(f"  ✓ {key}")

    except Exception as e:
        print(f"Error updating plant_advice.py: {e}")


# ── Step 1: Identify which PlantVillage classes will be in the merged dataset ──
all_target_classes = set(os.listdir(PLANTVILLAGE_PATH)) | set(CLASS_MAP.values())

# ── Step 2: Find which of those are missing from plant_advice.py ──────────────
existing_keys = get_existing_advice_keys()
missing_advice_keys = all_target_classes - existing_keys
keys_we_can_fill = missing_advice_keys & set(NEW_ADVICE_ENTRIES.keys())
keys_with_no_advice = missing_advice_keys - set(NEW_ADVICE_ENTRIES.keys())

# ── Step 3: Copy PlantVillage → output ────────────────────────────────────────
print("Copying PlantVillage dataset...")
for class_folder in os.listdir(PLANTVILLAGE_PATH):
    src = os.path.join(PLANTVILLAGE_PATH, class_folder)
    dst = os.path.join(OUTPUT_PATH, class_folder)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
print(f"  ✓ PlantVillage copied ({len(os.listdir(PLANTVILLAGE_PATH))} classes)")

# ── Step 4: Merge PlantDoc → output ───────────────────────────────────────────
print("\nMerging PlantDoc dataset...")
skipped = []
merged_count = 0
for plantdoc_class, plantvillage_class in CLASS_MAP.items():
    src_dir = os.path.join(PLANTDOC_PATH, plantdoc_class)
    dst_dir = os.path.join(OUTPUT_PATH, plantvillage_class)
    if not os.path.exists(src_dir):
        skipped.append(plantdoc_class)
        continue
    os.makedirs(dst_dir, exist_ok=True)
    count = 0
    for img in os.listdir(src_dir):
        src_img = os.path.join(src_dir, img)
        dst_img = os.path.join(dst_dir, f"plantdoc_{img}")
        shutil.copy2(src_img, dst_img)
        count += 1
    merged_count += count
    print(f"  ✓ {plantdoc_class} → {plantvillage_class} ({count} images)")

if skipped:
    print(f"\n  Skipped (not found): {skipped}")

print(f"\n  Total PlantDoc images merged: {merged_count}")

# ── Step 5: Update plant_advice.py ────────────────────────────────────────────
print("\nChecking plant_advice.py for missing entries...")
if keys_with_no_advice:
    print(f"  Note: These classes have no advice entry and none was written (manual update needed):")
    for k in sorted(keys_with_no_advice):
        print(f"    - {k}")

update_plant_advice(keys_we_can_fill)

# ── Step 6: Update finetune.py path reminder ───────────────────────────────────
print("\n" + "="*60)
print("DONE!")
print(f"Merged dataset: {OUTPUT_PATH}")
print(f"\nNext step — update finetune.py:")
print(f'  DATASET_PATH = "{OUTPUT_PATH}"')
print("Then run: python finetune.py")
print("="*60)