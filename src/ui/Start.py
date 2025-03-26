
from src.ui.UI import UI
from GUI import GUI


if __name__ == "__main__":
    option = input("Choose the interface(GUI/Console): ")
    if option == "GUI":
        gui = GUI()
        gui.run()
    elif option == "Console":
        ui = UI()
        ui.run()
    else:
        print("Invalid option, please choose between GUI and Console!")
