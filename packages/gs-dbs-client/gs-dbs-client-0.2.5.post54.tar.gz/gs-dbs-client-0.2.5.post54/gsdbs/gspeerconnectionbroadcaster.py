import ast
import json
import logging
import platform
import time

import socketio
from aiortc import RTCPeerConnection
from aiortc.contrib.media import MediaPlayer, MediaRelay


class GSPeerConnectionBroadcaster:
    #
    # def __init__(self):
    #     self.webcam = None
    #     self.relay = None

    def create_local_tracks(self, fr, hres, vres, rtbufsize, device):
        options = {"framerate": str(fr), "video_size": str(hres) + "x" + str(vres), "rtbufsize": str(rtbufsize)}
        if self.relay is None:
            if platform.system() == "Darwin":
                self.webcam = MediaPlayer("default:none", format="avfoundation", options=options)
            elif platform.system() == "Windows":
                self.webcam = MediaPlayer(f"video={device}", format="dshow", options=options)
            else:
                self.webcam = MediaPlayer(f"{device}", format="v4l2", options=options)
            self.relay = MediaRelay()
        return self.relay.subscribe(self.webcam.video)

    @classmethod
    async def create(cls, gsdbs):
        self = GSPeerConnectionBroadcaster()
        self.gsdbs = gsdbs
        self.sio = socketio.AsyncClient()
        self.peerConnections = {}
        self._logger = logging.getLogger(__name__)
        self.webcam = None
        self.relay = None

        @self.sio.event
        async def connect():
            self._logger.info('connection established')
            # await self.sio.emit("broadcaster", "")

        @self.sio.event
        async def answer(id, description):
            if type(description) == str:
                description = ast.literal_eval(description)
            desc = type('new_dict', (object,), description)
            await self.peerConnections[id].setRemoteDescription(desc)

        @self.sio.event
        async def watcher(id):
            pc = RTCPeerConnection()
            self.peerConnections[id] = pc
            pc.addTrack(self.create_local_tracks(
                self.gsdbs.credentials["framerate"],
                self.gsdbs.credentials["hres"],
                self.gsdbs.credentials["vres"],
                self.gsdbs.credentials["rtbufsize"],
                self.gsdbs.credentials["device"]
            ))

            channel = pc.createDataChannel("message")

            # def send_data():
            #     channel.send("test123")
            # channel.on("open", send_data)

            @pc.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                # self._logger.info("ICE connection state is %s", pc.iceConnectionState)
                if pc.iceConnectionState == "failed":
                    await pc.close()
                    self.peerConnections.pop(id, None)

            await pc.setLocalDescription(await pc.createOffer())
            await self.sio.emit("offer", {"id": id,
                                          "message": json.dumps(
                                              {"type": pc.localDescription.type, "sdp": pc.localDescription.sdp})})
            # self._logger.info(pc.signalingState)

        @self.sio.event
        async def disconnectPeer(id):
            if id in self.peerConnections:
                await self.peerConnections[id].close()
                self.peerConnections.pop(id, None)

        @self.sio.event
        async def disconnect():
            self._logger.info('disconnected from server')

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}')
        await self.sio.wait()
