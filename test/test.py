import numpy as np
import pyaudio

# 参数设置
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURATION = 5  # 录音时长（秒）

# 创建PyAudio对象
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("开始录音...")

frames = []

# 录音
for i in range(0, int(RATE / CHUNK * DURATION)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束.")

# 关闭音频流
stream.stop_stream()
stream.close()
audio.terminate()

# 将录取的音频数据转换为numpy数组
audio_data = np.frombuffer(b''.join(frames), dtype=np.float32)

# 计算频谱信息
fft_result = np.fft.fft(audio_data)
frequencies = np.fft.fftfreq(len(fft_result)) * RATE
spectrum = 20 * np.log10(np.abs(fft_result))

# 打印频谱信息
print("频率:", frequencies)
print("频谱:", spectrum)

# 绘制频谱图
