from editor import read_file, write_file
import encryption
import os


def multiline_input():
    print("Enter text (type ':wq' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == ":wq":
            break
        lines.append(line)
    return "\n".join(lines)


def open_file():
    name = input("Enter filename to open: ").strip()
    if not os.path.exists(name):
        print(" File not found.")
        return None, None, False, False

    data = read_file(name)
    is_new = False  

    if encryption.is_encrypted(data):
        print(" File is encrypted.")
        pwd = input("Enter password to decrypt: ")
        try:
            data = encryption.decrypt_text(data, pwd)
        except ValueError as e:
            print(f" {e}")
            return None, None, False, False
        print(" Decryption successful.")
    else:
        print(" File opened successfully.")

    print("\n--- File Content ---")
    print(data if data else "[empty]")
    print("--------------------")
    return name, data, is_new, False


def ensure_filename(name):
    if not name:
        name = input("Enter filename: ").strip()
    return name


def edit_content(name, content):
    name = ensure_filename(name)
    if content is None:
        content = ""

    changed = False

    while True:
        print(f"\nEditing: {name}")
        print("1. Replace entire content")
        print("2. Append to content")
        print("3. Find & Replace text")
        print("4. Show current content")
        print("5. Finish editing")
        choice = input("Choice: ").strip()

        if choice == "1":
            content = multiline_input()
            changed = True
        elif choice == "2":
            content += ("\n" if content else "") + multiline_input()
            changed = True
        elif choice == "3":
            find = input("Text to find: ")
            repl = input("Replace with: ")
            content = content.replace(find, repl)
            print(" Find & Replace done.")
            changed = True
        elif choice == "4":
            print("\n--- Current Content ---")
            print(content if content else "[empty]")
            print("------------------------")
        elif choice == "5":
            return name, content, changed
        else:
            print("Invalid choice. Try again.")


def save_file(name, content, is_new_file):
    if content is None:
        print(" Nothing to save.")
        return name, content, is_new_file

    name = ensure_filename(name)

 
    if not is_new_file and os.path.exists(name):
        confirm = input(f" File '{name}' exists. Overwrite? (y/n): ").strip().lower()
        if confirm != "y":
            print(" Save cancelled.")
            return name, content, is_new_file

    encrypt_choice = input("Encrypt before saving? (y/n): ").strip().lower()
    if encrypt_choice == "y":
        pwd = input("Enter password for encryption: ")
        data = encryption.encrypt_text(content, pwd)
    else:
        data = content

    write_file(name, data)
    print(f"  File saved successfully as '{name}'.")
    return name, data, False  


def main():
    filename = None
    content = None
    is_new_file = False
    unsaved = False

    while True:
        print("\n=== Secure Text Editor ===")
        print("1. Create New File")
        print("2. Open File")
        print("3. Edit File")
        print("4. Save File")
        print("5. Show Current Content")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            filename = input("Enter new filename: ").strip()
            content = ""
            is_new_file = True
            unsaved = True
            print("  New file created (not saved yet).")

        elif choice == "2":
            filename, content, is_new_file, unsaved = open_file()

        elif choice == "3":
            filename, content, changed = edit_content(filename, content)
            if changed:
                unsaved = True

        elif choice == "4":
            filename, content, is_new_file = save_file(filename, content, is_new_file)
            unsaved = False

        elif choice == "5":
            filename = ensure_filename(filename)
            print("\n--- Current Content ---")
            print(content if content else "[empty]")
            print("-----------------------")

        elif choice == "6":
            if unsaved:
                confirm = input(" You have unsaved changes. Save before exit? (y/n): ").strip().lower()
                if confirm == "y":
                    filename, content, is_new_file = save_file(filename, content, is_new_file)
            print("  Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

