import os
import argparse
from Utils import *
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--gt_poses_dir', type=str, default='./demo_data/Spherical_Markers_Default_a/obj_in_cam')
    parser.add_argument('--predicted_poses_dir', type=str, default='./demo_data/Spherical_Markers_Default_a/obj_in_cam_predictions')
    
    args = parser.parse_args()

    gt_pose_files = os.listdir(args.gt_poses_dir)
    predicted_pose_files = os.listdir(args.predicted_poses_dir)

    # Ensure files are sorted to match each other based on naming conventions
    gt_pose_files.sort()
    predicted_pose_files.sort()

    # Iterate through each pair of files
    for yaml_file, txt_file in zip(gt_pose_files, predicted_pose_files):

        # Ensure we are processing YAML files from folder1 and TXT files from folder2
        if yaml_file.endswith('.yaml') and txt_file.endswith('.txt'):
            yaml_filepath = os.path.join(args.gt_poses_dir, yaml_file)
            txt_filepath = os.path.join(args.predicted_poses_dir, txt_file)

            # Load transformation matrices from YAML file
            with open(yaml_filepath, 'r') as f:
                yaml_data = yaml.load(f)

            gt_rxx = yaml_data.get('rxx', 0.0)
            gt_rxy = yaml_data.get('rxy', 0.0)
            gt_rxz = yaml_data.get('rxz', 0.0)
            gt_ryx = yaml_data.get('ryx', 0.0)
            gt_ryy = yaml_data.get('ryy', 0.0)
            gt_ryz = yaml_data.get('ryz', 0.0)
            gt_rzx = yaml_data.get('rzx', 0.0)
            gt_rzy = yaml_data.get('rzy', 0.0)
            gt_rzz = yaml_data.get('rzz', 0.0)

            # Construct the rotation matrix
            gt_rotation_matrix = np.array([[gt_rxx, gt_rxy, gt_rxz],
                                        [gt_ryx, gt_ryy, gt_ryz],
                                        [gt_rzx, gt_rzy, gt_rzz]])
                    
            # Load transformation matrix values from TXT file
            with open(txt_filepath, 'r') as f:
                txt_data = {}
                for line in f:
                    key, value = line.split(':')
                    txt_data[key.strip()] = float(value.strip()[:-1])

            pred_rxx = txt_data.get('rxx', 0.0)
            pred_rxy = txt_data.get('rxy', 0.0)
            pred_rxz = txt_data.get('rxz', 0.0)
            pred_ryx = txt_data.get('ryx', 0.0)
            pred_ryy = txt_data.get('ryy', 0.0)
            pred_ryz = txt_data.get('ryz', 0.0)
            pred_rzx = txt_data.get('rzx', 0.0)
            pred_rzy = txt_data.get('rzy', 0.0)
            pred_rzz = txt_data.get('rzz', 0.0)

            # Construct the rotation matrix
            pred_rotation_matrix = np.array([[pred_rxx, pred_rxy, pred_rxz],
                                        [pred_ryx, pred_ryy, pred_ryz],
                                        [pred_rzx, pred_rzy, pred_rzz]])
            

            # Compare transformation matrices and print the differences
            print(f"Comparing files: {yaml_file} and {txt_file}")
            translation_keys = ['tx','ty','tz']
            for key in yaml_data:
                if key in translation_keys:
                    difference = abs(yaml_data[key] - txt_data[key]*1000)
                    print(f"{key}: {difference} mm")
            
            gt_euler_angles_list = rotation_matrix_to_euler_angles(gt_rotation_matrix)
            pred_euler_angles_list = rotation_matrix_to_euler_angles(pred_rotation_matrix)

            print(f"Rotation X: ",(abs(gt_euler_angles_list[2]) - abs({pred_euler_angles_list[2]})), "deg")
            print(f"Rotation Y: ",(abs(gt_euler_angles_list[1]) - abs({pred_euler_angles_list[1]})), "deg")
            print(f"Rotation Z: ",(abs(gt_euler_angles_list[0]) - abs({pred_euler_angles_list[0]})), "deg")
            print("\n")  # Print a newline for separation