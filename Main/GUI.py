import PySimpleGUI as sg
from Main import Run, simulation

sg.change_look_and_feel('DarkTeal6')  # for default look and feel

# Designing layout
layout = [[sg.Text("\n")],
          [sg.Text("\t\t\tDataset\t         "), sg.Combo(['highcost_H3','highcost_H6','lowcost_H3','lowcost_H6'], size=(13, 20)), sg.Text("\n")],
          [sg.Text("\t\t\tNo.of Vehicles   "), sg.Combo(['50','100','150','200']),sg.Button("START", size=(10, 1))],
          [sg.Text("\n")],
          [sg.Text("\t\t\t\t  GL+Deep RL\t     KSMIRP\t     Augmented TS+DE\t Integrated location inventory routing  \tProposed_SAEO_DQNN")],
          [sg.Text('\tTransportation Cost'), sg.In(key='11', size=(20, 20)), sg.In(key='12', size=(20, 20)),
           sg.In(key='13', size=(20, 20)), sg.In(key='14', size=(20, 20)), sg.In(key='15', size=(20, 20))],
          [sg.Text('\tTotal Cost\t'), sg.In(key='21', size=(20, 20)), sg.In(key='22', size=(20, 20)),
           sg.In(key='23', size=(20, 20)), sg.In(key='24', size=(20, 20)),sg.In(key='25', size=(20, 20))],
          [sg.Text('\tTranshipment Cost '), sg.In(key='31', size=(20, 20)), sg.In(key='32', size=(20, 20)),
           sg.In(key='33', size=(20, 20)), sg.In(key='34', size=(20, 20)),sg.In(key='35', size=(20, 20))],
          [sg.Text("\t\t\t\t\t\t\t\t\t\t\t\t\t       "),  sg.Button('Close', size=(10, 1))],
          [sg.Text("")]]


# Create the Window layout
window = sg.Window('SNAKE Optimazation Artificial Eco system', layout)

# event loop
while True:
    event, value = window.read()  # displays the window
    if event == "START":
        dataset,Vehicles = value[0],int(value[1])
        Transportation_Cost, Total_Cost, Transhipment_Cost, SR = Run.callmain(dataset,Vehicles)


        window.element('11').Update(Transportation_Cost[0])
        window.element('12').Update(Transportation_Cost[1])
        window.element('13').Update(Transportation_Cost[2])
        window.element('14').Update(Transportation_Cost[3])
        window.element('15').Update(Transportation_Cost[4])


        window.element('21').Update(Total_Cost[0])
        window.element('22').Update(Total_Cost[1])
        window.element('23').Update(Total_Cost[2])
        window.element('24').Update(Total_Cost[3])
        window.element('25').Update(Total_Cost[4])

        window.element('31').Update(Transhipment_Cost[0])
        window.element('32').Update(Transhipment_Cost[1])
        window.element('33').Update(Transhipment_Cost[2])
        window.element('34').Update(Transhipment_Cost[3])
        window.element('35').Update(Transhipment_Cost[4])



        print("\nRunning Simulation.")
        simulation.run(SR[0], SR[1], SR[2], SR[3], SR[4], SR[5], SR[6],SR[7],SR[8],Vehicles)


    if event == 'Close':
        window.close()
        break
