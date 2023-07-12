from flask import *
from cvzone.ClassificationModule import Classifier
import os
import cv2
import cvzone
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'staticFiles/'

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
# app = Flask(__name__)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_img(i):

	path = 'staticFiles/'
	img = cv2.imread(i)
	cv2.imwrite(os.path.join('staticFiles/user.png'), img)
	
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

	cv2.imwrite(os.path.join('staticFiles/ans.png'), imgBackground)

	return imgBackground


@app.route('/')
def main():
	return render_template("index.html")

@app.route('/success', methods=['GET', 'POST'])
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
	
		f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		pre = predict_img(f)
		pre = os.path.join(app.config['UPLOAD_FOLDER'], 'ans.png')

		flash('Image successfully uploaded and displayed below')
		# file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'user.png'))
		return render_template('upload.html', filename=filename, pre = pre)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('staticFiles', filename=filename), code=301)

if __name__ == '__main__':
	app.run(debug=True)
