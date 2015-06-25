import sys
import struct
import socket
import ssl
import threading
import time
import Mumble_pb2

class MumbleClient(object):
    def __init__(self, host, port, username, **kwargs):
        self.host = host
        self.port = port
        self.username = username

        self.password = None
        if "password" in kwargs:
            self.password = kwargs["password"]

        self.celt_versions = []
        if "celt_versions" in kwargs:
            self.celt_versions = kwargs["celt_versions"]

        self.opus_support = False
        if "opus" in kwargs:
            self.opus_support = kwargs["opus"]

        self.sock = None
        self.inbuf = ''

        self.ping_thread = threading.Thread(target=self.ping)
        self.ping_thread.setDaemon(True)

    def get_bytes(self, num):
        while len(self.inbuf) < num:
            data = self.sock.recv(4096)
            self.inbuf += data
            if len(data) == 0:
                raise Exception()

        return_bts = self.inbuf[:num]
        self.inbuf = self.inbuf[num:]

        return return_bts

    def send_packet(self, proto, code):
        data = proto.SerializeToString()
        prefix = struct.pack(">HI", code, len(data))
        packet = prefix + data
        self.sock.send(packet)

    def ping(self):
        while True:
            ping = Mumble_pb2.Ping()
            ping.timestamp = int(time.time())

            try:
                self.send_packet(ping, 3)
            except Exception:
                break

            time.sleep(20)

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock = ssl.wrap_socket(self.sock)

        cver = Mumble_pb2.Version()
        # Version is a 4-byte int in which each byte is a int.
        # '\x00\x01\x02\x03' = 1.2.3
        cver.version = struct.unpack(">I", struct.pack(">HBB", 1, 2, 3))[0]
        cver.release = "OnVar's Python Mumble client v0.1"
        cver.os = "Python"
        cver.os_version = sys.version

        self.send_packet(cver, 0)

        auth = Mumble_pb2.Authenticate()
        auth.username = self.username
        if self.password:
            auth.password = self.password
        if self.celt_versions:
            auth.celt_versions.extend(self.celt_versions)
        auth.opus = self.opus_support

        self.send_packet(auth, 2)

        self.connect_loop()

    def connect_loop(self):
        sound = ''
        while True:
            try:
                bts = self.get_bytes(6)
                code, length = struct.unpack(">HI", bts)
                data = self.get_bytes(length)
            except Exception:
                print("Connection Closed by Host")
                break

            if code == 0:
                # Version
                sver = Mumble_pb2.Version()
                sver.ParseFromString(data)

                self.on_Version(sver)

            elif code == 1:
                # UDPTunnel
                self.on_UDPTunnel(data)
                print repr(data)

            elif code == 2:
                # Authenticate
                # We should never get this as a client.
                auth = Mumble_pb2.Authenticate()
                auth.ParseFromString(data)

                self.on_Authenticate(auth)

            elif code == 3:
                # Ping
                # This is more of a pong, if we get this.
                pong = Mumble_pb2.Ping()
                pong.ParseFromString(data)

                self.on_Ping(pong)

            elif code == 4:
                # Reject
                rej = Mumble_pb2.Reject()
                rej.ParseFromString(data)

                self.on_Reject(rej)

            elif code == 5:
                # ServerSync
                # This means we're fully connected.
                # Start pinging every 20 seconds.
                self.ping_thread.start()

                sync = Mumble_pb2.ServerSync()
                sync.ParseFromString(data)

                self.on_ServerSync(sync)

            elif code == 6:
                # ChannelRemove
                chan = Mumble_pb2.ChannelRemove()
                chan.ParseFromString(data)

                self.on_ChannelRemove(chan)

            elif code == 7:
                # ChannelState
                chan = Mumble_pb2.ChannelState()
                chan.ParseFromString(data)

                self.on_ChannelState(chan)

            elif code == 8:
                # UserRemove
                user = Mumble_pb2.UserRemove()
                user.ParseFromString(data)

                self.on_UserRemove(user)

            elif code == 9:
                # UserState
                user = Mumble_pb2.UserState()
                user.ParseFromString(data)

                self.on_UserState(user)

            elif code == 10:
                # BanList
                banl = Mumble_pb2.BanList()
                banl.ParseFromString(data)

                self.on_BanList(banl)

            elif code == 11:
                # TextMessage
                text = Mumble_pb2.TextMessage()
                text.ParseFromString(data)

                self.on_TextMessage(text)

            elif code == 12:
                # PermissionDenied
                perm = Mumble_pb2.PermissionDenied()
                perm.ParseFromString(data)

                self.on_PermissionDenied(perm)

            elif code == 13:
                # ACL
                acl = Mumble_pb2.ACL()
                acl.ParseFromString(data)

                self.on_ACL(acl)

            elif code == 14:
                # QueryUsers
                query = Mumble_pb2.QueryUsers()
                query.ParseFromString(data)

                self.on_QueryUsers(query)

            elif code == 15:
                # CryptSetup
                crypt = Mumble_pb2.CryptSetup()
                crypt.ParseFromString(data)

                self.on_CryptSetup(crypt)

            elif code == 16:
                # ContextActionModify
                cam = Mumble_pb2.ContextActionModify()
                cam.ParseFromString(data)

                self.on_ContextActionModify(cam)

            elif code == 17:
                # ContextAction
                action = Mumble_pb2.ContextAction()
                action.ParseFromString(data)

                self.on_ContextAction(action)

            elif code == 18:
                # UserList
                userl = Mumble_pb2.UserList()
                userl.ParseFromString(data)

                self.on_UserList(userl)

            elif code == 19:
                # VoiceTarget
                vtarg = Mumble_pb2.VoiceTarget()
                vtarg.ParseFromString(data)

                self.on_VoiceTarget(vtarg)

            elif code == 20:
                # PermissionQuery
                query = Mumble_pb2.PermissionQuery()
                query.ParseFromString(data)

                self.on_PermissionQuery(query)

            elif code == 21:
                # CodecVersion
                codec = Mumble_pb2.CodecVersion()
                codec.ParseFromString(data)

                self.on_CodecVersion(codec)

            elif code == 22:
                # UserStats
                userstats = Mumble_pb2.UserStats()
                userstats.ParseFromString(data)

                self.on_UserStats(userstats)

            elif code == 23:
                # RequestBlob
                blob = Mumble_pb2.RequestBlob()
                blob.ParseFromString(data)

                self.on_RequestBlob(blob)

            elif code == 24:
                # ServerConfig
                config = Mumble_pb2.ServerConfig()
                config.ParseFromString(data)

                self.on_ServerConfig(config)

            elif code == 25:
                # SuggestConfig
                config = Mumble_pb2.SuggestConfig()
                config.ParseFromString(data)

                self.on_SuggestConfig(config)

            else:
                print("Unknown packet recieved.")

    def on_Version(self, ver):
        pass

    def on_UDPTunnel(self, data):
        pass

    def on_Authenticate(self, auth):
        pass

    def on_Ping(self, ping):
        pass

    def on_Reject(self, rej):
        pass

    def on_ServerSync(self, sync):
        pass

    def on_ChannelRemove(self, chan):
        pass

    def on_ChannelState(self, chan):
        pass

    def on_UserRemove(self, user):
        pass

    def on_UserState(self, user):
        pass

    def on_BanList(self, blist):
        pass

    def on_TextMessage(self, text):
        pass

    def on_PermissionDenied(self, perm):
        pass

    def on_ACL(self, acl):
        pass

    def on_QueryUsers(self, query):
        pass

    def on_CryptSetup(self, crypt):
        pass

    def on_ContextActionModify(self, cam):
        pass

    def on_ContextAction(self, action):
        pass

    def on_UserList(self, userl):
        pass

    def on_VoiceTarget(self, target):
        pass

    def on_PermissionQuery(self, query):
        pass

    def on_CodecVersion(self, codec):
        pass

    def on_UserStats(self, stats):
        pass

    def on_RequestBlob(self, blob):
        pass

    def on_ServerConfig(self, config):
        pass

    def on_SuggestConfig(self, config):
        pass

if __name__ == "__main__":
    cli = MumbleClient("localhost", 64738, "VarBot", opus=True)
    cli.connect()
