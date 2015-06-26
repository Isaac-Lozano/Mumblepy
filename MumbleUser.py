

class MumbleUser(object):
    def __init__(self, proto):
        self.session = proto.session
        self.name = proto.name
        self.user_id = None
        self.channel_id = proto.channel_id
        self.mute = False
        self.deaf = False
        self.suppress = False
        self.self_mute = False
        self.self_deaf = False
        self.texture = None
        self.plugin_context = None
        self.plugin_identity = None
        self.comment = None
        self.hash = None
        self.comment_hash = None
        self.texture_hash = None
        self.priority_speaker = False
        self.recording = False

        self.update(proto)

    def update(self, proto):
        if proto.HasField("name"):
            self.name = proto.name
        if proto.HasField("user_id"):
            self.user_id = proto.user_id
        if proto.HasField("channel_id"):
            self.channel_id = proto.channel_id
        if proto.HasField("mute"):
            self.mute = proto.mute
        if proto.HasField("deaf"):
            self.deaf = proto.deaf
        if proto.HasField("suppress"):
            self.suppress = proto.suppress
        if proto.HasField("self_mute"):
            self.self_mute = proto.self_mute
        if proto.HasField("self_deaf"):
            self.self_deaf = proto.self_deaf
        if proto.HasField("texture"):
            self.texture = proto.texture
        if proto.HasField("plugin_context"):
            self.plugin_context = proto.plugin_context
        if proto.HasField("plugin_identity"):
            self.plugin_identity = proto.plugin_identity
        if proto.HasField("comment"):
            self.comment = proto.comment
        if proto.HasField("hash"):
            self.hash = proto.hash
        if proto.HasField("comment_hash"):
            self.comment_hash = proto.comment_hash
        if proto.HasField("texture_hash"):
            self.texture_hash = proto.texture_hash
        if proto.HasField("priority_speaker"):
            self.priority_speaker = proto.priority_speaker
        if proto.HasField("recording"):
            self.recording = proto.recording

    def __str__(self):
        string = ""
        string += "Session: " + str(self.session) + "\n"
        string += "Name: " + self.name + "\n"
        string += "UserID: " + str(self.user_id or "")+ "\n"
        string += "ChannelID: " + str(self.channel_id) + "\n"
        string += "Mute: " + str(self.mute) + "\n"
        string += "Deaf: " + str(self.deaf) + "\n"
        string += "Suppress: " + str(self.suppress) + "\n"
        string += "SelfMute: " + str(self.self_mute) + "\n"
        string += "SelfDeaf: " + str(self.self_deaf)+ "\n"
        string += "Texture: " + repr(self.texture) + "\n"
        string += "PluginContext: " + repr(self.plugin_context) + "\n"
        string += "PluginIdentity: " + (self.plugin_identity or "") + "\n"
        string += "Comment: " + (self.comment or "") + "\n"
        string += "Hash: " + (self.hash or "") + "\n"
        string += "CommentHash: " + repr(self.comment_hash or "") + "\n"
        string += "TextureHash: " + repr(self.texture_hash or "") + "\n"
        string += "PrioritySpeaker: " + str(self.priority_speaker) + "\n"
        string += "Recording: " + str(self.recording) + "\n"
        return string
