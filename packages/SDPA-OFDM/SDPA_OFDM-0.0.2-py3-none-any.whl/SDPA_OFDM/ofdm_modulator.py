"""
Main OFDM modulator class

Must be instanciated as such :
    modulator = ofdm_modulator(settings)

Output can be requested by calling the appropriate function, i.e.
    I, Q = modulator.getIQ()
"""

from tabnanny import verbose
from SDPA_OFDM.modulations import get_modulator
import math
import numpy as np
from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq


class ofdm_modulator():
    def __init__(self, N_FFT=32, BW=8e6, modulation='BPSK', rate=None, rep=None, padding=None, MSB_first=True, verbose=False):
        """
        Returns an OFDM modulator with the desired settings

        Parameters
        ----------
        N_FFT : int
            Number of FFT channels used (default 32)
        BW : int, float
            Half bandwidth in Hz, total is 2*BW (default 8 Mhz)
        modulation : {'BPSK', 'QPSK', 'QAM16'}
            Type of modulation used, by default BPSK
        rate : ?
            TODO : Implement
        rep : ?
            TODO : Implement
        padding : ?
            TODO : Implement
        verbose : bool
            if True, prints informations throughout the process (False by default)
        MSB_first : bool
            Specifies is the MSB is first in the message (True by default)
        """
        # Check types and values
        if not isinstance(N_FFT, int):
            raise ValueError("N_FFT must be int type")
        else:
            if not math.log(N_FFT, 2).is_integer():
                raise ValueError("N_FFT must be a power of 2")
        if not (isinstance(BW, int) or isinstance(BW, float)):
            raise ValueError("BW must be int or float")
        if not isinstance(modulation, str):
            raise ValueError("modulation must be str")
            # No need to check for valid string, the modulation module will do it
            #             
        self._N_FFT = N_FFT
        self._BW = BW
        self._modulator = get_modulator(modulation, HIGH=1, MSB_first=MSB_first)
        self.verbose = verbose

        self._IG = 1/8 # TODO : do this correctly

        self._N_pilots = 4 # TODO : do this correctly
        self._bits_per_symbol = self._modulator.bits_per_symbol()

        self._message_split_length = (self._N_FFT - self._N_pilots) * self._bits_per_symbol



    def _split_message(self, message, pad=False):
        """
        Splits a message into multiple parts (each with a size suitable for the IFFT)

        Parameters
        ----------
        message : 1D numpy.array
            The message to modulate. Size must be a multiple of (N_FFT - number of pilots)
        pad : bool
            Pad the message with 0s to reach the desired length. False by default
        """
        # We assume the message is 1D and with the correct number of elements
        #
        # The split order is :
        #
        # 0  n+1 . .
        # 1  n+2 . .
        # .   .  . .
        # .   .  . .
        # n  2n  . .
        # 
        # Each column represents an OFDM symbol
        # Each element (row by row) is a IFFT channel (minus the pilots)
        self._print_verbose("Splitting message...")
        if pad:
            # Add 0s to reach the right size
            missing_zeros = int(np.ceil(message.size / self._message_split_length) * self._message_split_length - message.size)
            message = np.concatenate([message, np.zeros(missing_zeros)])
            self._print_verbose(f"    Padding message with {missing_zeros} zeros")
        
        message_split = message.reshape(self._message_split_length, -1, order='F')
        self._print_verbose(f"    Splitting message from length {message.size} to {message_split.shape} ({message_split.shape[0]} channels before mapping and {message_split.shape[1]} OFDM symbols)")
        return message_split
        
        
        
    def _constellation_map(self, message):
        """
        Maps the message with the specified constellation

        Parameters
        ----------
        message : numpy array
            Values to map along rows. Each column is a symbol 

        Returns
        -------
            mapped_message : numpy array
                Converted message
        """
        self._print_verbose(f"Constellation mapping using {self._modulator.name}...")
        mapped_message = self._modulator.convert(message)
        print(mapped_message.shape)
        self._print_verbose(f"    New message size {message.shape} -> {mapped_message.shape} ({mapped_message.shape[0]} + pilots as IFFT channels and {mapped_message.shape[1]} OFDM symbols)")
        return mapped_message

    def _add_pilots(self, message):
        """
        Adds pilots to the message (to reach IFFT size)

        Parameters
        ----------
        message : numpy array

        Returns
        -------
        ifft_channels : numpy array        
        """
        # Only adding 0s at the moment
        # TODO : Study OFDM pilots and update this code
        # Maybe add a sequential option (OFDM pilots are dependent on the previous ones)
        message_str = '-'*message.shape[0]
        self._print_verbose("Adding OFDM pilots...")
        self._print_verbose("    Message without pilots :")
        self._print_verbose(f"    {message_str} ({message.shape[0]}x)")
        
        # Currently this system puts a pilot at the beggining, one at the end and the rest in the middle
        # Pilots MUST be in the right order !
        pilots_indices = np.concatenate([np.array([0]), -np.arange(self._N_pilots - 2)[::-1] + self._N_FFT//2, np.array([self._N_FFT-1])])
        self._print_verbose(f"    Adding pilots at indices : {pilots_indices}")
        
        ifft_channels = message.copy()
        for i in pilots_indices:
            ifft_channels = np.insert(ifft_channels, i, 0, axis=0)
            message_str = message_str[0:i] + 'P' + message_str[i:]

        self._print_verbose("    Message with pilots :")
        self._print_verbose(f"    {message_str} ({ifft_channels.shape[0]}x)")

        return ifft_channels

    def _ifft(self, channels):
        """
        Applies iFFT to the message (channels). The iFFT is applied on the rows (each column is a separate symbol)

        Parameters
        ----------
        channels : numpy array
            The input data of the iFFT
        
        Returns
        -------
        t : numpy array
            time vector
        signal : numpy array
            time domain signal
        """
        self._print_verbose(f"Applying iFFT to the signal...")
        # ifftshift is very important since the spectrum was created "how it looks" but the ifft does 0-> Fs/2 -> -Fs/2 -> 0-dF
        signal = ifft(ifftshift(channels, axes=0), axis=0)
        # Time vector (and corresponding sampling period)
        deltaF = 2*self._BW / (channels.shape[0]-1)
        Ts = 1/(signal.shape[0] * deltaF)
        t = np.arange(0, signal.shape[0] * Ts, Ts)

        return t, signal

    def _cyclic_prefix(self, signal):
        """
        Adds cyclic prefix to the corresponding signal (along the rows). The fraction of cyclic prefix is given by IG

        Parameters
        ----------
        signal : numpy array
            the signal

        Returns
        -------
        cyclic_signal : numpy array
            the signal with cyclic prefix
        """
        self._print_verbose("Adding cyclic prefix...")
        
        cyclic_signal = np.concatenate([signal[0:int(signal.shape[0]*self._IG)], signal])
        self._print_verbose(f"    Signal {signal.shape} -> {cyclic_signal.shape}")        
        return cyclic_signal

    def messageToIQ(self, message, pad=False):
        """
        Applies OFDM modulation to the provided message

        Parameters
        ----------
        message : numpy array
            Array containing the bits to transmit
        pad : bool
            Pad the message with 0s to reach the desired length. False by default

        Returns
        -------
        I : Real part of the signal
        Q : Imaginary part of the signal
        """
        # Check types and values
        if not isinstance(message, np.ndarray):
            raise ValueError("Message must be a numpy array")
        message = np.squeeze(message)
        if message.ndim != 1:
            raise ValueError("Message must be one-dimensional")
        elif np.mod(message.size, self._message_split_length) != 0 and pad == False:
            raise ValueError(f"Message size must be a multiple of {self._message_split_length} (it currently is {message.size})")
        
        ### Splitting (separating message into OFDM symbols before IFFT) ###
        message_split = self._split_message(message, pad)

        ### Constellation mapping ###
        message_split_mapped = self._constellation_map(message_split)

        ### Adding pilots ###
        message_split_mapped_pilots = self._add_pilots(message_split_mapped)

        ### IFFT ###
        _, signal = self._ifft(message)

        ### Cyclic prefix ###
        signal_cyclic = self._cyclic_prefix(signal)

        I, Q = signal_cyclic.real, signal_cyclic.imag

        return I, Q

    def _print_verbose(self, message : str):
        """
        Prints additionnal information if the verbose flag is True
        """
        if(self.verbose):
            print(message)


        