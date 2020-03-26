import argparse
import os.path as osp
import glob
from mmaction.datasets.utils import (parse_directory,
                                     parse_ucf101_splits,
                                     parse_kinetics_splits,
                                     build_split_list)

#更改 frame path和format
def parse_args():
    parser = argparse.ArgumentParser(description='Build file list')
    parser.add_argument('--dataset', type=str, default='ucf101',choices=[
                        'ucf101', 'kinetics400'])
    parser.add_argument('--frame_path', type=str, default='/data/DataSets/UCF101/rawframes',
    # parser.add_argument('--frame_path', type=str, default='/data/DataSets/UCF101/flows',
    # parser.add_argument('--frame_path', type=str, default='/data/DataSets/UCF101/UCF-101',
                        help='root directory for the frames')
    parser.add_argument('--rgb_prefix', type=str, default='img_')
    parser.add_argument('--flow_x_prefix', type=str, default='flow_x_')
    parser.add_argument('--flow_y_prefix', type=str, default='flow_y_')
    parser.add_argument('--num_split', type=int, default=3)
    parser.add_argument('--subset', type=str, default='train',
                        choices=['train', 'val', 'test'])
    parser.add_argument('--level', type=int, default=2, choices=[1, 2])
    parser.add_argument('--format', type=str,
                        default='rawframes', choices=['rawframes', 'videos'])
                        # default='videos', choices=['rawframes', 'videos'])
    parser.add_argument('--out_list_path', type=str, default='/data/codes/mmaction/data/')
    parser.add_argument('--shuffle', action='store_true', default=True)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    if args.level == 2:
        def key_func(x): return '/'.join(x.split('/')[-2:])
    else:
        def key_func(x): return x.split('/')[-1]

    if args.format == 'rawframes':
        frame_info = parse_directory(args.frame_path,
                                     key_func=key_func,
                                     rgb_prefix=args.rgb_prefix,
                                     flow_x_prefix=args.flow_x_prefix,
                                     flow_y_prefix=args.flow_y_prefix,
                                     level=args.level)
    else:
        if args.level == 1:
            video_list = glob.glob(osp.join(args.frame_path, '*'))
        elif args.level == 2:
            video_list = glob.glob(osp.join(args.frame_path, '*', '*'))
        frame_info = {osp.relpath(
            x.split('.')[0], args.frame_path): (x, -1, -1) for x in video_list}

    if args.dataset == 'ucf101':
        split_tp = parse_ucf101_splits(args.level)
    elif args.dataset == 'kinetics400':
        split_tp = parse_kinetics_splits(args.level)
    assert len(split_tp) == args.num_split

    out_path = args.out_list_path + args.dataset
    if len(split_tp) > 1:
        for i, split in enumerate(split_tp):
            lists = build_split_list(split_tp[i], frame_info,
                                     shuffle=args.shuffle) # list[0]是rgb信息， list[1]是光流信息
            # 信息主要是关于video name，num_frames, class 的一个大树组
            filename = '{}_train_split_{}_{}.txt'.format(args.dataset,
                                                         i + 1, args.format)
            with open(osp.join(out_path, filename), 'w') as f:
                f.writelines(lists[0][0])
            filename = '{}_val_split_{}_{}.txt'.format(args.dataset,
                                                       i + 1, args.format)
            with open(osp.join(out_path, filename), 'w') as f:
                f.writelines(lists[0][1])
    else:
        lists = build_split_list(split_tp[0], frame_info,
                                 shuffle=args.shuffle)
        filename = '{}_{}_list_{}.txt'.format(args.dataset,
                                              args.subset,
                                              args.format)
        if args.subset == 'train':
            ind = 0
        elif args.subset == 'val':
            ind = 1
        elif args.subset == 'test':
            ind = 2
        with open(osp.join(out_path, filename), 'w') as f:
            f.writelines(lists[0][ind])


if __name__ == "__main__":
    main()
