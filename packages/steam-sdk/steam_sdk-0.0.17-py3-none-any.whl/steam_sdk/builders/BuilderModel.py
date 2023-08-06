import os
from pathlib import Path
import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from steam_sdk.data.DataModel import *
from steam_sdk.data.DataRoxieParser import APIdata
from steam_sdk.builders.BuilderLEDET import BuilderLEDET
from steam_sdk.builders.BuilderSIGMA import BuilderSIGMA
from steam_sdk.builders.BuilderProteCCT import BuilderProteCCT
from steam_sdk.parsers.ParserLEDET import ParserLEDET, copy_modified_map2d_ribbon_cable, copy_map2d
from steam_sdk.parsers.ParserProteCCT import ParserProteCCT
from steam_sdk.parsers.ParserRoxie import ParserRoxie
from steam_sdk.parsers.ParserMap2d import getParametersFromMap2d
from steam_sdk.utils.misc import displayWaitAndClose


class BuilderModel:
    """
        Class to generate STEAM models, which can be later on written to input files of supported programs
    """

    def __init__(self,
                 file_model_data: str = None, software: List[str] = None, relative_path_settings: str = '',
                 flag_build: bool = True, flag_dump_all: bool = False, flag_json: bool = False,
                 dump_all_path: str = '', output_path: str = '',
                 verbose: bool = False, flag_plot_all: bool = False):
        """
            Builder object to generate models from STEAM simulation tools specified by user

            output_path: path to the output models
            dump_all_path: path to the final yaml file
        """

        # Unpack arguments
        self.software: List[str] = software
        if not self.software: self.software = []  # This avoids error when None is passed to software # TODO: Verify this is sound coding
        self.file_model_data: str = file_model_data
        self.relative_path_settings: str = relative_path_settings
        self.flag_build = flag_build
        self.flag_dump_all: bool = flag_dump_all
        self.flag_plot_all: bool = flag_plot_all
        self.flag_json: bool = flag_json
        self.dump_all_path: str = dump_all_path  # TODO Merge dump_all_path and output_path ?
        self.output_path: str = output_path
        self.verbose: bool = verbose

        # Initialize
        self.model_data: DataModel = DataModel()
        self.roxie_data: APIdata = APIdata()
        self.path_magnet   = None
        self.path_data     = None
        self.path_cadata   = None
        self.path_iron     = None
        self.path_map2d    = None
        self.path_settings = None

        # Define plot style
        self.selectedFont = {'fontname': 'DejaVu Sans', 'size': 14}  # Define style for plots


        # If flag_build set true, the model will be generated during the initialization
        if flag_build:
            if self.verbose:
                print('output_path: {}'.format(self.output_path))

            # If the output folder is not an empty string, and it does not exist, make it
            if self.output_path != '' and not os.path.isdir(self.output_path):
                print("Output folder {} does not exist. Making it now".format(self.output_path))
                Path(self.output_path).mkdir(parents=True)

            # Load model data from the input .yaml file
            self.loadModelData()

            # Set paths of input files and settings
            self.set_input_paths()

            # Load model data from the input ROXIE files
            self.loadRoxieData()

            if 'LEDET' in self.software:
                self.buildLEDET()

            if 'SIGMA' in self.software:
                self.buildSIGMA()

            if 'ProteCCT' in self.software:
                self.buildProteCCT()

            if flag_dump_all:
                self.dumpAll()

            if flag_plot_all:
                self.plot_all()


    def set_input_paths(self):
        """
            Sets input paths and displays related information
        """
        # TODO: Add test for this method

        # Find folder where the input file is located, which will be used as the "anchor" for all input files
        self.path_magnet = Path(self.file_model_data).parent

        # Set a few paths relative to the "anchor" path
        # If input paths are not defined, their value remains to their default None
        # The construct Path(x / y).resolve() allows defining relative paths in the .yaml input file
        if self.model_data.Sources.coil_fromROXIE:
            self.path_data = Path(self.path_magnet / self.model_data.Sources.coil_fromROXIE).resolve()
        if self.model_data.Sources.magnetic_field_fromROXIE:
            self.path_map2d = Path(self.path_magnet / self.model_data.Sources.magnetic_field_fromROXIE).resolve()
        if self.model_data.Sources.conductor_fromROXIE:
            self.path_cadata = Path(self.path_magnet / self.model_data.Sources.conductor_fromROXIE).resolve()
        if self.model_data.Sources.iron_fromROXIE:
            self.path_iron = Path(self.path_magnet / self.model_data.Sources.iron_fromROXIE).resolve()

        # Set settings path
        # Find user name
        user_name = 'user'  # till GitLab path problem is solved
        for environ_var in ['HOMEPATH', 'SWAN_HOME']:
            if environ_var in os.environ:
                user_name = os.path.basename(os.path.normpath(os.environ[environ_var]))

        # TODO: Change this logic with a tree structure depending on the current location, not the file location
        if self.relative_path_settings == '':
            self.path_settings = Path(os.getcwd())
        else:
            self.path_settings = Path(os.getcwd() / self.relative_path_settings).resolve()

        if Path.exists(Path.joinpath(self.path_settings, f"settings.{user_name}.yaml")):
            with open(Path.joinpath(self.path_settings, f"settings.{user_name}.yaml"), 'r') as stream:
                self.settings_dict = yaml.safe_load(stream)
        else:
            with open(Path.joinpath(Path(os.getcwd()).parent, "settings.user.yaml"), 'r') as stream:
                self.settings_dict = yaml.safe_load(stream)
            # raise Exception('Cannot find paths without settings file')

        # Display defined paths
        if self.verbose:
            print('These paths were set:')
            print('path_magnet:   {}'.format(self.path_magnet))
            print('path_cadata:   {}'.format(self.path_cadata))
            print('path_iron:     {}'.format(self.path_iron))
            print('path_map2d:    {}'.format(self.path_map2d))
            print('path_settings: {}'.format(self.path_settings))


    def loadModelData(self):
        """
            Loads model data from yaml file to model data object
        """
        if self.verbose:
            print('Loading .yaml file to model data object.')

        if not self.file_model_data:
            raise Exception('No .yaml path provided.')

        with open(self.file_model_data, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            self.model_data = DataModel(**dictionary_yaml)


    def loadRoxieData(self):
        """
            Apply roxie parser to fetch magnet information for the given magnet and stores in member variable
        """
        if not self.model_data:
            raise Exception('Model data not loaded to object.')

        # TODO: add option to set a default path if no path is provided
        #######################################
        # Alternative if provided path is wrong
        if self.path_iron is not None and not os.path.isfile(self.path_iron):
            print('Cannot find {}, will attempt to proceed without file'.format(self.path_iron))
            self.path_iron = None
        if self.path_data is not None and not os.path.isfile(self.path_data):
            print('Cannot find {}, will attempt to proceed without file'.format(self.path_data))
            self.path_data = None
        if self.path_cadata is not None and not os.path.isfile(self.path_cadata):
            print('Cannot find {}, will attempt to proceed without file'.format(self.path_cadata))
            self.path_cadata = None

        ############################################################
        # Load information from ROXIE input files using ROXIE parser
        roxie_parser = ParserRoxie()
        self.roxie_data = roxie_parser.getData(dir_data=self.path_data, dir_cadata=self.path_cadata, dir_iron=self.path_iron)

    def buildLEDET(self):
        """
            Building a LEDET model
        """
        magnet_name = self.model_data.GeneralParameters.magnet_name
        nameFileSMIC = os.path.join(self.output_path,
                                    magnet_name + '_selfMutualInductanceMatrix.csv')  # full path of the .csv file with self-mutual inductances to write

        # Copy/edit the ROXIE map2d file
        suffix = "_All"
        if self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 1:
            #     # [[...half_turn_length, Ribbon...n_strands],.....]
            # TODO: geometry when conductor has a combination of ribbon and non-ribbon cables

            nT_from_original_map2d, _, _, _, _, _, _, _ = getParametersFromMap2d(
                map2dFile=self.path_map2d, headerLines=self.model_data.Options_LEDET.field_map_files.headerLines,
                verbose=self.verbose)

            n_groups_original_file = len(nT_from_original_map2d)
            geometry_ribbon_cable = [[None, None]] * n_groups_original_file

            for i in range(n_groups_original_file):
                geometry_ribbon_cable[i][0] = self.model_data.Conductors[
                    self.model_data.CoilWindings.conductor_to_group[i] - 1].cable.n_strands  # layers
                geometry_ribbon_cable[i][1] = nT_from_original_map2d[i]  # number of half-turns

            if self.verbose:
                print('geometry_ribbon_cable: {}'.format(geometry_ribbon_cable))

            file_name_output = copy_modified_map2d_ribbon_cable(self.model_data.GeneralParameters.magnet_name,
                                                                self.path_map2d,
                                                                self.output_path, geometry_ribbon_cable,
                                                                self.model_data.Options_LEDET.field_map_files.flagIron,
                                                                self.model_data.Options_LEDET.field_map_files.flagSelfField,
                                                                suffix=suffix, verbose=self.verbose)

        elif self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 0 or self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == None:
            file_name_output = copy_map2d(self.model_data.GeneralParameters.magnet_name, self.path_map2d,
                                          self.output_path, self.model_data.Options_LEDET.field_map_files.flagIron,
                                          self.model_data.Options_LEDET.field_map_files.flagSelfField, suffix=suffix,
                                          verbose=self.verbose)

        self.map2d_file_modified = os.path.join(self.output_path, file_name_output)

        builder_ledet = BuilderLEDET(path_magnet=self.path_magnet, input_model_data=self.model_data,
                                     input_roxie_data=self.roxie_data, input_map2d=self.map2d_file_modified,
                                     smic_write_path=nameFileSMIC, flag_build=self.flag_build, verbose=self.verbose)

        # Write output excel file
        parser_ledet = ParserLEDET(builder_ledet)
        nameFileLEDET = os.path.join(self.output_path, magnet_name + '.xlsx')  # full path of the LEDET input file to write
        parser_ledet.writeLedet2Excel(nameFileLEDET=nameFileLEDET, verbose=self.verbose, SkipConsistencyCheck=True)

        # Write output json file
        if self.flag_json:
            nameFileLedetJson = os.path.join(self.output_path, magnet_name + '.json')  # full path of the LEDET input file to write
            parser_ledet.write2json(full_path_file_name=nameFileLedetJson, verbose=self.verbose, SkipConsistencyCheck=True)


    def buildProteCCT(self):
        """
            Building a ProteCCT model
        """
        magnet_name = self.model_data.GeneralParameters.magnet_name
        builder_protecct = BuilderProteCCT(input_model_data=self.model_data, flag_build=self.flag_build, verbose=self.verbose)

        # Write output excel file
        parser_protecct = ParserProteCCT(builder_protecct)
        nameFileProteCCT = os.path.join(self.output_path, magnet_name + '.xlsx')  # full path of the ProteCCT input file to write
        parser_protecct.writeProtecct2Excel(full_path_file_name=nameFileProteCCT, verbose=self.verbose, SkipConsistencyCheck=True)


    def buildSIGMA(self):
        """
            Building a SIGMA model
        """
        BuilderSIGMA(input_model_data=self.model_data, input_roxie_data=self.roxie_data,
                     settings_dict=self.settings_dict, output_path=self.output_path,
                     flag_build=self.flag_build, verbose=self.verbose)

    def dumpAll(self):
        """
            Writes model data and data from Roxie parser in a combined .yaml file
        """
        # TODO add one more layer for model_data and roxie_data
        if self.verbose:
            print('Writing model data and data from Roxie parser in a combined .yaml file')
        # TODO: add also data from BuilderLEDET, BulderSIGMA, etc

        all_data_dict = {**self.model_data.dict(), **self.roxie_data.dict()}

        # Define output folder
        if self.dump_all_path != '':
            dump_all_path = self.dump_all_path
        elif self.output_path != '':
            dump_all_path = self.output_path
        else:
            dump_all_path = ''

        # If the output folder is not an empty string, and it does not exist, make it
        if self.dump_all_path != '' and not os.path.isdir(self.dump_all_path):
            print("Output folder {} does not exist. Making it now".format(self.dump_all_path))
            Path(self.dump_all_path).mkdir(parents=True)

        # Write output .yaml file
        dump_all_full_path = os.path.join(dump_all_path, self.model_data.GeneralParameters.magnet_name +
                                          '_all_data.yaml')
        with open(dump_all_full_path, 'w') as outfile:
            yaml.dump(all_data_dict, outfile, default_flow_style=False, sort_keys=False)

    ####################### Plotter methods - START #######################
    def plotter(self, data, titles, labels, types, texts, size):
        """
        Default plotter for most standard and simple cases
        """

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
            ax.set_xlabel(l["x"], **self.selectedFont)
            ax.set_ylabel(l["y"], **self.selectedFont)
            ax.set_title(f'{ti}', **self.selectedFont)
            # ax.set_aspect('equal')
            # ax.figure.autofmt_xdate()
            cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(plot, cax=cax, orientation='vertical')
            if len(l["z"]) != 0:
                cbar.set_label(l["z"], **self.selectedFont)
        plt.tight_layout()
        plt.show()

    # def plot_field(self):
    #     """
    #     Plot magnetic field components of a coil
    #     """
    #     data = [{'x': self.x, 'y': self.y, 'z': self.I},
    #             {'x': self.x, 'y': self.y, 'z': self.Bx},
    #             {'x': self.x, 'y': self.y, 'z': self.By},
    #             {'x': self.x, 'y': self.y, 'z': self.B}]
    #     titles = ['Current [A]', 'Br [T]', 'Bz [T]', 'Bmod [T]']
    #     labels = [{'x': "r (m)", 'y': "z (m)", 'z': ""}] * len(data)
    #     types = ['scatter'] * len(data)
    #     texts = [self.text] * len(data)
    #     self.plotter(data, titles, labels, types, texts, (15, 5))
    #
    # def plot_strands_groups_layers(self):
    #     types = ['scatter'] * 4
    #     data = [{'x': self.x, 'y': self.y, 'z': self.strandToHalfTurn},
    #             {'x': self.x, 'y': self.y, 'z': self.strandToGroup},
    #             {'x': self.x, 'y': self.y, 'z': self.halfTurnToTurn},
    #             {'x': self.x, 'y': self.y, 'z': self.nS}]
    #     titles = ['strandToHalfTurn', 'strandToGroup', 'halfTurnToTurn', 'Number of strands per half-turn']
    #     labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Half-turn [-]"},
    #               {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
    #               {'x': "r (m)", 'y': "z (m)", 'z': "Turn [-]"},
    #               {'x': "r (m)", 'y': "z (m)", 'z': "Number of  strands per cable [-]"}]
    #     t_ht = copy.deepcopy(self.text)
    #     for ht in range(self.nHalfTurns):
    #         t_ht['x'].append(self.x_ave[ht])
    #         t_ht['y'].append(self.y_ave[ht])
    #         t_ht['t'].append('{}'.format(ht + 1))
    #     t_ng = copy.deepcopy(self.text)
    #     for g in range(self.nGroups):
    #         t_ng['x'].append(self.x_ave_group[g])
    #         t_ng['y'].append(self.y_ave_group[g])
    #         t_ng['t'].append('{}'.format(g + 1))
    #     texts = [t_ht, t_ng, self.text, self.text]
    #     self.plotter(data, titles, labels, types, texts, (15, 5))
    #
    # def plot_polarities(self):
    #     polarities_inStrand = np.zeros((1, self.nStrands), dtype=int)
    #     polarities_inStrand = polarities_inStrand[0]
    #     for g in range(1, self.nGroupsDefined + 1):
    #         polarities_inStrand[np.where(self.strandToGroup == g)] = self.polarities_inGroup[g - 1]
    #     data = [{'x': self.x, 'y': self.y, 'z': polarities_inStrand}]
    #     titles = ['Current polarities']
    #     labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Polarity [-]"}]
    #     types = ['scatter'] * len(data)
    #     texts = [self.text] * len(data)
    #     self.plotter(data, titles, labels, types, texts, (5, 5))
    #
    # def plot_half_turns(self):
    #     data = [{'x': self.x_ave, 'y': self.y_ave, 'z': self.HalfTurnToGroup},
    #             {'x': self.x_ave, 'y': self.y_ave, 'z': self.HalfTurnToCoilSection},
    #             {'x': self.x, 'y': self.y, 'z': self.strandToGroup},
    #             {'x': self.x, 'y': self.y, 'z': self.strandToCoilSection}]
    #     titles = ['HalfTurnToGroup', 'HalfTurnToCoilSection', 'StrandToGroup', 'StrandToCoilSection']
    #     labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
    #               {'x': "r (m)", 'y': "z (m)", 'z': "Coil section [-]"},
    #               {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
    #               {'x': "r (m)", 'y': "z (m)", 'z': "Coil Section [-]"}]
    #     types = ['scatter'] * len(data)
    #     texts = [self.text] * len(data)
    #     self.plotter(data, titles, labels, types, texts, (15, 5))
    #
    # def plot_nonlin_induct(self):
    #     f = plt.figure(figsize=(7.5, 5))
    #     plt.plot(self.fL_I, self.fL_L, 'ro-')
    #     plt.xlabel('Current [A]', **self.selectedFont)
    #     plt.ylabel('Factor scaling nominal inductance [-]', **self.selectedFont)
    #     plt.title('Differential inductance versus current', **self.selectedFont)
    #     plt.xlim([0, self.I00 * 2])
    #     plt.grid(True)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.show()

    def plot_psu_and_trig(self):
        ps = self.model_data.Power_Supply
        ee = self.model_data.Quench_Protection.Energy_Extraction
        qh = self.model_data.Quench_Protection.Quench_Heaters
        cl = self.model_data.Quench_Protection.CLIQ

        # Plot
        f = plt.figure(figsize=(7.5, 5))
        plt.plot([ps.t_off, ps.t_off], [0, 1], 'k--', linewidth=4.0, label='t_PC')
        plt.plot([ee.t_trigger, ee.t_trigger], [0, 1], 'r--', linewidth=4.0, label='t_EE')
        plt.plot([cl.t_trigger, cl.t_trigger], [0, 1], 'g--', linewidth=4.0, label='t_CLIQ')
        plt.plot([np.min(qh.t_trigger), np.min(qh.t_trigger)], [0, 1], 'b:', linewidth=2.0, label='t_QH')
        plt.xlabel('Time [s]', self.selectedFont)
        plt.ylabel('Trigger [-]', self.selectedFont)
        plt.xlim([1E-4, self.model_data.Options_LEDET.time_vector.time_vector_params[-1]])
        plt.title('Power suppply and quench protection triggers', self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.legend(loc='best')

        displayWaitAndClose(waitTimeBeforeMessage=.1, waitTimeAfterMessage=10)

    # def plot_quench_prop_and_resist(self):
    #     f = plt.figure(figsize=(16, 6))
    #     plt.subplot(1, 4, 1)
    #     # fig, ax = plt.subplots()
    #     plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.vQ_iStartQuench)
    #     plt.xlabel('x [mm]', **self.selectedFont)
    #     plt.ylabel('y [mm]', **self.selectedFont)
    #     plt.title('2D cross-section Quench propagation velocity', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     plt.grid('minor', alpha=0.5)
    #     cbar = plt.colorbar()
    #     cbar.set_label('Quench velocity [m/s]', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     # plt.axis('equal')
    #
    #     plt.subplot(1, 4, 2)
    #     plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.rho_ht_10K)
    #     plt.xlabel('x [mm]', **self.selectedFont)
    #     plt.ylabel('y [mm]', **self.selectedFont)
    #     plt.title('Resistivity', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     plt.grid('minor', alpha=0.5)
    #     cbar = plt.colorbar()
    #     cbar.set_label('Resistivity [$\Omega$*m]', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     # plt.axis('equal')
    #
    #     plt.subplot(1, 4, 3)
    #     plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.r_el_ht_10K)
    #     plt.xlabel('x [mm]', **self.selectedFont)
    #     plt.ylabel('y [mm]', **self.selectedFont)
    #     plt.title('Resistance per unit length', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     plt.grid('minor', alpha=0.5)
    #     cbar = plt.colorbar()
    #     cbar.set_label('Resistance per unit length [$\Omega$/m]', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     # plt.axis('equal')
    #
    #     plt.subplot(1, 4, 4)
    #     plt.scatter(self.x_ave * 1000, self.y_ave * 1000, s=2, c=self.tQuenchDetection * 1e3)
    #     plt.xlabel('x [mm]', **self.selectedFont)
    #     plt.ylabel('y [mm]', **self.selectedFont)
    #     plt.title('Approximate quench detection time', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     plt.grid('minor', alpha=0.5)
    #     cbar = plt.colorbar()
    #     cbar.set_label('Time [ms]', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     # plt.axis('equal')
    #     plt.show()
    #
    # def plot_q_prop_v(self):
    #     f = plt.figure(figsize=(16, 6))
    #     plt.subplot(1, 2, 1)
    #     plt.plot(self.mean_B_ht, self.vQ_iStartQuench, 'ko')
    #     plt.xlabel('Average magnetic field in the half-turn [T]', **self.selectedFont)
    #     plt.ylabel('Quench propagation velocity [m/s]', **self.selectedFont)
    #     plt.title('Quench propagation velocity', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     plt.grid('minor', alpha=0.5)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.subplot(1, 2, 2)
    #     plt.plot(self.mean_B_ht, self.tQuenchDetection * 1e3, 'ko')
    #     plt.xlabel('Average magnetic field in the half-turn [T]', **self.selectedFont)
    #     plt.ylabel('Approximate quench detection time [ms]', **self.selectedFont)
    #     plt.title('Approximate quench detection time', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     plt.grid('minor', alpha=0.5)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.show()
    #
    # def plot_electrical_order(self):
    #     plt.figure(figsize=(16, 8))
    #     plt.subplot(1, 3, 1)
    #     plt.scatter(self.x_ave, self.y_ave, s=2, c=np.argsort(self.el_order_half_turns_Array))
    #     plt.xlabel('x [m]', **self.selectedFont)
    #     plt.ylabel('y [m]', **self.selectedFont)
    #     plt.title('Electrical order of the half-turns', **self.selectedFont)
    #     plt.set_cmap('jet')
    #     cbar = plt.colorbar()
    #     cbar.set_label('Electrical order [-]', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.axis('equal')
    #     # Plot
    #     plt.subplot(1, 3, 2)
    #     plt.plot(self.x_ave[self.el_order_half_turns_Array - 1], self.y_ave[self.el_order_half_turns_Array - 1], 'k')
    #     plt.scatter(self.x_ave, self.y_ave, s=2, c=self.nS)
    #     plt.scatter(self.x_ave[self.el_order_half_turns_Array[0] - 1],
    #                 self.y_ave[self.el_order_half_turns_Array[0] - 1], s=50, c='r',
    #                 label='Positive lead')
    #     plt.scatter(self.x_ave[self.el_order_half_turns_Array[-1] - 1],
    #                 self.y_ave[self.el_order_half_turns_Array[-1] - 1], s=50, c='b',
    #                 label='Negative lead')
    #     plt.xlabel('x [m]', **self.selectedFont)
    #     plt.ylabel('y [m]', **self.selectedFont)
    #     plt.title('Electrical order of the half-turns', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.axis('equal')
    #     plt.legend(loc='lower left')
    #     # Plot
    #     plt.subplot(1, 3, 3)
    #     # plt.plot(x_ave_group[elPairs_GroupTogether_Array[:,0]-1],y_ave_group[elPairs_GroupTogether_Array[:,1]-1],'b')
    #     plt.scatter(self.x, self.y, s=2, c='k')
    #     plt.scatter(self.x_ave_group, self.y_ave_group, s=10, c='r')
    #     plt.xlabel('x [m]', **self.selectedFont)
    #     plt.ylabel('y [m]', **self.selectedFont)
    #     plt.title('Electrical order of the groups (only go-lines)', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.axis('equal')
    #     plt.show()
    #
    # def plot_heat_exchange_order(self):
    #     plt.figure(figsize=(10, 10))
    #     # plot strand positions
    #     plt.scatter(self.x, self.y, s=2, c='b')
    #     # plot conductors
    #     # for c, (cXPos, cYPos) in enumerate(zip(xPos, yPos)):
    #     #     pt1, pt2, pt3, pt4 = (cXPos[0], cYPos[0]), (cXPos[1], cYPos[1]), (cXPos[2], cYPos[2]), (cXPos[3], cYPos[3])
    #     #     line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k', alpha=.25)
    #     #     plt.gca().add_line(line)
    #     # plot average conductor positions
    #     # plt.scatter(x_ave, y_ave, s=10, c='r')
    #     # plot heat exchange links along the cable narrow side
    #     for i in range(len(self.iContactAlongHeight_From)):
    #         plt.plot([self.x_ave[self.iContactAlongHeight_From_Array[i] - 1],
    #                   self.x_ave[self.iContactAlongHeight_To_Array[i] - 1]],
    #                  [self.y_ave[self.iContactAlongHeight_From_Array[i] - 1],
    #                   self.y_ave[self.iContactAlongHeight_To_Array[i] - 1]], 'k')
    #     # plot heat exchange links along the cable wide side
    #     for i in range(len(self.iContactAlongWidth_From)):
    #         plt.plot([self.x_ave[self.iContactAlongWidth_From_Array[i] - 1],
    #                   self.x_ave[self.iContactAlongWidth_To_Array[i] - 1]],
    #                  [self.y_ave[self.iContactAlongWidth_From_Array[i] - 1],
    #                   self.y_ave[self.iContactAlongWidth_To_Array[i] - 1]], 'r')
    #     # plot strands belonging to different conductor groups and clo ser to each other than max_distance
    #     # for p in pairs_close:
    #     #     if not strandToGroup[p[0]] == strandToGroup[p[1]]:
    #     #         plt.plot([X[p[0], 0], X[p[1], 0]], [X[p[0], 1], X[p[1], 1]], c='g')
    #     plt.xlabel('x [m]', **self.selectedFont)
    #     plt.ylabel('y [m]', **self.selectedFont)
    #     plt.title('Heat exchange order of the half-turns', **self.selectedFont)
    #     plt.rcParams.update({'font.size': 12})
    #     plt.axis('equal')
    #     plt.show()
    #
    def plot_power_supl_contr(self):
        ps = self.model_data.Power_Supply

        plt.figure(figsize=(5, 5))
        plt.plot([ps.t_off, ps.t_off], [np.min(ps.I_control_LUT), np.max(ps.I_control_LUT)], 'k--', linewidth=4.0,
                 label='t_PC')
        plt.plot(ps.t_control_LUT, ps.I_control_LUT, 'ro-', label='LUT')
        plt.xlabel('Time [s]', self.selectedFont)
        plt.ylabel('Current [A]', self.selectedFont)
        plt.title('Look-up table controlling power supply', self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        displayWaitAndClose(waitTimeBeforeMessage=.1, waitTimeAfterMessage=10)

    def plot_all(self):
        # self.plot_field()
        # self.plot_polarities()
        # self.plot_strands_groups_layers()
        # self.plot_electrical_order()
        # self.plot_q_prop_v()
        # self.plot_quench_prop_and_resist()
        self.plot_psu_and_trig()
        # self.plot_half_turns()
        # self.plot_heat_exchange_order()
        # self.plot_nonlin_induct()
        self.plot_power_supl_contr()
    ####################### Plotter methods - END #######################