import os
from editor import (
    read_file, write_file, create_file,
    delete_file, delete_content
)
import encryption
from font_api import convert_style


def multiline_input():
    print("Enter text (type ':wq' to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == ":wq":
            break
        lines.append(line)
    return "\n".join(lines)


def open_file():
    filename = input("Enter filename to open: ").strip()
    if not os.path.exists(filename):
        print("File not found.")
        return None, None, False, False

    raw_data = read_file(filename)
    is_new = False

    if encryption.is_encrypted(raw_data):
        print("This file is encrypted.")
        pwd = input("Enter password: ")
        try:
            data = encryption.decrypt_text(raw_data, pwd)
            print("Decryption successful.")
        except ValueError as e:
            print(e)
            return None, None, False, False
    else:
        data = raw_data
        print("File opened successfully.")

    print("\n--- File Content ---")
    print(data if data else "[empty]")
    print("--------------------")

    return filename, data, is_new, False


def ensure_filename(name):
    if not name:
        name = input("Enter filename: ").strip()
    return name


def edit_content(filename, content):
    filename = ensure_filename(filename)
    if content is None:
        content = ""

    plain = content
    styled = content
    changed = False

    while True:
        print(f"\nEditing: {filename}")
        print("1. Replace entire content")
        print("2. Append text")
        print("3. Find & Replace")
        print("4. Show content")
        print("5. Apply Font Style (preview only)")
        print("6. Finish Editing")
        choice = input("Choice: ")

        if choice == "1":
            plain = multiline_input()
            styled = plain
            changed = True

        elif choice == "2":
            add = multiline_input()
            plain += ("\n" if plain else "") + add
            styled = plain
            changed = True

        elif choice == "3":
            find = input("Find: ")
            repl = input("Replace with: ")
            plain = plain.replace(find, repl)
            styled = plain
            changed = True

        elif choice == "4":
            print("\n--- Current Content ---")
            print(styled if styled else "[empty]")
            print("------------------------")

        elif choice == "5":
            print("⚠ WARNING: If you encrypt AFTER applying a font style except lower and uppercase, your original plain text may be lost!")
            print("Styles: calligraphy, italic, bold, uppercase, lowercase")
            style = input("Enter style: ").lower().strip()

            try:
                styled = convert_style(plain, style)
                print(f"Applied {style} style (preview).")
            except ValueError as e:
                print(e)

        elif choice == "6":
            return filename, plain, styled, changed

        else:
            print("Invalid choice.")


def save_file(filename, plain, styled, is_new):
    filename = ensure_filename(filename)

    print("\nChoose save format:")
    print("1. Save plain text")
    print("2. Save styled text")
    print("3. Encrypt plain text")
    print("4. Encrypt styled text")
    choice = input("Enter choice: ")

    if choice == "1":
        content = plain

    elif choice == "2":
        content = styled

    elif choice == "3":
        pwd = input("Enter password: ")
        content = encryption.encrypt_text(plain, pwd)

    elif choice == "4":
        pwd = input("Enter password: ")
        content = encryption.encrypt_text(styled, pwd)

    else:
        print("Invalid choice — saving plain text by default.")
        content = plain

    write_file(filename, content)
    print("File saved.")
    return filename, content, False


def main():
    filename = None
    plain_content = None
    styled_content = None
    is_new_file = False
    unsaved = False

    while True:
        print("\n=== Secure Editor ===")
        print("1. Create New File")
        print("2. Open File")
        print("3. Edit File")
        print("4. Save File")
        print("5. Show Current Content")
        print("6. Delete File")
        print("7. Delete Content Only")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            filename = input("Enter filename: ").strip()
            create_file(filename)
            plain_content = ""
            styled_content = ""
            is_new_file = True
            unsaved = True

        elif choice == "2":
            filename, data, is_new_file, unsaved = open_file()
            plain_content = data
            styled_content = data

        elif choice == "3":
            filename, plain_content, styled_content, changed = edit_content(filename, plain_content)
            if changed:
                unsaved = True

        elif choice == "4":
            filename, saved, is_new_file = save_file(filename, plain_content, styled_content, is_new_file)
            unsaved = False

        elif choice == "5":
            print("\n--- Current Styled Content ---")
            print(styled_content if styled_content else "[empty]")
            print("-------------------------------")

        elif choice == "6":
            filename = ensure_filename(filename)
            delete_file(filename)
            filename = None
            plain_content = None
            styled_content = None
            unsaved = False

        elif choice == "7":
            filename = ensure_filename(filename)
            delete_content(filename)
            plain_content = ""
            styled_content = ""
            unsaved = False

        elif choice == "8":
            if unsaved:
                save = input("Unsaved changes. Save? (y/n): ")
                if save == "y":
                    filename, saved, is_new_file = save_file(filename, plain_content, styled_content, is_new_file)
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

