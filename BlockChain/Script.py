from manim import *
from manim.mobject.geometry import ArrowTriangleTip, ArrowSquareTip, ArrowSquareFilledTip, ArrowCircleTip, ArrowCircleFilledTip
from numpy.random import randint as RND
import time
import hashlib
import os
from copy import deepcopy

# ManimCE Version 0.4.0
# 1920x1080 60FPS

PixelWidth = config.pixel_width = 1920
PixelHeight = config.pixel_height = 1080
FPS = config.frame_rate = 60

print(f"Rendering ManimCE (0.4.0) at {PixelWidth}x{PixelHeight} {FPS}FPS.")

ScreenX, ScreenY = (-7, 7), (-3.9, 3.9)

def CreateRectEquation(x1, y1, x2, y2): # De dos puntos, devolvemos la recta que pasa por (x1, y1), (x2, y2).
    m = (y1 - y2) / (x1 - x2)
    n = y1 - m*x1
    return lambda x: m*x+n

def SHA256Encode(toEncode, splitBy=1):
    EncodedString = hashlib.sha256(toEncode.encode()).hexdigest().upper()
    return EncodedString[:(len(EncodedString)//splitBy)]

def toBinary(toConvert): return ''.join(format(ord(i), '08b') for i in toConvert)

N = 10
X = (0, N, 1) # Min, Max, Step Size
Y = (0, N, 1) # Min, Max, Step Size
class Introduction(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(self,
        x_min = X[0],
        x_max = X[1],
        y_min = Y[0],
        y_max = Y[1],
        y_tick_frequency = X[2],
        x_tick_frequency = Y[2],
        x_labeled_nums = np.arange(X[0], X[1]+1, 5),
        y_labeled_nums = np.arange(Y[0], Y[1]+1, 5),
        x_label_direction = DOWN,
        y_label_direction = UP,
        x_axis_visibility = True,
        y_axis_visibility = True,
        graph_origin = np.array([-7, -3.5, 0]),
        x_axis_label = '',
        y_axis_label = '')

    def CoinGIF(self, nTimes=1, waitTime=0.15):
        """ Para llamar a esta función: self.CoinGIF(N1, N2)
        Esta función crea una moneda en el centro de la pantalla.
        La moneda tiene 6 fases, que sirven para simular la rotación.
        El número de rotaciones es el valor de nTimes, que por defecto es una rotación.
        El tiempo entre cada fase se puede elegir con waitTime, que por defecto son 0.15s.
        """
        CoinPhases = [ImageMobject(f"Images/Coin{i+1}.png").scale(0.25) for i in range(6)] # Nuestra moneda tiene 6 fotogramas distintos.
        for _ in range(nTimes): # Repetimos la rotación 10 veces.
            for Coin in CoinPhases:
                self.add(Coin)
                self.wait(waitTime)
                self.remove(Coin)

        self.play(FadeOut(Coin))

    def SatoshiName_BitCoinDefinition(self):
        """
        En 2008 un usuario llamado Satoshi Nakamoto, publicó un paper en el que hablaba sobre el BitCoin,
        una forma de dinero electrónico basada en el Peer-to-Peer.
        """
        Year = Tex("2008")
        SatoshiName = Tex("Satoshi", " Nakamoto")
        SatoshiName[0].set_color(GREEN)
        SatoshiName[1].set_color(RED)
        IncognitoMan = SVGMobject("Images/IncognitoMan.svg")
        IncognitoMan.set_color(WHITE)
        SatoshiName.next_to(IncognitoMan, UP, buff=0.5)
        Year.next_to(IncognitoMan, DOWN, buff=0.5)

        self.play(DrawBorderThenFill(IncognitoMan), Write(SatoshiName), Write(Year), run_time=4)
        self.wait(2)

        BitCoinDefinition = Tex("BitCoin", ": ", "Una forma de ", "dinero electrónico ", "basada en el ", "Peer-to-Peer", ".")
        BitCoinDefinition[0].set_color(ORANGE)
        BitCoinDefinition[1].set_color(GREY)
        BitCoinDefinition[2].set_color(GREY)
        BitCoinDefinition[3].set_color(YELLOW)
        BitCoinDefinition[4].set_color(GREY)
        BitCoinDefinition[5].set_color(BLUE)
        BitCoinDefinition[6].set_color(GREY)
        BitCoinDefinition.scale(0.8)
        BitCoinDefinition.to_corner(UP)
        BitCoinDefinition.shift(np.array([0, -0.5, 0]))
        self.play(Write(BitCoinDefinition), SatoshiName.animate.shift(0.35*DOWN), IncognitoMan.animate.shift(0.35*DOWN), Year.animate.shift(0.35*DOWN), run_time=3)

        self.wait()

        self.play(Uncreate(IncognitoMan), Uncreate(SatoshiName), Uncreate(Year), Uncreate(BitCoinDefinition))

    def Centralized_Descentralized(self):
        """
        Esta moneda permitiría hacer pagos online directamente entre los usuarios sin pasar a través de una
        institución financiera central.
        """
        Bank = SVGMobject("Images/Bank.svg").to_corner(UP).scale(0.75)
        RedUser = SVGMobject("Images/RedUser.svg").to_corner(DOWN).scale(0.75)
        GreenUser = SVGMobject("Images/GreenUser.svg").to_corner(RIGHT+DOWN).scale(0.75)
        BlueUser = SVGMobject("Images/BlueUser.svg").to_corner(LEFT+DOWN).scale(0.75)

        # Blue pays one coin to red.
        # Red pays two coins to green.
        Coin1 = ImageMobject("Images/Coin1.png").scale(0.25).next_to(BlueUser, DOWN, buff=-0.15) # Coin1 goes from BlueUser to RedUser, then from RedUser to GreenUser.
        Coin2 = ImageMobject("Images/Coin1.png").scale(0.25).next_to(RedUser, DOWN, buff=-0.15) # Coin2 goes from RedUser to GreenUser.
        Transaction1 = Tex("Mr.Azul ", "paga una moneda a ", "Mr.Rojo.").scale(0.5).to_corner(UL)
        Transaction2 = Tex("Mr.Rojo ", "paga dos monedas a ","Mr.Verde.").scale(0.5).to_corner(UL)
        Transaction1[0].set_color(BLUE)
        Transaction1[2].set_color(RED)
        Transaction2[0].set_color(RED)
        Transaction2[2].set_color(GREEN)

        CentralizedText = Tex("Sistema Centralizado.").scale(0.75).to_corner(UR)
        DescentralizedText = Tex("Sistema Descentralizado.").scale(0.75).to_corner(UR)
        BankBlue_Connection = Line(BlueUser.get_center(), Bank.get_center())
        BankGreen_Connection = Line(GreenUser.get_center(), Bank.get_center())
        BankRed_Connection = Line(RedUser.get_center(), Bank.get_center())


        self.play(Write(BankBlue_Connection), Write(BankGreen_Connection), Write(BankRed_Connection), # Las conexiones del banco a cada usuario.
                  FadeIn(BlueUser), FadeIn(GreenUser), FadeIn(RedUser), FadeIn(Bank),  # Los iconos de Usuario y Banco.
                  FadeIn(Coin1), FadeIn(Coin2), Write(CentralizedText), run_time=0.5) # El dinero de cada usuario.

        self.play(Coin1.animate.move_to(Bank), Write(Transaction1), run_time=0.5)
        self.play(Coin1.animate.move_to(RedUser), run_time=0.5)

        self.play(Coin1.animate.move_to(Bank), Coin2.animate.move_to(Bank), Transform(Transaction1, Transaction2), run_time=0.5)
        self.play(Coin1.animate.move_to(GreenUser.get_center()+DOWN+0.5*RIGHT), Coin2.animate.move_to(GreenUser.get_center()+DOWN+0.5*LEFT), run_time=0.5)

        self.play(Uncreate(Bank), Uncreate(BankRed_Connection), Uncreate(BankBlue_Connection), Uncreate(BankGreen_Connection),
                  RedUser.animate.to_corner(UP), FadeOut(Transaction1), Transform(CentralizedText, DescentralizedText))

        Transaction1 = Tex("Mr.Azul ", "paga una moneda a ", "Mr.Rojo.").scale(0.5).to_corner(UL)
        Transaction2 = Tex("Mr.Rojo ", "paga dos monedas a ","Mr.Verde.").scale(0.5).to_corner(UL)
        Transaction1[0].set_color(BLUE)
        Transaction1[2].set_color(RED)
        Transaction2[0].set_color(RED)
        Transaction2[2].set_color(GREEN)
        BlueRed_Connection = Line(BlueUser.get_center(), RedUser.get_center())
        GreenRed_Connection = Line(GreenUser.get_center(), RedUser.get_center())
        BlueGreen_Connection = Line(BlueUser.get_center(), GreenUser.get_center())

        self.bring_to_back(BlueRed_Connection, GreenRed_Connection, BlueGreen_Connection)
        self.play(Write(BlueRed_Connection), Write(GreenRed_Connection), Write(BlueGreen_Connection), Coin1.animate.next_to(BlueUser, DOWN, buff=-0.15), Coin2.animate.next_to(RedUser, UP, buff=-0.15),
        Write(Transaction1), run_time=0.5)

        self.play(Coin1.animate.move_to(RedUser), run_time=0.5)
        self.play(Transform(Transaction1, Transaction2), run_time=0.25)
        self.play(Coin1.animate.move_to(GreenUser.get_center()+DOWN+0.5*RIGHT), Coin2.animate.move_to(GreenUser.get_center()+DOWN+0.5*LEFT), run_time=0.5)

        self.play(FadeOut(CentralizedText), FadeOut(Transaction1),
                  FadeOut(BlueUser), FadeOut(RedUser), FadeOut(GreenUser),
                  FadeOut(Coin1), FadeOut(Coin2),
                  Uncreate(BlueRed_Connection), Uncreate(GreenRed_Connection), Uncreate(BlueGreen_Connection))

    def NotBitCoin_BlockChain(self):
        """
        En este vídeo no nos centraremos directamente en el BitCoin, sino en el concepto de BlockChain y
        la tecnología que hay detrás de todas las criptomonedas.
        Veremos conceptos como el de Peer-to-Peer, Proof-of-Work y la Función de Hash.
        """
        BTC = SVGMobject("Images/BitCoin.svg")

        Block, Chain = Tex("BLOCK").to_corner(LEFT), Tex("CHAIN").to_corner(RIGHT)
        Block.set_color(ORANGE)
        Chain.set_color(GREY)

        self.play(DrawBorderThenFill(BTC))
        self.play(Uncreate(BTC))

        self.play(Block.animate.shift(4.95*RIGHT), Chain.animate.shift(4.95*LEFT))
        self.play(Block.animate.to_edge(UP), Chain.animate.to_edge(UP))

        self.setup_axes(animate=True)
        MyGraph1 = self.get_graph(lambda x: np.log(x**2), color=GREEN, x_min=.01, x_max=N)
        MyGraph2 = self.get_graph(lambda x: 2*np.cos(.5*x)+8, color=RED, x_min=.01, x_max=N)
        MyGraph3 = self.get_graph(lambda x: np.sqrt(x), color=ORANGE, x_min=.01, x_max=N)
        MyGraph4 = self.get_graph(lambda x: x + np.tan(np.sin(x)), color=BLUE, x_min=.01, x_max=N)
        self.bring_to_back(MyGraph1, MyGraph2, MyGraph3, MyGraph4)
        self.play(ShowCreation(MyGraph1), ShowCreation(MyGraph2), ShowCreation(MyGraph3), ShowCreation(MyGraph4))

        BinaryBlocks = []
        Blocks = 5
        DigitsPerBlock = 15
        for i in range(Blocks):
            BinaryString = ""
            for j in range(DigitsPerBlock):
                BinaryString += str(np.random.choice([0, 1]))
            Binary = Tex(BinaryString).to_edge(UR).shift(2*i*(.85*DOWN))
            self.play(Write(Binary), run_time=0.5)
            BinaryBlocks.append(Binary)

        self.play(Uncreate(MyGraph1), Uncreate(MyGraph2), Uncreate(MyGraph3), Uncreate(MyGraph4),
        FadeOut(BinaryBlocks[0]), FadeOut(BinaryBlocks[1]), FadeOut(BinaryBlocks[2]), FadeOut(BinaryBlocks[3]), FadeOut(BinaryBlocks[4]),
        FadeOut(Block), FadeOut(Chain), Uncreate(self.axes), run_time=2)

    def SourcesOnDescription(self):
        """
        Antes de empezar con las explicaciones, en la descripción del vídeo tenéis una lista de documentos
        de donde he sacado la información de este vídeo. El más importante de todos es el propio paper que
        publicó Satoshi Nakamoto en 2008, explicando como funciona el BitCoin.
        """
        Document = SVGMobject("Images/Document.svg")
        PaperTitle = Tex("BitCoin: ", "Peer-to-Peer", " Electronic Cash System", " (2008)").to_edge(UP)
        PaperTitle[0].set_color(ORANGE)
        PaperTitle[1].set_color(BLUE)
        PaperTitle[2].set_color(YELLOW)
        self.play(FadeIn(Document))
        self.play(Document.animate.scale(1.5))
        for _ in range(2):
            self.play(Document.animate.rotate(-10*DEGREES))
            self.play(Document.animate.rotate(+10*DEGREES))
            self.play(Document.animate.rotate(-10*DEGREES))
            self.play(Document.animate.rotate(+10*DEGREES))
        self.play(Write(PaperTitle), run_time=3)

        self.wait(0.5)

        self.play(Uncreate(Document), Uncreate(PaperTitle), run_time=1.5)

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("Audio/AudioIntroduction.mp3")

        self.SatoshiName_BitCoinDefinition()

        self.Centralized_Descentralized()

        self.NotBitCoin_BlockChain()

        self.SourcesOnDescription()

    def construct(self): self.ConstructScene()

class CryptoCurrencyConcept(Scene):
    def CentralizedSystem(self):
        """
        Esta moneda permitiría hacer pagos online directamente entre los usuarios sin pasar a través de una
        institución financiera central.
        """
        Bank = SVGMobject("Images/Bank.svg").to_corner(UP).scale(0.75).shift(0.75*DOWN)
        RedUser = SVGMobject("Images/RedUser.svg").to_corner(DOWN).scale(0.75)
        GreenUser = SVGMobject("Images/GreenUser.svg").to_corner(RIGHT+DOWN).scale(0.75)
        BlueUser = SVGMobject("Images/BlueUser.svg").to_corner(LEFT+DOWN).scale(0.75)

        # Blue pays one coin to red.
        # Red pays two coins to green.
        Coin1 = ImageMobject("Images/Coin1.png").scale(0.25).next_to(BlueUser, DOWN, buff=-0.15) # Coin1 goes from BlueUser to RedUser, then from RedUser to GreenUser.
        Coin2 = ImageMobject("Images/Coin1.png").scale(0.25).next_to(RedUser, DOWN, buff=-0.15) # Coin2 goes from RedUser to GreenUser.
        Transaction1 = Tex("Mr.Azul ", "paga una moneda a ", "Mr.Rojo.").scale(0.5).to_corner(UL)
        Transaction2 = Tex("Mr.Rojo ", "paga dos monedas a ","Mr.Verde.").scale(0.5).to_corner(UL)
        Transaction1[0].set_color(BLUE)
        Transaction1[2].set_color(RED)
        Transaction2[0].set_color(RED)
        Transaction2[2].set_color(GREEN)

        CentralizedText = Tex("Sistema Centralizado").scale(0.75).to_corner(UP)
        BankBlue_Connection = Line(BlueUser.get_center(), Bank.get_center())
        BankGreen_Connection = Line(GreenUser.get_center(), Bank.get_center())
        BankRed_Connection = Line(RedUser.get_center(), Bank.get_center())

        self.play(Write(BankBlue_Connection), Write(BankGreen_Connection), Write(BankRed_Connection), # Las conexiones del banco a cada usuario.
        FadeIn(BlueUser), FadeIn(GreenUser), FadeIn(RedUser), FadeIn(Bank),  # Los iconos de Usuario y Banco.
        FadeIn(Coin1), FadeIn(Coin2), Write(CentralizedText)) # El dinero de cada usuario.

        self.play(Coin1.animate.move_to(Bank), Write(Transaction1))
        self.play(Coin1.animate.move_to(RedUser))

        self.play(Coin1.animate.move_to(Bank), Coin2.animate.move_to(Bank), Transform(Transaction1, Transaction2))
        self.play(Coin1.animate.move_to(GreenUser.get_center()+DOWN+0.5*RIGHT), Coin2.animate.move_to(GreenUser.get_center()+DOWN+0.5*LEFT))


        self.play(Bank.animate.move_to(np.array([0,0,0])), Uncreate(BankRed_Connection), Uncreate(BankBlue_Connection), Uncreate(BankGreen_Connection), FadeOut(Transaction1),
                  FadeOut(RedUser), GreenUser.animate.to_edge(RIGHT).shift(2.5*UP), BlueUser.animate.to_edge(LEFT).shift(2.5*UP), Uncreate(CentralizedText),
                  FadeOut(Coin1), FadeOut(Coin2))

        Coin1 = Coin1.next_to(BlueUser, DOWN+0.5*LEFT, buff=-0.15)
        Coin2 = Coin2.next_to(BlueUser, DOWN, buff=-0.15)
        Coin3 = ImageMobject("Images/Coin1.png").scale(0.25).next_to(BlueUser, DOWN+0.5*RIGHT, buff=-0.15)
        SilverCoin1 = ImageMobject("Images/SilverCoin.png").scale(0.20).next_to(Coin2, DOWN+0.15*LEFT, buff=-0.15)
        SilverCoin2 = ImageMobject("Images/SilverCoin.png").scale(0.20).next_to(Coin2, DOWN+0.15*RIGHT, buff=-0.15)
        BankBlue_Connection = Line(BlueUser.get_center(), Bank.get_center())
        BankGreen_Connection = Line(GreenUser.get_center(), Bank.get_center())
        self.bring_to_back(BankBlue_Connection, BankGreen_Connection)
        self.play(Write(BankBlue_Connection), Write(BankGreen_Connection),
        FadeIn(Coin1), FadeIn(Coin2), FadeIn(Coin3), FadeIn(SilverCoin1), FadeIn(SilverCoin2))

        Transaction = Tex("Mr.Azul ", "paga dos monedas a ", "Mr.Verde.").to_edge(UP)
        TransactionCost = Tex("La administración del pago tiene un", " coste ", "de una moneda de plata.").next_to(Transaction, DOWN).scale(0.75)
        TransactionCost[1].set_color(RED)
        Transaction[0].set_color(BLUE)
        Transaction[2].set_color(GREEN)
        self.play(Write(Transaction), Write(TransactionCost))
        self.play(Coin1.animate.shift(0.5*UP), Coin3.animate.shift(0.5*UP), SilverCoin1.animate.shift(0.5*UP))
        self.play(Coin1.animate.move_to(Bank), Coin3.animate.move_to(Bank), SilverCoin1.animate.move_to(Bank), run_time=2)
        self.play(Coin1.animate.next_to(GreenUser, DOWN+2.5*LEFT, buff=-0.15), Coin3.animate.next_to(GreenUser, DOWN+2.5*RIGHT, buff=-0.15),
        SilverCoin1.animate.next_to(Bank, DOWN, buff=-0.15), SilverCoin2.animate.next_to(Coin2, DOWN, buff=-0.15), run_time=2)

        self.play(Uncreate(Transaction), Uncreate(TransactionCost), run_time=0.5)

        Devil = SVGMobject("Images/Devil.svg").move_to(Bank.get_center())
        Exclamation1, Exclamation2 = Tex("! ! !").next_to(BlueUser, UP).set_color(RED), Tex("! ! !").next_to(GreenUser, UP).set_color(RED)
        self.play(Transform(Bank, Devil), FadeOut(SilverCoin1))
        self.bring_to_front(Devil)
        self.play(Coin1.animate.move_to(Bank.get_center()), Coin2.animate.move_to(Bank.get_center()), Coin3.animate.move_to(Bank.get_center()),
        SilverCoin2.animate.move_to(Bank.get_center()))
        self.play(Write(Exclamation1), Write(Exclamation2))

        EvilBank = Tex(">Qué hace el ", "banco ", "con nuestros " ,"datos", "?").to_edge(UP)
        EvilBank[1].set_color(RED) # banco
        EvilBank[3].set_color(ORANGE) # datos
        EvilBank[4].set_color(GREY) # ?

        self.play(Write(EvilBank))

        self.wait()
        self.remove(Coin1, Coin2, Coin3, SilverCoin1, SilverCoin2)
        self.play(FadeOut(EvilBank), FadeOut(Bank), FadeOut(Devil), Uncreate(Exclamation1), Uncreate(Exclamation2))

        Lock1, Lock2 = SVGMobject("Images/Lock.svg").scale(0.5), SVGMobject("Images/Lock.svg").scale(0.5)

        self.play(Lock1.animate.next_to(BlueUser, RIGHT, buff=0).shift(0.25*LEFT), Lock2.animate.next_to(GreenUser, LEFT, buff=0).shift(0.25*RIGHT))

        Coin1 = Coin1.next_to(BlueUser, DOWN+0.5*LEFT, buff=-0.15)
        Coin2 = Coin2.next_to(BlueUser, DOWN, buff=-0.15)
        Coin3 = Coin3.next_to(BlueUser, DOWN+0.5*RIGHT, buff=-0.15)

        EncryptedTransaction = Tex("2CD7557AD16E ", "paga dos monedas a ", "436871E7AD94").to_edge(UP).scale(0.75)
        EncryptedTransaction[0].set_color(BLUE)
        EncryptedTransaction[2].set_color(GREEN)
        self.play(FadeIn(Coin1), FadeIn(Coin2), FadeIn(Coin3))

        self.play(Write(Transaction))
        self.play(Transform(Transaction, EncryptedTransaction), Coin1.animate.next_to(GreenUser, DOWN+2.5*LEFT, buff=-0.15), Coin3.animate.next_to(GreenUser, DOWN+2.5*RIGHT, buff=-0.15))
        self.wait(2)
        self.play(FadeOut(GreenUser), FadeOut(BlueUser), FadeOut(Lock1), FadeOut(Lock2), FadeOut(Coin1), FadeOut(Coin2), FadeOut(Coin3), FadeOut(BankGreen_Connection), FadeOut(BankBlue_Connection),
        Uncreate(Transaction), Uncreate(EncryptedTransaction))

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("Audio/AudioCryptoCurrencyConcept.mp3")

        self.CentralizedSystem()

    def construct(self): self.ConstructScene()

class PeerToPeer(Scene):
    def PeerToPeerTittle(self):
        self.wait()
        self.LongTittle = Tex("Peer", "-", "to", "-", "Peer").scale(2)
        ShortTittle = Tex("P", "2", "P").scale(2)

        self.LongTittle[0].set_color(BLUE)
        self.LongTittle[1].set_color(GREY)
        self.LongTittle[2].set_color(GREEN)
        self.LongTittle[3].set_color(GREY)
        self.LongTittle[4].set_color(RED)

        ShortTittle[0].set_color(BLUE)
        ShortTittle[1].set_color(GREEN)
        ShortTittle[2].set_color(RED)

        self.play(Write(self.LongTittle), run_time=5)
        self.play(Transform(self.LongTittle, ShortTittle), run_time=1)
        self.play(self.LongTittle.animate.to_edge(UP).scale(0.75), run_time=1)
        Tittle = Tex("Peer", "-", "to", "-", "Peer").scale(1.25).to_edge(UP)
        Tittle[0].set_color(BLUE)
        Tittle[1].set_color(GREY)
        Tittle[2].set_color(GREEN)
        Tittle[3].set_color(GREY)
        Tittle[4].set_color(RED)
        self.play(Transform(self.LongTittle, Tittle), run_time=1)


    def DescentralizedNetwork(self):
        Computer1, Computer2, Computer3, Computer4 = SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg")
        # Computer1             Computer3
        #             Server
        # Computer2             Computer4
        Computer1.to_corner(UL).scale(0.5).shift(0.5*DOWN)
        Computer2.to_corner(DL).scale(0.5)
        Computer3.to_corner(UR).scale(0.5).shift(0.5*DOWN)
        Computer4.to_corner(DR).scale(0.5)
        Server = SVGMobject("Images/Server.svg").scale(0.5)

        LS1, LS2 = Line(Computer1.get_center(), Server.get_center()), Line(Computer2.get_center(), Server.get_center())
        LS3, LS4 = Line(Computer3.get_center(), Server.get_center()), Line(Computer4.get_center(), Server.get_center())
        self.bring_to_back(LS1, LS2, LS3, LS4)
        self.play(FadeIn(Server), FadeIn(Computer1), FadeIn(Computer2), FadeIn(Computer3), FadeIn(Computer4),
        Write(LS1), Write(LS2), Write(LS3), Write(LS4), run_time=2)

        self.play(FadeOut(Server), Uncreate(LS1), Uncreate(LS2), Uncreate(LS3), Uncreate(LS4), run_time=2)

        L12 = Line(Computer1.get_center(), Computer2.get_center())
        L13 = Line(Computer1.get_center(), Computer3.get_center())
        L14 = Line(Computer1.get_center(), Computer4.get_center())
        L23 = Line(Computer3.get_center(), Computer2.get_center())
        L24 = Line(Computer4.get_center(), Computer2.get_center())
        L34 = Line(Computer4.get_center(), Computer3.get_center())

        self.bring_to_back(L12, L13, L14, L23, L24, L34)

        self.play(Write(L12), Write(L13), Write(L14), Write(L23), Write(L24), Write(L34), run_time=4)

        self.play(FadeOut(Computer1), FadeOut(Computer2), FadeOut(Computer3), FadeOut(Computer4),
        FadeOut(L12), FadeOut(L13), FadeOut(L14), FadeOut(L23), FadeOut(L24), FadeOut(L34), FadeOut(self.LongTittle))

        self.wait(1.5)

    def TorrentProtocol(self):
        self.clear()
        BitTorrentLogo = SVGMobject("Images/BitTorrentLogo.svg")
        ProtocoloTorrent = Tex("Protocolo ", "Torrent").scale(1.5).to_edge(UP)
        ProtocoloTorrent[0].set_color("#673398")
        ProtocoloTorrent[1].set_color(GREEN)

        self.play(DrawBorderThenFill(BitTorrentLogo))
        self.play(BitTorrentLogo.animate.to_edge(UP))
        self.play(Transform(BitTorrentLogo, ProtocoloTorrent))

        Computer1, Computer2, Computer3, Computer4 = SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg")
        # Computer1             Computer3
        #             Server
        # Computer2             Computer4
        Computer1.to_corner(UL).scale(0.5).shift(0.5*DOWN)
        Computer2.to_corner(DL).scale(0.5)
        Computer3.to_corner(UR).scale(0.5).shift(0.5*DOWN)
        Computer4.to_corner(DR).scale(0.5)

        L12 = Line(Computer1.get_center(), Computer2.get_center())
        L13 = Line(Computer1.get_center(), Computer3.get_center())
        L14 = Line(Computer1.get_center(), Computer4.get_center())
        L23 = Line(Computer3.get_center(), Computer2.get_center())
        L24 = Line(Computer4.get_center(), Computer2.get_center())
        L34 = Line(Computer4.get_center(), Computer3.get_center())

        self.bring_to_back(L12, L13, L14, L23, L24, L34)

        self.play(FadeIn(Computer1), FadeIn(Computer2), FadeIn(Computer3), FadeIn(Computer4),
        Write(L12), Write(L13), Write(L14), Write(L23), Write(L24), Write(L34), run_time=2)

        DownloadInformation = Tex("Se quiere", " descargar", " un", " archivo.").scale(0.5).next_to(Computer1, RIGHT).shift(0.25*UP)
        DownloadInformation[1].set_color(GREEN)
        DownloadInformation[3].set_color("#4086ee")

        CompleteFile = ImageMobject("Images/File.png").scale(.25).move_to(Computer1)
        LeftFile, RightFile = ImageMobject("Images/LeftFile.png").scale(.25), ImageMobject("Images/RightFile.png").scale(.25)
        RandomPart = ImageMobject("Images/LeftFile.png").scale(.25)
        LeftFile.next_to(Computer3, RIGHT, buff=-0.15)
        RightFile.next_to(Computer4, RIGHT, buff=-0.15)
        RandomPart.next_to(Computer2, LEFT, buff=-0.15)

        self.play(Write(DownloadInformation), FadeIn(LeftFile), FadeIn(RightFile), FadeIn(RandomPart), run_time=2)

        self.wait(2)

        self.play(L13.animate.set_color(GREEN), L14.animate.set_color(GREEN), L12.animate.set_opacity(0.25), L23.animate.set_opacity(0.25), L24.animate.set_opacity(0.25), L34.animate.set_opacity(0.25))
        self.wait()
        self.play(RandomPart.animate.set_opacity(0.25), Computer2.animate.set_opacity(0.25), run_time=1.5)
        self.wait()
        self.play(LeftFile.animate.move_to(Computer1), RightFile.animate.move_to(Computer1), Uncreate(DownloadInformation), run_time=4)
        self.play(FadeIn(CompleteFile), FadeOut(LeftFile), FadeOut(RightFile), FadeOut(RandomPart))
        self.wait(2)
        self.play(FadeOut(CompleteFile), Computer2.animate.set_opacity(1),
        L13.animate.set_color(WHITE), L14.animate.set_color(WHITE), L12.animate.set_opacity(1), L23.animate.set_opacity(1), L24.animate.set_opacity(1), L34.animate.set_opacity(1))

        LinesList = [L12, L13, L14, L23, L24, L34]
        last, randomIndex = -1, -1
        for _ in range(3):
            while randomIndex == last: randomIndex = np.random.randint(0, len(LinesList))
            CurrentLine = LinesList[randomIndex]
            last = randomIndex
            self.play(CurrentLine.animate.set_color(GREEN))
            self.wait(0.25)
            self.play(CurrentLine.animate.set_color(WHITE))

        self.play(FadeOut(Computer1), FadeOut(Computer2), FadeOut(Computer3), FadeOut(Computer4),
        Uncreate(L12), Uncreate(L13), Uncreate(L14), Uncreate(L23), Uncreate(L24), Uncreate(L34), FadeOut(BitTorrentLogo))

    def TransactionsNetwork(self):
        NetworkTittle = Tex("Red ", "de ", "Transacciones").to_edge(UP).shift(0.25*DOWN)
        NetworkTittle[0].set_color(BLUE)
        NetworkTittle[2].set_color(ORANGE)

        Computer1, Computer2, Computer3, Computer4 = SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg"), SVGMobject("Images/Computer.svg")

        Computer1.to_corner(UL).scale(0.5).shift(0.5*DOWN)
        Computer2.to_corner(DL).scale(0.5)
        Computer3.to_corner(UR).scale(0.5).shift(0.5*DOWN)
        Computer4.to_corner(DR).scale(0.5)

        L12 = Line(Computer1.get_center(), Computer2.get_center())
        L13 = Line(Computer1.get_center(), Computer3.get_center())
        L14 = Line(Computer1.get_center(), Computer4.get_center())
        L23 = Line(Computer3.get_center(), Computer2.get_center())
        L24 = Line(Computer4.get_center(), Computer2.get_center())
        L34 = Line(Computer4.get_center(), Computer3.get_center())

        self.bring_to_back(L12, L13, L14, L23, L24, L34)

        Coin = ImageMobject("Images/Coin1.png").scale(0.25).move_to(Computer1)
        User1 = SVGMobject("Images/User.svg").scale(0.25).next_to(Computer1, LEFT, buff=-0.15).set_color(GREY)
        User2 = SVGMobject("Images/User.svg").scale(0.25).next_to(Computer2, LEFT, buff=-0.15).set_color(GREY)
        User3 = SVGMobject("Images/User.svg").scale(0.25).next_to(Computer3, RIGHT, buff=-0.15).set_color(GREY)
        User4 = SVGMobject("Images/User.svg").scale(0.25).next_to(Computer4, RIGHT, buff=-0.15).set_color(GREY)

        self.play(Write(NetworkTittle), FadeIn(Computer1), FadeIn(Computer2), FadeIn(Computer3), FadeIn(Computer4),
        Write(L12), Write(L13), Write(L14), Write(L23), Write(L24), Write(L34), run_time=2)

        self.wait(2)

        self.play(DrawBorderThenFill(User1), DrawBorderThenFill(User2), DrawBorderThenFill(User3), DrawBorderThenFill(User4))

        self.play(FadeIn(Coin))
        self.play(Coin.animate.move_to(Computer2))
        self.play(Coin.animate.move_to(Computer4))
        self.play(Coin.animate.move_to(Computer1))
        self.play(Coin.animate.move_to(Computer3))
        self.play(Coin.animate.move_to(Computer2))

        TransactionsLog = Rectangle(height=6, width=5).shift(0.5*DOWN).set_fill(GREY, opacity=0.85)

        self.play(Computer1.animate.set_opacity(0.25), Computer2.animate.set_opacity(0.25), Computer3.animate.set_opacity(0.25), Computer4.animate.set_opacity(0.25), FadeOut(Coin),
        L12.animate.set_opacity(0.25), L13.animate.set_opacity(0.25), L14.animate.set_opacity(0.25), L23.animate.set_opacity(0.25), L24.animate.set_opacity(0.25), L34.animate.set_opacity(0.25),
        ShowCreation(TransactionsLog), run_time=2)

        Transaction1 = Tex("Usuario 4", " paga 2 monedas a ", "Usuario 1.").scale(0.5).next_to(TransactionsLog, UP).shift(DOWN)
        Transaction2 = Tex("Usuario 1", " paga 3 monedas a ", "Usuario 2.").scale(0.5).next_to(Transaction1, 2*DOWN)
        Transaction3 = Tex("Usuario 1", " paga 5 monedas a ", "Usuario 4.").scale(0.5).next_to(Transaction2, 2*DOWN)
        Transaction4 = Tex("Usuario 3", " paga 4 monedas a ", "Usuario 2.").scale(0.5).next_to(Transaction3, 2*DOWN)
        Transaction5 = Tex("Usuario 2", " paga 5 monedas a ", "Usuario 4.").scale(0.5).next_to(Transaction4, 2*DOWN)
        Final = Tex(". . . . . . . . . . . .").scale(0.5).next_to(Transaction5, 2*DOWN)

        # Usuario 1 ---> GREEN
        # Usuario 2 ---> #ff676c
        # Usuario 3 ---> #YELLOW
        # Usuario 4 ---> #dd85ff


        Transaction1[0].set_color("#dd85ff")
        Transaction1[2].set_color(GREEN)

        Transaction2[0].set_color(GREEN)
        Transaction2[2].set_color("#ff676c")

        Transaction3[0].set_color(GREEN)
        Transaction3[2].set_color("#dd85ff")

        Transaction4[0].set_color(YELLOW)
        Transaction4[2].set_color("#ff676c")

        Transaction5[0].set_color("#ff676c")
        Transaction5[2].set_color("#dd85ff")

        self.play(Write(Transaction1), run_time=0.5)
        self.play(Write(Transaction2), run_time=0.5)
        self.play(Write(Transaction3), run_time=0.5)
        self.play(Write(Transaction4), run_time=0.5)
        self.play(Write(Transaction5), run_time=0.5)
        self.play(Write(Final), run_time=0.25)

        LogBrace = Brace(TransactionsLog, direction=RIGHT).shift(LEFT)

        self.play(TransactionsLog.animate.shift(LEFT), Transaction1.animate.shift(LEFT),
        Transaction2.animate.shift(LEFT), Transaction3.animate.shift(LEFT), Transaction4.animate.shift(LEFT),
        Transaction5.animate.shift(LEFT), Final.animate.shift(LEFT), Write(LogBrace))

        User1Money = Tex("Usuario 1", " tiene ", "12 monedas.").scale(0.5).next_to(LogBrace, RIGHT).shift(0.67*UP)
        User2Money = Tex("Usuario 2", " tiene ", "25 monedas.").scale(0.5).next_to(User1Money, DOWN)
        User3Money = Tex("Usuario 3", " tiene ", "18 monedas.").scale(0.5).next_to(User2Money, DOWN)
        User4Money = Tex("Usuario 4", " tiene ", "10 monedas.").scale(0.5).next_to(User3Money, DOWN)

        User1Money[0].set_color(GREEN)
        User2Money[0].set_color("#ff676c")
        User3Money[0].set_color(YELLOW)
        User4Money[0].set_color("#dd85ff")

        self.play(Write(User1Money), Write(User2Money), Write(User3Money), Write(User4Money))

        self.wait(2)

        self.play(FadeOut(Computer1), FadeOut(Computer2), FadeOut(Computer3), FadeOut(Computer4),
        FadeOut(User1), FadeOut(User2), FadeOut(User3), FadeOut(User4),
        Uncreate(L12), Uncreate(L13), Uncreate(L14), Uncreate(L23), Uncreate(L24), Uncreate(L34))

        self.play(FadeOut(TransactionsLog), Uncreate(NetworkTittle), FadeOut(LogBrace),
        FadeOut(Transaction1), FadeOut(Transaction2), FadeOut(Transaction3), FadeOut(Transaction4), FadeOut(Transaction5),
        FadeOut(Final), FadeOut(User1Money), FadeOut(User2Money), FadeOut(User3Money), FadeOut(User4Money))

    def MaliciousTransaction(self):
        Danger = Tex("! ! ! ! !").scale(5).set_color(RED)
        self.play(Write(Danger))
        self.wait(2)

        RedUser = SVGMobject("Images/RedUser.svg").to_edge(LEFT)
        BlueUser = SVGMobject("Images/BlueUser.svg").to_edge(RIGHT)
        Connection = Line(RedUser.get_center(), BlueUser.get_center())

        self.bring_to_back(Connection)

        self.play(Uncreate(Danger), DrawBorderThenFill(RedUser), DrawBorderThenFill(BlueUser), Write(Connection))

        TransactionsLog = Rectangle(height=6, width=5.5).shift(0.5*DOWN).set_fill(GREY, opacity=0.85)

        Transaction1 = Tex(". . . . . . . . . . . . . . . . . . . .").scale(0.75).next_to(TransactionsLog, UP).shift(DOWN)
        Transaction2 = Tex(". . . . . . . . . . . . . . . . . . . .").scale(0.75).next_to(Transaction1, 2*DOWN)
        Transaction3 = Tex("Usuario Azul", " paga 10 euros al ", "Usuario Rojo.").scale(0.5).next_to(Transaction2, 2*DOWN)
        Transaction4 = Tex(". . . . . . . . . . . . . . . . . . . .").scale(0.75).next_to(Transaction3, 2*DOWN)
        Transaction5 = Tex(". . . . . . . . . . . . . . . . . . . .").scale(0.75).next_to(Transaction4, 2*DOWN)
        Transaction3[0].set_color("#2e5e99")
        Transaction3[2].set_color(RED)

        self.play(ShowCreation(TransactionsLog))
        self.play(Write(Transaction1), run_time=2.5)
        self.play(Write(Transaction2), run_time=2.5)
        self.play(Write(Transaction3), run_time=2.5)
        self.play(Write(Transaction4), run_time=2.5)
        self.play(Write(Transaction5), run_time=2.5)

        Surprise = Tex("! ! !").next_to(BlueUser, UP).set_color("#df2329")
        self.play(Write(Surprise))

        self.play(FadeOut(Surprise), Uncreate(Connection),
        RedUser.animate.to_corner(UL).shift(RIGHT), BlueUser.animate.to_corner(DL).shift(RIGHT))

        Connection = Line(RedUser.get_center(), BlueUser.get_center())
        LogBrace = Brace(TransactionsLog, direction=RIGHT).set_color(GREEN).shift(RIGHT)
        VerifyText = Tex("Verificar ", "Transacciones").rotate(DEGREES*270).next_to(LogBrace, RIGHT).shift(0.5*RIGHT)
        VerifyText[0].set_color(GREEN)
        self.bring_to_back(Connection)

        self.play(Write(Connection), Write(LogBrace), Write(VerifyText))

        Plus = Tex("+").scale(0.75).next_to(Transaction3, DOWN).set_color(BLACK)
        Hash = Tex("038CEE657E4250A15241E32E301").scale(0.5).next_to(Plus, DOWN).set_color(YELLOW)

        self.play(Write(Plus), Write(Hash), Transaction4.animate.next_to(Hash, 2*DOWN), Transaction5.animate.next_to(Hash, 4*DOWN))

        self.wait()

        self.play(FadeOut(RedUser), FadeOut(BlueUser), Uncreate(Connection), FadeOut(TransactionsLog), Uncreate(VerifyText), FadeOut(LogBrace),
        FadeOut(Transaction1), FadeOut(Transaction2), FadeOut(Transaction3), FadeOut(Transaction4), FadeOut(Transaction5), FadeOut(Plus), FadeOut(Hash))


    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("Audio/AudioPeerToPeer.mp3")

        self.PeerToPeerTittle()

        self.DescentralizedNetwork()

        self.TorrentProtocol()

        self.TransactionsNetwork()

        self.MaliciousTransaction()

        self.wait()

    def construct(self): self.ConstructScene()

class TheDigitalSignature(Scene):
    def DigitalFirmPresentation(self):
        Tittle = Tex("Firma", " Digital").scale(2)
        Tittle[0].set_color(GREEN)
        Tittle[1].set_color(BLUE)
        self.play(Write(Tittle), run_time=5)
        self.wait()
        self.play(Tittle.animate.to_edge(UP))

        User = SVGMobject("Images/User.svg").to_edge(LEFT).set_color("#b4b4b4")
        UserDigitalFirm = Tex("B79D4F4858F1AB36B476A0F0C061A435FB5", "C5B75036F07326E4354").scale(0.75).next_to(User, RIGHT)

        PrivateColor, PublicColor = "#ff3b3b", "#2bff8d"

        self.play(DrawBorderThenFill(User), Write(UserDigitalFirm))

        self.play(UserDigitalFirm[0].animate.set_color(PrivateColor), UserDigitalFirm[1].animate.set_color(PublicColor))

        self.play(FadeOut(User), UserDigitalFirm.animate.move_to(UP+DOWN+LEFT+RIGHT))

        PrivateKeyBrace, PublicKeyBrace = Brace(UserDigitalFirm[0], direction=DOWN).set_color(PrivateColor), Brace(UserDigitalFirm[1], direction=DOWN).set_color(PublicColor)

        PrivateKeyText, PublicKeyText = Tex("Clave Secreta").scale(0.75).set_color(PrivateColor).next_to(PrivateKeyBrace, DOWN), Tex("Clave Pública").scale(0.75).set_color(PublicColor).next_to(PublicKeyBrace, DOWN)

        self.play(Write(PublicKeyBrace), Write(PublicKeyText))
        self.play(Write(PrivateKeyBrace), Write(PrivateKeyText))

        self.wait(3)

        self.play(PublicKeyText.animate.scale(2), PublicKeyBrace.animate.scale(2), UserDigitalFirm[1].animate.scale(2),
        PrivateKeyText.animate.set_opacity(0.25), PrivateKeyBrace.animate.set_opacity(0.25), UserDigitalFirm[0].animate.set_opacity(0.25))
        self.wait(0.5)
        self.play(PublicKeyText.animate.scale(.5), PublicKeyBrace.animate.scale(.5), UserDigitalFirm[1].animate.scale(.5),
        PrivateKeyText.animate.set_opacity(1), PrivateKeyBrace.animate.set_opacity(1), UserDigitalFirm[0].animate.set_opacity(1))

        self.play(PrivateKeyText.animate.scale(2), PrivateKeyBrace.animate.scale(2), UserDigitalFirm[0].animate.scale(2),
        PublicKeyText.animate.set_opacity(0.25), PublicKeyBrace.animate.set_opacity(0.25), UserDigitalFirm[1].animate.set_opacity(0.25))
        self.wait(0.5)
        self.play(PrivateKeyText.animate.scale(.5), PrivateKeyBrace.animate.scale(.5), UserDigitalFirm[0].animate.scale(.5),
        PublicKeyText.animate.set_opacity(1), PublicKeyBrace.animate.set_opacity(1), UserDigitalFirm[1].animate.set_opacity(1))

        self.wait(10)

        self.play(Uncreate(Tittle), Uncreate(PublicKeyText), Uncreate(PrivateKeyText),
        Uncreate(PublicKeyBrace), Uncreate(PrivateKeyBrace), Uncreate(UserDigitalFirm))

    def ManualSignatureDigitalSignature(self):
        ManualSignature = SVGMobject("Images/ManualSignature.svg").set_color(WHITE).shift(UP)
        DigitalSignature = Tex("B79D4F4858F1AB36B476A0F0C061A435FB5").scale(0.75).shift(DOWN)

        PrivateColor, PublicColor = "#ff3b3b", "#2bff8d"

        self.play(Write(ManualSignature), Write(DigitalSignature), run_time=6)
        self.wait()
        self.play(FadeOut(ManualSignature), FadeOut(DigitalSignature))

        Strings = ["ContenidoDeUnArchivo", "ContenidoDeUnArchivo!", "SatoshiNakamoto", "TextoMuyLargoConMuchaInformaciónInnecesaria"]
        CurrentText1, CurrentText2 = Tex(Strings[0]), Tex(SHA256Encode(Strings[0], 2))
        CurrentText1.set_color(BLUE).shift(2*UP)
        CurrentText2.set_color(ORANGE).shift(2*DOWN)
        ArrowConnection = Arrow(CurrentText1.get_center(), CurrentText2.get_center(), stroke_width=3, buff=.5, max_tip_length_to_length_ratio=0.1)

        self.play(Write(CurrentText1), Write(CurrentText2), Write(ArrowConnection))
        for toEncode in Strings[1:]: # Ignoring first string.
            NewText1, NewText2 = Tex(toEncode), Tex(SHA256Encode(toEncode, 2))
            NewText1.set_color(BLUE).shift(2*UP)
            NewText2.set_color(ORANGE).shift(2*DOWN)
            self.play(Transform(CurrentText1, NewText1), Transform(CurrentText2, NewText2), run_time=2.5)
            self.wait()

        self.play(FadeOut(ArrowConnection), FadeOut(CurrentText1), FadeOut(CurrentText2))

    def GenerateVerifyFunctions(self):
        Tittle = Tex("Generar", " y ", "Verificar").scale(2).to_edge(UP)
        Tittle[0].set_color("#ff8b2c")
        Tittle[2].set_color("#61b6d6")

        PrivateColor, PublicColor = "#ff3b3b", "#2bff8d"

        GenerateFunction = Tex("GenerarFirma( , ) = ").set_color(ORANGE)
        FilledGenerateFunction = Tex("GenerarFirma(", "Mensaje", "," ," ClavePrivada", ")", " = ").scale(0.7).shift(UP).to_edge(LEFT)
        FilledGenerateFunction[0].set_color(ORANGE)
        FilledGenerateFunction[1].set_color("#ae29b4")
        FilledGenerateFunction[2].set_color(ORANGE)
        FilledGenerateFunction[3].set_color(PrivateColor)
        FilledGenerateFunction[4].set_color(ORANGE)
        FilledGenerateFunction[5].set_color(ORANGE)
        FilledGenerateFunction[2].set_color(WHITE)

        self.play(Write(GenerateFunction), Write(Tittle))
        self.wait(2)
        self.play(Transform(GenerateFunction, FilledGenerateFunction))

        self.add(FilledGenerateFunction)
        self.remove(GenerateFunction)

        User = SVGMobject("Images/User.svg").scale(0.7).shift(2*UP).shift(3*LEFT).set_color("#b4b4b4").to_corner(DL)
        PublicKey, PrivateKey = Tex("B79D4F4858F1F").set_color(PublicColor).scale(0.7), Tex("C5B75036F07").set_color(PrivateColor).scale(0.7)
        PublicKey.next_to(User, RIGHT).shift(0.25*UP)
        PrivateKey.next_to(PublicKey, DOWN)

        PrivateKeyCopy = Tex("C5B75036F07").set_color(PrivateColor).scale(0.7).move_to(PrivateKey)

        self.add(PrivateKeyCopy)

        self.play(Write(User), Write(PublicKey), Write(PrivateKey))

        self.wait()

        self.play(PrivateKey.animate.move_to(FilledGenerateFunction[3].get_center()), FadeOut(FilledGenerateFunction[3]))

        self.wait(2)

        Signature = Tex("A2CB4099EF72CF4A").scale(0.7).set_color(ORANGE).next_to(FilledGenerateFunction, RIGHT).shift(UP*0.025)

        self.play(Write(Signature))

        VerifyFunction = Tex("VerificarFirma( , ) = ").set_color(BLUE).scale(0.7)
        FilledVerifyFunction = Tex("VerificarFirma(", "Mensaje", ", ", "FirmaDigital", ", ", "ClavePública", ") = ").set_color(BLUE).scale(0.7).next_to(FilledGenerateFunction, DOWN).to_edge(LEFT)
        FilledVerifyFunction[1].set_color("#ae29b4")
        FilledVerifyFunction[3].set_color(ORANGE)
        FilledVerifyFunction[5].set_color(PublicColor)
        FilledVerifyFunction[2].set_color(WHITE)
        FilledVerifyFunction[4].set_color(WHITE)
        self.wait(1.5)

        self.play(VerifyFunction.animate.next_to(FilledGenerateFunction, DOWN).to_edge(LEFT))
        self.wait(1.5)
        self.play(Transform(VerifyFunction, FilledVerifyFunction), run_time=2.5)

        self.add(FilledVerifyFunction)
        self.remove(VerifyFunction)
        FilledGenerateFunction[3].set_color(BLACK)

        FilledVerifyFunctionCopy = Tex("VerificarFirma(", "Mensaje", ", ", "A2CB4099EF72CF4A", ", ", "B79D4F4858F1F", ") = ").set_color(BLUE).scale(0.7).move_to(FilledVerifyFunction).to_edge(LEFT)
        FilledVerifyFunctionCopy[1].set_color("#ae29b4")
        FilledVerifyFunctionCopy[3].set_color(ORANGE)
        FilledVerifyFunctionCopy[5].set_color(PublicColor)
        FilledVerifyFunctionCopy[2].set_color(WHITE)
        FilledVerifyFunctionCopy[4].set_color(WHITE)
        self.play(Transform(FilledVerifyFunction, FilledVerifyFunctionCopy), run_time=2.5)

        BooleanOutput = Tex("True", "/", "False").scale(0.7).next_to(FilledVerifyFunction, RIGHT)
        BooleanOutput[0].set_color(GREEN)
        BooleanOutput[1].set_color(BLUE)
        BooleanOutput[2].set_color(RED)

        self.play(Write(BooleanOutput))

        self.wait(7)

        self.play(FadeOut(FilledVerifyFunction), FadeOut(FilledGenerateFunction), FadeOut(BooleanOutput), FadeOut(Signature), FadeOut(PrivateKey),
        FadeOut(PublicKey), FadeOut(User), FadeOut(PrivateKeyCopy), FadeOut(Tittle))


    def TransactionVerification(self):
        RedUser = SVGMobject("Images/RedUser.svg").to_edge(LEFT)
        BlueUser = SVGMobject("Images/BlueUser.svg").to_edge(RIGHT)
        Connection = Line(RedUser.get_center(), BlueUser.get_center())

        PrivateColor, PublicColor = "#ff3b3b", "#2bff8d"
        PrivateKeyValue, PublicKeyValue = "B79D4F4858F1FGA84FHS", "C5B75036F07"

        self.bring_to_back(Connection)

        self.play(DrawBorderThenFill(RedUser), DrawBorderThenFill(BlueUser), Write(Connection))

        Transaction = Tex("TRN", " = ", "Usuario Azul", " paga 10 euros al ", "Usuario Rojo").to_edge(UP)
        Transaction[0].set_color("#ae29b4") # TRN
        Transaction[2].set_color("#2e5e99") # Usuario Azul
        Transaction[4].set_color(RED) # Usuario Rojo

        self.play(Write(Transaction), run_time=2)

        self.wait(2)

        PublicKey, PrivateKey = Tex(PublicKeyValue).set_color(PublicColor).scale(0.7), Tex(PrivateKeyValue).set_color(PrivateColor).scale(0.7)

        self.play(FadeOut(RedUser), Uncreate(Connection), BlueUser.animate.move_to(ORIGIN))
        PublicKey.next_to(BlueUser, DOWN)
        PrivateKey.next_to(PublicKey, DOWN)
        self.play(Write(PublicKey), Write(PrivateKey))

        self.wait(3)

        self.play(BlueUser.animate.shift(DOWN), PublicKey.animate.shift(DOWN), PrivateKey.animate.shift(DOWN))

        GenerateFunction = Tex("GenerarFirma(", "TRN", "," ," ***********", ")").next_to(Transaction, DOWN)
        GenerateFunction[0].set_color(ORANGE)
        GenerateFunction[1].set_color("#ae29b4")
        GenerateFunction[2].set_color(ORANGE)
        GenerateFunction[3].set_color(PrivateColor)
        GenerateFunction[4].set_color(ORANGE)

        FilledGenerateFunction = Tex("GenerarFirma(", "TRN", ", " , PrivateKeyValue, ")").next_to(Transaction, DOWN)
        FilledGenerateFunction[0].set_color(ORANGE)
        FilledGenerateFunction[1].set_color("#ae29b4")
        FilledGenerateFunction[2].set_color(ORANGE)
        FilledGenerateFunction[3].set_color(PrivateColor)
        FilledGenerateFunction[4].set_color(ORANGE)

        FinalTransaction = Tex("Usuario Azul", " paga 10 euros al ", "Usuario Rojo").to_edge(UP)
        FinalTransaction[0].set_color(BLUE)
        FinalTransaction[2].set_color(RED)

        SumSymbol = Tex("+").next_to(Transaction, DOWN, buff=-0.08)

        Signature = Tex("A2CB4099EF72CF4A").set_color(ORANGE).move_to(FilledGenerateFunction)

        self.play(Write(GenerateFunction))

        self.wait()

        self.play(Transform(GenerateFunction, FilledGenerateFunction))

        self.wait()

        self.play(Transform(GenerateFunction, Signature), Transform(Transaction, FinalTransaction), Write(SumSymbol))

        RedUser.shift(DOWN)
        RedPublicKey, RedPrivateKey, = Tex("9986B72F554").set_color(PublicColor).scale(0.7), Tex("6F4B498D574C6C5500B5").set_color(PrivateColor).scale(0.7)
        RedPublicKey.next_to(RedUser, DOWN).to_edge(LEFT)
        RedPrivateKey.next_to(RedPublicKey, DOWN).to_edge(LEFT)

        self.play(BlueUser.animate.to_edge(RIGHT), PublicKey.animate.to_edge(RIGHT), PrivateKey.animate.to_edge(RIGHT), FadeIn(RedUser),
        Write(RedPublicKey), Write(RedPrivateKey))

        TransactionsLog = Rectangle(height=3, width=5).shift(0.5*DOWN).set_fill(GREY, opacity=0.85).shift(0.25*LEFT)
        Connection = Line(RedUser.get_center(), BlueUser.get_center())

        PublicKeyCopy = Tex(PublicKeyValue).set_color(PublicColor).scale(0.7).move_to(PublicKey)
        self.add(PublicKeyCopy)

        self.remove(GenerateFunction)
        self.bring_to_back(Connection, TransactionsLog)
        self.bring_to_front(Transaction, Signature, SumSymbol, PublicKeyCopy)
        self.play(Write(Connection), ShowCreation(TransactionsLog), run_time=.5)

        self.play(
        Transaction.animate.next_to(TransactionsLog, UP).shift(DOWN).scale(0.5),
        SumSymbol.animate.next_to(TransactionsLog, UP).scale(0.75).shift(1.5*DOWN),
        Signature.animate.next_to(TransactionsLog, UP).scale(0.5).shift(2*DOWN),
        PublicKeyCopy.animate.next_to(TransactionsLog, UP).scale(0.75).shift(2.25*DOWN)
        )

        self.wait(1)

        VerifyBrace = Brace(TransactionsLog, direction=UP).set_color(BLUE)

        FilledVerifyFunction = Tex("VerificarFirma(", "TRN", ", ", "FirmaDigital", ", ", "ClavePública", ") = ", "True").set_color(BLUE).next_to(VerifyBrace, UP)
        FilledVerifyFunction[1].set_color("#ae29b4")
        FilledVerifyFunction[3].set_color(ORANGE)
        FilledVerifyFunction[5].set_color(PublicColor)
        FilledVerifyFunction[2].set_color(WHITE)
        FilledVerifyFunction[4].set_color(WHITE)
        FilledVerifyFunction[-1].set_color(GREEN)

        self.play(Write(VerifyBrace), Write(FilledVerifyFunction))

        self.wait(7)

        self.play(FadeOut(BlueUser), FadeOut(RedUser), FadeOut(Connection),
        Uncreate(PublicKey), Uncreate(PrivateKey), Uncreate(RedPublicKey), Uncreate(RedPrivateKey),
        FadeOut(TransactionsLog), FadeOut(Transaction), FadeOut(SumSymbol), FadeOut(Signature), FadeOut(PublicKeyCopy),
        FadeOut(VerifyBrace), Uncreate(FilledVerifyFunction))

    def SHA256Information(self):
        PrivateColor, PublicColor = "#ff3b3b", "#2bff8d"
        Tittle = Tex("Clave Privada", " y ", "Clave Pública")
        Tittle[0].set_color(PrivateColor)
        Tittle[2].set_color(PublicColor)
        self.play(Write(Tittle, run_time=5))
        self.play(Tittle.animate.to_edge(UP))

        FilledVerifyFunction = Tex("VerificarFirma(", "TRN", ", ", "? ? ? ? ? ?", ", ", "ClavePública", ") = ", "False").set_color(BLUE)
        FilledVerifyFunction[1].set_color("#ae29b4")
        FilledVerifyFunction[3].set_color(ORANGE)
        FilledVerifyFunction[5].set_color(PublicColor)
        FilledVerifyFunction[2].set_color(WHITE)
        FilledVerifyFunction[4].set_color(WHITE)
        FilledVerifyFunction[-1].set_color(RED)

        FilledVerifyFunction1 = Tex("VerificarFirma(", "TRN", ", ", "Z5CB3E05865", ", ", "ClavePública", ") = ", "False").set_color(BLUE)
        FilledVerifyFunction1[1].set_color("#ae29b4")
        FilledVerifyFunction1[3].set_color(ORANGE)
        FilledVerifyFunction1[5].set_color(PublicColor)
        FilledVerifyFunction1[2].set_color(WHITE)
        FilledVerifyFunction1[4].set_color(WHITE)
        FilledVerifyFunction1[-1].set_color(RED)

        FilledVerifyFunction2 = Tex("VerificarFirma(", "TRN", ", ", "TEF75F21202", ", ", "ClavePública", ") = ", "False").set_color(BLUE)
        FilledVerifyFunction2[1].set_color("#ae29b4")
        FilledVerifyFunction2[3].set_color(ORANGE)
        FilledVerifyFunction2[5].set_color(PublicColor)
        FilledVerifyFunction2[2].set_color(WHITE)
        FilledVerifyFunction2[4].set_color(WHITE)
        FilledVerifyFunction2[-1].set_color(RED)

        FilledVerifyFunction3 = Tex("VerificarFirma(", "TRN", ", ", "A3810E771AF", ", ", "ClavePública", ") = ", "False").set_color(BLUE)
        FilledVerifyFunction3[1].set_color("#ae29b4")
        FilledVerifyFunction3[3].set_color(ORANGE)
        FilledVerifyFunction3[5].set_color(PublicColor)
        FilledVerifyFunction3[2].set_color(WHITE)
        FilledVerifyFunction3[4].set_color(WHITE)
        FilledVerifyFunction3[-1].set_color(RED)

        self.play(Write(FilledVerifyFunction))
        for _ in range(7):
            self.play(Transform(FilledVerifyFunction, FilledVerifyFunction1), run_time=0.5)
            self.play(Transform(FilledVerifyFunction, FilledVerifyFunction2), run_time=0.5)
            self.play(Transform(FilledVerifyFunction, FilledVerifyFunction3), run_time=0.5)
        self.play(FadeOut(FilledVerifyFunction))

        SHA256Tittle = Tex("SHA","256").scale(2)
        self.play(Write(SHA256Tittle), run_time=2)
        self.play(SHA256Tittle.animate.scale(0.5).next_to(Tittle, DOWN))
        self.play(SHA256Tittle[1].animate.set_color(YELLOW))

        Bytes1, Bytes2 = Tex("D029F87E3D80F8FD").shift(0.5*UP), Tex("9B1BE67C7426B4CC").shift(0.5*DOWN)
        Bytes = VGroup(Bytes1, Bytes2)
        BytesBrace = Brace(Bytes, direction=RIGHT)
        BytesNumber = Tex("256", " Bytes").next_to(BytesBrace, RIGHT)
        BytesNumber[0].set_color(YELLOW)

        self.play(Write(Bytes))
        self.play(Bytes.animate.shift(0.5*LEFT), Write(BytesBrace), Write(BytesNumber))

        Binary1, Binary2 = Tex(toBinary("D029")).shift(UP), Tex(toBinary("E67C")).shift(DOWN)
        Binary3, Binary4 = Tex(toBinary("3D80")).next_to(Binary1, DOWN), Tex(toBinary("E67C")).next_to(Binary2, UP)
        Binary5, Binary6 = Tex(toBinary("F87E")).next_to(Binary3, DOWN), Tex(toBinary("B4CC")).next_to(Binary4, UP)
        Binary7, Binary8 = Tex(toBinary("F8FD")).next_to(Binary5, DOWN), Tex(toBinary("7426")).next_to(Binary6, UP)

        Binary1.shift(UP)
        Binary3.shift(UP)
        Binary5.shift(UP)
        Binary7.shift(UP)

        Binary2.shift(DOWN)
        Binary4.shift(DOWN)
        Binary6.shift(DOWN)
        Binary8.shift(DOWN)

        Binary = VGroup(Binary1, Binary2, Binary3, Binary4, Binary5, Binary6, Binary7, Binary8).shift(0.5*DOWN)
        BinaryBrace = Brace(Binary, direction=RIGHT)
        BitsNumber = Tex("2048", " Bits").next_to(BinaryBrace, RIGHT)
        BitsNumber[0].set_color(YELLOW)

        self.play(Transform(Bytes, Binary), Transform(BytesBrace, BinaryBrace),
        Transform(BytesNumber, BitsNumber))

        self.wait(7)

        Probabilty = MathTex(r"\frac{1}{2^{256}}").scale(2)
        self.play(Write(Probabilty), Bytes.animate.set_opacity(0.25), run_time=4)

        self.wait(7)

        self.play(FadeOut(Tittle), FadeOut(SHA256Tittle), Uncreate(Bytes), FadeOut(BytesBrace), FadeOut(BytesNumber), Uncreate(Probabilty))

    def TransactionTime(self):
        ColorA, ColorB = "#71ff8d", "#ec71ff"
        TimeColor = "#66e4c9"
        Tittle = Tex("----------", " paga X euros al ", "---------- ", "a las HH:MM:SS")
        Tittle[0].set_color(ColorA)
        Tittle[2].set_color(ColorB)
        Tittle[3].set_color(TimeColor)
        self.play(FadeIn(Tittle), run_time=5)

        self.wait(3)

        Transaction1, Transaction2, Transaction3 = Tex("Usuario B", " paga 10 euros al ", "Usuario A"), Tex("Usuario B", " paga 10 euros al ", "Usuario A"), Tex("Usuario B", " paga 10 euros al ", "Usuario A")
        Transaction1.scale(0.75)
        Transaction2.scale(0.75)
        Transaction3.scale(0.75)
        Transaction1[0].set_color(ColorA)
        Transaction2[0].set_color(ColorA)
        Transaction3[0].set_color(ColorA)
        Transaction1[2].set_color(ColorB)
        Transaction2[2].set_color(ColorB)
        Transaction3[2].set_color(ColorB)
        Transaction1.shift(UP)
        Transaction3.shift(DOWN)

        HashContent = "DB178E1A984C6918"
        NoDateHash1, NoDateHash2, NoDateHash3 =  Tex(" = ", HashContent).scale(0.75).set_color(YELLOW), Tex(" = ", HashContent).scale(0.75).set_color(YELLOW), Tex(" = ", HashContent).scale(0.75).set_color(YELLOW)
        NoDateHash1[0].set_color("#b3b5b3")
        NoDateHash2[0].set_color("#b3b5b3")
        NoDateHash3[0].set_color("#b3b5b3")
        NoDateHash1.next_to(Transaction1, RIGHT)
        NoDateHash2.next_to(Transaction2, RIGHT)
        NoDateHash3.next_to(Transaction3, RIGHT)

        Transaction1, Transaction2, Transaction3 = VGroup(Transaction1, NoDateHash1).move_to(ORIGIN+UP), VGroup(Transaction2, NoDateHash2).move_to(ORIGIN), VGroup(Transaction3, NoDateHash3).move_to(ORIGIN+DOWN)

        self.play(Tittle.animate.to_edge(UP))
        self.play(Write(Transaction1))
        self.play(Write(Transaction2))
        self.play(Write(Transaction3))

        TimeTrns1 = Tex("Usuario B", " paga 10 euros al ", "Usuario A ", "a las 10:00:01").scale(0.75)
        TimeTrns2 = Tex("Usuario B", " paga 10 euros al ", "Usuario A ", "a las 10:00:02").scale(0.75)
        TimeTrns3 = Tex("Usuario B", " paga 10 euros al ", "Usuario A ", "a las 10:00:03").scale(0.75)
        TimeTrns1[0].set_color(ColorA)
        TimeTrns2[0].set_color(ColorA)
        TimeTrns3[0].set_color(ColorA)
        TimeTrns1[2].set_color(ColorB)
        TimeTrns2[2].set_color(ColorB)
        TimeTrns3[2].set_color(ColorB)
        TimeTrns1[3].set_color(TimeColor)
        TimeTrns2[3].set_color(TimeColor)
        TimeTrns3[3].set_color(TimeColor)
        TimeTrns1.shift(UP)
        TimeTrns3.shift(DOWN)

        Hash1Content, Hash2Content, Hash3Content = "654370BE83B81451", "87AD9074B3A78432", "5E43471E0E230741"
        DateHash1, DateHash2, DateHash3 =  Tex(" = ", Hash1Content).scale(0.75).set_color(YELLOW), Tex(" = ", Hash2Content).scale(0.75).set_color(YELLOW), Tex(" = ", Hash3Content).scale(0.75).set_color(YELLOW)
        DateHash1[0].set_color("#b3b5b3")
        DateHash2[0].set_color("#b3b5b3")
        DateHash3[0].set_color("#b3b5b3")
        DateHash1.next_to(TimeTrns1, RIGHT)
        DateHash2.next_to(TimeTrns2, RIGHT)
        DateHash3.next_to(TimeTrns3, RIGHT)

        TimeTrns1, TimeTrns2, TimeTrns3 = VGroup(TimeTrns1, DateHash1).move_to(ORIGIN+UP), VGroup(TimeTrns2, DateHash2).move_to(ORIGIN), VGroup(TimeTrns3, DateHash3).move_to(ORIGIN+DOWN)

        self.play(Transform(Transaction1, TimeTrns1))
        self.play(Transform(Transaction2, TimeTrns2))
        self.play(Transform(Transaction3, TimeTrns3))

        self.wait(2)

        HashBrace = Brace(DateHash3[1], direction=DOWN).set_color(YELLOW)
        HashTittle = Tex("Hash").scale(2).next_to(HashBrace, DOWN)

        self.play(Write(HashBrace), Write(HashTittle))

        self.wait(2)

        self.play(FadeOut(Tittle), FadeOut(Transaction1), FadeOut(Transaction2), FadeOut(Transaction3), FadeOut(HashBrace), FadeOut(HashTittle))

    def SystemRules(self):
        TransactionsLog = Rectangle(height=6, width=5).set_fill(GREY, opacity=0.85)

        self.play(ShowCreation(TransactionsLog))

        Transaction1 = Tex("Usuario 4", " paga 2 monedas a ", "Usuario 1.").scale(0.5).next_to(TransactionsLog, UP).shift(DOWN)
        Transaction2 = Tex("Usuario 1", " paga 3 monedas a ", "Usuario 2.").scale(0.5).next_to(Transaction1, 2*DOWN)
        Transaction3 = Tex("Usuario 1", " paga 5 monedas a ", "Usuario 4.").scale(0.5).next_to(Transaction2, 2*DOWN)
        Transaction4 = Tex("Usuario 3", " paga 4 monedas a ", "Usuario 2.").scale(0.5).next_to(Transaction3, 2*DOWN)
        Transaction5 = Tex("Usuario 2", " paga 5 monedas a ", "Usuario 4.").scale(0.5).next_to(Transaction4, 2*DOWN)
        Final = Tex(". . . . . . . . . . . .").scale(0.5).next_to(Transaction5, 2*DOWN)

        # Usuario 1 ---> GREEN
        # Usuario 2 ---> #ff676c
        # Usuario 3 ---> #YELLOW
        # Usuario 4 ---> #dd85ff


        Transaction1[0].set_color("#dd85ff")
        Transaction1[2].set_color(GREEN)

        Transaction2[0].set_color(GREEN)
        Transaction2[2].set_color("#ff676c")

        Transaction3[0].set_color(GREEN)
        Transaction3[2].set_color("#dd85ff")

        Transaction4[0].set_color(YELLOW)
        Transaction4[2].set_color("#ff676c")

        Transaction5[0].set_color("#ff676c")
        Transaction5[2].set_color("#dd85ff")

        self.play(Write(Transaction1), run_time=0.8)
        self.play(Write(Transaction2), run_time=0.8)
        self.play(Write(Transaction3), run_time=0.8)
        self.play(Write(Transaction4), run_time=0.8)
        self.play(Write(Transaction5), run_time=0.8)
        self.play(Write(Final), run_time=0.8)

        LogBrace = Brace(TransactionsLog, direction=RIGHT).shift(LEFT)

        self.play(TransactionsLog.animate.shift(LEFT), Transaction1.animate.shift(LEFT),
        Transaction2.animate.shift(LEFT), Transaction3.animate.shift(LEFT), Transaction4.animate.shift(LEFT),
        Transaction5.animate.shift(LEFT), Final.animate.shift(LEFT), Write(LogBrace))

        User1Money = Tex("Usuario 1", " tiene ", "12 monedas.").scale(0.5).next_to(LogBrace, RIGHT).shift(0.67*UP)
        User2Money = Tex("Usuario 2", " tiene ", "25 monedas.").scale(0.5).next_to(User1Money, DOWN)
        User3Money = Tex("Usuario 3", " tiene ", "18 monedas.").scale(0.5).next_to(User2Money, DOWN)
        User4Money = Tex("Usuario 4", " tiene ", "10 monedas.").scale(0.5).next_to(User3Money, DOWN)

        User1Money[0].set_color(GREEN)
        User2Money[0].set_color("#ff676c")
        User3Money[0].set_color(YELLOW)
        User4Money[0].set_color("#dd85ff")

        self.play(Write(User1Money), Write(User2Money), Write(User3Money), Write(User4Money))

        Transactions = VGroup(Transaction1, Transaction2, Transaction3, Transaction4, Transaction5, Final, TransactionsLog)
        UsersMoney = VGroup(User1Money, User2Money, User3Money, User4Money, LogBrace)

        self.wait()

        self.play(Transactions.animate.set_opacity(0.25), UsersMoney.animate.set_opacity(0.25))

        Rule1 = Tex("Todos pueden escribir en el registro.")
        Rule2 = Tex("Las transacciones van con una Firma Digital")
        Rule3 = Tex("Las transacciones verificadas, se quedan escritas para siempre.")
        Rules = VGroup(Rule1, Rule2, Rule3)

        self.play(Write(Rule1))
        self.play(FadeOut(Rule1))
        self.play(Write(Rule2))
        self.play(FadeOut(Rule2))
        self.play(Write(Rule3))
        self.wait(4)
        self.play(FadeOut(Rule3))
        self.play(FadeOut(Transactions), FadeOut(UsersMoney))

    def WhosTheSystem(self):
        BlackBoxSystem = Square(side_length=2)
        TransactionSquare = Rectangle(height=1, width=2.5).set_fill(GREY, opacity=0.85).to_edge(LEFT)
        TransactionText = Tex("Transacción").scale(0.75).move_to(TransactionSquare.get_center())
        Interrogant = Tex(">?").scale(2) # ¿?
        OutputData = True
        Output = Tex(str(OutputData)).scale(2).set_color(GREEN).to_edge(RIGHT)
        TransactionToSystem = Arrow(TransactionSquare.get_right(), BlackBoxSystem.get_left(), stroke_width=3, buff=.5)
        SystemToOutput = Arrow(BlackBoxSystem.get_right(), Output.get_left(), stroke_width=3, buff=.5)

        self.play(ShowCreation(TransactionSquare), ShowCreation(BlackBoxSystem), run_time=2)
        self.play(FadeIn(TransactionText), run_time=2)
        self.play(Write(TransactionToSystem))
        self.play(Write(SystemToOutput), FadeIn(Output))


        for _ in range(13):
            OutputData = not(OutputData)
            if OutputData: NewData = Tex(str(OutputData)).scale(2).set_color(GREEN).to_edge(RIGHT)
            else: NewData = Tex(str(OutputData)).scale(2).set_color(RED).to_edge(RIGHT)
            self.play(Transform(Output, NewData))

        self.play(Write(Interrogant))
        self.wait()
        self.play(FadeOut(TransactionSquare), FadeOut(BlackBoxSystem), FadeOut(TransactionText), FadeOut(TransactionToSystem), FadeOut(Interrogant),
        FadeOut(Output), FadeOut(SystemToOutput))

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("Audio/FirmaDigital - 1.mp3")
        self.DigitalFirmPresentation()

        if useAudio: self.add_sound("Audio/FirmaDigital - 2.mp3")
        self.ManualSignatureDigitalSignature()

        if useAudio: self.add_sound("Audio/FirmaDigital - 3.mp3")
        self.GenerateVerifyFunctions()

        if useAudio: self.add_sound("Audio/FirmaDigital - 4.mp3")
        self.TransactionVerification()

        if useAudio: self.add_sound("Audio/FirmaDigital - 5.mp3")
        self.SHA256Information()

        if useAudio: self.add_sound("Audio/FirmaDigital - 6.mp3")
        self.TransactionTime()

        if useAudio: self.add_sound("Audio/FirmaDigital - 7.mp3")
        self.SystemRules()

        if useAudio: self.add_sound("Audio/FirmaDigital - 8.mp3")
        self.WhosTheSystem()

        self.wait()

    def construct(self): self.ConstructScene(True)

class BlockStruct():
    def __init__(self, BlockSize=(2.5, 2.5), BlockColour=WHITE, BlockFill=GREY, BlockOpacity=0.5, blockText=False, textPosition=None):
        self.Size, self.Colour, self.Fill, self.Opacity = BlockSize, BlockColour, BlockFill, BlockOpacity
        self.asRectangle = Rectangle(width=self.Size[0], height=self.Size[1]).set_color(self.Colour).set_fill(self.Fill, self.Opacity)
        if not blockText: self.Text = False
        else:
            self.Text = Tex(blockText).move_to(self.asRectangle.get_center()).scale_to_fit_width(self.Size[0]-1)
            self.asRectangle = VGroup(self.asRectangle, self.Text)

    def to_edge(self, toEdge): return self.asRectangle.to_edge(toEdge)
    def next_to(self, toPosition, toSide): return self.asRectangle.next_to(toPosition, toSide)
    def shift(self, toDirection): return self.asRectangle.shift(toDirection)
    def get_center(self): return self.asRectangle.get_center()
    def get_left(self): return self.asRectangle.get_left()
    def get_right(self): return self.asRectangle.get_right()
    def get_height(self): return self.asRectangle.get_height()
    def get_width(self): return self.asRectangle.get_width()
    def move_to(self, toDirection): return self.asRectangle.move_to(toDirection)

class BlockChainStruct():
    def __init__(self, BlocksSize=(2.5, 2.5), BlocksColour=WHITE, BlocksNumber=5, BlocksFill=BLACK, BlocksOpacity=0.5, fromSide=LEFT, toSide=RIGHT, BlocksSpace=1.5, blocksText=False, angle=90):
        self.nBlocks = BlocksNumber
        self.Size, self.Colour, self.Fill, self.Opacity = BlocksSize, BlocksColour, BlocksFill, BlocksOpacity
        self.fromSide, self.toSide = fromSide, toSide
        self.Space = BlocksSpace
        self.initialPosition, self.finalPosition = -1, -1
        self.Blocks = []
        self.LastBlock = False
        self.CurvatureAngle = angle*DEGREES
        text = blocksText
        for i in range(self.nBlocks):
            if type(blocksText) is list: text = blocksText[i] # Obtenemos el texto.
            CurrentBlock = BlockStruct(self.Size, self.Colour, self.Fill, self.Opacity, blockText=text)
            if not self.LastBlock: CurrentBlock.to_edge(self.fromSide) # Si es el primer bloque.
            else:
                CurrentBlock.next_to(self.LastBlock.asRectangle, self.toSide).shift(self.Space * self.toSide)
                self.CurvatureAngle*=-1
                Connection = CurvedArrow(self.LastBlock.get_right(), CurrentBlock.get_left(), angle=self.CurvatureAngle)
                self.Blocks.append(Connection)

            self.Blocks.append(CurrentBlock)
            self.LastBlock = CurrentBlock

        self.asRectangles = VGroup()
        for x in self.Blocks:
            if type(x) is BlockStruct:
                self.asRectangles.add(x.asRectangle)
            else:
                self.asRectangles.add(x)

        self.initialPosition, self.finalPosition = self.Blocks[0].get_center(), self.Blocks[-1].get_center()

    def addBlock(self, BlockSize=(2.5, 2.5), BlockColour=WHITE, BlockFill=BLACK, BlockOpacity=0.5, BlockSpace=1.5, blockText=False):
        self.CurvatureAngle*=-1
        MyBlock = BlockStruct(BlockSize, BlockColour, BlockFill, BlockOpacity, blockText, textPosition=None)
        MyBlock.next_to(self.LastBlock.asRectangle, self.toSide).shift(self.Space * self.toSide)
        MyConnection = CurvedArrow(self.LastBlock.get_right(), MyBlock.get_left(), angle=self.CurvatureAngle)

        self.Blocks.append(MyConnection)
        self.Blocks.append(MyBlock)

        self.LastBlock = MyBlock

        self.asRectangles.add(MyConnection)
        self.asRectangles.add(MyBlock.asRectangle)

        # self.asRectangles.move_to(ORIGIN)

        self.finalPosition = self.Blocks[-1].get_center()

    def to_edge(self, toEdge): return self.asRectangles.to_edge(toEdge)
    def next_to(self, toPosition, toSide): return self.asRectangles.next_to(toPosition, toSide)
    def shift(self, toDirection): return self.asRectangles.shift(toDirection)
    def get_center(self): return self.asRectangles.get_center()
    def get_left(self): return self.asRectangles.get_left()
    def get_right(self): return self.asRectangles.get_right()
    def move_to(self, toDirection): return self.asRectangles.move_to(toDirection)

    def __getitem__(self, fromIndex): return self.Blocks[fromIndex]

    def __len__(self): return self.nBlocks

class TheBlockChain(GraphScene, MovingCameraScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(self,
        x_min = X[0],
        x_max = X[1],
        y_min = Y[0],
        y_max = Y[1],
        y_tick_frequency = X[2],
        x_tick_frequency = Y[2],
        x_labeled_nums = np.arange(X[0], X[1]+1, 5),
        y_labeled_nums = [],
        x_label_direction = DOWN,
        y_label_direction = UP,
        x_axis_visibility = True,
        y_axis_visibility = True,
        graph_origin = np.array([-4.25, -3, 0]),
        x_axis_label = 'Usuarios',
        y_axis_label = 'Rendimiento')

    def BlockChainPresentation(self):
        BlockColour, ChainColor = "#ae58f8", "#6700ff"
        self.wait(0.5)
        Tittle = Tex("BLOCK", "CHAIN").scale(2)
        Tittle[0].set_color(BlockColour)
        Tittle[1].set_color(ChainColor)
        self.play(Write(Tittle))
        self.play(Tittle.animate.to_edge(UP))

        MyBlockChain = BlockChainStruct(BlocksNumber=10)
        MyBlockChain.shift(0.5*DOWN)

        Tittle.move_to(MyBlockChain.initialPosition).to_edge(UP)
        self.camera.frame.move_to(MyBlockChain.initialPosition)
        self.play(FadeIn(MyBlockChain.asRectangles))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(MyBlockChain.finalPosition).shift(RIGHT), Tittle.animate.move_to(MyBlockChain.finalPosition).shift(RIGHT).to_edge(UP), run_time=5)

        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        BlockBrace = Brace(MyBlockChain.asRectangles, direction=RIGHT).set_color("#ae58f8").shift(RIGHT)
        CompressedBlockChain = Rectangle(width=2.5, height=4).set_color(WHITE).set_fill(BLACK, 1).next_to(BlockBrace, RIGHT).shift(RIGHT)
        Block.move_to(CompressedBlockChain.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain.get_center()).shift(0.25*DOWN)

        CompressedBlockChain = VGroup(CompressedBlockChain, Block, Chain)

        self.play(Write(BlockBrace), FadeIn(CompressedBlockChain))

        self.camera.frame.save_state()
        self.play(FadeOut(MyBlockChain.asRectangles), FadeOut(BlockBrace), self.camera.frame.animate.move_to(ORIGIN), Tittle.animate.move_to(ORIGIN).to_edge(UP),
        CompressedBlockChain.animate.move_to(ORIGIN))

        User1, User2 = SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(UL), SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(UR)
        User3, User4 = SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(DL), SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(DR)
        C1, C2 = Line(User1.get_center(), CompressedBlockChain.get_center()), Line(User2.get_center(), CompressedBlockChain.get_center())
        C3, C4 = Line(User3.get_center(), CompressedBlockChain.get_center()), Line(User4.get_center(), CompressedBlockChain.get_center())
        L12 = Line(User1.get_center(), User2.get_center())
        L13 = Line(User1.get_center(), User3.get_center())
        L14 = Line(User1.get_center(), User4.get_center())
        L23 = Line(User3.get_center(), User2.get_center())
        L24 = Line(User4.get_center(), User2.get_center())
        L34 = Line(User4.get_center(), User3.get_center())

        Users = VGroup(User1, User2, User3, User4)
        Connections = VGroup(C1, C2, C3, C4)

        self.add_foreground_mobjects(Users, CompressedBlockChain)

        Network = VGroup(Users, Connections)

        self.play(Write(Network), FadeOut(Tittle))

        B1, B2, B3, B4 = deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4)

        self.play(Uncreate(Connections), FadeOut(CompressedBlockChain),
        B1.animate.move_to(User1).shift(RIGHT), B2.animate.move_to(User2).shift(LEFT), B3.animate.move_to(User3).shift(RIGHT), B4.animate.move_to(User4).shift(LEFT), run_time=3)

        self.wait(2)

        Connections = VGroup(L12, L13, L14, L23, L24, L34)

        self.bring_to_back(Connections)

        Network.add(B1, B2, B3, B4)
        Network.remove(C1, C2, C3, C4)
        Network.add(Connections)

        self.play(Write(Connections), run_time=2)

        Txt1, Txt2 = Tex("Minero 1").scale(0.5).next_to(User1, UP, buff=0.15), Tex("Minero 2").scale(0.5).next_to(User2, UP, buff=0.15)
        Txt3, Txt4 = Tex("Minero 3").scale(0.5).next_to(User3, DOWN, buff=0.15), Tex("Minero 4").scale(0.5).next_to(User4, DOWN, buff=0.15)

        Txt = VGroup(Txt1, Txt2, Txt3, Txt4)

        self.wait(2)

        self.play(FadeIn(Txt))

        self.wait(0.5)

        self.play(FadeOut(Txt), Uncreate(Network))

        ChainSize = 10
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=0.75, blocksText=[f"Transacción {i+1}" for i in range(ChainSize)], angle=45)
        MyBlockChainLonger = deepcopy(MyBlockChain)
        MyBlockChainLonger.addBlock(BlockSize=(4, 2.5), BlockSpace=0.75, blockText="Transacción 11", BlockColour="#77ff71")

        BlockChainBrace = Brace(MyBlockChain[0].asRectangle, direction=DOWN)
        Block = Tex("BLOQUE").scale(2.5).set_color("#854bff")
        Block.scale(0.5).next_to(BlockChainBrace, DOWN)

        self.camera.frame.move_to(MyBlockChain.initialPosition)
        self.play(Write(BlockChainBrace), Write(Block), FadeIn(MyBlockChain.asRectangles), run_time=5)

        self.wait(3)

        self.camera.frame.save_state()
        Miner = SVGMobject("Images/User.svg").next_to(MyBlockChainLonger.finalPosition, UP).shift(1.5*UP).set_color("#b4b4b4")
        self.play(self.camera.frame.animate.move_to(MyBlockChain.finalPosition), run_time=5)
        self.remove(BlockChainBrace, Block)

        self.play(Write(MyBlockChainLonger.asRectangles), Write(Miner), run_time=2)

        self.remove(MyBlockChain)

        self.wait(2)

        Transaction = Tex("Alice", " paga 10 euros a ", "Bob").next_to(Miner, LEFT).shift(.75*LEFT)
        Transaction[0].set_color("#71b8ff")
        Transaction[2].set_color("#ff4b6f")

        self.play(Write(Transaction), run_time=2)

        self.play(Transaction.animate.move_to(MyBlockChainLonger.finalPosition).set_opacity(0), run_time=2)

        self.wait()

        self.play(FadeOut(MyBlockChain.asRectangles), FadeOut(MyBlockChainLonger.asRectangles), FadeOut(Miner))

    def VotingSystem(self):
        self.camera.frame.move_to(ORIGIN) # Moving the camera to origin, since the camera has been moved to visualize the blockchain.
        SystemColor, VotationsColor, MinersColor = "#9764bb", "#5068d5", "#d58f50"
        Tittle = Tex("Sistema", " de ", "Votaciones").scale(2)
        Tittle[0].set_color(SystemColor) # Sistema
        Tittle[2].set_color(VotationsColor) # Votaciones

        self.play(Write(Tittle), run_time=2)
        MainUser = SVGMobject("Images/User.svg").set_color(SystemColor).to_edge(LEFT)
        User1, User2, User3 = SVGMobject("Images/User.svg").scale(0.75), SVGMobject("Images/User.svg").scale(0.75), SVGMobject("Images/User.svg").scale(0.75)
        User1.next_to(User2, UP).shift(UP)
        User3.next_to(User2, DOWN).shift(DOWN)

        Users = VGroup(User1, User2, User3).set_color(VotationsColor).to_edge(RIGHT)

        C1, C2, C3 = Line(MainUser.get_center(), User1.get_center()), Line(MainUser.get_center(), User2.get_center()), Line(MainUser.get_center(), User3.get_center())
        Connections = VGroup(C1, C2, C3)

        self.add_foreground_mobjects(Users, MainUser)
        Network = VGroup(Users, Connections)

        self.play(FadeOut(Tittle), FadeIn(Users), FadeIn(MainUser))

        MainUserBrace = Brace(MainUser, direction=UP).set_color(SystemColor)
        UsersBrace = Brace(Users, direction=LEFT).shift(LEFT).set_color(VotationsColor)
        Miners = Tex("Mineros de la Red").set_color(MinersColor).rotate(90*DEGREES).next_to(UsersBrace, LEFT)

        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        CompressedBlockChain_ = Rectangle(width=2.5, height=4).set_color(WHITE).set_fill(BLACK, 1)
        Block.move_to(CompressedBlockChain_.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain_.get_center()).shift(0.25*DOWN)
        CompressedBlockChain = VGroup(CompressedBlockChain_, Block, Chain).scale(0.5).next_to(MainUserBrace, UP)

        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        CompressedBlockChain_1 = Rectangle(width=2.5, height=4).set_color(GREEN).set_fill(BLACK, 1)
        Block.move_to(CompressedBlockChain_1.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain_1.get_center()).shift(0.25*DOWN)
        CompressedBlockChain1 = VGroup(CompressedBlockChain_1, Block, Chain).scale(0.4).next_to(User1, LEFT, buff=-0.15)

        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        CompressedBlockChain_2 = Rectangle(width=2.5, height=4).set_color(GREEN).set_fill(BLACK, 1)
        Block.move_to(CompressedBlockChain_2.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain_2.get_center()).shift(0.25*DOWN)
        CompressedBlockChain2 = VGroup(CompressedBlockChain_2, Block, Chain).scale(0.4).next_to(User2, LEFT, buff=-0.15)

        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        CompressedBlockChain_3 = Rectangle(width=2.5, height=4).set_color(GREEN).set_fill(BLACK, 1)
        Block.move_to(CompressedBlockChain_3.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain_3.get_center()).shift(0.25*DOWN)
        CompressedBlockChain3 = VGroup(CompressedBlockChain_3, Block, Chain).scale(0.4).next_to(User3, LEFT, buff=-0.15)

        self.wait()

        self.play(Write(UsersBrace), Write(Miners), Write(MainUserBrace), Write(CompressedBlockChain),
        FadeIn(CompressedBlockChain1), FadeIn(CompressedBlockChain2), FadeIn(CompressedBlockChain3))

        self.add_foreground_mobjects(CompressedBlockChain, CompressedBlockChain1, CompressedBlockChain2, CompressedBlockChain3)
        self.add_foreground_mobjects(Users, MainUser)

        self.wait(2)

        self.play(FadeOut(MainUserBrace), CompressedBlockChain.animate.next_to(MainUser, RIGHT, buff=-0.15))

        self.play(CompressedBlockChain_.animate.set_color(RED).set_fill(BLACK, 1))

        self.play(Write(Connections), FadeOut(UsersBrace), FadeOut(Miners))

        VotationStatus0 = np.array([0, 1]) # 0 - 3
        VotationStatus1 = np.array([0.33, 0.66]) # 1 - 2
        VotationStatus2 = np.array([0.66, 0.33]) # 2 - 1
        VotationStatus3 = np.array([1, 0]) # 3 - 0
        Bars0 = BarChart(VotationStatus0, bar_colors=["#4fff6c", "#ff584f"], height=1.5, width=2.5, label_y_axis=False).to_corner(UL)
        Bars1 = BarChart(VotationStatus1, bar_colors=["#4fff6c", "#ff584f"], height=1.5, width=2.5, label_y_axis=False).to_corner(UL)
        Bars2 = BarChart(VotationStatus2, bar_colors=["#4fff6c", "#ff584f"], height=1.5, width=2.5, label_y_axis=False).to_corner(UL)
        Bars3 = BarChart(VotationStatus3, bar_colors=["#4fff6c", "#ff584f"], height=1.5, width=2.5, label_y_axis=False).to_corner(UL)

        GraphBrace = Brace(Bars0, RIGHT).shift(0.5*RIGHT).set_color("#757575")
        Legend1, Legend2 = Tex("Usuarios que lo han aceptado.").set_color("#4fff6c").scale(0.7), Tex("Usuarios que no lo han aceptado.").set_color("#ff584f").scale(0.7)
        Legend1.next_to(GraphBrace, RIGHT).shift(0.25*UP)
        Legend2.next_to(GraphBrace, RIGHT).shift(0.25*DOWN)

        Legend = VGroup(GraphBrace, Legend1, Legend2)

        self.play(Write(Bars0), Write(Legend))
        self.wait(2)
        self.play(Transform(Bars0, Bars1), C1.animate.set_color("#4fff6c"), Uncreate(Legend), run_time=2)
        self.wait()
        self.play(Transform(Bars0, Bars2), C2.animate.set_color("#4fff6c"), CompressedBlockChain_.animate.set_color(GREEN).set_fill(BLACK, 1), run_time=2)
        self.wait()
        self.play(Transform(Bars0, Bars3), C3.animate.set_color("#4fff6c"), run_time=2)

        self.play(FadeOut(Bars0), FadeOut(Network),
        FadeOut(CompressedBlockChain), FadeOut(CompressedBlockChain1), FadeOut(CompressedBlockChain2), FadeOut(CompressedBlockChain3),
        FadeOut(MainUser), FadeOut(Users))

    def BlockContent(self):
        ChainSize = 2
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=1, blocksText=[f"Block {i+1}" for i in range(ChainSize)], angle=45)
        MyBlockChain_ = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=1, BlocksSpace=1, blocksText="BLOCK", angle=45)
        Block = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=1, BlocksSpace=1, angle=45)
        MyBlockChain.move_to(ORIGIN)
        MyBlockChain_.move_to(ORIGIN)
        Block.move_to(ORIGIN).scale(2.5)
        self.play(Write(MyBlockChain.asRectangles))
        self.wait()
        self.play(Transform(MyBlockChain.asRectangles, MyBlockChain_.asRectangles))
        self.wait()
        self.play(MyBlockChain.asRectangles.animate.scale(2.5))
        BC1 = Tex("2000 Transacciones").move_to(MyBlockChain.get_left()).shift(2.5*RIGHT).shift(2.5*UP)
        BC2 = Tex("Fecha de Creación").next_to(BC1, DOWN)
        BC3 = Tex("Mineros que lo han aceptado").next_to(BC2, DOWN)
        BC4 = Tex("Número de transacciones").next_to(BC3, DOWN)
        BC5 = Tex("Tamaño en Bytes").next_to(BC4, DOWN)
        BC6 = Tex("Recompensa").next_to(BC5, DOWN)
        BC7 = Tex("Número Aleatorio").next_to(BC6, DOWN)
        BC8 = Tex("Siguiente Bloque").next_to(BC7, DOWN)
        BC9 = Tex(". . . . .").next_to(BC8, DOWN)

        BlockContent = VGroup(BC1, BC2, BC3, BC4, BC5, BC6, BC7, BC8, BC9).move_to(Block.asRectangles)
        self.play(Transform(MyBlockChain.asRectangles, Block.asRectangles))
        self.play(Write(BlockContent), run_time=16)
        self.wait()
        self.play(BC6.animate.set_color(YELLOW))
        self.play(BC7.animate.set_color(YELLOW))

        self.wait(4)

        self.play(FadeOut(MyBlockChain.asRectangles), FadeOut(BlockContent))
        BlockRate = Tex("1 Bloque", " cada ", "10 minutos")
        TrnRate = Tex("3 o 4 Transacciones", " cada ", "segundo")

        BlockRate[0].set_color("#a94da8")
        BlockRate[2].set_color("#ff5179")

        TrnRate[0].set_color("#a94da8")
        TrnRate[2].set_color("#ff5179")

        self.play(Write(BlockRate), run_time=2)
        self.wait(1.5)
        self.play(Transform(BlockRate, TrnRate))
        self.wait()
        self.play(FadeOut(BlockRate))

    def MinersFunction(self):
        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        CompressedBlockChain = Rectangle(width=2.5, height=4).set_color(WHITE).set_fill(BLACK, 1)
        Block.move_to(CompressedBlockChain.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain.get_center()).shift(0.25*DOWN)
        CompressedBlockChain = VGroup(CompressedBlockChain, Block, Chain)

        User1, User2 = SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(UL), SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(UR)
        User3, User4 = SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(DL), SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(DR)

        B1, B2, B3, B4 = deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4)
        B1.move_to(User1).shift(RIGHT)
        B2.move_to(User2).shift(LEFT)
        B3.move_to(User3).shift(RIGHT)
        B4.move_to(User4).shift(LEFT)

        L12 = Line(User1.get_center(), User2.get_center())
        L13 = Line(User1.get_center(), User3.get_center())
        L14 = Line(User1.get_center(), User4.get_center())
        L23 = Line(User3.get_center(), User2.get_center())
        L24 = Line(User4.get_center(), User2.get_center())
        L34 = Line(User4.get_center(), User3.get_center())

        Blocks = VGroup(B1, B2, B3, B4)
        Users = VGroup(User1, User2, User3, User4)
        Connections = VGroup(L12, L13, L14, L23, L24, L34)

        self.add_foreground_mobjects(Blocks)
        self.add_foreground_mobjects(Users)

        Network = VGroup(Users, Connections, Blocks)

        self.play(Write(Network), run_time=3)

        self.play(Network.animate.set_opacity(0.1))

        self.setup_axes(animate=True)
        MyGraph = self.get_graph(lambda x: (1/15)*(x**2), color=ORANGE, x_min=.01, x_max=N)
        self.bring_to_back(MyGraph)
        self.play(ShowCreation(MyGraph))

        self.wait(4)

        self.play(Uncreate(self.axes), Uncreate(MyGraph))

        ChainSize = 50
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=1, blocksText=[f"{SHA256Encode(str(i), 4)}" for i in range(ChainSize)], angle=45)
        ColorAmount = "#fa4848"
        ColorBTC = "#ff9860"
        MiningReward = Tex("Recompensa:", " X ", "BTCs").scale(2).to_edge(UP)
        InitialReward = Tex("Recompensa:", " 50 ", "BTCs").scale(2).to_edge(UP)
        NextReward = Tex("Recompensa:", " 25 ", "BTCs").scale(2).to_edge(UP)
        CurrentReward = Tex("Recompensa:", " 6.25 ", "BTCs").scale(2).to_edge(UP)

        MiningReward[1].set_color(ColorAmount)
        MiningReward[2].set_color(ColorBTC)

        InitialReward[1].set_color(ColorAmount)
        InitialReward[2].set_color(ColorBTC)

        NextReward[1].set_color(ColorAmount)
        NextReward[2].set_color(ColorBTC)

        CurrentReward[1].set_color(ColorAmount)
        CurrentReward[2].set_color(ColorBTC)

        self.play(FadeIn(MyBlockChain.asRectangles), Write(MiningReward), FadeOut(Network))

        Network.set_opacity(0)
        self.remove_foreground_mobjects(Blocks)
        self.remove_foreground_mobjects(Users)

        self.camera.frame.save_state()

        InitialReward.move_to(MyBlockChain[10].get_center()).to_edge(UP)
        self.play(self.camera.frame.animate.move_to(MyBlockChain[10].get_center()), MiningReward.animate.move_to(MyBlockChain[10].get_center()).to_edge(UP), run_time=5)
        self.play(Transform(MiningReward, InitialReward))

        NextReward.move_to(MyBlockChain[30].get_center()).to_edge(UP)
        self.play(self.camera.frame.animate.move_to(MyBlockChain[30].get_center()), MiningReward.animate.move_to(MyBlockChain[30].get_center()).to_edge(UP), run_time=5)
        self.play(Transform(MiningReward, NextReward))

        CurrentReward.move_to(MyBlockChain[-1].get_center()).to_edge(UP)
        self.play(self.camera.frame.animate.move_to(MyBlockChain[-1].get_center()), MiningReward.animate.move_to(MyBlockChain[-1].get_center()).to_edge(UP), run_time=5)
        self.play(Transform(MiningReward, CurrentReward))

        self.wait()

        self.play(FadeOut(MiningReward), FadeOut(MyBlockChain.asRectangles))

    def HashAtTheBlock(self):
        self.camera.frame.move_to(ORIGIN)
        PrivateColor, PublicColor = "#ff3b3b", "#2bff8d"

        UserDigitalFirm = Tex("B79D4F4858F1AB36B476A0F0C061A435FB5", "C5B75036F07326E4354").scale(0.75)

        self.play(Write(UserDigitalFirm))
        self.play(UserDigitalFirm[0].animate.set_color(PrivateColor), UserDigitalFirm[1].animate.set_color(PublicColor))

        PrivateKeyBrace, PublicKeyBrace = Brace(UserDigitalFirm[0], direction=DOWN).set_color(PrivateColor), Brace(UserDigitalFirm[1], direction=DOWN).set_color(PublicColor)
        PrivateKeyText, PublicKeyText = Tex("Clave Privada").scale(0.75).set_color(PrivateColor).next_to(PrivateKeyBrace, DOWN), Tex("Clave Pública").scale(0.75).set_color(PublicColor).next_to(PublicKeyBrace, DOWN)

        self.wait()

        self.play(Write(PublicKeyBrace), Write(PublicKeyText))
        self.play(Write(PrivateKeyBrace), Write(PrivateKeyText))

        Keys = VGroup(UserDigitalFirm, PrivateKeyBrace, PublicKeyBrace, PrivateKeyText, PublicKeyText)

        self.wait(4)

        ChainSize = 3
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=0.5, blocksText=[f"{SHA256Encode(str(i), 4)}" for i in range(ChainSize)], angle=45)
        MyBlockChain.move_to(ORIGIN)
        self.play(Keys.animate.set_opacity(0.25), Write(MyBlockChain.asRectangles))

        self.wait()

        SHA256Tittle = Tex("SHA", "256").scale(2)
        SHA256Tittle[1].set_color(YELLOW)

        ExampleMessage = Tex("RandomText")
        EncodeMesssage = Tex(SHA256Encode("RandomText")).scale(0.75)
        MyBrace = Brace(EncodeMesssage, direction=DOWN).set_color(YELLOW)
        CharsNum, BytesNum = Tex("64 ", "Carácteres").next_to(MyBrace, DOWN), Tex("256 ", "Bytes").next_to(MyBrace, DOWN)
        CharsNum[0].set_color(YELLOW)
        BytesNum[0].set_color(YELLOW)

        self.play(MyBlockChain.asRectangles.animate.set_opacity(0.25), FadeOut(Keys), Write(SHA256Tittle))

        self.play(SHA256Tittle.animate.to_edge(UP))
        self.play(Write(ExampleMessage))
        self.wait()
        self.play(Transform(ExampleMessage, EncodeMesssage), Write(MyBrace), Write(CharsNum))
        self.wait(4)
        self.play(Transform(CharsNum, BytesNum))
        self.wait()

        self.play(FadeOut(MyBrace), FadeOut(CharsNum), Uncreate(SHA256Tittle), FadeOut(ExampleMessage), MyBlockChain.asRectangles.animate.set_opacity(1))

        SingleBlock = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=1, BlocksSpace=1, blocksText=False, angle=45)
        SingleBlock.asRectangles.scale(2.5).move_to(ORIGIN)
        TXT1, TXT2 = Tex("Mi Hash: ", "532EAABD9574880D").set_color(GREEN), Tex("Siguiente Hash: ", "8A863B145DC6E4ED").set_color(ORANGE)
        TXT1.shift(UP)
        TXT2.shift(DOWN)
        TXT = VGroup(TXT1, TXT2)
        SingleBlock = VGroup(SingleBlock.asRectangles, TXT)

        self.play(Transform(MyBlockChain.asRectangles, SingleBlock), run_time=3)

        self.wait(8)

        self.play(Uncreate(MyBlockChain.asRectangles))

    def AboutMining(self):
        ChainSize = 50
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=1, blocksText=[f"{SHA256Encode(str(i), 4)}" for i in range(ChainSize)], angle=45)
        self.play(FadeIn(MyBlockChain.asRectangles))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(MyBlockChain[-1].get_center()), run_time=12)
        self.wait(2)
        self.play(FadeOut(MyBlockChain.asRectangles))

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("Audio/BlockChain - 1.mp3")
        self.BlockChainPresentation()

        if useAudio: self.add_sound("Audio/BlockChain - 2.mp3")
        self.VotingSystem()

        if useAudio: self.add_sound("Audio/BlockChain - 3.mp3")
        self.BlockContent()

        if useAudio: self.add_sound("Audio/BlockChain - 4.mp3")
        self.MinersFunction()

        if useAudio: self.add_sound("Audio/BlockChain - 5.mp3")
        self.HashAtTheBlock()

        if useAudio: self.add_sound("Audio/BlockChain - 6.mp3")
        self.AboutMining()

        self.wait()

    def construct(self): self.ConstructScene(True)

class TheProofOfWork(GraphScene, MovingCameraScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(self,
        x_min = X[0],
        x_max = 5,
        y_min = Y[0],
        y_max = Y[1],
        y_tick_frequency = X[2],
        x_tick_frequency = Y[2],
        x_labeled_nums = [],
        y_labeled_nums = [],
        x_label_direction = DOWN,
        y_label_direction = UP,
        x_axis_visibility = True,
        y_axis_visibility = True,
        graph_origin = np.array([-4.25, -3, 0]),
        x_axis_label = 'Ceros',
        y_axis_label = 'Dificultad')

    def ZeroRule(self):
        Tittle = Tex("Proof", " of ", "Work").scale(2).to_edge(UP)
        Tittle[0].set_color("#e260e3")
        Tittle[2].set_color("#60bde3")
        ChainSize = 10
        CeroHashList = ["000000"+SHA256Encode(str(i), 8) for i in range(ChainSize)]
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=1, blocksText=CeroHashList, angle=90)

        self.play(Write(Tittle), Write(MyBlockChain.asRectangles), run_time=2)

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(MyBlockChain[-1].get_center()), run_time=8)

        self.play(FadeOut(MyBlockChain.asRectangles))
        self.camera.frame.move_to(ORIGIN)

        Block = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=1, BlocksSpace=1, angle=45)
        Block.move_to(ORIGIN).scale(1.5)

        self.play(Write(Block.asRectangles))
        self.wait()
        BC1 = Tex("2000 Transacciones").move_to(Block.get_left()).shift(2.5*RIGHT).shift(2.5*UP)
        BC2 = Tex("Fecha de Creación").next_to(BC1, DOWN)
        BC3 = Tex("Mineros que lo han aceptado").next_to(BC2, DOWN)
        BC4 = Tex("Número de transacciones").next_to(BC3, DOWN)
        BC5 = Tex("Tamaño en Bytes").next_to(BC4, DOWN)
        BC6 = Tex("Recompensa").next_to(BC5, DOWN)
        BC7 = Tex("Número Aleatorio").next_to(BC6, DOWN)
        BC8 = Tex("Siguiente Bloque").next_to(BC7, DOWN)
        BC9 = Tex(". . . . .").next_to(BC8, DOWN)

        BlockContent = VGroup(BC1, BC2, BC3, BC4, BC5, BC6, BC7, BC8, BC9).scale(0.6).move_to(Block.asRectangles)
        self.play(Write(BlockContent), run_time=3)
        Block = VGroup(BlockContent, Block.asRectangles)
        BlockBrace = Brace(Block, direction=DOWN)
        nHashes = 13
        HashList = [Tex(SHA256Encode(str(i), 4)).set_color(RED).next_to(BlockBrace, DOWN) for i in range(nHashes-1)] + [Tex("000000"+SHA256Encode(str(9), 6)).set_color(GREEN).next_to(BlockBrace, DOWN)]

        self.play(Write(BlockBrace), Write(HashList[0]))
        for i in range(1, 10):
            self.play(Transform(HashList[0], HashList[i]))
            self.wait(0.25)

        self.wait()

        self.play(BC7.animate.set_color(YELLOW).scale(2))
        self.play(BC7.animate.scale(0.5))

        RandomNumbers = [Tex(str(np.random.randint(1, 1000))).set_color(RED).move_to(BC7).scale(0.6) for _ in range(nHashes-1)] + [Tex(str(np.random.randint(1, 100))).set_color(GREEN).move_to(BC7).scale(0.6)]
        self.play(Transform(BC7, RandomNumbers[0]))

        for i in range(1, nHashes):
            self.play(Transform(HashList[0], HashList[i]), Transform(BC7, RandomNumbers[i]))
            self.wait(0.25)

        self.play(FadeOut(BlockBrace), FadeOut(Block), FadeOut(Tittle), FadeOut(HashList[0]))

    def ExponentialWork(self):
        self.setup_axes(animate=True)
        MyGraph = self.get_graph(lambda x: x**2, color=GREEN, x_min=0, x_max=N)
        self.bring_to_back(MyGraph)

        self.camera.frame.save_state() # Guardamos el estado initial para después de movernos a través de x², volvamos a ver la gráfica como al inicio.

        self.play(ShowCreation(MyGraph), run_time=3)

        MovingDot = Dot().move_to(MyGraph.points[0]).set_color(ORANGE) # Este punto se mueve con nosotros.

        self.play(ShowCreation(MovingDot), run_time=2)

        self.play(self.camera.frame.animate.scale(0.5).move_to(MovingDot), run_time=2.5)

        def UpdateCurve(x): x.move_to(MovingDot.get_center())

        self.camera.frame.add_updater(UpdateCurve)
        self.play(MoveAlongPath(MovingDot, MyGraph, rate_func=linear), run_time=2.5)
        self.wait(0.5)
        self.camera.frame.remove_updater(UpdateCurve)

        self.play(Restore(self.camera.frame), run_time=2.5)

        self.wait(0.5)

        TXT = Tex("Cada", " 2016 ", "bloques se revisa")
        TXT[1].set_color(RED)
        self.play(self.axes.animate.set_opacity(0.25), MyGraph.animate.set_stroke_opacity(0.25), Write(TXT), run_time=2)

        self.wait(1.5)

        self.play(FadeOut(TXT), FadeOut(self.axes), FadeOut(MyGraph))

    def DifferentRules(self):
        PATH = "Images/CryptoLogos"
        SVGs = []
        for IMG in os.listdir(PATH):
            try:
                SVGs.append(ImageMobject(f"{PATH}/{IMG}").scale(0.25))
            except NotImplementedError:
                print(f"ERROR! ---> {IMG}")
            else:
                print(f"CORRECT! ---> {IMG}")

        self.play(FadeIn(SVGs[0]))
        self.wait(2)
        for i in range(1, len(SVGs)):
            self.play(FadeOut(SVGs[i-1]), FadeIn(SVGs[i]))
            self.wait(2)
        self.play(FadeOut(SVGs[-1]))

    def PuttingAllTogether(self):
        CoinPhases = [ImageMobject(f"Images/Coin{i+1}.png") for i in range(6)] # Nuestra moneda tiene 6 fotogramas distintos.
        for _ in range(5):
            for Coin in CoinPhases:
                self.add(Coin)
                self.wait(0.2)
                self.remove(Coin)

        self.play(FadeOut(Coin), run_time=0.5)

        ChainSize = 3
        MyBlockChain = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=ChainSize, BlocksSpace=0.5, blocksText=[f"{SHA256Encode(str(i), 4)}" for i in range(ChainSize)], angle=45)

        self.play(Write(MyBlockChain.asRectangles))

        self.wait(2)

        Block, Chain = Tex("BLOCK").scale(0.75), Tex("CHAIN").scale(0.75)
        CompressedBlockChain = Rectangle(width=2.5, height=4).set_color(WHITE).set_fill(BLACK, 1)
        Block.move_to(CompressedBlockChain.get_center()).shift(0.25*UP)
        Chain.move_to(CompressedBlockChain.get_center()).shift(0.25*DOWN)
        CompressedBlockChain = VGroup(CompressedBlockChain, Block, Chain)

        User1, User2 = SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(UL), SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(UR)
        User3, User4 = SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(DL), SVGMobject("Images/User.svg").set_color("#b4b4b4").to_corner(DR)


        B1, B2, B3, B4 = deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4), deepcopy(CompressedBlockChain).scale(0.4)
        B1.move_to(User1).shift(RIGHT)
        B2.move_to(User2).shift(LEFT)
        B3.move_to(User3).shift(RIGHT)
        B4.move_to(User4).shift(LEFT)
        Blocks = VGroup(B1, B2, B3, B4)

        L12 = Line(User1.get_center(), User2.get_center())
        L13 = Line(User1.get_center(), User3.get_center())
        L14 = Line(User1.get_center(), User4.get_center())
        L23 = Line(User3.get_center(), User2.get_center())
        L24 = Line(User4.get_center(), User2.get_center())
        L34 = Line(User4.get_center(), User3.get_center())

        Users = VGroup(User1, User2, User3, User4)
        Blocks = VGroup(B1, B2, B3, B4)
        Connections = VGroup(L12, L13, L14, L23, L24, L34)

        self.add_foreground_mobjects(Blocks, Users)

        Network = VGroup(Users, Blocks, Connections)

        self.play(Write(Network), MyBlockChain.asRectangles.animate.set_opacity(0.25), run_time=2)
        self.wait(4)

        Block = BlockChainStruct(BlocksSize=(4, 2.5), BlocksNumber=1, BlocksSpace=1, angle=45)
        self.remove(Blocks, Users)
        Block.move_to(ORIGIN).scale(1.5)

        self.play(Write(Block.asRectangles), FadeOut(MyBlockChain.asRectangles), FadeOut(Network))
        self.wait()
        BC1 = Tex("2000 Transacciones").move_to(Block.get_left()).shift(2.5*RIGHT).shift(2.5*UP).set_color(YELLOW)
        BC2 = Tex("Fecha de Creación").next_to(BC1, DOWN)
        BC3 = Tex("HASH").next_to(BC2, DOWN).set_color(YELLOW)
        BC4 = Tex("Número de transacciones").next_to(BC3, DOWN)
        BC5 = Tex("Tamaño en Bytes").next_to(BC4, DOWN)
        BC6 = Tex("Recompensa").next_to(BC5, DOWN).set_color(YELLOW)
        BC7 = Tex("Número Aleatorio").next_to(BC6, DOWN).set_color(YELLOW)
        BC8 = Tex("Siguiente Bloque").next_to(BC7, DOWN)
        BC9 = Tex(". . . . .").next_to(BC8, DOWN)

        BlockContent = VGroup(BC1, BC2, BC3, BC4, BC5, BC6, BC7, BC8, BC9).scale(0.6).move_to(Block.asRectangles)
        self.play(Write(BlockContent), run_time=12)

        BlockBrace = Brace(Block.asRectangles, direction=DOWN)
        nHashes = 13
        HashList = [Tex(SHA256Encode(str(i), 4)).set_color(RED).next_to(BlockBrace, DOWN) for i in range(nHashes-1)] + [Tex("000000"+SHA256Encode(str(9), 6)).set_color(GREEN).next_to(BlockBrace, DOWN)]
        RandomNumbers = [Tex(str(np.random.randint(1, 1000))).set_color(RED).move_to(BC7).scale(0.75) for _ in range(nHashes-1)] + [Tex(str(np.random.randint(1, 100))).set_color(GREEN).move_to(BC7).scale(0.6)]

        self.play(Write(BlockBrace), Transform(BC7, RandomNumbers[0]))
        for i in range(1, nHashes):
            self.play(Transform(HashList[0], HashList[i]), Transform(BC7, RandomNumbers[i]))
            self.wait(0.25)

        self.wait(4)

        self.play(FadeOut(BlockContent), FadeOut(Block.asRectangles), FadeOut(HashList[0]), FadeOut(BlockBrace))

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("Audio/ProofOfWork - 1.mp3")
        self.ZeroRule()

        if useAudio: self.add_sound("Audio/ProofOfWork - 2.mp3")
        self.ExponentialWork()

        if useAudio: self.add_sound("Audio/ProofOfWork - 3.mp3")
        self.DifferentRules()

        if useAudio: self.add_sound("Audio/ProofOfWork - 4.mp3")
        self.PuttingAllTogether()

        self.wait()

    def construct(self): self.ConstructScene(True)

class Thumbnail(Scene):
    def construct(self):
        ChainSize = 3
        MyBlockChain = BlockChainStruct(BlocksSize=(2.5, 2.5), BlocksNumber=ChainSize, BlocksSpace=1.5, blocksText=[f"{SHA256Encode(str(i), 4)}" for i in range(ChainSize)], BlocksColour=ORANGE)
        MyBlockChain.move_to(ORIGIN)

        for ID in range(10):
            BinaryBG = Tex(toBinary(SHA256Encode(str(ID), 4))).to_edge(UP).shift(ID*DOWN).set_opacity(0.25)
            self.add(BinaryBG)

        self.add_foreground_mobjects(MyBlockChain.asRectangles)
