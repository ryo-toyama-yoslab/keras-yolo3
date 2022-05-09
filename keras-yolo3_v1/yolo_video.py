import sys
import argparse
import pathlib
import os
import glob
from yolo import YOLO, detect_video
from PIL import Image

def detect_file(yolo):
    while True:
        files = glob.glob('.\\img_file\\*.jpg')
        for f in files:
            #print("for文開始")
            try:#mAP-master/input/
                image = Image.open(f)
                name = os.path.splitext(os.path.basename(f))[0]
                img_path = './mAP-master/input/detection-results/' + name + ".txt"
                #img_path = './detection-results/result_name.txt'
                f = open(img_path, 'a')
                f.write("")
                f.close()
                print(name)
                #print("ファイル作成終了")
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image2(image, img_path)
                """
                r_image.show()
                r_image.save('result.jpg')
                global label_list
                label_list = yolo.get_label_name()
                for i in range(len(label_list)):
                    print(label_list[i]) 
                count_check = 1
                """
            #print("認識１回終了")
        break
    yolo.close_session()

FLAGS = None


if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )

    parser.add_argument(
        "--file", nargs='?', type=str,required=False,default='./path_img_file',
        help='Image file input path'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    
    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "file" in FLAGS:
        detect_file(YOLO(**vars(FLAGS)))
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
    
    '''
    elif "file" in FLAGS:
        detect_file(YOLO(**vars(FLAGS)))
    '''