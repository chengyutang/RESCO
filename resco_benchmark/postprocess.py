import os
from xml.etree import ElementTree
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--root-dir", type=str)

args = parser.parse_args()
root_dir = args.root_dir

for mode in ["train", "test"]:
    for sub in os.listdir(root_dir):
        if not sub.isdigit():
            continue
        filenames = []
        for fname in os.listdir(os.path.join(root_dir, sub, mode)):
            if fname.startswith("tripinfo"):
                filenames.append(os.path.join(root_dir, sub, mode, fname))
        filenames.sort(key=lambda x: int(x.split(".")[0].split("_")[-1]))
        csv_file = open(os.path.join(root_dir, sub, mode, "results.csv"), "w")
        if mode == "test":
            csv_file.write("episode,waiting_time,time_loss,CO2,CO,PMx,fuel\n")
        else:
            csv_file.write("episode,waiting_time,time_loss\n")
        for fname in filenames:
            episode = fname.split(".")[0].split("_")[-1]
            root = ElementTree.parse(fname).getroot()
            total_waiting_time = 0
            total_time_loss = 0
            total_co2 = 0
            total_co = 0
            total_pmx = 0
            total_fuel = 0
            num_vehicles = 0
            for vehicle in root:
                num_vehicles += 1
                total_waiting_time += float(vehicle.attrib["waitingTime"])
                total_time_loss += float(vehicle.attrib["timeLoss"])
                if mode == "test":
                    total_co2 += float(vehicle[0].attrib["CO2_abs"])
                    total_co += float(vehicle[0].attrib["CO_abs"])
                    total_pmx += float(vehicle[0].attrib["PMx_abs"])
                    total_fuel += float(vehicle[0].attrib["fuel_abs"])
            if mode == "test":
                csv_file.write(f"{episode},{total_waiting_time / num_vehicles},{total_time_loss / num_vehicles},{total_co2 / num_vehicles},{total_co / num_vehicles},{total_pmx / num_vehicles},{total_fuel / num_vehicles}\n")
            else:
                csv_file.write(f"{episode},{total_waiting_time / num_vehicles},{total_time_loss / num_vehicles}\n")
        for fname in filenames:
            os.remove(fname)
        csv_file.close()
