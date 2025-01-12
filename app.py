import os
import yt_dlp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar_musicas():
    urls = request.form['urls'].split(',')
    way_pend = request.form['pendrive']
    mensagens = []

    try:
        for url in urls:
            url = url.strip()
            if url:
                # Função de conversão e download
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(way_pend, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'ffmpeg_location': r"C:\Users\otavi\OneDrive\Área de Trabalho\ffmpeg\ffmpeg-7.1-full_build\ffmpeg-7.1-full_build\bin",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    sanitized_title = "".join([c if c.isalnum() or c in " ._-()" else "_" for c in info['title']])
                    music_title = f"{sanitized_title}.mp3"
                    music_path = os.path.join(way_pend, music_title)

                    if os.path.exists(music_path):
                        mensagens.append(f"A música '{music_title}' já está no pendrive.")
                    else:
                        ydl.download([url])
                        mensagens.append(f"Música '{music_title}' baixada com sucesso!")
    except Exception as e:
        mensagens.append(f"Houve um erro ao processar as URLs: {e}")

    return jsonify({'mensagens': mensagens})

if __name__ == '__main__':
    app.run(debug=True)
