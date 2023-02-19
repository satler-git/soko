'''fftを使って短時間フーリエ変換(stft)'''

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from skimage import util


rate, audio = wavfile.read(r"JEI説明.wav", "r") # waveファイルを読み込み用ファイルとして開く

audio = np.mean(audio, axis=1) # ステレオをモノラルに変換
N = audio.shape[0] # 要素数を返す
L = N/rate # 長さの算出


f, ax = plt.subplots()
ax.plot(np.arange(N)/rate, audio)
ax.set_xlabel('Time[s]')
ax.set_ylabel('Amplitude[unknown]')
plt.show()

M = 1024 # スライスのサンプル数

slices = util.view_as_windows(audio, window_shape=(M,), step=100) # スライス分割

window = np.hamming(M+1)[:-1] # 窓関数の生成
slices = slices * window # スライスに窓を掛け合わせる


slices = slices.T

spectrum = np.fft.fft(slices, axis=0)[:N] # スライスをフーリエ変換
spectrum = np.abs(spectrum) # スペクトラムの絶対値を取っている


f, ax = plt.subplots()

S = np.abs(spectrum) # スペクトラムの絶対値を取る
with np.errstate(divide='ignore', invalid='ignore'):
    S = 20 * np.log10(S / np.max(S)) # スペクトラムの対数値を取る

ax.imshow(S, origin='lower', cmap='viridis', extent=(0, L, 0, rate/2/1000))
ax.axis('tight')
ax.set_ylabel('Frequency[kHz]')
ax.set_xlabel('Time[s]')

plt.show()