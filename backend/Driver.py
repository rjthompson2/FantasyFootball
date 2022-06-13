import CollectData
import RunDraft
import TeamBuilder

def main(choice) -> None:
    choice.main(None)

#TODO distribution of recovery time per injury
#TODO change all historic data from webscraper to nfl api (nflfastR/nflfastR_python and nflfastpy)
#TODO save to SQL or google sheets instead of CSV
#TODO look into arcparse package
#TODO generative adversarial network for Drafting
#TODO something like synthea data obsucation
#TODO Faust event bus? 
#TODO Decision trees after adding events
#TODO Documenting and typing

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