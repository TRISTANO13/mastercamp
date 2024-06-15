from tkinter import Tk
from loginWin import LoginWindow
from database import*


if __name__ == "__main__":
    # Afficher les utilisateurs dans le terminal
    print_users()

    # Supprimer un utilisateur
    username_to_delete = "lucas"
    delete_user(username_to_delete)
    print(f"User '{username_to_delete}' deleted.")

    # Afficher les utilisateurs après suppression
    print_users()

    root = Tk()
    app = LoginWindow(root)
    root.mainloop()