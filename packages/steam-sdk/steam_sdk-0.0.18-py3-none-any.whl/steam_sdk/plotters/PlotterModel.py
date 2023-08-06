import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.utils.misc import displayWaitAndClose



def plotterModel(data, titles, labels, types, texts, size):
    """
        Default plotter for most standard and simple cases
    """

    # Define style
    selectedFont = {'fontname': 'DejaVu Sans', 'size': 14}  # Define style for plots

    fig, axs = plt.subplots(nrows=1, ncols=len(data), figsize=size)
    if len(data) == 1:
        axs = [axs]
    for ax, ty, d, ti, l, te in zip(axs, types, data, titles, labels, texts):
        if ty == 'scatter':
            plot = ax.scatter(d['x'], d['y'], s=2, c=d['z'], cmap='jet')  # =cm.get_cmap('jet'))
            if len(te["t"]) != 0:
                for x, y, z in zip(te["x"], te["y"], te["t"]):
                    ax.text(x, y, z)
        elif ty == 'plot':
            pass  # TODO make non scatter plots work. Some of non-scater plots are quite specific. Might be better off with a separate plotter
        ax.set_xlabel(l["x"], **selectedFont)
        ax.set_ylabel(l["y"], **selectedFont)
        ax.set_title(f'{ti}', **selectedFont)
        # ax.set_aspect('equal')
        # ax.figure.autofmt_xdate()
        cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(plot, cax=cax, orientation='vertical')
        if len(l["z"]) != 0:
            cbar.set_label(l["z"], **selectedFont)
    plt.tight_layout()
    plt.show()

    # Show plots in Pycharm, wait a certain time, alert time is up, and close the window
    displayWaitAndClose(waitTimeBeforeMessage=.1, waitTimeAfterMessage=10)  # Show plots in Pycharm, wait a certain time, alert time is up, and close the window


def plot_field(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    """
    Plot magnetic field components of a coil
    """
    data = [{'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.I},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.Bx},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.By},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.B}]
    titles = ['Current [A]', 'Br [T]', 'Bz [T]', 'Bmod [T]']
    labels = [{'x': "r (m)", 'y': "z (m)", 'z': ""}] * len(data)
    types = ['scatter'] * len(data)
    texts = [builder_model.text] * len(data)
    plotterModel(data, titles, labels, types, texts, (15, 5))


def plot_strands_groups_layers(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    types = ['scatter'] * 4
    data = [{'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.strandToHalfTurn},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.strandToGroup},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.halfTurnToTurn},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.nS}]
    titles = ['strandToHalfTurn', 'strandToGroup', 'halfTurnToTurn', 'Number of strands per half-turn']
    labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Half-turn [-]"},
              {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
              {'x': "r (m)", 'y': "z (m)", 'z': "Turn [-]"},
              {'x': "r (m)", 'y': "z (m)", 'z': "Number of  strands per cable [-]"}]
    t_ht = copy.deepcopy(builder_model.text)
    for ht in range(builder_model.nHalfTurns):
        t_ht['x'].append(builder_model.x_ave[ht])
        t_ht['y'].append(builder_model.y_ave[ht])
        t_ht['t'].append('{}'.format(ht + 1))
    t_ng = copy.deepcopy(builder_model.text)
    for g in range(builder_model.nGroups):
        t_ng['x'].append(builder_model.x_ave_group[g])
        t_ng['y'].append(builder_model.y_ave_group[g])
        t_ng['t'].append('{}'.format(g + 1))
    texts = [t_ht, t_ng, builder_model.text, builder_model.text]
    plotterModel(data, titles, labels, types, texts, (15, 5))


def plot_polarities(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    polarities_inStrand = np.zeros((1, builder_model.nStrands), dtype=int)
    polarities_inStrand = polarities_inStrand[0]
    for g in range(1, builder_model.nGroupsDefined + 1):
        polarities_inStrand[np.where(builder_model.strandToGroup == g)] = builder_model.polarities_inGroup[g - 1]
    data = [{'x': builder_model.x, 'y': builder_model.y, 'z': polarities_inStrand}]
    titles = ['Current polarities']
    labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Polarity [-]"}]
    types = ['scatter'] * len(data)
    texts = [builder_model.text] * len(data)
    plotterModel(data, titles, labels, types, texts, (5, 5))


def plot_half_turns(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    data = [{'x': builder_model.x_ave, 'y': builder_model.y_ave, 'z': builder_model.HalfTurnToGroup},
            {'x': builder_model.x_ave, 'y': builder_model.y_ave, 'z': builder_model.HalfTurnToCoilSection},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.strandToGroup},
            {'x': builder_model.x, 'y': builder_model.y, 'z': builder_model.strandToCoilSection}]
    titles = ['HalfTurnToGroup', 'HalfTurnToCoilSection', 'StrandToGroup', 'StrandToCoilSection']
    labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
              {'x': "r (m)", 'y': "z (m)", 'z': "Coil section [-]"},
              {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
              {'x': "r (m)", 'y': "z (m)", 'z': "Coil Section [-]"}]
    types = ['scatter'] * len(data)
    texts = [builder_model.text] * len(data)
    plotterModel(data, titles, labels, types, texts, (15, 5))


def plot_nonlin_induct(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    f = plt.figure(figsize=(7.5, 5))
    plt.plot(builder_model.fL_I, builder_model.fL_L, 'ro-')
    plt.xlabel('Current [A]', **builder_model.selectedFont)
    plt.ylabel('Factor scaling nominal inductance [-]', **builder_model.selectedFont)
    plt.title('Differential inductance versus current', **builder_model.selectedFont)
    plt.xlim([0, builder_model.I00 * 2])
    plt.grid(True)
    plt.rcParams.update({'font.size': 12})
    plt.show()


def plot_psu_and_trig(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    ps = builder_model.model_data.Power_Supply
    ee = builder_model.model_data.Quench_Protection.Energy_Extraction
    qh = builder_model.model_data.Quench_Protection.Quench_Heaters
    cl = builder_model.model_data.Quench_Protection.CLIQ

    # Plot
    f = plt.figure(figsize=(7.5, 5))
    plt.plot([ps.t_off, ps.t_off],         [0, 1], 'k--', linewidth=4.0, label='t_PC')
    plt.plot([ee.t_trigger, ee.t_trigger], [0, 1], 'r--', linewidth=4.0, label='t_EE')
    plt.plot([cl.t_trigger, cl.t_trigger], [0, 1], 'g--', linewidth=4.0, label='t_CLIQ')
    plt.plot([np.min(qh.t_trigger), np.min(qh.t_trigger)], [0, 1], 'b:', linewidth=2.0, label='t_QH')
    plt.xlabel('Time [s]', **builder_model.selectedFont)
    plt.ylabel('Trigger [-]', **builder_model.selectedFont)
    plt.xlim([1E-4, builder_model.time_vector_params[-1]])
    plt.title('Power suppply and quench protection triggers', **builder_model.selectedFont)
    plt.grid(True)
    plt.rcParams.update({'font.size': 12})
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()


# def plot_quench_prop_and_resist(builder_model: BuilderModel = BuilderModel(flag_build=False)):
#     f = plt.figure(figsize=(16, 6))
#     plt.subplot(1, 4, 1)
#     # fig, ax = plt.subplots()
#     plt.scatter(builder_model.x_ave * 1000, builder_model.y_ave * 1000, s=2, c=builder_model.vQ_iStartQuench)
#     plt.xlabel('x [mm]', **builder_model.selectedFont)
#     plt.ylabel('y [mm]', **builder_model.selectedFont)
#     plt.title('2D cross-section Quench propagation velocity', **builder_model.selectedFont)
#     plt.set_cmap('jet')
#     plt.grid('minor', alpha=0.5)
#     cbar = plt.colorbar()
#     cbar.set_label('Quench velocity [m/s]', **builder_model.selectedFont)
#     plt.rcParams.update({'font.size': 12})
#     # plt.axis('equal')
#
#     plt.subplot(1, 4, 2)
#     plt.scatter(builder_model.x_ave * 1000, builder_model.y_ave * 1000, s=2, c=builder_model.rho_ht_10K)
#     plt.xlabel('x [mm]', **builder_model.selectedFont)
#     plt.ylabel('y [mm]', **builder_model.selectedFont)
#     plt.title('Resistivity', **builder_model.selectedFont)
#     plt.set_cmap('jet')
#     plt.grid('minor', alpha=0.5)
#     cbar = plt.colorbar()
#     cbar.set_label('Resistivity [$\Omega$*m]', **builder_model.selectedFont)
#     plt.rcParams.update({'font.size': 12})
#     # plt.axis('equal')
#
#     plt.subplot(1, 4, 3)
#     plt.scatter(builder_model.x_ave * 1000, builder_model.y_ave * 1000, s=2, c=builder_model.r_el_ht_10K)
#     plt.xlabel('x [mm]', **builder_model.selectedFont)
#     plt.ylabel('y [mm]', **builder_model.selectedFont)
#     plt.title('Resistance per unit length', **builder_model.selectedFont)
#     plt.set_cmap('jet')
#     plt.grid('minor', alpha=0.5)
#     cbar = plt.colorbar()
#     cbar.set_label('Resistance per unit length [$\Omega$/m]', **builder_model.selectedFont)
#     plt.rcParams.update({'font.size': 12})
#     # plt.axis('equal')
#
#     plt.subplot(1, 4, 4)
#     plt.scatter(builder_model.x_ave * 1000, builder_model.y_ave * 1000, s=2, c=builder_model.tQuenchDetection * 1e3)
#     plt.xlabel('x [mm]', **builder_model.selectedFont)
#     plt.ylabel('y [mm]', **builder_model.selectedFont)
#     plt.title('Approximate quench detection time', **builder_model.selectedFont)
#     plt.set_cmap('jet')
#     plt.grid('minor', alpha=0.5)
#     cbar = plt.colorbar()
#     cbar.set_label('Time [ms]', **builder_model.selectedFont)
#     plt.rcParams.update({'font.size': 12})
#     # plt.axis('equal')
#     plt.show()


def plot_q_prop_v(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    f = plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    plt.plot(builder_model.mean_B_ht, builder_model.vQ_iStartQuench, 'ko')
    plt.xlabel('Average magnetic field in the half-turn [T]', **builder_model.selectedFont)
    plt.ylabel('Quench propagation velocity [m/s]', **builder_model.selectedFont)
    plt.title('Quench propagation velocity', **builder_model.selectedFont)
    plt.set_cmap('jet')
    plt.grid('minor', alpha=0.5)
    plt.rcParams.update({'font.size': 12})
    plt.subplot(1, 2, 2)
    plt.plot(builder_model.mean_B_ht, builder_model.tQuenchDetection * 1e3, 'ko')
    plt.xlabel('Average magnetic field in the half-turn [T]', **builder_model.selectedFont)
    plt.ylabel('Approximate quench detection time [ms]', **builder_model.selectedFont)
    plt.title('Approximate quench detection time', **builder_model.selectedFont)
    plt.set_cmap('jet')
    plt.grid('minor', alpha=0.5)
    plt.rcParams.update({'font.size': 12})
    plt.show()


def plot_electrical_order(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    plt.figure(figsize=(16, 8))
    plt.subplot(1, 3, 1)
    plt.scatter(builder_model.x_ave, builder_model.y_ave, s=2, c=np.argsort(builder_model.el_order_half_turns_Array))
    plt.xlabel('x [m]', **builder_model.selectedFont)
    plt.ylabel('y [m]', **builder_model.selectedFont)
    plt.title('Electrical order of the half-turns', **builder_model.selectedFont)
    plt.set_cmap('jet')
    cbar = plt.colorbar()
    cbar.set_label('Electrical order [-]', **builder_model.selectedFont)
    plt.rcParams.update({'font.size': 12})
    plt.axis('equal')
    # Plot
    plt.subplot(1, 3, 2)
    plt.plot(builder_model.x_ave[builder_model.el_order_half_turns_Array - 1], builder_model.y_ave[builder_model.el_order_half_turns_Array - 1], 'k')
    plt.scatter(builder_model.x_ave, builder_model.y_ave, s=2, c=builder_model.nS)
    plt.scatter(builder_model.x_ave[builder_model.el_order_half_turns_Array[0] - 1],
                builder_model.y_ave[builder_model.el_order_half_turns_Array[0] - 1], s=50, c='r',
                label='Positive lead')
    plt.scatter(builder_model.x_ave[builder_model.el_order_half_turns_Array[-1] - 1],
                builder_model.y_ave[builder_model.el_order_half_turns_Array[-1] - 1], s=50, c='b',
                label='Negative lead')
    plt.xlabel('x [m]', **builder_model.selectedFont)
    plt.ylabel('y [m]', **builder_model.selectedFont)
    plt.title('Electrical order of the half-turns', **builder_model.selectedFont)
    plt.rcParams.update({'font.size': 12})
    plt.axis('equal')
    plt.legend(loc='lower left')
    # Plot
    plt.subplot(1, 3, 3)
    # plt.plot(x_ave_group[elPairs_GroupTogether_Array[:,0]-1],y_ave_group[elPairs_GroupTogether_Array[:,1]-1],'b')
    plt.scatter(builder_model.x, builder_model.y, s=2, c='k')
    plt.scatter(builder_model.x_ave_group, builder_model.y_ave_group, s=10, c='r')
    plt.xlabel('x [m]', **builder_model.selectedFont)
    plt.ylabel('y [m]', **builder_model.selectedFont)
    plt.title('Electrical order of the groups (only go-lines)', **builder_model.selectedFont)
    plt.rcParams.update({'font.size': 12})
    plt.axis('equal')
    plt.show()


def plot_heat_exchange_order(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    plt.figure(figsize=(10, 10))
    # plot strand positions
    plt.scatter(builder_model.x, builder_model.y, s=2, c='b')
    # plot conductors
    # for c, (cXPos, cYPos) in enumerate(zip(xPos, yPos)):
    #     pt1, pt2, pt3, pt4 = (cXPos[0], cYPos[0]), (cXPos[1], cYPos[1]), (cXPos[2], cYPos[2]), (cXPos[3], cYPos[3])
    #     line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k', alpha=.25)
    #     plt.gca().add_line(line)
    # plot average conductor positions
    # plt.scatter(x_ave, y_ave, s=10, c='r')
    # plot heat exchange links along the cable narrow side
    for i in range(len(builder_model.iContactAlongHeight_From)):
        plt.plot([builder_model.x_ave[builder_model.iContactAlongHeight_From_Array[i] - 1],
                  builder_model.x_ave[builder_model.iContactAlongHeight_To_Array[i] - 1]],
                 [builder_model.y_ave[builder_model.iContactAlongHeight_From_Array[i] - 1],
                  builder_model.y_ave[builder_model.iContactAlongHeight_To_Array[i] - 1]], 'k')
    # plot heat exchange links along the cable wide side
    for i in range(len(builder_model.iContactAlongWidth_From)):
        plt.plot([builder_model.x_ave[builder_model.iContactAlongWidth_From_Array[i] - 1],
                  builder_model.x_ave[builder_model.iContactAlongWidth_To_Array[i] - 1]],
                 [builder_model.y_ave[builder_model.iContactAlongWidth_From_Array[i] - 1],
                  builder_model.y_ave[builder_model.iContactAlongWidth_To_Array[i] - 1]], 'r')
    # plot strands belonging to different conductor groups and clo ser to each other than max_distance
    # for p in pairs_close:
    #     if not strandToGroup[p[0]] == strandToGroup[p[1]]:
    #         plt.plot([X[p[0], 0], X[p[1], 0]], [X[p[0], 1], X[p[1], 1]], c='g')
    plt.xlabel('x [m]', **builder_model.selectedFont)
    plt.ylabel('y [m]', **builder_model.selectedFont)
    plt.title('Heat exchange order of the half-turns', **builder_model.selectedFont)
    plt.rcParams.update({'font.size': 12})
    plt.axis('equal')
    plt.show()


def plot_power_supl_contr(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    plt.figure(figsize=(5, 5))
    plt.plot([builder_model.t_PC, builder_model.t_PC], [np.min(builder_model.I_PC_LUT), np.max(builder_model.I_PC_LUT)], 'k--', linewidth=4.0,
             label='t_PC')
    plt.plot(builder_model.t_PC_LUT, builder_model.I_PC_LUT, 'ro-', label='LUT')
    plt.xlabel('Time [s]', **builder_model.selectedFont)
    plt.ylabel('Current [A]', **builder_model.selectedFont)
    plt.title('Look-up table controlling power supply', **builder_model.selectedFont)
    plt.grid(True)
    plt.rcParams.update({'font.size': 12})
    plt.show()


def plot_all(builder_model: BuilderModel = BuilderModel(flag_build=False)):
    '''
        Plot all default plots
    '''
    # # plot_field(builder_model)
    # plot_polarities(builder_model)
    # plot_strands_groups_layers(builder_model)
    # plot_electrical_order(builder_model)
    # plot_q_prop_v(builder_model)
    # # plot_quench_prop_and_resist(builder_model)
    plot_psu_and_trig(builder_model)
    # plot_half_turns(builder_model)
    # plot_heat_exchange_order(builder_model)
    # plot_nonlin_induct(builder_model)
    # plot_power_supl_contr(builder_model)