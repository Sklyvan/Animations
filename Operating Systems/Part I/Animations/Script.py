from manim import *
from manim.mobject.geometry import ArrowSquareTip

# ManimCE Version 0.8.0
# 1920x1080 60FPS

PixelWidth = config.pixel_width = 1920
PixelHeight = config.pixel_height = 1080
FPS = config.frame_rate = 60

print(f"Rendering ManimCE (0.8.0) at {PixelWidth}x{PixelHeight} {FPS}FPS.")

# Global Variables
CENTRAL_COLOR, PROCESSING_COLOR, UNIT_COLOR = WHITE, YELLOW, WHITE
CENTER = [0, 0, 0]

class ComputerParts(Scene):
    def TheCPU(self):
        CPU = Tex("C", "P", "U").scale(3)
        CentralProcessingUnit = Tex("Central", " Processing ", "Unit").scale(2).next_to(CPU, DOWN)
        CPU[0].set_color(CENTRAL_COLOR)
        CPU[1].set_color(PROCESSING_COLOR)
        CPU[2].set_color(UNIT_COLOR)
        CentralProcessingUnit[0].set_color(CENTRAL_COLOR)
        CentralProcessingUnit[1].set_color(PROCESSING_COLOR)
        CentralProcessingUnit[2].set_color(UNIT_COLOR)
        Tittle = VGroup(CPU, CentralProcessingUnit)

        self.play(Write(Tittle), run_time=3)

        self.wait()

        self.play(Tittle.animate.scale(0.5).to_edge(UP))

        ALU = Rectangle(height=2, width=2).set_fill(GREY, opacity=0.75)
        ALUText = Tex("ALU").scale(0.75).set_color(BLACK).move_to(ALU)
        ALU = VGroup(ALU, ALUText)

        Registers = Rectangle(height=1, width=2).set_fill(GREY, opacity=0.75)
        RegistersText = Tex("Registros").scale(0.75).set_color(BLACK).move_to(Registers)
        Registers = VGroup(Registers, RegistersText).next_to(ALU, UP)

        CPU_Contour = Rectangle(height=4, width=4)

        CPU = VGroup(ALU, Registers).move_to(CPU_Contour)
        CPU += CPU_Contour
        CPU.shift(0.5*DOWN)
        self.play(FadeIn(CPU))

        self.wait(0.5)

        self.play(ALUText.animate.set_color(YELLOW))

        self.wait()

        self.play(ALUText.animate.set_color(WHITE), RegistersText.animate.set_color(YELLOW))

        self.wait()

        Registers_ = Rectangle(height=1, width=3.5).set_fill(GREY, opacity=0.75)
        RegistersText_ = Tex("Registros ", " (1 KB)").scale(0.75).move_to(Registers_)
        RegistersText_[0].set_color(YELLOW)
        RegistersText_[1].set_color(BLUE)
        Registers_ = VGroup(Registers_, RegistersText_).move_to(Registers)

        self.play(Transform(Registers, Registers_))

        self.wait(4)

        self.play(RegistersText.animate.set_color(WHITE))

        ALU_ = Rectangle(height=2, width=2).set_fill(GREY, opacity=0.75)
        ALUText_ = Tex("ALU").scale(0.75).set_color(BLACK).move_to(ALU_)
        ALU_ = VGroup(ALU_, ALUText_).move_to(ALU)

        Registers_ = Rectangle(height=1, width=3.5).set_fill(GREY, opacity=0.75)
        RegistersText_ = Tex("Registros ", " (1 KB)").scale(0.75).move_to(Registers_)
        RegistersText_[0].set_color(WHITE)
        RegistersText_[1].set_color(BLUE)
        Registers_ = VGroup(Registers_, RegistersText_).move_to(Registers)

        Cache = Rectangle(height=1.5, width=3.5).set_fill(GREY, opacity=0.75)
        CacheText = Tex("Memoria Caché ", " (16 MB)").scale(0.5).move_to(Cache)
        CacheText[0].set_color(WHITE)
        CacheText[1].set_color(BLUE)
        Cache = VGroup(Cache, CacheText).next_to(ALU, DOWN)

        CPU_Contour_ = Rectangle(height=5.5, width=4)

        CPU_ = VGroup(ALU_, Registers_, Cache).move_to(CPU_Contour_)

        CPU_ += CPU_Contour_

        CPU_.shift(0.75*DOWN)

        self.play(Transform(CPU, CPU_))

        self.wait()

        self.play(CacheText[0].animate.set_color(YELLOW))

        self.wait(6)

        self.play(CacheText[0].animate.set_color(WHITE), ALUText.animate.set_color(RED))

        self.wait(4)

        self.play(Uncreate(Tittle), Uncreate(CPU), FadeOut(CacheText))

    def TheRAM(self):
        Tittle1 = Tex("Memoria ", " RAM").scale(2)
        Tittle2 = Tex("Random", " Access ", "Memory").scale(2).move_to(Tittle1)
        RAM_Icon = SVGMobject("../Images/RAM Module.svg").scale(0.5)
        RAM_Brace = Brace(RAM_Icon, direction=DOWN)
        RAM_Capacity = Tex("8 - 16 GB").next_to(RAM_Brace, DOWN)
        RAM = VGroup(RAM_Icon, RAM_Brace, RAM_Capacity).move_to(CENTER+0.5*DOWN)

        self.play(Write(Tittle1))

        self.wait()

        self.play(Transform(Tittle1, Tittle2))

        self.play(Tittle1[0].animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Tittle1[0].animate.set_color(WHITE), Tittle1[1].animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Tittle1[1].animate.set_color(WHITE), Tittle1[2].animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Tittle1[2].animate.set_color(WHITE))
        self.wait(0.10)

        self.play(Uncreate(Tittle1), FadeIn(RAM))

        self.wait()

        self.play(FadeOut(RAM))

    def TheDisk(self):
        Tittle = Tex("Disco Duro").scale(2)
        Disk = SVGMobject("../Images/Hard Disk.svg").scale(2)

        self.play(Write(Tittle), run_time=2)

        self.wait(2)

        self.play(FadeOut(Tittle), DrawBorderThenFill(Disk))

        self.wait(5)

        GPU_Tittle = Tex("Graphic Processing Unit").scale(1.5)
        GPU_Icon = SVGMobject("../Images/GPU.svg").scale(2).rotate(DEGREES*90).next_to(GPU_Tittle, DOWN)

        GPU = VGroup(GPU_Tittle, GPU_Icon).move_to(CENTER)

        self.play(FadeOut(Disk), Write(GPU), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(GPU))

    def DevicesComparison(self):
        SpeedColor = YELLOW
        ComponentColor = BLUE
        Tittle = Tex("Velocidad", " de los ", "Componentes").to_edge(UP)
        Tittle[0].set_color(SpeedColor)
        Tittle[2].set_color(ComponentColor)

        self.play(Write(Tittle), run_time=2)
        self.wait(3)

        HorizontalLine, VerticalLine = Line(5*LEFT, 5*RIGHT).next_to(Tittle, DOWN), Line(3*UP, 3*DOWN)
        VerticalLine.next_to(HorizontalLine, DOWN, buff=0)

        Table = VGroup(HorizontalLine, VerticalLine)

        self.play(Write(Table))

        Registers = Tex("Registros", " (1 KB)")
        Cache = Tex("Memoria Caché", " (16 MB)").next_to(Registers, DOWN, buff=1.75)
        RAM = Tex("Memoria RAM", " (8 - 16 GB)").next_to(Cache, DOWN, buff=1.75)
        Disk = Tex("Disco Duro", " (1 TB)").next_to(RAM, DOWN, buff=1.75)

        LeftSide = VGroup(Registers, Cache, RAM, Disk).scale(0.75).move_to(CENTER).shift(2.5*LEFT).shift(0.35*DOWN)

        RegistersTime = Tex("0.25 - 0.5", " Nanosegundos")
        CacheTime = Tex("0.5 - 25", " Nanosegundos").next_to(RegistersTime, DOWN, buff=1.75)
        RAMTime = Tex("80 - 250", " Nanosegundos").next_to(CacheTime, DOWN, buff=1.75)
        DiskTime = Tex("5000", " Nanosegundos").next_to(RAMTime, DOWN, buff=1.75)

        RighSide = VGroup(RegistersTime, CacheTime, RAMTime, DiskTime).scale(0.75).move_to(CENTER).shift(2.5*RIGHT).shift(0.35*DOWN)

        Registers[1].set_color(BLUE)
        Cache[1].set_color(BLUE)
        RAM[1].set_color(BLUE)
        Disk[1].set_color(BLUE)

        RegistersTime[0].set_color(YELLOW)
        CacheTime[0].set_color(YELLOW)
        RAMTime[0].set_color(YELLOW)
        DiskTime[0].set_color(YELLOW)

        self.play(Write(Registers))
        self.wait()
        self.play(Write(RegistersTime))
        self.wait()
        self.play(Write(Cache))
        self.play(Write(CacheTime))
        self.play(Write(RAM))
        self.wait(0.25)
        self.play(Write(RAMTime))
        self.wait()
        self.play(Write(Disk))
        self.wait(0.5)
        self.play(Write(DiskTime))
        self.wait()

        Plot2D = Axes(x_range=[0, 10], y_range=[0, 10, 1], axis_config={"include_tip": False})
        Labels = Plot2D.get_axis_labels(x_label="Bytes", y_label="Seconds")
        Graph = Plot2D.get_graph(lambda x: x, color=RED)

        self.play(FadeIn(Plot2D), Write(Labels), Tittle.animate.set_opacity(0.25), Table.animate.set_opacity(0.25), LeftSide.animate.set_opacity(0.25), RighSide.animate.set_opacity(0.25),
        Write(Graph))

        self.wait(3)

        self.play(FadeOut(Graph), FadeOut(Labels), FadeOut(Plot2D), FadeOut(Tittle), FadeOut(Table), FadeOut(LeftSide), FadeOut(RighSide))

    def ConstructScene(self, useAudio=True):
        if useAudio: self.add_sound("../Audio/2.1-Componentes.mp3")
        self.TheCPU()

        if useAudio: self.add_sound("../Audio/2.2-Componentes.mp3")
        self.TheRAM()

        if useAudio: self.add_sound("../Audio/2.3-Componentes.mp3")
        self.TheDisk()

        if useAudio: self.add_sound("../Audio/2.4-Componentes.mp3")
        self.DevicesComparison()

    def construct2(self): self.ConstructScene()

class RunningMultipleProcess(MovingCameraScene):
    def RunningOnCPU(self):
        P1_Color, P2_Color, P3_Color = "#3fe685", "#ee4d55", "#4dd4ee"
        CPU_Icon = SVGMobject("../Images/CPU.svg")

        self.play(FadeIn(CPU_Icon))

        P1, P2, P3 = Arrow(start=LEFT, end=RIGHT).set_color(P1_Color), Arrow(start=LEFT, end=RIGHT).shift(0.5*DOWN).set_color(P2_Color), Arrow(start=LEFT, end=RIGHT).shift(DOWN).set_color(P3_Color)
        Process = VGroup(P1, P2, P3).move_to(CENTER).to_edge(LEFT)
        T1, T2, T3 = Tex("Proceso", " 1").move_to(P1).scale(0.5), Tex("Proceso", " 2").move_to(P2).scale(0.5), Tex("Proceso", " 3").move_to(P3).scale(0.5)
        T1[1].set_color(P1_Color)
        T2[1].set_color(P2_Color)
        T3[1].set_color(P3_Color)
        Process.shift(1.5*RIGHT)
        Process.add(T1, T2, T3)

        self.play(FadeIn(Process))

        P1, P2, P3 = VGroup(P1, T1), VGroup(P2, T2), VGroup(P3, T3)

        self.add_foreground_mobjects(CPU_Icon)

        self.play(P1.animate.shift(14*RIGHT), P2.animate.shift(14*RIGHT), P3.animate.shift(14*RIGHT), run_time=5)

        Process1 = Tex("Nombre: ", "GNOME Shell Konsole", " ID: ", "2466", " Memoria: ", "318 MB")
        Process2 = Tex("Nombre: ", "DConf Service OAuth", " ID: ", "2751", " Memoria: ", "880 KB").next_to(Process1, DOWN)
        Process3 = Tex("Nombre: ", "GDM X-Session Kernel-X", " ID: ", "2019", " Memoria: ", "664 KB").next_to(Process2, DOWN)
        Process4 = Tex("Nombre: ", "SSH Secure Protocol Agent", " ID: ", "7185", " Memoria: ", "928 KB").next_to(Process3, DOWN)
        Process5 = Tex("Nombre: ", "io.elementary.appcenter", " ID: ", "5543", " Memoria: ", "161 MB").next_to(Process4, DOWN)
        Process6 = Tex("Nombre: ", "GSD-USB-Protection", " ID: ", "2845", " Memoria: ", "972 KB").next_to(Process5, DOWN)
        Process7 = Tex("Nombre: ", "Tracker Miner-FS", " ID: ", "1905", " Memoria: ", "18.2 MB").next_to(Process6, DOWN)
        Process8 = Tex("Nombre: ", "SystemD Boot Resources", " ID: ", "1892", " Memoria: ", "569 MB").next_to(Process7, DOWN)
        Process9 = Tex("Nombre: ", "GNOME Session Binary", " ID: ", "2398", " Memoria: ", "208 MB").next_to(Process8, DOWN)
        Process10 = Tex("Nombre: ", "GSD X-Settings", " ID: ", "2859", " Memoria: ", "9.3 MB").next_to(Process9, DOWN)

        SystemTasks = VGroup(Process1, Process2, Process3, Process4, Process5, Process6, Process7, Process8, Process9, Process10).scale(1.15).move_to(CENTER).set_opacity(0.5)

        self.play(Write(SystemTasks), run_time=5)

        self.wait()

        self.play(Process2.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process2.animate.set_color(WHITE))

        self.play(Process10.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process10.animate.set_color(WHITE))

        self.play(Process5.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process5.animate.set_color(WHITE))

        self.play(Process9.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process9.animate.set_color(WHITE))

        self.play(Process7.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process7.animate.set_color(WHITE))

        self.play(Process3.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process3.animate.set_color(WHITE))

        self.play(Process6.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process6.animate.set_color(WHITE))

        self.play(Process8.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process8.animate.set_color(WHITE))

        self.play(Process4.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process4.animate.set_color(WHITE))

        self.play(Process1.animate.set_color(YELLOW))
        self.wait(0.25)
        self.play(Process1.animate.set_color(WHITE))

    def ProcessDefinition(self):
        Definition1, Definition2 = Tex("Una", " instancia ", "de un programa informático"), Tex("que ejecuta un conjunto de", " instrucciones.")
        Definition2.next_to(Definition1, DOWN)
        Definition1[1].set_color(RED)
        Definition2[1].set_color(RED)
        Definition = VGroup(Definition1, Definition2).move_to(CENTER)
        self.play(Write(Definition), run_time=5)
        self.wait()

    def FunctionSum(self):
        SUM = 0
        SUM_VALUE = Tex("SUM", " = ", f"{SUM}")
        SUM_VALUE[0].set_color(GREEN)
        SUM_VALUE[2].set_color(YELLOW)
        self.play(Write(SUM_VALUE))
        for _ in range(10):
            SUM += 10
            SUM_VALUE_ = Tex("SUM", " = ", f"{SUM}")
            SUM_VALUE_[0].set_color(GREEN)
            SUM_VALUE_[2].set_color(YELLOW)
            self.wait(0.25)
            self.play(Transform(SUM_VALUE, SUM_VALUE_))

        self.wait()

    def C_Code(self):
        ProcessColor = "#3fe685"
        CPU = SVGMobject("../Images/CPU.svg")
        Exclamations = Tex("! ! !").scale(1.5).move_to(CPU).set_color(RED).set_opacity(0)
        self.add(Exclamations)

        ProcessArrow = Arrow(start=LEFT, end=2*RIGHT).set_color(ProcessColor)
        ProcessName = Tex("Proceso", " F1").next_to(ProcessArrow, UP)
        ProcessName[1].set_color(ProcessColor)
        Process = VGroup(ProcessArrow, ProcessName).move_to(CENTER).to_edge(LEFT)

        self.play(DrawBorderThenFill(CPU), Write(Process), run_time=2.5)

        self.wait(5)

        self.play(Process.animate.next_to(CPU, LEFT, buff=0.2).set_color(RED), Exclamations.animate.next_to(CPU, UP).set_opacity(1))

        self.wait()

    def AssemblyCode(self):
        Instructions = ["F1:", "daddiu !sp,!sp,-32", "sd !fp,24(!sp)", "move !fp,!sp", "sw !0,0(!fp)", "sw !0,4(!fp)", "b .L2", "nop", ".L3:", "lw !2,0(!fp)", "addiu !2,!2,10",
        "sw !2,0(!fp)", "lw !2,4(!fp)", "addiu !2,!2,1", "sw !2,4(!fp)", ".L2", "lw !2,4(!fp)", "slt !2,!2,10", "bne !2,!0,.L3", "nop", "lw !2,0(!fp)", "move !sp,!fp", "ld !fp,24(!sp)",
        "daddiu !sp,!sp,32", "j !31", "nop"]

        self.camera.frame.save_state()

        lastPosition = None
        for Instruction in Instructions:
            if lastPosition is None: CurrentInstruction = Tex(Instruction).to_edge(UP)
            else: CurrentInstruction = Tex(Instruction).move_to(lastPosition).shift(0.75*DOWN)
            lastPosition = CurrentInstruction.get_center()

            self.play(Write(CurrentInstruction), self.camera.frame.animate.move_to(lastPosition))
            self.wait(.25)

        self.play(Restore(self.camera.frame))
        self.wait()

    def AssemblyInstructions(self):
        I1 = Tex("lw", " !2,0(!fp)")
        I2 = Tex("addiu", " 2,!2,10")
        I3 = Tex("sw", " !2,0(1fp)")
        I4 = Tex("move", " 1sp,1fp")
        I5 = Tex("daddiu", " 1sp,1sp,-32")

        I1[0].set_color(BLUE)
        I2[0].set_color(BLUE)
        I3[0].set_color(BLUE)
        I4[0].set_color(BLUE)
        I5[0].set_color(BLUE)

        self.play(Write(I1))
        self.wait(.25)
        self.play(Transform(I1, I2))
        self.wait(.25)
        self.play(Transform(I1, I3))
        self.wait(.25)
        self.play(Transform(I1, I4))
        self.wait(.25)
        self.play(Transform(I1, I5))
        self.wait()

    def SmallCode(self):
        Declaration = Tex("int", " A ", "=", " 0", ";")
        Declaration[0].set_color(BLUE)
        Declaration[1].set_color(RED)
        Declaration[3].set_color(YELLOW)

        Operation = Tex("A", " = ", "A", " + ", "1", ";").next_to(Declaration, DOWN)
        Operation[0].set_color(RED)
        Operation[2].set_color(RED)
        Operation[4].set_color(YELLOW)

        Code = VGroup(Declaration, Operation).move_to(CENTER)

        self.play(Write(Code), run_time=3.5)

        self.wait()

        self.play(Declaration.animate.scale(2))
        self.wait(0.25)
        self.play(Declaration.animate.scale(0.5))

        self.wait(0.25)

        self.play(Operation.animate.scale(2))
        self.wait(0.25)
        self.play(Operation.animate.scale(0.5))

    def ConstructScene(self, useAudio=True):
        # if useAudio: self.add_sound("../Audio/3.1-Procesos Simultáneos.mp3")
        # self.RunningOnCPU()
        # self.ProcessDefinition()

        # self.FunctionSum()

        # if useAudio: self.add_sound("../Audio/3.2-Procesos Simultáneos.mp3")
        # self.C_Code()

        # self.AssemblyInstructions()

        # self.AssemblyCode()

        if useAudio: self.add_sound("../Audio/4.1-Context Switch.mp3")
        self.SmallCode()

    def construct(self): self.ConstructScene()


class ContextSwitch(Scene):
    def SmallCode(self):
        Declaration = Tex("int", " A ", "=", " 0", ";")
        Declaration[0].set_color(BLUE)
        Declaration[1].set_color(RED)
        Declaration[3].set_color(YELLOW)

        Operation = Tex("A", " = ", "A", " + ", "1", ";").next_to(Declaration, DOWN)
        Operation[0].set_color(RED)
        Operation[2].set_color(RED)
        Operation[4].set_color(YELLOW)

        Code = VGroup(Declaration, Operation).move_to(CENTER)

        self.play(Write(Code), run_time=3.5)

        self.wait()

        self.play(Declaration.animate.scale(2))
        self.wait(0.25)
        self.play(Declaration.animate.scale(0.5))

        self.wait(0.25)

        self.play(Operation.animate.scale(2))
        self.wait(0.25)
        self.play(Operation.animate.scale(0.5))

    def SmallAssemblyCode(self):
        Declaration = Tex("int", " A ", "=", " 0", ";")
        Declaration[0].set_color(BLUE)
        Declaration[1].set_color(RED)
        Declaration[3].set_color(YELLOW)

        Operation = Tex("A", " = ", "A", " + ", "1", ";").next_to(Declaration, DOWN)
        Operation[0].set_color(RED)
        Operation[2].set_color(RED)
        Operation[4].set_color(YELLOW)

        C_Code = VGroup(Declaration, Operation).move_to(CENTER)

        self.add(C_Code)

        self.wait(0.5)

        Store1 = Tex("sw", " !0, 0(!fp)")
        Load = Tex("lw", " !2, 0(!fp)").next_to(Store1, DOWN)
        Add = Tex("addiu", " !2, !2, 1").next_to(Load, DOWN)
        Store2 = Tex("sw", " !2, 0(!fp)").next_to(Add, DOWN)

        Store1[0].set_color(ORANGE)
        Load[0].set_color(ORANGE)
        Add[0].set_color(ORANGE)
        Store2[0].set_color(ORANGE)

        Assembly_Code = VGroup(Store1, Load, Add, Store2).move_to(CENTER)

        self.play(Transform(C_Code, Assembly_Code))
        self.add(Assembly_Code)
        self.remove(C_Code)

        self.wait(.15)

        self.play(Store1.animate.set_color(YELLOW))
        self.wait(9)
        self.play(Store1.animate.set_color(WHITE).set_opacity(0.5), Load.animate.set_color(YELLOW))
        self.wait(2)
        self.play(Load.animate.set_color(WHITE).set_opacity(0.5), Add.animate.set_color(YELLOW))
        self.wait()
        self.play(Add.animate.set_color(WHITE).set_opacity(0.5), Store2.animate.set_color(YELLOW))
        self.wait(3)

        self.play(Assembly_Code.animate.set_color(WHITE).set_opacity(1))

        self.wait()

        RAM = SVGMobject("../Images/RAM Module.svg").scale(0.5)
        Disk = SVGMobject("../Images/Hard Disk.svg").scale(2)

        self.play(Assembly_Code.animate.shift(7*UP), FadeIn(RAM))

        self.wait(7)

        self.play(RAM.animate.shift(7*UP), FadeIn(Disk))

        self.wait()

    def QuantumTime(self):
        Tittle = Tex("Quantum").scale(2).set_color(ORANGE)

        P1_Color, P2_Color, P3_Color = "#3fe685", "#ee4d55", "#4dd4ee"
        P1, P2, P3 = Arrow(start=LEFT, end=RIGHT).set_color(P1_Color), Arrow(start=LEFT, end=RIGHT).shift(0.5*DOWN).set_color(P2_Color), Arrow(start=LEFT, end=RIGHT).shift(DOWN).set_color(P3_Color)
        T1, T2, T3 = Tex("Proceso", " 1").scale(0.5).move_to(P1).shift(1.5*LEFT), Tex("Proceso", " 2").scale(0.5).move_to(P2).shift(1.5*LEFT), Tex("Proceso", " 3").scale(0.5).move_to(P3).shift(1.5*LEFT)
        T1.set_color(P1_Color)
        T2.set_color(P2_Color)
        T3.set_color(P3_Color)
        Q1, Q2, Q3 = Tex("3 Segundos").set_color(P1_Color), Tex("2 Segundos").set_color(P2_Color), Tex("5 Segundos").set_color(P3_Color)
        Q1.scale(0.5).move_to(P1).shift(1.5*RIGHT)
        Q2.scale(0.5).move_to(P2).shift(1.5*RIGHT)
        Q3.scale(0.5).move_to(P3).shift(1.5*RIGHT)
        Process = VGroup(P1, P2, P3, T1, T2, T3, Q1, Q2, Q3).scale(2).move_to(CENTER)

        self.play(Write(Process), run_time=5)

        self.wait(3)

        self.play(Process.animate.set_opacity(0.35), Write(Tittle), run_time=2)

        self.wait(3)

        self.play(Uncreate(Tittle), Uncreate(Process))

        Store1 = Tex("sw", " !0, 0(!fp)")
        Load = Tex("lw", " !2, 0(!fp)").next_to(Store1, DOWN)
        Add = Tex("addiu", " !2, !2, 1").next_to(Load, DOWN)
        Store2 = Tex("sw", " !2, 0(!fp)").next_to(Add, DOWN)

        Store1[0].set_color(ORANGE)
        Load[0].set_color(ORANGE)
        Add[0].set_color(ORANGE)
        Store2[0].set_color(ORANGE)

        Assembly_Code = VGroup(Store1, Load, Add, Store2).move_to(CENTER)

        self.play(Write(Assembly_Code))

        CodeBox = Rectangle(height=Assembly_Code.get_height()+0.5, width=Assembly_Code.get_width()+0.5).set_fill(BLUE, opacity=0.15)
        BoxBrace = Brace(CodeBox, RIGHT)
        CodeQuantum = Tex("2 Segundos").next_to(BoxBrace, RIGHT)
        Assembly_Code.add(CodeBox, BoxBrace, CodeQuantum)

        self.play(Write(CodeBox), Write(BoxBrace), Write(CodeQuantum))

        self.wait()

    def WorkingOnCPU(self):
        ProcessColor = "#3fe685"
        CPU = SVGMobject("../Images/CPU.svg")

        ProcessArrow = Arrow(start=LEFT, end=2*RIGHT).set_color(ProcessColor)
        ProcessName = Tex("Proceso").next_to(ProcessArrow, UP).set_color(ProcessColor)
        Process = VGroup(ProcessArrow, ProcessName).move_to(CENTER).to_edge(LEFT)

        self.play(DrawBorderThenFill(CPU), Write(Process))

        self.play(Process.animate.next_to(CPU, LEFT, buff=0.2))

        self.wait()

        Store1 = Tex("sw", " !0, 0(!fp)")
        Load = Tex("lw", " !2, 0(!fp)").next_to(Store1, DOWN)
        Add = Tex("addiu", " !2, !2, 1").next_to(Load, DOWN)
        Store2 = Tex("sw", " !2, 0(!fp)").next_to(Add, DOWN)

        Store1[0].set_color(ORANGE)
        Load[0].set_color(ORANGE)
        Add[0].set_color(ORANGE)
        Store2[0].set_color(ORANGE)

        Assembly_Code = VGroup(Store1, Load, Add, Store2).move_to(CENTER)

        CodeBox = Rectangle(height=Assembly_Code.get_height()+0.5, width=Assembly_Code.get_width()+0.5).set_fill(BLUE, opacity=0.15)

        Assembly_Code += CodeBox

        TotalTime = Tex("Tiempo Disponible: 2 Segundos").next_to(CodeBox, UP).set_color(GREEN)
        TotalTime1, TotalTime2 = Tex("Tiempo Disponible: 1 Segundo").next_to(CodeBox, UP).set_color(BLUE), Tex("Tiempo Disponible: 0 Segundos").next_to(CodeBox, UP).set_color(RED)

        self.play(Write(Assembly_Code), FadeOut(Process), FadeOut(CPU), Write(TotalTime), run_time=2)

        self.wait()

        T1, T2 = Tex("+1 Segundo").next_to(Store1, RIGHT).shift(0.5*RIGHT), Tex("+1 Segundo").next_to(Load, RIGHT).shift(0.5*RIGHT)

        self.play(Store1.animate.set_color(YELLOW), Write(T1), Transform(TotalTime, TotalTime1))
        self.wait(0.5)
        self.play(Store1.animate.set_opacity(0.5), Load.animate.set_color(YELLOW), Write(T2), Transform(TotalTime, TotalTime2))
        self.wait(0.25)
        self.play(Load.animate.set_opacity(0.5))
        self.wait()

    def WeHaveProblem(self):
        Tittle = Tex("A = 0").scale(3).set_color(RED)
        self.play(Write(Tittle), run_time=4)

        self.wait(6)

        P1, P2, P3, P4, P5 = Circle(1, RED), Circle(1, BLUE), Circle(1, GREEN), Circle(1, YELLOW), Circle(1, PURPLE)
        P2.next_to(P1, RIGHT)
        P3.next_to(P2, RIGHT)
        P4.next_to(P3, RIGHT)
        P5.next_to(P4, RIGHT)

        T1, T2, T3, T4, T5 = Tex("Process 1").set_color(RED), Tex("Process 2").set_color(BLUE), Tex("Process 3").set_color(GREEN), Tex("Process 4").set_color(YELLOW), Tex("Process 5").set_color(PURPLE)
        T1.scale(0.75).move_to(P1)
        T2.scale(0.75).move_to(P2)
        T3.scale(0.75).move_to(P3)
        T4.scale(0.75).move_to(P4)
        T5.scale(0.75).move_to(P5)

        P1, P2, P3, P4, P5 = VGroup(P1, T1), VGroup(P2, T2), VGroup(P3, T3), VGroup(P4, T4), VGroup(P5, T5)

        Queue = VGroup(P1, P2, P3, P4, P5).move_to(CENTER)

        self.play(FadeOut(Tittle), Write(Queue), run_time=3)

        self.wait(6)

        Queue.remove(P1)
        self.play(FadeOut(P1), Queue.animate.move_to(CENTER))

        self.wait(.25)

        Queue.remove(P2)
        self.play(FadeOut(P2), Queue.animate.move_to(CENTER))

        self.wait(.25)

        Queue.remove(P3)
        self.play(FadeOut(P3), Queue.animate.move_to(CENTER))

        self.wait(.25)

        Queue.remove(P4)
        self.play(FadeOut(P4), Queue.animate.move_to(CENTER))

        self.wait(.25)

        Queue.remove(P5)
        self.play(FadeOut(P5), Queue.animate.move_to(CENTER))

    def GoingInsideCPUAgain(self):
        ProcessColor = "#3fe685"
        CPU = SVGMobject("../Images/CPU.svg")

        ProcessArrow = Arrow(start=LEFT, end=2*RIGHT).set_color(ProcessColor)
        ProcessName = Tex("Proceso").next_to(ProcessArrow, UP).set_color(ProcessColor)
        Process = VGroup(ProcessArrow, ProcessName).move_to(CENTER).to_edge(LEFT)

        self.play(DrawBorderThenFill(CPU), Write(Process))

        self.play(Process.animate.next_to(CPU, LEFT, buff=0.2))

        self.wait()

        Store1 = Tex("sw", " !0, 0(!fp)")
        Load = Tex("lw", " !2, 0(!fp)").next_to(Store1, DOWN)
        Add = Tex("addiu", " !2, !2, 1").next_to(Load, DOWN)
        Store2 = Tex("sw", " !2, 0(!fp)").next_to(Add, DOWN)

        Store1[0].set_color(ORANGE)
        Load[0].set_color(ORANGE)
        Add[0].set_color(ORANGE)
        Store2[0].set_color(ORANGE)

        Assembly_Code = VGroup(Store1, Load, Add, Store2).move_to(CENTER)
        CodeBox = Rectangle(height=Assembly_Code.get_height()+0.5, width=Assembly_Code.get_width()+0.5).set_fill(BLUE, opacity=0.15)
        Assembly_Code += CodeBox

        TotalTime = Tex("Tiempo Disponible: 2 Segundos").next_to(CodeBox, UP).set_color(GREEN)
        TotalTime1, TotalTime2 = Tex("Tiempo Disponible: 1 Segundo").next_to(CodeBox, UP).set_color(BLUE), Tex("Tiempo Disponible: 0 Segundos").next_to(CodeBox, UP).set_color(RED)

        self.play(Write(Assembly_Code), FadeOut(CPU), FadeOut(Process), FadeIn(TotalTime))
        self.wait(.15)
        self.play(Store1.animate.set_color(YELLOW).set_opacity(0.5), Load.animate.set_color(YELLOW).set_opacity(0.5))

        self.wait(5)

        T1, T2 = Tex("+1 Segundo").next_to(Add, RIGHT).shift(0.5*RIGHT), Tex("+1 Segundo").next_to(Store2, RIGHT).shift(0.7*RIGHT)

        self.play(Add.animate.set_color(YELLOW), Write(T1), Transform(TotalTime, TotalTime1))
        self.wait(0.5)
        self.play(Add.animate.set_opacity(0.5), Store2.animate.set_color(YELLOW), Write(T2), Transform(TotalTime, TotalTime2))
        self.wait(0.25)
        self.play(Store2.animate.set_opacity(0.5))
        self.wait()

    def RegistersProblem(self):
        P1_Color, P2_Color, P3_Color = "#3fe685", "#ee4d55", "#4dd4ee"
        P4_Color, P5_Color, P6_Color = "#3fe685", "#ee4d55", "#4dd4ee"
        CPU = SVGMobject("../Images/CPU.svg")

        P1, P2, P3 = Arrow(start=LEFT, end=RIGHT).set_color(P1_Color), Arrow(start=LEFT, end=RIGHT).set_color(P2_Color), Arrow(start=LEFT, end=RIGHT).set_color(P3_Color)
        P4, P5, P6 = Arrow(start=LEFT, end=RIGHT).set_color(P4_Color), Arrow(start=LEFT, end=RIGHT).set_color(P5_Color), Arrow(start=LEFT, end=RIGHT).set_color(P6_Color)
        T1, T2, T3 = Tex("Proceso", " 3").next_to(P1, LEFT), Tex("Proceso", " 1").next_to(P2, LEFT), Tex("Proceso", " 2").next_to(P3, LEFT)
        T4, T5, T6 = Tex("Proceso", " 1").next_to(P4, LEFT), Tex("Proceso", " 3").next_to(P5, LEFT), Tex("Proceso", " 2").next_to(P6, LEFT)
        T1[1].set_color(P1_Color)
        T2[1].set_color(P2_Color)
        T3[1].set_color(P3_Color)
        T4[1].set_color(P4_Color)
        T5[1].set_color(P5_Color)
        T6[1].set_color(P6_Color)

        P1, P2, P3, P4, P5, P6 = VGroup(P1, T1), VGroup(P2, T2), VGroup(P3, T3), VGroup(P4, T4), VGroup(P5, T5), VGroup(P6, T6)
        Process = VGroup(P1, P2, P3, P4, P5, P6).to_edge(LEFT)

        self.add_foreground_mobjects(CPU)

        self.play(DrawBorderThenFill(CPU), Write(P1))

        self.wait()

        self.play(FadeIn(P2), P1.animate.to_edge(RIGHT).shift(5*RIGHT), run_time=3)

        self.wait()

        self.play(FadeIn(P3), P2.animate.to_edge(RIGHT).shift(5*RIGHT), run_time=3)

        self.wait()

        self.play(FadeIn(P4), P3.animate.to_edge(RIGHT).shift(5*RIGHT), run_time=3)

        self.wait()

        self.play(FadeIn(P5), P4.animate.to_edge(RIGHT).shift(5*RIGHT), run_time=3)

        self.wait()

        self.play(FadeIn(P6), P5.animate.to_edge(RIGHT).shift(5*RIGHT), run_time=3)

        self.wait()

        self.play(P6.animate.to_edge(RIGHT).shift(5*RIGHT), run_time=3)

        self.wait(.25)

        self.play(Uncreate(P6), Uncreate(CPU))

    def TheContextSwitch(self):
        Color1, Color2 = "#4DEE7E", "#A74DEE"
        Tittle = Tex("Context", " Switch").scale(2.5)

        self.play(Write(Tittle), run_time=2)

        self.wait(.25)

        self.play(Tittle[0].animate.set_color(Color1), run_time=0.35)
        self.play(Tittle[1].animate.set_color(Color2), run_time=0.35)

        self.wait(.25)

        self.play(FadeOut(Tittle))

        CPU = SVGMobject("../Images/CPU.svg")
        Process = Arrow(start=LEFT, end=RIGHT).to_edge(LEFT)

        CPU_Brace = Brace(CPU, direction=UP)
        Brace_Text = Tex("Usar la CPU").next_to(CPU_Brace, UP)
        Brace_Text1, Brace_Text2 = Tex("Recuperar Estado").next_to(CPU_Brace, UP), Tex("Guardar Estado").next_to(CPU_Brace, UP)

        self.play(FadeIn(Process), FadeIn(CPU))
        self.play(Process.animate.move_to(CPU).set_opacity(0))

        self.wait(.25)

        self.play(Write(Brace_Text2))

        self.wait(1.5)

        self.play(Process.animate.to_edge(RIGHT).set_opacity(1).shift(2*RIGHT), FadeOut(Brace_Text2))

        self.wait(3)

        Process.to_edge(LEFT)

        self.play(Process.animate.next_to(CPU, LEFT).set_opacity(1), Write(Brace_Text1)) # Proceso al lado de la CPU (Entrando)
        self.wait(.75)
        self.play(Process.animate.move_to(CPU).set_opacity(0), FadeOut(Brace_Text1), FadeIn(Brace_Text)) # Proceso dentro de la CPU
        self.wait(.75)
        self.play(Process.animate.next_to(CPU, RIGHT).set_opacity(1), FadeOut(Brace_Text), FadeIn(Brace_Text2)) # Proceso al lado de la CPU (Saliendo)
        self.wait(.75)
        self.play(Process.animate.to_edge(RIGHT).set_opacity(0).shift(2*RIGHT), Uncreate(Brace_Text2))
        self.wait(.75)

    def ProcessControlBlock(self):
        Tittle = Tex("Process", " Control ", "Block").scale(2).set_opacity(0.5)
        Tittle[0].set_color("#4dcff9")
        Tittle[1].set_color("#f94da4")
        Tittle[2].set_color("#f4f94d")

        self.play(Write(Tittle), run_time=3.75)
        self.wait(.25)
        self.play(Tittle[0].animate.set_opacity(1), run_time=.5)
        self.play(Tittle[1].animate.set_opacity(1), run_time=.5)
        self.play(Tittle[2].animate.set_opacity(1), run_time=.5)

        self.wait(.25)

        self.play(Tittle.animate.scale(0.5).to_edge(UP))

        PCB = Rectangle(height=5, width=4).shift(Tittle.height*DOWN)
        BlockBrace = Brace(PCB, direction=RIGHT)
        BraceText = Tex("Cada", " proceso ", "tiene su", " bloque").scale(0.5).rotate(DEGREES*(-90)).next_to(BlockBrace, RIGHT)
        BraceText[1].set_color("#4dcff9")
        BraceText[3].set_color("#f4f94d")
        PCB_Brace = VGroup(BlockBrace, BraceText)

        self.play(Write(PCB), run_time=2)

        self.play(Write(PCB_Brace), run_time=3)

        self.wait(3)

        PCB1 = Rectangle(height=1, width=4).move_to(PCB.get_corner(UL)).shift(RIGHT*(PCB.width/2)).shift(0.5*DOWN)
        PCB2 = Rectangle(height=1, width=4).next_to(PCB1, DOWN, buff=0)
        PCB3 = Rectangle(height=1, width=4).next_to(PCB2, DOWN, buff=0)
        PCB4 = Rectangle(height=1, width=4).next_to(PCB3, DOWN, buff=0)
        PCB5 = Rectangle(height=1, width=4).next_to(PCB4, DOWN, buff=0)

        T1 = Tex("Estado Actual").scale(0.75).move_to(PCB1)
        T2 = Tex("Indentificador").scale(0.75).move_to(PCB2)
        T3 = Tex("Instrucción Actual").scale(0.75).move_to(PCB3)
        T4 = Tex("Registros").scale(0.75).move_to(PCB4)
        T5 = Tex(". . . .").scale(0.75).move_to(PCB5)

        PCB_Content = VGroup(PCB1, PCB2, PCB3, PCB4, PCB5)
        PCB_Text = VGroup(T1, T2, T3, T4, T5)

        PCB_Data = VGroup(PCB_Content, PCB_Text)

        self.play(Write(PCB_Data), run_time=10)

        self.wait()

    def ConstructScene(self, useAudio=True):
        # if useAudio: self.add_sound("../Audio/4.1-Context Switch.mp3")
        # self.SmallCode()

        # if useAudio: self.add_sound("../Audio/4.2-Context Switch.mp3")
        # self.SmallAssemblyCode()

        # if useAudio: self.add_sound("../Audio/4.3-Context Switch.mp3")
        # self.QuantumTime()

        # if useAudio: self.add_sound("../Audio/4.4-Context Switch.mp3")
        # self.WorkingOnCPU()

        # if useAudio: self.add_sound("../Audio/4.5-Context Switch.mp3")
        # self.WeHaveProblem()

        # if useAudio: self.add_sound("../Audio/4.6-Context Switch.mp3")
        # self.GoingInsideCPUAgain()

        # if useAudio: self.add_sound("../Audio/4.7-Context Switch.mp3")
        # self.RegistersProblem()

        # if useAudio: self.add_sound("../Audio/4.8-Context Switch.mp3")
        # self.TheContextSwitch()

        if useAudio: self.add_sound("../Audio/4.9-Context Switch.mp3")
        self.ProcessControlBlock()

    def construct(self): self.ConstructScene()
