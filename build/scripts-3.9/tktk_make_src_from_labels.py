#!python

import argparse
import json
import numpy as np
import itk


def main():
    print(args)

    labels=itk.imread(args.labels)
    labels_np = itk.array_from_image(labels)

    labels_json = open(args.json).read()
    labels_json = json.loads(labels_json)

    src=np.zeros((labels_np.shape))

    for lbl,act in labels_json.items():
        src[labels_np==int(lbl)]=act

    src_itk=itk.image_from_array(src)
    src_itk.SetSpacing(labels.GetSpacing())
    src_itk.SetOrigin(labels.GetOrigin())
    src_itk.SetDirection(labels.GetDirection())
    itk.imwrite(src_itk,args.output)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels")
    parser.add_argument("--json", help="json that assigns to each label (1,2,3...) a level of activity")
    parser.add_argument("--output")
    args = parser.parse_args()

    main()
