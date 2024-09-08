from flask import Flask, render_template, request, redirect, url_for, send_file
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import speedx
import os
import random

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Verifica se as pastas de upload e processamento existem
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/30fps.mp4')
def ogfpsvideo():
    return send_file('30fps.mp4')
@app.route('/60fps.mp4')
def convertedfpsvideo():
    return send_file('60fps.mp4')
@app.route('/video.png')
def videoimage():
    return send_file('video.png')

@app.route('/') 
def index():
    return open('index.html', 'r').read()

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(url_for('index'))

    file = request.files['video']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(video_path)

        # Processa o vídeo (desacelerar, acelerar e definir para 60 FPS)
        processed_video_path = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_' + file.filename)
        process_video(video_path, processed_video_path)

        return send_file(processed_video_path, as_attachment=True)

def process_video(input_path, output_path):
    video = VideoFileClip(input_path)
    slowed_video = speedx(video, 0.25)  # Desacelerar
    slowed_video.set_fps(60)
    N = random.randint(1, 100)
    slowed_video.write_videofile(f'processing#{N}.mp4', fps=60)
    slowed_video = VideoFileClip(f'processing#{N}.mp4')
    accelerated_video = speedx(slowed_video, 4)  # Acelerar
    final_video = accelerated_video.set_fps(60)  # Definir para 60 FPS
    final_video.write_videofile(output_path, fps=60)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='2020')
