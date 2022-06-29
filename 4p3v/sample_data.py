import os
import sys

def generate(input_folder, output_file, goal_samples):
    print("generating")

    # find the number of samples
    first_eval = f"./bin/data_sampler {input_folder} 10 > {output_file}"
    print(first_eval)
    os.system(first_eval)
    with open(output_file, "r") as f:
        n_first_samples = sum(1 for line in f)
    samples = 10*goal_samples / n_first_samples

    # generate the problems
    second_eval = f"./bin/data_sampler {input_folder} {int(samples)+1} > {output_file}"
    print(second_eval)
    os.system(second_eval)
    with open(output_file, "r") as f:
        n_final_samples = sum(1 for line in f)

    # add the number of samples to the beginning of the file
    sed_eval = "sed -i '1s/^/" + str(n_final_samples) + "\\n/' " + output_file
    print(sed_eval)
    os.system(sed_eval)

    # print the result
    print(str(n_final_samples) + " p-s pairs generated")

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print("Run as:")
        print("python3 sample_data.py COLMAP_folder output_file num_samples")
        exit()
    input_folder = sys.argv[1]
    output_file = sys.argv[2]
    goal_samples = int(sys.argv[3])
    generate(input_folder, output_file, goal_samples)
