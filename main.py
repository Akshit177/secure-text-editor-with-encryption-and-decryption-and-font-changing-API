from editor import create_file, read_file, write_file
import encryption


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
    try:
        data = read_file(name)
    except FileNotFoundError:
        print(" File not found.")
        return None, None

    if encryption.is_encrypted(data):
        print("[!] File is encrypted.")
        pwd = input("Enter password to decrypt: ")
        try:
            data = encryption.decrypt_text(data, pwd)
            print("🔓 Decryption successful.")
        except ValueError as e:
            print(f"❌ {e}")
            return None, None
    else:
        print(" File opened successfully.")

    print("\n--- File Content ---")
    print(data if data else "[empty]")
    print("--------------------")
    return name, data


def edit_content(name, content):
    
    if not name:
        name = input("Enter filename to edit: ").strip()
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
            if changed:
                print(" Note: You have unsaved changes.")
            else:
                print("No changes made.")
            return name, content, changed
        else:
            print("Invalid choice. Try again.")


def save_file(name, content):
    """Save content with optional encryption and overwrite confirmation."""
    if content is None:
        print("❌ Nothing to save.")
        return name, content, False

    if not name:
        name = input("Enter filename to save as: ").strip()

    
    import os
    if os.path.exists(name):
        confirm = input(f" File '{name}' exists. Overwrite? (y/n): ").strip().lower()
        if confirm != "y":
            print(" Save cancelled.")
            return name, content, True  

    encrypt_choice = input("Encrypt before saving? (y/n): ").strip().lower()

    if encrypt_choice == "y":
        pwd = input("Enter password for encryption: ")
        data = encryption.encrypt_text(content, pwd)
    else:
        data = content

    write_file(name, data)
    print(f" File saved successfully as '{name}'.")
    return name, data, False  


def main():
    filename = None
    content = None
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
            name = input("Enter new filename: ").strip()
            try:
                create_file(name)
                print("File created.")
                filename, content, unsaved = name, "", False
            except FileExistsError:
                print(" File already exists.")

        elif choice == "2":
            name, data = open_file()
            if name:
                filename, content, unsaved = name, data, False

        elif choice == "3":
            filename, content, changed = edit_content(filename, content)
            if changed:
                unsaved = True

        elif choice == "4":
            filename, content, unsaved = save_file(filename, content)

        elif choice == "5":
            print("\n--- Current Content ---")
            print(content if content else "[empty]")
            print("-----------------------")

        elif choice == "6":
            if unsaved:
                confirm = input(" You have unsaved changes. Save before exit? (y/n): ").strip().lower()
                if confirm == "y":
                    filename, content, unsaved = save_file(filename, content)
            print(" Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
