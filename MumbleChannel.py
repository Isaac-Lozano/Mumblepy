

class MumbleChannel(object):
    def __init__(self, proto):
        # We assume channel_id and name are always there
        # when we add a new channel.
        # Channels cannot be made without a name, so...
        self.channel_id = proto.channel_id
        self.parent = None
        self.name = proto.name
        self.links = []
        self.description = None
        self.temporary = False
        self.position = 0
        self.description_hash = None

        self.update(proto)

    def update(self, proto):
        # Update everything but channel ID.
        # That doesn't change

        if proto.HasField("parent"):
            self.parent = proto.parent
        if proto.HasField("name"):
            self.name = proto.name
        if len(proto.links) != 0:
            self.links = proto.links
        if proto.HasField("description"):
            self.description = proto.description
        if len(proto.links_add):
            self.links.extend(proto.links_add)
        if len(proto.links_remove):
            for link in proto.links_remove:
                self.links.remove(link)
        if proto.HasField("temporary"):
            self.temporary = proto.temporary
        if proto.HasField("position"):
            self.position = proto.position
        if proto.HasField("description_hash"):
            self.description_hash = proto.description_hash

    def __str__(self):
        string = ""
        string += "ChannelID: " + str(self.channel_id) + "\n"
        string += "Parent: " + str(self.channel_id or "Root") + "\n"
        string += "Name: " + self.name + "\n"
        string += "Links: "
        for link in self.links:
            string += str(link) + " "
        string += "\n"
        string += "Description: " + (self.description or "") + "\n"
        string += "Temporary: " + str(self.temporary) + "\n"
        string += "Position: " + str(self.position) + "\n"
        string += "DescriptionHash: " + repr(self.description_hash or "") + "\n"
        return string
