from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                video_title = info_dict.get('title', None)
                
                filename = f"{video_title}.mp4"
                ydl_opts = {
                    'outtmpl': filename,
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                response = send_file(filename, as_attachment=True)
                response.headers["Content-Disposition"] = "attachment; filename=" + filename

                # Schedule file deletion after response is closed
                response.call_on_close(lambda: os.remove(filename))
                print("deleted")
                return response
        except Exception as e:
            return str(e)
    return '''
    <form method="post">
        <input type="text" name="video_url">
        <input type="submit" value="Download">
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)