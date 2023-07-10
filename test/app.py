from flask import *
from cvzone.ClassificationModule import Classifier
import os
import cv2
import cvzone
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def main():
	return render_template("index.html")

@app.route('/success', methods = ['POST'])
# def success():
# 	if request.method == 'POST':
# 		f = request.files['file']
# 		f.save(f.filename)
        
# 		#pred = predict_img(f)
# 		#return render_template("upload.html", name = pred.filename)
# 		return render_template("upload.html", name = f.filename)


def predict_img(i):

	img = cv2.imread(i)
	classifier = Classifier('Model/keras_model.h5', 'Model/labels.txt')
	imgArrow = cv2.imread('arrow.png', cv2.IMREAD_UNCHANGED)
	classIDBin = 0

	imgWasteList = []
	pathFolderWaste = "Waste"
	pathList = os.listdir(pathFolderWaste)
	for path in pathList:
		imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

	imgBinsList = []
	pathFolderBins = "Bins"
	pathList = os.listdir(pathFolderBins)
	for path in pathList:
		imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))

	classDic = {0: None,
				1: 0,
				2: 0,
				3: 3,
				4: 3,
				5: 1,
				6: 1,
				7: 2,
				8: 2}

	imgResize = cv2.resize(img, (454, 340))

	imgBackground = cv2.imread('background.png')

	predection = classifier.getPrediction(img)

	classID = predection[1]
	if classID != 0:
		imgBackground = cvzone.overlayPNG(imgBackground, imgWasteList[classID - 1], (909, 127))
		imgBackground = cvzone.overlayPNG(imgBackground, imgArrow, (978, 320))

		classIDBin = classDic[classID]

	imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[classIDBin], (895, 374))

	imgBackground[148:148 + 340, 159:159 + 454] = imgResize

	return imgBackground


def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		
		#print('upload_image filename: ' + filename)

		f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(f) 
		filename = predict_img(f)

		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

# @app.route('/<filename>')
# def send_file(filename):

#     print(filename)
#     filename = os.path.basename(filename)
    
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
	app.run(debug=True)
