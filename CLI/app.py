import os
import sys
import cv2

from .utils import READ_PATH, SAVE_PATH, \
                   CAM_WIDTH, CAM_HEIGHT, CAM_FPS, \
                   blend, show


def run():
    file_1 = None
    file_2 = None
    alpha = 0.1
    img_img = True
    img_vid = False
    vid_vid = False
    realtime = False
    width, height = 1920, 1080
    save = False

    args_1 = ["--file1", "-f1"]
    args_2 = ["--file2", "-f2"]
    args_3 = ["--alpha", "-a"]
    args_4 = ["--img-vid", "-iv"]
    args_5 = ["--vid-vid", "--vv"]
    args_6 = ["--realtime", "-rt"]
    args_7 = ["--width", "-w"]
    args_8 = ["--height", "-h"]
    args_9 = ["--save", "-s"]

    if args_1[0] in sys.argv: file_1 = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: file_1 = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: file_2 = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: file_2 = sys.argv[sys.argv.index(args_2[1]) + 1]
    
    if args_3[0] in sys.argv: alpha = float(sys.argv[sys.argv.index(args_3[0]) + 1])
    if args_3[1] in sys.argv: alpha = float(sys.argv[sys.argv.index(args_3[1]) + 1])

    if args_4[0] in sys.argv: img_vid, img_img = True, False
    if args_4[1] in sys.argv: img_vid, img_img = True, False

    if args_5[0] in sys.argv: vid_vid, img_img = True, False
    if args_5[1] in sys.argv: vid_vid, img_img = True, False

    if args_6[0] in sys.argv: realtime, img_img = True, False
    if args_6[1] in sys.argv: realtime, img_img = True, False

    if args_7[0] in sys.argv: width = int(sys.argv[sys.argv.index(args_7[0]) + 1])
    if args_7[1] in sys.argv: width = int(sys.argv[sys.argv.index(args_7[1]) + 1])

    if args_8[0] in sys.argv: height = int(sys.argv[sys.argv.index(args_8[0]) + 1])
    if args_8[1] in sys.argv: height = int(sys.argv[sys.argv.index(args_8[1]) + 1])

    if args_9[0] in sys.argv: save = True
    if args_9[1] in sys.argv: save = True

    assert file_1 is not None, "Enter Argument for (--file1 | -f1)"
    assert file_1 in os.listdir(READ_PATH), "File 1 Not Found"

    assert not (img_vid and img_img), "Fatal Error"
    assert not (img_vid and vid_vid), "Fatal Error"
    assert not (img_vid and realtime), "Fatal Error"
    assert not (vid_vid and img_img), "Fatal Error"
    assert not (vid_vid and realtime), "Fatal Error"
    assert not (realtime and img_img), "Fatal Error"

    if img_img:
        assert file_2 is not None, "Enter Argument for (--file2 | -f2)"
        assert file_2 in os.listdir(READ_PATH), "File 2 Not Found"


        image_1 = cv2.resize(src=cv2.imread(os.path.join(READ_PATH, file_1), cv2.IMREAD_COLOR), dsize=(width, height), interpolation=cv2.INTER_AREA)
        image_2 = cv2.resize(src=cv2.imread(os.path.join(READ_PATH, file_2), cv2.IMREAD_COLOR), dsize=(width, height), interpolation=cv2.INTER_AREA)
        image = cv2.addWeighted(image_1, alpha, image_2, 1-alpha, 0)

        if save:
            cv2.imwrite(os.path.join(SAVE_PATH, "Processed.jpg"), image)
        else:
            show(cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB))
    
    if img_vid:
        assert file_2 is not None, "Enter Argument for (--file2 | -f2)"
        assert file_2 in os.listdir(READ_PATH), "File 2 Not Found"

        cap = cv2.VideoCapture(os.path.join(READ_PATH, file_2))

        is_resize_w = True
        is_resize_h = True

        if args_7[0] not in sys.argv and args_7[1] not in sys.argv: 
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            is_resize_w = False
        if args_8[0] not in sys.argv and args_8[1] not in sys.argv: 
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            is_resize_h = False
        
        width = int(width)
        height = int(height)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        image = cv2.resize(src=cv2.imread(os.path.join(READ_PATH, file_1), cv2.IMREAD_COLOR), dsize=(width, height), interpolation=cv2.INTER_AREA)

        if save:
            out = cv2.VideoWriter(os.path.join(SAVE_PATH, "Processed.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                if is_resize_w or is_resize_h:
                    frame = cv2.resize(src=frame, dsize=(width, height), interpolation=cv2.INTER_AREA)
                frame = cv2.addWeighted(image, alpha, frame, 1-alpha, 0)
                if save:
                    out.write(frame)
                else:
                    cv2.imshow("Feed", frame)
                if cv2.waitKey(1) == ord("q"):
                    break
            else:
                if save:
                    break
                else:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
        cap.release()
        if save:
            out.release()
        cv2.destroyAllWindows()
