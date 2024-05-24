from views import *

app.config['UPLOAD_FOLDER'] = statics.csv_local_up

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

