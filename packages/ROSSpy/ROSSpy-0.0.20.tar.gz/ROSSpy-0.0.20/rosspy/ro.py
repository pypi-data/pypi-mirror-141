from scipy.constants import nano, kilo, milli, centi, liter, minute, day, hour
from chempy.properties.water_density_tanaka_2001 import water_density
from chemicals import periodic_table
from math import pi, exp, ceil
from matplotlib import pyplot 
from itertools import chain
from pprint import pprint
from sigfig import round
from glob import glob
import datetime
import pandas
import chemw
import json, os, re

def sigfigs_conversion(num, sigfigs_in = 2):
    return round(num, sigfigs=sigfigs_in, notation = 'sci')

elemental_masses = {}
for element in periodic_table:
    elemental_masses[element.symbol] = element.MW

def time_determination(time):
    unit = 'seconds'
    if time > 600:
        if time > 7200:
            if time > 2e5:
                time /= day
                unit = 'days'
            else:
                time /= hour
                unit = 'hours'
        else:
            time /= minute
            unit = 'minutes'
    return float(sigfigs_conversion(time, 3)), unit

def isnumber(num):
    try:
        float(num)
        return True
    except:
        try:
            int(num)
            return True
        except:
            return False

class ROSSPkg():
    def __init__(self, database_selection, simulation = 'scaling', simulation_type = 'transport', operating_system = 'windows',  export_content = True, domain_phase = None, quantity_of_modules = 1, simulation_title = None, verbose = False, printing = True, jupyter = False):      
        # establish the general organization structures and values
        self.parameters = {}
        self.variables = {}
        self.results = {}
        self.results['figures'] = {}
        self.printing = printing
        self.verbose = verbose
        self.jupyter = jupyter
        self.export_content = export_content
        self.plot_title = None
        self.chem_mw = chemw.ChemMW(printing = False,)
        
        self.water_mw = self.chem_mw.mass('H2O')
        self.water_gL = water_density()
        
        # import PHREEQpy
        self.parameters['os'] =  operating_system
        if operating_system == 'windows':
            import phreeqpy.iphreeqc.phreeqc_com as phreeqc_mod
        elif operating_system == 'unix':
            import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod
        else:
            raise TypeError(f'--> ERROR: The operating system {operating_system} is not supported.')
        self.phreeqc_mod = phreeqc_mod
        
        # define paths
        self.parameters['root_path'] = os.path.join(os.path.dirname(__file__))
        self.parameters['database_path'] = os.path.join(self.parameters['root_path'], 'databases',f'{database_selection}.dat')
        
        # define options
        self.databases = [re.search('(?<=processed_databases\\\\)(.+)(?=\.json)', database).group() for database in glob(os.path.join(self.parameters['root_path'], 'processed_databases', '*.json'))]
        self.feed_sources = [os.path.basename(feed).split('.')[0] for feed in glob(os.path.join(self.parameters['root_path'], 'water_bodies', '*.json'))]
        
        # define simulation parameters
        self.parameters['database_selection'] = database_selection 
        self.parameters['quantity_of_modules'] = quantity_of_modules
        self.parameters['simulation_type'] = simulation_type
        self.parameters['simulation'] = simulation
        self._define_database()
        
        self.parameters['domain'] = 'single'
        if domain_phase in ['mobile', 'immobile']:
            self.parameters['domain_phase'] = domain_phase
            self.parameters['domain'] = 'dual'
        elif domain_phase is not None:
            print(f'--> ERROR: The {domain_phase} domain phase is not one of the accepted terms: \'mobile\' or \'immobile\' .')

        # create the general_conditions block of the input file
        title_line = f'TITLE\t {simulation_title}'
        database_line = 'DATABASE {}'.format(self.parameters['database_path'])
#         if self.parameters['os'] == 'unix':
#             database_line = 'DATABASE C:{}'.format(self.parameters['database_path'])
        self.results['general_conditions'] = [database_line, title_line]
            
        
    def _define_database(self,):
        database_json = os.path.join(self.parameters['root_path'], 'processed_databases', '{}.json'.format(self.parameters['database_selection'])) 
        database = json.load(open(database_json, 'r'))
        self.elements = database['elements']
        self.minerals = database['minerals']

    def _transport(self, simulation_time, simulation_perspective = None, module_characteristics = {}, timestep = None, cells_per_module = 12, kinematic_flow_velocity = None, exchange_factor = 1e5):
        '''Define the TRANSPORT block'''
        self.parameters['simulation_time'] = simulation_time
        self.parameters['exchange_factor'] = exchange_factor
        self.parameters['simulation_perspective'] = simulation_perspective
        if self.parameters['simulation_perspective'] is None:
            if self.parameters['simulation'] == 'scaling':
                self.parameters['simulation_perspective'] = 'all_distance'
            elif self.parameters['simulation'] == 'brine':
                self.parameters['simulation_perspective'] = 'all_time'
        
        # assign default RO module dimensions 
        self.parameters['module_diameter_mm'] =  201                 
        self.parameters['permeate_tube_diameter_mm'] =  29            
        self.parameters['module_length_m'] =  1.016                 
        self.parameters['permeate_flow_m3_per_hour'] = 40/(day/hour)                  
        self.parameters['max_feed_flow_m3_per_hour'] = 15.9                  
        self.parameters['membrane_thickness_mm'] = 250 * (nano / milli)   
        self.parameters['feed_thickness_mm'] = 0.8636
        self.parameters['active_m2'] = 37
        self.parameters['permeate_thickness_mm'] = 0.3               
        self.parameters['polysulfonic_layer_thickness_mm'] = 0.05     
        self.parameters['support_layer_thickness_mm'] = 0.15           

        # assign parameterized module dimensions
        for parameter in module_characteristics:
            self.parameters[parameter] = module_characteristics[parameter]

        # calculate module properties
        self.parameters['repeated_membrane_winding_mm'] = 2 * self.parameters['membrane_thickness_mm'] + self.parameters['feed_thickness_mm'] + self.parameters['permeate_thickness_mm'] + 2 * self.parameters['polysulfonic_layer_thickness_mm'] + 2 * self.parameters['support_layer_thickness_mm']     
        if self.parameters['repeated_membrane_winding_mm'] == 0:
            print('--> ERROR: The module dimensions are not sensible.')
        self.parameters['cells_per_module'] = cells_per_module
        self.variables['cell_meters'] = self.parameters['module_length_m'] / self.parameters['cells_per_module']        
        self.parameters['active_m2_cell'] = self.parameters['active_m2'] / self.parameters['cells_per_module']
        
        module_cross_sectional_area = self.parameters['module_diameter_mm']**2 * pi / 4        #squared millimeters
        permeate_tube_cross_sectional_area = self.parameters['permeate_tube_diameter_mm']**2 * pi / 4     #squared millimeters
        filtration_cross_sectional_area = (module_cross_sectional_area - permeate_tube_cross_sectional_area) * milli**2         #squared meters
        feed_cross_sectional_area = (self.parameters['feed_thickness_mm'] / self.parameters['repeated_membrane_winding_mm']) * filtration_cross_sectional_area       #squared meters
        self.variables['feed_cubic_meters'] = feed_cross_sectional_area * self.parameters['module_length_m'] 
        self.variables['feed_kg'] = self.variables['feed_cubic_meters'] / liter * self.water_gL * milli    
        self.variables['feed_moles'] = self.variables['feed_kg'] * kilo / self.water_mw 

        # calculate fluid flow characteristics
        if not kinematic_flow_velocity:
            kinematic_flow_velocity = 9.33E-7    #square meters / second
        feed_velocity = self.parameters['max_feed_flow_m3_per_hour'] / (feed_cross_sectional_area) / hour     #meters / second
        reynolds_number = feed_velocity * (self.parameters['module_diameter_mm'] - self.parameters['permeate_tube_diameter_mm']) * milli**2 / kinematic_flow_velocity
        self.variables['Reynold\'s number'] = reynolds_number

        # calculate module cell characteristics
        self.variables['feed_kg_cell'] = self.variables['feed_kg'] / self.parameters['cells_per_module']   
        self.variables['feed_moles_cell'] = self.variables['feed_moles'] / self.parameters['cells_per_module']   

        # calculate simulation timestep that adheres to the Courant condition   
        self.parameters['timestep'] = self.parameters['module_length_m'] / feed_velocity  # seconds
        if timestep:
            self.parameters['timestep'] = timestep
            
        courant_timestep = self.variables['cell_meters'] / feed_velocity
        if self.parameters['timestep'] < courant_timestep:
            self.parameters['timestep'] = courant_timestep
            
        self.parameters['permeate_moles_per_cell'] = (self.parameters['permeate_flow_m3_per_hour']/hour/liter * self.water_gL / self.water_mw) * (self.parameters['timestep'] / self.parameters['cells_per_module'])      #moles / (cell * self.parameters['timestep'])
        
        # exit the function for evaporation simulations
        self.results['transport_block'] = []
        if self.parameters['simulation_type'] == 'evaporation':
            return None

        # define the transport black
        transport_line = '\nTRANSPORT'
        cells_line = '-cells\t\t\t{}'.format(self.parameters['cells_per_module'] * self.parameters['quantity_of_modules'])
        
        self.simulation_shifts = ceil(simulation_time / self.parameters['timestep']) #(self.parameters['cells_per_module']*self.parameters['quantity_of_modules'])
        shifts_line = f'-shifts\t\t\t{self.simulation_shifts}'
        lengths_line = '-lengths\t\t{}'.format(self.variables['cell_meters'])
        timestep_line = '-time_step\t\t{}\t# this satisfies the Courant condition with a feed velocity of {} m/s'.format(self.parameters['timestep'], sigfigs_conversion(feed_velocity, 4))
        initial_time_line = '-initial_time\t\t0'    
        boundary_conditions_line = '-boundary_conditions\tconstant\tflux \t # Dirichlet and Cachy boundary conditions'
        
        # define the domain-dependent parameters
        domain_line = ''
        cp_cell_volume_proportion = 0.05 #/self.parameters['cells_per_module']
        bulk_cell_volume_proportion = 0.95 #/self.parameters['cells_per_module']
        if self.parameters['domain'] == 'dual':
            domain_line = f'-stagnant\t\t1\t\t{exchange_factor}\t\t\t{cp_cell_volume_proportion}\t\t{bulk_cell_volume_proportion} \t # dual domain\n#\t\t\t^stagnant cells\t^exchange factor\t^CP porosity\t^bulk porosity'
        if self.parameters['domain'] == 'single' or (self.parameters['domain'] == 'dual' and self.parameters['domain_phase'] == 'mobile'):
            first_cell = 1
            final_cell = self.parameters['cells_per_module']*self.parameters['quantity_of_modules']
            if self.parameters['simulation_perspective'] == 'all_distance':
                punch_cells_line = '-punch_cells\t\t{}-{}'.format(first_cell, final_cell)
                punch_frequency_line = f'-punch_frequency\t{self.simulation_shifts}'
            elif self.parameters['simulation_perspective'] == 'all_time':
                punch_cells_line = '-punch_cells\t\t{}'.format(final_cell)
                punch_frequency_line = '-punch_frequency\t1'    
            
        elif self.parameters['domain'] == 'dual' and self.parameters['domain_phase'] == 'immobile':
            first_cell = self.parameters['cells_per_module']*self.parameters['quantity_of_modules']+2
            final_cell = self.parameters['cells_per_module']*self.parameters['quantity_of_modules']*2+1
            if self.parameters['simulation_perspective'] == 'all_distance':
                punch_cells_line = '-punch_cells\t\t{}-{}'.format(first_cell, final_cell)
                punch_frequency_line = f'-punch_frequency\t{self.simulation_shifts}'
            elif self.parameters['simulation_perspective'] == 'all_time':
                punch_cells_line = '-punch_cells\t\t{}'.format(final_cell)
                punch_frequency_line = '-punch_frequency\t1'
        
        # create the transport block
        self.results['transport_block'].extend((transport_line, cells_line, shifts_line, lengths_line, timestep_line, initial_time_line, boundary_conditions_line, domain_line, punch_cells_line, punch_frequency_line))

        # print simulation parameters
        if self.verbose:
            print('\nMembrane thickness (mm):', (self.parameters['repeated_membrane_winding_mm']))
            print('cell length (m): ', self.variables['cell_meters'])
            print('feed velocity (m/s): ', feed_velocity) 
            print('feed_cross_sectional_area (m^2): ', feed_cross_sectional_area)
            print('permeate_removal_per_cell', self.parameters['permeate_moles_per_cell'])
            print('active_cm_squared_cell', (self.parameters['active_m2_cell'] / centi**2))

    def _reaction(self, final_cf = None, permeate_efficiency = 1, head_loss = 0.89, evaporation_steps = 15):     
        '''Define the REACTION blocks'''
        # establish parameters
        self.parameters['permeate_approach'] = 'linear_permeate'
        if isnumber(final_cf):
            self.parameters['permeate_approach'] = 'linear_cf'
#             module_cf = final_cf**(1/self.parameters['quantity_of_modules'])
        elif final_cf is not None:
            print(f'--> ERROR: The final_cf parameter value < {final_cf} > is not a number.')
    
        cfs = []
        cell_moles = []
        reaction_parameters = []
        self.results['reaction_block'] = []
        self.cumulative_cf = 1 
        module_previous_moles_removed = 0 
        for module in range(self.parameters['quantity_of_modules']): 
            if self.parameters['permeate_approach'] == 'linear_permeate':
                initial_moles_removed = self.parameters['permeate_moles_per_cell'] * 2 / (1 + head_loss)
                final_moles_removed = initial_moles_removed * head_loss
                removed_moles_slope = ((final_moles_removed - initial_moles_removed) / (self.parameters['cells_per_module'])) / permeate_efficiency
                average_moles_removed = (final_moles_removed + initial_moles_removed) / 2
                module_parameters = []

                for cell in range(self.parameters['cells_per_module']):
                    removed_moles_in_cell = (cell * removed_moles_slope + initial_moles_removed)
                    reaction_parameters.append(removed_moles_in_cell)
                    module_parameters.append(removed_moles_in_cell)
                    
                moles_removed = sum(reaction_parameters)
                self.cumulative_cf = self.variables['feed_moles'] / (self.variables['feed_moles'] - moles_removed)
                module_moles_removed = sum(module_parameters)
                cf = self.variables['feed_moles'] / (self.variables['feed_moles'] - module_moles_removed)
                self.cumulative_cf *= cf
                
                self.variables[f'module {module}'] = {'cf': cf, 'permeate (moles/cell)': removed_moles_slope}
                moles_remaining = self.variables['feed_moles'] - moles_removed
                
                if sigfigs_conversion(average_moles_removed,14) != sigfigs_conversion(self.parameters['permeate_moles_per_cell'], 14):
                    print('--> ERROR: Inconsistent REACTION calculations.', )
                    print('average_moles_removed', average_moles_removed)
                    print('permeate_moles_per_cell', self.parameters['permeate_moles_per_cell'])
               
                if self.verbose:
                    print('\n')
                    print('permeate (moles/cell) ', removed_moles_slope)
                    print('moles_remaining', moles_remaining)
                    print('moles_removed', moles_removed)

            elif self.parameters['permeate_approach'] == 'linear_cf':
                module_iteration = moles_removed = 0
                initial_cf = 1
                cfs = []
                effective_cells = self.parameters['cells_per_module']*self.parameters['quantity_of_modules']
                cf_slope = (final_cf - initial_cf) / effective_cells
                for cell in range(self.parameters['cells_per_module']*(module), self.parameters['cells_per_module']*(module+1)):
                    cell_cf = (cell+1) * cf_slope + initial_cf
                    cfs.append(cell_cf)  
                for cf in cfs:
                    if self.verbose:
                        print('\n',)
                    moles_to_be_removed = self.variables['feed_moles'] - (self.variables['feed_moles'] / cf)
                    if module_iteration == 0:
                        if len(reaction_parameters) > 0:
                            if self.verbose:
                                print('to be', moles_to_be_removed, '\tlast parameter', reaction_parameters[-1], '\tprevious removal', sum(reaction_parameters))
                            module_previous_moles_removed += reaction_parameters[-1]
                        else:
                            if self.verbose:
                                print('to be', moles_to_be_removed, )
                        if module == 0:
                            reaction_parameters.append(moles_to_be_removed)
                        else:
                            reaction_parameters.append(moles_to_be_removed - module_previous_moles_removed)
                    else:
                        module_previous_moles_removed += reaction_parameters[-1] 
                        if moles_to_be_removed < module_previous_moles_removed:
                            print(f'--> ERROR: The reaction parameter is negative: {moles_to_be_removed - module_previous_moles_removed}.')
                        reaction_parameter = moles_to_be_removed - module_previous_moles_removed
                        if self.verbose:
                            print('to be', moles_to_be_removed, '\tlast parameter', reaction_parameters[-1], '\tthis parameter', reaction_parameter, '\tprevious removal', module_previous_moles_removed)
                        reaction_parameters.append(reaction_parameter)

                    moles_removed = sum(reaction_parameters)
                    module_iteration += 1

                    # verify the CF calculations and efffects in the system
                    measured_cf = self.variables['feed_moles'] / (self.variables['feed_moles']-moles_removed)
                    consistency = round(measured_cf, 5) == round(cf, 5)
                    if not consistency:
                        print(f'--> ERROR: The measured cf {measured_cf} is dissimilar from the target cf {cf}.') 
                    else:
                        if self.verbose:
                            print('cf consistency between the measured and predicted: ', consistency)

                self.cumulative_cf = cf = cfs[-1]
                
            moles_remaining = self.variables['feed_moles'] - moles_removed  
            self.variables[f'module {module}'] = {'cf': cf}

            if self.parameters['simulation_type'] == 'transport':
                for cell in range(1, self.parameters['cells_per_module']+1):
                    if self.parameters['domain'] == 'single':
                        cell_number = cell + self.parameters['cells_per_module'] * module
                        reaction_index = cell_number-1
                    elif self.parameters['domain'] == 'dual':
                        cell_number = cell + self.parameters['cells_per_module'] * (module + self.parameters['quantity_of_modules']) + 1
                        reaction_index = (cell + self.parameters['cells_per_module'] * module)-1
                        
                    reaction_line = f'\nREACTION {cell_number}'
                    if cell < self.parameters['cells_per_module']:
                        reaction_line += f'\n\tH2O -1; {reaction_parameters[reaction_index]}' 
                    elif cell == self.parameters['cells_per_module']:
                        reaction_line += f'''\n\tH2O -1; {reaction_parameters[reaction_index]}'''   
                           
                    self.results['reaction_block'].append(reaction_line)
                    
                # the calculated reaction parameters will be added and printed to a generated PHREEQC input file
                final_solution_mass = float(moles_remaining * self.water_mw * milli)  #kg water mass
                if self.parameters['os'] == 'windows':
                    self.results['reaction_block'].append('# {}'.format(self.parameters['permeate_approach']))
                    if self.parameters['permeate_approach'] == 'linear_permeate':
                        self.results['reaction_block'].append(f'''
    #Permeate efficiency parameter: {permeate_efficiency}
    #Effluent relative pressure: {head_loss}''')

                    self.results['reaction_block'].append(f'''    
    #Effluent module {module + 1}:
#Estimated CF: {sigfigs_conversion(cf, 4)}
#Estimated final water mass: {final_solution_mass}\n\n''')

            elif self.parameters['simulation_type'] == 'evaporation':
                # define the reaction block
                reaction_line = '\nREACTION 1'
                reaction_line += '\n\tH2O -1; '
                reaction_line += f'{moles_removed} in {evaporation_steps} step'
                reaction_line += ';\nINCREMENTAL_REACTIONS \ttrue'
                self.results['reaction_block'].append(reaction_line)

            if self.printing:
                print(f'Effluent module {module + 1} CF: {cf}')

                
    def reactive_transport(self, simulation_time, simulation_perspective = None, final_cf = None, module_characteristics = {}, permeate_efficiency = 1, head_loss = 0.89, evaporation_steps = 15, timestep = None, cells_per_module = 12, kinematic_flow_velocity = None, exchange_factor = 1e5):
        self._transport(simulation_time, simulation_perspective, module_characteristics, timestep, cells_per_module, kinematic_flow_velocity, exchange_factor)
        self._reaction(final_cf, permeate_efficiency, head_loss, evaporation_steps)
                       
                       
    def _described_minerals(self,):
        # determine the set of possible minerals 
        self.variables['described_minerals'] = {}
        for mineral in self.minerals:
            mineral_formula = self.minerals[mineral]['formula']
            original_formula = mineral_formula
            
            # remove entities is an ordered fashion
            mineral_formula = re.sub('(H2O|OH|CO3)', '', mineral_formula)
            if 'S(6)' in self.parameters['solution_elements']:
                mineral_formula = re.sub('(SO4)', '', mineral_formula)
            mineral_formula = re.sub('([0-9()•:.])', '', mineral_formula)
            mineral_elements = re.findall('[A-Z][a-z]?', mineral_formula)
            
            for element in mineral_elements:
                if all(element in self.parameters['solution_elements'] for element in mineral_elements):
                    self.variables['described_minerals'][mineral] = self.minerals[mineral]
                elif element not in self.parameters['solution_elements']:
                    if self.verbose:
                        print('--> The {} element is absent in the solution to describe the mineral < {} / {} >.'.format(element, original_formula, mineral))
                        

    def _define_elements(self,element_dict):
        elements_lines = []
        self.predicted_effluent = {}
        undefined_elements = []
        for element, information2 in element_dict.items():
            self.parameters['solution_elements'].append(element)

            conc = information2['concentration (ppm)']
            self.predicted_effluent[element] = conc*self.cumulative_cf
            ref = ''
            if 'reference' in information2:
                ref = information2['reference']

            form = ''
            if 'form' in information2:
                form = 'as {}'.format(information2['form'])

            if element in self.elements:                          
                if len(str(conc)) <= 3:
                    elements_lines.append(f'{element}\t\t{conc}\t{form}\t#{ref}')
                else:
                    elements_lines.append(f'{element}\t{conc}\t{form}\t#{ref}')
            else:
                undefined_elements.append(element)
        print('\n--> The {} elements are not accepted by the {} database'.format(undefined_elements, self.parameters['database_selection']))
        return elements_lines

    def feed_geochemistry(self, water_selection = '', water_characteristics = {}, solution_description = '', ignored_minerals = [], existing_parameters = {}, parameterized_ph_charge = True):
        # create the solution line of the input file
        self.results['solution_block'] = []
        
        if water_selection not in self.feed_sources and water_characteristics == {}:
            error = f'The {water_selection} does not have a corresponding parameter file. Either select an existing feed water {self.feed_sources}, or define a custom feed water with the water_characteristics dictionary.'
            raise ValueError(error)
        
        self.parameters['water_selection'] = water_selection
        if water_selection == '':
            self.parameters['water_selection'] = solution_description
            
        initial_number = 0
        if self.parameters['simulation_type'] == 'evaporation':
            initial_number = 1
            
        initial_solution_line = '\nSOLUTION {}\t{}'.format(initial_number, self.parameters['water_selection'])
        self.results['solution_block'].append(initial_solution_line)

        #========================= FEED IONS =================================           
        self.parameters['solution_elements'] = []
        temperature = ph = alkalinity = pe = None
        if water_selection in self.feed_sources:       
            # import the predefined water body
            water_file_path = os.path.join(self.parameters['root_path'], 'water_bodies', f'{water_selection}.json')
            water_body = json.load(open(water_file_path))
            
            for content, information in water_body.items():
                if content == 'element':
                    elements_lines = self._define_elements(information)       
                elif content == 'temperature (C)':
                    temperature = information['value']
                    temperature_reference = information['reference']
                elif content == 'pe':
                    pe = information['value']
                    pe_reference = information['reference']
                elif content == 'Alkalinity':
                    alkalinity = information['value']
                    alkalinity_reference = information['reference'] 
                    alkalinity_form = 'as {}'.format(information['form'])    
                elif content == 'pH':
                    ph = information['value']
                    ph_reference = information['reference']

        elif water_characteristics != {}:
            for content, information in water_characteristics.items():
                if content == 'element':
                    elements_lines = self._define_elements(information)
                # create the temperature line of the input file
                elif content == 'temperature (C)':                    
                    temperature = water_characteristics['temperature']['value']
                    temperature_reference = ''
                    if 'reference' in water_characteristics['temperature']:
                        temperature_reference = water_characteristics['temperature']['reference']
                elif content == 'pe':       
                    pe = water_characteristics['pe']['value']
                    pe_reference = ''
                    if 'reference' in water_characteristics['pe']:
                        pe_reference = water_characteristics['pe']['reference']
                elif content == 'Alkalinity':
                    alkalinity = water_characteristics['Alkalinity']['value']
                    alkalinity_reference = ''
                    alkalinity_form = ''
                    if 'reference' in water_characteristics['Alkalinity']:
                        alkalinity_reference = water_characteristics['Alkalinity']['reference']
                    if 'form' in water_characteristics['Alkalinity']:
                        alkalinity_form = 'as {}'.format(water_characteristics['Alkalinity']['form'])    
                elif content == 'pH':
                    ph = water_characteristics['pH']['value']
                    ph_reference = ''
                    if 'reference' in water_characteristics['pH']:
                        ph_reference = water_characteristics['pH']['reference']
                    
        # parameterize the lines of the SOLUTIONS block
        temperature_line = ''
        if temperature is not None:
            temperature_line = f'temp \t {temperature} \t #{temperature_reference}.'
        pe_line = ''
        if pe is not None:
            pe_line = f'pe \t\t {pe} \t   #{pe_reference} // 4.00 is the default (?)'     

        alkalinity_line = ''
        ph_line = ''
        if alkalinity:
            alkalinity_line = f'Alkalinity \t {alkalinity} {alkalinity_form} #{alkalinity_reference}'
        if ph is not None:
            ph_line = f'pH \t\t {ph} #{ph_reference}'
            if parameterized_ph_charge and not alkalinity:
                ph_line = f'pH \t\t {ph} charge #{ph_reference}'
                alkalinity_line = ''
                   
        unit_line = 'units \t ppm' 
        elements_line = '\n'.join(elements_lines)
        if water_selection == 'Bakken formation':
            water_line = '-water \t{}\t#TDS=300 ppthousand [before fudging]'.format(self.variables['feed_kg'])
        elif water_selection == 'German Basin':
            water_line = '-water \t{}\t#TDS=314 ppthousand [before fudging]'.format(self.variables['feed_kg'])
        else:
            water_line = '-water \t{}'.format(self.variables['feed_kg'])

        self.results['solution_block'].extend([temperature_line, ph_line, pe_line, alkalinity_line, unit_line, elements_line, water_line])

        #parameterize the initial module solution
        if self.parameters['simulation_type'] == 'transport':
            total_cells = self.parameters['cells_per_module'] * self.parameters['quantity_of_modules']
            if self.parameters['domain'] == 'dual':
                total_cells = total_cells*2+1
            feed_solution_line = f'\nSOLUTION 1-{total_cells}\tInitial solution in the RO module'
            water_line = '-water \t{}'.format(self.variables['feed_kg'])
            self.results['solution_block'].extend([feed_solution_line,'temp \t 25','units \t ppm',water_line])

        #========================= POTENTIAL SCALANTS =================================
        short_mineral_names = ['Barite', 'Gypsum','Halite', 'Natron', 'Quartz', 'Talc','Trona', 'Borax', 'Albite', 'K-mica','Illite', 'Pyrite', 'Sulfur',]
        long_mineral_names = ['Anthophyllite', 'Hexahydrite', 'Leonhardite', 'Nesquehonite', 'Pentahydrite', 'Portlandite','Sepiolite(d)', 'Boric_acid,s', 'K2B4O7:4H2O', 'NaB5O8:5H2O', 'Rhodochrosite', 'Strontianite','Hydroxyapatite', 'Chlorite(14A)', 'Mackinawite', 'Hausmannite', 'Pyrochroite']

        # define the equilibrium_phases block
        self.results['equilibrium_phases_block'] = []
        if self.parameters['simulation_type'] == 'transport':
            total_cells = self.parameters['cells_per_module'] * self.parameters['quantity_of_modules']
            if self.parameters['domain'] == 'dual':
                total_cells = total_cells*2+1
            equilibrium_phases_number = '1-{}'.format(total_cells)     
        elif self.parameters['simulation_type'] == 'evaporation':
            equilibrium_phases_number = '1'
            
        equilibrium_phases_line = f'\nEQUILIBRIUM_PHASES {equilibrium_phases_number}'
        self.results['equilibrium_phases_block'].append(equilibrium_phases_line)

        # define the equilibrium_phases lines for the code block
        self._described_minerals()
        for possible_mineral in self.variables['described_minerals']:
            if possible_mineral not in ignored_minerals:
                if possible_mineral in short_mineral_names:
                    mineral_line = f'{possible_mineral}\t\t' 
                elif possible_mineral == 'Ca-Montmorillonite':
                    mineral_line = possible_mineral
                else:
                    mineral_line = f'{possible_mineral}\t'

                if possible_mineral in existing_parameters:
                    for key, value in existing_parameters[possible_mineral].items():
                        if key == 'saturation':
                            mineral_saturation = value['saturation']
                            mineral_line += f'\t{mineral_saturation}'
                        if key == 'initial_moles':
                            initial_moles = value['initial_moles']
                            mineral_line += f'\t{initial_moles}'
                else:
                    mineral_line += f'\t0\t0'
                    
                self.results['equilibrium_phases_block'].append(mineral_line)     
                
        if self.verbose:
            pprint(self.variables['described_minerals'])
                        
    def _selected_output(self, output_filename):
        # create parameter lines             
        if output_filename is None:
            count = 0
            self.parameters['selected_output_file_name'] = '-'.join([str(x) for x in [datetime.date.today(), self.parameters['water_selection'], self.parameters['simulation_type'], self.parameters['database_selection'], self.parameters['simulation'], count]]) 
            while os.path.exists('{}.txt'.format(self.parameters['selected_output_file_name'])):
                count += 1
                self.parameters['selected_output_file_name'] = '-'.join([str(x) for x in [datetime.date.today(), self.parameters['water_selection'], self.parameters['simulation_type'], self.parameters['database_selection'], self.parameters['simulation'], count]]) 
        else:
            self.parameters['selected_output_file_name'] = output_filename
        self.parameters['selected_output_file_name'] += '.txt'

        minerals_line = ' '.join([mineral for mineral in self.variables['described_minerals']])
        elements_line = ' '.join([element for element in self.parameters['solution_elements']])

        # define parameter lines
        first_line = '\nSELECTED_OUTPUT'
        file_name_line = '-file\t\t\t{}'.format(self.parameters['selected_output_file_name'])
        reaction_line = '-reaction\t\ttrue'
        temperature_line = '-temperature\t\ttrue'
        total_elements_line = '-totals\t\t\t' + elements_line    
        saturation_indices_line = f'-saturation_indices\t{minerals_line}'
        equilibrium_phases_line = f'-equilibrium_phases\t{minerals_line}'
        ph_line = '-pH\t\t\ttrue'
        alkalinity_line ='-alkalinity\ttrue' 
        solution_line = '-solution'
        time_line = '-time\t\t\ttrue'
        distance_line = '-distance\t\ttrue'
        simulation_line = '-simulation\t\ttrue'
        high_precision_line = '-high_precision\ttrue'
        charge_balance_line = '-charge_balance\ttrue'
        ionic_strength_line = '-ionic_strength\ttrue'
        step_line = '-step'
        water_line = '-water'

        # establish the selected_output_block
        self.results['selected_output_block'] = []
        self.results['selected_output_block'].extend((first_line, file_name_line, reaction_line, temperature_line, total_elements_line, saturation_indices_line, equilibrium_phases_line, ph_line, time_line, distance_line, simulation_line, high_precision_line, alkalinity_line, solution_line, charge_balance_line, ionic_strength_line, step_line, water_line))
        
    def _define_paths(self, simulation_name = None, simulation_directory = None):
        # define the simulation name 
        simulation_number = 1
        if simulation_name is None:
            if self.parameters['simulation_type'] == 'evaporation':
                simulation_name = '-'.join([re.sub(' ', '_', str(x)) for x in [datetime.date.today(), 'ROSSpy', self.parameters['water_selection'], self.parameters['simulation_type'], self.parameters['database_selection'], self.parameters['simulation'], self.parameters['simulation_perspective']]])
            elif self.parameters['simulation_type'] == 'transport':
                if self.parameters['permeate_approach'] == 'linear_permeate':
                    permeate_approach_name = 'LinPerm'
                elif self.parameters['permeate_approach'] == 'linear_cf':
                    permeate_approach_name = 'LinCF'
                simulation_name = '-'.join([re.sub(' ', '_', str(x)) for x in [datetime.date.today(), 'ROSSpy', self.parameters['water_selection'], self.parameters['simulation_type'], self.parameters['database_selection'], self.parameters['simulation'], self.parameters['simulation_perspective'], permeate_approach_name]])
            
        if simulation_directory is None:
            directory = os.getcwd()
        else:
            directory = os.path.dirname(simulation_directory)
            
        while os.path.exists(os.path.join(directory, simulation_name)):
            simulation_number += 1
            simulation_name = re.sub('(\-\d+$)', '', simulation_name)
            simulation_name = '-'.join([simulation_name, str(simulation_number)])
            
        # define the simulation path 
        self.simulation_path = os.path.join(directory, simulation_name)
        os.mkdir(self.simulation_path)
        
        # define the input file export path
        self.parameters['input_path'] = os.path.join(self.simulation_path, 'input.pqi')                       
        self.parameters['output_path'] = os.path.join(self.simulation_path, 'selected_output.csv')
        self.parameters['simulation_path'] = self.variables['simulation_path'] = self.simulation_path
        
        return directory, simulation_name
        
    def parse_input(self, input_file_path, water_selection = None, active_m2 = None):        
        # open the input file
        
        with open(input_file_path, 'r') as file:
            self.input_file = file.read()
           
        # identify the database in the name
        for db in self.databases:
            if re.search(db, input_file_path):
                self.parameters['database_selection'] = db
            
        # parse the input_file       
        input_df = pandas.read_table(input_file_path, names = ['content'], sep='\n')
        input_df = input_df.squeeze()
        self.parameters['simulation_type'] = 'evaporation'
        self.parameters['permeate_approach'] = 'linear_permeate'
        self.parameters['water_selection'] = water_selection
        self.parameters['domain'] = 'single'
        self.predicted_effluent = {}
        permeate_moles = 0
        for index, row in input_df.iteritems():
            if re.search('DATABASE', row):
                row = re.sub('DATABASE ','',row)
                self.parameters['database_selection'] = re.sub('\.dat', '', os.path.basename(row))
            elif re.search('(^[A-Z][a-z \(]?[\s\d])', row):
                element = re.search('(^[A-Z][a-z]?)', row).group()
                conc = re.search('(?<!\()([\d\.]+)', row).group(1)
                if float(conc) > 0:
                    self.predicted_effluent[element] = float(conc)
            elif re.search('-water\s+\d', row):
                water_mass = float(re.sub('(-water\s+)', '', row))
            elif re.search('linear_cf', row):
                self.parameters['permeate_approach'] = 'linear_cf'
            elif re.search('EQUILIBRIUM_PHASES', row):
                row = re.sub('EQUILIBRIUM_PHASES ','',row)
                row = float(re.sub('(\-\d+)', '', row))
                if row != 1:
                    self.parameters['domain'] = 'dual'
                    self.parameters['domain_phase'] = 'Mobile'
            elif re.search('H2O -1; ', row):
                moles = re.search('([0-9]+\.[0-9]+)', row).group()
                permeate_moles += float(moles)
            elif re.search('TRANSPORT', row):
                self.parameters['simulation_type'] = 'transport'
            elif re.search('-cells', row):
                self.parameters['cells_per_module'] = float(re.sub('-cells\s+', '', row))
            elif re.search('-shifts', row):
                self.simulation_shifts = float(re.sub('-shifts\s+', '', row))
            elif re.search('-file', row):
                self.parameters['selected_output_file_name'] = re.sub('-file\s+', '', row)
            elif re.search('-time_step', row):
                self.parameters['timestep'] = float(re.sub('-time_step\s+', '', row).split('\t')[0])
                self.parameters['simulation_time'] = self.parameters['timestep'] * self.simulation_shifts
            elif re.search('-punch_cells', row):
                row = re.sub('-punch_cells\s+','',row)
                row = float(re.sub('(\-\d+)', '', row))
                if row != 1:
                    self.parameters['domain'] = 'dual'
                    self.parameters['domain_phase'] = 'Immobile'
            elif re.search('-punch_frequency', row):
                row = float(re.sub('-punch_frequency\s+','',row))
                if row > 1:
                    self.parameters['simulation_perspective'] = 'all_distance'               
                elif row == 1:
                    self.parameters['simulation_perspective'] = 'all_time'
                    
        # open the respective database
        self.parameters['database_path'] = os.path.join(self.parameters['root_path'], 'databases','{}.dat'.format(self.parameters['database_selection']))
        self.parameters['solution_elements'] = []
        self._define_database()
        self._described_minerals()
                    
        # predict the effluent concentrations
        water_molar_mass = 2*elemental_masses['H']+elemental_masses['O']
        final_water_mass = water_mass - permeate_moles*water_molar_mass*milli
        self.cumulative_cf = water_mass/final_water_mass
        for element in self.predicted_effluent:
            self.predicted_effluent[element] = self.predicted_effluent[element]*self.cumulative_cf
                
        # define the simulation folder and parameters
        if self.parameters['domain'] == 'dual':
            self.plot_title = '{} phase {} from the {} after {}'.format(self.parameters['domain_phase'], self.parameters['simulation'], self.parameters['water_selection'], sigfigs_conversion(self.parameters['simulation_time']))
        self.parameters['active_m2'] = active_m2
        if self.parameters['active_m2'] is None:
            self.parameters['active_m2'] = 37
        self.parameters['active_m2_cell'] = self.parameters['active_m2']/self.parameters['cells_per_module']
        
        
    def execute(self, simulation_name = None, selected_output_path = None, simulation_directory = None, plot_title = None, title_font = 'xx-large', label_font = 'x-large', x_label_number = 6, export_name = None, export_format = 'svg', individual_plots = None, scale_ions = True, selected_output_filename = None,):
        '''Execute a PHREEQC input file '''
        def run(input_file, first=False):
            phreeqc = self.phreeqc_mod.IPhreeqc()  
            phreeqc.load_database(self.parameters['database_path'])
            phreeqc.run_string(input_file)
            
            # define the conc dictionary
            output = phreeqc.get_selected_output_array()
            header = output[0]
            conc = {}
            for head in header:
                conc[head] = []
            for row in output[1:]:
                for col, head in enumerate(header):
                    conc[head].append(row[col])
            return phreeqc, conc

        def main(input_file):
            import timeit

            def measure_time(func, *args, **kwargs):
                start = timeit.default_timer()
                phreeqc, conc = func(*args, **kwargs)
                return phreeqc, conc, timeit.default_timer() - start

            phreeqc, conc, run_time = measure_time(run, input_file)            
            
            # export the simulation results
            headers = conc.keys()
            self.selected_output = pandas.DataFrame(conc, columns = headers)
            if self.verbose:
                if self.jupyter:
                    pandas.set_option('display.max_columns', None)
                    display(self.selected_output)
                else:
                    print(self.selected_output)
            self.variables['run_time (s)'] = float(run_time)
       
        # construct the SELECTED_OUTPUT file
        self._define_paths(simulation_name, simulation_directory)
        self._selected_output(selected_output_filename)
        if 'solution_block' in self.results:
            self.results['solution_block'].insert(0, f'# {self.simulation_path}')
            self.results['complete_lines'] = chain(self.results['general_conditions'], self.results['solution_block'], self.results['equilibrium_phases_block'], self.results['reaction_block'], self.results['selected_output_block'], self.results['transport_block']) 
                        
            self.input_file = '\n'.join([line for line in self.results['complete_lines']])       

        with open(self.parameters['input_path'], 'w') as input:
            input.write(self.input_file)
          
        # communicate progress to the user
        estimated_time = (self.parameters['simulation_time']/30)**(self.parameters['quantity_of_modules']/2)*1.0004936**self.parameters['simulation_time'] + 5*self.parameters['quantity_of_modules']
        if self.parameters['database_selection'] == 'sit':
            estimated_time *= 7
        estimated_completion = datetime.datetime.now() + datetime.timedelta(seconds = estimated_time)
        estimated_time, unit = time_determination(estimated_time)
        print(f'\nEstimated completion in {estimated_time} {unit}: {estimated_completion} local time.')
        
        # execute the simulation or parse the selected_output file
        if selected_output_path is None:
            main(self.input_file)
            print('run_time (s):', self.variables['run_time (s)'])
            selected_output_path = os.path.join(os.getcwd(), self.parameters['selected_output_file_name'])  
            
            # verify that the PHREEQC executed and generated the appropriate files
            if self.export_content:
                self.selected_output.to_csv(os.path.join(self.simulation_path, 'selected_output.csv'))
                if not os.path.exists(self.parameters['output_path']):
                    print('\nERROR: The {} output file does not exist. The simulation failed to execute.'.format(self.parameters['output_path']))
        else:
            # define the simulation perspective
            self.parameters['simulation'] = 'scaling'
            if re.search('(brine)', selected_output_path, flags=re.IGNORECASE):
                self.parameters['simulation'] = 'brine'

            # define the simulation type
            self.parameters['simulation_type'] = 'transport'
            for line in selected_output_path:
                if re.search('(evaporation)', line, re.IGNORECASE):
                    self.parameters['simulation_type'] = 'evaporation'

            # define the database contents
            self.parameters['database_selection'] = 'pitzer'
            for database in self.databases:
                names = database.split('_')
                if all(re.search(name, selected_output_path, re.IGNORECASE) for name in names):
                    self.parameters['database_selection'] = database                   
                    break                    

            database_json = json.load(open('./databases/{}.json'.format(self.parameters['database_selection'])))
            self.minerals = database_json['minerals']
            self.elements = database_json['elements']

            # define the simulation
            self.parameters['selected_output_file_name'] = re.search('(\w+)(?=\.)', selected_output_path).group()
                                  
            # preparing the SELECTED_OUTPUT file into a dataframe
            selected_output = open(selected_output_path, 'r')
            if re.search('pqo', selected_output_path):
                sep = '\t'
            else:
                sep = ','
                
            self.selected_output = pandas.read_table(selected_output, sep = sep)
            for column in self.selected_output.columns:
                new_column = column.strip()
                self.selected_output.rename(columns={column:new_column}, inplace = True)
            
        # process the data
        if plot_title is not None:
            self.plot_title = plot_title

        self.variables['initial_solution_mass'] = float(self.selected_output['mass_H2O'][0])
        if self.parameters['simulation_type'] == 'transport':
            self.selected_output.drop(self.selected_output.index[:3], inplace=True)
            self.variables['initial_solution_mass'] = float(self.selected_output['mass_H2O'][3])
        self.variables['final_solution_mass'] = float(self.selected_output['mass_H2O'].iloc[-1])
        self.variables['simulation_cf'] = self.variables['initial_solution_mass'] / self.variables['final_solution_mass']
        self.variables['final_time'] = float(self.selected_output['time'].iloc[-1])
                                 
        # conducting the appropriate visualization function
        if self.parameters['simulation'] == 'brine':
            self.processed_data = self._brine_plot(pyplot, title_font, label_font, export_format, x_label_number, export_name)
        elif self.parameters['simulation'] == 'scaling':
            self.processed_data = self._scaling_plot(title_font, label_font, individual_plots, x_label_number, export_name, export_format)
            if scale_ions and self.processed_data is not None:
                self._ion_proportions()
        else:
            raise TypeError('--> ERROR: The < simulation_perspective > parameter is unpredicted.')
            
        if self.export_content:            
            # export the predicted effluent concentrations
            effluent_concentrations = pandas.DataFrame(list(self.predicted_effluent.items()), columns = ['elements', 'ppm'])
            effluent_concentrations.index = effluent_concentrations['elements']
            del effluent_concentrations['elements']
            effluent_concentrations.to_csv(os.path.join(self.simulation_path, 'effluent_predictions.csv'))
            
            # export the parameters
            parameters = {'parameter':[], 'value':[]}
            for parameter in self.parameters:
                parameters['parameter'].append(parameter)
                parameters['value'].append(self.parameters[parameter])
                
            parameters_table = pandas.DataFrame(parameters)
            parameters_table.to_csv(os.path.join(self.simulation_path, 'parameters.csv'))

            # export the variables
            variables = {'variable':[], 'value':[]}
            for variable in self.variables:
                variables['variable'].append(variable)
                variables['value'].append(self.variables[variable])
                
            variables_table = pandas.DataFrame(variables)
            variables_table.to_csv(os.path.join(self.simulation_path, 'variables.csv'))
                    
        if self.verbose:
            print(self.input_file)
            if self.jupyter:
                display(variables_table)
                display(parameters_table)
            else:
                print(variables_table)
                print(parameters_table)
                
        return self.processed_data
    
    def _ion_proportions(self):
        # calculate the mass of each scalant
        chem_mw = chemw.ChemMW(printing = False)
        mineral_elements = {}
        for column in self.processed_data:                   
            mineral = re.search('([A-Za-z]+)', column).group()
            mineral_elements[mineral] = {}
            chem_mw.mass(self.minerals[mineral]['formula'])
            mineral_elements[mineral]['proportions'] = chem_mw.proportions

        # calculate the precipitated mass of each element
        self.elemental_masses = {}
        for mineral in mineral_elements:
            index = 0
            unit = '(g/m^2)'
            if self.parameters['simulation_type'] == 'evaporation':
                unit = '(g)'
            for scale in self.processed_data[f'{mineral} {unit}']:  
                df_index = f'{self.processed_data.index[index]} (m)'
                if df_index not in self.elemental_masses:
                    self.elemental_masses[df_index] = {}
                    self.elemental_masses[df_index]['ion (g/m^2)'] = {}
                    
                for element in mineral_elements[mineral]['proportions']:
                    precipitated_mass = mineral_elements[mineral]['proportions'][element] * float(scale)
                    if element in self.elemental_masses[df_index]['ion (g/m^2)']:
                        self.elemental_masses[df_index]['ion (g/m^2)'][element] += precipitated_mass
                    elif element in self.elemental_masses[df_index]:
                        self.elemental_masses[df_index][element] += precipitated_mass
                    else:
                        self.elemental_masses[df_index]['ion (g/m^2)'][element] = precipitated_mass

                index += 1

        # print and export the results
        if self.printing:
            print('ionic masses\n', '='*len('ionic masses  '))
            pprint(self.elemental_masses)
            
        if self.export_content:
            with open(os.path.join(self.simulation_path, 'scale_ions.json'), 'w') as output:
                json.dump(self.elemental_masses, output, indent = 4)
                
    def _error(self,error, error_type):
        try:
            export_path = self.simulation_path 
        except:
            export_path = os.getcwd()
            
        error_path = os.path.join(export_path, 'error.txt')
        with open(error_path, 'w') as output:
            output.write(error)
            output.close()
            
        if error_type == 'index':
            raise IndexError(error)
        elif error_type == 'value':
            raise ValueError(error)
            
                                 
    def _brine_plot(self, pyplot, title_font, label_font, export_format, x_label_number, export_name, log_scale = True):
        """Generate plots of the elemental concentrations from effluent brine in the PHREEQC SELECTED_OUTPUT file"""
        # determine the minerals in the simulation      
        columns = []
        for column in self.selected_output.columns:
            if re.search('([A-Z][a-z]?(?:\(\d\))?(?=\(mol\/kgw\)))', column) and not re.search('(_|H2O|pH)', column):
                columns.append(column)

        # parse the brine concentrations from the raw data
        pyplot.figure(figsize = (17,10))
        non_zero_elements = []
        non_zero_columns = []
        time = initial_solution_time = 0
        data = {} 
        concentration_serie = []
        
        # plot parameters
        if self.parameters['domain'] == 'dual':
            if self.parameters['simulation_perspective'] == 'all_distance':
                title_end = 'after {}'.format(sigfigs_conversion(self.parameters['simulation_time']))
            elif self.parameters['simulation_perspective'] == 'all_time':
                title_end = 'over time'     
            self.plot_title = '{} phase {} from the {} {}'.format(self.parameters['domain_phase'].capitalize(), self.parameters['simulation'], self.parameters['water_selection'], title_end)
            
        if self.parameters['simulation_perspective'] == 'all_distance':
            x_label = 'Distance (m)'
            if self.plot_title is None:
                plotted_time = sigfigs_conversion(self.variables['final_time'] - initial_solution_time*self.parameters['timestep'])
                self.plot_title = f'Brine concentrations along the module after {plotted_time} seconds'
        elif self.parameters['simulation_perspective'] == 'all_time':
            x_label = 'Time (s)'
            if self.plot_title is None:
                self.plot_title = 'Effluent brine concentration over time' 
        
        predicted_effluent_concentrations = {}
        for element in columns:
            data[element] = {}
            stripped_element = re.search('([A-Z][a-z]?(?:\(\d\))?(?=\(mol\/kgw\)))', element).group()
            if self.selected_output[element].iloc[-1] > 0: 
                non_zero_elements.append(stripped_element)
                non_zero_columns.append(element)
                
            concentration_serie = []
            if self.parameters['simulation_perspective'] == 'all_time':
                time_serie = []
                insufficient_elements = set()
                for index, row in self.selected_output.iterrows():
                    if all(row[element] > 1e-16 for element in non_zero_columns):
                        concentration_serie.append(row[element])
                        time = sigfigs_conversion(row['time'], 3)
                        time_serie.append(time) # - initial_solution_time * self.parameters['timestep'])
                        data[element][time] = row[element]
                    else:
                        initial_solution_time += 1
                        for element in non_zero_columns:
                            if row[element] < 1e-16:
                                insufficient_elements.add(element)
                pyplot.plot(time_serie,concentration_serie)
                                    
            elif self.parameters['simulation_perspective'] == 'all_distance':
                distance_serie = []
                quantity_of_steps_index = 0
                for index, row in self.selected_output.iterrows():
                    if row['time'] == 0:            
                        quantity_of_steps_index += 1                    
                    elif self.selected_output.at[index-1,'soln'] == quantity_of_steps_index:   
                        pyplot.plot(distance_serie,concentration_serie)
                        concentration_serie.append(row[element])
                        distance_serie.append(row['dist_x'])
                    elif index == len(self.selected_output[element]) + 2:
                        pyplot.plot(distance_serie,concentration_serie)
                        
                        # define the dataframe
                        for x in distance_serie:
                            sigfig_x = sigfigs_conversion(x, 3)
                            index = distance_serie.index(x)
                            data[element][sigfig_x] = concentration_serie[index]
                    else:
                        concentration_serie.append(row[element])
                        distance_serie.append(row['dist_x'])       
                        
        if self.parameters['simulation_perspective'] == 'all_time':
            if len(time_serie) == 0:
                error = f'\n\nThe {insufficient_elements} elements remain below the 1E-16 Molal threshold, and thus the figure could not be constructed.'
                self._error(error, 'index')
                        
        # define the brine plot
        if self.parameters['simulation_perspective'] == 'all_time':
            x_location = []
            index_space = len(time_serie)/x_label_number
            for x in range(x_label_number):
                index = int(index_space * x)
                time = time_serie[index]
                x_location.append(time)
            x_location.append(time_serie[-1])
            pyplot.xticks(x_location)
        legend = non_zero_elements
        legend_title = 'non-zero elements'
        mineral = None
        self._illustrate(pyplot, legend, legend_title, mineral, export_name, label_font, title_font, export_format, log_scale)

        # defining the datatable of brine concentrations
        if self.export_content:
            concentrations_table = pandas.DataFrame(data)
            concentrations_table.index.name = x_label
            concentrations_table.to_csv(os.path.join(self.simulation_path, 'brine_concentrations.csv'))
        if self.printing:
            if self.jupyter:
                display(concentrations_table)
            else:
                print(concentrations_table)
        return concentrations_table            

    def _scaling_plot(self, title_font, label_font, individual_plots, x_label_number, export_name, export_format = 'svg', log_scale = False):
        """Generate plots of scaling along the module distance in the PHREEQC SELECTED_OUTPUT file  """
        # define reused functions
        def legend_determination(time, mineral, mineral_formula):
            time, unit = time_determination(time)
            if self.parameters['simulation_type'] == 'evaporation':
                return f'{mineral} [{mineral_formula}]'
            elif self.parameters['simulation_perspective'] == "all_time":
                if self.parameters['individual_plots']:
                    return time
                elif not self.parameters['individual_plots']:
                    return f'{mineral} [{mineral_formula}] {time} {unit}'
            elif self.parameters['simulation_perspective'] == "all_distance":
                if not self.parameters['individual_plots']:
                    if len(set([t for t in self.selected_output['time']])) == 2:
                        return f'{mineral} [{mineral_formula}]'
                    else:
                        return f'{mineral} [{mineral_formula}] {time} {unit}'
                elif self.parameters['individual_plots']:
                    return sigfigs_conversion(time, 3)
                
        def evaporation():
            self.parameters['individual_plots'] = False
            scaling_data = pandas.DataFrame({})
            pyplot.figure(figsize = (17,10))
            legend = []
            data_length = len(self.selected_output['mass_H2O'])
            data = {}
            for mineral in self.variables['precipitated_minerals']: 
                mineral_formula = self.minerals[mineral]['formula']
                legend.append(legend_determination(0, mineral, mineral_formula))
                data[f'{mineral} (g)'] = {}
                cf_series = []        
                scaling_series = []
                for index, row in self.selected_output.iterrows():
                    if index != len(self.selected_output['mass_H2O']):
                        if row['step'] >= 1:
                            cf = self.variables['initial_solution_mass'] / row['mass_H2O']
                            scale_mass = row[mineral] * self.minerals[mineral]['mass']
                            scaling_series.append(scale_mass) 
                            cf_series.append(cf)   
                            data[f'{mineral} (g)'][float(sigfigs_conversion(cf, 6))] = scale_mass            

                pyplot.plot(cf_series,scaling_series)
                data_df = pandas.DataFrame(data)
                scaling_data = scaling_data.merge(data_df, how = 'outer', left_index = True, right_index = True)
                    
            legend_title = 'scale'
            mineral = None
            if self.plot_title is None:
                self.plot_title = 'Evaporation scaling from the {}'.format(self.parameters['water_selection'])                    
            self._illustrate(pyplot, legend, legend_title, mineral, export_name, label_font, title_font, export_format, log_scale)
            return scaling_data
        
        def all_time_plotting():
            def time_serie(mineral, scaling_data):
                legend_entries = []
                scaling_serie = []
                data = {}
                data[f'{mineral} (g/m^2)'] = {}
                time_serie = []
                for index, row in self.selected_output.iterrows():
                    if row[mineral] > 1e-12:
                        scaling_serie.append(row[mineral])
                        time_serie.append(row['time']) # - initial_solution_time * self.parameters['timestep'])
                        grams_area = (float(row[mineral]) * self.minerals[mineral]['mass']) / (self.parameters['active_m2_cell'])
                        data[f'{mineral} (g/m^2)'][sigfigs_conversion(row['time'], 4)] = sigfigs_conversion(grams_area, 4)
                        legend_entries.append(legend_determination(row['time'], mineral, mineral_formula))
                        
                # defining the plot
                x_location = []
                index_space = len(time_serie)/x_label_number
                for x in range(x_label_number):
                    index = int(index_space * x)
                    time = time_serie[index]
                    x_location.append(time)
                x_location.extend([time_serie[0], time_serie[-1]])
                x_location = [ceil(float(x)) for x in x_location] 
                pyplot.xticks(x_location, x_location)        
                pyplot.plot(time_serie,scaling_serie)
                
                # assigning the data dictionary
                data_df = pandas.DataFrame(data)
                scaling_data = scaling_data.merge(data_df, how = 'outer', left_index = True, right_index = True)
                return legend_entries, scaling_data
            
            scaling_data = pandas.DataFrame({})
            
            for mineral in self.variables['precipitated_minerals']:
                pyplot.figure(figsize = (17,10))
                mineral_formula = self.minerals[mineral]['formula']
                legend_entry, scaling_data = time_serie(mineral, scaling_data)                

                # export the scaling figure
                
                self.plot_title = f'Module end scaling of {mineral} [{mineral_formula}]'
                legend_title = legend = None
                self._illustrate(pyplot, legend, legend_title, mineral, export_name, label_font, title_font, export_format, log_scale)
            return scaling_data
            
        def all_distance_plotting():
            def distance_serie(mineral,):          
                mineral_formula = self.minerals[mineral]['formula'] 
                time = quantity_of_steps_index = 0   
                legend_entries = []
                distance_serie = []
                scaling_serie = []
                data = {}
                data[f'{mineral} (g/m^2)'] = {}
                for index, row in self.selected_output.iterrows():
                    if row['time'] == 0:
                        quantity_of_steps_index += 1
                    elif self.selected_output.at[index-1, 'soln'] == quantity_of_steps_index:
                        if time != 0:
                            legend_entries.append(legend_determination(time, mineral, mineral_formula))

                            pyplot.plot(distance_serie,scaling_serie)
                            grams_area = (float(row[mineral]) * self.minerals[mineral]['mass']) / (self.parameters['active_m2_cell'])
                            scaling_serie.append(sigfigs_conversion(grams_area, 3))
                            distance_serie.append(row['dist_x'])
                        time = row['time']

                    elif index == len(self.selected_output[mineral]) + 2:  
                        legend_entries.append(legend_determination(time, mineral, mineral_formula)) 
                        pyplot.plot(distance_serie,scaling_serie)
                        # define the dataframe
                        for x in distance_serie:
                            sigfig_x = sigfigs_conversion(x, 3)
                            index = distance_serie.index(x)
                            data[f'{mineral} (g/m^2)'][sigfig_x] = sigfigs_conversion(scaling_serie[index], 3)

                    else:
                        grams_area = (float(row[mineral]) * self.minerals[mineral]['mass']) / (self.parameters['active_m2_cell'])
                        scaling_serie.append(grams_area)
                        distance_serie.append(row['dist_x'])

                if self.printing:
                    print('mineral', mineral,' ', self.minerals[mineral]) 
                return legend_entries, data
        
            scaling_data = pandas.DataFrame({})
            pyplot.figure(figsize = (17,10))
            legend = []
            for mineral in self.variables['precipitated_minerals']: 
                legend_entries, data = distance_serie(mineral)
                data_df = pandas.DataFrame(data)
                scaling_data = scaling_data.merge(data_df, how = 'outer', left_index = True, right_index = True)
                legend.extend(legend_entries)
                        
            #pyplot.yscale('log')
            if self.plot_title is None:
                time, units = time_determination(self.variables['final_time'])
                self.plot_title = 'Scaling from the {} after {} {}'.format(self.parameters['water_selection'],time,units)
            
            return legend, scaling_data

        # all of the non-zero minerals are identified and the chemical formulas are sorted into a list
        csv_minerals = []
        non_zero_minerals = set()
        self.variables['precipitated_minerals'] = {}
        for column in self.selected_output.columns:
            if re.search('([A-Z][a-z]{2,})', column) and not re.search('[_(]|(?:Metal)', column):
                mineral = re.search('([A-Z][a-z]{2,})', column).group()
                csv_minerals.append(mineral)
                for value in self.selected_output[mineral]:
                    if value != 0:
                        non_zero_minerals.add(mineral)   
                        if column in self.minerals:
                            self.variables['precipitated_minerals'][mineral] = self.minerals[mineral]
        
        if non_zero_minerals == set():
            print('No scaling occurred.')
            return None            

        # plot the simulation depending upon the simulation perspective   
        self.parameters['individual_plots'] = individual_plots
        if self.parameters['simulation_type'] == 'evaporation':
            scaling_data = evaporation()
        elif self.parameters['simulation_perspective'] == "all_time":
            if self.parameters['individual_plots'] is None:
                self.parameters['individual_plots'] = True
            if self.parameters['individual_plots']:
                scaling_data = all_time_plotting()
            elif not self.parameters['individual_plots']:
                legend, scaling_data = all_distance_plotting()
                mineral = None
                self._illustrate(pyplot, legend, legend_title, mineral, export_name, label_font, title_font, export_format, log_scale)

        elif self.parameters['simulation_perspective'] == 'all_distance':
            if self.parameters['individual_plots'] is None:
                self.parameters['individual_plots'] = False    
            if not self.parameters['individual_plots']:
                legend, scaling_data = all_distance_plotting()
                legend_title = 'scale'
                mineral = None
                self._illustrate(pyplot, legend, legend_title, mineral, export_name, label_font, title_font, export_format, log_scale)
            elif self.parameters['individual_plots']:
                scaling_data = all_time_plotting()
                                
        # finalize the output data
        x_label, y_label = self._determine_labels()
        scaling_data.index.name = x_label
        scaling_data.sort_index(inplace = True)
        scaling_data.to_csv(os.path.join(self.simulation_path, 'scaling_data.csv'))
        
        return scaling_data
    
    def _determine_labels(self): 
        # determine the y-axis label
        if self.parameters['simulation'] == 'scaling':
            if self.parameters['simulation_type'] == 'transport':
                y_label = 'Mass concentration (g/m^2)'
            elif self.parameters['simulation_type'] == 'evaporation':
                y_label = 'Mass (g)'
        elif self.parameters['simulation'] == 'brine':
            y_label = 'Concentration (molal)'
        
        # determine the x-axis label
        if self.parameters['simulation_type'] == 'transport':
            if self.parameters['simulation_perspective'] == 'all_distance':
                x_label = 'Distance (m)'
            elif self.parameters['simulation_perspective'] == 'all_time':
                x_label = 'Time (s)'
        elif self.parameters['simulation_type'] == 'evaporation':
            x_label = 'Concentration Factor (CF)'
        return x_label, y_label
    
    def _illustrate(self, pyplot, legend, legend_title, mineral, export_name, label_font, title_font, export_format, log_scale):
        def export_plot(figure, mineral = None, export_name = None, export_format = 'svg'):
            if export_name is None:
                # define the output name
                if self.parameters['simulation'] == 'scaling':
                    if self.parameters['individual_plots']:
                        export_name = mineral
                    else:
                        export_name = 'all_minerals'
                if self.parameters['simulation'] == 'brine':
                    export_name = 'brine'
            self.results['figures'][export_name] = {'figure':figure, 'title':self.plot_title}

            # export the plot
            file_number = 0
            figure_path = os.path.join(self.simulation_path, export_name)
            if not os.path.exists('{}.{}'.format(figure_path, export_format)):
                figure.savefig('{}.{}'.format(figure_path, export_format))
            elif os.path.exists('{}.{}'.format(figure_path, export_format)):
                while os.path.exists('{}_{}.{}'.format(figure_path, file_number, export_format)):
                    file_number += 1
                figure.savefig('{}_{}.{}'.format(figure_path, file_number, export_format))
                
        # apply the attributes of the figure
        x_label, y_label = self._determine_labels()
        pyplot.grid(True)
        pyplot.title(self.plot_title, fontsize = title_font)
        pyplot.xlabel(x_label, fontsize = label_font)
        pyplot.ylabel(y_label, fontsize = label_font)  
        if legend is not None:
            pyplot.legend(legend, title = legend_title, loc='best', title_fontsize = 'x-large', fontsize = 'large')  
        if self.parameters['simulation_type'] == 'transport':
            pyplot.figtext(0.2, 0.07, 'Final CF: {}'.format(float(sigfigs_conversion(self.variables['simulation_cf'], 4))), wrap=True, horizontalalignment='left', fontsize=12)
        if log_scale:
            pyplot.yscale('log')
        
        figure = pyplot.gcf()
        if self.printing:
            pyplot.show()
        if self.export_content:
            export_plot(figure, mineral, export_name, export_format)

    def test(self):
        self.reactive_transport(simulation_time = 200)
        self.feed_geochemistry(water_selection = 'red_sea')
        self.execute(simulation_name = 'rosspy_test_{}'.format(self.parameters['os']))