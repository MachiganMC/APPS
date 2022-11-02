import MDP.Menu as Menu
from MDP.Entry import Entry
import MDP.SaveData as Save


if __name__ == '__main__':
    # entry = Entry("fezbnef", "moi", "google")
    # entry1 = Entry("dza", "pas moi", "google")
    # entry2 = Entry("addf", "yo", "pas google")
    # entry3 = Entry("fne", "salut", "pas google")
    Save.load()
    Menu.accueil()
