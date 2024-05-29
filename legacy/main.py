# Список для хранения данных
from typing import Dict, Any

ionogram_data = []
import pandas as pd

file = "../input_data/AS00Q_2003081131505.MMM"


# file = "WP937_2015053000008.MMM"
channel_to_Doppler: dict[int | Any, float | Any] = {
    # For Pol 90 degrees
    0: 0.781,
    2: 2.344,
    4: 3.906,
    6: 5.469,
    8: -0.781,
    10: -2.344,
    12: -3.906,
    14: -5.469,
    # For Pol -90 degrees
    1: 0.781,
    3: 2.344,
    5: 3.906,
    7: 5.469,
    9: -0.781,
    11: -2.344,
    13: -3.906,
    15: - 5.469,
}

class Preface:
    def __init__(self):
        pass


def read_preface(block):
    res = Preface()

    END_SYMBOL = block[-16]
    if END_SYMBOL == 14:
        res.NUMBER_HEIGHTS = 128
    else:
        raise ValueError("Программа не знает тип дигизонда")

    res.STATION = f"{block[43]}{block[44]}{block[45]}"
    res.YYYY = f"20{block[3]}{block[4]}"
    res.DDD = block[5] * 100 + block[6] * 10 + block[7]
    date_time = pd.to_datetime(res.DDD - 1, unit='D', origin=res.YYYY)
    res.MONTH = date_time.month
    res.DAY = date_time.day
    res.HH = f"{block[8]}{block[9]}"
    res.MM = f"{block[10]}{block[11]}"
    res.SS = f"{block[12]}{block[13]}"

    # P1=B ionograms by DGS-256

    # Start freq (MHz)
    res.START_FREQ = block[35] * 10 + block[36]

    # Increment freq:
    # 0 – 0.2 MHz
    # 1 – 0.1 MHz
    # 2 – 0.05 MHz
    # 3 – 0.025 MHz
    # 4 – 0.01 MHz
    # 5 – 0.05 MHz
    res.INC_FREQ = 0

    INC_FREQ_TYPE = block[37]
    if INC_FREQ_TYPE == 0:
        res.INC_FREQ = 0.2
    if INC_FREQ_TYPE == 1:
        res.INC_FREQ = 0.1
    if INC_FREQ_TYPE == 2:
        res.INC_FREQ = 0.05
    if INC_FREQ_TYPE == 3:
        res.INC_FREQ = 0.025
    if INC_FREQ_TYPE == 4:
        res.INC_FREQ = 0.01
    if INC_FREQ_TYPE == 5:
        res.INC_FREQ = 0.05

    # End freq (MHz)
    res.END_FREQ = block[38] * 10 + block[39]

    # Increment range (km):
    # 0 – 2.5 Km
    # 1 – 5 Km
    # 2 – 10Km
    res.INC_RANGE = 0

    INC_RANGE_TYPE = block[56]
    if INC_RANGE_TYPE == 0:
        res.INC_RANGE = 2.5
    if INC_RANGE_TYPE == 1:
        res.INC_RANGE = 5
    if INC_RANGE_TYPE == 2:
        res.INC_RANGE = 10

    # Start range (km):
    # 0 – 0Km
    # 1 – 10Km
    # 2 – 60Km
    # 3 – 160Km
    res.START_RANGE = 0
    START_RANGE_TYPE = block[57]
    if START_RANGE_TYPE == 1:
        res.START_RANGE = 10
    if START_RANGE_TYPE == 2:
        res.START_RANGE = 60
    if START_RANGE_TYPE == 3:
        res.START_RANGE = 160

    # End range (km):
    res.END_RANGE = res.START_RANGE + res.NUMBER_HEIGHTS * res.INC_RANGE

    return res


def high_nibble(byte):
    return byte >> 5


def low_nibble(byte):
    return byte & 0x07  # 0x0F == 15


cv = pd.DataFrame()

apms = []
AMP_Ps = []
statuses = []
heights = []
freqs = []
st_s = []
pols = []
NOISE = []

# THRESHOLD_MPA = 6

with open(file, "rb") as f:
    block = f.read(4096)
    preface = read_preface(block)
    current_freq = preface.START_FREQ
    step_freq = preface.INC_FREQ
    # end_freq = preface.END_FREQ
    end_freq = 14

    cur_range = preface.START_RANGE
    step_range = preface.INC_RANGE

    block = block[60:]
    while len(block) != 0 and current_freq <= end_freq:
        for i in range(30):
            if current_freq > end_freq:
                break
            prelude = block[:6]
            mpa = prelude[5]
            data = block[6:134]
            block = block[134:]
            cur_range = preface.START_RANGE
            step_range = preface.INC_RANGE

            # print(preface[5:6])
            # min_threshold = (high_nibble(data[0]) + 2) * 6
            # for j in range(len(data)) or current_freq <= end_freq:
            #     new_possible_threshold = (high_nibble(data[0]) + 2) * 6
            #     if new_possible_threshold < min_threshold:
            #         min_threshold = new_possible_threshold

            # min_threshold = preface[4] + THRESHOLD_MPA
            # min_threshold += THRESHOLD_MPA
            for j in range(len(data)):
                if current_freq > end_freq:
                    break
                # if min_threshold < (high_nibble(data[j])+2)*6:
                NOISE.append(mpa)

                apms.append(high_nibble(data[j]))
                AMP_Ps.append((high_nibble(data[j]))*6)

                number_channel = low_nibble(data[j])
                st_s.append(number_channel)
                if number_channel % 2 == 0:
                    pols.append(-90)
                else:
                    pols.append(90)

                doppler = channel_to_Doppler[number_channel]
                statuses.append(doppler)
                heights.append(cur_range)
                freqs.append(current_freq)
                cur_range += step_range
            current_freq += step_freq
        block = f.read(4096)

    df = pd.DataFrame({
        'Freq': freqs,
        'Range': heights,
        'Doppler': statuses,
        'Polarize': pols,
        'Ampltude': AMP_Ps,
        'Ampltude_before_proc': apms,
        'Antena_channel': st_s,
        'MPA': NOISE,
    })
    df.to_csv('formated_data.csv', index=False, float_format='%.3f')
