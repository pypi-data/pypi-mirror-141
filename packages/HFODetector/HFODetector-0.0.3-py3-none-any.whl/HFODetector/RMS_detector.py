import mne
import numpy as np
from calendar import EPOCH
import numpy as np
import pandas as pd
from scipy.signal import *
import matplotlib.pyplot as plt
from scipy.io import loadmat
import os 
from utils.utils import parallel_process, reorder
 
class RMS_detector():
    def __init__(self, params = None):
        
        self.params = {
            # default params for staba detector
            'sample_freq': 2000,        # (Hz)
            'filter_freq': [80, 500],   # filter freq (Hz)
            'rms_window' : 3 * 1e-3,    # RMS window time (s) *
            'min_window' : 6 * 1e-3,    # min window time for an HFO (s) *
            'min_gap'    : 10 * 1e-3,   # min gap time between two HFOs (s) *
            'epoch_len'  : 600,         # cycle time (s) *
            'min_osc'    : 6,           # min number of oscillations per interval
            'rms_thres'  : 5,           # threshold for RMS in (SD's)
            'peak_thres' : 3            # threshold for finding peaks
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.sos = loadmat(os.path.join(dir_path, 'SOS.mat'))['v_SOS'].copy(order='C')
    
    def predict_edf(self, edf_path):
        raw, channels = self._read_raw(edf_path)
        return self.predict_npz(data=raw, channels=channels)
    
    def predict_npz(self, data, channels):
        data = np.array(data)
        channels = np.array(channels)
        param_list = [{"data":data[i], "channel_names":channels[i]} for i in range(len(channels))]
        ret = parallel_process(param_list, self._predict, n_jobs=32, use_kwargs=True, front_num=1)
        channel_name, HFOs = [], []
        for j in ret:
            if not type(j) is tuple:
                print(j)
            if j[0] is None:
                continue
            HFOs.append(j[0])
            channel_name.append(j[1])
        channel_names = np.squeeze(np.array(channel_name))
        HFOs = np.array(HFOs, dtype=object)
        index = reorder(channels, channel_names)
        return channel_names[index], HFOs[index]
    
    def predict_channel(self, data):
        """_summary_

        Args:
            data (np.array): one-d array
        """
        filtered = self._preprocess(data)
        # filtered_all.append(filtered)
        rms = self._compute_rms(filtered)
        epoch_lims = self._compute_epoch_lims(len(filtered))
        HFOs = self._get_HFOs(filtered, rms, epoch_lims)
        return HFOs
    
    def _predict(self, data, channel_names):
        return self.predict_channel(data), channel_names
    
    def _read_raw(self, raw_path):
        raw = mne.io.read_raw_edf(raw_path) 
        raw_channels = raw.info['ch_names']
        channels = [ch for ch in raw_channels]
        data = []

        for raw_ch in raw_channels:
            ch_data = raw.get_data(raw_ch) * 1E6
            data.append(ch_data)
        
        data = np.squeeze(np.array(data))
        return data, channels


    def _preprocess(self, raw):
        
        SAMPLE_FREQ = self.params['sample_freq']
        FILTER_FREQ = self.params['filter_freq']

        # prepocessing filter: iir, cheby2
        nyq = SAMPLE_FREQ / 2 
        rp = 0.5 # max loss in passband (dB)
        rs = 100 # min attenuation in stopband (dB)
        space = 0.5

        low, high = FILTER_FREQ
        scale = 0
        while low > 0 and low < 1:
            low *= 10
            scale += 1
        low = FILTER_FREQ[0] - (space * 10**(-1 * scale)) 

        scale = 0
        while high < 1:
            high *= 10
            scale += 1
        high = FILTER_FREQ[1] + (space * 10**(-1 * scale))

        k = 8.5067E-4
        # filtered = sosfiltfilt(sos, raw) # similar but first parts different
        filtered = sosfilt(self.sos, raw)
        filtered = sosfilt(self.sos, np.flipud(filtered))
        filtered = np.flipud(filtered) * (k**2)
        
        return filtered


    def _compute_rms(self, filtered):
        RMS_WINDOW = round(self.params['rms_window'] * self.params['sample_freq'])
        if (RMS_WINDOW % 2) == 0:
            RMS_WINDOW += 1

        # rms calculus - calculate energy from filtered signal
        temp = np.square(filtered)
        temp = lfilter(np.ones((RMS_WINDOW)), 1, temp, axis=0)/RMS_WINDOW
        rms = np.zeros(len(temp))
        rms[:int(-np.floor(RMS_WINDOW/2))] = temp[int(np.floor(RMS_WINDOW/2)):]
        rms = np.sqrt(rms)

        return rms


    def _compute_epoch_lims(self, len_signal):
        EPOCH_LEN = round(self.params['epoch_len'] * self.params['sample_freq'])
        
        temp = np.arange(0, len_signal, EPOCH_LEN)
        if temp[-1] < len_signal:
            temp = np.append(temp, [len_signal])
        epoch_lims = np.vstack([[temp[:-1].T, temp[1:]]]).T
        return epoch_lims

    def _get_HFOs(self, filtered, rms, epoch_lims):
        RMS_THRES = self.params['rms_thres']
        MIN_WINDOW = round(self.params['min_window'] * self.params['sample_freq'])
        MIN_GAP = round(self.params['min_gap'] * self.params['sample_freq'])
        PEAK_THRES = self.params['peak_thres']
        MIN_OSC = self.params['min_osc']

        HFOs = []
        for i, j in epoch_lims:
            # calculate threshold
            window = np.zeros(len(rms))
            window[i:j] = 1
            rms_epoch = rms * window
            rms_interval = rms[i:j]
            epoch_filt = filtered[i:j]
            thres_rms = (rms_epoch > (np.mean(rms_interval) + RMS_THRES * np.std(rms_interval))).astype('int')

            if len(np.argwhere(thres_rms)) == 0:
                # print("none satisfies THRES_RMS requirement")
                pass
            
            wind_thres = np.pad(thres_rms, 1)
            wind_jumps = np.diff(wind_thres)
            wind_jump_up = np.argwhere(wind_jumps == 1)
            wind_jump_down = np.argwhere(wind_jumps == -1)
            wind_dist = wind_jump_down - wind_jump_up
            # print(np.array([wind_jump_up, wind_jump_down, wind_dist]).T)
            wind_ini = wind_jump_up[wind_dist > MIN_WINDOW]
            wind_end = wind_jump_down[wind_dist > MIN_WINDOW]

            if len(wind_ini) == 0:
                # print("none satisfies MIN_WINDOW requirement")
                pass

            while(True):
                next_ini = wind_ini[1:]
                last_end = wind_end[:-1]
                wind_idx = (next_ini - last_end) < MIN_GAP
                
                if np.sum(wind_idx) == 0:
                    # print("break while")
                    break
                
                new_end = wind_end[1:]
                last_end[wind_idx] = new_end[wind_idx]
                wind_end[:-1] = last_end

                idx = np.diff(np.pad(wind_end, (1, 0))) != 0
                wind_ini = wind_ini[idx]
                wind_end = wind_end[idx]

            wind_intervals = np.array([wind_ini, wind_end]).T
            # print(wind_intervals)

            # select intervals
            count = 1
            wind_select = []
            thres_peak = np.mean(np.abs(epoch_filt) + PEAK_THRES * np.std(np.abs(epoch_filt)))
            
            for ii, jj in wind_intervals:
                temp = np.abs(filtered[ii:jj])
                if len(temp) < 3:
                    continue

                peak_ind, _ = find_peaks(temp, height=thres_peak)
                if len(peak_ind) < MIN_OSC:
                    continue
                
                wind_select.append([ii+1, jj])
                count += 1

            if len(wind_select):
                HFOs += wind_select
        return HFOs
        
    