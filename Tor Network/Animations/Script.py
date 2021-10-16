from manim import *
from random import randint

# ManimCE Version 0.10.0
# 1920x1080 60FPS

PixelWidth = config.pixel_width = 1920
PixelHeight = config.pixel_height = 1080
FPS = config.frame_rate = 60

print(f"Rendering ManimCE (0.10.0) at {PixelWidth}x{PixelHeight} {FPS}FPS.")

# Global Variables
CENTER = [0, 0, 0]

class DataPacket():
    def __init__(self, isFrom='', to='', content='', packetColor=WHITE, rectangleExtraSize=1, fromColor=RED, toColor=BLUE, contentColor=GREEN):
        self.fromColor, self.toColor = fromColor, toColor
        self.isFrom, self.to, self.content = Tex(isFrom).set_color(fromColor), Tex(to).set_color(toColor), Tex(content).set_color(contentColor)
        self.height = max(self.isFrom.height, self.to.height, self.content.height) + rectangleExtraSize
        self.fromRectangle = Rectangle(width=self.isFrom.width + rectangleExtraSize, height=self.height).set_color(packetColor)
        self.toRectangle = Rectangle(width=self.to.width + rectangleExtraSize, height=self.height).set_color(packetColor)
        self.contentRectangle = Rectangle(width=self.content.width + rectangleExtraSize, height=self.height).set_color(packetColor)

        self.fromRectangle.next_to(self.contentRectangle, LEFT, buff=0)
        self.toRectangle.next_to(self.contentRectangle, RIGHT, buff=0)

        self.isFrom.move_to(self.fromRectangle.get_center())
        self.to.move_to(self.toRectangle.get_center())
        self.content.move_to(self.contentRectangle.get_center())

        self.asRectangle = VGroup(self.fromRectangle, self.toRectangle, self.contentRectangle, self.isFrom, self.to, self.content)
        self.width = self.asRectangle.width

    def replaceSender(self, newSender):
        toPosition = self.isFrom.get_center()
        self.asRectangle.remove(self.isFrom)
        self.isFrom = Tex(newSender).set_color(self.fromColor)
        self.isFrom.move_to(toPosition)
        self.asRectangle.add(self.isFrom)

    def replaceReciever(self, newReciever):
        toPosition = self.to.get_center()
        self.asRectangle.remove(self.to)
        self.to = Tex(newReciever).set_color(self.toColor)
        self.to.move_to(toPosition)
        self.asRectangle.add(self.to)

    def replaceComputers(self, newSender, newReciever):
        self.replaceSender(newSender)
        self.replaceReciever(newReciever)

    def fillIt(self): return None

class InternetTraffic(Scene):
    def PacketContent(self):
        Computer1, Computer2 = SVGMobject("../Images/Computer Icon.svg").scale(0.75).to_edge(LEFT), SVGMobject("../Images/Computer Icon.svg").scale(0.75).to_edge(RIGHT)
        Connection = Line(Computer1.get_center(), Computer2.get_center(), z_index=-1).set_color(GREY)
        Computers = VGroup(Computer1, Computer2, Connection)
        Packet = Rectangle(width=1, height=0.25, z_index=-1).set_fill(GREY, opacity=1).move_to(Computer1)
        self.play(FadeIn(Computers), FadeIn(Packet))
        self.wait()
        self.play(Packet.animate.move_to(Computer2), run_time=2.5)
        self.wait()
        self.play(Packet.animate.move_to(Computer1), run_time=2.5)
        self.wait(0.5)
        MyPacket = DataPacket("Emisor", "Receptor", "Contenido", fromColor=WHITE, toColor=WHITE, contentColor=WHITE)
        MyPacket.isFrom.set_opacity(0.25)
        MyPacket.to.set_opacity(0.25)
        MyPacket.content.set_opacity(0.25)
        self.play(FadeOut(Packet), FadeOut(Computers), FadeIn(MyPacket.asRectangle))
        self.play(MyPacket.isFrom.animate.set_color(YELLOW).set_opacity(1))
        self.wait(3)
        self.play(MyPacket.to.animate.set_color(YELLOW).set_opacity(1), MyPacket.isFrom.animate.set_color(WHITE).set_opacity(0.25))
        self.wait(4)
        self.play(MyPacket.content.animate.set_color(YELLOW).set_opacity(1), MyPacket.to.animate.set_color(WHITE).set_opacity(0.25))
        self.wait(3)

    def EncryptedPacket(self):
        MyPacket = DataPacket("Emisor", "Receptor", "Contenido", fromColor=BLUE, toColor=RED, contentColor=GREEN)
        self.play(FadeIn(MyPacket.asRectangle))
        self.wait(2)
        self.play(MyPacket.content.animate.set_fill(GREY), MyPacket.contentRectangle.animate.set_fill(GREY, opacity=1), run_time=2)
        self.wait(3)

    def ConstructScene(self, useAudio=True):
        # if useAudio: self.add_sound("../Audio/Petición a un Servidor-1.mp3")
        # self.PacketContent()

        if useAudio: self.add_sound("../Audio/Petición a un Servidor-2.mp3")
        self.EncryptedPacket()

    def construct(self): self.ConstructScene()

class TorMainIdea(Scene):
    def TorJumpingNodes(self):
        Computer_A = SVGMobject("../Images/Computer Icon.svg").scale(0.5).to_edge(LEFT)
        Computer_B = SVGMobject("../Images/Server Icon.svg").scale(0.5).to_edge(RIGHT)
        Computer_C = SVGMobject("../Images/Computer Icon.svg").scale(0.5).shift(DOWN+2*LEFT)
        Computer_D = SVGMobject("../Images/Computer Icon.svg").scale(0.5).shift(UP+2*RIGHT)
        C1 = Line(Computer_A.get_center(), Computer_C.get_center(), z_index=-1)
        C2 = Line(Computer_C.get_center(), Computer_D.get_center(), z_index=-1)
        C3 = Line(Computer_D.get_center(), Computer_B.get_center(), z_index=-1)
        Connections = VGroup(C1, C2, C3)
        Computers = VGroup(Computer_A, Computer_B, Computer_C, Computer_D)

        Packet = Rectangle(width=1, height=0.25, z_index=-2).set_fill(GREY, opacity=1).scale(0.3).move_to(Computer_A)

        self.play(FadeIn(Computers), FadeIn(Packet))

        self.wait()

        self.play(Write(Connections))

        A, B, C, D = Tex("A").set_color(RED), Tex("B").set_color(BLUE), Tex("C").set_color(GREEN), Tex("D").set_color(YELLOW)
        A.next_to(Computer_A, UP)
        B.next_to(Computer_B, UP)
        C.next_to(Computer_C, UP)
        D.next_to(Computer_D, UP)

        self.play(Write(A))
        self.play(Write(B))
        self.wait(1.5)
        self.play(Write(C))
        self.play(Write(D))

        self.wait(0.75)

        self.play(Packet.animate.move_to(Computer_C))
        self.wait(0.5)
        self.play(Packet.animate.move_to(Computer_D))
        self.wait(0.5)
        self.play(Packet.animate.move_to(Computer_B))
        self.wait()

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("../Audio/Idea Principal de Tor-1.mp3")
        self.TorJumpingNodes()

    def construct(self): self.ConstructScene()

class TextGenerator(Scene):
    def construct(self):
        Text = Tex("Capa", " III").scale(5)
        Text[1].set_color(RED)
        self.play(Write(Text), run_time=2)
        self.wait()
        self.play(Uncreate(Text))

class ConnectionToNetwork(Scene):
    def TorDirectory(self):
        Computer = SVGMobject("../Images/Computer Icon.svg").scale(0.75).to_edge(LEFT)
        Directory = SVGMobject("../Images/Server Icon.svg").scale(0.75).to_edge(RIGHT)
        Connection = Line(Computer.get_center(), Directory.get_center(), z_index=-1).set_color(GREY)
        Computers = VGroup(Computer, Directory, Connection)
        Packet = Rectangle(width=1, height=0.25, z_index=-1).set_fill(GREY, opacity=1).scale(0.75).move_to(Computer)

        self.play(Write(Computers))
        self.wait()
        self.play(Packet.animate.move_to(Directory))
        self.wait()

        self.remove(Packet)
        self.play(Uncreate(Computer), Uncreate(Connection), Directory.animate.scale(2).move_to(ORIGIN))
        self.wait()

    def CircuitCreation(self):
        Computer = SVGMobject("../Images/Computer Icon.svg").scale(0.75).to_edge(LEFT)
        Directory = SVGMobject("../Images/Server Icon.svg").scale(0.75).to_edge(RIGHT)
        ComputerText, DirectoryText = Tex("A").set_color(RED).next_to(Computer, DOWN), Tex("B").set_color(BLUE).next_to(Directory, DOWN)
        Connection = Line(Computer.get_center(), Directory.get_center(), z_index=-1).set_color(GREY)
        Computers = VGroup(Computer, Directory, Connection, ComputerText, DirectoryText)
        MyPacket = DataPacket("B", "A", "Nodo 1 | Nodo 2 | Nodo 3", fromColor=BLUE, toColor=RED, contentColor=WHITE)
        Packet = Rectangle(width=1, height=0.25, z_index=-1).set_fill(GREY, opacity=1).scale(0.75).move_to(Computer)

        self.play(Write(Computers))
        self.wait()
        self.play(Packet.animate.move_to(Directory))
        self.wait()
        self.play(Packet.animate.move_to(CENTER))
        self.wait(0.5)

        self.play(FadeOut(Computers), Transform(Packet, MyPacket.asRectangle))
        self.wait()
        MyPacket = DataPacket("B", "A", "Nodo 1 | Nodo 2 | Nodo 3 + circID", fromColor=BLUE, toColor=RED, contentColor=WHITE)
        self.play(Transform(Packet, MyPacket.asRectangle))
        self.wait()

    def KeyGeneration(self):
        FromComputer, ToServer = SVGMobject("../Images/Computer Icon.svg").scale(0.5).to_edge(LEFT), SVGMobject("../Images/Server Icon.svg").scale(0.5).to_edge(RIGHT)

        Node1, Node2, Node3 = SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5)
        Node1.next_to(FromComputer, RIGHT).shift(2*RIGHT).shift(1*UP)
        Node2.move_to(CENTER).shift(2*DOWN)
        Node3.next_to(ToServer, LEFT).shift(2*LEFT).shift(0.75*UP)

        C1, C2 = Line(FromComputer.get_center(), Node1.get_center(), z_index=-1), Line(Node1.get_center(), Node2.get_center(), z_index=-1)
        C3, C4 = Line(Node2.get_center(), Node3.get_center(), z_index=-1), Line(Node3.get_center(), ToServer.get_center(), z_index=-1)
        Connections = VGroup(C1, C2, C3, C4)

        T1, T2, T3 = Tex("A").set_color(YELLOW).next_to(Node1, UP), Tex("B").set_color(BLUE).next_to(Node2, UP), Tex("C").set_color(RED).next_to(Node3, UP)
        Node1, Node2, Node3 = VGroup(Node1, T1), VGroup(Node2, T2), VGroup(Node3, T3)

        Nodes = VGroup(Node1, Node2, Node3)

        Key1 = SVGMobject("../Images/Yellow Key.svg").set_fill(YELLOW, opacity=1).scale(0.15).next_to(Node1, DOWN)
        Key2 = SVGMobject("../Images/Yellow Key.svg").set_fill(BLUE, opacity=1).scale(0.15).next_to(Node2, DOWN)
        Key3 = SVGMobject("../Images/Yellow Key.svg").set_fill(RED, opacity=1).scale(0.15).next_to(Node3, DOWN)

        self.play(Write(Nodes), Write(FromComputer), Write(ToServer), Write(Connections))

        self.wait()

        self.play(FadeIn(Key1))
        self.play(FadeIn(Key2))
        self.play(FadeIn(Key3))

        Node1 += Key1
        Node2 += Key2
        Node3 += Key3

        self.wait(2)

        R1 = Rectangle(width=Node1.width+1, height=Node1.height+1, color=YELLOW).move_to(Node1)
        R2 = Rectangle(width=Node2.width+1, height=Node2.height+1, color=BLUE).move_to(Node2)
        R3 = Rectangle(width=Node3.width+1, height=Node3.height+1, color=RED).move_to(Node3)

        self.play(Write(R1))
        self.wait(0.15)
        self.play(Write(R2))
        self.wait(0.15)
        self.play(Write(R3))

    def ConstructScene(self, useAudio=True):
        # if useAudio: self.add_sound("../Audio/Conexión al Protocolo Tor-1.mp3")
        # self.TorDirectory()

        # if useAudio: self.add_sound("../Audio/Conexión al Protocolo Tor-2.mp3")
        # self.CircuitCreation()

        if useAudio: self.add_sound("../Audio/Conexión al Protocolo Tor-3.mp3")
        self.KeyGeneration()

    def construct(self): self.ConstructScene()

class SendingData(Scene):
    def EncryptionLayer1(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE
        FromComputer, ToServer = SVGMobject("../Images/Computer Icon.svg").scale(0.5).to_edge(LEFT), SVGMobject("../Images/Server Icon.svg").scale(0.5).to_edge(RIGHT)

        Node1, Node2, Node3 = SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5)
        Node1.next_to(FromComputer, RIGHT).shift(2*RIGHT)
        Node2.move_to(CENTER)
        Node3.next_to(ToServer, LEFT).shift(2*LEFT)

        C1, C2 = Line(FromComputer.get_center(), Node1.get_center(), z_index=-1), Line(Node1.get_center(), Node2.get_center(), z_index=-1)
        C3, C4 = Line(Node2.get_center(), Node3.get_center(), z_index=-1), Line(Node3.get_center(), ToServer.get_center(), z_index=-1)
        Connections = VGroup(C1, C2, C3, C4)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.15).move_to(Node1)
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.15).move_to(Node2)
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.15).move_to(Node3)

        T1, T2, T3 = Tex("N1").set_color(NODE1_COLOR).scale(0.75).next_to(Node1, UP), Tex("N2").set_color(NODE2_COLOR).scale(0.75).next_to(Node2, UP), Tex("N3").scale(0.75).set_color(NODE3_COLOR).next_to(Node3, UP)
        Node1, Node2, Node3 = VGroup(Node1, T1, K1), VGroup(Node2, T2, K2), VGroup(Node3, T3, K3)
        Nodes = VGroup(Node1, Node2, Node3)

        TA, TB = Tex("A").set_color(COMPUTER_COLOR).next_to(FromComputer, UP), Tex("B").set_color(SERVER_COLOR).next_to(ToServer, UP)
        FromComputer, ToServer = VGroup(FromComputer, TA), VGroup(ToServer, TB)
        Computers = VGroup(FromComputer, ToServer)

        Connections.set_opacity(0.5)
        Nodes.set_opacity(0.5)
        Computers.set_opacity(0.5)

        FromComputer.set_opacity(1)
        ToServer.set_opacity(1)

        Circuit = VGroup(Connections, Nodes, Computers)

        R1 = Rectangle(width=FromComputer.width+0.5, height=FromComputer.height+0.5, color=COMPUTER_COLOR).move_to(FromComputer)
        R2 = Rectangle(width=ToServer.width+0.5, height=ToServer.height+0.5, color=SERVER_COLOR).move_to(ToServer)

        Circuit += R1
        Circuit += R2

        self.play(Write(Connections), Write(Nodes), Write(Computers))

        self.wait(0.75)

        self.play(Write(R1))

        self.wait()

        self.play(Write(R2))

        self.wait()

        MyPacket1 = DataPacket("A", "B", "Contenido", fromColor=COMPUTER_COLOR, toColor=SERVER_COLOR, contentColor=WHITE)
        MyPacket1.asRectangle.scale(1.5).shift(DOWN)
        self.play(Write(MyPacket1.asRectangle), Circuit.animate.to_edge(UP))

        self.wait(10)

        MyPacket_ = DataPacket("N", "B", "Contenido", fromColor=NODE3_COLOR, toColor=SERVER_COLOR, contentColor=WHITE)
        MyPacket_.replaceSender("N3")
        MyPacket_.asRectangle.scale(1.5).shift(DOWN)

        self.play(Transform(MyPacket1.isFrom, MyPacket_.isFrom),
        FromComputer.animate.set_opacity(0.5), R1.animate.move_to(Node3.get_center()).set_color(NODE3_COLOR), Node3.animate.set_opacity(1))

        self.wait(6)

        Key3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=0.75).scale(0.5).move_to(MyPacket1.asRectangle.get_center())

        self.play(MyPacket1.fromRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket1.contentRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket1.toRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket1.content.animate.set_opacity(0), MyPacket1.isFrom.animate.set_opacity(0), MyPacket1.to.animate.set_opacity(0),
                  FadeIn(Key3))

        self.wait()

        self.wait()

        MyPacket2 = DataPacket("N2", "N3", "Contenido", fromColor=NODE2_COLOR, toColor=NODE3_COLOR, contentColor=WHITE)
        MyPacket2.asRectangle.scale(1.5).shift(DOWN)
        MyPacket2.content.set_opacity(0)

        EncryptedPacket = VGroup(Rectangle(width=MyPacket2.contentRectangle.width, height=MyPacket2.contentRectangle.height).set_fill(GREY, opacity=1)).move_to(MyPacket1.asRectangle.get_center())

        self.play(Write(MyPacket2.asRectangle), ToServer.animate.set_opacity(0.5), Node2.animate.set_opacity(1),
        R1.animate.move_to(Node2.get_center()).set_color(NODE2_COLOR),
        R2.animate.move_to(Node3.get_center()).set_color(NODE3_COLOR),
        Transform(MyPacket1.asRectangle, EncryptedPacket))

        MyPacket1.asRectangle.add(Key3)

        self.wait()

    def EncryptionLayer2(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE
        FromComputer, ToServer = SVGMobject("../Images/Computer Icon.svg").scale(0.5).to_edge(LEFT), SVGMobject("../Images/Server Icon.svg").scale(0.5).to_edge(RIGHT)

        Node1, Node2, Node3 = SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5)
        Node1.next_to(FromComputer, RIGHT).shift(2*RIGHT)
        Node2.move_to(CENTER)
        Node3.next_to(ToServer, LEFT).shift(2*LEFT)

        C1, C2 = Line(FromComputer.get_center(), Node1.get_center(), z_index=-1), Line(Node1.get_center(), Node2.get_center(), z_index=-1)
        C3, C4 = Line(Node2.get_center(), Node3.get_center(), z_index=-1), Line(Node3.get_center(), ToServer.get_center(), z_index=-1)
        Connections = VGroup(C1, C2, C3, C4)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.15).move_to(Node1)
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.15).move_to(Node2)
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.15).move_to(Node3)

        T1, T2, T3 = Tex("N1").set_color(NODE1_COLOR).scale(0.75).next_to(Node1, UP), Tex("N2").set_color(NODE2_COLOR).scale(0.75).next_to(Node2, UP), Tex("N3").scale(0.75).set_color(NODE3_COLOR).next_to(Node3, UP)
        Node1, Node2, Node3 = VGroup(Node1, T1, K1), VGroup(Node2, T2, K2), VGroup(Node3, T3, K3)
        Nodes = VGroup(Node1, Node2, Node3)

        TA, TB = Tex("A").set_color(COMPUTER_COLOR).next_to(FromComputer, UP), Tex("B").set_color(SERVER_COLOR).next_to(ToServer, UP)
        FromComputer, ToServer = VGroup(FromComputer, TA), VGroup(ToServer, TB)
        Computers = VGroup(FromComputer, ToServer)

        Connections.set_opacity(0.5)
        Nodes.set_opacity(0.5)
        Computers.set_opacity(0.5)

        Node2.set_opacity(1)
        Node3.set_opacity(1)

        Circuit = VGroup(Connections, Nodes, Computers)

        R1 = Rectangle(width=FromComputer.width+0.5, height=FromComputer.height+0.5, color=NODE2_COLOR).move_to(Node2)
        R2 = Rectangle(width=ToServer.width+0.5, height=ToServer.height+0.5, color=NODE3_COLOR).move_to(Node3)

        Circuit.add(R1, R2).to_edge(UP)

        self.add(Circuit)

        MyPacket2 = DataPacket("N2", "N3", "Contenido", fromColor=NODE2_COLOR, toColor=NODE3_COLOR, contentColor=WHITE)
        MyPacket2.asRectangle.scale(1.5).shift(DOWN)
        MyPacket2.content.set_opacity(0)

        EncryptedPacket1 = VGroup(Rectangle(width=MyPacket2.contentRectangle.width, height=MyPacket2.contentRectangle.height).set_fill(GREY, opacity=1)).move_to(MyPacket2.asRectangle.get_center())
        Key3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=0.75).scale(0.5).move_to(EncryptedPacket1.get_center())
        EncryptedPacket1 += Key3
        self.add(EncryptedPacket1, MyPacket2.asRectangle)

        self.wait(14)

        Key2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=0.75).scale(0.5).move_to(Key3.get_center())

        self.play(MyPacket2.fromRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket2.contentRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket2.toRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket2.content.animate.set_opacity(0), MyPacket2.isFrom.animate.set_opacity(0), MyPacket2.to.animate.set_opacity(0),
                  Write(Key2), FadeOut(Key3))

        self.wait(3)

        MyPacket3 = DataPacket("N1", "N2", "Contenido", fromColor=NODE1_COLOR, toColor=NODE2_COLOR, contentColor=WHITE)
        MyPacket3.asRectangle.scale(1.5).shift(DOWN)
        MyPacket3.content.set_opacity(0)

        EncryptedPacket2 = VGroup(Rectangle(width=MyPacket3.contentRectangle.width, height=MyPacket3.contentRectangle.height).set_fill(GREY, opacity=1)).move_to(MyPacket2.asRectangle.get_center())

        self.play(Write(MyPacket3.asRectangle), Node3.animate.set_opacity(0.5), Node1.animate.set_opacity(1),
        R1.animate.move_to(Node1.get_center()).set_color(NODE1_COLOR),
        R2.animate.move_to(Node2.get_center()).set_color(NODE2_COLOR),
        Transform(MyPacket2.asRectangle, EncryptedPacket2))

    def EncryptionLayer3(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE
        FromComputer, ToServer = SVGMobject("../Images/Computer Icon.svg").scale(0.5).to_edge(LEFT), SVGMobject("../Images/Server Icon.svg").scale(0.5).to_edge(RIGHT)

        Node1, Node2, Node3 = SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5)
        Node1.next_to(FromComputer, RIGHT).shift(2*RIGHT)
        Node2.move_to(CENTER)
        Node3.next_to(ToServer, LEFT).shift(2*LEFT)

        C1, C2 = Line(FromComputer.get_center(), Node1.get_center(), z_index=-1), Line(Node1.get_center(), Node2.get_center(), z_index=-1)
        C3, C4 = Line(Node2.get_center(), Node3.get_center(), z_index=-1), Line(Node3.get_center(), ToServer.get_center(), z_index=-1)
        Connections = VGroup(C1, C2, C3, C4)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.15).move_to(Node1)
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.15).move_to(Node2)
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.15).move_to(Node3)

        T1, T2, T3 = Tex("N1").set_color(NODE1_COLOR).scale(0.75).next_to(Node1, UP), Tex("N2").set_color(NODE2_COLOR).scale(0.75).next_to(Node2, UP), Tex("N3").scale(0.75).set_color(NODE3_COLOR).next_to(Node3, UP)
        Node1, Node2, Node3 = VGroup(Node1, T1, K1), VGroup(Node2, T2, K2), VGroup(Node3, T3, K3)
        Nodes = VGroup(Node1, Node2, Node3)

        TA, TB = Tex("A").set_color(COMPUTER_COLOR).next_to(FromComputer, UP), Tex("B").set_color(SERVER_COLOR).next_to(ToServer, UP)
        FromComputer, ToServer = VGroup(FromComputer, TA), VGroup(ToServer, TB)
        Computers = VGroup(FromComputer, ToServer)

        Connections.set_opacity(0.5)
        Nodes.set_opacity(0.5)
        Computers.set_opacity(0.5)

        Node1.set_opacity(1)
        Node2.set_opacity(1)

        Circuit = VGroup(Connections, Nodes, Computers)

        R1 = Rectangle(width=FromComputer.width+0.5, height=FromComputer.height+0.5, color=NODE1_COLOR).move_to(Node1)
        R2 = Rectangle(width=ToServer.width+0.5, height=ToServer.height+0.5, color=NODE2_COLOR).move_to(Node2)

        Circuit.add(R1, R2).to_edge(UP)

        self.add(Circuit)

        MyPacket3 = DataPacket("N1", "N2", "Contenido", fromColor=NODE1_COLOR, toColor=NODE2_COLOR, contentColor=WHITE)
        MyPacket3.asRectangle.scale(1.5).shift(DOWN)
        MyPacket3.content.set_opacity(0)

        EncryptedPacket2 = VGroup(Rectangle(width=MyPacket3.contentRectangle.width, height=MyPacket3.contentRectangle.height).set_fill(GREY, opacity=1)).move_to(MyPacket3.asRectangle.get_center()).set_color(GREY)
        Key2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=0.75).scale(0.5).move_to(MyPacket3.content.get_center())
        EncryptedPacket2 += Key2

        self.add(MyPacket3.asRectangle, EncryptedPacket2)

        Key1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=0.75).scale(0.5).move_to(Key2.get_center())

        self.wait(3)

        self.play(MyPacket3.fromRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket3.contentRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket3.toRectangle.animate.set_fill(GREY, opacity=1).set_color(GREY),
                  MyPacket3.content.animate.set_opacity(0), MyPacket3.isFrom.animate.set_opacity(0), MyPacket3.to.animate.set_opacity(0),
                  Write(Key1), FadeOut(Key2))

        self.wait(1)

        MyPacket4 = DataPacket("N1", "N1", "Contenido", fromColor=COMPUTER_COLOR, toColor=NODE1_COLOR, contentColor=WHITE)
        MyPacket4.replaceSender("A")
        MyPacket4.asRectangle.scale(1.5).shift(DOWN)
        MyPacket4.content.set_opacity(0)

        EncryptedPacket3 = VGroup(Rectangle(width=MyPacket4.contentRectangle.width, height=MyPacket4.contentRectangle.height).set_fill(GREY, opacity=1)).move_to(MyPacket3.asRectangle.get_center())

        self.play(FadeIn(MyPacket4.asRectangle), Node2.animate.set_opacity(0.5), FromComputer.animate.set_opacity(1),
        R1.animate.move_to(FromComputer.get_center()).set_color(COMPUTER_COLOR),
        R2.animate.move_to(Node1.get_center()).set_color(NODE1_COLOR),
        Transform(MyPacket3.asRectangle, EncryptedPacket3))

        self.wait()

    def EncryptionConclusion(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE
        FromComputer, ToServer = SVGMobject("../Images/Computer Icon.svg").scale(0.5).to_edge(LEFT), SVGMobject("../Images/Server Icon.svg").scale(0.5).to_edge(RIGHT)

        Node1, Node2, Node3 = SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5), SVGMobject("../Images/Computer Icon.svg").scale(0.5)
        Node1.next_to(FromComputer, RIGHT).shift(2*RIGHT)
        Node2.move_to(CENTER)
        Node3.next_to(ToServer, LEFT).shift(2*LEFT)

        C1, C2 = Line(FromComputer.get_center(), Node1.get_center(), z_index=-1), Line(Node1.get_center(), Node2.get_center(), z_index=-1)
        C3, C4 = Line(Node2.get_center(), Node3.get_center(), z_index=-1), Line(Node3.get_center(), ToServer.get_center(), z_index=-1)
        Connections = VGroup(C1, C2, C3, C4)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.15).move_to(Node1)
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.15).move_to(Node2)
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.15).move_to(Node3)

        T1, T2, T3 = Tex("N1").set_color(NODE1_COLOR).scale(0.75).next_to(Node1, UP), Tex("N2").set_color(NODE2_COLOR).scale(0.75).next_to(Node2, UP), Tex("N3").scale(0.75).set_color(NODE3_COLOR).next_to(Node3, UP)
        Node1, Node2, Node3 = VGroup(Node1, T1, K1), VGroup(Node2, T2, K2), VGroup(Node3, T3, K3)
        Nodes = VGroup(Node1, Node2, Node3)

        TA, TB = Tex("A").set_color(COMPUTER_COLOR).next_to(FromComputer, UP), Tex("B").set_color(SERVER_COLOR).next_to(ToServer, UP)
        FromComputer, ToServer = VGroup(FromComputer, TA), VGroup(ToServer, TB)
        Computers = VGroup(FromComputer, ToServer)

        Connections.set_opacity(0.5)
        Nodes.set_opacity(1)
        Computers.set_opacity(1)

        Circuit = VGroup(Connections, Nodes, Computers)

        R1 = Rectangle(width=FromComputer.width+0.5, height=FromComputer.height+0.5, color=COMPUTER_COLOR).move_to(FromComputer)
        R2 = Rectangle(width=ToServer.width+0.5, height=ToServer.height+0.5, color=NODE1_COLOR).move_to(Node1)

        Circuit.add(R1, R2).move_to(CENTER)

        self.add(Circuit)

        self.wait()
        self.play(R1.animate.move_to(Node1).set_color(NODE1_COLOR), R2.animate.move_to(Node2).set_color(NODE2_COLOR))
        self.wait()
        self.play(R1.animate.move_to(Node2).set_color(NODE2_COLOR), R2.animate.move_to(Node3).set_color(NODE3_COLOR))
        self.wait()
        self.play(R1.animate.move_to(Node3).set_color(NODE3_COLOR), R2.animate.move_to(ToServer).set_color(SERVER_COLOR))
        self.wait()
        self.play(R1.animate.move_to(Node2).set_color(NODE2_COLOR), R2.animate.move_to(Node3).set_color(NODE3_COLOR))
        self.wait()
        self.play(R1.animate.move_to(Node1).set_color(NODE1_COLOR), R2.animate.move_to(Node2).set_color(NODE2_COLOR))
        self.wait()


    def ConstructScene(self, useAudio=True):
        # if useAudio: self.add_sound("../Audio/Lanzando una Petición-1.mp3")
        # self.EncryptionLayer1()

        # if useAudio: self.add_sound("../Audio/Lanzando una Petición-2.mp3")
        # self.EncryptionLayer2()

        # if useAudio: self.add_sound("../Audio/Lanzando una Petición-3.mp3")
        # self.EncryptionLayer3()

        if useAudio: self.add_sound("../Audio/Lanzando una Petición-4.mp3")
        self.EncryptionConclusion()

    def construct(self): self.ConstructScene()

class TransferingPacket(MovingCameraScene):
    def Layer1(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE

        Packet1 = DataPacket("XX", "XX", "Contenido", fromColor=COMPUTER_COLOR, toColor=NODE1_COLOR, contentColor=WHITE)
        Packet1.replaceComputers("A", "N1")
        Packet1.asRectangle.scale(1.5)
        Packet1.content.set_opacity(0)
        Packet1.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet1.asRectangle.to_edge(UP)

        Packet2 = DataPacket("XX", "XX", "Contenido", fromColor=NODE1_COLOR, toColor=NODE2_COLOR, contentColor=WHITE)
        Packet2.replaceComputers("N1", "N2")
        Packet2.asRectangle.scale(1.5)
        Packet2.content.set_opacity(0)
        Packet2.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet2.asRectangle.next_to(Packet1.asRectangle, DOWN).shift(2*DOWN)

        Packet3 = DataPacket("XX", "XX", "Contenido", fromColor=NODE2_COLOR, toColor=NODE3_COLOR, contentColor=WHITE)
        Packet3.replaceComputers("N2", "N3")
        Packet3.asRectangle.scale(1.5)
        Packet3.content.set_opacity(0)
        Packet3.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet3.asRectangle.next_to(Packet2.asRectangle, DOWN).shift(2*DOWN)

        Packet4 = DataPacket("XX", "XX", "Contenido", fromColor=NODE3_COLOR, toColor=SERVER_COLOR, contentColor=WHITE)
        Packet4.replaceComputers("N3", "B")
        Packet4.asRectangle.scale(1.5)
        Packet4.asRectangle.next_to(Packet3.asRectangle, DOWN).shift(2*DOWN)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.25).move_to(Packet1.asRectangle.get_center())
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.25).move_to(Packet2.asRectangle.get_center())
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.25).move_to(Packet3.asRectangle.get_center())

        Brace1 = VGroup(Line(Packet2.asRectangle.get_corner(UL), Packet1.contentRectangle.get_corner(DL)), Line(Packet2.asRectangle.get_corner(UR), Packet1.contentRectangle.get_corner(DR)))
        Brace2 = VGroup(Line(Packet3.asRectangle.get_corner(UL), Packet2.contentRectangle.get_corner(DL)), Line(Packet3.asRectangle.get_corner(UR), Packet2.contentRectangle.get_corner(DR)))
        Brace3 = VGroup(Line(Packet4.asRectangle.get_corner(UL), Packet3.contentRectangle.get_corner(DL)), Line(Packet4.asRectangle.get_corner(UR), Packet3.contentRectangle.get_corner(DR)))

        Keys = VGroup(K1, K2, K3)
        Packets = VGroup(Packet1.asRectangle, Packet2.asRectangle, Packet3.asRectangle, Packet4.asRectangle)
        Braces = VGroup(Brace1, Brace2, Brace3)

        self.camera.frame.move_to(Packet1.asRectangle.get_center())
        self.camera.frame.save_state()

        self.play(Write(Keys), Write(Packets), Write(Braces))

        self.wait(8)
        self.play(self.camera.frame.animate.move_to(Packet2.asRectangle.get_center()))
        self.wait()
        # self.play(self.camera.frame.animate.move_to(Packet3.asRectangle.get_center()))
        # self.wait()
        # self.play(self.camera.frame.animate.move_to(Packet4.asRectangle.get_center()))
        # self.wait()

        # self.play(Restore(self.camera.frame))

    def Layer2(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE

        Packet1 = DataPacket("XX", "XX", "Contenido", fromColor=COMPUTER_COLOR, toColor=NODE1_COLOR, contentColor=WHITE)
        Packet1.replaceComputers("A", "N1")
        Packet1.asRectangle.scale(1.5)
        Packet1.content.set_opacity(0)
        Packet1.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet1.asRectangle.to_edge(UP)

        Packet2 = DataPacket("XX", "XX", "Contenido", fromColor=NODE1_COLOR, toColor=NODE2_COLOR, contentColor=WHITE)
        Packet2.replaceComputers("N1", "N2")
        Packet2.asRectangle.scale(1.5)
        Packet2.content.set_opacity(0)
        Packet2.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet2.asRectangle.next_to(Packet1.asRectangle, DOWN).shift(2*DOWN)

        Packet3 = DataPacket("XX", "XX", "Contenido", fromColor=NODE2_COLOR, toColor=NODE3_COLOR, contentColor=WHITE)
        Packet3.replaceComputers("N2", "N3")
        Packet3.asRectangle.scale(1.5)
        Packet3.content.set_opacity(0)
        Packet3.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet3.asRectangle.next_to(Packet2.asRectangle, DOWN).shift(2*DOWN)

        Packet4 = DataPacket("XX", "XX", "Contenido", fromColor=NODE3_COLOR, toColor=SERVER_COLOR, contentColor=WHITE)
        Packet4.replaceComputers("N3", "B")
        Packet4.asRectangle.scale(1.5)
        Packet4.asRectangle.next_to(Packet3.asRectangle, DOWN).shift(2*DOWN)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.25).move_to(Packet1.asRectangle.get_center())
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.25).move_to(Packet2.asRectangle.get_center())
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.25).move_to(Packet3.asRectangle.get_center())

        Brace1 = VGroup(Line(Packet2.asRectangle.get_corner(UL), Packet1.contentRectangle.get_corner(DL)), Line(Packet2.asRectangle.get_corner(UR), Packet1.contentRectangle.get_corner(DR)))
        Brace2 = VGroup(Line(Packet3.asRectangle.get_corner(UL), Packet2.contentRectangle.get_corner(DL)), Line(Packet3.asRectangle.get_corner(UR), Packet2.contentRectangle.get_corner(DR)))
        Brace3 = VGroup(Line(Packet4.asRectangle.get_corner(UL), Packet3.contentRectangle.get_corner(DL)), Line(Packet4.asRectangle.get_corner(UR), Packet3.contentRectangle.get_corner(DR)))

        Keys = VGroup(K1, K2, K3)
        Packets = VGroup(Packet1.asRectangle, Packet2.asRectangle, Packet3.asRectangle, Packet4.asRectangle)
        Braces = VGroup(Brace1, Brace2, Brace3)

        self.camera.frame.move_to(Packet1.asRectangle.get_center())
        self.camera.frame.save_state()

        self.add(Keys, Packets, Braces)

        self.camera.frame.move_to(Packet2.asRectangle.get_center())
        self.wait(6)
        self.play(self.camera.frame.animate.move_to(Packet3.asRectangle.get_center()))
        # self.wait()
        # self.play(self.camera.frame.animate.move_to(Packet4.asRectangle.get_center()))
        # self.wait()

        # self.play(Restore(self.camera.frame))

    def Layer3(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE

        Packet1 = DataPacket("XX", "XX", "Contenido", fromColor=COMPUTER_COLOR, toColor=NODE1_COLOR, contentColor=WHITE)
        Packet1.replaceComputers("A", "N1")
        Packet1.asRectangle.scale(1.5)
        Packet1.content.set_opacity(0)
        Packet1.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet1.asRectangle.to_edge(UP)

        Packet2 = DataPacket("XX", "XX", "Contenido", fromColor=NODE1_COLOR, toColor=NODE2_COLOR, contentColor=WHITE)
        Packet2.replaceComputers("N1", "N2")
        Packet2.asRectangle.scale(1.5)
        Packet2.content.set_opacity(0)
        Packet2.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet2.asRectangle.next_to(Packet1.asRectangle, DOWN).shift(2*DOWN)

        Packet3 = DataPacket("XX", "XX", "Contenido", fromColor=NODE2_COLOR, toColor=NODE3_COLOR, contentColor=WHITE)
        Packet3.replaceComputers("N2", "N3")
        Packet3.asRectangle.scale(1.5)
        Packet3.content.set_opacity(0)
        Packet3.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet3.asRectangle.next_to(Packet2.asRectangle, DOWN).shift(2*DOWN)

        Packet4 = DataPacket("XX", "XX", "Contenido", fromColor=NODE3_COLOR, toColor=SERVER_COLOR, contentColor=WHITE)
        Packet4.replaceComputers("N3", "B")
        Packet4.asRectangle.scale(1.5)
        Packet4.asRectangle.next_to(Packet3.asRectangle, DOWN).shift(2*DOWN)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.25).move_to(Packet1.asRectangle.get_center())
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.25).move_to(Packet2.asRectangle.get_center())
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.25).move_to(Packet3.asRectangle.get_center())

        Brace1 = VGroup(Line(Packet2.asRectangle.get_corner(UL), Packet1.contentRectangle.get_corner(DL)), Line(Packet2.asRectangle.get_corner(UR), Packet1.contentRectangle.get_corner(DR)))
        Brace2 = VGroup(Line(Packet3.asRectangle.get_corner(UL), Packet2.contentRectangle.get_corner(DL)), Line(Packet3.asRectangle.get_corner(UR), Packet2.contentRectangle.get_corner(DR)))
        Brace3 = VGroup(Line(Packet4.asRectangle.get_corner(UL), Packet3.contentRectangle.get_corner(DL)), Line(Packet4.asRectangle.get_corner(UR), Packet3.contentRectangle.get_corner(DR)))

        Keys = VGroup(K1, K2, K3)
        Packets = VGroup(Packet1.asRectangle, Packet2.asRectangle, Packet3.asRectangle, Packet4.asRectangle)
        Braces = VGroup(Brace1, Brace2, Brace3)

        self.camera.frame.move_to(Packet1.asRectangle.get_center())
        self.camera.frame.save_state()

        self.add(Keys, Packets, Braces)

        self.camera.frame.move_to(Packet2.asRectangle.get_center())
        self.camera.frame.move_to(Packet3.asRectangle.get_center())
        self.wait(2)
        self.play(self.camera.frame.animate.move_to(Packet4.asRectangle.get_center()))
        # self.wait()

        # self.play(Restore(self.camera.frame))

    def ConstructScene(self, useAudio=True):
        # if useAudio: self.add_sound("../Audio/Transferir el Paquete-2.mp3")
        # self.Layer1()

        # if useAudio: self.add_sound("../Audio/Transferir el Paquete-3.mp3")
        # self.Layer2()

        if useAudio: self.add_sound("../Audio/Transferir el Paquete-4.mp3")
        self.Layer3()

    def construct(self): self.ConstructScene()

class Ending(MovingCameraScene):
    def Layers(self):
        COMPUTER_COLOR, SERVER_COLOR = RED, BLUE
        NODE1_COLOR, NODE2_COLOR, NODE3_COLOR = YELLOW, GREEN, ORANGE

        Packet1 = DataPacket("XX", "XX", "Contenido", fromColor=COMPUTER_COLOR, toColor=NODE1_COLOR, contentColor=WHITE)
        Packet1.replaceComputers("A", "N1")
        Packet1.asRectangle.scale(1.5)
        Packet1.content.set_opacity(0)
        Packet1.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet1.asRectangle.to_edge(UP)

        Packet2 = DataPacket("XX", "XX", "Contenido", fromColor=NODE1_COLOR, toColor=NODE2_COLOR, contentColor=WHITE)
        Packet2.replaceComputers("N1", "N2")
        Packet2.asRectangle.scale(1.5)
        Packet2.content.set_opacity(0)
        Packet2.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet2.asRectangle.next_to(Packet1.asRectangle, DOWN).shift(2*DOWN)

        Packet3 = DataPacket("XX", "XX", "Contenido", fromColor=NODE2_COLOR, toColor=NODE3_COLOR, contentColor=WHITE)
        Packet3.replaceComputers("N2", "N3")
        Packet3.asRectangle.scale(1.5)
        Packet3.content.set_opacity(0)
        Packet3.contentRectangle.set_fill(GREY, opacity=0.5)
        Packet3.asRectangle.next_to(Packet2.asRectangle, DOWN).shift(2*DOWN)

        Packet4 = DataPacket("XX", "XX", "Contenido", fromColor=NODE3_COLOR, toColor=SERVER_COLOR, contentColor=WHITE)
        Packet4.replaceComputers("N3", "B")
        Packet4.asRectangle.scale(1.5)
        Packet4.asRectangle.next_to(Packet3.asRectangle, DOWN).shift(2*DOWN)

        K1 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE1_COLOR, opacity=1).scale(0.25).move_to(Packet1.asRectangle.get_center())
        K2 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE2_COLOR, opacity=1).scale(0.25).move_to(Packet2.asRectangle.get_center())
        K3 = SVGMobject("../Images/Yellow Key.svg").set_fill(NODE3_COLOR, opacity=1).scale(0.25).move_to(Packet3.asRectangle.get_center())

        Brace1 = VGroup(Line(Packet2.asRectangle.get_corner(UL), Packet1.contentRectangle.get_corner(DL)), Line(Packet2.asRectangle.get_corner(UR), Packet1.contentRectangle.get_corner(DR)))
        Brace2 = VGroup(Line(Packet3.asRectangle.get_corner(UL), Packet2.contentRectangle.get_corner(DL)), Line(Packet3.asRectangle.get_corner(UR), Packet2.contentRectangle.get_corner(DR)))
        Brace3 = VGroup(Line(Packet4.asRectangle.get_corner(UL), Packet3.contentRectangle.get_corner(DL)), Line(Packet4.asRectangle.get_corner(UR), Packet3.contentRectangle.get_corner(DR)))

        Keys = VGroup(K1, K2, K3)
        Packets = VGroup(Packet1.asRectangle, Packet2.asRectangle, Packet3.asRectangle, Packet4.asRectangle)
        Braces = VGroup(Brace1, Brace2, Brace3)

        self.camera.frame.move_to(Packet1.asRectangle.get_center())
        self.camera.frame.save_state()

        self.add(Keys, Packets, Braces)

        self.camera.frame.move_to(Packet2.asRectangle.get_center())
        self.camera.frame.move_to(Packet3.asRectangle.get_center())
        self.camera.frame.move_to(Packet4.asRectangle.get_center())

        self.wait()

        self.play(self.camera.frame.animate.move_to(Packets.get_center()), run_time=2)

        self.wait()

        self.play(self.camera.frame.animate.scale(2))

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("../Audio/Conclusión-1.mp3")
        self.Layers()

    def construct(self): self.ConstructScene()
