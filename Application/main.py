from cv_class import *

def main():

    print("Creating new CV engine instance using roomconf file")
    cv_engine = CV()

    print("Engine successfully created")

    b = False
    while True:

        img = cv_engine.camera.read()[1][..., ::-1] #Read in new image
        img = cv_engine.preprocess(img) #Preprocess image
        out = cv_engine.model(img, size=640) #Run image through model
        bboxes = cv_engine.convert_xyxytoxywh(out, img.shape) #convert bbox dim
        
        cv_engine.samples += [bboxes] #Add to temporary sample list

        #Once we reach samples required for an update
        if len(cv_engine.samples) >= CV.SAMPLES_PER_UPDATE:
            print(bboxes)

            #threshold images for confidence and correct perspective
            #bboxes = cv_engine.get_highest_confidence_image()
            #bboxes = cv_engine.correct_perspective(bboxes)

            #calculate occupancy and send to server
            occupancy = cv_engine.calculate_occupancy(bboxes)
            print(occupancy)
            cv_engine.send_to_server(occupancy)

            #reset samples
            cv_engine.samples = []
        time.sleep(CV.CYCLE_PERIOD-2)

main()




