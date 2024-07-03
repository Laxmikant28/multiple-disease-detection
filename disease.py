from flask import Flask,render_template,url_for,redirect,request
import pickle
import json
from flask_mail import Mail

with open("config.json", "r") as c:
    params = json.load(c)["params"]

disease = Flask(__name__)

disease.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = "465",
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params["gmail_password"]
)

mail = Mail(disease)

try:
    model1 = pickle.load(open("new_diabetes_model.sav", "rb"))
    model2 = pickle.load(open("new_heartDisease.sav", "rb"))
except Exception as e:
    print("error occure1111111111")

@disease.route('/')
def home():
    return render_template("home.html")

@disease.route("/diabetes")
def diabetes():
    return render_template("ddindex.html")

@disease.route("/heart")
def heart():
    return  render_template("hdindex.html")


@disease.route("/diabetes_results",methods=["GET","POST"])
def diabetes_results():
    if request.method == "POST":
        email = request.form["email"]
        Age = float(request.form["Age"])
        blood_glucose_level = float(request.form["blood_glucose_level"])
        HbA1c_level = float(request.form["HbA1c_level"])
        hypertension = int(request.form["hypertension"])
        BMI_category = request.form["BMI_category"]
        gender = request.form["gender"]
        smoking_history = request.form["smoking_history"]
        try:
            pred1 = model1.predict([[Age,blood_glucose_level,HbA1c_level,hypertension,BMI_category,gender,smoking_history]])
        except Exception as e:
            print("error occure")

        ''' Message sending '''
        ''' send Result'''
        if pred1==1:
            result = "You are Detected as Diabetes Patient...."
        else:
            result = "You rae well...."

        if 70 > blood_glucose_level:
            bgl = "Potentially Dangerous Low Blood Sugar.\nPreventative Measures:Seek immediate medical attention. This level indicates hypoglycemia, which can be life-threatening and wouldn't typically occur after eating."
        elif 141 < blood_glucose_level < 200 :
            bgl = "High Risk Blood Sugar.\nPreventative Measures:Prioritize a balanced diet with whole grains, fruits, vegetables, and lean protein.\nConsider consulting a registered dietitian or certified diabetes educator for personalized guidance."
        elif blood_glucose_level > 200:
            bgl = "Very High Risk Blood Sugar,Seek medical advice immediately.\nThis blood sugar level might indicate undiagnosed diabetes. Your doctor will recommend the most appropriate course of action, potentially including."

        if 5.7 > HbA1c_level:
            hl = "indicates a low risk of developing diabetes.."
        elif 5.7 <= HbA1c_level <= 6.4:
            hl = "suggests a higher risk of developing diabetes. Here, lifestyle changes become even more important for prevention:\nYou must maintain it below 5.7\nFocus on balanced diet and physical activity"
        elif HbA1c_level > 6.5:
            hl = "hba1c level is above 6.5 ,You have a high risk of diabetes. Consult a doctor"

        if hypertension == 1:
            ht = '''
            1.Stress management:Chronic stress can elevate blood pressure.Find healthy ways to manage stress, like yoga, meditation, or spending time in nature.\n
            2.Exercise:Regular physical activity, like brisk walking for 30 minutes most days of the week,lowers blood pressure naturally.\n
            3.Diet(Reduce salt intake):This is a big one! Aim for less than 2,300mg of sodium daily. Consider the DASH diet, which focuses on fruits, vegetables, whole grains, and low-fat dairy  all excellent for blood pressure control.'''
        else: ht = "be happy.."

        if BMI_category == "normal":
            bc=""

        if BMI_category == "underweight":
            bc='''
            1.Focus on a balanced diet:You are underweight Maintain BMI in between 18.5 to 24.9.\n
            2.While weight gain might be recommended, ensure it comes from healthy sources. Prioritize fruits, vegetables, whole grains, and lean protein.\n
            3.Discuss with your doctor:There may be underlying reasons for being underweight. Your doctor can help identify these and recommend a healthy weight gain plan.'''

        elif BMI_category == "overweight":
            bc='''You are overweight ,Maintain BMI in between 18.5 to 24.9.\nAim for gradual weight loss (1-2 lbs per week) through healthy eating and exercise.\n
            1.Increase physical activity:Regular exercise helps manage weight and improve insulin sensitivity.'''
        elif BMI_category in ["obesity class1", "obesity class2", "obesity class3"]:
            bc='''Aggressive weight loss:You are overweight ,Maintain BMI in between 18.5 to 24.9.
            1.In addition to lifestyle changes, medications or weight loss surgery might be considered under doctor's supervision.\n
            2.Blood sugar control:Regularly monitor blood sugar levels to track progress and identify any pre-diabetic signs.\n
            3.Increase physical activity:Regular exercise helps manage weight and improve insulin sensitivity.'''

        if smoking_history in ["never", "not current"]:
            sh="This is the ideal category for reducing diabetes risk."
        elif smoking_history in ["former","current","ever"]:
            sh="Quitting smoking is the single most beneficial action you can take to reduce your risk of diabetes and improve overall health.\nTalk to your doctor about resources and strategies to help you quit."


        print("Email is :",email)
        mail.send_message("Diabetes Result",sender=params["gmail_user"],recipients=[email],
                          body=f"{result}\nHere are some suggestion......\n\nblood glucose level:\n{bgl}\n\nHbA1c level:\n{hl}\n\nHypertension:\n{ht}\n\nBMI category:\n{bc}\n\nsmoking history:\n{sh}")
        return render_template("ddresult.html",result=pred1,HbA1c_level=HbA1c_level, hypertension=hypertension, BMI_category=BMI_category, blood_glucose_level=blood_glucose_level, smoking_history=smoking_history)


@disease.route("/heart_results",methods=["GET","POST"])
def heart_results():
    if request.method == "POST":
        Age = float(request.form["Age"])
        sex = request.form["sex"]
        is_smoking = request.form["is_smoking"]
        cigsPerDay = int(request.form["cigsPerDay"])
        prevalentStroke = int(request.form["prevalentStroke"])
        prevalentHyp = request.form["prevalentHyp"]
        diabetes = request.form["diabetes"]
        totChol = float(request.form["totChol"])
        sysBP = float(request.form["sysBP"])
        diaBP = float(request.form["diaBP"])
        BMI = float(request.form["BMI"])
        heartRate = float(request.form["heartRate"])
        glucose = float(request.form["glucose"])
        BPMeds = request.form["BPMeds"]
        try:
            pred2 = model2.predict([[Age,sex,is_smoking,cigsPerDay,prevalentStroke,prevalentHyp,diabetes,totChol,sysBP,diaBP,BMI,heartRate,glucose,BPMeds]])
            print(pred2)
        except Exception as e:
            print("error occure222222222")

        return render_template("hdresult.html",result=pred2,is_smoking=is_smoking,prevalentStroke=prevalentStroke,prevalentHyp=prevalentHyp,diabetes=diabetes,totChol=totChol,glucose=glucose)


if __name__ == "__main__":
    disease.run(debug=True,port=5000,use_reloader=False)
