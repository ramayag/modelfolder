import PoseDetector 
import motion
import math
import more_functions
import cv2
import numpy as np
from flask_socketio import SocketIO, emit
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin
import connection_database 
import time

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
socketio = SocketIO(app, cors_allowed_origins="*")
# from connection_database import user_id

user_id = 5
path = r'C:\Users\USER\Desktop\DjangoProject\db.sqlite3'

# def set_user_id(value):      
#     global user_id  # Declare global_var as global inside the function
#     user_id = value
#     print("my_variable" + str(user_id))

detector = PoseDetector.PoseDetector()

cap = cv2.VideoCapture(0)

# r# @socketio.on('test')
# r# def handle_test(data):
def tas():
    # r# print(data)
    frame_count = 0

    # تعريف متغير مصفوفة الحركات :
    motion_in_secound_array = []
    motions_array = []
    start_time = time.time()
    while cap.isOpened():
        try :
            frame_count=frame_count+1
            if frame_count%1==0:
                # frame_count=0
                # emit('test', str("rama")+str(frame_count))
                # socketio.sleep(1)
                success, image = cap.read()
                image = cv2.flip(image,1)
                blackie = np.zeros(image.shape) # Black image
                image,blackie = detector.find_pose(image ,blackie)
                h, w = image.shape[:2]
                detector.Landmark_pos(w,h)
                more = more_functions.more_functions()
        #         if detector.results
                image = more.draw_img(image,
                            str(more.angle_between_points(detector.R_sholder, detector.R_elbow, detector.R_wrist)),
                                [100,100])
                more.draw_img(blackie,
                            str(more.angle_between_points(detector.R_sholder, detector.R_elbow, detector.R_wrist)),
                                [100,100])

        #         destance = destances(detector)
        #         diatance_sholders,diatance_wrist,distance_RSH_LW,distance_LSH_RW,distance_REL_LW,distance_LEL_RW , distance_LEL_LW,distance_REL_RW,distance_RSH_RW,distance_LSH_LW,distance_nose_RW,distance_nose_LW,distance_RSH_Nose ,distance_LSH_Nose   = destance
                #حساب المسافات لاستخدامها في القوانين

                diatance_sholders = math.dist(detector.R_sholder, detector.L_sholder)
                diatance_wrist = math.dist(detector.R_wrist, detector.L_wrist)

                distance_RSH_LW =math.dist(detector.R_wrist, detector.L_sholder)
                distance_LSH_RW =math.dist(detector.L_wrist, detector.R_sholder)

                distance_REL_LW =math.dist(detector.L_wrist, detector.R_elbow)
                distance_LEL_RW =math.dist(detector.R_wrist, detector.L_elbow)

                distance_LEL_LW =math.dist(detector.L_wrist, detector.L_elbow)
                distance_REL_RW =math.dist(detector.R_wrist, detector.R_elbow)

                distance_RSH_RW =math.dist(detector.R_wrist, detector.R_sholder)
                distance_LSH_LW =math.dist(detector.L_wrist, detector.L_sholder)

                distance_nose_RW =math.dist(detector.R_wrist, detector.Nose)
                distance_nose_LW =math.dist(detector.L_wrist, detector.Nose)

                distance_RSH_Nose =math.dist(detector.R_sholder, detector.Nose)
                distance_LSH_Nose =math.dist(detector.L_sholder, detector.Nose)


                R_Wrist_angle = more.angle_between_points(detector.R_sholder, detector.R_elbow, detector.R_wrist)
                L_Wrist_angle = more.angle_between_points(detector.L_sholder, detector.L_elbow, detector.L_wrist)

                R_sholder_angle = more.angle_between_points(detector.R_hip,detector.R_sholder, detector.R_elbow)
                L_sholder_angle = more.angle_between_points(detector.L_hip, detector.L_sholder, detector.L_elbow)

                cv2.putText(blackie,str("{:.2f}".format(R_Wrist_angle)),(detector.R_elbow[0],detector.R_elbow[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                cv2.putText(blackie,str("{:.2f}".format(L_Wrist_angle)),(detector.L_elbow[0],detector.L_elbow[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)

                cv2.putText(blackie,str("{:.2f}".format(R_sholder_angle)),(detector.R_sholder[0],detector.R_sholder[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                cv2.putText(blackie,str("{:.2f}".format(L_sholder_angle)),(detector.L_sholder[0],detector.L_sholder[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)

                cv2.putText(blackie,str("{:.2f}".format(R_Wrist_angle)),(detector.R_elbow[0],detector.R_elbow[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                cv2.putText(blackie,str("{:.2f}".format(L_Wrist_angle)),(detector.L_elbow[0],detector.L_elbow[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)

                # cv2.putText(blackie,str("{}".format(detector.L_wrist[1])),(detector.L_wrist[0],detector.L_wrist[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                # cv2.putText(blackie,str("{}".format(detector.L_sholder[1])),(detector.L_sholder[0],detector.L_sholder[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)

                # cv2.putText(blackie,str("{:.2f}".format(diatance_wrist)),(detector.L_wrist[0],detector.L_wrist[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                # cv2.putText(blackie,str("{:.2f}".format(diatance_sholders)),(150,150),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)


                cv2.putText(blackie,"*__*",(detector.R_sholder[0],0),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
                cv2.putText(blackie,"*__*",(detector.R_sholder[0],detector.R_sholder[1]),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)



                #استدعاء الاكسبيرت سيستم
                instance_of_my_class = motion.ReturnValueFact()
                engine = motion.Tree(instance_of_my_class)
                engine.set_normalize_destance(diatance_sholders)
                # var = more.turnR_L(image,detector.L_sholder,detector.R_sholder,detector.R_hip)
                var=more.turnR_L(image,detector.L_sholder,detector.R_sholder,detector.R_hip)
                _ ,outside_box = more.strike_zone(blackie,detector.L_sholder,detector.R_sholder,detector.R_wrist,detector.L_wrist,var)

                _ ,Head = more.strike_zone(blackie,detector.LEFT_EAR,detector.RIGHT_EAR,detector.R_wrist,detector.L_wrist,var)

                print ( "vaaaaaaaaaa " + str(var))
                print("the out side isisisisisisisisiiisi" + str(outside_box))

                cv2.putText(image , str(var) ,(50,450),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)


                #مكتف وعلى جنب
                engine.reset()
                engine.declare(
                     motion.angle_L_sholder(angle1=L_sholder_angle),
                     motion.angle_L_elbow(angle2=L_Wrist_angle),
                     motion.angle_R_sholder(angle3=R_sholder_angle),
                     motion.angle_R_elbow(angle4=R_Wrist_angle),
                     motion.Dist_Wrists_sholds (dist1=diatance_wrist,dist2=diatance_sholders),
                     motion.Dist_LSH_RW__LSH_LW(dist3=distance_LSH_RW,dist4=distance_LSH_LW),
                     motion.BodyPart_Lsh_Lw_x(Lsh_x_pos=detector.L_sholder[0],Lw_x_pos = detector.L_wrist[0]),
                     motion.BodyPart_Rsh_Rw_x(Rsh_x_pos=detector.R_sholder[0],Rw_x_pos = detector.R_wrist[0]),
                     motion.Dist_N_LW_LSH(dist1 = distance_nose_LW,dist2 = distance_LSH_Nose),
                     motion.Dist_N_RW_RSH(dist3 = distance_nose_RW,dist4 = distance_RSH_Nose),
                     motion.Y_LW_POS(y_lw =detector.L_wrist[1] ,y_lsh = detector.L_sholder[1]),
                     motion.Y_RW_POS(y_rw = detector.R_wrist[1],y_rsh = detector.R_sholder[1]),
                     motion.direction_type(direct = var ),
                    #  motion.BodyPart_L(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
                     motion.OUT_BOX(out = outside_box)
                     )
                engine.run()

                # engine.reset()
                # engine.declare(motion.angle_L_elbow(angle1=L_Wrist_angle),motion.angle_R_elbow(angle2=R_Wrist_angle),motion.BodyPart(Rsh_x_pos=detector.R_sholder[0],Rw_x_pos = detector.R_wrist[0]),motion.BodyPart(Lsh_x_pos=detector.L_sholder[0],Lw_x_pos = detector.L_wrist[0]),motion.direction_type(direct = var ))
                # engine.run()

                # #مكتف وعلى جنب
                # engine.reset()
                # engine.declare(motion.angle_L_sholder(angle1=L_sholder_angle),motion.angle_L_elbow(angle2=L_Wrist_angle)
                # ,motion.angle_R_sholder(angle3=R_sholder_angle),motion.angle_R_elbow(angle4=R_Wrist_angle),motion.Dist_Wrists_sholds(dist1=diatance_wrist,dist2=diatance_sholders),motion.Dist_LSH_RW__LSH_LW(dist3=distance_LSH_RW,dist4=distance_LSH_LW)
                # ,motion.direction_type(direct = var ))
                # engine.run()


                # #out side box
                # # engine.reset()
                # # engine.declare(motion.Out_Box(out = outside_box))
                # # engine.run()




                # engine.reset()
                # # hand on heap l/r
                # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),motion.BodyPart(Lsh_x_pos=detector.L_sholder[0],Lw_x_pos = detector.L_wrist[0]),motion.direction_type(direct = var ))
                # engine.run()

                # engine.reset()
                # engine.declare(motion.angle(angle1=R_sholder_angle),motion.angle(angle2=R_Wrist_angle),motion.BodyPart(Rsh_x_pos=detector.R_sholder[0],Rw_x_pos = detector.R_wrist[0]),motion.direction_type(direct = var ))
                # engine.run()

                # engine.reset()
                # #مكتف
                # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),motion.angle(angle3=R_sholder_angle),motion.angle(angle4=R_Wrist_angle),Fact(dist1=distance_REL_LW,dist2=distance_REL_RW),Fact(dist3=distance_LEL_RW,dist4=distance_LEL_LW),motion.direction_type(direct = var ))
                # engine.run()

                # engine.reset()
                # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),motion.angle(angle3=R_sholder_angle),motion.angle(angle4=R_Wrist_angle),Fact(dist1=diatance_wrist,dist2=diatance_sholders),Fact(dist3=distance_LSH_RW,dist4=distance_LSH_LW),motion.direction_type(direct = var ))
                # engine.run()

                # engine.reset()
                # #hand on head left  / right
                # # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),Fact(Fact(dist1=distance_nose_LW,dist2=distance_LSH_Nose)),motion.direction_type(direct = var ))
                # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),Fact(Y1=detector.L_wrist[1],Y2=detector.L_sholder[1]),motion.direction_type(direct = var ))

                # engine.run()

                # engine.reset()
                # engine.declare(motion.angle(angle1=R_sholder_angle),motion.angle(angle2=R_Wrist_angle),Fact(Fact(dist1=distance_nose_RW,dist2=distance_RSH_Nose)),motion.direction_type(direct = var ))
                # engine.run()


                # #استدعاء الايد على الوجه و خارج البوكس
                # engine.reset()
                # # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),motion.angle(angle3=R_sholder_angle),motion.angle(angle4=R_Wrist_angle),Fact(dist1=distance_nose_LW,dist2=distance_LSH_Nose),Fact(dist3=distance_nose_RW,dist4=distance_RSH_Nose),motion.direction_type(direct = var ))
                # engine.declare(motion.angle(angle1=L_sholder_angle),motion.angle(angle2=L_Wrist_angle),motion.angle(angle3=R_sholder_angle),motion.angle(angle4=R_Wrist_angle),Fact(dist1=distance_nose_LW,dist2=distance_LSH_Nose),Fact(dist3=distance_nose_RW,dist4=distance_RSH_Nose),
                # motion.Y_position(Y1=detector.L_wrist[1],Y2=detector.L_sholder[1]),motion.Y_position(Y4=detector.R_wrist[1],Y3=detector.R_sholder[1]),motion.direction_type(direct = var ),motion.Out_Box(out = outside_box))

                # engine.run()


                variable = engine.instance_of_my_class.my_variable

                #اضافة الحركة الى المصفوفة تبع الحركات
                try :
                    motion_in_secound_array.append(variable.name)

                    par_time = time.time()
                    partly_time = par_time - start_time

                    if int(partly_time)%1 ==0 :
                        par_time = time.time()
                        partly_time = par_time - start_time
                        general_motion = more.general_motion_in_secound(motion_in_secound_array)
                       # r # emit('test',str(general_motion))
                       # r # socketio.sleep(1)
                        print(str(partly_time) + "the motion in secound  : : : "+ str(general_motion))
                        motions_array.append(general_motion)
                        motion_in_secound_array=[]


                    if int(partly_time)%5 ==0 and prevent_repeate != int(partly_time):
                        motion_eval=more.motions_evaluations(motions_array[-5:-1])
                        print("you still on your motion for long time !!!!!!!!!!!!" + str(motion_eval))
                    prevent_repeate = int(partly_time)

                except :
                    print('error')


                cv2.putText(blackie,str(variable),(100,400),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)

                cv2.imshow("blackie", blackie)
                cv2.imshow("Image", image)
                cv2.waitKey(1)
                if not success:
                    break
            if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('×'):
                            break
        except :
            print ("error")
    cap.release()
    cv2.destroyAllWindows()


    end_time = time.time()

    elapsed_time = end_time - start_time

    connection_database.DataBase.store_vedio_cols(path ,frame_count,int(elapsed_time),1,user_id)
    print(frame_count)
    print(elapsed_time)

    #حساب التقييم لكل حركة
    motion_count = more.motions_evaluations(motions_array)
    print(motion_count)
    counter = 0
    for key, value in motion_count.items():
        if key == 'HAND_ON_HEAD' :
            counter += value
    print(counter)


    connection_database.DataBase.store_Hands_cols(path,motion_count,elapsed_time)

    # print(motion_count.get('<motion.HAND_ON_HEAD: 6>'))



if __name__ == "__main__":
    tas()
    # r# socketio.run(app, host='192.168.137.48', port=8080)
    # print("run")
    

# 192.168.1.102
