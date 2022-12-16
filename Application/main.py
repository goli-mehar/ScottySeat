from cv_class import *
import sys
import time 
def main():
    
    print("Creating new CV engine instance using roomconf file")
    roomconf = str(sys.argv[1])
    cv_engine = CV(roomconf)
    print("Engine successfully created")

    b = False
    total = 0
    window_title = "YOLO Frames"
    window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    total_time = time.time()
    read_time_total = 0
    preproc_time_total = 0
    postinfer_time_total = 0
    postproc_time_total = 0
    total_time = 0

    while total < 100:
        print(total)
        cv_engine.camera.set(cv2.CAP_PROP_POS_MSEC, (CV.CYCLE_PERIOD*250*total))
        start_time = time.time()
        img = cv_engine.camera.read()[1][..., ::-1] #Read in new image
        capture_time = time.time()
        img = cv_engine.preprocess(img) #Preprocess image
        preproc_time = time.time()
        out = cv_engine.model(img) #Run image through model
        postinfer_time = time.time()

        #bboxes = cv_engine.convert_xyxytoxywh(out, img.shape) #convert bbox dim
        
        cv_engine.samples += [out] #Add to temporary sample list

        #Once we reach samples required for an update
        if len(cv_engine.samples) >= CV.SAMPLES_PER_UPDATE:
            #print(bboxes)

            #threshold images for confidence and correct perspective
            bboxes, full_sample = cv_engine.get_highest_confidence_image()
            #full_sample.show()
            bboxes = cv_engine.convert_xyxytoxywh(bboxes, (img.shape[0], img.shape[1])) #convert bbox dim
            #bboxes = cv_engine.correct_perspective(bboxes)

            #correct perspective and send to server
            occupancy = cv_engine.calculate_occupancy(bboxes)
            #cv_engine.send_to_server(occupancy)

            #reset samples
            cv_engine.samples = []
        end_time = time.time()
        total += 1
        read_time_total += capture_time - start_time
        preproc_time_total += preproc_time - capture_time
        postinfer_time_total += postinfer_time - preproc_time
        postproc_time_total += end_time - postinfer_time
        total_time += end_time - start_time
        
        #time.sleep(CV.CYCLE_PERIOD)
    
    print("Results")
    print("Read Time: ", read_time_total/total)
    print("Preproc Time: ", preproc_time_total/total)
    print("Postinfer Time: ", postinfer_time_total/total)
    print("Postproc Time: ", postproc_time_total/total)
    print("Total Time: ", total_time/total)

main()




