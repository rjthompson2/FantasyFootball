import CollectData
from backend.draft import RunDraft
from backend.draft import TeamBuilder

def main(choice) -> None:
    choice.main(None)

if __name__ == '__main__':
    choices = {
        '0': CollectData,
        '1': RunDraft,
        '2': TeamBuilder,
    }

    while True:
        print("Enter '0' to set up data")
        print("Enter '1' to start draft")
        print("Enter '2' for post-draft trading suggestions")
        print("Enter 'exit' to exit the program")
        choice = input("")
        if choice == 'exit':
            quit()
        if choice in choices:
            main(choices[choice])