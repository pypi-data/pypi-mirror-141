import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import lasio
from welly import Well
from segysak.segy import segy_loader

class prep_data:
    '''
    This class in the SeisLog package loads the well and depth seismic data in a format that allows
    all other classes to be properly executed. It is recommended to use this class to load the data which
    includes the well deviation survey for each well.
    
    The class requires the paths to the LAS file, deviation survey and seismic data.
    '''
    def __init__(self, well, dev_survey, seismic, which='both'):   
        self.well_name=well
        self.seismic_volume=seismic
        
        if which == 'both':
            # load well
            self.well = self.load_well(dev_survey)
            # load seismic
            self.seismic = self.load_seismic()
        elif which == 'well':
            # load well
            self.well = self.load_well(dev_survey)
        elif which == 'seismic':
            # load seismic
            self.seismic = self.load_seismic()
            
    def load_well(self,dev_survey):
        '''
        Load well and deviation survey using Welly
        '''
        self.well_data = Well.from_las(self.well_name)
        # Load deviation survey
        dev = np.loadtxt(dev_survey, skiprows=2, usecols = [0,1,2])
        # Add deviation to wells location attribute
        self.well_data.location.add_deviation(dev)
        # Add positioning (deltaX, deltaY, TVD_KB)
        self.position = np.loadtxt(dev_survey, skiprows=2, usecols = [4,5,3])
        self.position =  np.insert(self.position, 0, np.array((0, 0, 0)), 0)
        self.well_data.location.position=self.position
        return self.well_data

    def load_seismic(self):
        '''
        Load seismic survey using SegySak
        '''
        # load seismic data based on byte locations read from header
        # Based on header there is a scaler of 100 applied to the coordinates which must be reversed
        seis_data = segy_loader(self.seismic_volume, iline=189, xline=193, cdpx=181, cdpy=185, vert_domain='DEPTH')
        self.seis_data = seis_data.assign_coords(cdp_x=seis_data.cdp_x/100, cdp_y=seis_data.cdp_y/100)
        return self.seis_data
    
class depth_conversion:
    '''
    This class in the SeisLog package converts a list of depth values from measured depth
    into total vertical depth subsea. 
    
    The class requires the path to the LAS file, the prepped well data and the list of depth data to 
    be converted. The header of the well LAS file should also contain an elevation value.
    '''
    def MD2TVDSS(well, prepped_well, data):

        # Reload well using lasio for the purposes of extracting the depth  
        well_lasio = lasio.read(well)
        well_df = well_lasio.df().reset_index()
        
        # Convert well MD depths to TVDSS to match seismic depth standard
        temp = prepped_well.location.md2tvd(data) # MDD to TVD
        tvdss = temp - well_lasio.header['Well']['ELEV'].value # TVD to TVDSS  
        return tvdss
        
class trace_extraction:
    '''
    This class in the SeisLog package extracts the seismic trace along the wellbore path. 
    It uses the 'prepped' seismic volume and 'prepped' well with deviation survey loaded.
    'Prepped' here refers to the fact that the data has been appropriately loaded for use 
    in the SeisLog package. Please refer to class 'prep_data'.
    
    The class requires the path to the LAS file, the prepped well and seismic output from the prep_data class, a min
    and max depth of extraction in TVDSS and the sampling interval of the depth seismic
    '''
    def __init__(self, well, prepped_well, prepped_seis, min_depth, max_depth, samp):
        
        self.well = well
        self.prep_well = prepped_well
        self.prep_seis = prepped_seis
        
        # Reload well using lasio for the purposes of extracting the depth  
        self.well_lasio = lasio.read(self.well)
        self.well_df = self.well_lasio.df().reset_index()
        
        # Convert well MD depths to TVDSS to match seismic depth standard
        temp = self.prep_well.location.md2tvd(self.well_df.DEPT) # MDD to TVD
        self.well_df['DEPT'] = temp - self.well_lasio.header['Well']['ELEV'].value # TVD to TVDSS

        # From well header, identify well location
        self.UTM_E = self.well_lasio.sections['Well']['XCOORD'].value
        self.UTM_N = self.well_lasio.sections['Well']['YCOORD'].value
        
        # Define extraction points 
        self.extraction_points = self.define_extraction_points(min_depth, max_depth, samp)
        
        self.trace = pd.DataFrame(columns = ['TVDSS','Amplitude'])
        
        for i in range(len(self.extraction_points)):
            space = self.prep_seis.seis.xysel(cdp_x=self.extraction_points[0][i],cdp_y=self.extraction_points[1][i])
            dep = self.extraction_points[2][i]*-1
            depth = space.sel(depth = self.extraction_points[2][i]*-1 )
            value = depth.data.values[0]
            self.trace.loc[i] = [dep]+[value]

    def define_extraction_points(self, min_depth, max_depth, samp):
        '''
        Define points along wellbore path at which seismic amplitudes will be extracted
        '''
        # Extract depth values along well path
        extraction_points = self.prep_well.location.trajectory(datum=[self.UTM_E,self.UTM_N,self.well_lasio.header['Well']['ELEV'].value],elev=True)
        # Limit extraction points between user defined min and max depths
        extraction_points = extraction_points[-extraction_points[:,2] >= min_depth]
        extraction_points = extraction_points[-extraction_points[:,2] <= max_depth]
        # Round depth extraction values to the sampling of the depth seismic
        extraction_points[:,2] = np.round(extraction_points[:,2]/samp)*samp

        # Build data frame of extraction points
        df = pd.DataFrame(extraction_points)
        extraction_points = df.drop_duplicates(subset=[2], keep='first')
        extraction_points = extraction_points.reset_index()
        
        return extraction_points
    
    
class plot_extractions:
    '''
    This class in the SeisLog package plots the prepped data in map view as well as the 
    extracted trace data in a conventional well log display format. 'Prepped' here refers 
    to the fact that the data has been appropriately loaded for use 
    in the SeisLog package. Please refer to class 'prep_data'.
    
    The class requires a list containing the outputs from the trace_extraction class,
    the prepped seismic data and it is optional to include a list of the well tops. 
    '''
    def pmap(well_list, prepped_seis):
        '''
        Plot a map view of the wellbore path within the seismic survey outline
        '''
        fig = plt.figure(figsize=(8, 8))
        
        # Plot seismic survey outline
        prepped_seis.seismic.seis.plot_bounds(ax=plt.gca())

        # Plot wellbore path  in X-Y
        color = iter(plt.cm.brg(np.linspace(0, len(well_list), 8))) 

        # Plot well path for every well in well_list
        for i in range(len(well_list)):
            c = next(color)
            well_path = well_list[i].prep_well.location.trajectory(
                datum=[well_list[i].UTM_E, well_list[i].UTM_N, well_list[i].well_lasio.header['Well']['ELEV'].value],elev=True)
            df = pd.DataFrame(well_path)
            plt.plot(df[0].values, df[1].values, color = c, label=f"{well_list[i].well}")
            plt.gca().plot(np.array([well_list[i].UTM_E]), np.array([well_list[i].UTM_N]), "ok")
        
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.gca().set_aspect('equal', 'box')

        txt=f"Location of wells relative to 3D seismic extent (dotted line)."
        plt.figtext(0.5, 0.83, txt, wrap=True, horizontalalignment='center', fontsize=14, fontweight='bold');

    def ptrace(well_list, well_tops=[]):
        '''
        Plot a log display of the extracted seismic trace amplitudes
        '''
        fig = plt.figure(figsize=(len(well_list)*2, len(well_list)*4))
        
        # Plot extracted trace for every well in well_list, with corresponding set of tops
        for i in range(len(well_list)):
            fig.add_subplot(1,len(well_list),i+1, sharey = plt.gca(), sharex = plt.gca())
            well_list[i].trace.plot(x='Amplitude', y='TVDSS', kind="line", ax=plt.gca(), legend=False)
            plt.gca().set_title(f'Trace extracted along\n{well_list[i].well}',rotation=90)
            plt.gca().invert_yaxis()
            plt.gca().set_xticks([min(well_list[i].trace['Amplitude']),max(well_list[i].trace['Amplitude'])]) 
            plt.tight_layout()
            
            # If tops exist for this well, then add tops to plot
            if len(well_tops)!=0:
                color = iter(plt.cm.brg(np.linspace(0, well_tops.nunique().top, 20))) 
                for t in range(len(well_tops.iloc[:,0])):
                    if well_tops.iloc[t][0] in well_list[i].well:
                        c = next(color)
                        plt.gca().axhline(y=well_tops.iloc[t,1], color=c, linestyle='-', label=well_tops.iloc[t,2])
                            
    def ptraceplus( well_data, path_well, well_list, well_names, curves, xlims, ylim, well_tops=[]):
        '''
        Plot a trace alongside specified log curves
        '''
        fig, ax = plt.subplots(nrows=1, ncols=(len(curves)+1)*len(well_names), figsize=((len(curves)+1)*len(well_names)*1.8, 14))
        curvecolor = iter(plt.cm.brg(np.linspace(0, len(well_list), 8))) 

        for ind in range(0, len(well_names)*len(curves), len(curves)+1):
            cc = next(curvecolor)
            ii = int(ind/(len(curves)+1))
            well_lasio = lasio.read(path_well+well_names[ii]+'.las')
            dframe = well_lasio.df().reset_index()
            dframe.DEPT = depth_conversion.MD2TVDSS(path_well+well_names[ii]+'.las', well_data[ii].well, dframe.DEPT)

            well_list[ii].trace.plot(x='Amplitude', y='TVDSS', kind="area", ax=ax[ind], legend=False, color=cc)
            ax[ind].set_title(f'{well_names[ii]}\nTrace', fontsize=14, fontweight='bold')
            ax[ind].grid(which='major', color='lightgrey', linestyle='-')
            ax[ind].set_ylim(ylim[1],ylim[0])
            ax[ind].set_xlim([-.25,.25])

            # Loop through each curve and create a track with that data
            for i, c in enumerate(curves, start=1):

                ax[ind+i].plot(dframe[c], dframe.DEPT, color=cc)

                # Cosmetics
                ax[ind+i].set_title(f'{well_names[ii]}\n'+c, fontsize=12, fontweight='bold')
                ax[ind+i].grid(which='major', color='lightgrey', linestyle='-')
                ax[ind+i].invert_yaxis()

                # Only set the y-label for the first track. Hide it for the rest
                if i == 0:
                    ax[ind+i].set_ylabel('DEPTH (m)', fontsize=18, fontweight='bold')
                else:
                    plt.setp(ax[ind+i].get_yticklabels(), visible = False)

                ax[ind+i].set_xlim(xlims[i-1])
                ax[ind+i].grid(which='minor', color='lightgrey', linestyle='-')  
                ax[ind+i].set_ylim(ylim[1],ylim[0])

                # Resistivity scale
                if str(c) in ['RDEP','RMED','RES','RT']:
                    ax[ind+i].set_xscale('log')

            # If tops exist for this well, then add tops to plot
            if len(well_tops)!=0:
                color = iter(plt.cm.brg(np.linspace(0, well_tops.nunique().top, 20))) 
                for t in range(len(well_tops.iloc[:,0])):
                    if well_tops.iloc[t][0] in well_list[ii].well:
                        c = next(color)
                        for i in range(len(curves)+1):
                            ax[ind+i].axhline(y=well_tops.iloc[t,1], color=c, linestyle='-', label=well_tops.iloc[t,2])

        ax[len(curves)].legend(bbox_to_anchor=(0.5, -0.1), loc='lower center',ncol=well_tops.nunique().top, fontsize=12)
        plt.subplots_adjust(wspace=.5)
        plt.show()