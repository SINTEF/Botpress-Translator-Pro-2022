import json
import tarfile
import tempfile
import os
from load_translations_from_excel import load_translations_from_excel

def pack(bot_path, excel_path, new_path):
    translations = load_translations_from_excel(excel_path)

    def get_translation(path, expected_existing_english):
        if not path in translations:
            raise Exception("No translation found for " + str(path)) 
        (english, translation) = translations[path]
        if expected_existing_english and english != expected_existing_english:
            raise Exception("Expected " + str(expected_existing_english) + " but found " + str(english))
        
        return translation

    print("Patching the bot " + bot_path)
    # Extract the bot to a temporary directory
    with tempfile.TemporaryDirectory() as temporary_directory:
        # Extract the .tgz file in python
        with tarfile.open(bot_path, "r:gz") as tar:
            tar.extractall(temporary_directory)

        # Open content-elements/builtin_text.json
        with open(
            temporary_directory + "/content-elements/builtin_text.json", "r"
        ) as f:
            # read and parse json
            builtin_texts = json.load(f)
            # builtin_text is an array of objects containing an id and a formData object
            for builtin_text in builtin_texts:
                translation = get_translation(builtin_text["id"], builtin_text["formData"]["text$en"])
                # We keep the $en field because it seems that our version of botpress
                # does not support other languages
                builtin_text["formData"]["text$en"] = translation

            translated_builtin_texts = json.dumps(builtin_texts, indent=2, ensure_ascii=False)

        with open(
            temporary_directory + "/content-elements/builtin_text.json", "w"
        ) as f:
            f.write(translated_builtin_texts)

        # Open content-elements/builtin_card.json
        with open(
            temporary_directory + "/content-elements/builtin_card.json", "r"
        ) as f:
            # read and parse json
            builtin_cards = json.load(f)
            # builtin_card is an array of objects containing an id and a formData object
            for builtin_card in builtin_cards:

                translation = get_translation(builtin_card["id"]+".title", builtin_card["formData"]["title$en"])
                builtin_card["formData"]["title$en"] = translation

                if "subtitle$en" in builtin_card["formData"]:
                    translation = get_translation(builtin_card["id"]+".subtitle", builtin_card["formData"]["subtitle$en"])
                    builtin_card["formData"]["subtitle$en"] = translation

                for index, option in enumerate(builtin_card["formData"]["actions$en"]):
                    translation = get_translation(builtin_card["id"] + ".actionTitle[" + str(index) + "]", option["title"])
                    builtin_card["formData"]["actions$en"][index]["title"] = translation
                    if "text" in option:
                        translation = get_translation(builtin_card["id"] + ".actionText[" + str(index) + "]", option["text"])
                        builtin_card["formData"]["actions$en"][index]["text"] = translation

            translated_builtin_cards = json.dumps(builtin_cards, indent=2, ensure_ascii=False)
        
        with open(
            temporary_directory + "/content-elements/builtin_card.json", "w"
        ) as f:
            f.write(translated_builtin_cards)

        # Open content-elements/builtin_carousel.json
        with open(
            temporary_directory + "/content-elements/builtin_carousel.json", "r"
        ) as f:
            # read and parse json
            builtin_carousels = json.load(f)
            # builtin_carousel is an array of objects containing an id and a formData object
            for builtin_carousel in builtin_carousels:
                for index, option in enumerate(builtin_carousel["formData"]["items$en"]):
                    translation = get_translation(builtin_carousel["id"] + ".itemTitle[" + str(index) + "]", option["title"])
                    builtin_carousel["formData"]["items$en"][index]["title"] = translation
                    for actionIndex, option in enumerate(option["actions"]):
                        translation = get_translation(builtin_carousel["id"] + ".itemActionTitle[" + str(index) + "][" + str(actionIndex) + "]", option["title"])
                        builtin_carousel["formData"]["items$en"][index]["actions"][actionIndex]["title"] = translation

            translated_builtin_carousels = json.dumps(builtin_carousels, indent=2, ensure_ascii=False)

        with open(
            temporary_directory + "/content-elements/builtin_carousel.json", "w"
        ) as f:
            f.write(translated_builtin_carousels)

        # Open content-elements/builtin_image.json
        with open(
            temporary_directory + "/content-elements/builtin_image.json", "r"
        ) as f:
            # read and parse json
            builtin_images = json.load(f)
            # builtin_image is an array of objects containing an id and a formData object
            for builtin_image in builtin_images:
                if "title$en" in builtin_image["formData"]:
                    translation = get_translation(builtin_image["id"]+".title", builtin_image["formData"]["title$en"])
                    builtin_image["formData"]["title$en"] = translation

            translated_builtin_images = json.dumps(builtin_images, indent=2, ensure_ascii=False)

        with open(
            temporary_directory + "/content-elements/builtin_image.json", "w"
        ) as f:
            f.write(translated_builtin_images)

        # Open content-elements/builtin_single-choice.json
        with open(
            temporary_directory + "/content-elements/builtin_single-choice.json", "r"
        ) as f:
            # read and parse json
            builtin_single_choices = json.load(f)
            # builtin_single_choice is an array of objects containing an id and a formData object
            for builtin_single_choice in builtin_single_choices:
                translation = get_translation(builtin_single_choice["id"]+".dropdown", builtin_single_choice["formData"]["dropdownPlaceholder$en"])
                builtin_single_choice["formData"]["dropdownPlaceholder$en"] = translation

                if "text$en" in builtin_single_choice["formData"]:
                    translation = get_translation(builtin_single_choice["id"]+".text", builtin_single_choice["formData"]["text$en"])
                    builtin_single_choice["formData"]["text$en"] = translation

                for index, option in enumerate(builtin_single_choice["formData"]["choices$en"]):
                    translation = get_translation(builtin_single_choice["id"] + ".choice[" + str(index) + "]", option["title"])
                    builtin_single_choice["formData"]["choices$en"][index]["title"] = translation

            translated_builtin_single_choices = json.dumps(builtin_single_choices, indent=2, ensure_ascii=False)

        with open(
            temporary_directory + "/content-elements/builtin_single-choice.json", "w"
        ) as f:
            f.write(translated_builtin_single_choices)

        # Open content-elements/dropdown.json
        with open(
            temporary_directory + "/content-elements/dropdown.json", "r"
        ) as f:
            # read and parse json
            dropdowns = json.load(f)
            # dropdown is an array of objects containing an id and a formData object
            for dropdown in dropdowns:
                translation = get_translation(dropdown["id"]+".message", dropdown["formData"]["message$en"])
                dropdown["formData"]["message$en"] = translation

                translation = get_translation(dropdown["id"]+".placeholderText", dropdown["formData"]["placeholderText$en"])
                dropdown["formData"]["placeholderText$en"] = translation

                for index, option in enumerate(dropdown["formData"]["options$en"]):
                    translation = get_translation(dropdown["id"] + ".option[" + str(index) + "]", option["label"])
                    dropdown["formData"]["options$en"][index]["label"] = translation

            translated_dropdowns = json.dumps(dropdowns, indent=2, ensure_ascii=False)

        with open(
            temporary_directory + "/content-elements/dropdown.json", "w"
        ) as f:
            f.write(translated_dropdowns)

        # This is disabled as translations are not available in our botpress version
        # # Open bot.config.json
        # with open(
        #     temporary_directory + "/bot.config.json", "r"
        # ) as f:
        #     # read and parse json
        #     bot_config = json.load(f)
        #     bot_config["languages"] = ["no", "en", "fr"]
        #     bot_config["defaultLanguage"] = "no"

        #     translated_bot_config = json.dumps(bot_config, indent=2, ensure_ascii=False)

        # with open(
        #     temporary_directory + "/bot.config.json", "w"
        # ) as f:
        #     f.write(translated_bot_config)

        print("Writing the new bot to " + new_path)
        # Create a .tgz file of the temporary directory
        with tarfile.open(new_path, "w:gz") as tar:
            for name in os.listdir(temporary_directory):
                tar.add(temporary_directory + "/" + name, arcname=name)

