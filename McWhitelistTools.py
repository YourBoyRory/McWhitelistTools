import json
import requests
import traceback
from uuid import UUID

class McWhitelistTools:

    def __init__(self, whitelistJSON):
        self.whitelistJSON = whitelistJSON
        self.dropChanges()
    
    # set the list to a empty one
    def clearAll(self):
        self.whitelist = []
    
    # Removed all entries with that name
    def removeByName(self, username):
        count = 0
        itemsToDelete = []
        for entry in self.whitelist:
            count += 1
            if entry['name'] == username:
                # This is silly, we need to store the items in a list before remove
                # I think this is because once we delete the item in whitelist drop by X 
                # and it gets confused and skips the last X unchecked in the list
                temp = [None]
                temp[0] = entry
                itemsToDelete += temp
        if itemsToDelete:
            for entry in itemsToDelete:
                self.whitelist.remove(entry)
            return True
        else:
            print(f"[McWhitelistTools/INFO] {username} not in list, skipping delete...")
            return False
        
    # Adds a user by looking up the users UUID, similar to how 'minecraft:whitelist add' does
    def addByName(self, username):
        uuid = self.getUUID(username)
        if uuid is not None or username is not None:
            self.addEntry(username, uuid)
            return True
        return False
        
    # Removed all entries with that uuid
    def removeByUUID(self, uuid):
        count = 0
        itemsToDelete = []
        for entry in self.whitelist:
            count += 1
            if entry['uuid'] == uuid:
                # This is silly, we need to store the items in a list before remove
                # I think this is because once we delete the item in whitelist drop by X 
                # and it gets confused and skips the last X unchecked in the list
                temp = [None]
                temp[0] = entry
                itemsToDelete += temp
                entriesRemoved = True
        if  itemsToDelete:
            for entry in itemsToDelete:
                self.whitelist.remove(entry)
            return True
        else:
            return False
            
    def uuidExists(self, uuid):
        for entry in self.whitelist:
            if entry['uuid'] == uuid:
                return True
        return False
        
    def nameExists(self, name):
        for entry in self.whitelist:
            if entry['name'] == name:
                return True
        return False
    
    # Reloads the list from stored state
    def dropChanges(self):
        try:
            with open(self.whitelistJSON) as f:
                self.whitelist = json.load(f)
        except:
            print("[McWhitelistTools/WARN] Could not find existing whitelist")
            self.clearAll()

    # Saves the stored list and all changes
    def writeChanges(self):
        try:
            with open(self.whitelistJSON, 'w') as f:
                json.dump(self.whitelist, f, indent=2)
        except:
            print("[McWhitelistTools/ERROR] Changes did not save: The file is not Writable.")
            print(traceback.format_exc())

    # adds an entry to the list
    def addEntry(self, username, uuid):
        entry = { }
        entry['uuid'] = uuid
        entry['name'] = username
        temp = [None]
        temp[0] = entry
        for entry in self.whitelist:
            if entry['uuid'] == uuid:
                return 
        self.whitelist += temp
        
    # adds an entry to the list
    def removeEntry(self, username, uuid):
        entriesRemoved = False
        for entry in self.whitelist:
            if entry['name'] == username and entry['uuid'] == uuid:
                self.whitelist.remove(entry)
                entriesRemoved = True
        return entriesRemoved
        
    # looks up users UUID
    def getUUID(self, username):
        try:
            response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
            uuid = UUID(response['id'])
            return str(uuid)
        except:
            print(f"[McWhitelistTools/WARN] could not find user {username}, skipping...")
            return None
    
    # returns a prettied list
    def getList(self):
        dump = json.dumps(self.whitelist, indent=2)
        return dump
