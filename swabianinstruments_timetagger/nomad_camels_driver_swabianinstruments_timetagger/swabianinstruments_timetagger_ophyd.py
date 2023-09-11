from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO

import TimeTagger as TT


class TimeTagger(Device):
    countrate = Cpt(Custom_Function_SignalRO, name='countrate')
    correlation = Cpt(Custom_Function_SignalRO, name='correlation')
    count_between_markers = Cpt(Custom_Function_SignalRO, name='count_between_markers')


    countrate_time = Cpt(Custom_Function_Signal, name='countrate_time', kind='config')
    countrate_channels = Cpt(Custom_Function_Signal, name='countrate_channels', kind='config')

    correlation_channel_1 = Cpt(Custom_Function_Signal, name='correlation_channel_1', kind='config')
    correlation_channel_2 = Cpt(Custom_Function_Signal, name='correlation_channel_2', kind='config')
    correlation_binwidth = Cpt(Custom_Function_Signal, name='correlation_binwidth', kind='config')
    correlation_bins = Cpt(Custom_Function_Signal, name='correlation_bins', kind='config')
    correlation_meas_time = Cpt(Custom_Function_Signal, name='correlation_meas_time', kind='config')
    
    cbm_click_channel = Cpt(Custom_Function_Signal, name='cbm_click_channel', kind='config')
    cbm_begin_channel = Cpt(Custom_Function_Signal, name='cbm_begin_channel', kind='config')
    cbm_end_channel = Cpt(Custom_Function_Signal, name='cbm_end_channel', kind='config')
    cbm_n_values = Cpt(Custom_Function_Signal, name='cbm_n_values', kind='config')
    cbm_meas_time = Cpt(Custom_Function_Signal, name='cbm_meas_time', kind='config')

    def __init__(self, prefix="", *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, serial_number='',
                 channels=None, **kwargs):
        super().__init__(prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)

        if name == 'test':
            return
        self.tagger = TT.createTimeTagger(serial=serial_number)
        self.tt_countrate = TT.Countrate(tagger=self.tagger, channels=[0, 1])
        self.tt_countrate.stop()
        self.tt_correlation = None
        self.correlation_config_change = True
        self.tt_cbm = None
        self.cbm_config_change = True

        channels = channels or {}
        for channel, info in channels.items():
            self.tagger.setTriggerLevel(int(channel), float(info['trigger_level']))
            self.tagger.setInputDelay(int(channel), int(info['input_delay']))
            self.tagger.setDeadtime(int(channel), int(info['dead_time']))
            self.tagger.setTestSignal(int(channel), info['test_signal'])

        self.countrate.read_function = self.read_countrate
        self.countrate.trigger_function = self.start_countrate

        self._countrate_avg_time = 1e12
        self.countrate_time.put_function = self._set_countrate_time
        self.countrate_channels.put_function = self._update_countrate_channels
        

        self.correlation.trigger_function = self.start_correlation
        self.correlation.read_function = self.read_correlation

        self._correlation_meas_time = 1e12
        self.correlation_bins.put_function = self._set_correlation_config
        self.correlation_binwidth.put_function = self._set_correlation_config
        self.correlation_channel_1.put_function = self._set_correlation_config
        self.correlation_channel_2.put_function = self._set_correlation_config
        self.correlation_meas_time.put_function = self._set_correlation_meas_time
        

        self.count_between_markers.trigger_function = self.start_cbm
        self.count_between_markers.read_function = self.read_cbm

        self._cbm_meas_time = 1e12
        self.cbm_n_values.put_function = self._set_cbm_config
        self.cbm_click_channel.put_function = self._set_cbm_config
        self.cbm_begin_channel.put_function = self._set_cbm_config
        self.cbm_end_channel.put_function = self._set_cbm_config
        self.cbm_meas_time.put_function = self._set_cbm_meas_time


    
    def _update_countrate_channels(self, channels):
        if not channels:
            raise Exception('there are no channels for the countrate measurement!')
        if isinstance(channels, str):
            if ' ' in channels:
                channels = channels.split(' ')
            elif ',' in channels:
                channels = channels.split(',')
            elif ';' in channels:
                channels = channels.split(';')
        if isinstance(channels[0], str):
            for i, chan in enumerate(channels):
                channels[i] = int(chan)
        self.tt_countrate.stop()
        self.tt_countrate = TT.Countrate(tagger=self.tagger, channels=channels)
        self.tt_countrate.stop()

    def _set_countrate_time(self, value):
        self._countrate_avg_time = value*1e12

    def _set_correlation_config(self, value):
        self.correlation_config_change = True

    def _set_correlation_meas_time(self, value):
        self._correlation_meas_time = value*1e12

    def _set_cbm_config(self, value):
        self.cbm_config_change = True

    def _set_cbm_meas_time(self, value):
        self._cbm_meas_time = value*1e12
    
    def start_correlation(self):
        if self.correlation_config_change:
            self.tt_correlation = TT.Correlation(tagger=self.tagger,
                                                channel_1=self.correlation_channel_1.get(),
                                                channel_2=self.correlation_channel_2.get(),
                                                binwidth=self.correlation_binwidth.get(),
                                                n_bins=self.correlation_bins.get())
            self.correlation_config_change = False
        self.tt_correlation.stop()
        self.tt_correlation.clear()
        self.tt_correlation.startFor(self._correlation_meas_time)
    
    def read_correlation(self):
        self.tt_correlation.waitUntilFinished()
        self.tt_correlation.stop()
        data = self.tt_correlation.getData()
        return data

    def start_cbm(self):
        if self.cbm_config_change:
            self.tt_cbm = TT.CountBetweenMarkers(tagger=self.tagger,
                                                 click_channel=self.cbm_click_channel.get(),
                                                 begin_channel=self.cbm_begin_channel.get(),
                                                 end_channel=self.cbm_end_channel.get(),
                                                 n_values=self.cbm_n_values.get())
        self.tt_cbm.stop()
        self.tt_cbm.clear()
        self.tt_cbm.startFor(self._cbm_meas_time)
    
    def read_cbm(self):
        self.tt_cbm.waitUntilFinished()
        self.tt_cbm.stop()
        data = self.tt_cbm.getData()
        return data

    def start_countrate(self):
        self.tt_countrate.stop()
        self.tt_countrate.clear()
        self.tt_countrate.startFor(self._countrate_avg_time)
    
    def read_countrate(self):
        self.tt_countrate.waitUntilFinished()
        self.tt_countrate.stop()
        data = self.tt_countrate.getData()
        return data

    def finalize_steps(self):
        TT.freeTimeTagger(self.tagger)


if __name__ == '__main__':
    # tagg = TimeTagger(name='tagg', serial_number='1729000IDH')
    
    settings = {'serial_number': '1729000IDH', 'channels': {'0': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': True}, '8': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': True}, '1': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': True}, '9': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': True}, '2': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '10': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '3': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '11': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '4': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '12': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '5': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '13': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '6': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '14': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '7': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}, '15': {'trigger_level': 0.5, 'dead_time': 6000, 'input_delay': 0, 'test_signal': False}}}
    additional_info = {'description': '', 'device_class_name': 'TimeTagger'}
    tagg = TimeTagger("swabianinstruments_timetagger:", name="swabianinstruments_timetagger", **settings)
    tagg.countrate.trigger()
    print(tagg.countrate.get())
    tagg.finalize_steps()

