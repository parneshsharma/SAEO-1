import random
import wsnsimpy.wsnsimpy_tk as wsp

def run(x_value, y_value, n_V, r, BS, col_n,n_r,Final_path,dead_vehicle,Vehicle):

    n_r=n_r+1
    class MyNode(wsp.Node):
        tx_range = 50

        ###################
        def run(self):  # loop until Vehicles
            yield self.timeout(3)  # shows created Vehicles


            if self.id is BS:
                self.scene.nodecolor(self.id, 0, 0, 0)  # if Vehicle is Base station, Vehicle color => black, with width 15
                self.scene.nodewidth(self.id, 15)
            else:
                for i in range(len(dead_vehicle)):  # dead node will be disabled
                    if (self.id is dead_vehicle[i]) and (self.id != 0):
                        self.scene.nodecolor(self.id, .7, .7, .7)  # else, node color => grey (disable)
            for i in range(n_r):
                if self.id is i:

                    self.scene.nodecolor(self.id, R[i], G[i],
                                         B[i])  # displays Vehicle in
                self.scene.nodewidth(self.id, nod_wid)
            for i in range(len(Final_path) - 1):
                 if self.id is Final_path[i]:
                     self.start_process(self.start_send_data(Final_path[i + 1]))  # source, destination


        ###################
        def start_send_data(self, dest):
            #
            seq = 0

            while True:
                yield self.timeout(0.5)  # transmission will be displayed after 0.5s
                self.scene.clearlinks()
                d = random.uniform(.3, .35)  # uniform value between 0.5 - 0.6
                yield self.timeout(d)  # timeout of the link between nodes
                self.send_data(dest)  ##################source, dest
                seq += 1

        ###################
        def send_data(self, dest):
            self.send(dest, msg='data', src=self.id)


    WS = col_n * 70  # window size
    nod_wid = 2  # width of Vehicle
    R, G, B = [1, 0, 0.8, 1, 0.6, 0.2, 1], [0, 0.4, 0.5, 0, 0, 0, 0.3], [0, 0, 0.1, 0.5, 0.7, 0.3,
                                                                         0]  # color for clusters

    # simulation will display for 30s
    sim = wsp.Simulator(until=15, timescale=1, visual=True, terrain_size=(WS, WS), title="NUmber of Vehicles " + str(
        n_V))  # simulation window (30s,True - to display, ter -- wnd. size, tit -- wnd. title)

    for i in range(len(x_value)):  # x columns1
        px, py = x_value[i], y_value[i]
        Vehicles = sim.add_node(MyNode, (px, py))  # create Vehicles at (px,py)

    # start the simulation
    sim.run()
