import xml.etree.ElementTree as ET
from os.path import join

# res_dir = "./results/MPLight-tr0-grid3x3-0-mplight-pressure"
res_dir = "./results/IDQN-tr0-grid3x3-0-drq_norm-wait_norm"
total_episodes = 100

for episode in range(2, total_episodes + 1):
    print(f"Episode {episode}/{total_episodes}")
    waiting_time = []
    time_loss = []
    file_path = join(res_dir, f"tripinfo_{episode}.xml")
    # print(file_path)
    root = ET.parse(file_path).getroot()
    for trip in root:
        waiting_time.append(float(trip.get('waitingTime')))
        time_loss.append(float(trip.get('timeLoss')))

    avg_waiting_time = sum(waiting_time) / len(waiting_time)
    avg_time_loss = sum(time_loss) / len(time_loss)

    print(f"\tAverage waiting time: {avg_waiting_time}, average time loss: {avg_time_loss}")
